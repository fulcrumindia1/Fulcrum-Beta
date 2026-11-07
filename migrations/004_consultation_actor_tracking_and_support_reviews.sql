-- ============================================================================
-- MIGRATION: 004_consultation_actor_tracking_and_support_reviews.sql
-- TYPE: Safe Additive (Non-Destructive)
-- PURPOSE: Adds actor attribution columns to help_requests and scheme review table
-- ============================================================================

-- 1. Add interaction actor tracking to help_requests (if not already present)
ALTER TABLE public.help_requests 
ADD COLUMN IF NOT EXISTS last_interaction_actor_id UUID REFERENCES public.profiles(id),
ADD COLUMN IF NOT EXISTS last_interaction_actor_role TEXT,
ADD COLUMN IF NOT EXISTS last_mentor_response_at TIMESTAMPTZ,
ADD COLUMN IF NOT EXISTS last_aspirant_response_at TIMESTAMPTZ;

-- 2. Add Scheme Support Review Request table for Guide -> Admin Human-in-the-Loop review
CREATE TABLE IF NOT EXISTS public.scheme_support_reviews (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aspirant_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    scheme_id TEXT NOT NULL REFERENCES public.schemes(id) ON DELETE CASCADE,
    guide_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    match_score INTEGER NOT NULL,
    guide_justification TEXT NOT NULL,
    failed_criteria TEXT[] DEFAULT '{}',
    missing_criteria TEXT[] DEFAULT '{}',
    status TEXT NOT NULL DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'APPROVED', 'REJECTED')),
    admin_decision_notes TEXT,
    reviewed_by UUID REFERENCES public.profiles(id),
    reviewed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT uq_scheme_review UNIQUE (aspirant_id, scheme_id, guide_id)
);

CREATE INDEX IF NOT EXISTS idx_ssr_status ON public.scheme_support_reviews(status);
CREATE INDEX IF NOT EXISTS idx_ssr_aspirant ON public.scheme_support_reviews(aspirant_id);
CREATE INDEX IF NOT EXISTS idx_ssr_guide ON public.scheme_support_reviews(guide_id);

-- 3. Row Level Security (RLS)
ALTER TABLE public.scheme_support_reviews ENABLE ROW LEVEL SECURITY;

DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies 
        WHERE tablename = 'scheme_support_reviews' AND policyname = 'scheme_reviews_admin_all'
    ) THEN
        CREATE POLICY "scheme_reviews_admin_all" ON public.scheme_support_reviews
            FOR ALL TO authenticated
            USING (EXISTS (SELECT 1 FROM public.profiles WHERE id = auth.uid() AND role = 'admin'))
            WITH CHECK (EXISTS (SELECT 1 FROM public.profiles WHERE id = auth.uid() AND role = 'admin'));
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_policies 
        WHERE tablename = 'scheme_support_reviews' AND policyname = 'scheme_reviews_guide_insert'
    ) THEN
        CREATE POLICY "scheme_reviews_guide_insert" ON public.scheme_support_reviews
            FOR INSERT TO authenticated
            WITH CHECK (auth.uid() = guide_id);
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_policies 
        WHERE tablename = 'scheme_support_reviews' AND policyname = 'scheme_reviews_guide_select'
    ) THEN
        CREATE POLICY "scheme_reviews_guide_select" ON public.scheme_support_reviews
            FOR SELECT TO authenticated
            USING (auth.uid() = guide_id);
    END IF;
END $$;

-- 4. Reload PostgREST schema cache
NOTIFY pgrst, 'reload schema';

