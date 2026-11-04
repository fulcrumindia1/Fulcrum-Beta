-- =============================================================================
-- FULCRUM-INDIA: Migration 001 — Multi-Role Architecture, Legal Terms & NDA, 
-- Administrative Scopes, Complaints, Conflicts & Case Collaboration
-- =============================================================================
-- Non-destructive additive migration. Safe to run idempotently on Supabase PostgreSQL.

-- 1. USER ROLES (Multi-Role Support: One Identity, Multiple Roles)
CREATE TABLE IF NOT EXISTS public.user_roles (
    id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id           UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    role              TEXT NOT NULL CHECK (role IN ('aspirant', 'guide', 'sme', 'admin', 'district_admin', 'operational_admin')),
    status            TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'pending_nda', 'suspended', 'revoked')),
    granted_by        UUID REFERENCES public.profiles(id),
    granted_at        TIMESTAMPTZ DEFAULT NOW(),
    activated_at      TIMESTAMPTZ,
    suspended_at      TIMESTAMPTZ,
    revoked_at        TIMESTAMPTZ,
    revocation_reason TEXT,
    created_at        TIMESTAMPTZ DEFAULT NOW(),
    updated_at        TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT uq_user_role UNIQUE (user_id, role)
);

CREATE INDEX IF NOT EXISTS idx_user_roles_user_id ON public.user_roles(user_id);
CREATE INDEX IF NOT EXISTS idx_user_roles_role_status ON public.user_roles(role, status);

-- 2. LEGAL DOCUMENTS (Version-Controlled Terms & Conditions and NDAs)
CREATE TABLE IF NOT EXISTS public.legal_documents (
    id             TEXT PRIMARY KEY,
    doc_type       TEXT NOT NULL CHECK (doc_type IN ('terms_and_conditions', 'nda_guide', 'nda_sme', 'nda_dual')),
    version        TEXT NOT NULL,
    title          TEXT NOT NULL,
    content        TEXT NOT NULL,
    content_hash   TEXT NOT NULL,
    roles_covered  JSONB DEFAULT '[]'::jsonb,
    effective_date DATE DEFAULT CURRENT_DATE,
    is_mandatory   BOOLEAN DEFAULT TRUE,
    is_active      BOOLEAN DEFAULT TRUE,
    created_at     TIMESTAMPTZ DEFAULT NOW()
);

-- 3. LEGAL ACCEPTANCES (Immutable Audit Trail for Terms and NDA Signatures)
CREATE TABLE IF NOT EXISTS public.legal_acceptances (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id                 UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    document_id             TEXT NOT NULL,
    doc_type                TEXT NOT NULL,
    doc_version             TEXT NOT NULL,
    doc_hash                TEXT NOT NULL,
    user_email_snapshot     TEXT NOT NULL,
    typed_legal_name        TEXT NOT NULL,
    typed_acceptance_phrase TEXT NOT NULL,
    checkbox_confirmed      BOOLEAN DEFAULT TRUE,
    roles_covered           JSONB DEFAULT '[]'::jsonb,
    ip_address              TEXT,
    user_agent              TEXT,
    status                  TEXT DEFAULT 'ACCEPTED',
    accepted_at             TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_legal_acceptances_user ON public.legal_acceptances(user_id, doc_type);

-- 4. CONFIDENTIAL GUIDE COMPLAINTS
CREATE TABLE IF NOT EXISTS public.guide_complaints (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aspirant_id      UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    guide_id         UUID NOT NULL REFERENCES public.profiles(id),
    reason           TEXT NOT NULL CHECK (reason IN ('inactivity', 'poor_communication', 'conflict_of_interest', 'professional_conduct', 'other')),
    details          TEXT,
    status           TEXT DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'UNDER_REVIEW', 'RESOLVED', 'DISMISSED')),
    resolution_notes TEXT,
    resolved_by      UUID REFERENCES public.profiles(id),
    resolved_at      TIMESTAMPTZ,
    created_at       TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_guide_complaints_aspirant ON public.guide_complaints(aspirant_id);
CREATE INDEX IF NOT EXISTS idx_guide_complaints_status ON public.guide_complaints(status);

-- 5. SME CONFLICT OF INTEREST DECLARATIONS
CREATE TABLE IF NOT EXISTS public.sme_conflict_declarations (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sme_id           UUID NOT NULL REFERENCES public.profiles(id),
    aspirant_id      UUID NOT NULL REFERENCES public.profiles(id),
    has_conflict     BOOLEAN DEFAULT FALSE,
    conflict_details TEXT,
    status           TEXT DEFAULT 'DECLARED' CHECK (status IN ('DECLARED', 'APPROVED', 'REJECTED')),
    reviewed_by      UUID REFERENCES public.profiles(id),
    reviewed_at      TIMESTAMPTZ,
    created_at       TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_sme_conflict_sme_asp ON public.sme_conflict_declarations(sme_id, aspirant_id);

-- 6. CASE COLLABORATION & DISCUSSIONS
CREATE TABLE IF NOT EXISTS public.case_discussions (
    id                     UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aspirant_id            UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    author_id              UUID NOT NULL REFERENCES public.profiles(id),
    author_role            TEXT NOT NULL,
    title                  TEXT NOT NULL,
    message                TEXT NOT NULL,
    attachments            JSONB DEFAULT '[]'::jsonb,
    is_private_mentor_note BOOLEAN DEFAULT FALSE,
    created_at             TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_case_discussions_aspirant ON public.case_discussions(aspirant_id);

-- 7. INACTIVITY LOGS (Deduplication for Day 7, 10, 14 Alerts)
CREATE TABLE IF NOT EXISTS public.inactivity_logs (
    id                   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    relationship_id      UUID,
    guide_id             UUID NOT NULL REFERENCES public.profiles(id),
    aspirant_id          UUID NOT NULL REFERENCES public.profiles(id),
    days_inactive        INTEGER NOT NULL,
    escalation_stage     TEXT NOT NULL CHECK (escalation_stage IN ('DAY_7_REMINDER', 'DAY_10_ADMIN_ALERT', 'DAY_14_ADMIN_REVIEW')),
    notification_sent_at TIMESTAMPTZ DEFAULT NOW(),
    created_at           TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT uq_inactivity_stage UNIQUE (guide_id, aspirant_id, escalation_stage)
);

-- 8. INITIAL LEGAL DOCUMENTS SEED (Approved Templates for Terms & Conditions and Master NDA)
INSERT INTO public.legal_documents (id, doc_type, version, title, content, content_hash, roles_covered, effective_date, is_mandatory, is_active)
VALUES 
(
    'terms_v1_0',
    'terms_and_conditions',
    '1.0.0',
    'Fulcrum-India Platform Terms & Conditions',
    'FULCRUM-INDIA PLATFORM TERMS & CONDITIONS\nVersion 1.0.0 — Effective Date: 2026-09-01\n\n1. PURPOSE & SCOPE\nFulcrum-India is an enterprise guidance operating system designed to assist entrepreneurs in Tamil Nadu and India by coordinating mentorship, journey documentation, and funding scheme intelligence.\n\n2. USER CONDUCT & ACCURACY OF DATA\nEntrepreneurs, Guides, Subject Matter Experts (SMEs), and Administrators agree to provide accurate, up-to-date venture information and respect intellectual property.\n\n3. SCHEME RECOMMENDATIONS & DISCLAIMER\nScheme matching scores and recommendations are strictly indicative ("Recommended" or "Potentially Eligible") based on deterministic algorithms and do not constitute a legal grant guarantee or financial approval.\n\n4. PRIVACY & DATA GOVERNANCE\nUser profile data is protected under institutional governance and Row Level Security. Data is shared with designated Guides and SMEs solely for authorized advisory engagements.\n\n5. TERMINATION & MODIFICATION\nAdministration reserves the right to suspend accounts violating professional ethics or confidentiality agreements.',
    'b8c9d2e1f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1',
    '["aspirant", "guide", "sme", "admin"]'::jsonb,
    '2026-09-01',
    TRUE,
    TRUE
),
(
    'nda_dual_v1_0',
    'nda_dual',
    '1.0.0',
    'Fulcrum-India Confidentiality & Non-Disclosure Agreement (Guide & SME)',
    'FULCRUM-INDIA CONFIDENTIALITY & NON-DISCLOSURE AGREEMENT (NDA)\nFor Certified Guides and Domain Subject Matter Experts (SMEs)\nVersion 1.0.0 — Effective Date: 2026-09-01\n\n1. CONFIDENTIAL INFORMATION\nAs an institutional mentor (Guide) or specialist advisory consultant (SME), you will receive access to proprietary business plans, financial projections, GST details, trade secrets, intellectual property, private journey events, and funding strategies of grassroots entrepreneurs.\n\n2. MANDATORY CONFIDENTIALITY OBLIGATION\nYou agree to maintain strict confidentiality of all entrepreneur information. You shall not disclose, copy, distribute, commercialize, or use any entrepreneur data for any purpose other than providing authorized guidance through Fulcrum-India.\n\n3. CONFLICT OF INTEREST\nYou must promptly disclose any commercial, financial, or personal interest in an entrepreneur''s venture or direct competitors before engaging in advisory consults.\n\n4. NON-CIRCUMVENTION\nYou shall not independently solicit, contract, or transact with assigned entrepreneurs outside the governing framework of Fulcrum-India without prior administrative approval.\n\n5. REMEDIES & GOVERNING LAW\nBreach of this agreement shall result in immediate revocation of mentor privileges and may result in legal remedies under the Indian Contract Act, 1872 and Information Technology Act, 2000.',
    'c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8',
    '["guide", "sme"]'::jsonb,
    '2026-09-01',
    TRUE,
    TRUE
)
ON CONFLICT (id) DO UPDATE SET 
    title = EXCLUDED.title,
    content = EXCLUDED.content,
    content_hash = EXCLUDED.content_hash,
    roles_covered = EXCLUDED.roles_covered,
    is_active = EXCLUDED.is_active;

-- 9. SEED INITIAL ROLES FROM PROFILES (Backfill existing users into user_roles)
INSERT INTO public.user_roles (user_id, role, status, granted_at, activated_at)
SELECT id, role, 'active', created_at, created_at
FROM public.profiles
ON CONFLICT (user_id, role) DO NOTHING;

-- Ensure every existing user also retains their base 'aspirant' role grant
INSERT INTO public.user_roles (user_id, role, status, granted_at, activated_at)
SELECT id, 'aspirant', 'active', created_at, created_at
FROM public.profiles
WHERE role != 'aspirant'
ON CONFLICT (user_id, role) DO NOTHING;

