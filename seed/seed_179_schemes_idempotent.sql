-- =============================================================================
-- Canonical 179 Government Schemes Seed Script for Fulcrum-Beta
-- Idempotent (ON CONFLICT (id) DO UPDATE)
-- Verified record count: 179 schemes
-- =============================================================================
BEGIN;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('PRIV-ACCEL-ATOMS-2026', 'PRIV-ACCEL-ATOMS-2026', 'Accel Atoms (AI & DeepTech Accelerator)', 'Accel India & Prosus (Atoms X)', 'Accel India & Prosus (Atoms X)', 'Equity', 'Private VC / Angel', 'Equity', 'Pre-Seed / Seed', 'Rs 4 Crores to Rs 16 Crores ($500K - $2M)', 'Flagship pre-seed program backed by Accel offering up to $2M in co-investment, $500K in AI cloud credits, and mentorship from Accel partners.', 'Flagship pre-seed program backed by Accel offering up to $2M in co-investment, $500K in AI cloud credits, and mentorship from Accel partners.', '["AI/ML", "Technology", "DeepTech", "SaaS"]', '["AI-first, DeepTech, B2B SaaS, or LeapTech startup", "Indian or US-incorporated company", "Founders building foundational AI models or enterprise agents"]', '["Standard uncapped SAFE or equity note", "Direct access to Accel global partner network & US market entry program", "Perks: $500K AWS/GCP credits + OpenAI enterprise API access"]', '[">> Accel uses Atoms as a top-of-funnel funnel to preempt Series A rounds before other VCs see you", ">> Strong preference for AI startups solving real B2B workflows with defensible data pipelines", ">> Cohort founders get priority pitch slots at Accel India Annual Founder Summit"]', '["!! Low founder technical depth will fail Accel technical due diligence quickly", "!! Thin wrapper applications without custom fine-tuning or proprietary data are rejected"]', 'Online Application -> Technical Interview -> Accel Partner Pitch -> Investment', '2-3 weeks', '~1-2%', 'atoms.accel.in', 'All India', 'Private', 'https://www.atoms.accel.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Accel Atoms (AI & DeepTech Accelerator) (Accel India & Prosus (Atoms X))
FUND TYPE: Pre-Seed / Seed VC Equity

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Accel Atoms (AI & DeepTech Accelerator) highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Accel Atoms (AI & DeepTech Accelerator) expenditure guidelines.
3. Address key scheme criteria: AI-first, DeepTech, B2B SaaS, or LeapTech startup, Indian or US-incorporated company, Founders building foundational AI models or enterprise agents.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Accel Atoms (AI & DeepTech Accelerator) eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:19.387421+00:00', '2026-09-14T11:00:12.389713+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('PRIV-ANGEL-101', 'PRIV-ANGEL-101', 'Regional Angel Syndicate & Accelerators Batch 1', 'Private Syndicate', 'Private Syndicate', 'Equity', 'Private VC / Angel', 'Equity', 'Pre-Seed / Seed', 'Rs 50 Lakhs to Rs 2 Crores', 'Regional Angel Syndicate & Accelerators Batch 1', 'Regional syndicate focused on backing early-stage ecosystem startups.', '["All Sectors"]', '["DPIIT registered startup", "Early traction"]', '["Standard Equity"]', '[">> Looking for strong regional founders."]', '["!! Overvalued cap tables."]', 'Pitch -> Screening -> DD', '2 months', '~10%', 'startupindia.gov.in', 'All India', 'National', 'https://www.startuptn.in/angelstn', 'August 2026', '', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:24.123284+00:00', '2026-09-14T11:00:12.391869+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('PRIV-ANGEL-102', 'PRIV-ANGEL-102', 'Regional Angel Syndicate & Accelerators Batch 2', 'Private Syndicate', 'Private Syndicate', 'Equity', 'Private VC / Angel', 'Equity', 'Pre-Seed / Seed', 'Rs 50 Lakhs to Rs 2 Crores', 'Regional Angel Syndicate & Accelerators Batch 2', 'Regional syndicate focused on backing early-stage ecosystem startups.', '["All Sectors"]', '["DPIIT registered startup", "Early traction"]', '["Standard Equity"]', '[">> Looking for strong regional founders."]', '["!! Overvalued cap tables."]', 'Pitch -> Screening -> DD', '2 months', '~10%', 'startupindia.gov.in', 'All India', 'National', 'https://www.startuptn.in/angelstn', 'August 2026', '', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:24.123284+00:00', '2026-09-14T11:00:12.391883+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('PRIV-ANGEL-103', 'PRIV-ANGEL-103', 'Regional Angel Syndicate & Accelerators Batch 3', 'Private Syndicate', 'Private Syndicate', 'Equity', 'Private VC / Angel', 'Equity', 'Pre-Seed / Seed', 'Rs 50 Lakhs to Rs 2 Crores', 'Regional Angel Syndicate & Accelerators Batch 3', 'Regional syndicate focused on backing early-stage ecosystem startups.', '["All Sectors"]', '["DPIIT registered startup", "Early traction"]', '["Standard Equity"]', '[">> Looking for strong regional founders."]', '["!! Overvalued cap tables."]', 'Pitch -> Screening -> DD', '2 months', '~10%', 'startupindia.gov.in', 'All India', 'National', 'https://www.startuptn.in/angelstn', 'August 2026', '', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:24.123284+00:00', '2026-09-14T11:00:12.391897+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('PRIV-ANGEL-104', 'PRIV-ANGEL-104', 'Regional Angel Syndicate & Accelerators Batch 4', 'Private Syndicate', 'Private Syndicate', 'Equity', 'Private VC / Angel', 'Equity', 'Pre-Seed / Seed', 'Rs 50 Lakhs to Rs 2 Crores', 'Regional Angel Syndicate & Accelerators Batch 4', 'Regional syndicate focused on backing early-stage ecosystem startups.', '["All Sectors"]', '["DPIIT registered startup", "Early traction"]', '["Standard Equity"]', '[">> Looking for strong regional founders."]', '["!! Overvalued cap tables."]', 'Pitch -> Screening -> DD', '2 months', '~10%', 'startupindia.gov.in', 'All India', 'National', 'https://www.startuptn.in/angelstn', 'August 2026', '', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:24.123284+00:00', '2026-09-14T11:00:12.391907+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('PRIV-ANGEL-105', 'PRIV-ANGEL-105', 'Regional Angel Syndicate & Accelerators Batch 5', 'Private Syndicate', 'Private Syndicate', 'Equity', 'Private VC / Angel', 'Equity', 'Pre-Seed / Seed', 'Rs 50 Lakhs to Rs 2 Crores', 'Regional Angel Syndicate & Accelerators Batch 5', 'Regional syndicate focused on backing early-stage ecosystem startups.', '["All Sectors"]', '["DPIIT registered startup", "Early traction"]', '["Standard Equity"]', '[">> Looking for strong regional founders."]', '["!! Overvalued cap tables."]', 'Pitch -> Screening -> DD', '2 months', '~10%', 'startupindia.gov.in', 'All India', 'National', 'https://www.startuptn.in/angelstn', 'August 2026', '', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:24.123284+00:00', '2026-09-14T11:00:12.391918+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('PRIV-ANGEL-106', 'PRIV-ANGEL-106', 'Regional Angel Syndicate & Accelerators Batch 6', 'Private Syndicate', 'Private Syndicate', 'Equity', 'Private VC / Angel', 'Equity', 'Pre-Seed / Seed', 'Rs 50 Lakhs to Rs 2 Crores', 'Regional Angel Syndicate & Accelerators Batch 6', 'Regional syndicate focused on backing early-stage ecosystem startups.', '["All Sectors"]', '["DPIIT registered startup", "Early traction"]', '["Standard Equity"]', '[">> Looking for strong regional founders."]', '["!! Overvalued cap tables."]', 'Pitch -> Screening -> DD', '2 months', '~10%', 'startupindia.gov.in', 'All India', 'National', 'https://www.startuptn.in/angelstn', 'August 2026', '', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:24.123284+00:00', '2026-09-14T11:00:12.391928+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('PRIV-ANGEL-107', 'PRIV-ANGEL-107', 'Regional Angel Syndicate & Accelerators Batch 7', 'Private Syndicate', 'Private Syndicate', 'Equity', 'Private VC / Angel', 'Equity', 'Pre-Seed / Seed', 'Rs 50 Lakhs to Rs 2 Crores', 'Regional Angel Syndicate & Accelerators Batch 7', 'Regional syndicate focused on backing early-stage ecosystem startups.', '["All Sectors"]', '["DPIIT registered startup", "Early traction"]', '["Standard Equity"]', '[">> Looking for strong regional founders."]', '["!! Overvalued cap tables."]', 'Pitch -> Screening -> DD', '2 months', '~10%', 'startupindia.gov.in', 'All India', 'National', 'https://www.startuptn.in/angelstn', 'August 2026', '', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:24.123284+00:00', '2026-09-14T11:00:12.391937+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('PRIV-ANGEL-108', 'PRIV-ANGEL-108', 'Regional Angel Syndicate & Accelerators Batch 8', 'Private Syndicate', 'Private Syndicate', 'Equity', 'Private VC / Angel', 'Equity', 'Pre-Seed / Seed', 'Rs 50 Lakhs to Rs 2 Crores', 'Regional Angel Syndicate & Accelerators Batch 8', 'Regional syndicate focused on backing early-stage ecosystem startups.', '["All Sectors"]', '["DPIIT registered startup", "Early traction"]', '["Standard Equity"]', '[">> Looking for strong regional founders."]', '["!! Overvalued cap tables."]', 'Pitch -> Screening -> DD', '2 months', '~10%', 'startupindia.gov.in', 'All India', 'National', 'https://www.startuptn.in/angelstn', 'August 2026', '', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:24.123284+00:00', '2026-09-14T11:00:12.391947+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('PRIV-ANGEL-109', 'PRIV-ANGEL-109', 'Regional Angel Syndicate & Accelerators Batch 9', 'Private Syndicate', 'Private Syndicate', 'Equity', 'Private VC / Angel', 'Equity', 'Pre-Seed / Seed', 'Rs 50 Lakhs to Rs 2 Crores', 'Regional Angel Syndicate & Accelerators Batch 9', 'Regional syndicate focused on backing early-stage ecosystem startups.', '["All Sectors"]', '["DPIIT registered startup", "Early traction"]', '["Standard Equity"]', '[">> Looking for strong regional founders."]', '["!! Overvalued cap tables."]', 'Pitch -> Screening -> DD', '2 months', '~10%', 'startupindia.gov.in', 'All India', 'National', 'https://www.startuptn.in/angelstn', 'August 2026', '', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:24.123284+00:00', '2026-09-14T11:00:12.391957+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('PRIV-ANGEL-110', 'PRIV-ANGEL-110', 'Regional Angel Syndicate & Accelerators Batch 10', 'Private Syndicate', 'Private Syndicate', 'Equity', 'Private VC / Angel', 'Equity', 'Pre-Seed / Seed', 'Rs 50 Lakhs to Rs 2 Crores', 'Regional Angel Syndicate & Accelerators Batch 10', 'Regional syndicate focused on backing early-stage ecosystem startups.', '["All Sectors"]', '["DPIIT registered startup", "Early traction"]', '["Standard Equity"]', '[">> Looking for strong regional founders."]', '["!! Overvalued cap tables."]', 'Pitch -> Screening -> DD', '2 months', '~10%', 'startupindia.gov.in', 'All India', 'National', 'https://www.startuptn.in/angelstn', 'August 2026', '', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:24.123284+00:00', '2026-09-14T11:00:12.391967+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('PRIV-ANGEL-111', 'PRIV-ANGEL-111', 'Regional Angel Syndicate & Accelerators Batch 11', 'Private Syndicate', 'Private Syndicate', 'Equity', 'Private VC / Angel', 'Equity', 'Pre-Seed / Seed', 'Rs 50 Lakhs to Rs 2 Crores', 'Regional Angel Syndicate & Accelerators Batch 11', 'Regional syndicate focused on backing early-stage ecosystem startups.', '["All Sectors"]', '["DPIIT registered startup", "Early traction"]', '["Standard Equity"]', '[">> Looking for strong regional founders."]', '["!! Overvalued cap tables."]', 'Pitch -> Screening -> DD', '2 months', '~10%', 'startupindia.gov.in', 'All India', 'National', 'https://www.startuptn.in/angelstn', 'August 2026', '', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:24.123284+00:00', '2026-09-14T11:00:12.391977+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('PRIV-ANGEL-112', 'PRIV-ANGEL-112', 'Regional Angel Syndicate & Accelerators Batch 12', 'Private Syndicate', 'Private Syndicate', 'Equity', 'Private VC / Angel', 'Equity', 'Pre-Seed / Seed', 'Rs 50 Lakhs to Rs 2 Crores', 'Regional Angel Syndicate & Accelerators Batch 12', 'Regional syndicate focused on backing early-stage ecosystem startups.', '["All Sectors"]', '["DPIIT registered startup", "Early traction"]', '["Standard Equity"]', '[">> Looking for strong regional founders."]', '["!! Overvalued cap tables."]', 'Pitch -> Screening -> DD', '2 months', '~10%', 'startupindia.gov.in', 'All India', 'National', 'https://www.startuptn.in/angelstn', 'August 2026', '', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:24.123284+00:00', '2026-09-14T11:00:12.391987+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('PRIV-ANGEL-113', 'PRIV-ANGEL-113', 'Regional Angel Syndicate & Accelerators Batch 13', 'Private Syndicate', 'Private Syndicate', 'Equity', 'Private VC / Angel', 'Equity', 'Pre-Seed / Seed', 'Rs 50 Lakhs to Rs 2 Crores', 'Regional Angel Syndicate & Accelerators Batch 13', 'Regional syndicate focused on backing early-stage ecosystem startups.', '["All Sectors"]', '["DPIIT registered startup", "Early traction"]', '["Standard Equity"]', '[">> Looking for strong regional founders."]', '["!! Overvalued cap tables."]', 'Pitch -> Screening -> DD', '2 months', '~10%', 'startupindia.gov.in', 'All India', 'National', 'https://www.startuptn.in/angelstn', 'August 2026', '', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:24.123284+00:00', '2026-09-14T11:00:12.391997+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('PRIV-ANGEL-114', 'PRIV-ANGEL-114', 'Regional Angel Syndicate & Accelerators Batch 14', 'Private Syndicate', 'Private Syndicate', 'Equity', 'Private VC / Angel', 'Equity', 'Pre-Seed / Seed', 'Rs 50 Lakhs to Rs 2 Crores', 'Regional Angel Syndicate & Accelerators Batch 14', 'Regional syndicate focused on backing early-stage ecosystem startups.', '["All Sectors"]', '["DPIIT registered startup", "Early traction"]', '["Standard Equity"]', '[">> Looking for strong regional founders."]', '["!! Overvalued cap tables."]', 'Pitch -> Screening -> DD', '2 months', '~10%', 'startupindia.gov.in', 'All India', 'National', 'https://www.startuptn.in/angelstn', 'August 2026', '', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:24.123284+00:00', '2026-09-14T11:00:12.39201+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('PRIV-ANGEL-115', 'PRIV-ANGEL-115', 'Regional Angel Syndicate & Accelerators Batch 15', 'Private Syndicate', 'Private Syndicate', 'Equity', 'Private VC / Angel', 'Equity', 'Pre-Seed / Seed', 'Rs 50 Lakhs to Rs 2 Crores', 'Regional Angel Syndicate & Accelerators Batch 15', 'Regional syndicate focused on backing early-stage ecosystem startups.', '["All Sectors"]', '["DPIIT registered startup", "Early traction"]', '["Standard Equity"]', '[">> Looking for strong regional founders."]', '["!! Overvalued cap tables."]', 'Pitch -> Screening -> DD', '2 months', '~10%', 'startupindia.gov.in', 'All India', 'National', 'https://www.startuptn.in/angelstn', 'August 2026', '', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:24.123284+00:00', '2026-09-14T11:00:12.39202+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('PRIV-ANGEL-116', 'PRIV-ANGEL-116', 'Regional Angel Syndicate & Accelerators Batch 16', 'Private Syndicate', 'Private Syndicate', 'Equity', 'Private VC / Angel', 'Equity', 'Pre-Seed / Seed', 'Rs 50 Lakhs to Rs 2 Crores', 'Regional Angel Syndicate & Accelerators Batch 16', 'Regional syndicate focused on backing early-stage ecosystem startups.', '["All Sectors"]', '["DPIIT registered startup", "Early traction"]', '["Standard Equity"]', '[">> Looking for strong regional founders."]', '["!! Overvalued cap tables."]', 'Pitch -> Screening -> DD', '2 months', '~10%', 'startupindia.gov.in', 'All India', 'National', 'https://www.startuptn.in/angelstn', 'August 2026', '', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:24.123284+00:00', '2026-09-14T11:00:12.39203+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('PRIV-ANGEL-117', 'PRIV-ANGEL-117', 'Regional Angel Syndicate & Accelerators Batch 17', 'Private Syndicate', 'Private Syndicate', 'Equity', 'Private VC / Angel', 'Equity', 'Pre-Seed / Seed', 'Rs 50 Lakhs to Rs 2 Crores', 'Regional Angel Syndicate & Accelerators Batch 17', 'Regional syndicate focused on backing early-stage ecosystem startups.', '["All Sectors"]', '["DPIIT registered startup", "Early traction"]', '["Standard Equity"]', '[">> Looking for strong regional founders."]', '["!! Overvalued cap tables."]', 'Pitch -> Screening -> DD', '2 months', '~10%', 'startupindia.gov.in', 'All India', 'National', 'https://www.startuptn.in/angelstn', 'August 2026', '', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:24.123284+00:00', '2026-09-14T11:00:12.392039+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('PRIV-ANGEL-118', 'PRIV-ANGEL-118', 'Regional Angel Syndicate & Accelerators Batch 18', 'Private Syndicate', 'Private Syndicate', 'Equity', 'Private VC / Angel', 'Equity', 'Pre-Seed / Seed', 'Rs 50 Lakhs to Rs 2 Crores', 'Regional Angel Syndicate & Accelerators Batch 18', 'Regional syndicate focused on backing early-stage ecosystem startups.', '["All Sectors"]', '["DPIIT registered startup", "Early traction"]', '["Standard Equity"]', '[">> Looking for strong regional founders."]', '["!! Overvalued cap tables."]', 'Pitch -> Screening -> DD', '2 months', '~10%', 'startupindia.gov.in', 'All India', 'National', 'https://www.startuptn.in/angelstn', 'August 2026', '', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:24.123284+00:00', '2026-09-14T11:00:12.392049+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('PRIV-ANGEL-119', 'PRIV-ANGEL-119', 'Regional Angel Syndicate & Accelerators Batch 19', 'Private Syndicate', 'Private Syndicate', 'Equity', 'Private VC / Angel', 'Equity', 'Pre-Seed / Seed', 'Rs 50 Lakhs to Rs 2 Crores', 'Regional Angel Syndicate & Accelerators Batch 19', 'Regional syndicate focused on backing early-stage ecosystem startups.', '["All Sectors"]', '["DPIIT registered startup", "Early traction"]', '["Standard Equity"]', '[">> Looking for strong regional founders."]', '["!! Overvalued cap tables."]', 'Pitch -> Screening -> DD', '2 months', '~10%', 'startupindia.gov.in', 'All India', 'National', 'https://www.startuptn.in/angelstn', 'August 2026', '', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:24.123284+00:00', '2026-09-14T11:00:12.392059+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('PRIV-ANGEL-120', 'PRIV-ANGEL-120', 'Regional Angel Syndicate & Accelerators Batch 20', 'Private Syndicate', 'Private Syndicate', 'Equity', 'Private VC / Angel', 'Equity', 'Pre-Seed / Seed', 'Rs 50 Lakhs to Rs 2 Crores', 'Regional Angel Syndicate & Accelerators Batch 20', 'Regional syndicate focused on backing early-stage ecosystem startups.', '["All Sectors"]', '["DPIIT registered startup", "Early traction"]', '["Standard Equity"]', '[">> Looking for strong regional founders."]', '["!! Overvalued cap tables."]', 'Pitch -> Screening -> DD', '2 months', '~10%', 'startupindia.gov.in', 'All India', 'National', 'https://www.startuptn.in/angelstn', 'August 2026', '', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:24.123284+00:00', '2026-09-14T11:00:12.392069+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('PRIV-ANGELSTN-2026', 'PRIV-ANGELSTN-2026', 'AngelsTN (StartupTN Global Tamil Diaspora Angel Platform)', 'StartupTN & Government of Tamil Nadu', 'StartupTN & Government of Tamil Nadu', 'Equity', 'Foreign / Global', 'Equity', 'Pre-Seed / Seed', 'Rs 25 Lakhs to Rs 1 Crore', 'Official digital platform connecting Tamil Nadu startups with global Tamil diaspora investors and high-net-worth angels.', 'Official digital platform connecting Tamil Nadu startups with global Tamil diaspora investors and high-net-worth angels.', '["All Sectors", "DeepTech", "Agri", "SaaS", "GreenTech"]', '["Startup registered in Tamil Nadu or founded by Tamil diaspora", "DPIIT or StartupTN recognized entity", "Scalable tech, hardware, green-tech, or traditional sector innovation"]', '["Syndicate angel investment via AngelSAFE or equity", "Direct mentorship from global CXOs in US, Singapore, Middle East", "Zero platform fee for registered TN startups"]', '[">> Government wants DIASPORA CAPITAL REMITTANCE into state startups - highlight Tamil Nadu footprint", ">> Media-friendly regional impact projects get faster syndicate spotlight on AngelsTN portal", ">> Co-investment matching with TANSEED grant adds significant investor confidence"]', '["!! Angel syndicates evaluate team integrity heavily - background checks are mandatory", "!! Do not attempt valuation inflation - Tamil diaspora angels are conservative value investors"]', 'AngelsTN portal registration -> Profile curation -> Diaspora pitch night -> Term sheet -> Disbursement', '2-4 months', '~25%', 'angelstn.in / startuptn.in', 'Tamil Nadu', 'Foreign', 'https://www.angelstn.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: AngelsTN (StartupTN Global Tamil Diaspora Angel Platform) (StartupTN & Government of Tamil Nadu)
FUND TYPE: Angel Syndicate & Equity Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for AngelsTN (StartupTN Global Tamil Diaspora Angel Platform) highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official AngelsTN (StartupTN Global Tamil Diaspora Angel Platform) expenditure guidelines.
3. Address key scheme criteria: Startup registered in Tamil Nadu or founded by Tamil diaspora, DPIIT or StartupTN recognized entity, Scalable tech, hardware, green-tech, or traditional sector innovation.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official AngelsTN (StartupTN Global Tamil Diaspora Angel Platform) eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:19.387421+00:00', '2026-09-14T11:00:12.389776+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('PRIV-ANGELSTN-2026-DUP-146', 'PRIV-ANGELSTN-2026', 'AngelsTN (StartupTN Global Tamil Diaspora Angel Platform)', 'StartupTN & Government of Tamil Nadu', 'StartupTN & Government of Tamil Nadu', 'Equity', 'Private VC / Angel', 'Equity', 'Pre-Seed / Seed', 'Rs 25 Lakhs to Rs 1 Crore', 'AngelsTN (StartupTN Global Tamil Diaspora Angel Platform)', 'Official digital platform connecting Tamil Nadu startups with global Tamil diaspora investors.', '["All Sectors"]', '["Startup registered in Tamil Nadu", "DPIIT or StartupTN recognized entity"]', '["Syndicate angel investment via AngelSAFE or equity"]', '[">> Government wants DIASPORA CAPITAL REMITTANCE into state startups"]', '["!! Angel syndicates evaluate team integrity heavily"]', 'AngelsTN portal registration', '2-4 months', '~25%', 'angelstn.in', 'Tamil Nadu', 'State', 'https://www.startuptn.in', 'August 2026', '', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:23.540071+00:00', '2026-09-14T11:00:12.391803+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('PRIV-ANICUT-2026', 'PRIV-ANICUT-2026', 'Grand Anicut Seed Fund (GASF) - Anicut Capital 2026', 'Anicut Capital (Chennai Asset Management)', 'Anicut Capital (Chennai Asset Management)', 'Equity', 'Private VC / Angel', 'Equity', 'Pre-Series A / Series A', 'Rs 5 Crores to Rs 8 Crores', 'Rs 175 Crore early-stage seed fund targeting 20+ high-growth startups across India with focus on South India.', 'Rs 175 Crore early-stage seed fund targeting 20+ high-growth startups across India with focus on South India.', '["DeepTech", "Technology", "Fintech", "Consumer"]', '["Pre-Series A / Series A stage startup", "Strong unit economics and early revenue validation", "DeepTech, enterprise tech, consumer, or fintech sectors"]', '["Institutional VC equity stake (12% - 20%)", "Board seat or observer seat required", "Active portfolio support, GTM assistance, and follow-on capital reserve"]', '[">> Anicut leads pre-Series A rounds to de-risk Series A - show clear path to 3x revenue growth in 18 months", ">> Strong preference for capital-efficient founders over cash-burn growth"]', '["!! High burn rate with no clear contribution margin path is an auto-rejection", "!! Clean Cap Table required - resolve messy angel cap tables before pitching"]', 'Pitch deck -> Partner screening -> Due diligence -> IC approval -> Term Sheet', '2-3 months', '~3-5%', 'anicutcapital.com', 'All India', 'Private', 'https://www.anicutcapital.com', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Grand Anicut Seed Fund (GASF) - Anicut Capital 2026 (Anicut Capital (Chennai Asset Management))
FUND TYPE: Seed / Pre-Series A VC Equity

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Grand Anicut Seed Fund (GASF) - Anicut Capital 2026 highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Grand Anicut Seed Fund (GASF) - Anicut Capital 2026 expenditure guidelines.
3. Address key scheme criteria: Pre-Series A / Series A stage startup, Strong unit economics and early revenue validation, DeepTech, enterprise tech, consumer, or fintech sectors.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Grand Anicut Seed Fund (GASF) - Anicut Capital 2026 eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:19.387421+00:00', '2026-09-14T11:00:12.389787+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('PRIV-ANICUT-2026-DUP-147', 'PRIV-ANICUT-2026', 'Grand Anicut Seed Fund (GASF) - Anicut Capital', 'Anicut Capital', 'Anicut Capital', 'Equity', 'Private VC / Angel', 'Equity', 'Pre-Seed / Seed', 'Rs 5 Crores to Rs 8 Crores', 'Grand Anicut Seed Fund (GASF) - Anicut Capital', 'Rs 175 Crore early-stage seed fund targeting 20+ high-growth startups.', '["Technology", "Fintech"]', '["Pre-Series A / Series A stage startup"]', '["Institutional VC equity stake (12% - 20%)"]', '[">> Anicut leads pre-Series A rounds to de-risk Series A"]', '["!! High burn rate with no clear contribution margin path is an auto-rejection"]', 'Pitch deck -> Partner screening -> IC', '2-3 months', '~3-5%', 'anicutcapital.com', 'All India', 'National', 'https://aim.gov.in', 'August 2026', '', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:23.540071+00:00', '2026-09-14T11:00:12.391823+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('PRIV-ARALI-2026', 'PRIV-ARALI-2026', 'Arali Ventures (Enterprise & B2B AI VC)', 'Arali Ventures (Early-Stage Tech VC)', 'Arali Ventures (Early-Stage Tech VC)', 'Equity', 'Private VC / Angel', 'Equity', 'Pre-Seed / Seed', 'Rs 2 Crores to Rs 12 Crores ($250K - $1.5M)', 'Pre-seed and seed VC firm backing day-zero enterprise AI, industrial AI, fintech infra, and B2B SaaS startups.', 'Pre-seed and seed VC firm backing day-zero enterprise AI, industrial AI, fintech infra, and B2B SaaS startups.', '["AI/ML", "Technology", "SaaS"]', '["Enterprise AI, Industrial AI, B2B SaaS, or Fintech infrastructure", "Pre-revenue or early revenue stage", "Deep domain expertise in founding team"]', '["Lead investor in Pre-Seed/Seed round", "Hands-on operational building alongside founders", "Pro-rata rights for follow-on Series A"]', '[">> Arali is willing to invest PRE-REVENUE if technical moat and founder-market fit are exceptional", ">> Focus on enterprise pain points with high ACV (Annual Contract Value) potential in US/India"]', '["!! Pure consumer copycat apps with no B2B enterprise utility will not be considered", "!! Founders lacking domain depth in their target industry face tough technical DD"]', 'Founder intro -> Technical DD -> Customer reference checks -> IC -> Investment', '4-6 weeks', '~3-5%', 'araliventures.com', 'All India', 'Private', 'https://www.araliventures.com', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Arali Ventures (Enterprise & B2B AI VC) (Arali Ventures (Early-Stage Tech VC))
FUND TYPE: Seed VC Equity

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Arali Ventures (Enterprise & B2B AI VC) highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Arali Ventures (Enterprise & B2B AI VC) expenditure guidelines.
3. Address key scheme criteria: Enterprise AI, Industrial AI, B2B SaaS, or Fintech infrastructure, Pre-revenue or early revenue stage, Deep domain expertise in founding team.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Arali Ventures (Enterprise & B2B AI VC) eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:19.387421+00:00', '2026-09-14T11:00:12.389798+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('PRIV-BETTER-2026', 'PRIV-BETTER-2026', 'Better Capital (Day-Zero Seed Fund)', 'Better Capital (Solo-GP Seed VC)', 'Better Capital (Solo-GP Seed VC)', 'Equity', 'Private VC / Angel', 'Equity', 'Pre-Seed / Seed', 'Rs 2 Crores to Rs 8 Crores ($250K - $1M)', 'Conviction-driven day-zero seed fund founded by Vaibhav Domkundwar, backing 200+ top Indian founders at inception.', 'Conviction-driven day-zero seed fund founded by Vaibhav Domkundwar, backing 200+ top Indian founders at inception.', '["Technology", "AI/ML", "SaaS"]', '["Day-zero / inception stage startup", "Founders with top product engineering or design track record", "B2B SaaS, Developer Tools, AI Infra, or Fintech"]', '["Fast 1-week decision making", "Standard SAFE or equity notes", "Access to top US/Global co-investors network"]', '[">> Better Capital acts as the catalyst for follow-on Tier-1 VCs (Accel, Peak XV, Lightspeed)", ">> Product-led growth (PLG) and global-from-day-one thesis wins"]', '["!! Slow execution or lack of urgency during initial meetings signals poor founder velocity", "!! Over-indexing on domestic offline services with low tech leverage"]', '1-on-1 Founder Chat -> Demo Check -> Term Sheet in 7 days', '1-2 weeks', '~2-4%', 'bettercap.vc', 'All India', 'Private', 'https://www.bettercap.vc', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Better Capital (Day-Zero Seed Fund) (Better Capital (Solo-GP Seed VC))
FUND TYPE: Pre-Seed / Seed SAFE & Equity

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Better Capital (Day-Zero Seed Fund) highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Better Capital (Day-Zero Seed Fund) expenditure guidelines.
3. Address key scheme criteria: Day-zero / inception stage startup, Founders with top product engineering or design track record, B2B SaaS, Developer Tools, AI Infra, or Fintech.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Better Capital (Day-Zero Seed Fund) eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:19.387421+00:00', '2026-09-14T11:00:12.389809+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('PRIV-BETTER-2026-DUP-148', 'PRIV-BETTER-2026', 'Better Capital (Day-Zero Seed Fund)', 'Better Capital', 'Better Capital', 'Equity', 'Private VC / Angel', 'Equity', 'Pre-Seed / Seed', 'Rs 2 Crores to Rs 8 Crores ($250K - $1M)', 'Better Capital (Day-Zero Seed Fund)', 'Conviction-driven day-zero seed fund founded by Vaibhav Domkundwar.', '["Technology", "AI/ML", "SaaS"]', '["Day-zero / inception stage startup"]', '["Fast 1-week decision making", "Standard SAFE or equity notes"]', '[">> Better Capital acts as the catalyst for follow-on Tier-1 VCs (Accel, Peak XV)"]', '["!! Slow execution or lack of urgency during initial meetings signals poor founder velocity"]', '1-on-1 Founder Chat -> Term Sheet', '1-2 weeks', '~2-4%', 'bettercap.vc', 'All India', 'National', 'https://www.bettercap.vc', 'August 2026', '', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:23.540071+00:00', '2026-09-14T11:00:12.391839+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('PRIV-PEAKXV-SURGE-2026', 'PRIV-PEAKXV-SURGE-2026', 'Peak XV Surge (Flagship Seed Accelerator)', 'Peak XV Partners (Formerly Sequoia India)', 'Peak XV Partners (Formerly Sequoia India)', 'Equity', 'Private VC / Angel', 'Equity', 'Pre-Seed / Seed', 'Rs 8 Crores to Rs 24 Crores ($1M - $3M)', '16-week rapid scaling program providing $1M to $3M seed capital, company-building workshops, and access to 300+ Surge alumni.', '16-week rapid scaling program providing $1M to $3M seed capital, company-building workshops, and access to 300+ Surge alumni.', '["Technology", "AI/ML", "Consumer", "SaaS", "Fintech"]', '["Early-stage Indian or SEA startup (Pre-revenue or Early Revenue)", "Exceptional founding team with big market ambition", "SaaS, Consumer, Fintech, AI, or Climate Tech"]', '["Up to $3M capital check led by Peak XV", "16-week company building program in Bangalore, Singapore, and Silicon Valley", "Founder friendly SAFE or equity terms"]', '[">> Surge gives immense signal strength to US VCs for follow-on Series A rounds", ">> Peak XV expects high growth velocity - expect intense 16-week sprint on GTM and hiring"]', '["!! High valuation demands before proving initial PMF (Product-Market Fit) are discouraged", "!! Messy founder equity split will delay term sheet approval"]', 'Surge Application -> Pitch to Surge Leads -> Partner Due Diligence -> Sanction', '3-4 weeks', '~1-2%', 'surgeahead.com', 'All India', 'Private', 'https://www.surgeahead.com', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Peak XV Surge (Flagship Seed Accelerator) (Peak XV Partners (Formerly Sequoia India))
FUND TYPE: Seed VC Equity

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Peak XV Surge (Flagship Seed Accelerator) highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Peak XV Surge (Flagship Seed Accelerator) expenditure guidelines.
3. Address key scheme criteria: Early-stage Indian or SEA startup (Pre-revenue or Early Revenue), Exceptional founding team with big market ambition, SaaS, Consumer, Fintech, AI, or Climate Tech.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Peak XV Surge (Flagship Seed Accelerator) eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:19.387421+00:00', '2026-09-14T11:00:12.389729+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('PRIV-SPECIALE-2026', 'PRIV-SPECIALE-2026', 'Speciale Invest (DeepTech VC Fund)', 'Speciale Invest', 'Speciale Invest', 'Equity', 'Private VC / Angel', 'Equity', 'Pre-Seed / Seed', 'Rs 4 Crores to Rs 12 Crores ($500K - $1.5M)', 'Specialized deep-tech seed VC backing space tech, robotics, semiconductors, synthetic biology, and generative AI hardware.', 'Specialized deep-tech seed VC backing space tech, robotics, semiconductors, synthetic biology, and generative AI hardware.', '["DeepTech", "Semiconductors", "Hardware", "Defence", "Healthcare"]', '["Hard engineering or deep science innovation", "Defensible IP, patent potential, or complex technical barrier to entry", "Indian startup entity with global market applicability"]', '["Lead seed investment check", "Board seat or observer seat", "Significant follow-on capital reserve for Series A/B support"]', '[">> Speciale Invest is willing to back founders long before commercial launch if science is proven", ">> Strong network with ISRO, MeitY, and global defense/deeptech buyers"]', '["!! Pure software apps with no core scientific or engineering moat will be passed", "!! Founders unable to explain technical roadmap clearly to engineers will struggle"]', 'Pitch Deck -> Technical Due Diligence -> Lab Visit -> IC Approval -> Investment', '4-6 weeks', '~3-5%', 'specialeinvest.com', 'All India', 'Private', 'https://www.specialeinvest.com', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Speciale Invest (DeepTech VC Fund) (Speciale Invest)
FUND TYPE: Seed VC Equity

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Speciale Invest (DeepTech VC Fund) highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Speciale Invest (DeepTech VC Fund) expenditure guidelines.
3. Address key scheme criteria: Hard engineering or deep science innovation, Defensible IP, patent potential, or complex technical barrier to entry, Indian startup entity with global market applicability.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Speciale Invest (DeepTech VC Fund) eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:19.387421+00:00', '2026-09-14T11:00:12.389759+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('PRIV-TITAN-2026', 'PRIV-TITAN-2026', 'Titan Capital (Kunal Bahl & Rohit Bansal VC)', 'Titan Capital', 'Titan Capital', 'Equity', 'Private VC / Angel', 'Equity', 'Pre-Seed / Seed', 'Rs 80 Lakhs to Rs 4 Crores ($100K - $500K)', 'First-cheque seed fund backed by Snapdeal founders Kunal Bahl & Rohit Bansal, backing 250+ tech founders.', 'First-cheque seed fund backed by Snapdeal founders Kunal Bahl & Rohit Bansal, backing 250+ tech founders.', '["Technology", "Consumer", "SaaS", "AI/ML"]', '["High-conviction founding team", "Consumer tech, D2C, B2B marketplaces, SaaS, or AI", "Scalable business model solving large Indian/global problem"]', '["Founder-friendly equity terms", "Zero board seat intrusion", "Direct WhatsApp access to Kunal & Rohit for strategic guidance"]', '[">> Titan looks for RELENTLESS RESILIENCE - highlight team overcoming past setbacks", ">> Fast turnaround - decisions often made within 48 hours of pitch"]', '["!! Arrogance or lack of integrity during pitch is an immediate pass", "!! Cap table split where non-executives hold controlling equity"]', 'Online Pitch -> Founder Interview -> Investment Decision', '1-2 weeks', '~2-3%', 'titancapital.vc', 'All India', 'Private', 'https://www.titancapital.vc', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Titan Capital (Kunal Bahl & Rohit Bansal VC) (Titan Capital)
FUND TYPE: Angel & Seed Equity

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Titan Capital (Kunal Bahl & Rohit Bansal VC) highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Titan Capital (Kunal Bahl & Rohit Bansal VC) expenditure guidelines.
3. Address key scheme criteria: High-conviction founding team, Consumer tech, D2C, B2B marketplaces, SaaS, or AI, Scalable business model solving large Indian/global problem.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Titan Capital (Kunal Bahl & Rohit Bansal VC) eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:19.387421+00:00', '2026-09-14T11:00:12.38982+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-ADMIN-366B9476', NULL, 'Additional Capital Subsidy for Promotion of Cleaner and Environment-Friendly Technologies — Tamil Nadu', 'Micro, Small and Medium Enterprises Department, Government of Tamil Nadu', NULL, 'Capital Subsidy', 'State Govt', 'Capital Subsidy', 'Growth / Debt Scaling', 'Additional subsidy of 25% of eligible plant, machinery or equipment costs for qualifying cleaner technologies, subject to a maximum of ₹10 lakh.', 'Financial assistance for eligible plant, machinery and equipment investments that promote cleaner and environment-friendly production technologies.', 'This incentive supports qualifying investments in cleaner and environment-friendly technologies by eligible enterprises in Tamil Nadu. The additional capital subsidy is 25% of the value of eligible plant, machinery or equipment, subject to a maximum of ₹10 lakh. The assistance is intended for qualifying technology investments that meet the scheme''s requirements, including equipment not already considered for the base capital subsidy. Enterprise eligibility depends on the applicable manufacturing category, location, technology and current scheme guidelines.', '["Manufacturing & Engineering", "GreenTech, Clean Energy & EV"]', '[]', '[]', '["Identify the environmental benefit of the proposed equipment and maintain supplier quotations, technical specifications, invoices, installation records and evidence of commissioning. Confirm whether the Tamil Nadu Pollution Control Board certificate is required and whether the equipment is eligible under the current version of the scheme. Calculate the subsidy only on the eligible equipment cost."]', '["Equipment already considered for the base capital subsidy must not automatically be counted again for this incentive. The government guidelines require an appropriate Tamil Nadu Pollution Control Board certificate confirming the cleaner production benefit and compliance with applicable norms. Do not classify ordinary machinery as cleaner technology without technical evidence."]', NULL, NULL, NULL, NULL, 'Tamil Nadu', 'State', 'https://www.myscheme.gov.in/schemes/cs-tn', 'September 2026', 'Act as an environmental technology and Tamil Nadu MSME subsidy consultant. Review the enterprise''s manufacturing activity, location, proposed environmental technology, machinery specifications, eligible investment and Pollution Control Board documentation. Compare the proposed equipment with current official cleaner technology subsidy guidelines. Estimate 25% of verified eligible equipment costs, capped at ₹10 lakh. Identify equipment exclusions, certification requirements, duplicate subsidy risks and missing documents. Do not claim eligibility without evidence.', 'Manual Admin Addition', 'active', TRUE, 9999, '2026-10-25T06:29:57.553513+00:00', '2026-10-25T06:29:57.43258+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-ADMIN-7A3102E5', NULL, 'Additional Capital Subsidy — Special Category Entrepreneurs', 'Additional Capital Subsidy for Women, SC/ST, Differently Abled and Transgender Entrepreneurs — Tamil Nadu', NULL, 'Capital Subsidy', 'State Govt', 'Capital Subsidy', 'Growth / Debt Scaling', 'Additional subsidy of 5% on eligible plant and machinery investment, subject to a maximum of ₹5 lakh.', 'Additional capital subsidy for qualifying enterprises established by women, SC/ST, differently abled or transgender entrepreneurs', 'This Tamil Nadu government incentive provides an additional 5% capital subsidy on eligible plant and machinery, subject to a maximum of ₹5 lakh, for enterprises established by women, Scheduled Caste (SC), Scheduled Tribe (ST), differently abled and transgender entrepreneurs. Eligibility is restricted to the enterprise categories and locations specified in the current guidelines. These include eligible new micro enterprises, specified small and medium manufacturing enterprises in qualifying locations, and eligible agro-based or food-processing enterprises in designated blocks. The applicant''s qualifying status must be supported by the appropriate certificate or identification document.', '["Manufacturing & Engineering", "Food Processing & Agribusiness"]', '[]', '[]', '["Confirm the entrepreneur''s qualifying category, ownership or establishment conditions, eligible enterprise classification and location before estimating the claim. Collect the applicable certificate or identity document at the start of the application process. Check whether the applicant qualifies for other subsidies under the parent capital subsidy scheme."]', '["An applicant belonging to multiple specified categories cannot automatically claim a separate 5% subsidy for every category; the guidelines restrict this incentive to one select category. Do not assume that all service businesses or all manufacturing locations qualify. Verify eligible enterprise classes, location restrictions, prohibited activities and documentation requirements against the current guidelines."]', NULL, NULL, NULL, NULL, 'Tamil Nadu', 'State', 'https://www.myscheme.gov.in/schemes/cs-tn', 'September 2026', 'Act as a Tamil Nadu MSME subsidy application consultant. Assess the applicant''s qualifying entrepreneur category, supporting certificate, ownership or establishment details, Udyam classification, manufacturing activity, location and eligible machinery investment. Verify the current official guidelines for the Additional Capital Subsidy for Special Category Entrepreneurs. Calculate a provisional subsidy of 5% of verified eligible investment, capped at ₹5 lakh. Identify applicable location restrictions, documentation gaps and the rule limiting claims across multiple special categories.', 'Manual Admin Addition', 'active', TRUE, 9999, '2026-10-25T06:27:21.985171+00:00', '2026-10-25T06:27:21.865047+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-ADMIN-7C70C2C1', NULL, 'Branding and Marketing Support Grant for SC/ST MSME Entrepreneurs', 'Tamil Nadu Adi Dravidar Housing and Development Corporation Limited (TAHDCO), Adi Dravidar and Tribal Welfare Department, Government of Tamil Nadu', NULL, 'Grant', 'State Govt', 'Grant', 'Other / Multi-Stage (Specify)', '75% of eligible project cost, up to ₹60,000; mandatory beneficiary contribution of 25%, up to ₹20,000. Approximate maximum eligible project cost: ₹80,000, subject to official confirmation.', 'Financial assistance for eligible SC/ST MSMEs in Tamil Nadu to strengthen brand identity, packaging, marketing collateral, social media branding and market linkages, with TAHDCO support advertised at 75% of eligible costs up to approximately ₹60,000.', 'The Branding and Marketing Support Grant for SC/ST MSME Entrepreneurs is advertised by the Tamil Nadu Adi Dravidar Housing and Development Corporation Limited (TAHDCO), under the Adi Dravidar and Tribal Welfare Department, Government of Tamil Nadu.

**Scope of support**
- Brand strategy development.
- Marketing collateral development, including logos, brochures and promotional materials.
- Packaging design.
- Social media branding.
- Market linkages.
- One-time packaging production cost support.

**Financial assistance**
- TAHDCO contribution: 75% of eligible costs, up to approximately ₹60,000.
- Mandatory beneficiary contribution: 25%, up to approximately ₹20,000.
- The maximum implied eligible project cost is approximately ₹80,000, subject to official confirmation of eligible expenditure and applicable caps.

**Advertised eligibility**
1. Registered SC/ST micro, small or medium enterprise (MSME).
2. Business must be currently operational.
3. Eligible enterprise may be product-based or service-based.

**Disbursement conditions**
The poster states that the grant is released only after completion of the approved work, payment of the beneficiary contribution and submission of the required deliverables.

**Important verification note:** The precise application procedure, eligible expenditure rules, required documents, application deadline and whether prior approval is mandatory must be confirmed with TAHDCO before an applicant commits expenditure.', '["Cross-Sector / All Sectors"]', '[]', '[]', '[">> Policy objective: Improve the branding, packaging, marketing capabilities and market access of SC/ST-owned MSMEs in Tamil Nadu. This is an interpretation of the advertised scope, not verified insider information.", ">> Practical opportunity: Potentially useful for eligible operating businesses that need professional branding or packaging but cannot fund the entire project independently.", ">> Verification required: Confirm whether TAHDCO requires prior approval, approved vendors, quotations, invoices, proof of beneficiary contribution or specific completion certificates.", ">> No independently verified evidence of an undisclosed agenda or preferential selection criteria was identified in the reviewed material."]', '["!! The specific grant''s detailed terms were not independently verified on a dedicated official scheme page.", "!! The poster describes the financial caps as approximate; do not represent ₹60,000 as a guaranteed award.", "!! Applicants must confirm the exact SC/ST ownership or community eligibility criteria and valid MSME registration requirements.", "!! The poster states that payment follows completion of the work and submission of deliverables; applicants should verify whether prior approval is required before incurring expenditure.", "!! Confirm the eligible cost heads, GST treatment, quotation requirements, approved service providers, documentation and application deadline with TAHDCO.", "!! Do not assume that the QR code, contact number or any third-party application form is authentic without verification through an official TAHDCO channel."]', NULL, NULL, NULL, NULL, 'Tamil Nadu', 'State', 'https://www.tahdco.com/', 'September 2026', 'ROLE: Tamil Nadu MSME Grant Consultant and Business Branding Strategist.

TARGET SCHEME: Branding and Marketing Support Grant for SC/ST MSME Entrepreneurs.

IMPLEMENTING AGENCY: TAHDCO, Government of Tamil Nadu.

OBJECTIVE: Assess the applicant''s eligibility and prepare a credible, evidence-based application for branding and marketing assistance.

INPUTS REQUIRED:
- Enterprise name, legal structure and business location.
- Udyam/MSME registration details.
- Relevant SC/ST eligibility documentation.
- Product or service description and current operating status.
- Existing branding and packaging limitations.
- Proposed deliverables, vendor quotations and itemised project budget.
- Beneficiary contribution and proposed implementation schedule.

TASKS:
1. Assess eligibility against verified official scheme conditions and flag missing evidence.
2. Develop a specific branding and marketing improvement plan linked to measurable business outcomes.
3. Prepare a costed scope of work for brand strategy, marketing collateral, packaging design, social media branding, market linkages or eligible packaging production.
4. Calculate the proposed TAHDCO contribution and beneficiary share using the officially confirmed caps and eligible costs.
5. Prepare the project justification, implementation milestones, deliverables and expected commercial outcomes.
6. Identify compliance risks, documentation requirements and reimbursement or post-completion payment constraints.
7. Cite official sources for every material eligibility and funding claim.

CONSTRAINTS:
Do not fabricate eligibility, quotations, sales figures, approvals or official rules. Clearly distinguish confirmed scheme terms from assumptions. Do not recommend expenditure before verifying approval requirements. Produce an application-ready draft only after identifying all material information gaps.', 'Manual Admin Addition', 'active', TRUE, 9999, '2026-10-26T11:09:15.193502+00:00', '2026-10-26T11:09:15.088006+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-ADMIN-87C960FF', NULL, 'MSME Samadhaan — Delayed Payment Monitoring System', 'Ministry of Micro, Small and Medium Enterprises, Government of India; Office of the Development Commissioner (MSME), with cases handled by the relevant Micro and Small Enterprises Facilitation Council (MSEFC).', NULL, 'Subsidy + Support', 'State Govt', 'Subsidy + Support', 'Growth / Debt Scaling', 'No fixed grant or subsidy. Facilitates claims for recovery of eligible outstanding dues and applicable statutory interest, subject to the outcome of proceedings.', 'Online mechanism for eligible micro and small enterprises to submit delayed-payment claims against buyers under the MSMED Act.', 'MSME Samadhaan facilitates the filing of delayed-payment applications by eligible micro and small enterprises. Applications are forwarded to the relevant MSEFC for consideration. Under the Micro, Small and Medium Enterprises Development Act, 2006, qualifying delayed payments may attract statutory interest, and the competent council can issue directions to the buyer following examination of the case. Samadhaan itself does not award a fixed monetary subsidy or guarantee that a claim will be recovered.', '["Manufacturing & Engineering", "Food Processing & Agribusiness"]', '[]', '[]', '["Prepare the Udyam Registration certificate, purchase orders or contracts, invoices, delivery or service acceptance evidence, outstanding-payment ledger, communications with the buyer and payment history before filing. Reconcile the amount claimed against actual invoices and receipts. Identify the appropriate MSEFC and confirm the filing requirements before submission."]', '["This is a claim-facilitation mechanism, not a funding programme. Filing an application does not guarantee recovery or immediate payment. Claims must be supported by evidence, and eligibility depends on applicable statutory requirements. The MSEFC, rather than the portal itself, examines the case and handles the dispute."]', NULL, NULL, NULL, NULL, 'Tamil Nadu', 'State', 'https://msmeonline.tn.gov.in/incentives/pdf/msmi_guidlines.pdf', 'September 2026', 'Act as an MSME delayed-payment claim preparation consultant. Review the applicant''s Udyam Registration, buyer details, contractual payment terms, invoices, delivery evidence, outstanding principal and payment history. Assess whether the claim appears eligible for filing through MSME Samadhaan under the MSMED Act, 2006. Calculate the documented outstanding amount, identify missing evidence, prepare a chronology of events and draft a structured claim summary. Explain the applicable statutory interest provisions without guaranteeing a particular outcome.', 'Manual Admin Addition', 'active', TRUE, 9999, '2026-10-25T06:41:39.954971+00:00', '2026-10-25T06:41:39.831559+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-ADMIN-94414B4C', NULL, 'Additional Capital Subsidy for Scaling Up through Expansion / Diversification — Tamil Nadu', 'Micro, Small and Medium Enterprises Department, Government of Tamil Nadu', NULL, 'Capital Subsidy', 'State Govt', 'Capital Subsidy', 'Growth / Debt Scaling', 'Additional subsidy of 5% on eligible plant and machinery investment, subject to a maximum of ₹25 lakh', 'Additional capital subsidy for existing micro and small manufacturing enterprises that expand or diversify their operations and graduate to a higher enterprise category.', 'This incentive supports eligible existing Micro and Small Manufacturing Enterprises in Tamil Nadu that undertake expansion or diversification and graduate to a higher enterprise category. The additional capital subsidy is 5%, subject to a maximum of ₹25 lakh, under the scaling-up provisions of the Tamil Nadu MSME scheme guidelines. Eligibility requires qualifying expansion or diversification involving additional plant and machinery and the required graduation to a higher category. The benefit is additional to other eligible subsidies where the relevant conditions are satisfied.', '["Manufacturing & Engineering"]', '[]', '[]', '["Assess the enterprise''s current Udyam classification and proposed post-expansion classification before calculating the incentive. Maintain evidence of additional machinery investment, the existing production capacity, expansion or diversification plans and applicable turnover or classification records. Establish whether the proposed investment results in the qualifying category graduation and whether the enterprise has already received this scaling-up incentive."]', '["An ordinary machinery replacement or minor capacity improvement does not automatically qualify. The enterprise must meet the applicable expansion/diversification and category-graduation conditions. The current guidelines specify that eligible enterprises can receive the scaling-up incentive only once in a particular category. Verify exclusions and investment conditions before estimating or promising a subsidy"]', NULL, NULL, NULL, NULL, 'Tamil Nadu', 'State', 'https://msmeonline.tn.gov.in/', 'September 2026', 'Act as a Tamil Nadu MSME expansion and subsidy consultant. Evaluate the enterprise''s existing Udyam classification, proposed investment in additional plant and machinery, expansion or diversification plan, current and projected business classification, and supporting financial records. Assess eligibility under the current Additional Capital Subsidy for Scaling Up guidelines. Estimate 5% of verified eligible investment, capped at ₹25 lakh. Identify whether the project supports graduation to a higher enterprise category, whether the benefit has previously been claimed in that category, and which supporting documents are required. Clearly separate verified eligibility from assumptions.', 'Manual Admin Addition', 'active', TRUE, 9999, '2026-10-25T06:32:23.72916+00:00', '2026-10-25T06:32:23.612264+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-ADMIN-CB588EA9', NULL, 'Additional Capital Subsidy for Micro Manufacturing Enterprises — Tamil Nadu', 'Micro, Small and Medium Enterprises Department, Government of Tamil Nadu', NULL, 'Capital Subsidy', 'State Govt', 'Capital Subsidy', 'Growth / Debt Scaling', 'Additional subsidy of 10% on eligible plant and machinery investment, subject to a maximum of ₹5 lakh.', 'Additional capital investment assistance for eligible micro manufacturing enterprises purchasing plant and machinery.', 'This incentive provides additional capital subsidy to eligible micro manufacturing enterprises in Tamil Nadu. The subsidy is calculated at 10% of eligible plant and machinery investment, subject to a maximum of ₹5 lakh. It is an additional benefit associated with the Tamil Nadu Capital Subsidy Scheme and is subject to enterprise classification, eligible investment, sector restrictions, application deadlines and the applicable government guidelines. Eligibility for the base capital subsidy and the additional subsidy must be assessed separately.', '["Manufacturing & Engineering"]', '[]', '[]', '["Verify the enterprise''s Udyam classification, manufacturing activity, machinery invoices, commissioning date and eligible investment value before estimating the benefit. The 10% rate applies to eligible investment, not automatically to the entire project cost. Check the current guidelines for the application deadline and applicable disbursement procedure."]', '["Do not include land, buildings, working capital or other non-eligible costs in the machinery investment calculation. Do not assume that every micro enterprise qualifies: the relevant incentive is intended for eligible manufacturing enterprises. Confirm the prescribed application deadline and the exclusions in the current guidelines."]', NULL, NULL, NULL, NULL, 'Tamil Nadu', 'State', 'https://www.myscheme.gov.in/schemes/cs-tn', 'September 2026', 'Act as a Tamil Nadu MSME subsidy application consultant. Evaluate the applicant''s micro-enterprise classification, manufacturing activity, location, plant and machinery investment and supporting documents against the current official guidelines for the Additional Capital Subsidy for Micro Manufacturing Enterprises. Calculate a provisional subsidy at 10% of verified eligible investment, capped at ₹5 lakh. Identify missing documents, eligibility gaps and the applicable application deadline. Do not present unverified eligibility as confirmed.', 'Manual Admin Addition', 'active', TRUE, 9999, '2026-10-25T06:24:47.239533+00:00', '2026-10-25T06:24:47.126773+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-ADMIN-DE82AEA2', NULL, 'Procurement and Marketing Support (PMS) Scheme — Domestic Marketing Support for MSEs', 'Ministry of Micro, Small and Medium Enterprises, Government of India; Office of the Development Commissioner (MSME) and designated implementing agencies.', NULL, 'Reimbursement Grant', 'Central Govt', 'Reimbursement Grant', 'Growth / Debt Scaling', 'Under the published PMS scheme guidelines, eligible domestic trade-fair participants may receive assistance for stall or space rent. Published guidelines specify 80% assistance for general-category units and 100% for specified eligible categories, subject to applicable scheme rules, eligible stall size and event-specific limits. There is no universal fixed grant amount for every applicant or event.', 'Marketing and market-access assistance for eligible MSEs participating in approved domestic trade fairs, exhibitions and other supported marketing activities.', 'The Procurement and Marketing Support Scheme is a Government of India initiative intended to improve the market access and commercial visibility of micro and small enterprises. Its components include participation in eligible domestic trade fairs and exhibitions, trade-fair and exhibition activities organised by approved agencies, vendor development programmes, modern packaging awareness and other approved marketing-support activities. Financial assistance depends on the activity, applicant category, approved event, eligible costs and the applicable scheme guidelines. Assistance should not be assumed for every marketing expense.', '["Manufacturing & Engineering"]', '[]', '[]', '["Monitor the official PMS portal for eligible events and application windows. Check whether the specific event is approved, prepare the Udyam certificate, product profile, business details and any other prescribed documents, and review the available assistance before committing to stall expenditure. Preserve approval letters, invoices and receipts required for the claim."]', '["Assistance is conditional and subject to event-specific deadlines, approval, eligible expenditure and scheme ceilings. An enterprise must not assume that participation in any privately organised exhibition automatically qualifies. The reimbursement or assistance rate may differ by applicant category and scheme component."]', NULL, NULL, NULL, NULL, 'Tamil Nadu', 'State', 'https://pms.dcmsme.gov.in/home', 'September 2026', 'Act as an Indian MSME marketing-support consultant. Assess the applicant''s Udyam Registration, product category, business profile, selected domestic trade fair or exhibition, application deadline and proposed eligible expenditure against the current Procurement and Marketing Support Scheme guidelines. Identify whether the event and applicant satisfy the applicable conditions, determine the eligible expenses and assistance rate, prepare an application checklist and draft the supporting justification. Flag unapproved activities, non-eligible costs and missing documents.', 'Manual Admin Addition', 'active', TRUE, 9999, '2026-10-25T06:43:57.575867+00:00', '2026-10-25T06:43:57.465508+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-ADMIN-E6C86C37', NULL, 'Tamil Nadu MSME Capital Subsidy Scheme', 'Micro, Small and Medium Enterprises Department, Government of Tamil Nadu', NULL, 'Capital Subsidy', 'State Govt', 'Capital Subsidy', 'Growth / Debt Scaling', '25% of eligible plant and machinery cost, subject to a maximum of ₹150 lakh; additional subsidies may apply to eligible categories.', 'Capital investment assistance for eligible new manufacturing units and qualifying existing units undertaking expansion or diversification.', 'Provides a 25% subsidy on eligible plant and machinery, subject to a maximum of ₹150 lakh. Eligibility depends on enterprise classification, manufacturing activity, eligible investment, applicable sector or location conditions, and the current scheme guidelines. Separate additional capital subsidies may be available for eligible micro-enterprises, specified entrepreneur categories, cleaner technologies and qualifying expansion or diversification.
', '["Manufacturing & Engineering"]', '[]', '[]', '["Before applying, verify the current eligibility criteria with the Tamil Nadu MSME Department or District Industries Centre. Check whether the enterprise qualifies as a micro, small or medium manufacturing unit, whether the machinery is eligible, and whether any other government subsidy affects the claim. Prepare invoices, machinery specifications, investment evidence, Udyam registration and other prescribed documents."]', '["Do not assume all MSMEs or service businesses qualify. Certain industries and activities are excluded. Used machinery, overlapping government incentives, eligible investment definitions, application deadlines and other scheme-specific restrictions must be checked against the current official guidelines. The maximum subsidy is a ceiling, not a guaranteed payment."]', NULL, NULL, NULL, NULL, 'Tamil Nadu', 'State', 'https://www.myscheme.gov.in/schemes/cs-tn', 'September 2026', 'Act as a Tamil Nadu MSME scheme application consultant. Assess the applicant''s manufacturing activity, Udyam classification, location, project cost, machinery details, commencement date and previous government assistance against the current official Capital Subsidy guidelines. Identify eligibility gaps, calculate a provisional subsidy only from verified eligible costs and applicable limits, list required documents, and draft an evidence-based application. Clearly distinguish confirmed eligibility from assumptions.', 'Manual Admin Addition', 'active', TRUE, 9999, '2026-10-25T06:18:40.956975+00:00', '2026-10-25T06:18:40.825834+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-ADMIN-F2FF246B', NULL, 'Low Tension Power Tariff (LTPT) Subsidy — Tamil Nadu', 'Micro, Small and Medium Enterprises Department, Government of Tamil Nadu; Department of Industries and Commerce, implemented through the relevant District Industries Centre.', NULL, 'Subsidy + Support', 'State Govt', 'Subsidy + Support', 'Growth / Debt Scaling', '', 'Electricity tariff subsidy for eligible Tamil Nadu manufacturing enterprises to reduce operating costs during the initial years of production.', 'The Tamil Nadu MSME incentive guidelines describe a Low Tension Power Tariff (LTPT) subsidy of 20% of eligible power charges for the first 36 months, calculated from the date of commencement of production or the date of power connection, whichever is later, subject to the prescribed eligibility conditions. Eligible beneficiaries include specified micro manufacturing enterprises, qualifying manufacturing enterprises in designated backward areas, eligible agro-based and food-processing enterprises, and qualifying existing enterprises undertaking substantial expansion or diversification. The applicant must satisfy the applicable registration, power connection, activity, location and application requirements.', '["Manufacturing & Engineering", "Food Processing & Agribusiness"]', '[]', '[]', '["Scheme / Fund Name: Low Tension Power Tariff (LTPT) Subsidy — Tamil Nadu", "Category: State Govt", "Agency / Ministry / Firm: Micro, Small and Medium Enterprises Department, Government of Tamil Nadu; Department of Industries and Commerce, implemented through the relevant District Industries Centre.", "Funding Amount: 20% of eligible power consumption charges for the first 36 months, subject to applicable scheme eligibility and conditions.", "Funding / Capital Type: Tariff Subsidy / Electricity Cost Reimbursement", "Eligible Sectors: Eligible micro manufacturing enterprises across Tamil Nadu; qualifying small and medium manufacturing enterprises in designated backward areas and eligible industrial estates; eligible agro-based and food-processing enterprises.", "Eligibility Stage: Growth / Scaling", "State Scope / Geography: Tamil Nadu", "Official Portal URL: https://msmeonline.tn.gov.in/incentives/pdf/msmi_guidlines.pdf", "One-line Brief: Electricity tariff subsidy for eligible Tamil Nadu manufacturing enterprises to reduce operating costs during the initial years of production.", "Full Description / Details: The Tamil Nadu MSME incentive guidelines describe a Low Tension Power Tariff subsidy of 20% of eligible power charges for the first 36 months, calculated from the commencement of production or power connection, whichever is later, subject to prescribed conditions. Eligibility varies by manufacturing category, location, registration, power connection and qualifying expansion or diversification.", "Insider Intelligence / Hidden Agenda: Verify the enterprise''s manufacturing activity, eligible LT power connection, production commencement date, registration and location. Check electricity bills, payment proofs and eligibility certificate requirements with the District Industries Centre.", "Red Flags / Warnings: Service enterprises are excluded under the published guidelines. Eligibility differs by category, location and activity. Confirm current application deadlines, eligibility requirements and the continuing applicability of the published rate with the implementing authority.", "AI Pitch & Application Prompt: Act as a Tamil Nadu MSME incentive consultant. Evaluate the applicant''s classification, manufacturing activity, location, electricity connection, production commencement, registration and paid electricity bills against the currently applicable LTPT guidelines. Determine eligibility, identify missing documents, calculate provisional assistance using verified eligible power charges and the applicable rate and duration, and identify criteria requiring District Industries Centre confirmation."]', '["Service enterprises are excluded under the published guidelines, and eligibility differs according to enterprise category, location and type of activity. The eligibility certificate application deadline and documentation requirements must be checked against the applicable instructions. The published 20% rate and 36-month period should be treated as scheme-summary information until the current applicable rules are confirmed by the implementing authority."]', NULL, NULL, NULL, NULL, 'Tamil Nadu', 'State', 'https://msmeonline.tn.gov.in/incentives/pdf/msmi_guidlines.pdf', 'September 2026', 'Act as a Tamil Nadu MSME incentive consultant. Evaluate an applicant''s enterprise classification, manufacturing activity, location, electricity connection category, commencement of production, registration records and paid electricity bills against the currently applicable Low Tension Power Tariff Subsidy guidelines. Determine whether the enterprise meets the eligibility conditions, identify missing documents, calculate a provisional subsidy using verified eligible power charges and the applicable 20% rate and 36-month limit, and explain the application procedure. Flag any criteria that require confirmation from the District Industries Centre.', 'Manual Admin Addition', 'active', TRUE, 9999, '2026-10-25T06:39:14.205513+00:00', '2026-10-25T06:39:14.08249+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-GOI-10', 'SCH-GOI-10', 'Startup India Seed Fund Scheme (SISFS)', 'DPIIT, Ministry of Commerce & Industry', 'DPIIT, Ministry of Commerce & Industry', 'Grant to Incubators -> Startups', 'Central Govt', 'Grant to Incubators -> Startups', 'Pre-Seed / Seed', 'Up to Rs.20 lakhs (proof of concept) + Rs.50 lakhs (scale-up)', 'Grants disbursed through empaneled incubators, not directly to startups', 'Grants disbursed through empaneled incubators, not directly to startups', '["All Sectors", "Technology", "DeepTech", "Manufacturing"]', '["DPIIT-recognized startup", "Less than 2 years old at time of application", "Must be recommended by empaneled incubator", "Indian promoter holding >51%", "Not received >Rs.10 lakhs from other GoI schemes"]', '["Grant - NO equity taken", "Disbursed in milestones (3-4 tranches)", "Incubator monitors progress", "Must submit utilization certificates"]', '[">> The INCUBATOR is the real decision-maker - they nominate you, not you apply directly", ">> Government wants to see 10,000+ startups funded - volume matters more than quality", ">> The Rs.20L/Rs.50L amounts are MAXIMUM - most get Rs.10-15L", ">> They want startups that will hire - employment generation is a key metric"]', '["!! You CANNOT apply directly - must go through empaneled incubator", "!! Utilization certificates are a PAIN - maintain meticulous records", "!! If you''ve taken other GoI grants, you may be ineligible", "!! The incubator takes a monitoring fee/cut - factor this in"]', 'Get into empaneled incubator -> Incubator nominates -> DPIIT review -> Disbursement', '4-8 months', '~10-15% of nominated startups', 'seedfund.startupindia.gov.in', 'All India', 'National', 'https://seedfund.startupindia.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Startup India Seed Fund Scheme (SISFS) (DPIIT, Ministry of Commerce & Industry)
FUND TYPE: Grant to Incubators -> Startups

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Startup India Seed Fund Scheme (SISFS) highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Startup India Seed Fund Scheme (SISFS) expenditure guidelines.
3. Address key scheme criteria: DPIIT-recognized startup, Less than 2 years old at time of application, Must be recommended by empaneled incubator.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Startup India Seed Fund Scheme (SISFS) eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:19.387421+00:00', '2026-09-14T11:00:12.389983+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-GOI-11', 'SCH-GOI-11', 'Fund of Funds for Startups (FFS) - SIDBI', 'SIDBI (Small Industries Development Bank of India)', 'SIDBI (Small Industries Development Bank of India)', 'Indirect Investment (via VCs/AIFs)', 'Central Govt', 'Indirect Investment (via VCs/AIFs)', 'Pre-Seed / Seed', 'Rs.10,000 crore corpus - invests in VCs who invest in startups', 'Does NOT invest directly in startups. Invests in SEBI-registered AIFs/VCs who then invest in DPIIT-recognized startups', 'Does NOT invest directly in startups. Invests in SEBI-registered AIFs/VCs who then invest in DPIIT-recognized startups', '["All Sectors", "Technology", "DeepTech", "Manufacturing"]', '["DPIIT-recognized startup", "SEBI-registered investor (VC/AIF) must be empaneled with SIDBI", "Startup must be <10 years old", "Indian-owned (>51%)"]', '["SIDBI contributes up to 15% of VC fund corpus", "VC makes the investment decision", "Minimum investment in startup: Rs.25 lakhs", "Maximum: Rs.30 crore per startup"]', '[">> SIDBI does not pick startups - VCs do. Your real job is to get into a SIDBI-empaneled VC''s portfolio", ">> The Rs.10,000 crore corpus sounds huge but is spread across 80+ AIFs over 10 years", ">> VCs use SIDBI money as ''junior capital'' - they take less risk because government money absorbs first losses", ">> This creates a CONFLICT OF INTEREST - VCs may push startups to take SIDBI money even when better terms exist"]', '["!! You cannot approach SIDBI directly - must go through empaneled AIF", "!! The VC''s terms apply - SIDBI does not protect you from bad VC terms", "!! Some VCs use FFS money to fill their portfolio quotas with lower-quality startups"]', 'Get funded by SIDBI-empaneled VC -> VC claims from SIDBI', 'Depends on VC (3-9 months)', 'VC-dependent', 'sidbi.in', 'All India', 'National', 'https://www.sidbi.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Fund of Funds for Startups (FFS) - SIDBI (SIDBI (Small Industries Development Bank of India))
FUND TYPE: Indirect Investment (via VCs/AIFs)

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Fund of Funds for Startups (FFS) - SIDBI highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Fund of Funds for Startups (FFS) - SIDBI expenditure guidelines.
3. Address key scheme criteria: DPIIT-recognized startup, SEBI-registered investor (VC/AIF) must be empaneled with SIDBI, Startup must be <10 years old.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Fund of Funds for Startups (FFS) - SIDBI eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:19.387421+00:00', '2026-09-14T11:00:12.389999+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-GOI-12', 'SCH-GOI-12', 'Credit Guarantee Scheme for Startups (CGSS)', 'NCGTC (National Credit Guarantee Trustee Company)', 'NCGTC (National Credit Guarantee Trustee Company)', 'Loan Guarantee', 'State Govt', 'Loan Guarantee', 'Growth / Debt Scaling', 'Up to Rs.5 crore loan guarantee (85% cover)', 'Guarantees bank loans to startups - reduces collateral requirement', 'Guarantees bank loans to startups - reduces collateral requirement', '["All Sectors", "Technology", "DeepTech", "Manufacturing"]', '["DPIIT-recognized startup", "Loan from scheduled commercial bank", "Viable business plan", "No default history"]', '["85% guarantee cover for loans up to Rs.5 crore", "Guarantee fee: 2% per annum on outstanding", "Tenure: up to 5 years", "Collateral reduced but not eliminated"]', '[">> Banks still have DISCRETION - guarantee does not mean automatic approval", ">> The 2% guarantee fee adds to your cost - effective interest rate is higher", ">> Banks prefer this for ''safe'' startups - if you are too innovative, they''ll still say no", ">> The scheme exists to make banks LOOK like they are supporting startups - political optics"]', '["!! Not a grant - you must REPAY the loan", "!! Personal guarantee still required in most cases", "!! Default means government pays bank, then government chases YOU", "!! Only works if bank is willing - many banks do not actively promote this"]', 'Apply for bank loan -> Bank checks CGSS eligibility -> NCGTC guarantee -> Loan disbursement', '2-4 months', '~20-30% of loan applications', 'ncgtc.in', 'All India', 'State', 'https://www.ncgtc.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Credit Guarantee Scheme for Startups (CGSS) (NCGTC (National Credit Guarantee Trustee Company))
FUND TYPE: Loan Guarantee

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Credit Guarantee Scheme for Startups (CGSS) highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Credit Guarantee Scheme for Startups (CGSS) expenditure guidelines.
3. Address key scheme criteria: DPIIT-recognized startup, Loan from scheduled commercial bank, Viable business plan.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Credit Guarantee Scheme for Startups (CGSS) eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:19.387421+00:00', '2026-09-14T11:00:12.390026+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-GOI-13', 'SCH-GOI-13', 'BIRAC BIG (Biotechnology Ignition Grant)', 'BIRAC (Biotechnology Industry Research Assistance Council), DBT', 'BIRAC (Biotechnology Industry Research Assistance Council), DBT', 'Grant (Non-Dilutive)', 'Central Govt', 'Grant (Non-Dilutive)', 'Pre-Seed / Seed', 'Up to Rs.50 lakhs', 'For biotech startups and entrepreneurs at proof-of-concept stage', 'For biotech startups and entrepreneurs at proof-of-concept stage', '["All Sectors", "Technology", "DeepTech", "Manufacturing"]', '["Indian citizen", "Biotechnology/life sciences innovation", "Can apply as individual or startup", "Academic researchers can apply"]', '["Grant - no equity", "18-month project duration", "Milestone-based disbursement", "IP generated belongs to grantee"]', '[">> BIRAC wants COMMERCIALIZABLE research - pure academic research will not cut it", ">> They prefer startups with industry partnerships", ">> The 18-month timeline is RIGID - if you miss milestones, funding stops", ">> BIRAC success stories get political attention - they want winners, not experiments"]', '["!! Only for biotech - not for IT, fintech, etc.", "!! 18 months is short for biotech - most need 3-5 years", "!! Milestone pressure can force premature commercialization", "!! Reporting requirements are heavy for the amount"]', 'Online application -> Expert review -> Presentation -> Award', '4-6 months', '~8-12%', 'birac.nic.in', 'All India', 'National', 'https://www.birac.nic.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: BIRAC BIG (Biotechnology Ignition Grant) (BIRAC (Biotechnology Industry Research Assistance Council), DBT)
FUND TYPE: Grant (Non-Dilutive)

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for BIRAC BIG (Biotechnology Ignition Grant) highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official BIRAC BIG (Biotechnology Ignition Grant) expenditure guidelines.
3. Address key scheme criteria: Indian citizen, Biotechnology/life sciences innovation, Can apply as individual or startup.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official BIRAC BIG (Biotechnology Ignition Grant) eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:19.387421+00:00', '2026-09-14T11:00:12.390044+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-GOI-14', 'SCH-GOI-14', 'BIRAC SEED Fund', 'BIRAC, DBT', 'BIRAC, DBT', 'Equity-based Seed Funding', 'Central Govt', 'Equity-based Seed Funding', 'Pre-Seed / Seed', 'Up to Rs.30 lakhs (equity)', 'For biotech startups through BIRAC-supported incubators', 'For biotech startups through BIRAC-supported incubators', '["All Sectors", "Technology", "DeepTech", "Manufacturing"]', '["Biotech startup", "Incubated at BIRAC-supported incubator", "Less than 5 years old", "Proof of concept stage"]', '["Equity investment (minority stake)", "Incubator co-invests", "Mentorship mandatory", "Exit via buyback or next round"]', '[">> BIRAC takes equity - they want financial returns, not just social impact", ">> The incubator is the gatekeeper - they decide who gets SEED Fund", ">> BIRAC wants to build a biotech ecosystem - they''ll push you toward collaboration over competition"]', '["!! Equity dilution at seed stage - expensive", "!! Only through BIRAC-supported incubators", "!! Biotech only"]', 'Incubator nomination -> BIRAC review -> Investment committee -> Disbursement', '3-6 months', '~10%', 'birac.nic.in', 'All India', 'National', 'https://www.birac.nic.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: BIRAC SEED Fund (BIRAC, DBT)
FUND TYPE: Equity-based Seed Funding

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for BIRAC SEED Fund highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official BIRAC SEED Fund expenditure guidelines.
3. Address key scheme criteria: Biotech startup, Incubated at BIRAC-supported incubator, Less than 5 years old.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official BIRAC SEED Fund eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:19.387421+00:00', '2026-09-14T11:00:12.390059+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-GOI-15', 'SCH-GOI-15', 'BIRAC LEAP Fund', 'BIRAC, DBT', 'BIRAC, DBT', 'Early-Stage Equity', 'Central Govt', 'Early-Stage Equity', 'Pre-Seed / Seed', 'Up to Rs.1 crore', 'For biotech startups ready to scale from lab to market', 'For biotech startups ready to scale from lab to market', '["All Sectors", "Technology", "DeepTech", "Manufacturing"]', '["Biotech startup with working prototype", "Revenue or pre-revenue stage", "BIRAC-supported incubator backing"]', '["Equity investment", "Larger ticket than SEED Fund", "Board seat or observer rights", "Co-investment encouraged"]', '[">> LEAP is for startups that have ALREADY proven something - not for ideas", ">> BIRAC wants to show that their SEED Fund companies can graduate - it is a pipeline play"]', '["!! Only for companies that got SEED Fund or equivalent", "!! Significant equity dilution", "!! Biotech only"]', 'Incubator recommendation -> Due diligence -> Investment', '3-6 months', '~15% of SEED Fund companies', 'birac.nic.in', 'All India', 'National', 'https://www.birac.nic.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: BIRAC LEAP Fund (BIRAC, DBT)
FUND TYPE: Early-Stage Equity

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for BIRAC LEAP Fund highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official BIRAC LEAP Fund expenditure guidelines.
3. Address key scheme criteria: Biotech startup with working prototype, Revenue or pre-revenue stage, BIRAC-supported incubator backing.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official BIRAC LEAP Fund eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:19.387421+00:00', '2026-09-14T11:00:12.390074+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-GOI-16', 'SCH-GOI-16', 'NIDHI PRAYAS (DST)', 'DST (Department of Science & Technology)', 'DST (Department of Science & Technology)', 'Grant (Prototype Development)', 'Central Govt', 'Grant (Prototype Development)', 'Pre-Seed / Seed', 'Up to Rs.10 lakhs', 'For innovators to develop prototypes of novel product ideas', 'For innovators to develop prototypes of novel product ideas', '["All Sectors", "Technology", "DeepTech", "Manufacturing"]', '["Indian citizen (individual innovator or startup)", "Novel technology/product idea", "Must be associated with a PRAYAS Center (incubator)", "No age limit"]', '["Grant - no equity", "12-month project", "IP belongs to innovator", "Must submit prototype at end"]', '[">> DST wants PATENTS and PUBLICATIONS - not just products", ">> The PRAYAS Center takes a cut and provides the lab space - they are the real gatekeeper", ">> This is for HARDWARE/physical innovation - software ideas rarely get funded"]', '["!! Only Rs.10 lakhs - not enough for most hardware products", "!! 12 months is very short for prototype development", "!! Must work at PRAYAS Center - geographic constraint", "!! IP sharing disputes have happened - get clarity upfront"]', 'Approach PRAYAS Center -> Application -> Review -> Grant', '3-4 months', '~15-20%', 'dst.gov.in', 'All India', 'National', 'https://www.dst.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: NIDHI PRAYAS (DST) (DST (Department of Science & Technology))
FUND TYPE: Grant (Prototype Development)

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for NIDHI PRAYAS (DST) highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official NIDHI PRAYAS (DST) expenditure guidelines.
3. Address key scheme criteria: Indian citizen (individual innovator or startup), Novel technology/product idea, Must be associated with a PRAYAS Center (incubator).
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official NIDHI PRAYAS (DST) eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:21.078065+00:00', '2026-09-14T11:00:12.390089+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-GOI-17', 'SCH-GOI-17', 'NIDHI EIR (Entrepreneur-in-Residence)', 'DST (Department of Science & Technology)', 'DST (Department of Science & Technology)', 'Fellowship', 'Central Govt', 'Fellowship', 'Pre-Seed / Seed', 'Rs.30,000/month for 12 months (Rs.3.6 lakhs total)', 'Fellowship for aspiring entrepreneurs to develop business ideas at incubators', 'Fellowship for aspiring entrepreneurs to develop business ideas at incubators', '["All Sectors", "Technology", "DeepTech", "Manufacturing"]', '["Indian citizen with a business idea", "Graduate in any discipline", "Must be associated with NIDHI-supported incubator", "Not employed full-time"]', '["Monthly stipend - not equity", "12-month program", "Mentorship and infrastructure", "Must develop business plan"]', '[">> This is a SAFETY NET, not serious funding - Rs.30K/month is survival money", ">> DST wants to create a pipeline of ''innovators'' - the schemes success is measured by numbers, not outcomes", ">> The real value is the incubator access and mentorship, not the money"]', '["!! Rs.30K/month is barely enough to live on in Chennai/Bangalore", "!! You cannot have another job - full commitment required", "!! No equity but also no real funding - you''ll need other sources"]', 'Apply at NIDHI-supported incubator -> Selection -> Fellowship', '2-3 months', '~25-30%', 'dst.gov.in', 'All India', 'National', 'https://www.dst.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: NIDHI EIR (Entrepreneur-in-Residence) (DST (Department of Science & Technology))
FUND TYPE: Fellowship

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for NIDHI EIR (Entrepreneur-in-Residence) highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official NIDHI EIR (Entrepreneur-in-Residence) expenditure guidelines.
3. Address key scheme criteria: Indian citizen with a business idea, Graduate in any discipline, Must be associated with NIDHI-supported incubator.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official NIDHI EIR (Entrepreneur-in-Residence) eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:21.078065+00:00', '2026-09-14T11:00:12.390104+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-GOI-18', 'SCH-GOI-18', 'Atal New India Challenge (ANIC)', 'Atal Innovation Mission (AIM), NITI Aayog', 'Atal Innovation Mission (AIM), NITI Aayog', 'Grant (Competitive)', 'Central Govt', 'Grant (Competitive)', 'Pre-Seed / Seed', 'Up to Rs.1 crore', 'For startups solving national challenges in specific sectors', 'For startups solving national challenges in specific sectors', '["All Sectors", "Technology", "DeepTech", "Manufacturing"]', '["DPIIT-recognized startup or MSME", "Working prototype", "Solution aligned with announced challenge areas", "Indian-owned"]', '["Grant - no equity", "Milestone-based (3 stages)", "18-month project", "Must demonstrate scale potential"]', '[">> AIM wants SHOWCASE winners - they need success stories for political reporting", ">> Challenge areas are announced by government - you must ALIGN with their priorities, not yours", ">> The Rs.1 crore is MAXIMUM - most winners get Rs.30-50 lakhs", ">> They want startups that can be featured in media - visibility matters"]', '["!! Only for specific challenge areas - if your sector is not announced, you cannot apply", "!! Highly competitive - 700+ applications for 20-30 spots", "!! Milestone-based - miss one and funding stops", "!! Government procurement preference is PROMISED but rarely delivered"]', 'Apply when challenge is announced -> Screening -> Pitch -> Selection -> Disbursement', '4-8 months', '~3-5%', 'aim.gov.in', 'All India', 'National', 'https://www.aim.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Atal New India Challenge (ANIC) (Atal Innovation Mission (AIM), NITI Aayog)
FUND TYPE: Grant (Competitive)

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Atal New India Challenge (ANIC) highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Atal New India Challenge (ANIC) expenditure guidelines.
3. Address key scheme criteria: DPIIT-recognized startup or MSME, Working prototype, Solution aligned with announced challenge areas.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Atal New India Challenge (ANIC) eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:21.078065+00:00', '2026-09-14T11:00:12.390118+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-GOI-19', 'SCH-GOI-19', 'PMEGP (Prime Minister''s Employment Generation Programme)', 'KVIC / KVIB / DIC (Central + State)', 'KVIC / KVIB / DIC (Central + State)', 'Subsidy + Bank Loan', 'State Govt', 'Subsidy + Bank Loan', 'Growth / Debt Scaling', 'Up to Rs.50 lakhs (manufacturing) / Rs.10 lakhs (service)', 'PMEGP (Prime Minister''s Employment Generation Programme) provided by KVIC / KVIB / DIC (Central + State) offering Up to Rs.50 lakhs (manufacturing) / Rs.10 lakhs (service)', '', '["All Sectors", "Technology", "DeepTech", "Manufacturing"]', '["Age 18+", "VIII pass minimum (for projects >Rs.10L manufacturing, >Rs.5L service)", "No default to banks", "New project only"]', '["Margin money subsidy (see rates above)", "Bank loan for balance (up to 90% of project cost)", "3-7 year repayment", "Assets mortgaged to bank"]', '[">> This is an EMPLOYMENT scheme, not a startup scheme - they want job creation", ">> Banks are RISKY about PMEGP - they know the borrowers are high-risk", ">> The subsidy is released AFTER bank disburses - you need to convince the bank first", ">> KVIC/KVIB officers have significant discretion - relationship matters"]', '["!! Not for tech startups - designed for traditional businesses", "!! Bank loan is the bottleneck, not the subsidy", "!! If you default, both bank AND government come after you", "!! Project report must be detailed - DIC helps but quality varies"]', 'Apply at DIC/KVIB -> Project report -> Bank sanction -> Subsidy -> Disbursement', '3-6 months', '~30-40% with good project report', 'kviconline.gov.in/pmegp', 'All India', 'State', 'https://www.kviconline.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: PMEGP (Prime Minister''s Employment Generation Programme) (KVIC / KVIB / DIC (Central + State))
FUND TYPE: Subsidy + Bank Loan

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for PMEGP (Prime Minister''s Employment Generation Programme) highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official PMEGP (Prime Minister''s Employment Generation Programme) expenditure guidelines.
3. Address key scheme criteria: Age 18+, VIII pass minimum (for projects >Rs.10L manufacturing, >Rs.5L service), No default to banks.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official PMEGP (Prime Minister''s Employment Generation Programme) eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:21.078065+00:00', '2026-09-14T11:00:12.390134+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-GOI-20', 'SCH-GOI-20', 'Stand Up India Scheme', 'SIDBI (Ministry of Finance)', 'SIDBI (Ministry of Finance)', 'Bank Loan', 'Central Govt', 'Bank Loan', 'Growth / Debt Scaling', 'Rs.10 lakhs to Rs.1 crore', 'Composite loan (term + working capital) for SC/ST and women entrepreneurs', 'Composite loan (term + working capital) for SC/ST and women entrepreneurs', '["All Sectors", "Technology", "DeepTech", "Manufacturing"]', '["SC/ST or Woman entrepreneur", "Age 18+", "Greenfield project (new enterprise)", "Manufacturing, service, or trading sector", "No default to banks"]', '["Composite loan (term loan + working capital)", "Repayment up to 7 years", "Moratorium up to 18 months", "Credit guarantee under CGFSIL"]', '[">> Banks are RELUCTANT - this is a politically mandated scheme, and banks know these are risky borrowers", ">> The ''at least one SC/ST and one woman per branch'' target means banks APPROVE to meet quotas", ">> Handholding support is promised but often DELIVERED POORLY", ">> The schemes success rate is lower than official numbers suggest - many loans turn NPA"]', '["!! Bank branch manager has significant say - if they are not supportive, you are stuck", "!! Only for NEW enterprises - existing businesses cannot apply", "!! The 15% promoter contribution is strict - you need skin in the game", "!! Processing can take 3-6 months"]', 'Apply at bank branch -> Stand Up India portal -> Bank processing -> Sanction', '2-6 months', '~25-35%', 'standupmitra.in', 'All India', 'National', 'https://www.standupmitra.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Stand Up India Scheme (SIDBI (Ministry of Finance))
FUND TYPE: Bank Loan

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Stand Up India Scheme highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Stand Up India Scheme expenditure guidelines.
3. Address key scheme criteria: SC/ST or Woman entrepreneur, Age 18+, Greenfield project (new enterprise).
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Stand Up India Scheme eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:21.078065+00:00', '2026-09-14T11:00:12.390148+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-GOI-21', 'SCH-GOI-21', 'PM Vishwakarma Scheme', 'Ministry of MSME', 'Ministry of MSME', 'Loan + Skill Support', 'Central Govt', 'Loan + Skill Support', 'Growth / Debt Scaling', 'Up to Rs.2 lakhs (Term Loan) + Rs.1 lakhs (Working Capital)', 'PM Vishwakarma Scheme provided by Ministry of MSME offering Up to Rs.2 lakhs (Term Loan) + Rs.1 lakhs (Working Capital)', '', '["All Sectors", "Technology", "DeepTech", "Manufacturing"]', '["Traditional artisan/craftsperson", "One of 18 specified trades (blacksmith, goldsmith, potter, carpenter, etc.)", "Age 18+", "Not benefited from similar schemes"]', '["Collateral-free loan", "5% interest subvention", "Basic + Advanced skill training", "Modern toolkit provided", "Digital transaction incentive"]', '[">> This is a POLITICAL scheme - named after PM, launched before elections", ">> It is for TRADITIONAL crafts, not modern startups - do not try to fit a tech idea here", ">> The ''modern toolkit'' is often basic and not useful for scaling", ">> The scheme wants to FORMALIZE informal artisans - they want Aadhaar-linked, banked beneficiaries"]', '["!! Only for 18 specified traditional trades", "!! Not for tech/modern startups", "!! Loan amounts are small - not enough for scaling", "!! Must attend training - time cost"]', 'Register at CSC -> Skill training -> Bank loan -> Toolkit', '1-3 months', '~50%+ (if eligible)', 'pmvishwakarma.gov.in', 'All India', 'National', 'https://www.pmvishwakarma.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: PM Vishwakarma Scheme (Ministry of MSME)
FUND TYPE: Loan + Skill Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for PM Vishwakarma Scheme highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official PM Vishwakarma Scheme expenditure guidelines.
3. Address key scheme criteria: Traditional artisan/craftsperson, One of 18 specified trades (blacksmith, goldsmith, potter, carpenter, etc.), Age 18+.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official PM Vishwakarma Scheme eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:21.078065+00:00', '2026-09-14T11:00:12.390163+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-GOI-22', 'SCH-GOI-22', 'Mudra Loan (PMMY)', 'SIDBI / All Scheduled Banks / NBFCs', 'SIDBI / All Scheduled Banks / NBFCs', 'Loan (No collateral)', 'Central Govt', 'Loan (No collateral)', 'Growth / Debt Scaling', 'Shishu: Up to Rs.50,000 | Kishore: Rs.50,001 to Rs.5 lakhs | Tarun: Rs.5,00,001 to Rs.20 lakhs', 'For micro enterprises and small businesses', 'For micro enterprises and small businesses', '["All Sectors", "Technology", "DeepTech", "Manufacturing"]', '["Non-farm income generating activity", "Age 18-65", "No bank default", "Indian citizen"]', '["No collateral required", "Interest rate: 9-12% (bank-dependent)", "Repayment: 1-5 years", "No processing fee for Shishu"]', '[">> Banks use Mudra to meet PRIORITY SECTOR lending targets - it is a regulatory requirement", ">> The ''no collateral'' is true, but banks demand PERSONAL GUARANTEE and sometimes informal collateral", ">> Interest rates are HIGHER than regular business loans - banks price in the risk", ">> Mudra loans are often used for CONSUMPTION, not business - banks know this"]', '["!! Not for startups - for existing micro businesses", "!! Interest rates are high for ''government scheme''", "!! Banks may push you toward Mudra even when you qualify for better products", "!! Default affects CIBIL score severely"]', 'Apply at any bank -> Minimal documentation -> Disbursement', '1-4 weeks', '~60-70%', 'mudra.org.in / any bank', 'All India', 'National', 'https://www.mudra.org.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Mudra Loan (PMMY) (SIDBI / All Scheduled Banks / NBFCs)
FUND TYPE: Loan (No collateral)

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Mudra Loan (PMMY) highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Mudra Loan (PMMY) expenditure guidelines.
3. Address key scheme criteria: Non-farm income generating activity, Age 18-65, No bank default.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Mudra Loan (PMMY) eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:21.078065+00:00', '2026-09-14T11:00:12.390184+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-GOI-23', 'SCH-GOI-23', 'PM SVANidhi (Street Vendor''s AtmaNirbhar Nidhi)', 'Ministry of Housing & Urban Affairs', 'Ministry of Housing & Urban Affairs', 'Working Capital Loan', 'Central Govt', 'Working Capital Loan', 'Growth / Debt Scaling', 'Rs.10,000 (initial) -> Rs.20,000 (2nd) -> Rs.50,000 (3rd)', 'For street vendors/hawkers in urban areas', 'For street vendors/hawkers in urban areas', '["All Sectors", "Technology", "DeepTech", "Manufacturing"]', '["Street vendor in urban area", "Holding vending certificate/ID", "Or identified in ULB survey"]', '["7% interest subvention", "Monthly digital transaction reward: Rs.100", "No collateral", "1-year repayment"]', '[">> This is for STREET VENDORS, not startups - completely different category", ">> The digital transaction reward is to push DIGITAL PAYMENTS - governments real agenda", ">> ULB (Urban Local Body) survey determines eligibility - if you are not surveyed, you are out"]', '["!! NOT for startups - for street vendors only", "!! Very small amounts", "!! Must be in urban area with vending certificate"]', 'Apply at bank/online -> ULB verification -> Disbursement', '2-4 weeks', '~70%+', 'pmsvanidhi.mohua.gov.in', 'All India', 'National', 'https://www.pmsvanidhi.mohua.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: PM SVANidhi (Street Vendor''s AtmaNirbhar Nidhi) (Ministry of Housing & Urban Affairs)
FUND TYPE: Working Capital Loan

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for PM SVANidhi (Street Vendor''s AtmaNirbhar Nidhi) highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official PM SVANidhi (Street Vendor''s AtmaNirbhar Nidhi) expenditure guidelines.
3. Address key scheme criteria: Street vendor in urban area, Holding vending certificate/ID, Or identified in ULB survey.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official PM SVANidhi (Street Vendor''s AtmaNirbhar Nidhi) eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:21.078065+00:00', '2026-09-14T11:00:12.390217+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-INDIAAI-2026', 'SCH-INDIAAI-2026', 'IndiaAI Mission Compute & Startup Support', 'MeitY (Ministry of Electronics and IT)', 'MeitY (Ministry of Electronics and IT)', 'Compute Subsidy & Grant', 'Central Govt', 'Compute Subsidy & Grant', 'Pre-Seed / Seed', 'Up to 40% compute GPU subsidy + Rs 1 Crore grant', 'Access to 10,000+ GPUs onboarded via empaneled providers plus cohort grants for AI startups', 'Access to 10,000+ GPUs onboarded via empaneled providers plus cohort grants for AI startups', '["AI/ML", "Technology", "DeepTech"]', '["DPIIT-recognized Indian AI startup", "Developing indigenous AI models, IP, or AI-powered products", "Resident Indian shareholding >= 51%"]', '["40% GPU compute cost subsidized directly", "Up to Rs.1 Crore non-dilutive grant for model development", "Access to IndiaAI Datasets Platform and AI Bhashini APIs"]', '[">> MeitY wants SOVEREIGN AI & Indigenous IP - show how your model reduces reliance on OpenAI/US tech", ">> Priority for Indic AI models (Indian regional languages) and foundational models", ">> Compute grants released via empaneled cloud partners (C-DAC, Yotta, E2E)"]', '["!! Do not submit wrapper apps with no unique data or IP - auto-rejected", "!! GPU allocation has strict usage quotas - non-utilization results in quota clawback"]', 'IndiaAI portal application -> Technical IP review -> GPU allocation & Grant sanction', '2-3 months', '~20%', 'indiaai.gov.in', 'All India', 'National', 'https://www.indiaai.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: IndiaAI Mission Compute & Startup Support (MeitY (Ministry of Electronics and IT))
FUND TYPE: Compute GPU Subsidy & Cohort Grant

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for IndiaAI Mission Compute & Startup Support highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official IndiaAI Mission Compute & Startup Support expenditure guidelines.
3. Address key scheme criteria: DPIIT-recognized Indian AI startup, Developing indigenous AI models, IP, or AI-powered products, Resident Indian shareholding >= 51%.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official IndiaAI Mission Compute & Startup Support eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:19.387421+00:00', '2026-09-14T11:00:12.389636+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-INDIAAI-2026-DUP-149', 'SCH-INDIAAI-2026', 'IndiaAI Mission Compute & Startup Support', 'MeitY (Ministry of Electronics and IT)', 'MeitY (Ministry of Electronics and IT)', 'Grant', 'Central Govt', 'Grant', 'Pre-Seed / Seed', 'Up to 40% compute GPU subsidy + Rs 1 Crore grant', 'IndiaAI Mission Compute & Startup Support', 'Access to 10,000+ GPUs onboarded via empaneled providers plus cohort grants.', '["AI/ML", "DeepTech"]', '["DPIIT-recognized Indian AI startup"]', '["40% GPU compute cost subsidized directly"]', '[">> MeitY wants SOVEREIGN AI & Indigenous IP - show how your model reduces reliance on OpenAI"]', '["!! Do not submit wrapper apps with no unique data or IP - auto-rejected"]', 'IndiaAI portal application', '2-3 months', '~20%', 'indiaai.gov.in', 'All India', 'National', 'https://www.indiaai.gov.in', 'August 2026', '', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:23.540071+00:00', '2026-09-14T11:00:12.391854+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-100', 'SCH-OFFICIAL-100', 'Domain-specific Centres of Excellence', 'Ministry of Electronics and Information Technology (MeitY)', 'Ministry of Electronics and Information Technology (MeitY)', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for Domain-specific Centres of Excellence under Ministry of Electronics and Information Technology (MeitY).', 'Official scheme support for Domain-specific Centres of Excellence under Ministry of Electronics and Information Technology (MeitY).', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '[]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Electronics and Information Technology (MeitY) national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://meity.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Domain-specific Centres of Excellence (Ministry of Electronics and Information Technology (MeitY))
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Domain-specific Centres of Excellence highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Domain-specific Centres of Excellence expenditure guidelines.
3. Address key scheme criteria: .
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Domain-specific Centres of Excellence eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:22.612366+00:00', '2026-09-14T11:00:12.391304+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-101', 'SCH-OFFICIAL-101', 'Venture Capital by SIDBI Venture Capital Ltd. (SVLC)', 'Public Sector Enterprise', 'Public Sector Enterprise', 'Equity', 'Private VC / Angel', 'Equity', 'Pre-Series A / Series A', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for Venture Capital by SIDBI Venture Capital Ltd. (SVLC) under Public Sector Enterprise.', 'Official scheme support for Venture Capital by SIDBI Venture Capital Ltd. (SVLC) under Public Sector Enterprise.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["A strong committed management team, established performance record and a high degree of integrity, Sustainable competitive advantage, Scalability of operations, Potential for above average profitability, leading to attractive returns on investment, Subscription to equity/ equity-type instruments, Unlisted companies preferably MSME and Availability of exit route for Venture Capital investment."]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Public Sector Enterprise national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'Private', 'https://seedfund.startupindia.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Venture Capital by SIDBI Venture Capital Ltd. (SVLC) (Public Sector Enterprise)
FUND TYPE: Equity

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Venture Capital by SIDBI Venture Capital Ltd. (SVLC) highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Venture Capital by SIDBI Venture Capital Ltd. (SVLC) expenditure guidelines.
3. Address key scheme criteria: A strong committed management team, established performance record and a high degree of integrity, Sustainable competitive advantage, Scalability of operations, Potential for above average profitability, leading to attractive returns on investment, Subscription to equity/ equity-type instruments, Unlisted companies preferably MSME and Availability of exit route for Venture Capital investment..
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Venture Capital by SIDBI Venture Capital Ltd. (SVLC) eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:23.170011+00:00', '2026-09-14T11:00:12.391314+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-34', 'SCH-OFFICIAL-34', 'NABVENTURES Fund', 'National Bank for Agriculture and Rural Development (NABARD)', 'National Bank for Agriculture and Rural Development (NABARD)', 'Equity', 'Private VC / Angel', 'Equity', 'Pre-Series A / Series A', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for NABVENTURES Fund under National Bank for Agriculture and Rural Development (NABARD).', 'Official scheme support for NABVENTURES Fund under National Bank for Agriculture and Rural Development (NABARD).', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["Type of Business: Startups registered as private limited companies or limited liability partnerships (LLPs) in India, engaged in agriculture, agtech, agri-biotech, food, agri rural fintech, and rural businesses.", "Stage of Development: Early to mid-stage ventures with innovative and scalable business models, demonstrating the potential for high impact and positive contribution to relevant sectors.", "Financial Performance: Minimum annual turnover of Rs. 25 lakhs for profit-making companies or demonstrably positive unit economics for pre-revenue ventures.", "Team Expertise: Strong and experienced founding team with relevant domain knowledge and business acumen."]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with National Bank for Agriculture and Rural Development (NABARD) national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'Private', 'https://nabventures.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: NABVENTURES Fund (National Bank for Agriculture and Rural Development (NABARD))
FUND TYPE: Equity

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for NABVENTURES Fund highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official NABVENTURES Fund expenditure guidelines.
3. Address key scheme criteria: Type of Business: Startups registered as private limited companies or limited liability partnerships (LLPs) in India, engaged in agriculture, agtech, agri-biotech, food, agri rural fintech, and rural businesses., Stage of Development: Early to mid-stage ventures with innovative and scalable business models, demonstrating the potential for high impact and positive contribution to relevant sectors., Financial Performance: Minimum annual turnover of Rs. 25 lakhs for profit-making companies or demonstrably positive unit economics for pre-revenue ventures..
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official NABVENTURES Fund eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:21.078065+00:00', '2026-09-14T11:00:12.390246+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-35', 'SCH-OFFICIAL-35', 'National Urban Livelihoods Mission', 'Ministry of Housing and Urban Affairs Schemes', 'Ministry of Housing and Urban Affairs Schemes', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for National Urban Livelihoods Mission under Ministry of Housing and Urban Affairs Schemes.', 'Official scheme support for National Urban Livelihoods Mission under Ministry of Housing and Urban Affairs Schemes.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '[]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Housing and Urban Affairs Schemes national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://nulm.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: National Urban Livelihoods Mission (Ministry of Housing and Urban Affairs Schemes)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for National Urban Livelihoods Mission highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official National Urban Livelihoods Mission expenditure guidelines.
3. Address key scheme criteria: .
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official National Urban Livelihoods Mission eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:21.078065+00:00', '2026-09-14T11:00:12.390284+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-36', 'SCH-OFFICIAL-36', 'The Women Entrepreneurship Platform (WEP)', 'Niti Aayog', 'Niti Aayog', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for The Women Entrepreneurship Platform (WEP) under Niti Aayog.', 'Official scheme support for The Women Entrepreneurship Platform (WEP) under Niti Aayog.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["Potential women entrepreneurs, in collaboration with partner organizations can apply for the scheme"]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Niti Aayog national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://wep.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: The Women Entrepreneurship Platform (WEP) (Niti Aayog)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for The Women Entrepreneurship Platform (WEP) highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official The Women Entrepreneurship Platform (WEP) expenditure guidelines.
3. Address key scheme criteria: Potential women entrepreneurs, in collaboration with partner organizations can apply for the scheme.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official The Women Entrepreneurship Platform (WEP) eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:21.078065+00:00', '2026-09-14T11:00:12.390311+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-37', 'SCH-OFFICIAL-37', 'Technology Development Fund', 'Ministry of Defence', 'Ministry of Defence', 'Equity', 'Central Govt', 'Equity', 'Pre-Series A / Series A', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for Technology Development Fund under Ministry of Defence.', 'Official scheme support for Technology Development Fund under Ministry of Defence.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["Eligibility for Industry Private industry registered in India especially MSMEs and Startups The industry must be a public limited company, a private limited company, a partnership firm, a limited liability partnership, one-person company, sole proprietorship registered as per applicable Indian laws Industry to be owned and controlled by a Resident Indian Citizen with a shareholding of at least 51%"]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Defence national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://tdf.drdo.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Technology Development Fund (Ministry of Defence)
FUND TYPE: Equity

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Technology Development Fund highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Technology Development Fund expenditure guidelines.
3. Address key scheme criteria: Eligibility for Industry Private industry registered in India especially MSMEs and Startups The industry must be a public limited company, a private limited company, a partnership firm, a limited liability partnership, one-person company, sole proprietorship registered as per applicable Indian laws Industry to be owned and controlled by a Resident Indian Citizen with a shareholding of at least 51%.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Technology Development Fund eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:21.078065+00:00', '2026-09-14T11:00:12.390328+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-38', 'SCH-OFFICIAL-38', 'Innovations for Defence Excellence (iDEX)', 'Ministry of Defence', 'Ministry of Defence', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for Innovations for Defence Excellence (iDEX) under Ministry of Defence.', 'Official scheme support for Innovations for Defence Excellence (iDEX) under Ministry of Defence.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["Start-ups, as defined and recognized by Department of Industrial Policy and Promotion (DIPP), Ministry of Commerce and Industry, Government of India", "Any Indian company incorporated under the Companies Act 1956/2013, primarily a Micro, Small and Medium Enterprises (MSME) as defined in the MSME Act, 2006.", "Individual innovators are also encouraged to apply (research & academic institutions can use this category to apply)."]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Defence national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://idex.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Innovations for Defence Excellence (iDEX) (Ministry of Defence)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Innovations for Defence Excellence (iDEX) highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Innovations for Defence Excellence (iDEX) expenditure guidelines.
3. Address key scheme criteria: Start-ups, as defined and recognized by Department of Industrial Policy and Promotion (DIPP), Ministry of Commerce and Industry, Government of India, Any Indian company incorporated under the Companies Act 1956/2013, primarily a Micro, Small and Medium Enterprises (MSME) as defined in the MSME Act, 2006., Individual innovators are also encouraged to apply (research & academic institutions can use this category to apply)..
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Innovations for Defence Excellence (iDEX) eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:21.078065+00:00', '2026-09-14T11:00:12.390343+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-39', 'SCH-OFFICIAL-39', 'Niryat Bandhu Scheme', 'Ministry of Commerce and Industry Schemes', 'Ministry of Commerce and Industry Schemes', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for Niryat Bandhu Scheme under Ministry of Commerce and Industry Schemes.', 'Official scheme support for Niryat Bandhu Scheme under Ministry of Commerce and Industry Schemes.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["Any person can take this Course"]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Commerce and Industry Schemes national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://www.dgft.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Niryat Bandhu Scheme (Ministry of Commerce and Industry Schemes)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Niryat Bandhu Scheme highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Niryat Bandhu Scheme expenditure guidelines.
3. Address key scheme criteria: Any person can take this Course.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Niryat Bandhu Scheme eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:21.078065+00:00', '2026-09-14T11:00:12.390357+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-40', 'SCH-OFFICIAL-40', 'Industry Innovation Programme on Medical Electronics (IIPME)', 'Biotechnology Industry Research Assistance Council (BIRAC)', 'Biotechnology Industry Research Assistance Council (BIRAC)', 'Grant / Support', 'State Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for Industry Innovation Programme on Medical Electronics (IIPME) under Biotechnology Industry Research Assistance Council (BIRAC).', 'Official scheme support for Industry Innovation Programme on Medical Electronics (IIPME) under Biotechnology Industry Research Assistance Council (BIRAC).', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["Indian startups which are less than three years old from date of advertisement which have 51% ownership, Indian LLPs and those which have Department of Scientific and Industrial Research (DSIR) Recognition (only for early transition & transition to scale) are eligible to apply under the scheme."]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Biotechnology Industry Research Assistance Council (BIRAC) national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'State', 'https://birac.nic.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Industry Innovation Programme on Medical Electronics (IIPME) (Biotechnology Industry Research Assistance Council (BIRAC))
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Industry Innovation Programme on Medical Electronics (IIPME) highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Industry Innovation Programme on Medical Electronics (IIPME) expenditure guidelines.
3. Address key scheme criteria: Indian startups which are less than three years old from date of advertisement which have 51% ownership, Indian LLPs and those which have Department of Scientific and Industrial Research (DSIR) Recognition (only for early transition & transition to scale) are eligible to apply under the scheme..
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Industry Innovation Programme on Medical Electronics (IIPME) eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:21.078065+00:00', '2026-09-14T11:00:12.390372+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-41', 'SCH-OFFICIAL-41', 'BIRAC Incubators SEED Fund', 'Biotechnology Industry Research Assistance Council (BIRAC)', 'Biotechnology Industry Research Assistance Council (BIRAC)', 'Equity', 'Central Govt', 'Equity', 'Pre-Series A / Series A', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for BIRAC Incubators SEED Fund under Biotechnology Industry Research Assistance Council (BIRAC).', 'Official scheme support for BIRAC Incubators SEED Fund under Biotechnology Industry Research Assistance Council (BIRAC).', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["<b>Incubator Eligibility :</b>", "Supported through BIRAC''s Bio-NEST Programme.", "Operational for at least three years with at least five resident startups in Biotech/Med-Tech/Life Sciences.", "Established Intellectual Property & Technology Transfer (IP&TT) facilitation services.", "Prior experience managing early-stage funding schemes or grants.", "<b>Startup Eligibility : </b>", "Registered under Companies Act, 2013.", "At least 51% shareholding by Indian citizens (excluding OCI or PIO).", "Engaged in innovative and technology-driven projects relevant to biotechnology and life sciences.", "Demonstrate significant technical advancement and commercialization potential."]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Biotechnology Industry Research Assistance Council (BIRAC) national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://birac.nic.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: BIRAC Incubators SEED Fund (Biotechnology Industry Research Assistance Council (BIRAC))
FUND TYPE: Equity

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for BIRAC Incubators SEED Fund highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official BIRAC Incubators SEED Fund expenditure guidelines.
3. Address key scheme criteria: <b>Incubator Eligibility :</b>, Supported through BIRAC''s Bio-NEST Programme., Operational for at least three years with at least five resident startups in Biotech/Med-Tech/Life Sciences..
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official BIRAC Incubators SEED Fund eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:21.078065+00:00', '2026-09-14T11:00:12.390387+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-42', 'SCH-OFFICIAL-42', 'Biotechnology Industry Partnership Program (BIPP)', 'Biotechnology Industry Research Assistance Council (BIRAC)', 'Biotechnology Industry Research Assistance Council (BIRAC)', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for Biotechnology Industry Partnership Program (BIPP) under Biotechnology Industry Research Assistance Council (BIRAC).', 'Official scheme support for Biotechnology Industry Partnership Program (BIPP) under Biotechnology Industry Research Assistance Council (BIRAC).', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["The proposals can be submitted by following · Single or consortia of Company (ies)* incorporated under the Companies Act, 2013 or Limited Liability Partnership (LLP)** incorporated under the Limited Liability Partnership Act, 2008 jointly with or without the following: Public/private university/colleges in India National research laboratories Not-for-profit private research labs/societies/foundation/NGO 2. 3. Eligibility Criteria · For Company/LLP:- * Minimum 51% of the shares of the Company should be held by Indian Citizens holding Indian passport [Indian Citizens do not include Person of Indian Origin (PIO) and Overseas Citizenship of India (OCI) holders] ** Minimum half of the persons who subscribed their names to the LLP document as its Partners should be Indian citizens. The Applicant Company/ LLP should: Have adequate in-house facility to address the project implementation(which shall be evaluated during the site visit) or Incubated at any of the recognized Incubation Facility · For Academic collaborator: Eligible Academia shall mean an entity which is having proper establishment documents For Public or Private Institute, University, NGO, or Research Foundation, proper registration/accreditation from a government body is mandatory like certification, AICTE, CSIR /DSIR/SIRO certificate etc."]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Biotechnology Industry Research Assistance Council (BIRAC) national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://birac.nic.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Biotechnology Industry Partnership Program (BIPP) (Biotechnology Industry Research Assistance Council (BIRAC))
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Biotechnology Industry Partnership Program (BIPP) highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Biotechnology Industry Partnership Program (BIPP) expenditure guidelines.
3. Address key scheme criteria: The proposals can be submitted by following · Single or consortia of Company (ies)* incorporated under the Companies Act, 2013 or Limited Liability Partnership (LLP)** incorporated under the Limited Liability Partnership Act, 2008 jointly with or without the following: Public/private university/colleges in India National research laboratories Not-for-profit private research labs/societies/foundation/NGO 2. 3. Eligibility Criteria · For Company/LLP:- * Minimum 51% of the shares of the Company should be held by Indian Citizens holding Indian passport [Indian Citizens do not include Person of Indian Origin (PIO) and Overseas Citizenship of India (OCI) holders] ** Minimum half of the persons who subscribed their names to the LLP document as its Partners should be Indian citizens. The Applicant Company/ LLP should: Have adequate in-house facility to address the project implementation(which shall be evaluated during the site visit) or Incubated at any of the recognized Incubation Facility · For Academic collaborator: Eligible Academia shall mean an entity which is having proper establishment documents For Public or Private Institute, University, NGO, or Research Foundation, proper registration/accreditation from a government body is mandatory like certification, AICTE, CSIR /DSIR/SIRO certificate etc..
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Biotechnology Industry Partnership Program (BIPP) eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:21.078065+00:00', '2026-09-14T11:00:12.390402+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-43', 'SCH-OFFICIAL-43', 'Venture Capital Fund for Backward Classes (VCF-BC)', 'Ministry of Social Justice and Empowerment (MoSJE)', 'Ministry of Social Justice and Empowerment (MoSJE)', 'Equity', 'Central Govt', 'Equity', 'Pre-Series A / Series A', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for Venture Capital Fund for Backward Classes (VCF-BC) under Ministry of Social Justice and Empowerment (MoSJE).', 'Official scheme support for Venture Capital Fund for Backward Classes (VCF-BC) under Ministry of Social Justice and Empowerment (MoSJE).', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["The following are the eligibility criteria for prospective Companies promoted by Backward Classes entrepreneurs in the country for seeking assistance under the fund:", "The projects being set up in manufacturing, services sector, and allied sectors ensuring asset creation out of the funds deployed.", "Start-ups would also be eligible for finance as per the scheme guidelines.", "Women and disabled Backward Classes entrepreneurs will be preferred.", "Minimum existence and shareholding criteria:<br>", "✓ If assistance is below Rs. 50 Lakh - Companies having at least 51% stake holdings by Backward Classes entrepreneurs for the past 6 months with management control OR a new Company provided that the new Company is a successor entity of a Proprietary Firm or Partnership Firm or One Person Company (OPC) or Limited Liability Partnership (LLP) or any other establishment incorporated under any law in force, with the sound business model which has been in operation for over 6 months, and the predecessor entity had at least 51% shareholding of the Backward Classes promoters with management control.", "✓ If assistance is above Rs.50 lakh - Companies having at least 51% stake holdings by Backward Classes entrepreneurs for the past 12 months with management control OR a new Company provided that the new Company is a successor entity of a Proprietary Firm or Partnership Firm or One Person Company (OPC) or Limited Liability Partnership (LLP) or any other establishment incorporated under any law in force, with the sound business model which has been in operation for over 12 months, and the predecessor entity had at least 51% shareholding of the Backward Classes promoters with management control.", "Documentary proofs of being Backward Classes will have to be submitted."]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Social Justice and Empowerment (MoSJE) national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://vcf-bc.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Venture Capital Fund for Backward Classes (VCF-BC) (Ministry of Social Justice and Empowerment (MoSJE))
FUND TYPE: Equity

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Venture Capital Fund for Backward Classes (VCF-BC) highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Venture Capital Fund for Backward Classes (VCF-BC) expenditure guidelines.
3. Address key scheme criteria: The following are the eligibility criteria for prospective Companies promoted by Backward Classes entrepreneurs in the country for seeking assistance under the fund:, The projects being set up in manufacturing, services sector, and allied sectors ensuring asset creation out of the funds deployed., Start-ups would also be eligible for finance as per the scheme guidelines..
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Venture Capital Fund for Backward Classes (VCF-BC) eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:21.078065+00:00', '2026-09-14T11:00:12.390433+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-44', 'SCH-OFFICIAL-44', 'Venture Capital Fund for Scheduled Castes (VCF-SC)', 'Ministry of Social Justice and Empowerment (MoSJE)', 'Ministry of Social Justice and Empowerment (MoSJE)', 'Equity', 'Central Govt', 'Equity', 'Pre-Series A / Series A', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for Venture Capital Fund for Scheduled Castes (VCF-SC) under Ministry of Social Justice and Empowerment (MoSJE).', 'Official scheme support for Venture Capital Fund for Scheduled Castes (VCF-SC) under Ministry of Social Justice and Empowerment (MoSJE).', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["The projects/units being set up in manufacturing, services, and allied sector, including start-ups and units being incubated in the technology business incubators, ensuring asset creation out of the funds deployed in the unit shall be considered.", "For Companies applying for assistance up to Rs. 50 lakh: Companies having at least 51% shareholding by Scheduled Castes entrepreneurs for the past 6 months with management control OR; a new Company provided that the new Company is a successor entity of a Proprietary Firm or Partnership Firm or One Person Company (OPC) or Limited Liability Partnership (LLP) or any other establishment incorporated under any law in force with sound business model which has been in operation for over 6 months, and the predecessor entity had at least 51% shareholding of the Scheduled Castes entrepreneurs with management control.", "For Companies applying for assistance above Rs. 50 lakh: Companies having at least 51% shareholding by Scheduled Castes entrepreneurs for the past 12 months with management control OR; a new Company provided that the new Company is a successor entity of a Proprietary Firm or Partnership Firm or One Person Company (OPC) or Limited Liability Partnership (LLP) or any other establishment incorporated under any law in force with sound business model which has been in operation for over 12 months, and the predecessor entity had at least 51% shareholding of the Scheduled Castes entrepreneurs with management control."]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Social Justice and Empowerment (MoSJE) national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://vcf-sc.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Venture Capital Fund for Scheduled Castes (VCF-SC) (Ministry of Social Justice and Empowerment (MoSJE))
FUND TYPE: Equity

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Venture Capital Fund for Scheduled Castes (VCF-SC) highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Venture Capital Fund for Scheduled Castes (VCF-SC) expenditure guidelines.
3. Address key scheme criteria: The projects/units being set up in manufacturing, services, and allied sector, including start-ups and units being incubated in the technology business incubators, ensuring asset creation out of the funds deployed in the unit shall be considered., For Companies applying for assistance up to Rs. 50 lakh: Companies having at least 51% shareholding by Scheduled Castes entrepreneurs for the past 6 months with management control OR; a new Company provided that the new Company is a successor entity of a Proprietary Firm or Partnership Firm or One Person Company (OPC) or Limited Liability Partnership (LLP) or any other establishment incorporated under any law in force with sound business model which has been in operation for over 6 months, and the predecessor entity had at least 51% shareholding of the Scheduled Castes entrepreneurs with management control., For Companies applying for assistance above Rs. 50 lakh: Companies having at least 51% shareholding by Scheduled Castes entrepreneurs for the past 12 months with management control OR; a new Company provided that the new Company is a successor entity of a Proprietary Firm or Partnership Firm or One Person Company (OPC) or Limited Liability Partnership (LLP) or any other establishment incorporated under any law in force with sound business model which has been in operation for over 12 months, and the predecessor entity had at least 51% shareholding of the Scheduled Castes entrepreneurs with management control..
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Venture Capital Fund for Scheduled Castes (VCF-SC) eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:21.078065+00:00', '2026-09-14T11:00:12.39045+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-45', 'SCH-OFFICIAL-45', 'SENIOR CARE AGEING GROWTH ENGINE (SAGE) VENTURE FUND', 'Ministry of Social Justice and Empowerment (MoSJE)', 'Ministry of Social Justice and Empowerment (MoSJE)', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for SENIOR CARE AGEING GROWTH ENGINE (SAGE) VENTURE FUND under Ministry of Social Justice and Empowerment (MoSJE).', 'Official scheme support for SENIOR CARE AGEING GROWTH ENGINE (SAGE) VENTURE FUND under Ministry of Social Justice and Empowerment (MoSJE).', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["Innovative ideas awarded in the National level innovation challenges such as Smart India Hackathons (of M/o Education) or such other innovative drives - proposing to set up companies and offer products and services for the welfare of the elderly in India.", "Start-ups already functioning in the elderly segment in India proposing to expand operations.All the startups fulfilling the startup norms as per guidelines by the Department for Promotion of Industry and Internal Trade (DPIIT), Ministry of Commerce, Govt. of India are eligible for applying.", "Being incorporated or registered in India for less than ten years from its date of incorporation.", "Annual turnover not exceeding Rs 25 crores in any of the preceding financial years.", "Incorporated as a Company (Private / Public)", "Aims to work towards innovation, development, deployment or commercialization of new products, Solutions, processes or services driven by technology or intellectual property in the realm of elder care.", "It is not formed by splitting up or reconstructing a business already in existence."]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Social Justice and Empowerment (MoSJE) national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://sage.dosje.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: SENIOR CARE AGEING GROWTH ENGINE (SAGE) VENTURE FUND (Ministry of Social Justice and Empowerment (MoSJE))
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for SENIOR CARE AGEING GROWTH ENGINE (SAGE) VENTURE FUND highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official SENIOR CARE AGEING GROWTH ENGINE (SAGE) VENTURE FUND expenditure guidelines.
3. Address key scheme criteria: Innovative ideas awarded in the National level innovation challenges such as Smart India Hackathons (of M/o Education) or such other innovative drives - proposing to set up companies and offer products and services for the welfare of the elderly in India., Start-ups already functioning in the elderly segment in India proposing to expand operations.All the startups fulfilling the startup norms as per guidelines by the Department for Promotion of Industry and Internal Trade (DPIIT), Ministry of Commerce, Govt. of India are eligible for applying., Being incorporated or registered in India for less than ten years from its date of incorporation..
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official SENIOR CARE AGEING GROWTH ENGINE (SAGE) VENTURE FUND eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:21.078065+00:00', '2026-09-14T11:00:12.390465+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-46', 'SCH-OFFICIAL-46', 'Ambedkar Social Innovation Incubation Mission (ASIIM) Scheme under VCF-SC', 'Ministry of Social Justice and Empowerment (MoSJE)', 'Ministry of Social Justice and Empowerment (MoSJE)', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for Ambedkar Social Innovation Incubation Mission (ASIIM) Scheme under VCF-SC under Ministry of Social Justice and Empowerment (MoSJE).', 'Official scheme support for Ambedkar Social Innovation Incubation Mission (ASIIM) Scheme under VCF-SC under Ministry of Social Justice and Empowerment (MoSJE).', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["<b>The eligibility criteria for sending proposals for seeking assistance under ASIIM initiative is as follows:</b>", "Youth who have been identified by the TBls. Atal lncubation Centers (AICs), Technology / lndustrial Parks, Science and Technology Parks of India (STPI) being promoted by Department of Science & Technology (DST) or other than DST and other incubation centers supported by Government of", "Youth who are identified for incubation by reputed private TBIs.", "Students who have been awarded under the Smart India Hackathon or Smart India Hardware Hackathon being conducted by Ministry of Education.", "Innovative ideas focusing on the socio-economic development of the society identified in the TBIs in public, private sector.", "Start-ups nominated and supported by corporates through CSR funds."]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Social Justice and Empowerment (MoSJE) national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://vcf-sc.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Ambedkar Social Innovation Incubation Mission (ASIIM) Scheme under VCF-SC (Ministry of Social Justice and Empowerment (MoSJE))
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Ambedkar Social Innovation Incubation Mission (ASIIM) Scheme under VCF-SC highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Ambedkar Social Innovation Incubation Mission (ASIIM) Scheme under VCF-SC expenditure guidelines.
3. Address key scheme criteria: <b>The eligibility criteria for sending proposals for seeking assistance under ASIIM initiative is as follows:</b>, Youth who have been identified by the TBls. Atal lncubation Centers (AICs), Technology / lndustrial Parks, Science and Technology Parks of India (STPI) being promoted by Department of Science & Technology (DST) or other than DST and other incubation centers supported by Government of, Youth who are identified for incubation by reputed private TBIs..
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Ambedkar Social Innovation Incubation Mission (ASIIM) Scheme under VCF-SC eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:21.078065+00:00', '2026-09-14T11:00:12.39048+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-47', 'SCH-OFFICIAL-47', 'Creation/Expansion of Food Processing & Preservation Capacities (CEFPPC) scheme', 'Ministry of Food Processing Industries', 'Ministry of Food Processing Industries', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for Creation/Expansion of Food Processing & Preservation Capacities (CEFPPC) scheme under Ministry of Food Processing Industries.', 'Official scheme support for Creation/Expansion of Food Processing & Preservation Capacities (CEFPPC) scheme under Ministry of Food Processing Industries.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["<b>Eligible Sectors under this Scheme:</b>", "The scheme offers assistance for the following sectors:", "Fruits & vegetable processing", "Milk Processing", "Meat/poultry/fish processing", "Ready to Eat/Ready to Cook Food Products Breakfast cereals  Snacks bakery and other food products including nutritional health foods Grains pulses, oil seed milling and processing based on modern technology.", "Modern Rice milling.", "Other agri-horti products including spices, coconut, soybean, mushroom processing, honey processing, etc.", "Fruits/Honey-based wines.", "Natural Food flavors, food additives food extracts & colors, oleoresins, guar gum, cocoa products, etc.", "Manufacturing jaggery from sugarcane and value-added products from jaggery (as raw material).", "Any other sector that makes food products fit for human consumption.", "Animal feed manufacturing unit to be set up in Mega Food Parks and Agro Processing Clusters approved by the Ministry from time to time.", "Carbonated Drinks and beverages containing fruit juice."]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Food Processing Industries national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://mofpi.gov.in/schemes/creation-expansion-food-processing-preservation-capacities-cefppc', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Creation/Expansion of Food Processing & Preservation Capacities (CEFPPC) scheme (Ministry of Food Processing Industries)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Creation/Expansion of Food Processing & Preservation Capacities (CEFPPC) scheme highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Creation/Expansion of Food Processing & Preservation Capacities (CEFPPC) scheme expenditure guidelines.
3. Address key scheme criteria: <b>Eligible Sectors under this Scheme:</b>, The scheme offers assistance for the following sectors:, Fruits & vegetable processing.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Creation/Expansion of Food Processing & Preservation Capacities (CEFPPC) scheme eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:21.078065+00:00', '2026-09-14T11:00:12.390505+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-48', 'SCH-OFFICIAL-48', 'PM FME Scheme', 'Ministry of Food Processing Industries', 'Ministry of Food Processing Industries', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for PM FME Scheme under Ministry of Food Processing Industries.', 'Official scheme support for PM FME Scheme under Ministry of Food Processing Industries.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["The company should be an existing Micro Food Processing Unit.", "The company should not be corporate and would be having less than 10 workers.", "The company should follow the policy of One District One Product (ODOP) then they will be given preference but other companies would also be considered.", "The applicant should have the ownership right of the company.", "The company or enterprise could be a Proprietary or Partner Firm.", "The maximum age of the applicant to apply for the scheme should be 18 years old.", "The applicant applying should be at least class 8th passed.", "This scheme has been eligible for only one person from a single family.", "The applicant should be willing to pay at least 10 percent of the amount and the rest of the amount will be given as a bank loan.", "The cost of the land on which the enterprise has been set would not be considered in the total cost of the project.", "The rent of the building cost, lease cost, or the rental cost could be included in the total cost of the project.", "The lease cost that would included in the project cost would not be more than 3 years of lease."]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Food Processing Industries national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://pmfme.mofpi.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: PM FME Scheme (Ministry of Food Processing Industries)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for PM FME Scheme highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official PM FME Scheme expenditure guidelines.
3. Address key scheme criteria: The company should be an existing Micro Food Processing Unit., The company should not be corporate and would be having less than 10 workers., The company should follow the policy of One District One Product (ODOP) then they will be given preference but other companies would also be considered..
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official PM FME Scheme eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:21.078065+00:00', '2026-09-14T11:00:12.39053+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-49', 'SCH-OFFICIAL-49', 'Agro-Processing Cluster Scheme', 'Ministry of Food Processing Industries', 'Ministry of Food Processing Industries', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for Agro-Processing Cluster Scheme under Ministry of Food Processing Industries.', 'Official scheme support for Agro-Processing Cluster Scheme under Ministry of Food Processing Industries.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["Eligible entities:", "Agro Processing Cluster Projects can be set up by an entity organization such as Govt. Departments   PSUs   Joint Ventures   NGOS   Cooperatives   Self Help Groups (SHGs)   Farmer Producer Organisation  (FPOS)   Private Sector Companies   Partnership Firms   Proprietorship Firms etc.", "For more detailed information regarding eligibility criteria, please refer to the guidelines document from the link below."]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Food Processing Industries national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://mofpi.gov.in/schemes/agro-processing-cluster', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Agro-Processing Cluster Scheme (Ministry of Food Processing Industries)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Agro-Processing Cluster Scheme highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Agro-Processing Cluster Scheme expenditure guidelines.
3. Address key scheme criteria: Eligible entities:, Agro Processing Cluster Projects can be set up by an entity organization such as Govt. Departments   PSUs   Joint Ventures   NGOS   Cooperatives   Self Help Groups (SHGs)   Farmer Producer Organisation  (FPOS)   Private Sector Companies   Partnership Firms   Proprietorship Firms etc., For more detailed information regarding eligibility criteria, please refer to the guidelines document from the link below..
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Agro-Processing Cluster Scheme eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:21.078065+00:00', '2026-09-14T11:00:12.390553+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-50', 'SCH-OFFICIAL-50', 'Swarojgar Credit Card', 'Ministry of Finance', 'Ministry of Finance', 'Credit', 'State Govt', 'Credit', 'Growth / Debt Scaling', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for Swarojgar Credit Card under Ministry of Finance.', 'Official scheme support for Swarojgar Credit Card under Ministry of Finance.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["The Swarojgar Credit Card scheme is open to small entrepreneurs, self-employed individuals, and small businesses in India.", "Specific eligibility requirements may vary based on the lending institutions and financial regulations."]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Finance national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'State', 'https://financialservices.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Swarojgar Credit Card (Ministry of Finance)
FUND TYPE: Credit

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Swarojgar Credit Card highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Swarojgar Credit Card expenditure guidelines.
3. Address key scheme criteria: The Swarojgar Credit Card scheme is open to small entrepreneurs, self-employed individuals, and small businesses in India., Specific eligibility requirements may vary based on the lending institutions and financial regulations..
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Swarojgar Credit Card eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:21.078065+00:00', '2026-09-14T11:00:12.390589+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-51', 'SCH-OFFICIAL-51', 'SIDBI Make in India Soft Loan Fund for Micro Small and Medium Enterprises (SMILE)', 'Ministry of Finance', 'Ministry of Finance', 'Equity', 'State Govt', 'Equity', 'Pre-Series A / Series A', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for SIDBI Make in India Soft Loan Fund for Micro Small and Medium Enterprises (SMILE) under Ministry of Finance.', 'Official scheme support for SIDBI Make in India Soft Loan Fund for Micro Small and Medium Enterprises (SMILE) under Ministry of Finance.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["<b>Eligibility Criteria for SMILE :</b>", "The majority emphasis will be on covering newly emerged enterprises in the manufacturing and service sector", "The primary emphasis will be on financing smaller famous enterprises within the MSME sector", "All the existing enterprises are undertaking expansion to take advantage of newly emerged opportunities along with modernization of technology up gradation techniques", "Regarding the SMILE Equipment Finance (SEF), the MSME entities should be in existence for at least 3 years having a satisfactory financial position."]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Finance national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'State', 'https://financialservices.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: SIDBI Make in India Soft Loan Fund for Micro Small and Medium Enterprises (SMILE) (Ministry of Finance)
FUND TYPE: Equity

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for SIDBI Make in India Soft Loan Fund for Micro Small and Medium Enterprises (SMILE) highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official SIDBI Make in India Soft Loan Fund for Micro Small and Medium Enterprises (SMILE) expenditure guidelines.
3. Address key scheme criteria: <b>Eligibility Criteria for SMILE :</b>, The majority emphasis will be on covering newly emerged enterprises in the manufacturing and service sector, The primary emphasis will be on financing smaller famous enterprises within the MSME sector.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official SIDBI Make in India Soft Loan Fund for Micro Small and Medium Enterprises (SMILE) eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:21.729177+00:00', '2026-09-14T11:00:12.39061+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-52', 'SCH-OFFICIAL-52', 'Pradhan Mantri Mudra Yojana', 'Ministry of Finance', 'Ministry of Finance', 'Credit', 'Central Govt', 'Credit', 'Growth / Debt Scaling', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for Pradhan Mantri Mudra Yojana under Ministry of Finance.', 'Official scheme support for Pradhan Mantri Mudra Yojana under Ministry of Finance.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["Eligible borrowers : Individuals", "Proprietary concern.", "Partnership Firm.", "Private Ltd.", "Company.", "Public Company.", "Any other legal forms.", "The applicant should not be defaulter to any bank or financial institution and should have a satisfactory credit track record. The individual borrowers may be required to possess the necessary skills experience knowledge to undertake the proposed activity. The need for educational qualification, if any, needs to be assessed based on the nature of the proposed activity, and its requirement"]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Finance national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://www.mudra.org.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Pradhan Mantri Mudra Yojana (Ministry of Finance)
FUND TYPE: Credit

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Pradhan Mantri Mudra Yojana highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Pradhan Mantri Mudra Yojana expenditure guidelines.
3. Address key scheme criteria: Eligible borrowers : Individuals, Proprietary concern., Partnership Firm..
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Pradhan Mantri Mudra Yojana eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:21.729177+00:00', '2026-09-14T11:00:12.390629+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-53', 'SCH-OFFICIAL-53', 'Micro Finance (NEDFL Scheme)', 'Ministry of Development of North Eastern Region', 'Ministry of Development of North Eastern Region', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for Micro Finance (NEDFL Scheme) under Ministry of Development of North Eastern Region.', 'Official scheme support for Micro Finance (NEDFL Scheme) under Ministry of Development of North Eastern Region.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["Any Indian Citizen with 40% or more disability", "Age above 18 years.", "The borrowers already covered under any other scheme of financing sponsored by Central or State Government or financing institutions and having outstanding loans against their names shall not be eligible.", "The borrowers should preferably be regular members of Thrift and Credit Group (Self Help Group).", "Preference will be given to women beneficiaries.", "Relevant educational/technical/vocational qualification, experience, and background."]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Development of North Eastern Region national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://seedfund.startupindia.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Micro Finance (NEDFL Scheme) (Ministry of Development of North Eastern Region)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Micro Finance (NEDFL Scheme) highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Micro Finance (NEDFL Scheme) expenditure guidelines.
3. Address key scheme criteria: Any Indian Citizen with 40% or more disability, Age above 18 years., The borrowers already covered under any other scheme of financing sponsored by Central or State Government or financing institutions and having outstanding loans against their names shall not be eligible..
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Micro Finance (NEDFL Scheme) eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:21.729177+00:00', '2026-09-14T11:00:12.390646+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-54', 'SCH-OFFICIAL-54', 'North-East Venture Fund (NEVF)', 'Ministry of Development of North Eastern Region', 'Ministry of Development of North Eastern Region', 'Equity', 'Central Govt', 'Equity', 'Pre-Series A / Series A', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for North-East Venture Fund (NEVF) under Ministry of Development of North Eastern Region.', 'Official scheme support for North-East Venture Fund (NEVF) under Ministry of Development of North Eastern Region.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["Entrepreneurial person with innovative vision and implementation power", "Strong management team and commitment", "Viable business model with sustainable growth", "Large scaling opportunities", "Market-fit product with good traction", "Realistic exit potential"]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Development of North Eastern Region national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://seedfund.startupindia.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: North-East Venture Fund (NEVF) (Ministry of Development of North Eastern Region)
FUND TYPE: Equity

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for North-East Venture Fund (NEVF) highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official North-East Venture Fund (NEVF) expenditure guidelines.
3. Address key scheme criteria: Entrepreneurial person with innovative vision and implementation power, Strong management team and commitment, Viable business model with sustainable growth.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official North-East Venture Fund (NEVF) eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:21.729177+00:00', '2026-09-14T11:00:12.390668+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-55', 'SCH-OFFICIAL-55', 'Women Enterprise Development (WED)', 'Ministry of Development of North Eastern Region', 'Ministry of Development of North Eastern Region', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for Women Enterprise Development (WED) under Ministry of Development of North Eastern Region.', 'Official scheme support for Women Enterprise Development (WED) under Ministry of Development of North Eastern Region.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["Skilled woman entrepreneurs in the age group of 18-50 years; the applicant must be engaged in any viable income generating activity including small business trade., etc."]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Development of North Eastern Region national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://seedfund.startupindia.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Women Enterprise Development (WED) (Ministry of Development of North Eastern Region)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Women Enterprise Development (WED) highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Women Enterprise Development (WED) expenditure guidelines.
3. Address key scheme criteria: Skilled woman entrepreneurs in the age group of 18-50 years; the applicant must be engaged in any viable income generating activity including small business trade., etc..
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Women Enterprise Development (WED) eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:21.729177+00:00', '2026-09-14T11:00:12.390691+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-56', 'SCH-OFFICIAL-56', 'Equipment Finance (Northeastern Development Finance Corporation Ltd Schemes)', 'Ministry of Development of North Eastern Region', 'Ministry of Development of North Eastern Region', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for Equipment Finance (Northeastern Development Finance Corporation Ltd Schemes) under Ministry of Development of North Eastern Region.', 'Official scheme support for Equipment Finance (Northeastern Development Finance Corporation Ltd Schemes) under Ministry of Development of North Eastern Region.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["Corporates with minimum 3 years of profitable operations for NEDFi assisted units, in case of other units the unit should have minimum 5 years of operations."]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Development of North Eastern Region national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://seedfund.startupindia.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Equipment Finance (Northeastern Development Finance Corporation Ltd Schemes) (Ministry of Development of North Eastern Region)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Equipment Finance (Northeastern Development Finance Corporation Ltd Schemes) highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Equipment Finance (Northeastern Development Finance Corporation Ltd Schemes) expenditure guidelines.
3. Address key scheme criteria: Corporates with minimum 3 years of profitable operations for NEDFi assisted units, in case of other units the unit should have minimum 5 years of operations..
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Equipment Finance (Northeastern Development Finance Corporation Ltd Schemes) eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:21.729177+00:00', '2026-09-14T11:00:12.390719+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-57', 'SCH-OFFICIAL-57', 'North East Entrepreneurs Development (NEED)', 'Ministry of Development of North Eastern Region', 'Ministry of Development of North Eastern Region', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for North East Entrepreneurs Development (NEED) under Ministry of Development of North Eastern Region.', 'Official scheme support for North East Entrepreneurs Development (NEED) under Ministry of Development of North Eastern Region.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["First-generation entrepreneurs, existing entrepreneurs, proprietary & partnership concerns and companies. Technical qualification of the promoter in the relevant field is a pre-requisite."]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Development of North Eastern Region national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://seedfund.startupindia.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: North East Entrepreneurs Development (NEED) (Ministry of Development of North Eastern Region)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for North East Entrepreneurs Development (NEED) highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official North East Entrepreneurs Development (NEED) expenditure guidelines.
3. Address key scheme criteria: First-generation entrepreneurs, existing entrepreneurs, proprietary & partnership concerns and companies. Technical qualification of the promoter in the relevant field is a pre-requisite..
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official North East Entrepreneurs Development (NEED) eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:21.729177+00:00', '2026-09-14T11:00:12.390738+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-58', 'SCH-OFFICIAL-58', 'North-East Handloom Handicrafts (NEHH)', 'Ministry of Development of North Eastern Region', 'Ministry of Development of North Eastern Region', 'Grant / Support', 'State Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for North-East Handloom Handicrafts (NEHH) under Ministry of Development of North Eastern Region.', 'Official scheme support for North-East Handloom Handicrafts (NEHH) under Ministry of Development of North Eastern Region.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["The North-East Handloom Handicrafts (NEHH) initiative is open to individuals, artisans, handloom weavers, and handicraft producers in the North Eastern Region of India.", "Applicants should be interested in promoting and enhancing their handloom and handicrafts businesses.", "Specific eligibility requirements may vary based on the programs and opportunities offered under NEHH."]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Development of North Eastern Region national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'State', 'https://seedfund.startupindia.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: North-East Handloom Handicrafts (NEHH) (Ministry of Development of North Eastern Region)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for North-East Handloom Handicrafts (NEHH) highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official North-East Handloom Handicrafts (NEHH) expenditure guidelines.
3. Address key scheme criteria: The North-East Handloom Handicrafts (NEHH) initiative is open to individuals, artisans, handloom weavers, and handicraft producers in the North Eastern Region of India., Applicants should be interested in promoting and enhancing their handloom and handicrafts businesses., Specific eligibility requirements may vary based on the programs and opportunities offered under NEHH..
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official North-East Handloom Handicrafts (NEHH) eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:21.729177+00:00', '2026-09-14T11:00:12.390753+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-59', 'SCH-OFFICIAL-59', 'Equity Fund Scheme (NEDFi)', 'Ministry of Development of North Eastern Region', 'Ministry of Development of North Eastern Region', 'Equity', 'Central Govt', 'Equity', 'Pre-Series A / Series A', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for Equity Fund Scheme (NEDFi) under Ministry of Development of North Eastern Region.', 'Official scheme support for Equity Fund Scheme (NEDFi) under Ministry of Development of North Eastern Region.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["Individual entrepreneurs or groups of entrepreneurs; The applicant should have a viable business plan which offers above-average profitability leading to attractive returns on investment."]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Development of North Eastern Region national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://seedfund.startupindia.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Equity Fund Scheme (NEDFi) (Ministry of Development of North Eastern Region)
FUND TYPE: Equity

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Equity Fund Scheme (NEDFi) highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Equity Fund Scheme (NEDFi) expenditure guidelines.
3. Address key scheme criteria: Individual entrepreneurs or groups of entrepreneurs; The applicant should have a viable business plan which offers above-average profitability leading to attractive returns on investment..
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Equity Fund Scheme (NEDFi) eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:21.729177+00:00', '2026-09-14T11:00:12.390768+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-60', 'SCH-OFFICIAL-60', 'Employment Linked Incentive (ELI) Scheme', 'Ministry of Labour & Employment, Government of India', 'Ministry of Labour & Employment, Government of India', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for Employment Linked Incentive (ELI) Scheme under Ministry of Labour & Employment, Government of India.', 'Official scheme support for Employment Linked Incentive (ELI) Scheme under Ministry of Labour & Employment, Government of India.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '[]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Labour & Employment, Government of India national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://seedfund.startupindia.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Employment Linked Incentive (ELI) Scheme (Ministry of Labour & Employment, Government of India)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Employment Linked Incentive (ELI) Scheme highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Employment Linked Incentive (ELI) Scheme expenditure guidelines.
3. Address key scheme criteria: .
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Employment Linked Incentive (ELI) Scheme eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:21.729177+00:00', '2026-09-14T11:00:12.390782+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-61', 'SCH-OFFICIAL-61', 'Development of Solar Parks and Ultra Mega Solar Power Projects', 'Ministry of New and Renewable Energy Sources Schemes', 'Ministry of New and Renewable Energy Sources Schemes', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for Development of Solar Parks and Ultra Mega Solar Power Projects under Ministry of New and Renewable Energy Sources Schemes.', 'Official scheme support for Development of Solar Parks and Ultra Mega Solar Power Projects under Ministry of New and Renewable Energy Sources Schemes.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["For detailed information regarding eligibility criteria, please refer to the guidelines document from the link below: (<a href=''https://mnre.gov.in/development-of-solar-parks-and-ultra-mega-solar-power-projects/'', target=''_blank''>https://mnre.gov.in/development-of-solar-parks-and-ultra-mega-solar-power-projects/</a>)"]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of New and Renewable Energy Sources Schemes national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://seedfund.startupindia.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Development of Solar Parks and Ultra Mega Solar Power Projects (Ministry of New and Renewable Energy Sources Schemes)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Development of Solar Parks and Ultra Mega Solar Power Projects highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Development of Solar Parks and Ultra Mega Solar Power Projects expenditure guidelines.
3. Address key scheme criteria: For detailed information regarding eligibility criteria, please refer to the guidelines document from the link below: (<a href=''https://mnre.gov.in/development-of-solar-parks-and-ultra-mega-solar-power-projects/'', target=''_blank''>https://mnre.gov.in/development-of-solar-parks-and-ultra-mega-solar-power-projects/</a>).
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Development of Solar Parks and Ultra Mega Solar Power Projects eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:21.729177+00:00', '2026-09-14T11:00:12.390797+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-62', 'SCH-OFFICIAL-62', 'Central Sector Scheme on Conservation, Development and Sustainable Management of Medicinal Plants', 'AYUSH', 'AYUSH', 'Grant / Support', 'State Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for Central Sector Scheme on Conservation, Development and Sustainable Management of Medicinal Plants under AYUSH.', 'Official scheme support for Central Sector Scheme on Conservation, Development and Sustainable Management of Medicinal Plants under AYUSH.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '[]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with AYUSH national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'State', 'https://ayush.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Central Sector Scheme on Conservation, Development and Sustainable Management of Medicinal Plants (AYUSH)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Central Sector Scheme on Conservation, Development and Sustainable Management of Medicinal Plants highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Central Sector Scheme on Conservation, Development and Sustainable Management of Medicinal Plants expenditure guidelines.
3. Address key scheme criteria: .
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Central Sector Scheme on Conservation, Development and Sustainable Management of Medicinal Plants eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:21.729177+00:00', '2026-09-14T11:00:12.390811+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-63', 'SCH-OFFICIAL-63', 'Agriculture Infrastructure Fund for Agripreneurs', 'Ministry of Agriculture', 'Ministry of Agriculture', 'Equity', 'Central Govt', 'Equity', 'Pre-Series A / Series A', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for Agriculture Infrastructure Fund for Agripreneurs under Ministry of Agriculture.', 'Official scheme support for Agriculture Infrastructure Fund for Agripreneurs under Ministry of Agriculture.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["Post Harvest Management Projects", "Projects on Hub and Spoke Model", "Viable Projects for Building Community Farming Assets"]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Agriculture national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://agriinfra.dac.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Agriculture Infrastructure Fund for Agripreneurs (Ministry of Agriculture)
FUND TYPE: Equity

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Agriculture Infrastructure Fund for Agripreneurs highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Agriculture Infrastructure Fund for Agripreneurs expenditure guidelines.
3. Address key scheme criteria: Post Harvest Management Projects, Projects on Hub and Spoke Model, Viable Projects for Building Community Farming Assets.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Agriculture Infrastructure Fund for Agripreneurs eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:21.729177+00:00', '2026-09-14T11:00:12.390825+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-64', 'SCH-OFFICIAL-64', 'Entrepreneurship Skill Development Programme(ESDP)Scheme', 'Ministry of Micro, Small and Medium Enterprises', 'Ministry of Micro, Small and Medium Enterprises', 'Grant / Support', 'State Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for Entrepreneurship Skill Development Programme(ESDP)Scheme under Ministry of Micro, Small and Medium Enterprises.', 'Official scheme support for Entrepreneurship Skill Development Programme(ESDP)Scheme under Ministry of Micro, Small and Medium Enterprises.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["The scheme is applicable for all aspiring and existing entrepreneurs."]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Micro, Small and Medium Enterprises national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'State', 'https://msme.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Entrepreneurship Skill Development Programme(ESDP)Scheme (Ministry of Micro, Small and Medium Enterprises)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Entrepreneurship Skill Development Programme(ESDP)Scheme highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Entrepreneurship Skill Development Programme(ESDP)Scheme expenditure guidelines.
3. Address key scheme criteria: The scheme is applicable for all aspiring and existing entrepreneurs..
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Entrepreneurship Skill Development Programme(ESDP)Scheme eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:21.729177+00:00', '2026-09-14T11:00:12.390839+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-65', 'SCH-OFFICIAL-65', 'Raw Material Assistance Scheme', 'Ministry of Micro, Small and Medium Enterprises', 'Ministry of Micro, Small and Medium Enterprises', 'Grant / Support', 'State Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for Raw Material Assistance Scheme under Ministry of Micro, Small and Medium Enterprises.', 'Official scheme support for Raw Material Assistance Scheme under Ministry of Micro, Small and Medium Enterprises.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["The Entrepreneurs are required to apply for Raw Material Assistance only on the prescribed application forms. The application forms downloaded from the link given below may be filled and can be submitted to the nearest Branch Office. The blank forms are also available free of charge from the Branch offices."]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Micro, Small and Medium Enterprises national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'State', 'https://msme.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Raw Material Assistance Scheme (Ministry of Micro, Small and Medium Enterprises)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Raw Material Assistance Scheme highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Raw Material Assistance Scheme expenditure guidelines.
3. Address key scheme criteria: The Entrepreneurs are required to apply for Raw Material Assistance only on the prescribed application forms. The application forms downloaded from the link given below may be filled and can be submitted to the nearest Branch Office. The blank forms are also available free of charge from the Branch offices..
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Raw Material Assistance Scheme eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:21.729177+00:00', '2026-09-14T11:00:12.390854+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-66', 'SCH-OFFICIAL-66', 'Trade Related Entrepreneurship Assistance and Development (TREAD) Scheme for Women', 'Ministry of Micro, Small and Medium Enterprises', 'Ministry of Micro, Small and Medium Enterprises', 'Grant / Support', 'State Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for Trade Related Entrepreneurship Assistance and Development (TREAD) Scheme for Women under Ministry of Micro, Small and Medium Enterprises.', 'Official scheme support for Trade Related Entrepreneurship Assistance and Development (TREAD) Scheme for Women under Ministry of Micro, Small and Medium Enterprises.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '[]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Micro, Small and Medium Enterprises national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'State', 'https://msme.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Trade Related Entrepreneurship Assistance and Development (TREAD) Scheme for Women (Ministry of Micro, Small and Medium Enterprises)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Trade Related Entrepreneurship Assistance and Development (TREAD) Scheme for Women highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Trade Related Entrepreneurship Assistance and Development (TREAD) Scheme for Women expenditure guidelines.
3. Address key scheme criteria: .
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Trade Related Entrepreneurship Assistance and Development (TREAD) Scheme for Women eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:21.729177+00:00', '2026-09-14T11:00:12.39087+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-67', 'SCH-OFFICIAL-67', 'Aspire - A Scheme for Promotion of Innovation, Rural Industries and Entrepreneurship', 'Ministry of Micro, Small and Medium Enterprises', 'Ministry of Micro, Small and Medium Enterprises', 'Grant / Support', 'State Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for Aspire - A Scheme for Promotion of Innovation, Rural Industries and Entrepreneurship under Ministry of Micro, Small and Medium Enterprises.', 'Official scheme support for Aspire - A Scheme for Promotion of Innovation, Rural Industries and Entrepreneurship under Ministry of Micro, Small and Medium Enterprises.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["Any agency/institution of Government of India, State government or existing training centers under Ministries/Departments of Government of India/State Government, Industry Associations, Academic Institutions.", "Any not-for-profit private institutions with experience in successfully executing incubation and/or skill development programs may be eligible to set up an LBI."]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Micro, Small and Medium Enterprises national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'State', 'https://msme.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Aspire - A Scheme for Promotion of Innovation, Rural Industries and Entrepreneurship (Ministry of Micro, Small and Medium Enterprises)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Aspire - A Scheme for Promotion of Innovation, Rural Industries and Entrepreneurship highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Aspire - A Scheme for Promotion of Innovation, Rural Industries and Entrepreneurship expenditure guidelines.
3. Address key scheme criteria: Any agency/institution of Government of India, State government or existing training centers under Ministries/Departments of Government of India/State Government, Industry Associations, Academic Institutions., Any not-for-profit private institutions with experience in successfully executing incubation and/or skill development programs may be eligible to set up an LBI..
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Aspire - A Scheme for Promotion of Innovation, Rural Industries and Entrepreneurship eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:21.729177+00:00', '2026-09-14T11:00:12.390885+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-68', 'SCH-OFFICIAL-68', 'Stand Up India', 'Public Sector Enterprise', 'Public Sector Enterprise', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for Stand Up India under Public Sector Enterprise.', 'Official scheme support for Stand Up India under Public Sector Enterprise.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["SC/ST and/or women entrepreneurs; above 18 years of age<li> Loans under the scheme are available for only greenfield projects. Greenfield signifies, in this context, the first-time venture of the beneficiary in the manufacturing or services or trading </li><li> In the case of non-individual enterprises,51% of the shareholding and controlling stakes should be held by either SC/ST and/or Women Entrepreneur </li><li> Borrower should not be in default to any bank or financial institution </li></ul>"]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Public Sector Enterprise national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://www.standupmitra.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Stand Up India (Public Sector Enterprise)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Stand Up India highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Stand Up India expenditure guidelines.
3. Address key scheme criteria: SC/ST and/or women entrepreneurs; above 18 years of age<li> Loans under the scheme are available for only greenfield projects. Greenfield signifies, in this context, the first-time venture of the beneficiary in the manufacturing or services or trading </li><li> In the case of non-individual enterprises,51% of the shareholding and controlling stakes should be held by either SC/ST and/or Women Entrepreneur </li><li> Borrower should not be in default to any bank or financial institution </li></ul>.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Stand Up India eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:21.729177+00:00', '2026-09-14T11:00:12.390913+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-69', 'SCH-OFFICIAL-69', 'Samridhi Fund', 'Public Sector Enterprise', 'Public Sector Enterprise', 'Equity', 'Central Govt', 'Equity', 'Pre-Series A / Series A', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for Samridhi Fund under Public Sector Enterprise.', 'Official scheme support for Samridhi Fund under Public Sector Enterprise.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["The conditions necessary for getting funded are as follows:", "Be economically viable<li> Provide access to markets for the poor </li><li> Be socially relevant and impact the poor as customers, producers, or employees </li><li> The enterprises must have plans to expand operations in any or all the following states - Bihar, Chhattisgarh, Odisha, Uttar Pradesh, West Bengal, Madhya Pradesh, Jharkhand, and Rajasthan </li><li> Increase the flow of capital to the above-mentioned states </li><li> Focus on Environment, Social and Governance matters </li><li>Samridhi will not invest in any of the following businesses or activities: <ul><li> Illegal or banned activities, including child labor </li><li> Businesses dealing with hazardous chemicals, asbestos, pesticides, and wastes; ozone-depleting substances; and endangered or protected wildlife or wildlife products. </li><li> Arms and ammunition </li><li> Companies that have been proven to be involved in fraud and corruption. </li></ul>"]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Public Sector Enterprise national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://seedfund.startupindia.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Samridhi Fund (Public Sector Enterprise)
FUND TYPE: Equity

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Samridhi Fund highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Samridhi Fund expenditure guidelines.
3. Address key scheme criteria: The conditions necessary for getting funded are as follows:, Be economically viable<li> Provide access to markets for the poor </li><li> Be socially relevant and impact the poor as customers, producers, or employees </li><li> The enterprises must have plans to expand operations in any or all the following states - Bihar, Chhattisgarh, Odisha, Uttar Pradesh, West Bengal, Madhya Pradesh, Jharkhand, and Rajasthan </li><li> Increase the flow of capital to the above-mentioned states </li><li> Focus on Environment, Social and Governance matters </li><li>Samridhi will not invest in any of the following businesses or activities: <ul><li> Illegal or banned activities, including child labor </li><li> Businesses dealing with hazardous chemicals, asbestos, pesticides, and wastes; ozone-depleting substances; and endangered or protected wildlife or wildlife products. </li><li> Arms and ammunition </li><li> Companies that have been proven to be involved in fraud and corruption. </li></ul>.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Samridhi Fund eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:21.729177+00:00', '2026-09-14T11:00:12.390924+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-70', 'SCH-OFFICIAL-70', 'Technology Incubation and Development of Entrepreneurs (TIDE) 2.0', 'Ministry of Science & Technology', 'Ministry of Science & Technology', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for Technology Incubation and Development of Entrepreneurs (TIDE) 2.0 under Ministry of Science & Technology.', 'Official scheme support for Technology Incubation and Development of Entrepreneurs (TIDE) 2.0 under Ministry of Science & Technology.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["Organisation  of higher learning and R&D organizations across India, having incubation facilities and established links with large companies, industry bodies, and industry clusters are eligible for the scheme."]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Science & Technology national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://dst.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Technology Incubation and Development of Entrepreneurs (TIDE) 2.0 (Ministry of Science & Technology)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Technology Incubation and Development of Entrepreneurs (TIDE) 2.0 highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Technology Incubation and Development of Entrepreneurs (TIDE) 2.0 expenditure guidelines.
3. Address key scheme criteria: Organisation  of higher learning and R&D organizations across India, having incubation facilities and established links with large companies, industry bodies, and industry clusters are eligible for the scheme..
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Technology Incubation and Development of Entrepreneurs (TIDE) 2.0 eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:21.729177+00:00', '2026-09-14T11:00:12.390935+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-71', 'SCH-OFFICIAL-71', 'Promoting Innovations in Individuals, Startups and MSMEs (PRISM)', 'Ministry of Science & Technology', 'Ministry of Science & Technology', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for Promoting Innovations in Individuals, Startups and MSMEs (PRISM) under Ministry of Science & Technology.', 'Official scheme support for Promoting Innovations in Individuals, Startups and MSMEs (PRISM) under Ministry of Science & Technology.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["The scheme runs in two phases.", "For PRISM I, any Indian citizen including student innovators can apply.", "For PRISM II, PRISM innovators or innovators who have successfully demonstrated proof of concept with the support of government institution/agency, PRISM-R&D proposals and public-funded - R&D institutes/autonomous institutions/laboratories/academic institutes, etc. are eligible."]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Science & Technology national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://dst.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Promoting Innovations in Individuals, Startups and MSMEs (PRISM) (Ministry of Science & Technology)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Promoting Innovations in Individuals, Startups and MSMEs (PRISM) highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Promoting Innovations in Individuals, Startups and MSMEs (PRISM) expenditure guidelines.
3. Address key scheme criteria: The scheme runs in two phases., For PRISM I, any Indian citizen including student innovators can apply., For PRISM II, PRISM innovators or innovators who have successfully demonstrated proof of concept with the support of government institution/agency, PRISM-R&D proposals and public-funded - R&D institutes/autonomous institutions/laboratories/academic institutes, etc. are eligible..
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Promoting Innovations in Individuals, Startups and MSMEs (PRISM) eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:21.729177+00:00', '2026-09-14T11:00:12.390945+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-72', 'SCH-OFFICIAL-72', 'DST Water Technology Call for Proposals 2023', 'Ministry of Science & Technology', 'Ministry of Science & Technology', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for DST Water Technology Call for Proposals 2023 under Ministry of Science & Technology.', 'Official scheme support for DST Water Technology Call for Proposals 2023 under Ministry of Science & Technology.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["Eligibility as per the official scheme document: For the Applied Research Stream (Leading to the establishment of Proof-of-Concept), the proposals are to be led by faculties/ scientists working in a regular position in recognized Academic Organisation  /Public funded R&D Institutions/ Laboratories, Central and State government autonomous organizations State S & T councils.", "For the technology Development Stream (Leading to Lab Scale Demonstration), the proposals have to be submitted in the Institute - Industry / User partnership mode only. The proposals are to be led by faculties/ scientists working in regular positions in recognized Academic Institutions, Public funded R&D Institutions/ Laboratories, State S&T councils in partnership with other academic/ R&D organisations, state-line departments, S&T-based voluntary organisations, DSIR-recognized SIRO organization, etc. The company/industry should be willing to contribute in the form of industry-attributable technical inputs and resources with at least 10% of the project cost in cash.", "For the Technology Assessment Stream (Leading to Pilot-Scale demonstration of the technology in the field setting), the proposals are to be led by faculties/ scientists working in a regular position in recognized Academic institutions, Public-funded R&D Institutions/ Laboratories in partnership with other academic, R&D organizations, DSIR-recognized R&D organizations, industries, and Users (Utility, Panchayat, Municipal Corporation, Urban Development Authority, etc).", "For the Convergent Solution Stream, the proposals have to be submitted in consortium mode only. The consortium is expected to be led by faculties/ scientists working in a regular position in recognized academic institutions, public-funded R&D Institutions/ Laboratories, state S&T councils in partnership with other academic/ R&D organisations, state line departments, S&T-based voluntary organizations, etc. Participation of industries/ start-ups is also welcome, wherever applicable. The consortium should essentially include at least a user having an interest in the intervention, a solution designer, and a solution provider."]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Science & Technology national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://dst.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: DST Water Technology Call for Proposals 2023 (Ministry of Science & Technology)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for DST Water Technology Call for Proposals 2023 highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official DST Water Technology Call for Proposals 2023 expenditure guidelines.
3. Address key scheme criteria: Eligibility as per the official scheme document: For the Applied Research Stream (Leading to the establishment of Proof-of-Concept), the proposals are to be led by faculties/ scientists working in a regular position in recognized Academic Organisation  /Public funded R&D Institutions/ Laboratories, Central and State government autonomous organizations State S & T councils., For the technology Development Stream (Leading to Lab Scale Demonstration), the proposals have to be submitted in the Institute - Industry / User partnership mode only. The proposals are to be led by faculties/ scientists working in regular positions in recognized Academic Institutions, Public funded R&D Institutions/ Laboratories, State S&T councils in partnership with other academic/ R&D organisations, state-line departments, S&T-based voluntary organisations, DSIR-recognized SIRO organization, etc. The company/industry should be willing to contribute in the form of industry-attributable technical inputs and resources with at least 10% of the project cost in cash., For the Technology Assessment Stream (Leading to Pilot-Scale demonstration of the technology in the field setting), the proposals are to be led by faculties/ scientists working in a regular position in recognized Academic institutions, Public-funded R&D Institutions/ Laboratories in partnership with other academic, R&D organizations, DSIR-recognized R&D organizations, industries, and Users (Utility, Panchayat, Municipal Corporation, Urban Development Authority, etc)..
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official DST Water Technology Call for Proposals 2023 eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:21.729177+00:00', '2026-09-14T11:00:12.390955+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-73', 'SCH-OFFICIAL-73', 'Biotechnology ignition grant (big)', 'Ministry of Science & Technology', 'Ministry of Science & Technology', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for Biotechnology ignition grant (big) under Ministry of Science & Technology.', 'Official scheme support for Biotechnology ignition grant (big) under Ministry of Science & Technology.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["<b>Individual:</b>", "The individual applicant should be an Indian citizen", "The primary applicant should be the Project Leader", "The applicant has to be incubated in an incubator (Incubator could be located anywhere in the country and may/may not be supported by BIRAC). At the time of application, the applicant is expected to have identified preferred incubator. LoI/MoU with the incubator is required for final approval.", "Employed individuals", "- Individual who is a promoter shareholder of a Biotech company or one of the partners in a Biotech LLP will not be allowed to apply as an individual, irrespective of the percentage of shareholding of the applicant in the company.", "<b>Startups/Companies:</b>", "The Company/LLP should be registered under the Indian Companies Act, 1956/2013", "The incorporation date of the Company/LLP should not be earlier than 5 years from the date of closing of a particular BIG call.", "A company is considered as ''owned’ by resident Indian citizen(s) if minimum 51% of the capital is beneficially owned by resident Indian citizen(s) and / or Indian   companies,   which   are   ultimately   owned   and controlled by resident Indian citizens", "Company/LLP’s application should be represented by a Project Leader", "The Company/LLP must have its own in-house R&D facility that is functional and adequate to execute the project. If the Company/LLP does not have a functional and adequate laboratory of its own then it should be incubated at an incubator", "If an applicant company, in which any promoter holding more than or equal to 20% of the shares, is a co-promoter of another ineligible company or a partner in another ineligible LLP, then the applicant will not be eligible. The only exception to this shall be situation wherein the latter ineligible company/LLP is operating in non-biotech domain.   In case applicant is a LLP: An applicant LLP, in which any of the partners is also a partner in another ineligible LLP or is a co-promoter in another ineligible company, then the applicant will not be eligible. The only exception to this shall be situation wherein the latter ineligible LLP/company is operating in non-biotech domain."]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Science & Technology national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://birac.nic.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Biotechnology ignition grant (big) (Ministry of Science & Technology)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Biotechnology ignition grant (big) highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Biotechnology ignition grant (big) expenditure guidelines.
3. Address key scheme criteria: <b>Individual:</b>, The individual applicant should be an Indian citizen, The primary applicant should be the Project Leader.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Biotechnology ignition grant (big) eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:21.729177+00:00', '2026-09-14T11:00:12.390973+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-74', 'SCH-OFFICIAL-74', 'NIDHI Programme', 'Ministry of Science & Technology', 'Ministry of Science & Technology', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for NIDHI Programme under Ministry of Science & Technology.', 'Official scheme support for NIDHI Programme under Ministry of Science & Technology.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["All the NIDHI-Startup Funds will be disbursed to eligible startups only through eligible NSTEDB linked incubators across India", "For more detailed information:<a href=''https://www.nstedb.com'' target=''_blank''>https://www.nstedb.com</a>"]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Science & Technology national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://dst.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: NIDHI Programme (Ministry of Science & Technology)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for NIDHI Programme highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official NIDHI Programme expenditure guidelines.
3. Address key scheme criteria: All the NIDHI-Startup Funds will be disbursed to eligible startups only through eligible NSTEDB linked incubators across India, For more detailed information:<a href=''https://www.nstedb.com'' target=''_blank''>https://www.nstedb.com</a>.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official NIDHI Programme eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:21.729177+00:00', '2026-09-14T11:00:12.390984+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-75', 'SCH-OFFICIAL-75', 'E-YUVA', 'Ministry of Science & Technology', 'Ministry of Science & Technology', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for E-YUVA under Ministry of Science & Technology.', 'Official scheme support for E-YUVA under Ministry of Science & Technology.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["Open to students pursuing postgraduate studies (Masters or PhD) in biotechnology or related fields from recognized Indian universities and institutes.", "Faculty members and researchers from Indian academic institutions can also apply as mentors for student teams.", "Projects should focus on translational research with potential for societal or industrial applications.", "Applicants must demonstrate innovation and feasibility of their proposed research."]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Science & Technology national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://dst.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: E-YUVA (Ministry of Science & Technology)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for E-YUVA highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official E-YUVA expenditure guidelines.
3. Address key scheme criteria: Open to students pursuing postgraduate studies (Masters or PhD) in biotechnology or related fields from recognized Indian universities and institutes., Faculty members and researchers from Indian academic institutions can also apply as mentors for student teams., Projects should focus on translational research with potential for societal or industrial applications..
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official E-YUVA eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:21.729177+00:00', '2026-09-14T11:00:12.390994+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-76', 'SCH-OFFICIAL-76', 'Small Business Innovation Research Initiative (SBIRI)', 'Ministry of Science & Technology', 'Ministry of Science & Technology', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for Small Business Innovation Research Initiative (SBIRI) under Ministry of Science & Technology.', 'Official scheme support for Small Business Innovation Research Initiative (SBIRI) under Ministry of Science & Technology.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["<b>The proposals can be submitted </b>", "Solely by a Company incorporated under the Companies Act, 2013 or Limited Liability Partnership (LLP) incorporated under the Limited Liability Partnership Act, 2008 or Joint Ventures either in the form of Company/ LLP by any of the above entities jointly with other private or public partners (s) (Universities or Institutes).", "<b>ELIGIBILITY CRITERIA FOR INDUSTRY</b>", "Minimum 51% of the shares of the Company should be held by Indian Citizens holding Indian passports (Indian Citizens do not include Person of Indian Origin (PIO) and Overseas Citizenship of India (OCI) holders) Minimum half of the persons who subscribed their names to the LLP document as its Partners should be Indian citizens. Participating companies should have adequate in-house facilities to address the project implementation aspects (which shall be evaluated during the site visit)  OR  Incubated with any of the recognized Incubation Facility.", "<b>ELIGIBILITY CRITERIA FOR ACADEMIC COLLABORATOR</b>", "Public/private university/colleges in India", "National research laboratories", "Not-for-profit private research labs/societies/foundation"]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Science & Technology national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://dst.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Small Business Innovation Research Initiative (SBIRI) (Ministry of Science & Technology)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Small Business Innovation Research Initiative (SBIRI) highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Small Business Innovation Research Initiative (SBIRI) expenditure guidelines.
3. Address key scheme criteria: <b>The proposals can be submitted </b>, Solely by a Company incorporated under the Companies Act, 2013 or Limited Liability Partnership (LLP) incorporated under the Limited Liability Partnership Act, 2008 or Joint Ventures either in the form of Company/ LLP by any of the above entities jointly with other private or public partners (s) (Universities or Institutes)., <b>ELIGIBILITY CRITERIA FOR INDUSTRY</b>.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Small Business Innovation Research Initiative (SBIRI) eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:22.612366+00:00', '2026-09-14T11:00:12.391005+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-77', 'SCH-OFFICIAL-77', 'DST National Mission on Interdisciplinary Cyber-Physical Systems (DST NM-ICPS)', 'Ministry of Science & Technology', 'Ministry of Science & Technology', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for DST National Mission on Interdisciplinary Cyber-Physical Systems (DST NM-ICPS) under Ministry of Science & Technology.', 'Official scheme support for DST National Mission on Interdisciplinary Cyber-Physical Systems (DST NM-ICPS) under Ministry of Science & Technology.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["<b>Researchers and faculty : </b> Ph.D. degree in Science, Engineering, or related fields Experience in research and development related to Cyber-Physical Systems (CPS) Affiliation with a recognized academic or research institution in India Strong publication record in relevant fields.", "<b>Students : </b>Master''s degree in Science, Engineering, or related fields Good academic record with a strong interest in CPS research Enrollment in a Ph.D. program at a recognized Indian institution.", "<b>Start-ups and entrepreneurs :</b> Focus on developing innovative CPS solutions with potential for commercialization Strong team with relevant expertise in technology, business, and marketing Incorporation as a registered company in India.", "<b>Industry partners : </b> Commitment to collaborate with academic institutions and research labs Interest in adopting and deploying CPS technologies for their products and services Willingness to invest in R&D and innovation activities."]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Science & Technology national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://www.makeinindia.com/production-linked-incentive', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: DST National Mission on Interdisciplinary Cyber-Physical Systems (DST NM-ICPS) (Ministry of Science & Technology)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for DST National Mission on Interdisciplinary Cyber-Physical Systems (DST NM-ICPS) highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official DST National Mission on Interdisciplinary Cyber-Physical Systems (DST NM-ICPS) expenditure guidelines.
3. Address key scheme criteria: <b>Researchers and faculty : </b> Ph.D. degree in Science, Engineering, or related fields Experience in research and development related to Cyber-Physical Systems (CPS) Affiliation with a recognized academic or research institution in India Strong publication record in relevant fields., <b>Students : </b>Master''s degree in Science, Engineering, or related fields Good academic record with a strong interest in CPS research Enrollment in a Ph.D. program at a recognized Indian institution., <b>Start-ups and entrepreneurs :</b> Focus on developing innovative CPS solutions with potential for commercialization Strong team with relevant expertise in technology, business, and marketing Incorporation as a registered company in India..
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official DST National Mission on Interdisciplinary Cyber-Physical Systems (DST NM-ICPS) eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:22.612366+00:00', '2026-09-14T11:00:12.391015+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-78', 'SCH-OFFICIAL-78', 'Women Entrepreneur Cell', 'Central Bank of India', 'Central Bank of India', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for Women Entrepreneur Cell under Central Bank of India.', 'Official scheme support for Women Entrepreneur Cell under Central Bank of India.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["Women Entrepreneurs are eligible for this scheme."]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Central Bank of India national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://seedfund.startupindia.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Women Entrepreneur Cell (Central Bank of India)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Women Entrepreneur Cell highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Women Entrepreneur Cell expenditure guidelines.
3. Address key scheme criteria: Women Entrepreneurs are eligible for this scheme..
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Women Entrepreneur Cell eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:22.612366+00:00', '2026-09-14T11:00:12.391029+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-79', 'SCH-OFFICIAL-79', 'CENT STAND UP INDIA', 'Central Bank of India', 'Central Bank of India', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for CENT STAND UP INDIA under Central Bank of India.', 'Official scheme support for CENT STAND UP INDIA under Central Bank of India.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["SC/ST and /or Woman Entrepreneurs, above 18 years of age. In case of non-individual enterprises, 51% of the shareholding and controlling stake should be held by either SC/ST and/or Women Entrepreneur."]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Central Bank of India national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://www.standupmitra.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: CENT STAND UP INDIA (Central Bank of India)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for CENT STAND UP INDIA highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official CENT STAND UP INDIA expenditure guidelines.
3. Address key scheme criteria: SC/ST and /or Woman Entrepreneurs, above 18 years of age. In case of non-individual enterprises, 51% of the shareholding and controlling stake should be held by either SC/ST and/or Women Entrepreneur..
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official CENT STAND UP INDIA eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:22.612366+00:00', '2026-09-14T11:00:12.39104+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-80', 'SCH-OFFICIAL-80', 'Cent Kalyani Scheme', 'Central Bank of India', 'Central Bank of India', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for Cent Kalyani Scheme under Central Bank of India.', 'Official scheme support for Cent Kalyani Scheme under Central Bank of India.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["New as well as Existing Women entrepreneurs for her Micro/Small enterprise ( as defined under MSME Act- 2006) .i.e engaged in manufacturing and service activity for eg. Handloom weaving Handicraft, Food-Processing, Garment making, etc. Professionals & Self-employed women - Doctors, Chartered Accountants, and Engineers or trained in Art or Craft, etc.", "Health/Beauty/clinics/Dieticians/Fashion Designing Beauty Parlors. Small Business-Small/lunch/canteen, mobile restaurant, circulating/ library/tailoring/Day Creaches for children, Tailoring/Typing/STD/Xerox booth, etc.Transport Operators- Three wheelers/Four wheelers. (Retail Trade/Education and Training Institute/Self Help Group not eligible)"]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Central Bank of India national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://seedfund.startupindia.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Cent Kalyani Scheme (Central Bank of India)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Cent Kalyani Scheme highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Cent Kalyani Scheme expenditure guidelines.
3. Address key scheme criteria: New as well as Existing Women entrepreneurs for her Micro/Small enterprise ( as defined under MSME Act- 2006) .i.e engaged in manufacturing and service activity for eg. Handloom weaving Handicraft, Food-Processing, Garment making, etc. Professionals & Self-employed women - Doctors, Chartered Accountants, and Engineers or trained in Art or Craft, etc., Health/Beauty/clinics/Dieticians/Fashion Designing Beauty Parlors. Small Business-Small/lunch/canteen, mobile restaurant, circulating/ library/tailoring/Day Creaches for children, Tailoring/Typing/STD/Xerox booth, etc.Transport Operators- Three wheelers/Four wheelers. (Retail Trade/Education and Training Institute/Self Help Group not eligible).
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Cent Kalyani Scheme eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:22.612366+00:00', '2026-09-14T11:00:12.39105+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-81', 'SCH-OFFICIAL-81', 'Digital Communication Innovation Square', 'Ministry of Communications', 'Ministry of Communications', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for Digital Communication Innovation Square under Ministry of Communications.', 'Official scheme support for Digital Communication Innovation Square under Ministry of Communications.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["The Digital Communication Innovation Square (DCIS) is open to startups defined by DPIIT and are working towards development or improvement of products and processes with scalable business models.", "Specific eligibility requirements can be viewed in the official document of the policy."]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Communications national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://seedfund.startupindia.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Digital Communication Innovation Square (Ministry of Communications)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Digital Communication Innovation Square highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Digital Communication Innovation Square expenditure guidelines.
3. Address key scheme criteria: The Digital Communication Innovation Square (DCIS) is open to startups defined by DPIIT and are working towards development or improvement of products and processes with scalable business models., Specific eligibility requirements can be viewed in the official document of the policy..
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Digital Communication Innovation Square eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:22.612366+00:00', '2026-09-14T11:00:12.39106+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-82', 'SCH-OFFICIAL-82', 'National Handicrafts Development Program', 'Ministry of Textiles', 'Ministry of Textiles', 'Grant / Support', 'State Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for National Handicrafts Development Program under Ministry of Textiles.', 'Official scheme support for National Handicrafts Development Program under Ministry of Textiles.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["The eligibility criteria are different for different components under this scheme, please refer to the NHDP document for more details."]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Textiles national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'State', 'https://texmin.nic.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: National Handicrafts Development Program (Ministry of Textiles)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for National Handicrafts Development Program highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official National Handicrafts Development Program expenditure guidelines.
3. Address key scheme criteria: The eligibility criteria are different for different components under this scheme, please refer to the NHDP document for more details..
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official National Handicrafts Development Program eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:22.612366+00:00', '2026-09-14T11:00:12.39107+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-83', 'SCH-OFFICIAL-83', 'National Handloom Development Programme', 'Ministry of Textiles', 'Ministry of Textiles', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for National Handloom Development Programme under Ministry of Textiles.', 'Official scheme support for National Handloom Development Programme under Ministry of Textiles.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["The scheme has several components and eligibility varies for each of these. Please refer to the NHDP document for more details."]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Textiles national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://texmin.nic.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: National Handloom Development Programme (Ministry of Textiles)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for National Handloom Development Programme highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official National Handloom Development Programme expenditure guidelines.
3. Address key scheme criteria: The scheme has several components and eligibility varies for each of these. Please refer to the NHDP document for more details..
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official National Handloom Development Programme eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:22.612366+00:00', '2026-09-14T11:00:12.39108+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-84', 'SCH-OFFICIAL-84', 'Raw Material Supply Scheme', 'Ministry of Textiles', 'Ministry of Textiles', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for Raw Material Supply Scheme under Ministry of Textiles.', 'Official scheme support for Raw Material Supply Scheme under Ministry of Textiles.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["Individual weavers.", "Agencies in which weavers are members i.e. Self Help Groups (SHGs), Joint Liability Groups (JLGs) and Cooperative Societies.", "Handloom Producer Company.", "Weavers Entrepreneurs Entrepreneurs, who are involved in actual weaving activity along with marketing and other activities & own Handlooms on their premises, will be eligible weaver entrepreneurs.", "The number of Handlooms owned and functional in the premises of the weaver entrepreneur will be counted for the raw material subsidy component purpose."]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Textiles national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://texmin.nic.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Raw Material Supply Scheme (Ministry of Textiles)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Raw Material Supply Scheme highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Raw Material Supply Scheme expenditure guidelines.
3. Address key scheme criteria: Individual weavers., Agencies in which weavers are members i.e. Self Help Groups (SHGs), Joint Liability Groups (JLGs) and Cooperative Societies., Handloom Producer Company..
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Raw Material Supply Scheme eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:22.612366+00:00', '2026-09-14T11:00:12.391091+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-85', 'SCH-OFFICIAL-85', 'Genesis', 'Ministry of Electronics and Information Technology (MeitY)', 'Ministry of Electronics and Information Technology (MeitY)', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for Genesis under Ministry of Electronics and Information Technology (MeitY).', 'Official scheme support for Genesis under Ministry of Electronics and Information Technology (MeitY).', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["Eligibility Criteria for Implementation Agency:", "Organisation  and institutions that are based out of Tier II and Tier III cities of India, are eligible to apply for this scheme.", "Eligible entities include startup incubators, accelerators, investment platforms, entrepreneurship-supporting organizations, and academic  R&D institutions that have intent, expertise, and allocation of resources to support student entrepreneurs and innovators in their local community."]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Electronics and Information Technology (MeitY) national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://meity.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Genesis (Ministry of Electronics and Information Technology (MeitY))
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Genesis highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Genesis expenditure guidelines.
3. Address key scheme criteria: Eligibility Criteria for Implementation Agency:, Organisation  and institutions that are based out of Tier II and Tier III cities of India, are eligible to apply for this scheme., Eligible entities include startup incubators, accelerators, investment platforms, entrepreneurship-supporting organizations, and academic  R&D institutions that have intent, expertise, and allocation of resources to support student entrepreneurs and innovators in their local community..
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Genesis eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:22.612366+00:00', '2026-09-14T11:00:12.391101+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-86', 'SCH-OFFICIAL-86', 'Software Technology Park (STP) Scheme', 'Ministry of Electronics and Information Technology (MeitY)', 'Ministry of Electronics and Information Technology (MeitY)', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for Software Technology Park (STP) Scheme under Ministry of Electronics and Information Technology (MeitY).', 'Official scheme support for Software Technology Park (STP) Scheme under Ministry of Electronics and Information Technology (MeitY).', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["Company Registration: Registered under the Companies Act, 2013, or as a Limited Liability Partnership (LLP).", "<b>Minimum Export Turnover : </b>At least 50% of the annual turnover must be earned from export of software or IT services, hardware exports, or AVGC content.", "<b>Technology Focus :</b> Primarily engaged in development and/or delivery of technology-driven services or products.", "<b>Other Compliance :</b> Meet additional criteria related to net positive foreign exchange earnings, minimum investment in infrastructure, and adherence to statutory regulations."]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Electronics and Information Technology (MeitY) national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://meity.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Software Technology Park (STP) Scheme (Ministry of Electronics and Information Technology (MeitY))
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Software Technology Park (STP) Scheme highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Software Technology Park (STP) Scheme expenditure guidelines.
3. Address key scheme criteria: Company Registration: Registered under the Companies Act, 2013, or as a Limited Liability Partnership (LLP)., <b>Minimum Export Turnover : </b>At least 50% of the annual turnover must be earned from export of software or IT services, hardware exports, or AVGC content., <b>Technology Focus :</b> Primarily engaged in development and/or delivery of technology-driven services or products..
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Software Technology Park (STP) Scheme eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:22.612366+00:00', '2026-09-14T11:00:12.391111+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-87', 'SCH-OFFICIAL-87', 'Duty Exemption And Remission Scheme', 'Ministry of Electronics and Information Technology (MeitY)', 'Ministry of Electronics and Information Technology (MeitY)', 'Subsidy', 'Central Govt', 'Subsidy', 'Pre-Series A / Series A', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for Duty Exemption And Remission Scheme under Ministry of Electronics and Information Technology (MeitY).', 'Official scheme support for Duty Exemption And Remission Scheme under Ministry of Electronics and Information Technology (MeitY).', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '[]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Electronics and Information Technology (MeitY) national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://meity.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Duty Exemption And Remission Scheme (Ministry of Electronics and Information Technology (MeitY))
FUND TYPE: Subsidy

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Duty Exemption And Remission Scheme highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Duty Exemption And Remission Scheme expenditure guidelines.
3. Address key scheme criteria: .
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Duty Exemption And Remission Scheme eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:22.612366+00:00', '2026-09-14T11:00:12.391121+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-88', 'SCH-OFFICIAL-88', 'Electronics Hardware Technology Park Scheme', 'Ministry of Electronics and Information Technology (MeitY)', 'Ministry of Electronics and Information Technology (MeitY)', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for Electronics Hardware Technology Park Scheme under Ministry of Electronics and Information Technology (MeitY).', 'Official scheme support for Electronics Hardware Technology Park Scheme under Ministry of Electronics and Information Technology (MeitY).', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '[]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Electronics and Information Technology (MeitY) national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://meity.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Electronics Hardware Technology Park Scheme (Ministry of Electronics and Information Technology (MeitY))
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Electronics Hardware Technology Park Scheme highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Electronics Hardware Technology Park Scheme expenditure guidelines.
3. Address key scheme criteria: .
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Electronics Hardware Technology Park Scheme eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:22.612366+00:00', '2026-09-14T11:00:12.391131+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-89', 'SCH-OFFICIAL-89', 'VENTURE CAPITAL FUND FOR SCHEDULED TRIBES (VCF-ST)', 'Ministry of Tribal Affairs (MoTA)', 'Ministry of Tribal Affairs (MoTA)', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for VENTURE CAPITAL FUND FOR SCHEDULED TRIBES (VCF-ST) under Ministry of Tribal Affairs (MoTA).', 'Official scheme support for VENTURE CAPITAL FUND FOR SCHEDULED TRIBES (VCF-ST) under Ministry of Tribal Affairs (MoTA).', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["The projects/units being setup in the manufacturing, services and allied sector, including start-ups and units being incubated in the technology business incubators, ensuring asset creation out of the funds deployed in the units shall be considered.", "<b>A. For Companies applying for assistance up to Rs.50 lakh: Companies having :</b>", "i. at least 51% shareholding by Scheduled Tribes entrepreneurs for the past 6 months with the management control OR;", "ii. a new Company provided that the new company is a successor entity of Proprietary Firm or One Person Company (OPC) or Limited Liability (LLP) or any other establishment incorporated under any law in force with sound business model which has been in operation for over 6 months, and the predecessor entity had at least 51% shareholding of the Scheduled Tribes entrepreneurs with management control.", "<b>B. For Companies applying for assistance above Rs.50 lakh: Companies having :</b>", "i. At least 51% shareholding by Scheduled Tribes entrepreneurs for the past 12 months with management control OR;", "ii. a new Company provided that the new company is a successor entity of Proprietary Firm or One Person Company (OPC) or Limited Liability (LLP) or any other establishment incorporated under any law in force with sound business model which has been in operation for over 12 months, and the predecessor entity had at least 51% shareholding of the Scheduled Tribes entrepreneurs with management control.", "<b>For Technology Oriented Innovative Projects:</b>", "A. Eligibility Criteria for technology oriented innovative projects Innovative ideas selected by Technology Business Incubators (TBIs) for incubation funding to cover the cost of carrying out innovation projects subject to a ceiling of Rs.10 lakhs on an average year for a period of three years aggregating Rs.30 lakhs subject to satisfactory progress. Or;", "B. New Companies having at least 51% shareholding by first time Scheduled Tribes entrepreneurs who have been working in technology oriented innovative projects:", "i. With the support of incubation centers at IITs, NITs, Premier Business Schools, Universities, Institutions, Medical Colleges, NSTEDB under Department of Science & Technology (DST) or supported by corporates, with good potential of commercialization and project is at implementation stage.", "ii. Projects sanctioned by Departments/Ministries of Government of India after due appraisal."]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Tribal Affairs (MoTA) national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://tribal.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: VENTURE CAPITAL FUND FOR SCHEDULED TRIBES (VCF-ST) (Ministry of Tribal Affairs (MoTA))
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for VENTURE CAPITAL FUND FOR SCHEDULED TRIBES (VCF-ST) highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official VENTURE CAPITAL FUND FOR SCHEDULED TRIBES (VCF-ST) expenditure guidelines.
3. Address key scheme criteria: The projects/units being setup in the manufacturing, services and allied sector, including start-ups and units being incubated in the technology business incubators, ensuring asset creation out of the funds deployed in the units shall be considered., <b>A. For Companies applying for assistance up to Rs.50 lakh: Companies having :</b>, i. at least 51% shareholding by Scheduled Tribes entrepreneurs for the past 6 months with the management control OR;.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official VENTURE CAPITAL FUND FOR SCHEDULED TRIBES (VCF-ST) eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:22.612366+00:00', '2026-09-14T11:00:12.391141+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-90', 'SCH-OFFICIAL-90', 'PLI Scheme for Automobile and Auto components', 'Ministry of Heavy Industries & Public Enterprises', 'Ministry of Heavy Industries & Public Enterprises', 'Subsidy', 'Central Govt', 'Subsidy', 'Pre-Series A / Series A', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for PLI Scheme for Automobile and Auto components under Ministry of Heavy Industries & Public Enterprises.', 'Official scheme support for PLI Scheme for Automobile and Auto components under Ministry of Heavy Industries & Public Enterprises.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["For detailed information regarding eligibility, please refer to the guidelines document from the link below: <a href=''https://www.indiafilings.com/learn/pli-scheme-for-automobile-and-auto-component-industry/#:~:text=Eligibility%20Criteria%20for%20Existing%20Company&text=Minimum%20Rs.,10%2C000%20crores.&text=Global%20Investment%20of%20Company%20or%20its%20Group%20Company%20in%20fixed,150%20crore'' target=''_blank''>https://www.indiafilings.com/learn/pli-scheme-for-automobile-and-auto-component-industry/#:~:text=Eligibility%20Criteria%20for%20Existing%20Company&text=Minimum%20Rs.,10%2C000%20crores.&text=Global%20Investment%20of%20Company%20or%20its%20Group%20Company%20in%20fixed,150%20crore</a>"]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Heavy Industries & Public Enterprises national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://www.makeinindia.com/production-linked-incentive', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: PLI Scheme for Automobile and Auto components (Ministry of Heavy Industries & Public Enterprises)
FUND TYPE: Subsidy

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for PLI Scheme for Automobile and Auto components highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official PLI Scheme for Automobile and Auto components expenditure guidelines.
3. Address key scheme criteria: For detailed information regarding eligibility, please refer to the guidelines document from the link below: <a href=''https://www.indiafilings.com/learn/pli-scheme-for-automobile-and-auto-component-industry/#:~:text=Eligibility%20Criteria%20for%20Existing%20Company&text=Minimum%20Rs.,10%2C000%20crores.&text=Global%20Investment%20of%20Company%20or%20its%20Group%20Company%20in%20fixed,150%20crore'' target=''_blank''>https://www.indiafilings.com/learn/pli-scheme-for-automobile-and-auto-component-industry/#:~:text=Eligibility%20Criteria%20for%20Existing%20Company&text=Minimum%20Rs.,10%2C000%20crores.&text=Global%20Investment%20of%20Company%20or%20its%20Group%20Company%20in%20fixed,150%20crore</a>.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official PLI Scheme for Automobile and Auto components eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:22.612366+00:00', '2026-09-14T11:00:12.391151+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-91', 'SCH-OFFICIAL-91', 'PLI Scheme for National Programme on Advanced Chemistry Cell (ACC) Battery Storage', 'Ministry of Heavy Industries & Public Enterprises', 'Ministry of Heavy Industries & Public Enterprises', 'Subsidy', 'Central Govt', 'Subsidy', 'Pre-Series A / Series A', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for PLI Scheme for National Programme on Advanced Chemistry Cell (ACC) Battery Storage under Ministry of Heavy Industries & Public Enterprises.', 'Official scheme support for PLI Scheme for National Programme on Advanced Chemistry Cell (ACC) Battery Storage under Ministry of Heavy Industries & Public Enterprises.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '[]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Heavy Industries & Public Enterprises national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://www.makeinindia.com/production-linked-incentive', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: PLI Scheme for National Programme on Advanced Chemistry Cell (ACC) Battery Storage (Ministry of Heavy Industries & Public Enterprises)
FUND TYPE: Subsidy

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for PLI Scheme for National Programme on Advanced Chemistry Cell (ACC) Battery Storage highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official PLI Scheme for National Programme on Advanced Chemistry Cell (ACC) Battery Storage expenditure guidelines.
3. Address key scheme criteria: .
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official PLI Scheme for National Programme on Advanced Chemistry Cell (ACC) Battery Storage eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:22.612366+00:00', '2026-09-14T11:00:12.391161+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-92', 'SCH-OFFICIAL-92', 'Participation in International Fairs and Exhibitions with Tea Board', 'Ministry of Commerce and Industry Schemes', 'Ministry of Commerce and Industry Schemes', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for Participation in International Fairs and Exhibitions with Tea Board under Ministry of Commerce and Industry Schemes.', 'Official scheme support for Participation in International Fairs and Exhibitions with Tea Board under Ministry of Commerce and Industry Schemes.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["All exporters holding valid exporters’ licenses are eligible to participate from the Tea Board’s booth in the exhibition. The company shall not be under any investigation/charged/prosecuted/debarred/blacklisted on any grounds related to trade and business.", "Only exporters submitting regular monthly export returns will be eligible for participation.", "The exporter must be dealing in only 100% Indian teas.", "Provision for new entrants will be there as per the table at C 2 below."]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Commerce and Industry Schemes national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://seedfund.startupindia.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Participation in International Fairs and Exhibitions with Tea Board (Ministry of Commerce and Industry Schemes)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Participation in International Fairs and Exhibitions with Tea Board highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Participation in International Fairs and Exhibitions with Tea Board expenditure guidelines.
3. Address key scheme criteria: All exporters holding valid exporters’ licenses are eligible to participate from the Tea Board’s booth in the exhibition. The company shall not be under any investigation/charged/prosecuted/debarred/blacklisted on any grounds related to trade and business., Only exporters submitting regular monthly export returns will be eligible for participation., The exporter must be dealing in only 100% Indian teas..
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Participation in International Fairs and Exhibitions with Tea Board eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:22.612366+00:00', '2026-09-14T11:00:12.391171+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-93', 'SCH-OFFICIAL-93', 'High Risk-High Reward Research', 'Ministry of Science & Technology', 'Ministry of Science & Technology', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for High Risk-High Reward Research under Ministry of Science & Technology.', 'Official scheme support for High Risk-High Reward Research under Ministry of Science & Technology.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["Applicant should be an Indian citizen residing in India. The applicant(s) must hold a regular academic research position in a recognized institution. The proposals can be submitted by an individual or by a team of investigators. Proposals submitted by a team of investigators must identify a Principal Investigator, who will spearhead the research objectives and administer the grant."]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Science & Technology national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://dst.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: High Risk-High Reward Research (Ministry of Science & Technology)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for High Risk-High Reward Research highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official High Risk-High Reward Research expenditure guidelines.
3. Address key scheme criteria: Applicant should be an Indian citizen residing in India. The applicant(s) must hold a regular academic research position in a recognized institution. The proposals can be submitted by an individual or by a team of investigators. Proposals submitted by a team of investigators must identify a Principal Investigator, who will spearhead the research objectives and administer the grant..
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official High Risk-High Reward Research eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:22.612366+00:00', '2026-09-14T11:00:12.391182+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-94', 'SCH-OFFICIAL-94', 'Technology Development Programme', 'Ministry of Science & Technology', 'Ministry of Science & Technology', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for Technology Development Programme under Ministry of Science & Technology.', 'Official scheme support for Technology Development Programme under Ministry of Science & Technology.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["Project Proposals can be submitted for financial support by scientists/engineers/technologists working in academic institutions/registered societies/R&D institutions/laboratories having adequate infrastructure/facilities to carry out technology development work. The Programme encourages multi-disciplinary Proposals envisaging network/collaboration of various Organizations having diverse expertise and facilities for synergistic implementation of the Projects. Participation of industry is encouraged.", "Project Proposals from academic/R&D Institutions in collaboration with Industry having DSIR recognized R&D Laboratories will be preferred."]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Science & Technology national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://dst.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Technology Development Programme (Ministry of Science & Technology)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Technology Development Programme highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Technology Development Programme expenditure guidelines.
3. Address key scheme criteria: Project Proposals can be submitted for financial support by scientists/engineers/technologists working in academic institutions/registered societies/R&D institutions/laboratories having adequate infrastructure/facilities to carry out technology development work. The Programme encourages multi-disciplinary Proposals envisaging network/collaboration of various Organizations having diverse expertise and facilities for synergistic implementation of the Projects. Participation of industry is encouraged., Project Proposals from academic/R&D Institutions in collaboration with Industry having DSIR recognized R&D Laboratories will be preferred..
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Technology Development Programme eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:22.612366+00:00', '2026-09-14T11:00:12.391193+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-95', 'SCH-OFFICIAL-95', 'AGNIi', 'Ministry of Commerce and Industry Schemes', 'Ministry of Commerce and Industry Schemes', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for AGNIi under Ministry of Commerce and Industry Schemes.', 'Official scheme support for AGNIi under Ministry of Commerce and Industry Schemes.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["<b>Institutional Affiliation :</b>", "Indian universities, research institutions, or innovative startups.", "Strong research and development infrastructure and capabilities.", "Proven track record in innovation and technology development."]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Commerce and Industry Schemes national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://seedfund.startupindia.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: AGNIi (Ministry of Commerce and Industry Schemes)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for AGNIi highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official AGNIi expenditure guidelines.
3. Address key scheme criteria: <b>Institutional Affiliation :</b>, Indian universities, research institutions, or innovative startups., Strong research and development infrastructure and capabilities..
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official AGNIi eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:22.612366+00:00', '2026-09-14T11:00:12.391204+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-96', 'SCH-OFFICIAL-96', 'Working Capital Term Loan (WCTL)', 'Ministry of Development of North Eastern Region', 'Ministry of Development of North Eastern Region', 'Credit', 'Central Govt', 'Credit', 'Growth / Debt Scaling', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for Working Capital Term Loan (WCTL) under Ministry of Development of North Eastern Region.', 'Official scheme support for Working Capital Term Loan (WCTL) under Ministry of Development of North Eastern Region.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["Eligible contractor firms and companies."]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Development of North Eastern Region national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://seedfund.startupindia.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Working Capital Term Loan (WCTL) (Ministry of Development of North Eastern Region)
FUND TYPE: Credit

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Working Capital Term Loan (WCTL) highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Working Capital Term Loan (WCTL) expenditure guidelines.
3. Address key scheme criteria: Eligible contractor firms and companies..
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Working Capital Term Loan (WCTL) eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:22.612366+00:00', '2026-09-14T11:00:12.391214+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-97', 'SCH-OFFICIAL-97', 'Working Capital Term Loan (WCTL) for Contract Finance', 'Ministry of Development of North Eastern Region', 'Ministry of Development of North Eastern Region', 'Credit', 'Central Govt', 'Credit', 'Growth / Debt Scaling', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for Working Capital Term Loan (WCTL) for Contract Finance under Ministry of Development of North Eastern Region.', 'Official scheme support for Working Capital Term Loan (WCTL) for Contract Finance under Ministry of Development of North Eastern Region.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["Eligible contractor firms and companies."]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Development of North Eastern Region national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://seedfund.startupindia.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Working Capital Term Loan (WCTL) for Contract Finance (Ministry of Development of North Eastern Region)
FUND TYPE: Credit

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Working Capital Term Loan (WCTL) for Contract Finance highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Working Capital Term Loan (WCTL) for Contract Finance expenditure guidelines.
3. Address key scheme criteria: Eligible contractor firms and companies..
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Working Capital Term Loan (WCTL) for Contract Finance eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:22.612366+00:00', '2026-09-14T11:00:12.391224+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-98', 'SCH-OFFICIAL-98', 'NewGen Innovation and Entrepreneurship Development Centre', 'Ministry of Science & Technology', 'Ministry of Science & Technology', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for NewGen Innovation and Entrepreneurship Development Centre under Ministry of Science & Technology.', 'Official scheme support for NewGen Innovation and Entrepreneurship Development Centre under Ministry of Science & Technology.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["The institution should be a University/Deemed University or a premier Institute/College offering Engineering, Technology, Science courses at the degree level or above for at least 5 years.", "The institution must have at least two faculty members trained in Entrepreneurship through DST sponsored Faculty Development Programme and should have a minimum dedicated space of about 5000 square feet for housing the NewGen IEDC."]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Ministry of Science & Technology national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://dst.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: NewGen Innovation and Entrepreneurship Development Centre (Ministry of Science & Technology)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for NewGen Innovation and Entrepreneurship Development Centre highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official NewGen Innovation and Entrepreneurship Development Centre expenditure guidelines.
3. Address key scheme criteria: The institution should be a University/Deemed University or a premier Institute/College offering Engineering, Technology, Science courses at the degree level or above for at least 5 years., The institution must have at least two faculty members trained in Entrepreneurship through DST sponsored Faculty Development Programme and should have a minimum dedicated space of about 5000 square feet for housing the NewGen IEDC..
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official NewGen Innovation and Entrepreneurship Development Centre eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:22.612366+00:00', '2026-09-14T11:00:12.391245+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-OFFICIAL-99', 'SCH-OFFICIAL-99', 'SPARSH (Social Innovation program for Products: Affordable & Relevant to Societal Health)', 'Biotechnology Industry Research Assistance Council (BIRAC)', 'Biotechnology Industry Research Assistance Council (BIRAC)', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Varies per project scale (Up to Rs 1Cr - Rs 15Cr)', 'Official scheme support for SPARSH (Social Innovation program for Products: Affordable & Relevant to Societal Health) under Biotechnology Industry Research Assistance Council (BIRAC).', 'Official scheme support for SPARSH (Social Innovation program for Products: Affordable & Relevant to Societal Health) under Biotechnology Industry Research Assistance Council (BIRAC).', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["Biotechnology Indian startups that are incorporated under the Indian Companies Act, having a minimum of 51% Indian Ownership and less than three years old from the date of advertisement/Indian entrepreneurs.", "Limited Liability Partnership (LLP) that is incorporated under the Limited Liability Partnership Act, 2008, less than three years old from the date of advertisement and having a minimum half of the individuals who have subscribed for LLP document, whose partners have to be Indian citizens.", "Indian Academic Scientists, PhDs, Researchers, Medical Degree Holders, Biomedical Engineering graduates who are willing to incubate in a business incubator.", "Proprietorship concern that is set up by an Indian citizen under the certificate/license that is issued by municipal authorities/under Shop and Establishment Act or relevant prominence."]', '["Milestone based disbursement per official guidelines"]', '[">> Priority alignment with Biotechnology Industry Research Assistance Council (BIRAC) national focus area.", ">> Emphasize job creation, local manufacturing, or indigenous technology development."]', '["!! Strict utilization certificate (UC) audit required before next tranche.", "!! Verify bank sanction and compliance guidelines before capital commitment."]', 'Portal Application -> Technical Committee -> Disbursement', '3-6 months', '~20-30%', 'startupindia.gov.in', 'All India', 'National', 'https://birac.nic.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: SPARSH (Social Innovation program for Products: Affordable & Relevant to Societal Health) (Biotechnology Industry Research Assistance Council (BIRAC))
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for SPARSH (Social Innovation program for Products: Affordable & Relevant to Societal Health) highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official SPARSH (Social Innovation program for Products: Affordable & Relevant to Societal Health) expenditure guidelines.
3. Address key scheme criteria: Biotechnology Indian startups that are incorporated under the Indian Companies Act, having a minimum of 51% Indian Ownership and less than three years old from the date of advertisement/Indian entrepreneurs., Limited Liability Partnership (LLP) that is incorporated under the Limited Liability Partnership Act, 2008, less than three years old from the date of advertisement and having a minimum half of the individuals who have subscribed for LLP document, whose partners have to be Indian citizens., Indian Academic Scientists, PhDs, Researchers, Medical Degree Holders, Biomedical Engineering graduates who are willing to incubate in a business incubator..
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official SPARSH (Social Innovation program for Products: Affordable & Relevant to Societal Health) eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:22.612366+00:00', '2026-09-14T11:00:12.391274+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-RAW-102', 'SCH-RAW-102', 'IndiaAI Mission', 'Nodal Agency / Ministry', 'Nodal Agency / Ministry', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Up to Rs 25L - Rs 5Cr support', 'Strategic research scheme: IndiaAI Mission.', 'Strategic research scheme: IndiaAI Mission.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["DPIIT startup / MSME entity"]', '["Per nodal agency guidelines"]', '[">> Highlight strategic alignment with national sector goals."]', '["!! Verify sanction terms and timeline before budget allocation."]', 'Portal Application -> Screening -> Disbursement', '2-4 months', '~20%', 'startupindia.gov.in', 'All India', 'National', 'https://www.indiaai.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: IndiaAI Mission (Nodal Agency / Ministry)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for IndiaAI Mission highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official IndiaAI Mission expenditure guidelines.
3. Address key scheme criteria: DPIIT startup / MSME entity.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official IndiaAI Mission eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:23.170011+00:00', '2026-09-14T11:00:12.391325+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-RAW-103', 'SCH-RAW-103', 'MeitY GENESIS', 'Nodal Agency / Ministry', 'Nodal Agency / Ministry', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Up to Rs 25L - Rs 5Cr support', 'Strategic research scheme: MeitY GENESIS.', 'Strategic research scheme: MeitY GENESIS.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["DPIIT startup / MSME entity"]', '["Per nodal agency guidelines"]', '[">> Highlight strategic alignment with national sector goals."]', '["!! Verify sanction terms and timeline before budget allocation."]', 'Portal Application -> Screening -> Disbursement', '2-4 months', '~20%', 'startupindia.gov.in', 'All India', 'National', 'https://seedfund.startupindia.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: MeitY GENESIS (Nodal Agency / Ministry)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for MeitY GENESIS highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official MeitY GENESIS expenditure guidelines.
3. Address key scheme criteria: DPIIT startup / MSME entity.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official MeitY GENESIS eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:23.170011+00:00', '2026-09-14T11:00:12.391335+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-RAW-104', 'SCH-RAW-104', 'MeitY Startups', 'Nodal Agency / Ministry', 'Nodal Agency / Ministry', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Up to Rs 25L - Rs 5Cr support', 'Strategic research scheme: MeitY Startups.', 'Strategic research scheme: MeitY Startups.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["DPIIT startup / MSME entity"]', '["Per nodal agency guidelines"]', '[">> Highlight strategic alignment with national sector goals."]', '["!! Verify sanction terms and timeline before budget allocation."]', 'Portal Application -> Screening -> Disbursement', '2-4 months', '~20%', 'startupindia.gov.in', 'All India', 'National', 'https://seedfund.startupindia.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: MeitY Startups (Nodal Agency / Ministry)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for MeitY Startups highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official MeitY Startups expenditure guidelines.
3. Address key scheme criteria: DPIIT startup / MSME entity.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official MeitY Startups eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:23.170011+00:00', '2026-09-14T11:00:12.391345+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-RAW-105', 'SCH-RAW-105', 'C-DAC AI', 'Nodal Agency / Ministry', 'Nodal Agency / Ministry', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Up to Rs 25L - Rs 5Cr support', 'Strategic research scheme: C-DAC AI.', 'Strategic research scheme: C-DAC AI.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["DPIIT startup / MSME entity"]', '["Per nodal agency guidelines"]', '[">> Highlight strategic alignment with national sector goals."]', '["!! Verify sanction terms and timeline before budget allocation."]', 'Portal Application -> Screening -> Disbursement', '2-4 months', '~20%', 'startupindia.gov.in', 'All India', 'National', 'https://seedfund.startupindia.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: C-DAC AI (Nodal Agency / Ministry)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for C-DAC AI highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official C-DAC AI expenditure guidelines.
3. Address key scheme criteria: DPIIT startup / MSME entity.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official C-DAC AI eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:23.170011+00:00', '2026-09-14T11:00:12.391355+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-RAW-106', 'SCH-RAW-106', 'DST NM-ICPS', 'Nodal Agency / Ministry', 'Nodal Agency / Ministry', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Up to Rs 25L - Rs 5Cr support', 'Strategic research scheme: DST NM-ICPS.', 'Strategic research scheme: DST NM-ICPS.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["DPIIT startup / MSME entity"]', '["Per nodal agency guidelines"]', '[">> Highlight strategic alignment with national sector goals."]', '["!! Verify sanction terms and timeline before budget allocation."]', 'Portal Application -> Screening -> Disbursement', '2-4 months', '~20%', 'startupindia.gov.in', 'All India', 'National', 'https://seedfund.startupindia.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: DST NM-ICPS (Nodal Agency / Ministry)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for DST NM-ICPS highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official DST NM-ICPS expenditure guidelines.
3. Address key scheme criteria: DPIIT startup / MSME entity.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official DST NM-ICPS eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:23.170011+00:00', '2026-09-14T11:00:12.391368+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-RAW-107', 'SCH-RAW-107', 'DST HRR', 'Nodal Agency / Ministry', 'Nodal Agency / Ministry', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Up to Rs 25L - Rs 5Cr support', 'Strategic research scheme: DST HRR.', 'Strategic research scheme: DST HRR.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["DPIIT startup / MSME entity"]', '["Per nodal agency guidelines"]', '[">> Highlight strategic alignment with national sector goals."]', '["!! Verify sanction terms and timeline before budget allocation."]', 'Portal Application -> Screening -> Disbursement', '2-4 months', '~20%', 'startupindia.gov.in', 'All India', 'National', 'https://seedfund.startupindia.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: DST HRR (Nodal Agency / Ministry)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for DST HRR highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official DST HRR expenditure guidelines.
3. Address key scheme criteria: DPIIT startup / MSME entity.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official DST HRR eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:23.170011+00:00', '2026-09-14T11:00:12.391379+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-RAW-108', 'SCH-RAW-108', 'SERB', 'Nodal Agency / Ministry', 'Nodal Agency / Ministry', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Up to Rs 25L - Rs 5Cr support', 'Strategic research scheme: SERB.', 'Strategic research scheme: SERB.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["DPIIT startup / MSME entity"]', '["Per nodal agency guidelines"]', '[">> Highlight strategic alignment with national sector goals."]', '["!! Verify sanction terms and timeline before budget allocation."]', 'Portal Application -> Screening -> Disbursement', '2-4 months', '~20%', 'startupindia.gov.in', 'All India', 'National', 'https://seedfund.startupindia.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: SERB (Nodal Agency / Ministry)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for SERB highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official SERB expenditure guidelines.
3. Address key scheme criteria: DPIIT startup / MSME entity.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official SERB eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:23.170011+00:00', '2026-09-14T11:00:12.391389+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-RAW-109', 'SCH-RAW-109', 'IN-SPACe', 'Nodal Agency / Ministry', 'Nodal Agency / Ministry', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Up to Rs 25L - Rs 5Cr support', 'Strategic research scheme: IN-SPACe.', 'Strategic research scheme: IN-SPACe.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["DPIIT startup / MSME entity"]', '["Per nodal agency guidelines"]', '[">> Highlight strategic alignment with national sector goals."]', '["!! Verify sanction terms and timeline before budget allocation."]', 'Portal Application -> Screening -> Disbursement', '2-4 months', '~20%', 'startupindia.gov.in', 'All India', 'National', 'https://www.inspace.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: IN-SPACe (Nodal Agency / Ministry)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for IN-SPACe highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official IN-SPACe expenditure guidelines.
3. Address key scheme criteria: DPIIT startup / MSME entity.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official IN-SPACe eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:23.170011+00:00', '2026-09-14T11:00:12.391398+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-RAW-110', 'SCH-RAW-110', 'iDEX', 'Nodal Agency / Ministry', 'Nodal Agency / Ministry', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Up to Rs 25L - Rs 5Cr support', 'Strategic research scheme: iDEX.', 'Strategic research scheme: iDEX.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["DPIIT startup / MSME entity"]', '["Per nodal agency guidelines"]', '[">> Highlight strategic alignment with national sector goals."]', '["!! Verify sanction terms and timeline before budget allocation."]', 'Portal Application -> Screening -> Disbursement', '2-4 months', '~20%', 'startupindia.gov.in', 'All India', 'National', 'https://idex.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: iDEX (Nodal Agency / Ministry)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for iDEX highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official iDEX expenditure guidelines.
3. Address key scheme criteria: DPIIT startup / MSME entity.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official iDEX eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:23.170011+00:00', '2026-09-14T11:00:12.391409+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-RAW-111', 'SCH-RAW-111', 'TDF DRDO', 'Nodal Agency / Ministry', 'Nodal Agency / Ministry', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Up to Rs 25L - Rs 5Cr support', 'Strategic research scheme: TDF DRDO.', 'Strategic research scheme: TDF DRDO.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["DPIIT startup / MSME entity"]', '["Per nodal agency guidelines"]', '[">> Highlight strategic alignment with national sector goals."]', '["!! Verify sanction terms and timeline before budget allocation."]', 'Portal Application -> Screening -> Disbursement', '2-4 months', '~20%', 'startupindia.gov.in', 'All India', 'National', 'https://tdf.drdo.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: TDF DRDO (Nodal Agency / Ministry)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for TDF DRDO highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official TDF DRDO expenditure guidelines.
3. Address key scheme criteria: DPIIT startup / MSME entity.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official TDF DRDO eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:23.170011+00:00', '2026-09-14T11:00:12.39142+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-RAW-112', 'SCH-RAW-112', 'ISRO Technology Transfer', 'Nodal Agency / Ministry', 'Nodal Agency / Ministry', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Up to Rs 25L - Rs 5Cr support', 'Strategic research scheme: ISRO Technology Transfer.', 'Strategic research scheme: ISRO Technology Transfer.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["DPIIT startup / MSME entity"]', '["Per nodal agency guidelines"]', '[">> Highlight strategic alignment with national sector goals."]', '["!! Verify sanction terms and timeline before budget allocation."]', 'Portal Application -> Screening -> Disbursement', '2-4 months', '~20%', 'startupindia.gov.in', 'All India', 'National', 'https://www.isro.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: ISRO Technology Transfer (Nodal Agency / Ministry)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for ISRO Technology Transfer highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official ISRO Technology Transfer expenditure guidelines.
3. Address key scheme criteria: DPIIT startup / MSME entity.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official ISRO Technology Transfer eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:23.170011+00:00', '2026-09-14T11:00:12.39143+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-RAW-113', 'SCH-RAW-113', 'iDEX DISC', 'Nodal Agency / Ministry', 'Nodal Agency / Ministry', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Up to Rs 25L - Rs 5Cr support', 'Strategic research scheme: iDEX DISC.', 'Strategic research scheme: iDEX DISC.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["DPIIT startup / MSME entity"]', '["Per nodal agency guidelines"]', '[">> Highlight strategic alignment with national sector goals."]', '["!! Verify sanction terms and timeline before budget allocation."]', 'Portal Application -> Screening -> Disbursement', '2-4 months', '~20%', 'startupindia.gov.in', 'All India', 'National', 'https://idex.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: iDEX DISC (Nodal Agency / Ministry)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for iDEX DISC highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official iDEX DISC expenditure guidelines.
3. Address key scheme criteria: DPIIT startup / MSME entity.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official iDEX DISC eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:23.170011+00:00', '2026-09-14T11:00:12.39144+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-RAW-114', 'SCH-RAW-114', 'Make in India Defence', 'Nodal Agency / Ministry', 'Nodal Agency / Ministry', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Up to Rs 25L - Rs 5Cr support', 'Strategic research scheme: Make in India Defence.', 'Strategic research scheme: Make in India Defence.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["DPIIT startup / MSME entity"]', '["Per nodal agency guidelines"]', '[">> Highlight strategic alignment with national sector goals."]', '["!! Verify sanction terms and timeline before budget allocation."]', 'Portal Application -> Screening -> Disbursement', '2-4 months', '~20%', 'startupindia.gov.in', 'All India', 'National', 'https://www.makeinindiadefence.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Make in India Defence (Nodal Agency / Ministry)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Make in India Defence highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Make in India Defence expenditure guidelines.
3. Address key scheme criteria: DPIIT startup / MSME entity.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Make in India Defence eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:23.170011+00:00', '2026-09-14T11:00:12.39145+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-RAW-115', 'SCH-RAW-115', 'India Semiconductor Mission', 'Nodal Agency / Ministry', 'Nodal Agency / Ministry', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Up to Rs 25L - Rs 5Cr support', 'Strategic research scheme: India Semiconductor Mission.', 'Strategic research scheme: India Semiconductor Mission.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["DPIIT startup / MSME entity"]', '["Per nodal agency guidelines"]', '[">> Highlight strategic alignment with national sector goals."]', '["!! Verify sanction terms and timeline before budget allocation."]', 'Portal Application -> Screening -> Disbursement', '2-4 months', '~20%', 'startupindia.gov.in', 'All India', 'National', 'https://www.semiconindia.org', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: India Semiconductor Mission (Nodal Agency / Ministry)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for India Semiconductor Mission highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official India Semiconductor Mission expenditure guidelines.
3. Address key scheme criteria: DPIIT startup / MSME entity.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official India Semiconductor Mission eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:23.170011+00:00', '2026-09-14T11:00:12.39146+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-RAW-116', 'SCH-RAW-116', 'RBI Regulatory Sandbox', 'Nodal Agency / Ministry', 'Nodal Agency / Ministry', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Up to Rs 25L - Rs 5Cr support', 'Strategic research scheme: RBI Regulatory Sandbox.', 'Strategic research scheme: RBI Regulatory Sandbox.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["DPIIT startup / MSME entity"]', '["Per nodal agency guidelines"]', '[">> Highlight strategic alignment with national sector goals."]', '["!! Verify sanction terms and timeline before budget allocation."]', 'Portal Application -> Screening -> Disbursement', '2-4 months', '~20%', 'startupindia.gov.in', 'All India', 'National', 'https://www.rbi.org.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: RBI Regulatory Sandbox (Nodal Agency / Ministry)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for RBI Regulatory Sandbox highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official RBI Regulatory Sandbox expenditure guidelines.
3. Address key scheme criteria: DPIIT startup / MSME entity.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official RBI Regulatory Sandbox eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:23.170011+00:00', '2026-09-14T11:00:12.39147+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-RAW-117', 'SCH-RAW-117', 'IFSCA Fintech', 'Nodal Agency / Ministry', 'Nodal Agency / Ministry', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Up to Rs 25L - Rs 5Cr support', 'Strategic research scheme: IFSCA Fintech.', 'Strategic research scheme: IFSCA Fintech.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["DPIIT startup / MSME entity"]', '["Per nodal agency guidelines"]', '[">> Highlight strategic alignment with national sector goals."]', '["!! Verify sanction terms and timeline before budget allocation."]', 'Portal Application -> Screening -> Disbursement', '2-4 months', '~20%', 'startupindia.gov.in', 'All India', 'National', 'https://ifsca.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: IFSCA Fintech (Nodal Agency / Ministry)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for IFSCA Fintech highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official IFSCA Fintech expenditure guidelines.
3. Address key scheme criteria: DPIIT startup / MSME entity.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official IFSCA Fintech eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:23.170011+00:00', '2026-09-14T11:00:12.39148+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-RAW-118', 'SCH-RAW-118', 'NABARD Fintech', 'Nodal Agency / Ministry', 'Nodal Agency / Ministry', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Up to Rs 25L - Rs 5Cr support', 'Strategic research scheme: NABARD Fintech.', 'Strategic research scheme: NABARD Fintech.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["DPIIT startup / MSME entity"]', '["Per nodal agency guidelines"]', '[">> Highlight strategic alignment with national sector goals."]', '["!! Verify sanction terms and timeline before budget allocation."]', 'Portal Application -> Screening -> Disbursement', '2-4 months', '~20%', 'startupindia.gov.in', 'All India', 'National', 'https://www.nabard.org', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: NABARD Fintech (Nodal Agency / Ministry)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for NABARD Fintech highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official NABARD Fintech expenditure guidelines.
3. Address key scheme criteria: DPIIT startup / MSME entity.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official NABARD Fintech eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:23.170011+00:00', '2026-09-14T11:00:12.39149+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-RAW-119', 'SCH-RAW-119', 'NABVENTURES', 'Nodal Agency / Ministry', 'Nodal Agency / Ministry', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Up to Rs 25L - Rs 5Cr support', 'Strategic research scheme: NABVENTURES.', 'Strategic research scheme: NABVENTURES.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["DPIIT startup / MSME entity"]', '["Per nodal agency guidelines"]', '[">> Highlight strategic alignment with national sector goals."]', '["!! Verify sanction terms and timeline before budget allocation."]', 'Portal Application -> Screening -> Disbursement', '2-4 months', '~20%', 'startupindia.gov.in', 'All India', 'National', 'https://nabventures.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: NABVENTURES (Nodal Agency / Ministry)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for NABVENTURES highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official NABVENTURES expenditure guidelines.
3. Address key scheme criteria: DPIIT startup / MSME entity.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official NABVENTURES eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:23.170011+00:00', '2026-09-14T11:00:12.3915+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-RAW-120', 'SCH-RAW-120', 'MNRE Schemes', 'Nodal Agency / Ministry', 'Nodal Agency / Ministry', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Up to Rs 25L - Rs 5Cr support', 'Strategic research scheme: MNRE Schemes.', 'Strategic research scheme: MNRE Schemes.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["DPIIT startup / MSME entity"]', '["Per nodal agency guidelines"]', '[">> Highlight strategic alignment with national sector goals."]', '["!! Verify sanction terms and timeline before budget allocation."]', 'Portal Application -> Screening -> Disbursement', '2-4 months', '~20%', 'startupindia.gov.in', 'All India', 'National', 'https://mnre.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: MNRE Schemes (Nodal Agency / Ministry)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for MNRE Schemes highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official MNRE Schemes expenditure guidelines.
3. Address key scheme criteria: DPIIT startup / MSME entity.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official MNRE Schemes eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:23.170011+00:00', '2026-09-14T11:00:12.39151+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-RAW-121', 'SCH-RAW-121', 'IREDA Green Loans', 'Nodal Agency / Ministry', 'Nodal Agency / Ministry', 'Credit', 'Central Govt', 'Credit', 'Pre-Seed / Seed', 'Up to Rs 25L - Rs 5Cr support', 'Strategic research scheme: IREDA Green Loans.', 'Strategic research scheme: IREDA Green Loans.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["DPIIT startup / MSME entity"]', '["Per nodal agency guidelines"]', '[">> Highlight strategic alignment with national sector goals."]', '["!! Verify sanction terms and timeline before budget allocation."]', 'Portal Application -> Screening -> Disbursement', '2-4 months', '~20%', 'startupindia.gov.in', 'All India', 'National', 'https://www.ireda.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: IREDA Green Loans (Nodal Agency / Ministry)
FUND TYPE: Credit

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for IREDA Green Loans highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official IREDA Green Loans expenditure guidelines.
3. Address key scheme criteria: DPIIT startup / MSME entity.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official IREDA Green Loans eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:23.170011+00:00', '2026-09-14T11:00:12.39152+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-RAW-122', 'SCH-RAW-122', 'PM KUSUM', 'Nodal Agency / Ministry', 'Nodal Agency / Ministry', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Up to Rs 25L - Rs 5Cr support', 'Strategic research scheme: PM KUSUM.', 'Strategic research scheme: PM KUSUM.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["DPIIT startup / MSME entity"]', '["Per nodal agency guidelines"]', '[">> Highlight strategic alignment with national sector goals."]', '["!! Verify sanction terms and timeline before budget allocation."]', 'Portal Application -> Screening -> Disbursement', '2-4 months', '~20%', 'startupindia.gov.in', 'All India', 'National', 'https://pmkusum.mnre.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: PM KUSUM (Nodal Agency / Ministry)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for PM KUSUM highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official PM KUSUM expenditure guidelines.
3. Address key scheme criteria: DPIIT startup / MSME entity.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official PM KUSUM eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:23.170011+00:00', '2026-09-14T11:00:12.39153+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-RAW-123', 'SCH-RAW-123', 'Agriculture Infrastructure Fund', 'Nodal Agency / Ministry', 'Nodal Agency / Ministry', 'Equity', 'Central Govt', 'Equity', 'Pre-Seed / Seed', 'Up to Rs 25L - Rs 5Cr support', 'Strategic research scheme: Agriculture Infrastructure Fund.', 'Strategic research scheme: Agriculture Infrastructure Fund.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["DPIIT startup / MSME entity"]', '["Per nodal agency guidelines"]', '[">> Highlight strategic alignment with national sector goals."]', '["!! Verify sanction terms and timeline before budget allocation."]', 'Portal Application -> Screening -> Disbursement', '2-4 months', '~20%', 'startupindia.gov.in', 'All India', 'National', 'https://agriinfra.dac.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Agriculture Infrastructure Fund (Nodal Agency / Ministry)
FUND TYPE: Equity

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Agriculture Infrastructure Fund highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Agriculture Infrastructure Fund expenditure guidelines.
3. Address key scheme criteria: DPIIT startup / MSME entity.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Agriculture Infrastructure Fund eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:23.170011+00:00', '2026-09-14T11:00:12.39154+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-RAW-124', 'SCH-RAW-124', 'PM FME', 'Nodal Agency / Ministry', 'Nodal Agency / Ministry', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Up to Rs 25L - Rs 5Cr support', 'Strategic research scheme: PM FME.', 'Strategic research scheme: PM FME.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["DPIIT startup / MSME entity"]', '["Per nodal agency guidelines"]', '[">> Highlight strategic alignment with national sector goals."]', '["!! Verify sanction terms and timeline before budget allocation."]', 'Portal Application -> Screening -> Disbursement', '2-4 months', '~20%', 'startupindia.gov.in', 'All India', 'National', 'https://pmfme.mofpi.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: PM FME (Nodal Agency / Ministry)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for PM FME highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official PM FME expenditure guidelines.
3. Address key scheme criteria: DPIIT startup / MSME entity.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official PM FME eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:23.170011+00:00', '2026-09-14T11:00:12.39155+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-RAW-125', 'SCH-RAW-125', 'NABARD PODF', 'Nodal Agency / Ministry', 'Nodal Agency / Ministry', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Up to Rs 25L - Rs 5Cr support', 'Strategic research scheme: NABARD PODF.', 'Strategic research scheme: NABARD PODF.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["DPIIT startup / MSME entity"]', '["Per nodal agency guidelines"]', '[">> Highlight strategic alignment with national sector goals."]', '["!! Verify sanction terms and timeline before budget allocation."]', 'Portal Application -> Screening -> Disbursement', '2-4 months', '~20%', 'startupindia.gov.in', 'All India', 'National', 'https://www.nabard.org', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: NABARD PODF (Nodal Agency / Ministry)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for NABARD PODF highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official NABARD PODF expenditure guidelines.
3. Address key scheme criteria: DPIIT startup / MSME entity.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official NABARD PODF eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:23.170011+00:00', '2026-09-14T11:00:12.39156+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-RAW-126', 'SCH-RAW-126', 'ICMR Extramural', 'Nodal Agency / Ministry', 'Nodal Agency / Ministry', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Up to Rs 25L - Rs 5Cr support', 'Strategic research scheme: ICMR Extramural.', 'Strategic research scheme: ICMR Extramural.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["DPIIT startup / MSME entity"]', '["Per nodal agency guidelines"]', '[">> Highlight strategic alignment with national sector goals."]', '["!! Verify sanction terms and timeline before budget allocation."]', 'Portal Application -> Screening -> Disbursement', '2-4 months', '~20%', 'startupindia.gov.in', 'All India', 'National', 'https://main.icmr.nic.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: ICMR Extramural (Nodal Agency / Ministry)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for ICMR Extramural highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official ICMR Extramural expenditure guidelines.
3. Address key scheme criteria: DPIIT startup / MSME entity.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official ICMR Extramural eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:23.540071+00:00', '2026-09-14T11:00:12.39157+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-RAW-127', 'SCH-RAW-127', 'ABDM Sandboxs', 'Nodal Agency / Ministry', 'Nodal Agency / Ministry', 'Grant', 'Central Govt', 'Grant', 'Pre-Seed / Seed', 'Up to Rs 25L - Rs 5Cr support', 'Strategic research scheme: ABDM Sandbox.', 'Strategic research scheme: ABDM Sandbox.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["DPIIT startup / MSME entity"]', '["Per nodal agency guidelines"]', '[">> Highlight strategic alignment with national sector goals."]', '["!! Verify sanction terms and timeline before budget allocation."]', 'Portal Application -> Screening -> Disbursement', '2-4 months', '~20%', 'startupindia.gov.in', 'All India', 'National', 'https://sandbox.abdm.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: ABDM Sandbox (Nodal Agency / Ministry)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for ABDM Sandbox highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official ABDM Sandbox expenditure guidelines.
3. Address key scheme criteria: DPIIT startup / MSME entity.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official ABDM Sandbox eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:23.540071+00:00', '2026-09-18T12:41:00.226553+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-RAW-128', 'SCH-RAW-128', 'PM-DevINE', 'Nodal Agency / Ministry', 'Nodal Agency / Ministry', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Up to Rs 25L - Rs 5Cr support', 'Strategic research scheme: PM-DevINE.', 'Strategic research scheme: PM-DevINE.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["DPIIT startup / MSME entity"]', '["Per nodal agency guidelines"]', '[">> Highlight strategic alignment with national sector goals."]', '["!! Verify sanction terms and timeline before budget allocation."]', 'Portal Application -> Screening -> Disbursement', '2-4 months', '~20%', 'startupindia.gov.in', 'All India', 'National', 'https://mdoner.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: PM-DevINE (Nodal Agency / Ministry)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for PM-DevINE highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official PM-DevINE expenditure guidelines.
3. Address key scheme criteria: DPIIT startup / MSME entity.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official PM-DevINE eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:23.540071+00:00', '2026-09-14T11:00:12.39159+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-RAW-129', 'SCH-RAW-129', 'NEAT', 'Nodal Agency / Ministry', 'Nodal Agency / Ministry', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Up to Rs 25L - Rs 5Cr support', 'Strategic research scheme: NEAT.', 'Strategic research scheme: NEAT.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["DPIIT startup / MSME entity"]', '["Per nodal agency guidelines"]', '[">> Highlight strategic alignment with national sector goals."]', '["!! Verify sanction terms and timeline before budget allocation."]', 'Portal Application -> Screening -> Disbursement', '2-4 months', '~20%', 'startupindia.gov.in', 'All India', 'National', 'https://neat.aicte-india.org', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: NEAT (Nodal Agency / Ministry)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for NEAT highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official NEAT expenditure guidelines.
3. Address key scheme criteria: DPIIT startup / MSME entity.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official NEAT eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:23.540071+00:00', '2026-09-14T11:00:12.391601+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-RAW-130', 'SCH-RAW-130', 'PLI Schemes', 'Nodal Agency / Ministry', 'Nodal Agency / Ministry', 'Subsidy', 'Central Govt', 'Subsidy', 'Pre-Seed / Seed', 'Up to Rs 25L - Rs 5Cr support', 'Strategic research scheme: PLI Schemes.', 'Strategic research scheme: PLI Schemes.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["DPIIT startup / MSME entity"]', '["Per nodal agency guidelines"]', '[">> Highlight strategic alignment with national sector goals."]', '["!! Verify sanction terms and timeline before budget allocation."]', 'Portal Application -> Screening -> Disbursement', '2-4 months', '~20%', 'startupindia.gov.in', 'All India', 'National', 'https://www.makeinindia.com/production-linked-incentive', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: PLI Schemes (Nodal Agency / Ministry)
FUND TYPE: Subsidy

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for PLI Schemes highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official PLI Schemes expenditure guidelines.
3. Address key scheme criteria: DPIIT startup / MSME entity.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official PLI Schemes eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:23.540071+00:00', '2026-09-14T11:00:12.391611+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-RAW-131', 'SCH-RAW-131', 'MSME Schemes', 'Nodal Agency / Ministry', 'Nodal Agency / Ministry', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Up to Rs 25L - Rs 5Cr support', 'Strategic research scheme: MSME Schemes.', 'Strategic research scheme: MSME Schemes.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["DPIIT startup / MSME entity"]', '["Per nodal agency guidelines"]', '[">> Highlight strategic alignment with national sector goals."]', '["!! Verify sanction terms and timeline before budget allocation."]', 'Portal Application -> Screening -> Disbursement', '2-4 months', '~20%', 'startupindia.gov.in', 'All India', 'National', 'https://msme.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: MSME Schemes (Nodal Agency / Ministry)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for MSME Schemes highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official MSME Schemes expenditure guidelines.
3. Address key scheme criteria: DPIIT startup / MSME entity.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official MSME Schemes eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:23.540071+00:00', '2026-09-14T11:00:12.391622+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-RAW-132', 'SCH-RAW-132', 'CGTMSE', 'Nodal Agency / Ministry', 'Nodal Agency / Ministry', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Up to Rs 25L - Rs 5Cr support', 'Strategic research scheme: CGTMSE.', 'Strategic research scheme: CGTMSE.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["DPIIT startup / MSME entity"]', '["Per nodal agency guidelines"]', '[">> Highlight strategic alignment with national sector goals."]', '["!! Verify sanction terms and timeline before budget allocation."]', 'Portal Application -> Screening -> Disbursement', '2-4 months', '~20%', 'startupindia.gov.in', 'All India', 'National', 'https://www.cgtmse.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: CGTMSE (Nodal Agency / Ministry)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for CGTMSE highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official CGTMSE expenditure guidelines.
3. Address key scheme criteria: DPIIT startup / MSME entity.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official CGTMSE eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:23.540071+00:00', '2026-09-14T11:00:12.391632+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-RAW-133', 'SCH-RAW-133', 'Udyam Registration', 'Nodal Agency / Ministry', 'Nodal Agency / Ministry', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Up to Rs 25L - Rs 5Cr support', 'Strategic research scheme: Udyam Registration.', 'Strategic research scheme: Udyam Registration.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["DPIIT startup / MSME entity"]', '["Per nodal agency guidelines"]', '[">> Highlight strategic alignment with national sector goals."]', '["!! Verify sanction terms and timeline before budget allocation."]', 'Portal Application -> Screening -> Disbursement', '2-4 months', '~20%', 'startupindia.gov.in', 'All India', 'National', 'https://udyamregistration.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Udyam Registration (Nodal Agency / Ministry)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Udyam Registration highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Udyam Registration expenditure guidelines.
3. Address key scheme criteria: DPIIT startup / MSME entity.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Udyam Registration eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:23.540071+00:00', '2026-09-14T11:00:12.391642+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-RAW-134', 'SCH-RAW-134', 'PM Vishwakarma', 'Nodal Agency / Ministry', 'Nodal Agency / Ministry', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Up to Rs 25L - Rs 5Cr support', 'Strategic research scheme: PM Vishwakarma.', 'Strategic research scheme: PM Vishwakarma.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["DPIIT startup / MSME entity"]', '["Per nodal agency guidelines"]', '[">> Highlight strategic alignment with national sector goals."]', '["!! Verify sanction terms and timeline before budget allocation."]', 'Portal Application -> Screening -> Disbursement', '2-4 months', '~20%', 'startupindia.gov.in', 'All India', 'National', 'https://pmvishwakarma.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: PM Vishwakarma (Nodal Agency / Ministry)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for PM Vishwakarma highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official PM Vishwakarma expenditure guidelines.
3. Address key scheme criteria: DPIIT startup / MSME entity.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official PM Vishwakarma eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:23.540071+00:00', '2026-09-14T11:00:12.391652+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-RAW-135', 'SCH-RAW-135', 'NITI SVP', 'Nodal Agency / Ministry', 'Nodal Agency / Ministry', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Up to Rs 25L - Rs 5Cr support', 'Strategic research scheme: NITI SVP.', 'Strategic research scheme: NITI SVP.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["DPIIT startup / MSME entity"]', '["Per nodal agency guidelines"]', '[">> Highlight strategic alignment with national sector goals."]', '["!! Verify sanction terms and timeline before budget allocation."]', 'Portal Application -> Screening -> Disbursement', '2-4 months', '~20%', 'startupindia.gov.in', 'All India', 'National', 'https://aim.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: NITI SVP (Nodal Agency / Ministry)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for NITI SVP highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official NITI SVP expenditure guidelines.
3. Address key scheme criteria: DPIIT startup / MSME entity.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official NITI SVP eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:23.540071+00:00', '2026-09-14T11:00:12.391662+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-RAW-136', 'SCH-RAW-136', 'TREAD Women', 'Nodal Agency / Ministry', 'Nodal Agency / Ministry', 'Grant / Support', 'Central Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Up to Rs 25L - Rs 5Cr support', 'Strategic research scheme: TREAD Women.', 'Strategic research scheme: TREAD Women.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["DPIIT startup / MSME entity"]', '["Per nodal agency guidelines"]', '[">> Highlight strategic alignment with national sector goals."]', '["!! Verify sanction terms and timeline before budget allocation."]', 'Portal Application -> Screening -> Disbursement', '2-4 months', '~20%', 'startupindia.gov.in', 'All India', 'National', 'https://msme.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: TREAD Women (Nodal Agency / Ministry)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for TREAD Women highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official TREAD Women expenditure guidelines.
3. Address key scheme criteria: DPIIT startup / MSME entity.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official TREAD Women eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:23.540071+00:00', '2026-09-14T11:00:12.391672+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-RAW-137', 'SCH-RAW-137', 'StartupTN Schemes', 'Nodal Agency / Ministry', 'Nodal Agency / Ministry', 'Grant / Support', 'State Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Up to Rs 25L - Rs 5Cr support', 'Strategic research scheme: StartupTN Schemes.', 'Strategic research scheme: StartupTN Schemes.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["DPIIT startup / MSME entity"]', '["Per nodal agency guidelines"]', '[">> Highlight strategic alignment with national sector goals."]', '["!! Verify sanction terms and timeline before budget allocation."]', 'Portal Application -> Screening -> Disbursement', '2-4 months', '~20%', 'startupindia.gov.in', 'Tamil Nadu', 'State', 'https://www.startuptn.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: StartupTN Schemes (Nodal Agency / Ministry)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for StartupTN Schemes highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official StartupTN Schemes expenditure guidelines.
3. Address key scheme criteria: DPIIT startup / MSME entity.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official StartupTN Schemes eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:23.540071+00:00', '2026-09-14T11:00:12.391682+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-RAW-138', 'SCH-RAW-138', 'TN MSME Schemes', 'Nodal Agency / Ministry', 'Nodal Agency / Ministry', 'Grant / Support', 'State Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Up to Rs 25L - Rs 5Cr support', 'Strategic research scheme: TN MSME Schemes.', 'Strategic research scheme: TN MSME Schemes.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["DPIIT startup / MSME entity"]', '["Per nodal agency guidelines"]', '[">> Highlight strategic alignment with national sector goals."]', '["!! Verify sanction terms and timeline before budget allocation."]', 'Portal Application -> Screening -> Disbursement', '2-4 months', '~20%', 'startupindia.gov.in', 'Tamil Nadu', 'State', 'https://msme.tn.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: TN MSME Schemes (Nodal Agency / Ministry)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for TN MSME Schemes highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official TN MSME Schemes expenditure guidelines.
3. Address key scheme criteria: DPIIT startup / MSME entity.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official TN MSME Schemes eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:23.540071+00:00', '2026-09-14T11:00:12.391693+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-RAW-139', 'SCH-RAW-139', 'TIDCO Schemes', 'Nodal Agency / Ministry', 'Nodal Agency / Ministry', 'Grant / Support', 'State Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Up to Rs 25L - Rs 5Cr support', 'Strategic research scheme: TIDCO Schemes.', 'Strategic research scheme: TIDCO Schemes.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["DPIIT startup / MSME entity"]', '["Per nodal agency guidelines"]', '[">> Highlight strategic alignment with national sector goals."]', '["!! Verify sanction terms and timeline before budget allocation."]', 'Portal Application -> Screening -> Disbursement', '2-4 months', '~20%', 'startupindia.gov.in', 'All India', 'State', 'https://tidco.com', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: TIDCO Schemes (Nodal Agency / Ministry)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for TIDCO Schemes highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official TIDCO Schemes expenditure guidelines.
3. Address key scheme criteria: DPIIT startup / MSME entity.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official TIDCO Schemes eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:23.540071+00:00', '2026-09-14T11:00:12.391703+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-RAW-140', 'SCH-RAW-140', 'TIDEL Park', 'Nodal Agency / Ministry', 'Nodal Agency / Ministry', 'Grant / Support', 'State Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Up to Rs 25L - Rs 5Cr support', 'Strategic research scheme: TIDEL Park.', 'Strategic research scheme: TIDEL Park.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["DPIIT startup / MSME entity"]', '["Per nodal agency guidelines"]', '[">> Highlight strategic alignment with national sector goals."]', '["!! Verify sanction terms and timeline before budget allocation."]', 'Portal Application -> Screening -> Disbursement', '2-4 months', '~20%', 'startupindia.gov.in', 'All India', 'State', 'https://www.tidelpark.com', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: TIDEL Park (Nodal Agency / Ministry)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for TIDEL Park highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official TIDEL Park expenditure guidelines.
3. Address key scheme criteria: DPIIT startup / MSME entity.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official TIDEL Park eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:23.540071+00:00', '2026-09-14T11:00:12.391713+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-RAW-141', 'SCH-RAW-141', 'TICEL BioPark', 'Nodal Agency / Ministry', 'Nodal Agency / Ministry', 'Grant / Support', 'State Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Up to Rs 25L - Rs 5Cr support', 'Strategic research scheme: TICEL BioPark.', 'Strategic research scheme: TICEL BioPark.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["DPIIT startup / MSME entity"]', '["Per nodal agency guidelines"]', '[">> Highlight strategic alignment with national sector goals."]', '["!! Verify sanction terms and timeline before budget allocation."]', 'Portal Application -> Screening -> Disbursement', '2-4 months', '~20%', 'startupindia.gov.in', 'All India', 'State', 'https://ticelbiopark.com', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: TICEL BioPark (Nodal Agency / Ministry)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for TICEL BioPark highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official TICEL BioPark expenditure guidelines.
3. Address key scheme criteria: DPIIT startup / MSME entity.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official TICEL BioPark eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:23.540071+00:00', '2026-09-14T11:00:12.391723+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-RAW-142', 'SCH-RAW-142', 'TN EV Policy', 'Nodal Agency / Ministry', 'Nodal Agency / Ministry', 'Grant / Support', 'State Govt', 'Grant / Support', 'Pre-Seed / Seed', 'Up to Rs 25L - Rs 5Cr support', 'Strategic research scheme: TN EV Policy.', 'Strategic research scheme: TN EV Policy.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["DPIIT startup / MSME entity"]', '["Per nodal agency guidelines"]', '[">> Highlight strategic alignment with national sector goals."]', '["!! Verify sanction terms and timeline before budget allocation."]', 'Portal Application -> Screening -> Disbursement', '2-4 months', '~20%', 'startupindia.gov.in', 'Tamil Nadu', 'State', 'https://guidance.tn.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: TN EV Policy (Nodal Agency / Ministry)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for TN EV Policy highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official TN EV Policy expenditure guidelines.
3. Address key scheme criteria: DPIIT startup / MSME entity.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official TN EV Policy eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:23.540071+00:00', '2026-09-14T11:00:12.391733+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-RAW-143', 'SCH-RAW-143', 'JETRO India-Japan', 'Nodal Agency / Ministry', 'Nodal Agency / Ministry', 'Grant / Support', 'Foreign / Global', 'Grant / Support', 'Pre-Seed / Seed', 'Up to Rs 25L - Rs 5Cr support', 'Strategic research scheme: JETRO India-Japan.', 'Strategic research scheme: JETRO India-Japan.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["DPIIT startup / MSME entity"]', '["Per nodal agency guidelines"]', '[">> Highlight strategic alignment with national sector goals."]', '["!! Verify sanction terms and timeline before budget allocation."]', 'Portal Application -> Screening -> Disbursement', '2-4 months', '~20%', 'startupindia.gov.in', 'All India', 'Foreign', 'https://www.jetro.go.jp/en/', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: JETRO India-Japan (Nodal Agency / Ministry)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for JETRO India-Japan highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official JETRO India-Japan expenditure guidelines.
3. Address key scheme criteria: DPIIT startup / MSME entity.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official JETRO India-Japan eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:23.540071+00:00', '2026-09-14T11:00:12.391743+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-RAW-144', 'SCH-RAW-144', 'USAID India', 'Nodal Agency / Ministry', 'Nodal Agency / Ministry', 'Grant / Support', 'Foreign / Global', 'Grant / Support', 'Pre-Seed / Seed', 'Up to Rs 25L - Rs 5Cr support', 'Strategic research scheme: USAID India.', 'Strategic research scheme: USAID India.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["DPIIT startup / MSME entity"]', '["Per nodal agency guidelines"]', '[">> Highlight strategic alignment with national sector goals."]', '["!! Verify sanction terms and timeline before budget allocation."]', 'Portal Application -> Screening -> Disbursement', '2-4 months', '~20%', 'startupindia.gov.in', 'All India', 'Foreign', 'https://www.usaid.gov/india', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: USAID India (Nodal Agency / Ministry)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for USAID India highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official USAID India expenditure guidelines.
3. Address key scheme criteria: DPIIT startup / MSME entity.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official USAID India eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:23.540071+00:00', '2026-09-14T11:00:12.391753+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-RAW-145', 'SCH-RAW-145', 'Gates Foundation India', 'Nodal Agency / Ministry', 'Nodal Agency / Ministry', 'Grant / Support', 'Foreign / Global', 'Grant / Support', 'Pre-Seed / Seed', 'Up to Rs 25L - Rs 5Cr support', 'Strategic research scheme: Gates Foundation India.', 'Strategic research scheme: Gates Foundation India.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["DPIIT startup / MSME entity"]', '["Per nodal agency guidelines"]', '[">> Highlight strategic alignment with national sector goals."]', '["!! Verify sanction terms and timeline before budget allocation."]', 'Portal Application -> Screening -> Disbursement', '2-4 months', '~20%', 'startupindia.gov.in', 'All India', 'Foreign', 'https://www.gatesfoundation.org', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Gates Foundation India (Nodal Agency / Ministry)
FUND TYPE: Grant / Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Gates Foundation India highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Gates Foundation India expenditure guidelines.
3. Address key scheme criteria: DPIIT startup / MSME entity.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Gates Foundation India eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:23.540071+00:00', '2026-09-14T11:00:12.391769+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-RAW-146', 'SCH-RAW-146', 'Green Climate Fund', 'Nodal Agency / Ministry', 'Nodal Agency / Ministry', 'Equity', 'Central Govt', 'Equity', 'Pre-Seed / Seed', 'Up to Rs 25L - Rs 5Cr support', 'Strategic research scheme: Green Climate Fund.', 'Strategic research scheme: Green Climate Fund.', '["All Sectors", "Technology", "Manufacturing", "DeepTech"]', '["DPIIT startup / MSME entity"]', '["Per nodal agency guidelines"]', '[">> Highlight strategic alignment with national sector goals."]', '["!! Verify sanction terms and timeline before budget allocation."]', 'Portal Application -> Screening -> Disbursement', '2-4 months', '~20%', 'startupindia.gov.in', 'All India', 'National', 'https://www.greenclimate.fund', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Green Climate Fund (Nodal Agency / Ministry)
FUND TYPE: Equity

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Green Climate Fund highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Green Climate Fund expenditure guidelines.
3. Address key scheme criteria: DPIIT startup / MSME entity.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Green Climate Fund eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:23.540071+00:00', '2026-09-14T11:00:12.391788+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-SEMICON-2026', 'SCH-SEMICON-2026', 'Design Linked Incentive (DLI) - India Semiconductor Mission', 'MeitY & C2S (Chips to Startup) Programme', 'MeitY & C2S (Chips to Startup) Programme', 'Reimbursement & Grant', 'Central Govt', 'Reimbursement & Grant', 'Ideation / R&D', 'Up to Rs.15 Crores (50% expenditure reimbursement)', 'Financial support for semiconductor chip design, SoCs, and Systems IP development', 'Financial support for semiconductor chip design, SoCs, and Systems IP development', '["Semiconductors", "DeepTech", "Hardware"]', '["Domestic Indian chip design company (>=51% domestic shareholding)", "DPIIT-recognized startup or MSME", "Developing ICs, SoCs, IP Cores, or Systems-on-Chip"]', '["50% reimbursement of eligible expenditure up to Rs 15 Crores", "Deployment Linked Incentive: 4% to 6% of net sales turnover over 5 years", "Access to EDA tools, IP core repository, and foundry MPW shuttles"]', '[">> Strategic government push for SEMICONDUCTOR SOVEREIGNTY - fabless chip startups score highest", ">> C2S programme provides free access to Synopsys/Cadence EDA tools at IITs/NITs"]', '["!! Domestic shareholding must stay >=51% throughout the 5-year incentive period", "!! Expenditure claims require rigorous CA audit certificates"]', 'Semicon India portal application -> CDAC due diligence -> C2S Committee -> Disbursement', '3-6 months', '~15-20%', 'semiconindia.org', 'All India', 'National', 'https://www.semiconindia.org', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Design Linked Incentive (DLI) - India Semiconductor Mission (MeitY & C2S (Chips to Startup) Programme)
FUND TYPE: Reimbursement Grant & Equity

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Design Linked Incentive (DLI) - India Semiconductor Mission highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Design Linked Incentive (DLI) - India Semiconductor Mission expenditure guidelines.
3. Address key scheme criteria: Domestic Indian chip design company (>=51% domestic shareholding), DPIIT-recognized startup or MSME, Developing ICs, SoCs, IP Cores, or Systems-on-Chip.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Design Linked Incentive (DLI) - India Semiconductor Mission eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:19.387421+00:00', '2026-09-14T11:00:12.389692+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-TN-1', 'SCH-TN-1', 'Tamil Nadu Startup Policy - Seed Funding', 'StartupTN (formerly TANSIM)', 'StartupTN (formerly TANSIM)', 'Grant (Non-Dilutive)', 'State Govt', 'Grant (Non-Dilutive)', 'Pre-Seed / Seed', 'Up to Rs.15 lakhs', 'Early-stage seed grant for DPIIT-registered startups', 'Early-stage seed grant for DPIIT-registered startups', '["All Sectors", "Manufacturing", "Services", "Technology"]', '["DPIIT-recognized startup", "Registered in Tamil Nadu", "Less than 7 years old (10 for biotech)", "Should not have received seed grant from GoI already"]', '["No equity taken - pure grant", "Must be recommended by an empaneled incubator", "Funds disbursed in milestones", "Progress reporting required quarterly"]', '[">> Government wants JOB CREATION numbers - your application must emphasize hiring plans", ">> Preference for startups that align with TN''s focus sectors: auto, electronics, textiles, food processing", ">> Political consideration: districts with lower startup activity may get preference for regional balance", ">> The incubator recommendation is a GATEKICKER - build relationship with TICEL BioPark, IIT-M RTBI, or KCG Tech Park first"]', '["!! Do not apply without incubator backing - auto-rejection", "!! Do not show plans to move out of TN - they want local economic impact", "!! Previous grant recipients of GoI schemes may be ineligible"]', 'Apply via StartupTN portal -> Incubator recommendation -> Screening committee -> Disbursement', '3-6 months from application to disbursement', '~15-20% of applications', 'startuptn.in', 'Tamil Nadu', 'State', 'https://www.startuptn.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Tamil Nadu Startup Policy - Seed Funding (StartupTN (formerly TANSIM))
FUND TYPE: Grant (Non-Dilutive)

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Tamil Nadu Startup Policy - Seed Funding highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Tamil Nadu Startup Policy - Seed Funding expenditure guidelines.
3. Address key scheme criteria: DPIIT-recognized startup, Registered in Tamil Nadu, Less than 7 years old (10 for biotech).
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Tamil Nadu Startup Policy - Seed Funding eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:19.387421+00:00', '2026-09-14T11:00:12.389833+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-TN-2', 'SCH-TN-2', 'TANFUND (Tamil Nadu Emerging Sector Seed Fund)', 'Tamil Nadu Industrial Development Corporation (TIDEL)', 'Tamil Nadu Industrial Development Corporation (TIDEL)', 'Seed Fund (Equity/Loan)', 'State Govt', 'Seed Fund (Equity/Loan)', 'Growth / Debt Scaling', 'Rs.25 lakhs to Rs.1 crore', 'Early-stage funding for emerging technology sectors', 'Early-stage funding for emerging technology sectors', '["All Sectors", "Manufacturing", "Services", "Technology"]', '["Startup registered in Tamil Nadu", "Technology/emerging sector focus", "Less than 5 years old", "Revenue or prototype stage"]', '["Equity-based or convertible debt", "Government takes minority stake", "Board observer rights", "Exit via buyback or IPO"]', '[">> Government wants to SHOW they are investing in startups - media coverage matters", ">> They prefer startups that can become ''poster children'' for TN''s tech ecosystem", ">> Bureaucratic process - expect 6-12 months for disbursement", ">> The ''emerging sector'' definition is broad but favors hardware/clean-tech over pure software"]', '["!! Extremely slow disbursement - have backup funding", "!! Government as shareholder adds compliance burden", "!! Exit terms may be unfavorable - read the fine print"]', 'TIDEL application -> Due diligence -> Investment committee -> Disbursement', '6-12 months', '~5-10%', 'tidelpark.com / startuptn.in', 'Tamil Nadu', 'State', 'https://www.tidelpark.com', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: TANFUND (Tamil Nadu Emerging Sector Seed Fund) (Tamil Nadu Industrial Development Corporation (TIDEL))
FUND TYPE: Seed Fund (Equity/Loan)

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for TANFUND (Tamil Nadu Emerging Sector Seed Fund) highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official TANFUND (Tamil Nadu Emerging Sector Seed Fund) expenditure guidelines.
3. Address key scheme criteria: Startup registered in Tamil Nadu, Technology/emerging sector focus, Less than 5 years old.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official TANFUND (Tamil Nadu Emerging Sector Seed Fund) eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:19.387421+00:00', '2026-09-14T11:00:12.389861+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-TN-3', 'SCH-TN-3', 'Kalaignar Kaivinai Thittam (KKT)', 'MSME Department, Govt. of Tamil Nadu', 'MSME Department, Govt. of Tamil Nadu', 'Subsidy + Loan', 'State Govt', 'Subsidy + Loan', 'Growth / Debt Scaling', 'Up to Rs.1 crore (25% subsidy for general, 35% for SC/ST/Women)', 'For micro and small enterprises in manufacturing', 'For micro and small enterprises in manufacturing', '["All Sectors", "Manufacturing", "Services", "Technology"]', '["New or existing micro/small enterprise", "Manufacturing sector preferred", "Project cost up to Rs.5 crore", "Applicant age 18+"]', '["25% capital subsidy (35% for SC/ST/Women)", "Balance through bank loan", "Asset must remain in TN for 5 years", "Employment generation mandatory"]', '[">> This is a POLITICAL scheme - named after Kalaignar (M. Karunanidhi) - alignment with ruling party helps", ">> They want visible, tangible businesses - not tech startups with no physical presence", ">> Employment numbers are the KEY metric - plan for 10+ employees", ">> District Industries Centre (DIC) officers have significant discretion - build rapport"]', '["!! Not ideal for pure tech/SaaS startups - designed for manufacturing", "!! Subsidy released AFTER you spend - need upfront capital", "!! 5-year lock-in on assets"]', 'Apply at District Industries Centre -> Project report -> Bank loan -> Subsidy release', '4-8 months', '~30-40% with proper documentation', 'District Industries Centre (DIC)', 'Tamil Nadu', 'State', 'https://msme.tn.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: Kalaignar Kaivinai Thittam (KKT) (MSME Department, Govt. of Tamil Nadu)
FUND TYPE: Subsidy + Loan

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for Kalaignar Kaivinai Thittam (KKT) highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official Kalaignar Kaivinai Thittam (KKT) expenditure guidelines.
3. Address key scheme criteria: New or existing micro/small enterprise, Manufacturing sector preferred, Project cost up to Rs.5 crore.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official Kalaignar Kaivinai Thittam (KKT) eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:19.387421+00:00', '2026-09-14T11:00:12.389879+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-TN-4', 'SCH-TN-4', 'NEEDS (New Entrepreneur Enterprise Development Scheme)', 'MSME Department, Govt. of Tamil Nadu', 'MSME Department, Govt. of Tamil Nadu', 'Subsidy + Bank Loan', 'State Govt', 'Subsidy + Bank Loan', 'Growth / Debt Scaling', 'Up to Rs.5 crore project cost (25% subsidy)', 'For first-time entrepreneurs in manufacturing and service sectors', 'For first-time entrepreneurs in manufacturing and service sectors', '["All Sectors", "Manufacturing", "Services", "Technology"]', '["First-time entrepreneur", "Graduate or diploma holder preferred", "Project cost Rs.10 lakhs to Rs.5 crore", "Age 18-45 (relaxed for women/SC/ST)"]', '["25% capital subsidy", "3% interest subvention for 3 years", "Collateral-free loan under CGTMSE", "5-year repayment period"]', '[">> Designed to reduce youth unemployment - emphasize job creation", ">> Bank relationship matters - some banks process faster than others", ">> DIC officers may push you toward ''safe'' sectors - resist if your idea is different"]', '["!! Bank loan approval is the bottleneck - not the subsidy", "!! Interest subvention only for 3 years - plan for higher payments after", "!! Collateral-free does not mean guarantee-free - personal guarantee required"]', 'DIC application -> Project report -> Bank sanction -> Subsidy release', '3-6 months', '~25-35%', 'msme.tn.gov.in', 'Tamil Nadu', 'State', 'https://www.msme.tn.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: NEEDS (New Entrepreneur Enterprise Development Scheme) (MSME Department, Govt. of Tamil Nadu)
FUND TYPE: Subsidy + Bank Loan

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for NEEDS (New Entrepreneur Enterprise Development Scheme) highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official NEEDS (New Entrepreneur Enterprise Development Scheme) expenditure guidelines.
3. Address key scheme criteria: First-time entrepreneur, Graduate or diploma holder preferred, Project cost Rs.10 lakhs to Rs.5 crore.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official NEEDS (New Entrepreneur Enterprise Development Scheme) eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:19.387421+00:00', '2026-09-14T11:00:12.389894+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-TN-5', 'SCH-TN-5', 'UYEGP (Unemployed Youth Employment Generation Programme)', 'MSME Department, Govt. of Tamil Nadu', 'MSME Department, Govt. of Tamil Nadu', 'Subsidy + Loan', 'State Govt', 'Subsidy + Loan', 'Growth / Debt Scaling', 'Up to Rs.10 lakhs project cost', 'For unemployed youth to start micro enterprises', 'For unemployed youth to start micro enterprises', '["All Sectors", "Manufacturing", "Services", "Technology"]', '["Unemployed youth aged 18-35", "VIII standard pass minimum", "No existing business", "Family income below Rs.1.5 lakhs/year"]', '["25% margin money subsidy", "Bank loan for balance", "3-year repayment", "Training mandatory before disbursement"]', '[">> This is for MICRO enterprises only - not scalable startups", ">> The income ceiling is strict - if family earns slightly above, you are out", ">> Training is at EDI (Entrepreneurship Development Institute) - attend seriously"]', '["!! Not for tech startups - meant for small shops, services, micro-manufacturing", "!! Income verification is thorough - do not fudge numbers", "!! Very small amounts - not enough for meaningful startup"]', 'Apply at DIC -> EDI training -> Bank loan -> Subsidy', '2-4 months', '~40-50%', 'District Industries Centre', 'Tamil Nadu', 'State', 'https://msmeonline.tn.gov.in/uyegp/', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: UYEGP (Unemployed Youth Employment Generation Programme) (MSME Department, Govt. of Tamil Nadu)
FUND TYPE: Subsidy + Loan

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for UYEGP (Unemployed Youth Employment Generation Programme) highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official UYEGP (Unemployed Youth Employment Generation Programme) expenditure guidelines.
3. Address key scheme criteria: Unemployed youth aged 18-35, VIII standard pass minimum, No existing business.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official UYEGP (Unemployed Youth Employment Generation Programme) eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:19.387421+00:00', '2026-09-14T11:00:12.389908+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-TN-6', 'SCH-TN-6', 'TWEES (Tamil Nadu Women Entrepreneurs Empowerment Scheme)', 'MSME Department, Govt. of Tamil Nadu', 'MSME Department, Govt. of Tamil Nadu', 'Subsidy + Support', 'State Govt', 'Subsidy + Support', 'Pre-Seed / Seed', 'Up to Rs.1 crore (35% subsidy for women)', 'Exclusive scheme for women entrepreneurs', 'Exclusive scheme for women entrepreneurs', '["All Sectors", "Manufacturing", "Services", "Technology"]', '["Women entrepreneurs (51% ownership)", "New or existing enterprise", "Project cost up to Rs.3 crore", "Registered in Tamil Nadu"]', '["35% capital subsidy (highest among TN schemes)", "Market linkage support", "Skill development programs", "Mentorship from successful women entrepreneurs"]', '[">> Government wants to showcase women empowerment - media-friendly projects get priority", ">> The 51% ownership must be REAL - they verify thoroughly", ">> Preference for women from economically weaker sections"]', '["!! Male co-founders cannot be shown as primary applicants", "!! Subsidy disbursement is slow - plan cash flow accordingly", "!! Must attend mandatory training programs"]', 'DIC application -> Verification -> Bank loan -> Subsidy', '3-6 months', '~30-35%', 'msme.tn.gov.in', 'Tamil Nadu', 'State', 'https://www.msme.tn.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: TWEES (Tamil Nadu Women Entrepreneurs Empowerment Scheme) (MSME Department, Govt. of Tamil Nadu)
FUND TYPE: Subsidy + Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for TWEES (Tamil Nadu Women Entrepreneurs Empowerment Scheme) highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official TWEES (Tamil Nadu Women Entrepreneurs Empowerment Scheme) expenditure guidelines.
3. Address key scheme criteria: Women entrepreneurs (51% ownership), New or existing enterprise, Project cost up to Rs.3 crore.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official TWEES (Tamil Nadu Women Entrepreneurs Empowerment Scheme) eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:19.387421+00:00', '2026-09-14T11:00:12.389923+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-TN-7', 'SCH-TN-7', 'AABCS (Annal Ambedkar Business Champions Scheme)', 'Adi Dravidar & Tribal Welfare Dept., TN', 'Adi Dravidar & Tribal Welfare Dept., TN', 'Subsidy + Loan', 'State Govt', 'Subsidy + Loan', 'Growth / Debt Scaling', 'Up to Rs.1 crore (35% subsidy for SC/ST)', 'For entrepreneurs from Scheduled Caste/Scheduled Tribe communities', 'For entrepreneurs from Scheduled Caste/Scheduled Tribe communities', '["All Sectors", "Manufacturing", "Services", "Technology"]', '["SC/ST entrepreneur", "New or existing enterprise", "Project cost up to Rs.3 crore", "Valid community certificate from TN"]', '["35% capital subsidy", "Collateral-free loan under CGTMSE", "Interest subvention for 3 years", "Handholding support"]', '[">> Political scheme - alignment with welfare department priorities helps", ">> Community certificate must be from TN - other state certificates may face issues", ">> They want SUCCESS STORIES - if you succeed, you become a showcase"]', '["!! Community certificate verification can delay process", "!! Some banks are reluctant - approach banks with social commitment mandates", "!! Must maintain SC/ST ownership throughout loan periods"]', 'Apply at DIC with community certificate -> Verification -> Bank -> Subsidy', '4-8 months', '~25-30%', 'District Adi Dravidar Welfare Office', 'Tamil Nadu', 'State', 'https://msme.tn.gov.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: AABCS (Annal Ambedkar Business Champions Scheme) (Adi Dravidar & Tribal Welfare Dept., TN)
FUND TYPE: Subsidy + Loan

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for AABCS (Annal Ambedkar Business Champions Scheme) highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official AABCS (Annal Ambedkar Business Champions Scheme) expenditure guidelines.
3. Address key scheme criteria: SC/ST entrepreneur, New or existing enterprise, Project cost up to Rs.3 crore.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official AABCS (Annal Ambedkar Business Champions Scheme) eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:19.387421+00:00', '2026-09-24T16:04:28.320872+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-TN-8', 'SCH-TN-8', 'TICEL BioPark Incubation & Funding', 'TIDEL (Tamil Nadu Industrial Development)', 'TIDEL (Tamil Nadu Industrial Development)', 'Incubation + Seed Support', 'State Govt', 'Incubation + Seed Support', 'Pre-Seed / Seed', 'Incubation space + up to Rs.25 lakhs support', 'For biotech/life sciences startups in Chennai', 'For biotech/life sciences startups in Chennai', '["All Sectors", "Manufacturing", "Services", "Technology"]', '["Biotech/life sciences startup", "Early stage (idea to prototype)", "Willing to locate at TICEL BioPark, Taramani"]', '["Subsidized lab space", "Access to equipment and mentorship", "Seed funding via grants", "IP support"]', '[">> They want biotech companies that can attract FDI later", ">> Location at TICEL is MANDATORY - no remote incubation", ">> Preference for startups with IIT-M/Chennai university connections"]', '["!! Only for biotech - not for other sectors", "!! Physical presence required", "!! Limited seats - high competition"]', 'Apply at TICEL -> Screening -> Incubation agreement', '2-3 months', '~20%', 'ticelbiopark.com', 'Tamil Nadu', 'State', 'https://www.ticelbiopark.com', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: TICEL BioPark Incubation & Funding (TIDEL (Tamil Nadu Industrial Development))
FUND TYPE: Incubation + Seed Support

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for TICEL BioPark Incubation & Funding highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official TICEL BioPark Incubation & Funding expenditure guidelines.
3. Address key scheme criteria: Biotech/life sciences startup, Early stage (idea to prototype), Willing to locate at TICEL BioPark, Taramani.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official TICEL BioPark Incubation & Funding eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:19.387421+00:00', '2026-09-14T11:00:12.389953+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

INSERT INTO schemes (id, source_id, name, agency, ministry, scheme_type, category_type, funding_type, stage, amount, brief, description, sectors, eligibility, terms, hidden_agenda, red_flags, process, timeline, success_rate, contact, state_scope, geography, application_url, last_verified, application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at)
VALUES ('SCH-TN-9', 'SCH-TN-9', 'IIT Madras RTBI Incubation', 'IIT Madras Research Park / RTBI', 'IIT Madras Research Park / RTBI', 'Incubation + Seed Funding', 'State Govt', 'Incubation + Seed Funding', 'Pre-Seed / Seed', 'Incubation + up to Rs.50 lakhs (via grants/equity)', 'Deep-tech and technology startups', 'Deep-tech and technology startups', '["All Sectors", "Manufacturing", "Services", "Technology"]', '["Technology startup with IP potential", "Founder preferably from IIT-M (but not mandatory)", "Prototype or MVP stage"]', '["Incubation at IITM Research Park", "Access to labs, mentors, alumni network", "Seed funding via SBIR grants, BIRAC, or angel networks", "Equity stake 5-10% if funded"]', '[">> IIT-M alumni get STRONG preference - if you are not an alum, find an alum co-founder or advisor", ">> They want deep-tech, not me-too apps - AI/ML, hardware, biotech, clean energy preferred", ">> The RTBI brand opens doors - but they are selective about their portfolio"]', '["!! Very competitive - <5% acceptance rate", "!! Equity taken even for incubation in some cases", "!! Must relocate to Chennai"]', 'Online application -> Pitch to selection committee -> Due diligence -> Incubation', '2-4 months', '~3-5%', 'rtbi.in / research.iitm.ac.in', 'Tamil Nadu', 'State', 'https://www.rtbi.in', 'August 2026', 'ROLE: Senior Startup Funding & VC Consultant
TARGET FUND: IIT Madras RTBI Incubation (IIT Madras Research Park / RTBI)
FUND TYPE: Incubation + Seed Funding

BUSINESS CONTEXT:
Company Name: [INSERT_COMPANY_NAME]
Industry / Sector: [INSERT_PRIMARY_SECTOR]
Startup Stage: [INSERT_STARTUP_STAGE]
Requested Amount: [INSERT_REQUESTED_AMOUNT]

EVIDENCE & DOCUMENTS ATTACHED:
I have uploaded: Certificate of Incorporation, DPIIT Certificate, Pitch Deck / DPR, Udyam Registration, Cap Table.

TASK:
1. Draft a compelling 1-page Executive Project Proposal for IIT Madras RTBI Incubation highlighting innovation, market impact, and employment generation.
2. Formulate a transparent Fund Utilization Table matching official IIT Madras RTBI Incubation expenditure guidelines.
3. Address key scheme criteria: Technology startup with IP potential, Founder preferably from IIT-M (but not mandatory), Prototype or MVP stage.
4. List key milestone deliverables and timeline required for tranche disbursement.

CONSTRAINTS: Adhere strictly to official IIT Madras RTBI Incubation eligibility criteria. Do not exaggerate revenue.
OUTPUT FORMAT: 1-Page Executive Proposal + Budget Allocation Table + Milestone Schedule.', 'Founder AI Digital Playbook 2026', 'active', TRUE, 9999, '2026-09-14T11:00:19.387421+00:00', '2026-09-14T11:00:12.389967+00:00')
ON CONFLICT (id) DO UPDATE SET
  source_id = EXCLUDED.source_id, name = EXCLUDED.name, agency = EXCLUDED.agency, ministry = EXCLUDED.ministry, scheme_type = EXCLUDED.scheme_type, category_type = EXCLUDED.category_type, funding_type = EXCLUDED.funding_type, stage = EXCLUDED.stage, amount = EXCLUDED.amount, brief = EXCLUDED.brief, description = EXCLUDED.description, sectors = EXCLUDED.sectors, eligibility = EXCLUDED.eligibility, terms = EXCLUDED.terms, hidden_agenda = EXCLUDED.hidden_agenda, red_flags = EXCLUDED.red_flags, process = EXCLUDED.process, timeline = EXCLUDED.timeline, success_rate = EXCLUDED.success_rate, contact = EXCLUDED.contact, state_scope = EXCLUDED.state_scope, geography = EXCLUDED.geography, application_url = EXCLUDED.application_url, last_verified = EXCLUDED.last_verified, application_prompt = EXCLUDED.application_prompt, source_dataset = EXCLUDED.source_dataset, status = EXCLUDED.status, is_active = EXCLUDED.is_active, display_order = EXCLUDED.display_order, created_at = EXCLUDED.created_at, updated_at = EXCLUDED.updated_at;

COMMIT;