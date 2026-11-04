-- =============================================================================
-- FULCRUM-INDIA: Migration 002 — Journey Event Revisions & Immutable Audit Log
-- =============================================================================
CREATE TABLE IF NOT EXISTS public.journey_event_revisions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    journey_event_id UUID NOT NULL REFERENCES public.journey_events(id) ON DELETE CASCADE,
    editor_id UUID NOT NULL REFERENCES public.profiles(id),
    editor_role TEXT NOT NULL,
    previous_data JSONB NOT NULL DEFAULT '{}'::jsonb,
    new_data JSONB NOT NULL DEFAULT '{}'::jsonb,
    revision_number INTEGER NOT NULL DEFAULT 1,
    change_reason TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_journey_event_revisions_event ON public.journey_event_revisions(journey_event_id);
CREATE INDEX IF NOT EXISTS idx_journey_event_revisions_editor ON public.journey_event_revisions(editor_id);

ALTER TABLE public.journey_event_revisions ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Admin full access journey_event_revisions" ON public.journey_event_revisions;
CREATE POLICY "Admin full access journey_event_revisions" ON public.journey_event_revisions
    FOR ALL TO authenticated USING (public.is_admin());

DROP POLICY IF EXISTS "Users read related journey_event_revisions" ON public.journey_event_revisions;
CREATE POLICY "Users read related journey_event_revisions" ON public.journey_event_revisions
    FOR SELECT TO authenticated USING (
        editor_id = auth.uid() OR public.is_admin()
    );
