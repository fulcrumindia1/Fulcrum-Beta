-- =============================================================================
-- Migration 010: Align Account Lifecycle Columns (Bridge Live & 009 Schema)
-- =============================================================================
-- Ensures both legacy live columns (status_reason, archived_at, restored_at,
-- reactivated_at, old_status, details) and Migration 009 columns (lifecycle_reason,
-- status_updated_at, status_updated_by, deletion_requested_by, retention_notes,
-- previous_status, metadata) exist idempotently on profiles and
-- account_lifecycle_log without overwriting existing records or Admin identity.
-- =============================================================================

ALTER TABLE IF EXISTS public.profiles
    ADD COLUMN IF NOT EXISTS account_status TEXT NOT NULL DEFAULT 'ACTIVE',
    ADD COLUMN IF NOT EXISTS status_reason TEXT,
    ADD COLUMN IF NOT EXISTS lifecycle_reason TEXT,
    ADD COLUMN IF NOT EXISTS status_updated_at TIMESTAMPTZ DEFAULT now(),
    ADD COLUMN IF NOT EXISTS status_updated_by UUID,
    ADD COLUMN IF NOT EXISTS archived_at TIMESTAMPTZ,
    ADD COLUMN IF NOT EXISTS restored_at TIMESTAMPTZ,
    ADD COLUMN IF NOT EXISTS reactivated_at TIMESTAMPTZ,
    ADD COLUMN IF NOT EXISTS deletion_requested_at TIMESTAMPTZ,
    ADD COLUMN IF NOT EXISTS deletion_requested_by UUID,
    ADD COLUMN IF NOT EXISTS deletion_scheduled_for TIMESTAMPTZ,
    ADD COLUMN IF NOT EXISTS legal_hold BOOLEAN NOT NULL DEFAULT false,
    ADD COLUMN IF NOT EXISTS retention_notes TEXT;

ALTER TABLE IF EXISTS public.account_lifecycle_log
    ADD COLUMN IF NOT EXISTS old_status TEXT,
    ADD COLUMN IF NOT EXISTS previous_status TEXT,
    ADD COLUMN IF NOT EXISTS details JSONB NOT NULL DEFAULT '{}'::jsonb,
    ADD COLUMN IF NOT EXISTS metadata JSONB NOT NULL DEFAULT '{}'::jsonb;

-- Backfill dual-schema aliases only where one side is populated and the other is empty
UPDATE public.profiles
SET lifecycle_reason = COALESCE(lifecycle_reason, status_reason),
    status_reason = COALESCE(status_reason, lifecycle_reason)
WHERE (lifecycle_reason IS NULL AND status_reason IS NOT NULL)
   OR (status_reason IS NULL AND lifecycle_reason IS NOT NULL);

UPDATE public.account_lifecycle_log
SET previous_status = COALESCE(previous_status, old_status),
    old_status = COALESCE(old_status, previous_status),
    metadata = CASE WHEN metadata = '{}'::jsonb THEN details ELSE metadata END,
    details = CASE WHEN details = '{}'::jsonb THEN metadata ELSE details END;

