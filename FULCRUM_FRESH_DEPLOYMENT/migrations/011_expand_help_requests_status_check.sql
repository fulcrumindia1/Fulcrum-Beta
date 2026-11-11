-- ============================================================================
-- MIGRATION: 011_expand_help_requests_status_check.sql
-- TYPE: Safe Additive / Constraint Expansion (Idempotent)
-- PURPOSE: Expand public.help_requests.help_requests_status_check to allow
--          bidirectional waiting statuses used across Guide/SME/Aspirant/SLA
--          workflows ('WAITING_ON_ASPIRANT', 'WAITING_ON_GUIDE_SME',
--          'ACTION_REQUIRED', 'REPLIED') alongside existing statuses.
-- ============================================================================

DO $$
BEGIN
    ALTER TABLE public.help_requests
        DROP CONSTRAINT IF EXISTS help_requests_status_check;

    ALTER TABLE public.help_requests
        ADD CONSTRAINT help_requests_status_check
        CHECK (status IN (
            'OPEN',
            'IN_PROGRESS',
            'WAITING_ON_ASPIRANT',
            'WAITING_ON_GUIDE_SME',
            'ACTION_REQUIRED',
            'REPLIED',
            'RESOLVED',
            'ESCALATED',
            'PENDING_ADMIN',
            'DIRECTIVE_ISSUED'
        ));
END $$;

NOTIFY pgrst, 'reload schema';
