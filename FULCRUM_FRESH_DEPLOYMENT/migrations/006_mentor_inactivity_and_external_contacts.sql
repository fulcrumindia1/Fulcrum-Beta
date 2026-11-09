-- =============================================================================
-- FULCRUM-BETA: MIGRATION 006 — GUIDE + SME INACTIVITY & EXTERNAL CONTACT AUDIT
-- =============================================================================
-- Summary:
-- 1. Extends public.inactivity_logs to support Domain SMEs, co-guides, and
--    inactivity episode tracking without duplicate alert suppression.
-- 2. Creates public.external_contact_logs to audit manual WhatsApp & Gmail
--    outreach to Guides, SMEs, and Aspirants from Fulcrum Support.
-- 3. Enables Row Level Security (RLS) restricting external contact logs to Admin.
-- 4. Reloads PostgREST schema cache.
-- =============================================================================

-- 1. Extend inactivity_logs for Mentor Role and Inactivity Episodes
ALTER TABLE public.inactivity_logs
ADD COLUMN IF NOT EXISTS mentor_id UUID REFERENCES public.profiles(id),
ADD COLUMN IF NOT EXISTS mentor_role TEXT NOT NULL DEFAULT 'guide',
ADD COLUMN IF NOT EXISTS inactivity_episode TEXT,
ADD COLUMN IF NOT EXISTS status TEXT NOT NULL DEFAULT 'ACTIVE',
ADD COLUMN IF NOT EXISTS follow_up_channel TEXT,
ADD COLUMN IF NOT EXISTS follow_up_sent_at TIMESTAMPTZ,
ADD COLUMN IF NOT EXISTS follow_up_notes TEXT;

-- Backfill legacy records
UPDATE public.inactivity_logs
SET mentor_id = guide_id,
    mentor_role = 'guide',
    status = 'HISTORICAL'
WHERE mentor_id IS NULL;

-- Drop legacy guide-only unique constraint if present to allow subsequent episodes
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'uq_inactivity_stage'
          AND conrelid = 'public.inactivity_logs'::regclass
    ) THEN
        ALTER TABLE public.inactivity_logs DROP CONSTRAINT uq_inactivity_stage;
    END IF;
END $$;

-- Add episode-aware unique index (prevents duplicates in the SAME episode, allows new episodes)
CREATE UNIQUE INDEX IF NOT EXISTS uq_inactivity_episode_stage
ON public.inactivity_logs (mentor_id, aspirant_id, mentor_role, inactivity_episode, escalation_stage)
WHERE inactivity_episode IS NOT NULL;

-- Add indexes for performance
CREATE INDEX IF NOT EXISTS idx_inactivity_mentor ON public.inactivity_logs(mentor_id);
CREATE INDEX IF NOT EXISTS idx_inactivity_role ON public.inactivity_logs(mentor_role);
CREATE INDEX IF NOT EXISTS idx_inactivity_status ON public.inactivity_logs(status);

-- 2. Create external_contact_logs Table
CREATE TABLE IF NOT EXISTS public.external_contact_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    admin_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    recipient_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    recipient_role TEXT NOT NULL CHECK (recipient_role IN ('guide', 'sme', 'aspirant')),
    aspirant_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    inactivity_record_id UUID REFERENCES public.inactivity_logs(id) ON DELETE SET NULL,
    channel TEXT NOT NULL CHECK (channel IN ('whatsapp', 'email')),
    purpose TEXT DEFAULT 'General check-in',
    status TEXT NOT NULL DEFAULT 'SENT_CONFIRMED' CHECK (status IN ('DRAFT_OPENED', 'SENT_CONFIRMED', 'ACKNOWLEDGED')),
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Performance Indexes
CREATE INDEX IF NOT EXISTS idx_ext_contact_recipient ON public.external_contact_logs(recipient_id);
CREATE INDEX IF NOT EXISTS idx_ext_contact_aspirant ON public.external_contact_logs(aspirant_id);
CREATE INDEX IF NOT EXISTS idx_ext_contact_admin ON public.external_contact_logs(admin_id);
CREATE INDEX IF NOT EXISTS idx_ext_contact_inactivity ON public.external_contact_logs(inactivity_record_id);

-- 3. Row Level Security (RLS)
ALTER TABLE public.external_contact_logs ENABLE ROW LEVEL SECURITY;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies 
        WHERE tablename = 'external_contact_logs' 
        AND policyname = 'Admin full access external_contact_logs'
    ) THEN
        CREATE POLICY "Admin full access external_contact_logs" 
        ON public.external_contact_logs
        FOR ALL TO authenticated 
        USING (public.is_admin());
    END IF;
END $$;

-- 4. Reload PostgREST schema cache
NOTIFY pgrst, 'reload schema';

