"""
services/local_db.py — Resilient Persistent Local Database Engine
==================================================================
Implements identical PostgreSQL schema and relationships in SQLite
to ensure 100% testability, zero crashes, and seamless synchronization
with Supabase cloud tables.
"""

import sqlite3
import json
import os
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any, Tuple

DB_PATH = Path(__file__).resolve().parent.parent / "cluster_a.db"

class LocalDatabase:
    def __init__(self, db_file: Path = DB_PATH):
        self.db_file = db_file
        self._init_db()

    def _get_conn(self):
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        conn = self._get_conn()
        cur = conn.cursor()

        # 1. Profiles
        cur.execute("""
        CREATE TABLE IF NOT EXISTS profiles (
            id TEXT PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('aspirant', 'guide', 'sme', 'admin')),
            full_name TEXT NOT NULL,
            phone TEXT,
            district TEXT,
            state TEXT DEFAULT 'Tamil Nadu',
            profile_data TEXT DEFAULT '{}',
            is_active INTEGER DEFAULT 1,
            password_hash TEXT,
            created_at TEXT,
            updated_at TEXT
        );
        """)

        # 2. Relationships
        cur.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id TEXT PRIMARY KEY,
            aspirant_id TEXT UNIQUE NOT NULL REFERENCES profiles(id),
            guide_id TEXT REFERENCES profiles(id),
            sme_id TEXT REFERENCES profiles(id),
            sme_ids TEXT DEFAULT '[]',
            assigned_by TEXT REFERENCES profiles(id),
            status TEXT DEFAULT 'active',
            notes TEXT,
            created_at TEXT,
            updated_at TEXT
        );
        """)

        # 3. Journeys
        cur.execute("""
        CREATE TABLE IF NOT EXISTS journeys (
            id TEXT PRIMARY KEY,
            aspirant_id TEXT UNIQUE NOT NULL REFERENCES profiles(id),
            title TEXT NOT NULL,
            business_type TEXT,
            stage TEXT DEFAULT 'idea',
            start_date TEXT,
            status TEXT DEFAULT 'active',
            created_at TEXT,
            updated_at TEXT
        );
        """)

        # 4. Journey Events
        cur.execute("""
        CREATE TABLE IF NOT EXISTS journey_events (
            id TEXT PRIMARY KEY,
            journey_id TEXT NOT NULL REFERENCES journeys(id),
            aspirant_id TEXT NOT NULL REFERENCES profiles(id),
            actor_id TEXT NOT NULL REFERENCES profiles(id),
            actor_role TEXT NOT NULL,
            event_type TEXT NOT NULL,
            event_data TEXT NOT NULL DEFAULT '{}',
            event_date TEXT,
            deleted_at TEXT,
            deleted_by TEXT,
            created_at TEXT,
            updated_at TEXT
        );
        """)

        # 4B. Journey Event Revisions (Audit Trail)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS journey_event_revisions (
            id TEXT PRIMARY KEY,
            journey_event_id TEXT NOT NULL REFERENCES journey_events(id),
            editor_id TEXT NOT NULL REFERENCES profiles(id),
            editor_role TEXT NOT NULL,
            previous_data TEXT NOT NULL DEFAULT '{}',
            new_data TEXT NOT NULL DEFAULT '{}',
            revision_number INTEGER NOT NULL DEFAULT 1,
            change_reason TEXT,
            created_at TEXT
        );
        """)
        cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_rev_event ON journey_event_revisions(journey_event_id);
        """)

        # 5. Help Requests
        cur.execute("""
        CREATE TABLE IF NOT EXISTS help_requests (
            id TEXT PRIMARY KEY,
            aspirant_id TEXT NOT NULL REFERENCES profiles(id),
            subject TEXT NOT NULL,
            message TEXT NOT NULL,
            priority TEXT DEFAULT 'MEDIUM',
            status TEXT DEFAULT 'OPEN',
            admin_response TEXT,
            responded_by TEXT,
            created_at TEXT,
            updated_at TEXT
        );
        """)

        # 6. Schemes
        cur.execute("""
        CREATE TABLE IF NOT EXISTS schemes (
            id TEXT PRIMARY KEY,
            source_id TEXT,
            name TEXT NOT NULL,
            agency TEXT,
            ministry TEXT,
            scheme_type TEXT,
            category_type TEXT,
            funding_type TEXT,
            stage TEXT,
            amount TEXT,
            brief TEXT,
            description TEXT,
            sectors TEXT DEFAULT '[]',
            eligibility TEXT DEFAULT '[]',
            terms TEXT DEFAULT '[]',
            hidden_agenda TEXT DEFAULT '[]',
            red_flags TEXT DEFAULT '[]',
            process TEXT,
            timeline TEXT,
            success_rate TEXT,
            contact TEXT,
            state_scope TEXT,
            geography TEXT,
            application_url TEXT,
            last_verified TEXT,
            application_prompt TEXT,
            source_dataset TEXT,
            status TEXT DEFAULT 'active',
            is_active INTEGER DEFAULT 1,
            display_order INTEGER DEFAULT 9999,
            created_at TEXT,
            updated_at TEXT
        );
        """)

        # 7. Activity Log
        cur.execute("""
        CREATE TABLE IF NOT EXISTS activity_log (
            id TEXT PRIMARY KEY,
            user_id TEXT,
            action TEXT NOT NULL,
            entity TEXT NOT NULL,
            entity_id TEXT,
            details TEXT DEFAULT '{}',
            created_at TEXT
        );
        """)

        # 8. Scheme Releases (Guide Governance & Visibility Gate)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS scheme_releases (
            id TEXT PRIMARY KEY,
            aspirant_id TEXT NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
            guide_id TEXT NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
            scheme_id TEXT NOT NULL REFERENCES schemes(id) ON DELETE CASCADE,
            status TEXT NOT NULL DEFAULT 'RELEASED' CHECK(status IN ('DRAFT', 'RELEASED', 'WITHDRAWN')),
            guide_note TEXT,
            guide_recommendation TEXT,
            eligibility_summary TEXT,
            released_at TEXT,
            released_by TEXT REFERENCES profiles(id),
            withdrawn_at TEXT,
            withdrawn_by TEXT REFERENCES profiles(id),
            created_at TEXT,
            updated_at TEXT,
            UNIQUE(aspirant_id, scheme_id)
        );
        """)

        cur.execute("CREATE INDEX IF NOT EXISTS idx_sr_aspirant ON scheme_releases(aspirant_id);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_sr_guide ON scheme_releases(guide_id);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_sr_scheme ON scheme_releases(scheme_id);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_sr_status ON scheme_releases(status);")

        # 9. Notifications (In-App Universal Alert System)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
            actor_id TEXT REFERENCES profiles(id),
            title TEXT NOT NULL,
            message TEXT NOT NULL,
            notification_type TEXT NOT NULL,
            link TEXT,
            is_read INTEGER DEFAULT 0,
            created_at TEXT
        );
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_notif_user ON notifications(user_id, created_at DESC);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_notif_unread ON notifications(user_id, is_read);")

        # 10. Assignment History (Roster Transition & Audit Log)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS assignment_history (
            id TEXT PRIMARY KEY,
            aspirant_id TEXT NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
            mentor_id TEXT NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
            mentor_role TEXT NOT NULL CHECK(mentor_role IN ('guide', 'sme')),
            assigned_by TEXT REFERENCES profiles(id),
            action TEXT NOT NULL CHECK(action IN ('ASSIGNED', 'REPLACED', 'UNASSIGNED')),
            previous_mentor_id TEXT REFERENCES profiles(id),
            notes TEXT,
            created_at TEXT
        );
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_asghist_asp ON assignment_history(aspirant_id);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_asghist_mentor ON assignment_history(mentor_id);")

        conn.commit()

        # Dynamic schema migration: ensure display_order exists in schemes table
        cur.execute("PRAGMA table_info(schemes)")
        existing_cols = [r[1] for r in cur.fetchall()]
        if "display_order" not in existing_cols:
            try:
                cur.execute("ALTER TABLE schemes ADD COLUMN display_order INTEGER DEFAULT 9999")
                conn.commit()
            except Exception as e:
                print(f"[LocalDB] Migration notice: {e}")

        # Dynamic schema migration: ensure sme_ids and guide_ids exist in relationships table
        cur.execute("PRAGMA table_info(relationships)")
        rel_cols = [r[1] for r in cur.fetchall()]
        if "sme_ids" not in rel_cols:
            try:
                cur.execute("ALTER TABLE relationships ADD COLUMN sme_ids TEXT DEFAULT '[]'")
                conn.commit()
            except Exception as e:
                print(f"[LocalDB] Relationships migration notice (sme_ids): {e}")
        if "guide_ids" not in rel_cols:
            try:
                cur.execute("ALTER TABLE relationships ADD COLUMN guide_ids TEXT DEFAULT '[]'")
                conn.commit()
            except Exception as e:
                print(f"[LocalDB] Relationships migration notice (guide_ids): {e}")

        # Dynamic schema migration: ensure guide routing & escalation columns exist in help_requests
        cur.execute("PRAGMA table_info(help_requests)")
        hr_cols = [r[1] for r in cur.fetchall()]
        if "assigned_guide_id" not in hr_cols:
            try: cur.execute("ALTER TABLE help_requests ADD COLUMN assigned_guide_id TEXT REFERENCES profiles(id)")
            except Exception: pass
        if "assigned_at" not in hr_cols:
            try: cur.execute("ALTER TABLE help_requests ADD COLUMN assigned_at TEXT")
            except Exception: pass
        if "last_handled_at" not in hr_cols:
            try: cur.execute("ALTER TABLE help_requests ADD COLUMN last_handled_at TEXT")
            except Exception: pass
        if "escalated_at" not in hr_cols:
            try: cur.execute("ALTER TABLE help_requests ADD COLUMN escalated_at TEXT")
            except Exception: pass
        if "escalation_reason" not in hr_cols:
            try: cur.execute("ALTER TABLE help_requests ADD COLUMN escalation_reason TEXT")
            except Exception: pass
        if "resolved_by" not in hr_cols:
            try: cur.execute("ALTER TABLE help_requests ADD COLUMN resolved_by TEXT REFERENCES profiles(id)")
            except Exception: pass
        if "guide_response" not in hr_cols:
            try: cur.execute("ALTER TABLE help_requests ADD COLUMN guide_response TEXT")
            except Exception: pass
        if "category" not in hr_cols:
            try: cur.execute("ALTER TABLE help_requests ADD COLUMN category TEXT DEFAULT 'GENERAL'")
            except Exception: pass
        if "assigned_sme_id" not in hr_cols:
            try: cur.execute("ALTER TABLE help_requests ADD COLUMN assigned_sme_id TEXT REFERENCES profiles(id)")
            except Exception: pass
        if "sme_response" not in hr_cols:
            try: cur.execute("ALTER TABLE help_requests ADD COLUMN sme_response TEXT")
            except Exception: pass
        if "target_role" not in hr_cols:
            try: cur.execute("ALTER TABLE help_requests ADD COLUMN target_role TEXT DEFAULT 'guide'")
            except Exception: pass
        if "requester_id" not in hr_cols:
            try: cur.execute("ALTER TABLE help_requests ADD COLUMN requester_id TEXT REFERENCES profiles(id)")
            except Exception: pass
        if "requester_role" not in hr_cols:
            try: cur.execute("ALTER TABLE help_requests ADD COLUMN requester_role TEXT DEFAULT 'aspirant'")
            except Exception: pass
        if "request_type" not in hr_cols:
            try: cur.execute("ALTER TABLE help_requests ADD COLUMN request_type TEXT DEFAULT 'aspirant_consultation'")
            except Exception: pass
        if "category_detail" not in hr_cols:
            try: cur.execute("ALTER TABLE help_requests ADD COLUMN category_detail TEXT")
            except Exception: pass
        if "admin_directive" not in hr_cols:
            try: cur.execute("ALTER TABLE help_requests ADD COLUMN admin_directive TEXT")
            except Exception: pass
        if "directive_issued_at" not in hr_cols:
            try: cur.execute("ALTER TABLE help_requests ADD COLUMN directive_issued_at TEXT")
            except Exception: pass
        if "aspirant_response" not in hr_cols:
            try: cur.execute("ALTER TABLE help_requests ADD COLUMN aspirant_response TEXT")
            except Exception: pass
        if "aspirant_responded_at" not in hr_cols:
            try: cur.execute("ALTER TABLE help_requests ADD COLUMN aspirant_responded_at TEXT")
            except Exception: pass
        conn.commit()

        # Seed default super admin (fulcrumindia1@gmail.com) if missing
        cur.execute("SELECT id FROM profiles WHERE email = 'fulcrumindia1@gmail.com' LIMIT 1")
        if not cur.fetchone():
            now_iso = datetime.now(timezone.utc).isoformat()
            admin_id = "616304b5-aef5-4cd0-88be-2fda7ddf7f88"
            admin_pw_hash = hashlib.sha256("Admin@123".encode("utf-8")).hexdigest()
            cur.execute("""
            INSERT INTO profiles (id, email, role, full_name, phone, district, state, password_hash, profile_data, is_active, created_at, updated_at)
            VALUES (?, ?, 'admin', 'Fulcrum Administrator', '9876543213', 'Chennai', 'Tamil Nadu', ?, '{}', 1, ?, ?)
            """, (admin_id, "fulcrumindia1@gmail.com", admin_pw_hash, now_iso, now_iso))
            conn.commit()

        # Seed 170 schemes from seed/schemes.json if empty
        cur.execute("SELECT COUNT(*) FROM schemes")
        count = cur.fetchone()[0]
        if count == 0:
            seed_json = Path(__file__).resolve().parent.parent / "seed" / "schemes.json"
            if seed_json.exists():
                try:
                    with open(seed_json, "r", encoding="utf-8") as f:
                        schemes_list = json.load(f)
                    for idx, s in enumerate(schemes_list):
                        cur.execute("""
                        INSERT OR REPLACE INTO schemes (
                            id, source_id, name, agency, ministry, scheme_type, category_type,
                            funding_type, stage, amount, brief, description, sectors, eligibility,
                            terms, hidden_agenda, red_flags, process, timeline, success_rate,
                            contact, state_scope, geography, application_url, last_verified,
                            application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            s["id"], s.get("source_id"), s["name"], s.get("agency"), s.get("ministry"),
                            s.get("scheme_type"), s.get("category_type"), s.get("funding_type"), s.get("stage"),
                            s.get("amount"), s.get("brief"), s.get("description"),
                            json.dumps(s.get("sectors", [])), json.dumps(s.get("eligibility", [])),
                            json.dumps(s.get("terms", [])), json.dumps(s.get("hidden_agenda", [])),
                            json.dumps(s.get("red_flags", [])), s.get("process"), s.get("timeline"),
                            s.get("success_rate"), s.get("contact"), s.get("state_scope"), s.get("geography"),
                            s.get("application_url"), s.get("last_verified"), s.get("application_prompt"),
                            s.get("source_dataset"), s.get("status", "active"), 1 if s.get("is_active", True) else 0,
                            s.get("display_order", idx + 1),
                            datetime.now(timezone.utc).isoformat(), datetime.now(timezone.utc).isoformat()
                        ))
                    conn.commit()
                except Exception as e:
                    print(f"[LocalDB] Notice seeding schemes: {e}")

        # ── 11. Multi-Role & Legal Governance Tables ──
        cur.execute("""
        CREATE TABLE IF NOT EXISTS user_roles (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
            role TEXT NOT NULL CHECK (role IN ('aspirant', 'guide', 'sme', 'admin', 'district_admin', 'operational_admin')),
            status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'pending_nda', 'suspended', 'revoked')),
            granted_by TEXT REFERENCES profiles(id),
            granted_at TEXT,
            activated_at TEXT,
            suspended_at TEXT,
            revoked_at TEXT,
            revocation_reason TEXT,
            created_at TEXT,
            updated_at TEXT,
            UNIQUE(user_id, role)
        );
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_user_roles_user ON user_roles(user_id);")

        cur.execute("""
        CREATE TABLE IF NOT EXISTS legal_documents (
            id TEXT PRIMARY KEY,
            doc_type TEXT NOT NULL CHECK (doc_type IN ('terms_and_conditions', 'nda_guide', 'nda_sme', 'nda_dual')),
            version TEXT NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            content_hash TEXT NOT NULL,
            roles_covered TEXT DEFAULT '[]',
            effective_date TEXT,
            is_mandatory INTEGER DEFAULT 1,
            is_active INTEGER DEFAULT 1,
            created_at TEXT
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS legal_acceptances (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
            document_id TEXT NOT NULL,
            doc_type TEXT NOT NULL,
            doc_version TEXT NOT NULL,
            doc_hash TEXT NOT NULL,
            user_email_snapshot TEXT NOT NULL,
            typed_legal_name TEXT NOT NULL,
            typed_acceptance_phrase TEXT NOT NULL,
            checkbox_confirmed INTEGER DEFAULT 1,
            roles_covered TEXT DEFAULT '[]',
            ip_address TEXT,
            user_agent TEXT,
            status TEXT DEFAULT 'ACCEPTED',
            accepted_at TEXT
        );
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_legal_acceptances_user ON legal_acceptances(user_id, doc_type);")

        cur.execute("""
        CREATE TABLE IF NOT EXISTS guide_complaints (
            id TEXT PRIMARY KEY,
            aspirant_id TEXT NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
            guide_id TEXT NOT NULL REFERENCES profiles(id),
            reason TEXT NOT NULL CHECK (reason IN ('inactivity', 'poor_communication', 'conflict_of_interest', 'professional_conduct', 'other')),
            details TEXT,
            status TEXT DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'UNDER_REVIEW', 'RESOLVED', 'DISMISSED')),
            resolution_notes TEXT,
            resolved_by TEXT REFERENCES profiles(id),
            resolved_at TEXT,
            created_at TEXT
        );
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_guide_complaints_asp ON guide_complaints(aspirant_id);")

        cur.execute("""
        CREATE TABLE IF NOT EXISTS sme_conflict_declarations (
            id TEXT PRIMARY KEY,
            sme_id TEXT NOT NULL REFERENCES profiles(id),
            aspirant_id TEXT NOT NULL REFERENCES profiles(id),
            has_conflict INTEGER DEFAULT 0,
            conflict_details TEXT,
            status TEXT DEFAULT 'DECLARED' CHECK (status IN ('DECLARED', 'APPROVED', 'REJECTED')),
            reviewed_by TEXT REFERENCES profiles(id),
            reviewed_at TEXT,
            created_at TEXT
        );
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_sme_conflict ON sme_conflict_declarations(sme_id, aspirant_id);")

        cur.execute("""
        CREATE TABLE IF NOT EXISTS case_discussions (
            id TEXT PRIMARY KEY,
            aspirant_id TEXT NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
            author_id TEXT NOT NULL REFERENCES profiles(id),
            author_role TEXT NOT NULL,
            title TEXT NOT NULL,
            message TEXT NOT NULL,
            attachments TEXT DEFAULT '[]',
            is_private_mentor_note INTEGER DEFAULT 0,
            created_at TEXT
        );
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_case_discussions_asp ON case_discussions(aspirant_id);")

        cur.execute("""
        CREATE TABLE IF NOT EXISTS inactivity_logs (
            id TEXT PRIMARY KEY,
            relationship_id TEXT,
            guide_id TEXT NOT NULL REFERENCES profiles(id),
            aspirant_id TEXT NOT NULL REFERENCES profiles(id),
            days_inactive INTEGER NOT NULL,
            escalation_stage TEXT NOT NULL CHECK (escalation_stage IN ('DAY_7_REMINDER', 'DAY_10_ADMIN_ALERT', 'DAY_14_ADMIN_REVIEW')),
            notification_sent_at TEXT,
            created_at TEXT,
            mentor_id TEXT REFERENCES profiles(id),
            mentor_role TEXT DEFAULT 'guide',
            inactivity_episode TEXT,
            status TEXT DEFAULT 'ACTIVE',
            follow_up_channel TEXT,
            follow_up_sent_at TEXT,
            follow_up_notes TEXT
        );
        """)

        # Dynamic schema migration for inactivity_logs
        cur.execute("PRAGMA table_info(inactivity_logs)")
        inact_cols = [r[1] for r in cur.fetchall()]
        if "mentor_id" not in inact_cols:
            try: cur.execute("ALTER TABLE inactivity_logs ADD COLUMN mentor_id TEXT REFERENCES profiles(id)")
            except Exception: pass
        if "mentor_role" not in inact_cols:
            try: cur.execute("ALTER TABLE inactivity_logs ADD COLUMN mentor_role TEXT DEFAULT 'guide'")
            except Exception: pass
        if "inactivity_episode" not in inact_cols:
            try: cur.execute("ALTER TABLE inactivity_logs ADD COLUMN inactivity_episode TEXT")
            except Exception: pass
        if "status" not in inact_cols:
            try: cur.execute("ALTER TABLE inactivity_logs ADD COLUMN status TEXT DEFAULT 'ACTIVE'")
            except Exception: pass
        if "follow_up_channel" not in inact_cols:
            try: cur.execute("ALTER TABLE inactivity_logs ADD COLUMN follow_up_channel TEXT")
            except Exception: pass
        if "follow_up_sent_at" not in inact_cols:
            try: cur.execute("ALTER TABLE inactivity_logs ADD COLUMN follow_up_sent_at TEXT")
            except Exception: pass
        if "follow_up_notes" not in inact_cols:
            try: cur.execute("ALTER TABLE inactivity_logs ADD COLUMN follow_up_notes TEXT")
            except Exception: pass

        # Upgrade table if it contains the legacy episode-suppressing UNIQUE constraint
        cur.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='inactivity_logs'")
        tbl_row = cur.fetchone()
        if tbl_row and "UNIQUE(guide_id, aspirant_id, escalation_stage)" in tbl_row[0]:
            try:
                cur.execute("""
                CREATE TABLE IF NOT EXISTS inactivity_logs_migration (
                    id TEXT PRIMARY KEY,
                    relationship_id TEXT,
                    guide_id TEXT NOT NULL REFERENCES profiles(id),
                    aspirant_id TEXT NOT NULL REFERENCES profiles(id),
                    days_inactive INTEGER NOT NULL,
                    escalation_stage TEXT NOT NULL CHECK (escalation_stage IN ('DAY_7_REMINDER', 'DAY_10_ADMIN_ALERT', 'DAY_14_ADMIN_REVIEW')),
                    notification_sent_at TEXT,
                    created_at TEXT,
                    mentor_id TEXT REFERENCES profiles(id),
                    mentor_role TEXT DEFAULT 'guide',
                    inactivity_episode TEXT,
                    status TEXT DEFAULT 'ACTIVE',
                    follow_up_channel TEXT,
                    follow_up_sent_at TEXT,
                    follow_up_notes TEXT
                );
                """)
                cur.execute("""
                INSERT INTO inactivity_logs_migration (
                    id, relationship_id, guide_id, aspirant_id, days_inactive,
                    escalation_stage, notification_sent_at, created_at, mentor_id,
                    mentor_role, inactivity_episode, status, follow_up_channel,
                    follow_up_sent_at, follow_up_notes
                )
                SELECT
                    id, relationship_id, guide_id, aspirant_id, days_inactive,
                    escalation_stage, notification_sent_at, created_at,
                    COALESCE(mentor_id, guide_id), COALESCE(mentor_role, 'guide'),
                    inactivity_episode, COALESCE(status, 'ACTIVE'),
                    follow_up_channel, follow_up_sent_at, follow_up_notes
                FROM inactivity_logs;
                """)
                cur.execute("DROP TABLE inactivity_logs;")
                cur.execute("ALTER TABLE inactivity_logs_migration RENAME TO inactivity_logs;")
                conn.commit()
            except Exception as e:
                print(f"[LocalDB] Inactivity migration note: {e}")

        cur.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS uq_inact_ep_stage
        ON inactivity_logs(mentor_id, aspirant_id, mentor_role, inactivity_episode, escalation_stage)
        WHERE inactivity_episode IS NOT NULL;
        """)
        cur.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS uq_inact_legacy
        ON inactivity_logs(guide_id, aspirant_id, escalation_stage)
        WHERE inactivity_episode IS NULL;
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS external_contact_logs (
            id TEXT PRIMARY KEY,
            admin_id TEXT NOT NULL REFERENCES profiles(id),
            recipient_id TEXT NOT NULL REFERENCES profiles(id),
            recipient_role TEXT NOT NULL CHECK(recipient_role IN ('guide', 'sme', 'aspirant')),
            aspirant_id TEXT NOT NULL REFERENCES profiles(id),
            inactivity_record_id TEXT,
            channel TEXT NOT NULL CHECK(channel IN ('whatsapp', 'email')),
            purpose TEXT,
            status TEXT NOT NULL DEFAULT 'SENT_CONFIRMED',
            notes TEXT,
            created_at TEXT
        );
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_extcontact_rec ON external_contact_logs(recipient_id);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_extcontact_asp ON external_contact_logs(aspirant_id);")

        cur.execute("""
        CREATE TABLE IF NOT EXISTS aspirant_photos (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL UNIQUE,
            storage_bucket TEXT NOT NULL DEFAULT 'aspirant-profile-photos',
            storage_path TEXT NOT NULL,
            content_type TEXT NOT NULL DEFAULT 'image/webp',
            file_size_bytes INTEGER NOT NULL,
            width INTEGER,
            height INTEGER,
            data_blob BLOB,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_aspirant_photos_user ON aspirant_photos(user_id);")

        cur.execute("""
        CREATE TABLE IF NOT EXISTS scheme_support_reviews (
            id TEXT PRIMARY KEY,
            aspirant_id TEXT NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
            scheme_id TEXT NOT NULL REFERENCES schemes(id) ON DELETE CASCADE,
            guide_id TEXT NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
            match_score INTEGER NOT NULL,
            guide_justification TEXT NOT NULL,
            failed_criteria TEXT DEFAULT '[]',
            missing_criteria TEXT DEFAULT '[]',
            status TEXT NOT NULL DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'APPROVED', 'REJECTED')),
            admin_decision_notes TEXT,
            reviewed_by TEXT REFERENCES profiles(id),
            reviewed_at TEXT,
            created_at TEXT,
            updated_at TEXT,
            UNIQUE(aspirant_id, scheme_id, guide_id)
        );
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_ssr_status ON scheme_support_reviews(status);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_ssr_aspirant ON scheme_support_reviews(aspirant_id);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_ssr_guide ON scheme_support_reviews(guide_id);")
        conn.commit()

        # Seed legal documents if empty or update if placeholder content
        from services.legal import DEFAULT_TERMS_DOC, DEFAULT_NDA_DOC
        cur.execute("SELECT COUNT(*) FROM legal_documents")
        if cur.fetchone()[0] == 0:
            now_iso = datetime.now(timezone.utc).isoformat()
            cur.execute("""
            INSERT OR REPLACE INTO legal_documents (id, doc_type, version, title, content, content_hash, roles_covered, effective_date, is_mandatory, is_active, created_at)
            VALUES (?, 'terms_and_conditions', '1.0.0', ?, ?, ?, ?, '2026-11-01', 1, 1, ?)
            """, ("terms_v1_0", DEFAULT_TERMS_DOC["title"], DEFAULT_TERMS_DOC["content"], DEFAULT_TERMS_DOC["content_hash"], json.dumps(DEFAULT_TERMS_DOC["roles_covered"]), now_iso))
            cur.execute("""
            INSERT OR REPLACE INTO legal_documents (id, doc_type, version, title, content, content_hash, roles_covered, effective_date, is_mandatory, is_active, created_at)
            VALUES (?, 'nda_dual', '1.0.0', ?, ?, ?, ?, '2026-11-01', 1, 1, ?)
            """, ("nda_dual_v1_0", DEFAULT_NDA_DOC["title"], DEFAULT_NDA_DOC["content"], DEFAULT_NDA_DOC["content_hash"], json.dumps(DEFAULT_NDA_DOC["roles_covered"]), now_iso))
            conn.commit()
        else:
            cur.execute("SELECT content FROM legal_documents WHERE doc_type = 'terms_and_conditions' LIMIT 1")
            row = cur.fetchone()
            if row and len(row[0] or "") < 500:
                cur.execute("UPDATE legal_documents SET title = ?, content = ?, content_hash = ? WHERE doc_type = 'terms_and_conditions'",
                            (DEFAULT_TERMS_DOC["title"], DEFAULT_TERMS_DOC["content"], DEFAULT_TERMS_DOC["content_hash"]))
                cur.execute("UPDATE legal_documents SET title = ?, content = ?, content_hash = ? WHERE doc_type = 'nda_dual'",
                            (DEFAULT_NDA_DOC["title"], DEFAULT_NDA_DOC["content"], DEFAULT_NDA_DOC["content_hash"]))
                conn.commit()

        # Backfill user_roles from profiles if empty
        cur.execute("SELECT COUNT(*) FROM user_roles")
        if cur.fetchone()[0] == 0:
            cur.execute("SELECT id, role, created_at FROM profiles")
            profs = cur.fetchall()
            now_iso = datetime.now(timezone.utc).isoformat()
            for p in profs:
                p_id, p_role, p_created = p[0], p[1], p[2] or now_iso
                cur.execute("""
                INSERT OR IGNORE INTO user_roles (id, user_id, role, status, granted_at, activated_at, created_at, updated_at)
                VALUES (?, ?, ?, 'active', ?, ?, ?, ?)
                """, (f"ur_{p_id}_{p_role}", p_id, p_role, p_created, p_created, p_created, p_created))
            conn.commit()

        conn.close()

    # ── PASSWORD HELPERS ──
    @staticmethod
    def hash_pw(pw: str) -> str:
        return hashlib.sha256(pw.encode("utf-8")).hexdigest()

    def verify_password(self, email: str, password: str) -> bool:
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("SELECT password_hash FROM profiles WHERE LOWER(email) = ?", (email.lower(),))
        row = cur.fetchone()
        conn.close()
        if not row or not row["password_hash"]:
            return False
        return row["password_hash"] == self.hash_pw(password)

    def create_user_with_password(self, email: str, password: str, profile: Dict) -> Dict:
        conn = self._get_conn()
        cur = conn.cursor()
        pw_hash = self.hash_pw(password)
        now_iso = datetime.now(timezone.utc).isoformat()
        clean_email = email.lower().strip()

        cur.execute("SELECT id FROM profiles WHERE email = ?", (clean_email,))
        existing = cur.fetchone()
        user_id = existing["id"] if existing else profile["id"]
        profile["id"] = user_id

        cur.execute("""
        INSERT INTO profiles (id, email, role, full_name, phone, district, state, profile_data, is_active, password_hash, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            email = excluded.email,
            full_name = excluded.full_name,
            role = excluded.role,
            phone = excluded.phone,
            district = excluded.district,
            state = excluded.state,
            profile_data = excluded.profile_data,
            password_hash = excluded.password_hash,
            updated_at = excluded.updated_at
        """, (
            user_id, clean_email, profile.get("role", "aspirant"),
            profile.get("full_name", ""), profile.get("phone", ""),
            profile.get("district", "Madurai"), profile.get("state", "Tamil Nadu"),
            json.dumps(profile.get("profile_data", {})),
            1 if profile.get("is_active", True) else 0,
            pw_hash, now_iso, now_iso
        ))
        conn.commit()
        conn.close()
        return profile

    def update_user_password(self, user_id: str, new_password: str) -> bool:
        conn = self._get_conn()
        cur = conn.cursor()
        pw_hash = self.hash_pw(new_password)
        now_iso = datetime.now(timezone.utc).isoformat()
        cur.execute("UPDATE profiles SET password_hash = ?, updated_at = ? WHERE id = ?", (pw_hash, now_iso, user_id))
        count = cur.rowcount
        conn.commit()
        conn.close()
        return count > 0

    # ── PROFILES ──
    def get_profile_by_id(self, user_id: str) -> Optional[Dict]:
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM profiles WHERE id = ?", (user_id,))
        row = cur.fetchone()
        conn.close()
        if not row: return None
        d = dict(row)
        d["profile_data"] = json.loads(d["profile_data"]) if d.get("profile_data") else {}
        d.pop("password_hash", None)
        return d

    def get_profile_by_email(self, email: str) -> Optional[Dict]:
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM profiles WHERE LOWER(email) = ?", (email.lower(),))
        row = cur.fetchone()
        conn.close()
        if not row: return None
        d = dict(row)
        d["profile_data"] = json.loads(d["profile_data"]) if d.get("profile_data") else {}
        d.pop("password_hash", None)
        return d

    def upsert_profile(self, profile: Dict) -> Dict:
        conn = self._get_conn()
        cur = conn.cursor()
        now_iso = datetime.now(timezone.utc).isoformat()
        cur.execute("""
        INSERT INTO profiles (id, email, role, full_name, phone, district, state, profile_data, is_active, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            full_name = excluded.full_name,
            phone = excluded.phone,
            district = excluded.district,
            state = excluded.state,
            profile_data = excluded.profile_data,
            updated_at = excluded.updated_at
        """, (
            profile["id"], profile["email"].lower(), profile.get("role", "aspirant"),
            profile.get("full_name", ""), profile.get("phone", ""),
            profile.get("district", "Madurai"), profile.get("state", "Tamil Nadu"),
            json.dumps(profile.get("profile_data", {})),
            1 if profile.get("is_active", True) else 0,
            now_iso, now_iso
        ))
        conn.commit()
        conn.close()
        return profile

    def list_profiles_by_role(self, role: str) -> List[Dict]:
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT DISTINCT p.* FROM profiles p
            LEFT JOIN user_roles ur ON p.id = ur.user_id
            WHERE (p.role = ? OR (ur.role = ? AND ur.status = 'active'))
              AND p.is_active = 1
            ORDER BY p.created_at DESC
        """, (role, role))
        rows = cur.fetchall()
        conn.close()
        res = []
        for r in rows:
            d = dict(r)
            d["profile_data"] = json.loads(d["profile_data"]) if d.get("profile_data") else {}
            d.pop("password_hash", None)
            res.append(d)
        return res

    # ── RELATIONSHIPS ──
    def get_relationship(self, aspirant_id: str) -> Optional[Dict]:
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM relationships WHERE aspirant_id = ?", (aspirant_id,))
        row = cur.fetchone()
        conn.close()
        if not row:
            return None
        d = dict(row)
        if d.get("sme_ids"):
            try:
                d["sme_ids"] = json.loads(d["sme_ids"])
            except Exception:
                d["sme_ids"] = []
        else:
            d["sme_ids"] = []
        return d

    def list_all_relationships(self) -> List[Dict]:
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM relationships WHERE status = 'active'")
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        for d in rows:
            if d.get("sme_ids"):
                try: d["sme_ids"] = json.loads(d["sme_ids"])
                except Exception: d["sme_ids"] = []
            else:
                d["sme_ids"] = []
            if d.get("guide_ids"):
                try: d["guide_ids"] = json.loads(d["guide_ids"])
                except Exception: d["guide_ids"] = []
            else:
                d["guide_ids"] = []
        return rows

    def assign_guide(self, aspirant_id: str, guide_id: str, admin_id: str, notes: str = ""):
        conn = self._get_conn()
        cur = conn.cursor()
        now_iso = datetime.now(timezone.utc).isoformat()
        import uuid
        cur.execute("""
        INSERT INTO relationships (id, aspirant_id, guide_id, assigned_by, notes, status, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, 'active', ?, ?)
        ON CONFLICT(aspirant_id) DO UPDATE SET
            guide_id = excluded.guide_id,
            assigned_by = excluded.assigned_by,
            notes = excluded.notes,
            updated_at = excluded.updated_at
        """, (str(uuid.uuid4()), aspirant_id, guide_id, admin_id, notes, now_iso, now_iso))
        conn.commit()
        conn.close()

    def assign_sme(self, aspirant_id: str, sme_id: str, admin_id: str, notes: str = "", mode: str = "add"):
        conn = self._get_conn()
        cur = conn.cursor()
        now_iso = datetime.now(timezone.utc).isoformat()
        import uuid

        cur.execute("SELECT id, sme_id, sme_ids FROM relationships WHERE aspirant_id = ?", (aspirant_id,))
        row = cur.fetchone()

        sme_ids_list = []
        if row:
            existing_sme_id = row["sme_id"]
            raw_sme_ids = row["sme_ids"] if "sme_ids" in row.keys() else None
            if raw_sme_ids:
                try:
                    sme_ids_list = json.loads(raw_sme_ids)
                except Exception:
                    sme_ids_list = []
            if existing_sme_id and existing_sme_id not in sme_ids_list:
                sme_ids_list.insert(0, existing_sme_id)

        if mode == "add":
            if sme_id not in sme_ids_list:
                sme_ids_list.append(sme_id)
        else:
            sme_ids_list = [sme_id]

        new_sme_ids_json = json.dumps(sme_ids_list)

        cur.execute("""
        INSERT INTO relationships (id, aspirant_id, sme_id, sme_ids, assigned_by, notes, status, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, 'active', ?, ?)
        ON CONFLICT(aspirant_id) DO UPDATE SET
            sme_id = excluded.sme_id,
            sme_ids = excluded.sme_ids,
            assigned_by = excluded.assigned_by,
            notes = excluded.notes,
            updated_at = excluded.updated_at
        """, (str(uuid.uuid4()), aspirant_id, sme_id, new_sme_ids_json, admin_id, notes, now_iso, now_iso))
        conn.commit()
        conn.close()

    def list_aspirants_for_guide(self, guide_id: str) -> List[Dict]:
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("""
        SELECT p.*, r.notes as assignment_notes
        FROM profiles p
        JOIN relationships r ON p.id = r.aspirant_id
        WHERE (r.guide_id = ? OR r.guide_ids LIKE ?) AND p.is_active = 1
        ORDER BY r.created_at DESC
        """, (guide_id, f'%"{guide_id}"%'))
        rows = cur.fetchall()
        conn.close()
        res = []
        for r in rows:
            d = dict(r)
            d["profile_data"] = json.loads(d["profile_data"]) if d.get("profile_data") else {}
            d.pop("password_hash", None)
            res.append(d)
        return res

    def list_aspirants_for_sme(self, sme_id: str) -> List[Dict]:
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("""
        SELECT p.*, r.notes as assignment_notes
        FROM profiles p
        JOIN relationships r ON p.id = r.aspirant_id
        WHERE (r.sme_id = ? OR r.sme_ids LIKE ?) AND p.is_active = 1
        ORDER BY r.created_at DESC
        """, (sme_id, f'%"{sme_id}"%'))
        rows = cur.fetchall()
        conn.close()
        res = []
        for r in rows:
            d = dict(r)
            d["profile_data"] = json.loads(d["profile_data"]) if d.get("profile_data") else {}
            d.pop("password_hash", None)
            res.append(d)
        return res

    # ── JOURNEYS ──
    def create_initial_journey(self, aspirant_id: str, title: str):
        conn = self._get_conn()
        cur = conn.cursor()
        now_iso = datetime.now(timezone.utc).isoformat()
        import uuid
        cur.execute("""
        INSERT INTO journeys (id, aspirant_id, title, business_type, stage, start_date, status, created_at, updated_at)
        VALUES (?, ?, ?, 'Entrepreneurship', 'idea', date('now'), 'active', ?, ?)
        ON CONFLICT(aspirant_id) DO NOTHING
        """, (str(uuid.uuid4()), aspirant_id, title, now_iso, now_iso))
        conn.commit()
        conn.close()

    def get_journey(self, aspirant_id: str) -> Optional[Dict]:
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM journeys WHERE aspirant_id = ?", (aspirant_id,))
        row = cur.fetchone()
        conn.close()
        return dict(row) if row else None

    def add_journey_event(self, journey_id: str, aspirant_id: str, actor_id: str, actor_role: str, event_type: str, event_data: Dict, event_date: Optional[str] = None) -> Dict:
        conn = self._get_conn()
        cur = conn.cursor()
        import uuid
        event_id = str(uuid.uuid4())
        now_iso = datetime.now(timezone.utc).isoformat()
        if not event_date or str(event_date).strip() == now_iso[:10]:
            event_date = now_iso

        cur.execute("""
        INSERT INTO journey_events (id, journey_id, aspirant_id, actor_id, actor_role, event_type, event_data, event_date, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            event_id, journey_id, aspirant_id, actor_id, actor_role, event_type,
            json.dumps(event_data), event_date, now_iso, now_iso
        ))
        conn.commit()
        conn.close()
        return {
            "id": event_id,
            "journey_id": journey_id,
            "aspirant_id": aspirant_id,
            "actor_id": actor_id,
            "actor_role": actor_role,
            "event_type": event_type,
            "event_data": event_data,
            "title": event_data.get("title", event_type),
            "description": event_data.get("description", ""),
            "event_date": event_date
        }

    def get_journey_events(self, aspirant_id: str) -> List[Dict]:
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("""
        SELECT e.*, p.full_name as actor_name
        FROM journey_events e
        LEFT JOIN profiles p ON e.actor_id = p.id
        WHERE e.aspirant_id = ? AND e.deleted_at IS NULL
        ORDER BY e.event_date DESC, e.created_at DESC
        """, (aspirant_id,))
        rows = cur.fetchall()
        conn.close()
        res = []
        for r in rows:
            d = dict(r)
            d["event_data"] = json.loads(d["event_data"]) if d.get("event_data") else {}
            d["title"] = d["event_data"].get("title", d.get("event_type", "Event"))
            d["description"] = d["event_data"].get("description", "")
            d["included_in_roadmap"] = d["event_data"].get("included_in_roadmap", True)
            res.append(d)

        def _key(e):
            ed = str(e.get("event_date") or "").strip()
            ca = str(e.get("created_at") or "").strip()
            date_part = ed[:10] if len(ed) >= 10 else (ca[:10] if len(ca) >= 10 else "1970-01-01")
            has_ed_time = (
                ("T" in ed or " " in ed)
                and not ed.endswith("00:00:00")
                and not ed.endswith("00:00:00+00:00")
                and not ed.endswith("00:00:00Z")
                and not " 00:00:00" in ed
                and not "T00:00:00" in ed
            )
            if has_ed_time:
                time_part = ed[11:]
            else:
                time_part = ca[11:] if len(ca) > 11 else ""
            return (date_part, time_part, ca)

        res.sort(key=_key, reverse=True)
        return res

    def toggle_journey_event_inclusion(
        self,
        event_id: str,
        aspirant_id: str,
        included: bool,
        actor_id: Optional[str] = None,
        actor_role: Optional[str] = None
    ) -> Tuple[bool, Optional[str]]:
        """Toggles whether an event is included in the aspirant's journey roadmap, verifying ownership and role authorization."""
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("SELECT event_data, aspirant_id FROM journey_events WHERE id = ?", (event_id,))
        row = cur.fetchone()
        if not row:
            conn.close()
            return False, "Journey event not found."

        raw_data = row[0]
        ev_aspirant_id = row[1]

        # 1. Verify that event belongs to the requested aspirant
        if not ev_aspirant_id or str(ev_aspirant_id) != str(aspirant_id):
            conn.close()
            return False, "Unauthorized: Event does not belong to the specified aspirant."

        # 2. If actor_id is provided, verify it matches the owning aspirant
        if actor_id and str(actor_id) != str(ev_aspirant_id):
            conn.close()
            return False, "Unauthorized: You can only alter roadmap inclusion for your own journey."

        # 3. If actor_role is provided, verify it is 'aspirant'
        if actor_role and actor_role != "aspirant":
            conn.close()
            return False, f"Permission denied: {actor_role.capitalize()}s cannot alter the entrepreneur's personal roadmap inclusion."

        try:
            ev_data = json.loads(raw_data) if raw_data else {}
        except Exception:
            ev_data = {}
        ev_data["included_in_roadmap"] = bool(included)
        now_iso = datetime.now(timezone.utc).isoformat()
        cur.execute("""
        UPDATE journey_events
        SET event_data = ?, updated_at = ?
        WHERE id = ? AND aspirant_id = ?
        """, (json.dumps(ev_data), now_iso, event_id, aspirant_id))
        conn.commit()
        changes = conn.total_changes
        conn.close()
        if changes > 0:
            return True, None
        return False, "Database update produced no changes."

    def soft_delete_journey_event(self, event_id: str, deleted_by: str) -> bool:
        conn = self._get_conn()
        cur = conn.cursor()
        now_iso = datetime.now(timezone.utc).isoformat()
        cur.execute("""
        UPDATE journey_events
        SET deleted_at = ?, deleted_by = ?
        WHERE id = ?
        """, (now_iso, deleted_by, event_id))
        conn.commit()
        changes = conn.total_changes
        conn.close()
        return changes > 0

    def update_journey_event(
        self,
        event_id: str,
        new_event_data: Dict,
        new_date: Optional[str] = None,
        new_included_in_roadmap: Optional[bool] = None,
        now_iso: Optional[str] = None
    ) -> bool:
        if not now_iso:
            now_iso = datetime.now(timezone.utc).isoformat()
        conn = self._get_conn()
        cur = conn.cursor()
        data_str = json.dumps(new_event_data)
        
        sql = "UPDATE journey_events SET event_data = ?, updated_at = ?"
        params = [data_str, now_iso]
        if new_date:
            sql += ", event_date = ?"
            params.append(new_date)
        if new_included_in_roadmap is not None:
            sql += ", included_in_roadmap = ?"
            params.append(1 if new_included_in_roadmap else 0)
        sql += " WHERE id = ?"
        params.append(event_id)

        cur.execute(sql, tuple(params))
        conn.commit()
        changes = conn.total_changes
        conn.close()
        return changes > 0

    def record_journey_event_revision(
        self,
        event_id: str,
        editor_id: str,
        editor_role: str,
        previous_data: Dict,
        new_data: Dict,
        revision_number: int = 1,
        change_reason: str = ""
    ) -> bool:
        conn = self._get_conn()
        cur = conn.cursor()
        rev_id = str(uuid.uuid4())
        now_iso = datetime.now(timezone.utc).isoformat()
        cur.execute("""
            INSERT INTO journey_event_revisions (
                id, journey_event_id, editor_id, editor_role,
                previous_data, new_data, revision_number, change_reason, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            rev_id, event_id, editor_id, editor_role,
            json.dumps(previous_data), json.dumps(new_data),
            revision_number, change_reason, now_iso
        ))
        conn.commit()
        conn.close()
        return True

    # ── HELP REQUESTS ──
    def create_help_request(
        self,
        aspirant_id: str,
        subject: str,
        message: str,
        priority: str = "MEDIUM",
        assigned_guide_id: Optional[str] = None,
        category: str = "GENERAL",
        assigned_sme_id: Optional[str] = None,
        target_role: str = "guide",
        category_detail: Optional[str] = None
    ) -> Dict:
        conn = self._get_conn()
        cur = conn.cursor()
        import uuid
        req_id = str(uuid.uuid4())
        now_iso = datetime.now(timezone.utc).isoformat()
        assigned_at = now_iso if (assigned_guide_id or assigned_sme_id) else None
        cur.execute("""
        INSERT INTO help_requests (
            id, aspirant_id, subject, message, priority, status,
            assigned_guide_id, assigned_sme_id, category, target_role,
            category_detail, assigned_at, created_at, updated_at
        )
        VALUES (?, ?, ?, ?, ?, 'OPEN', ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            req_id, aspirant_id, subject, message, priority,
            assigned_guide_id, assigned_sme_id, category, target_role,
            category_detail, assigned_at, now_iso, now_iso
        ))
        conn.commit()
        conn.close()
        return {
            "id": req_id,
            "aspirant_id": aspirant_id,
            "subject": subject,
            "message": message,
            "priority": priority,
            "status": "OPEN",
            "assigned_guide_id": assigned_guide_id,
            "assigned_sme_id": assigned_sme_id,
            "category": category,
            "category_detail": category_detail,
            "target_role": target_role,
            "assigned_at": assigned_at,
            "created_at": now_iso
        }

    def list_help_requests(
        self,
        aspirant_id: Optional[str] = None,
        guide_id: Optional[str] = None,
        sme_id: Optional[str] = None
    ) -> List[Dict]:
        conn = self._get_conn()
        cur = conn.cursor()
        if aspirant_id:
            cur.execute("""
            SELECT h.*, p.full_name as aspirant_name, p.email as aspirant_email,
                   g.full_name as guide_name, s.full_name as sme_name
            FROM help_requests h
            JOIN profiles p ON h.aspirant_id = p.id
            LEFT JOIN profiles g ON h.assigned_guide_id = g.id
            LEFT JOIN profiles s ON h.assigned_sme_id = s.id
            WHERE h.aspirant_id = ? AND (h.request_type IS NULL OR h.request_type != 'mentor_admin_query')
            ORDER BY h.created_at DESC
            """, (aspirant_id,))
        elif guide_id:
            cur.execute("""
            SELECT h.*, p.full_name as aspirant_name, p.email as aspirant_email,
                   g.full_name as guide_name, s.full_name as sme_name
            FROM help_requests h
            JOIN profiles p ON h.aspirant_id = p.id
            LEFT JOIN profiles g ON h.assigned_guide_id = g.id
            LEFT JOIN profiles s ON h.assigned_sme_id = s.id
            WHERE (h.assigned_guide_id = ?
               OR (h.assigned_guide_id IS NULL AND h.aspirant_id IN (SELECT aspirant_id FROM relationships WHERE guide_id = ?)))
               AND (h.target_role IS NULL OR h.target_role != 'sme')
               AND (h.request_type IS NULL OR h.request_type != 'mentor_admin_query')
            ORDER BY h.created_at DESC
            """, (guide_id, guide_id))
        elif sme_id:
            cur.execute("""
            SELECT h.*, p.full_name as aspirant_name, p.email as aspirant_email,
                   g.full_name as guide_name, s.full_name as sme_name
            FROM help_requests h
            JOIN profiles p ON h.aspirant_id = p.id
            LEFT JOIN profiles g ON h.assigned_guide_id = g.id
            LEFT JOIN profiles s ON h.assigned_sme_id = s.id
            WHERE (h.assigned_sme_id = ?
               OR (h.assigned_sme_id IS NULL AND h.aspirant_id IN (SELECT aspirant_id FROM relationships WHERE sme_id = ?)))
               AND (h.target_role == 'sme' OR h.assigned_sme_id = ?)
               AND (h.request_type IS NULL OR h.request_type != 'mentor_admin_query')
            ORDER BY h.created_at DESC
            """, (sme_id, sme_id, sme_id))
        else:
            cur.execute("""
            SELECT h.*, p.full_name as aspirant_name, p.email as aspirant_email,
                   g.full_name as guide_name, s.full_name as sme_name
            FROM help_requests h
            JOIN profiles p ON h.aspirant_id = p.id
            LEFT JOIN profiles g ON h.assigned_guide_id = g.id
            LEFT JOIN profiles s ON h.assigned_sme_id = s.id
            WHERE (h.request_type IS NULL OR h.request_type != 'mentor_admin_query')
            ORDER BY h.created_at DESC
            """)
        rows = cur.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def update_help_request_status(self, request_id: str, status: str, admin_response: str, responded_by: str) -> bool:
        conn = self._get_conn()
        cur = conn.cursor()
        now_iso = datetime.now(timezone.utc).isoformat()
        resolved_by = responded_by if status == "RESOLVED" else None
        cur.execute("""
        UPDATE help_requests
        SET status = ?, admin_response = ?, responded_by = ?, resolved_by = COALESCE(resolved_by, ?), updated_at = ?
        WHERE id = ?
        """, (status, admin_response, responded_by, resolved_by, now_iso, request_id))
        conn.commit()
        conn.close()
        return True

    def guide_respond_help_request(self, request_id: str, guide_id: str, status: str, guide_response: str) -> bool:
        conn = self._get_conn()
        cur = conn.cursor()
        now_iso = datetime.now(timezone.utc).isoformat()
        resolved_by = guide_id if status == "RESOLVED" else None
        cur.execute("""
        UPDATE help_requests
        SET status = ?, guide_response = ?, last_handled_at = ?, last_mentor_response_at = ?,
            last_interaction_actor_id = ?, last_interaction_actor_role = 'guide',
            resolved_by = COALESCE(resolved_by, ?), updated_at = ?
        WHERE id = ? AND (assigned_guide_id = ? OR assigned_guide_id IS NULL)
        """, (status, guide_response, now_iso, now_iso, guide_id, resolved_by, now_iso, request_id, guide_id))
        conn.commit()
        changes = conn.total_changes
        conn.close()
        return changes > 0

    def sme_respond_help_request(self, request_id: str, sme_id: str, status: str, sme_response: str) -> bool:
        conn = self._get_conn()
        cur = conn.cursor()
        now_iso = datetime.now(timezone.utc).isoformat()
        resolved_by = sme_id if status == "RESOLVED" else None
        cur.execute("""
        UPDATE help_requests
        SET status = ?, sme_response = ?, last_handled_at = ?, last_mentor_response_at = ?,
            last_interaction_actor_id = ?, last_interaction_actor_role = 'sme',
            resolved_by = COALESCE(resolved_by, ?), updated_at = ?
        WHERE id = ? AND (assigned_sme_id = ? OR assigned_sme_id IS NULL)
        """, (status, sme_response, now_iso, now_iso, sme_id, resolved_by, now_iso, request_id, sme_id))
        conn.commit()
        changes = conn.total_changes
        conn.close()
        return changes > 0

    def create_mentor_consultation(
        self,
        mentor_id: str,
        mentor_role: str,
        aspirant_id: str,
        subject: str,
        message: str,
        priority: str = "MEDIUM",
        category: str = "GENERAL",
        category_detail: Optional[str] = None
    ) -> Dict:
        conn = self._get_conn()
        cur = conn.cursor()
        import uuid
        req_id = str(uuid.uuid4())
        now_iso = datetime.now(timezone.utc).isoformat()
        assigned_guide_id = mentor_id if mentor_role == "guide" else None
        assigned_sme_id = mentor_id if mentor_role == "sme" else None
        target_role = mentor_role
        cur.execute("""
        INSERT INTO help_requests (
            id, aspirant_id, subject, message, priority, status,
            assigned_guide_id, assigned_sme_id, category, target_role,
            requester_id, requester_role, request_type, category_detail,
            assigned_at, created_at, updated_at
        )
        VALUES (?, ?, ?, ?, ?, 'OPEN', ?, ?, ?, ?, ?, ?, 'mentor_initiated', ?, ?, ?, ?)
        """, (
            req_id, aspirant_id, subject, message, priority,
            assigned_guide_id, assigned_sme_id, category, target_role,
            mentor_id, mentor_role, category_detail,
            now_iso, now_iso, now_iso
        ))
        conn.commit()
        conn.close()
        return {
            "id": req_id,
            "aspirant_id": aspirant_id,
            "subject": subject,
            "message": message,
            "priority": priority,
            "status": "OPEN",
            "assigned_guide_id": assigned_guide_id,
            "assigned_sme_id": assigned_sme_id,
            "category": category,
            "target_role": target_role,
            "requester_id": mentor_id,
            "requester_role": mentor_role,
            "request_type": "mentor_initiated",
            "category_detail": category_detail,
            "created_at": now_iso
        }

    def aspirant_respond_help_request(self, request_id: str, aspirant_id: str, response: str) -> bool:
        conn = self._get_conn()
        cur = conn.cursor()
        now_iso = datetime.now(timezone.utc).isoformat()
        cur.execute("""
        UPDATE help_requests
        SET status = 'WAITING_ON_GUIDE_SME', aspirant_response = ?, aspirant_responded_at = ?,
            last_handled_at = ?, last_aspirant_response_at = ?,
            last_interaction_actor_id = ?, last_interaction_actor_role = 'aspirant', updated_at = ?
        WHERE id = ? AND aspirant_id = ?
        """, (response, now_iso, now_iso, now_iso, aspirant_id, now_iso, request_id, aspirant_id))
        conn.commit()
        changes = conn.total_changes
        conn.close()
        return changes > 0

    def create_mentor_admin_query(
        self,
        mentor_id: str,
        mentor_role: str,
        aspirant_id: str,
        subject: str,
        message: str,
        priority: str = "MEDIUM"
    ) -> Dict:
        conn = self._get_conn()
        cur = conn.cursor()
        import uuid
        req_id = str(uuid.uuid4())
        now_iso = datetime.now(timezone.utc).isoformat()
        cur.execute("""
        INSERT INTO help_requests (
            id, aspirant_id, subject, message, priority, status,
            requester_id, requester_role, request_type,
            created_at, updated_at
        )
        VALUES (?, ?, ?, ?, ?, 'PENDING_ADMIN', ?, ?, 'mentor_admin_query', ?, ?)
        """, (
            req_id, aspirant_id, subject, message, priority,
            mentor_id, mentor_role, now_iso, now_iso
        ))
        conn.commit()
        conn.close()
        return {
            "id": req_id,
            "aspirant_id": aspirant_id,
            "subject": subject,
            "message": message,
            "priority": priority,
            "status": "PENDING_ADMIN",
            "requester_id": mentor_id,
            "requester_role": mentor_role,
            "request_type": "mentor_admin_query",
            "created_at": now_iso
        }

    def list_mentor_admin_queries(
        self,
        mentor_id: Optional[str] = None,
        aspirant_id: Optional[str] = None
    ) -> List[Dict]:
        conn = self._get_conn()
        cur = conn.cursor()
        params = []
        where_clauses = ["h.request_type = 'mentor_admin_query'"]
        if mentor_id:
            where_clauses.append("h.requester_id = ?")
            params.append(mentor_id)
        if aspirant_id:
            where_clauses.append("h.aspirant_id = ?")
            params.append(aspirant_id)
        where_str = " AND ".join(where_clauses)
        cur.execute(f"""
        SELECT h.*, p.full_name as aspirant_name, p.email as aspirant_email,
               m.full_name as requester_name, m.role as requester_role_actual
        FROM help_requests h
        LEFT JOIN profiles p ON h.aspirant_id = p.id
        LEFT JOIN profiles m ON h.requester_id = m.id
        WHERE {where_str}
        ORDER BY h.created_at DESC
        """, tuple(params))
        rows = cur.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def admin_respond_to_mentor_query(
        self,
        query_id: str,
        admin_id: str,
        directive: str,
        new_status: str = "DIRECTIVE_ISSUED"
    ) -> bool:
        conn = self._get_conn()
        cur = conn.cursor()
        now_iso = datetime.now(timezone.utc).isoformat()
        cur.execute("""
        UPDATE help_requests
        SET status = ?, admin_directive = ?, directive_issued_at = ?, responded_by = ?, updated_at = ?
        WHERE id = ?
        """, (new_status, directive, now_iso, admin_id, now_iso, query_id))
        conn.commit()
        changes = conn.total_changes
        conn.close()
        return changes > 0

    # ── SCHEME SUPPORT REVIEWS (Guide -> Admin Human Review) ──
    def insert_or_update_scheme_support_review(self, record: Dict) -> bool:
        conn = self._get_conn()
        cur = conn.cursor()
        import json
        fc = json.dumps(record.get("failed_criteria", [])) if isinstance(record.get("failed_criteria"), list) else (record.get("failed_criteria") or "[]")
        mc = json.dumps(record.get("missing_criteria", [])) if isinstance(record.get("missing_criteria"), list) else (record.get("missing_criteria") or "[]")
        cur.execute("""
        INSERT INTO scheme_support_reviews (
            id, aspirant_id, scheme_id, guide_id, match_score,
            guide_justification, failed_criteria, missing_criteria, status,
            admin_decision_notes, reviewed_by, reviewed_at, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(aspirant_id, scheme_id, guide_id) DO UPDATE SET
            match_score = excluded.match_score,
            guide_justification = excluded.guide_justification,
            failed_criteria = excluded.failed_criteria,
            missing_criteria = excluded.missing_criteria,
            status = excluded.status,
            updated_at = excluded.updated_at
        """, (
            record["id"], record["aspirant_id"], record["scheme_id"], record["guide_id"],
            record.get("match_score", 0), record.get("guide_justification", ""),
            fc, mc, record.get("status", "PENDING"),
            record.get("admin_decision_notes"), record.get("reviewed_by"),
            record.get("reviewed_at"), record.get("created_at"), record.get("updated_at")
        ))
        conn.commit()
        conn.close()
        return True

    def list_scheme_support_reviews(
        self,
        status: Optional[str] = None,
        guide_id: Optional[str] = None,
        aspirant_id: Optional[str] = None
    ) -> List[Dict]:
        conn = self._get_conn()
        cur = conn.cursor()
        try:
            where_clauses = []
            params = []
            if status:
                where_clauses.append("ssr.status = ?")
                params.append(status)
            if guide_id:
                where_clauses.append("ssr.guide_id = ?")
                params.append(guide_id)
            if aspirant_id:
                where_clauses.append("ssr.aspirant_id = ?")
                params.append(aspirant_id)
            where_str = f"WHERE {' AND '.join(where_clauses)}" if where_clauses else ""
            cur.execute(f"""
            SELECT ssr.*, s.name as scheme_name, s.agency as scheme_agency, s.amount as scheme_amount,
                   p.full_name as aspirant_name, p.email as aspirant_email,
                   g.full_name as guide_name, g.email as guide_email
            FROM scheme_support_reviews ssr
            LEFT JOIN schemes s ON ssr.scheme_id = s.id
            LEFT JOIN profiles p ON ssr.aspirant_id = p.id
            LEFT JOIN profiles g ON ssr.guide_id = g.id
            {where_str}
            ORDER BY ssr.created_at DESC
            """, tuple(params))
            rows = cur.fetchall()
            results = []
            for r in rows:
                row_dict = dict(r)
                if isinstance(row_dict.get("failed_criteria"), str):
                    try: row_dict["failed_criteria"] = json.loads(row_dict["failed_criteria"])
                    except Exception: row_dict["failed_criteria"] = []
                if isinstance(row_dict.get("missing_criteria"), str):
                    try: row_dict["missing_criteria"] = json.loads(row_dict["missing_criteria"])
                    except Exception: row_dict["missing_criteria"] = []
                results.append(row_dict)
            return results
        except Exception as e:
            print(f"[LocalDB] list_scheme_support_reviews error: {e}")
            return []
        finally:
            conn.close()

    def update_scheme_support_review(
        self,
        review_id: str,
        status: str,
        admin_decision_notes: str,
        reviewed_by: str
    ) -> bool:
        conn = self._get_conn()
        cur = conn.cursor()
        now_iso = datetime.now(timezone.utc).isoformat()
        cur.execute("""
        UPDATE scheme_support_reviews
        SET status = ?, admin_decision_notes = ?, reviewed_by = ?, reviewed_at = ?, updated_at = ?
        WHERE id = ?
        """, (status, admin_decision_notes, reviewed_by, now_iso, now_iso, review_id))
        conn.commit()
        changes = conn.total_changes
        conn.close()
        return changes > 0

    # ── NOTIFICATIONS (In-App Alert System) ──
    def create_notification(
        self,
        user_id: str,
        title: str,
        message: str,
        notification_type: str,
        actor_id: Optional[str] = None,
        link: Optional[str] = None
    ) -> Dict:
        conn = self._get_conn()
        cur = conn.cursor()
        import uuid
        notif_id = str(uuid.uuid4())
        now_iso = datetime.now(timezone.utc).isoformat()
        cur.execute("""
        INSERT INTO notifications (id, user_id, actor_id, title, message, notification_type, link, is_read, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, 0, ?)
        """, (notif_id, user_id, actor_id, title, message, notification_type, link, now_iso))
        conn.commit()
        conn.close()
        return {
            "id": notif_id,
            "user_id": user_id,
            "actor_id": actor_id,
            "title": title,
            "message": message,
            "notification_type": notification_type,
            "link": link,
            "is_read": False,
            "created_at": now_iso
        }

    def list_notifications(self, user_id: str, unread_only: bool = False) -> List[Dict]:
        conn = self._get_conn()
        cur = conn.cursor()
        if unread_only:
            cur.execute("""
            SELECT * FROM notifications
            WHERE user_id = ? AND is_read = 0
            ORDER BY created_at DESC
            """, (user_id,))
        else:
            cur.execute("""
            SELECT * FROM notifications
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT 50
            """, (user_id,))
        rows = cur.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def mark_notification_as_read(self, notification_id: str, user_id: str) -> bool:
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("""
        UPDATE notifications
        SET is_read = 1
        WHERE id = ? AND user_id = ?
        """, (notification_id, user_id))
        conn.commit()
        changes = conn.total_changes
        conn.close()
        return changes > 0

    def mark_all_notifications_as_read(self, user_id: str) -> bool:
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("""
        UPDATE notifications
        SET is_read = 1
        WHERE user_id = ?
        """, (user_id,))
        conn.commit()
        changes = conn.total_changes
        conn.close()
        return changes > 0

    def get_unread_notifications_count(self, user_id: str) -> int:
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("""
        SELECT COUNT(*) FROM notifications
        WHERE user_id = ? AND is_read = 0
        """, (user_id,))
        count = cur.fetchone()[0]
        conn.close()
        return int(count)

    # ── ASSIGNMENT HISTORY ──
    def record_assignment_history(
        self,
        aspirant_id: str,
        mentor_id: str,
        mentor_role: str,
        assigned_by: str,
        action: str,
        previous_mentor_id: Optional[str] = None,
        notes: Optional[str] = None
    ) -> Dict:
        conn = self._get_conn()
        cur = conn.cursor()
        import uuid
        hist_id = str(uuid.uuid4())
        now_iso = datetime.now(timezone.utc).isoformat()
        cur.execute("""
        INSERT INTO assignment_history (
            id, aspirant_id, mentor_id, mentor_role, assigned_by,
            action, previous_mentor_id, notes, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            hist_id, aspirant_id, mentor_id, mentor_role, assigned_by,
            action, previous_mentor_id, notes, now_iso
        ))
        conn.commit()
        conn.close()
        return {
            "id": hist_id,
            "aspirant_id": aspirant_id,
            "mentor_id": mentor_id,
            "mentor_role": mentor_role,
            "assigned_by": assigned_by,
            "action": action,
            "previous_mentor_id": previous_mentor_id,
            "notes": notes,
            "created_at": now_iso
        }

    def list_assignment_history(self, aspirant_id: Optional[str] = None, mentor_id: Optional[str] = None) -> List[Dict]:
        conn = self._get_conn()
        cur = conn.cursor()
        if aspirant_id:
            cur.execute("""
            SELECT ah.*, p.full_name as aspirant_name, m.full_name as mentor_name,
                   prev.full_name as previous_mentor_name
            FROM assignment_history ah
            JOIN profiles p ON ah.aspirant_id = p.id
            JOIN profiles m ON ah.mentor_id = m.id
            LEFT JOIN profiles prev ON ah.previous_mentor_id = prev.id
            WHERE ah.aspirant_id = ?
            ORDER BY ah.created_at DESC
            """, (aspirant_id,))
        elif mentor_id:
            cur.execute("""
            SELECT ah.*, p.full_name as aspirant_name, m.full_name as mentor_name,
                   prev.full_name as previous_mentor_name
            FROM assignment_history ah
            JOIN profiles p ON ah.aspirant_id = p.id
            JOIN profiles m ON ah.mentor_id = m.id
            LEFT JOIN profiles prev ON ah.previous_mentor_id = prev.id
            WHERE ah.mentor_id = ? OR ah.previous_mentor_id = ?
            ORDER BY ah.created_at DESC
            """, (mentor_id, mentor_id))
        else:
            cur.execute("""
            SELECT ah.*, p.full_name as aspirant_name, m.full_name as mentor_name,
                   prev.full_name as previous_mentor_name
            FROM assignment_history ah
            JOIN profiles p ON ah.aspirant_id = p.id
            JOIN profiles m ON ah.mentor_id = m.id
            LEFT JOIN profiles prev ON ah.previous_mentor_id = prev.id
            ORDER BY ah.created_at DESC
            """)
        rows = cur.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def escalate_overdue_help_requests(self) -> int:
        conn = self._get_conn()
        cur = conn.cursor()
        now_iso = datetime.now(timezone.utc).isoformat()
        cur.execute("""
        UPDATE help_requests
        SET status = 'ESCALATED',
            escalated_at = ?,
            escalation_reason = 'Automatically escalated after 7 days without resolution.',
            updated_at = ?
        WHERE status IN ('OPEN', 'IN_PROGRESS')
          AND datetime(created_at) <= datetime('now', '-7 days')
        """, (now_iso, now_iso))
        count = cur.rowcount
        conn.commit()
        conn.close()
        return max(0, count)

    # ── SCHEME RELEASES (Guide Governance) ──
    def create_or_update_scheme_release(
        self,
        aspirant_id: str,
        guide_id: str,
        scheme_id: str,
        guide_recommendation: str,
        guide_note: str = "",
        eligibility_summary: str = ""
    ) -> Dict:
        conn = self._get_conn()
        cur = conn.cursor()
        import uuid
        now_iso = datetime.now(timezone.utc).isoformat()
        rel_id = str(uuid.uuid4())

        cur.execute("""
        INSERT INTO scheme_releases (
            id, aspirant_id, guide_id, scheme_id, status, guide_note,
            guide_recommendation, eligibility_summary, released_at, released_by,
            withdrawn_at, withdrawn_by, created_at, updated_at
        ) VALUES (?, ?, ?, ?, 'RELEASED', ?, ?, ?, ?, ?, NULL, NULL, ?, ?)
        ON CONFLICT(aspirant_id, scheme_id) DO UPDATE SET
            guide_id = excluded.guide_id,
            status = 'RELEASED',
            guide_note = excluded.guide_note,
            guide_recommendation = excluded.guide_recommendation,
            eligibility_summary = excluded.eligibility_summary,
            released_at = excluded.released_at,
            released_by = excluded.released_by,
            withdrawn_at = NULL,
            withdrawn_by = NULL,
            updated_at = excluded.updated_at
        """, (
            rel_id, aspirant_id, guide_id, scheme_id, guide_note,
            guide_recommendation, eligibility_summary, now_iso, guide_id,
            now_iso, now_iso
        ))
        conn.commit()

        cur.execute("SELECT * FROM scheme_releases WHERE aspirant_id = ? AND scheme_id = ?", (aspirant_id, scheme_id))
        row = cur.fetchone()
        conn.close()
        return dict(row) if row else {}

    def withdraw_scheme_release(self, aspirant_id: str, scheme_id: str, guide_id: str) -> bool:
        conn = self._get_conn()
        cur = conn.cursor()
        now_iso = datetime.now(timezone.utc).isoformat()
        cur.execute("""
        UPDATE scheme_releases
        SET status = 'WITHDRAWN',
            withdrawn_at = ?,
            withdrawn_by = ?,
            updated_at = ?
        WHERE aspirant_id = ? AND scheme_id = ?
        """, (now_iso, guide_id, now_iso, aspirant_id, scheme_id))
        conn.commit()
        changes = conn.total_changes
        conn.close()
        return changes > 0

    def get_released_schemes_for_aspirant(self, aspirant_id: str) -> List[Dict]:
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("""
        SELECT s.*, r.id as release_id, r.guide_id, r.guide_recommendation, r.guide_note,
               r.released_at, r.status as release_status, g.full_name as guide_name
        FROM scheme_releases r
        JOIN schemes s ON r.scheme_id = s.id
        LEFT JOIN profiles g ON r.guide_id = g.id
        WHERE r.aspirant_id = ? AND r.status = 'RELEASED' AND s.is_active = 1
        ORDER BY r.released_at DESC
        """, (aspirant_id,))
        rows = cur.fetchall()
        conn.close()
        res = []
        for r in rows:
            d = dict(r)
            d["sectors"] = json.loads(d["sectors"]) if d.get("sectors") else []
            d["eligibility"] = json.loads(d["eligibility"]) if d.get("eligibility") else []
            d["terms"] = json.loads(d["terms"]) if d.get("terms") else []
            # STRICTLY STRIP GUIDE-ONLY PRIVATE INTELLIGENCE FOR ASPIRANT
            d["hidden_agenda"] = []
            d["red_flags"] = []
            d["application_prompt"] = ""
            res.append(d)
        return res

    def get_scheme_releases_for_guide(self, guide_id: str, aspirant_id: Optional[str] = None) -> List[Dict]:
        conn = self._get_conn()
        cur = conn.cursor()
        if aspirant_id:
            cur.execute("""
            SELECT r.*, s.name as scheme_name, s.agency as scheme_agency, s.amount as scheme_amount,
                   p.full_name as aspirant_name, p.email as aspirant_email
            FROM scheme_releases r
            JOIN schemes s ON r.scheme_id = s.id
            JOIN profiles p ON r.aspirant_id = p.id
            WHERE r.guide_id = ? AND r.aspirant_id = ?
            ORDER BY r.updated_at DESC
            """, (guide_id, aspirant_id))
        else:
            cur.execute("""
            SELECT r.*, s.name as scheme_name, s.agency as scheme_agency, s.amount as scheme_amount,
                   p.full_name as aspirant_name, p.email as aspirant_email
            FROM scheme_releases r
            JOIN schemes s ON r.scheme_id = s.id
            JOIN profiles p ON r.aspirant_id = p.id
            WHERE r.guide_id = ?
            ORDER BY r.updated_at DESC
            """, (guide_id,))
        rows = cur.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_scheme_release(self, aspirant_id: str, scheme_id: str) -> Optional[Dict]:
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM scheme_releases WHERE aspirant_id = ? AND scheme_id = ?", (aspirant_id, scheme_id))
        row = cur.fetchone()
        conn.close()
        return dict(row) if row else None

    # ── SCHEMES ──
    def list_schemes(self, search: str = "", category: str = "ALL", stage: str = "ALL", sector: str = "ALL", active_only: bool = True) -> List[Dict]:
        conn = self._get_conn()
        cur = conn.cursor()
        query = "SELECT * FROM schemes WHERE 1=1"
        params = []

        if active_only:
            query += " AND is_active = 1"

        if search:
            query += " AND (LOWER(name) LIKE ? OR LOWER(agency) LIKE ? OR LOWER(description) LIKE ? OR LOWER(brief) LIKE ?)"
            s_param = f"%{search.lower()}%"
            params.extend([s_param, s_param, s_param, s_param])

        if category and category != "ALL":
            query += " AND category_type = ?"
            params.append(category)

        if stage and stage != "ALL":
            query += " AND stage = ?"
            params.append(stage)

        try:
            cur.execute(query + " ORDER BY COALESCE(display_order, 9999) ASC, name ASC", params)
        except Exception:
            try:
                cur.execute(query + " ORDER BY rowid ASC", params)
            except Exception:
                cur.execute(query + " ORDER BY name ASC", params)

        rows = cur.fetchall()
        conn.close()

        res = []
        for r in rows:
            d = dict(r)
            d["sectors"] = json.loads(d["sectors"]) if d.get("sectors") else []
            d["eligibility"] = json.loads(d["eligibility"]) if d.get("eligibility") else []
            d["terms"] = json.loads(d["terms"]) if d.get("terms") else []
            d["hidden_agenda"] = json.loads(d["hidden_agenda"]) if d.get("hidden_agenda") else []
            d["red_flags"] = json.loads(d["red_flags"]) if d.get("red_flags") else []
            d["is_active"] = bool(d.get("is_active", 1))
            # Sector filter in memory if specified
            if sector and sector != "ALL":
                sec_lower = sector.lower()
                if not any(sec_lower in str(s).lower() for s in d["sectors"]) and "all sectors" not in [str(s).lower() for s in d["sectors"]]:
                    continue
            res.append(d)
        return res

    def get_scheme_by_id(self, scheme_id: str) -> Optional[Dict]:
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM schemes WHERE id = ? OR source_id = ?", (scheme_id, scheme_id))
        row = cur.fetchone()
        conn.close()
        if not row: return None
        d = dict(row)
        d["sectors"] = json.loads(d["sectors"]) if d.get("sectors") else []
        d["eligibility"] = json.loads(d["eligibility"]) if d.get("eligibility") else []
        d["terms"] = json.loads(d["terms"]) if d.get("terms") else []
        d["hidden_agenda"] = json.loads(d["hidden_agenda"]) if d.get("hidden_agenda") else []
        d["red_flags"] = json.loads(d["red_flags"]) if d.get("red_flags") else []
        d["is_active"] = bool(d.get("is_active", 1))
        return d

    def upsert_scheme(self, scheme: Dict) -> bool:
        conn = self._get_conn()
        cur = conn.cursor()
        now_iso = datetime.now(timezone.utc).isoformat()
        cur.execute("""
        INSERT INTO schemes (
            id, source_id, name, agency, ministry, scheme_type, category_type,
            funding_type, stage, amount, brief, description, sectors, eligibility,
            terms, hidden_agenda, red_flags, process, timeline, success_rate,
            contact, state_scope, geography, application_url, last_verified,
            application_prompt, source_dataset, status, is_active, display_order, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            name = excluded.name,
            agency = excluded.agency,
            category_type = excluded.category_type,
            funding_type = excluded.funding_type,
            stage = excluded.stage,
            amount = excluded.amount,
            brief = excluded.brief,
            description = excluded.description,
            sectors = excluded.sectors,
            eligibility = excluded.eligibility,
            terms = excluded.terms,
            hidden_agenda = excluded.hidden_agenda,
            red_flags = excluded.red_flags,
            process = excluded.process,
            timeline = excluded.timeline,
            contact = excluded.contact,
            state_scope = excluded.state_scope,
            geography = excluded.geography,
            application_url = excluded.application_url,
            is_active = excluded.is_active,
            status = excluded.status,
            display_order = excluded.display_order,
            updated_at = excluded.updated_at
        """, (
            scheme["id"], scheme.get("source_id", scheme["id"]), scheme["name"],
            scheme.get("agency", ""), scheme.get("ministry", ""), scheme.get("scheme_type", "Grant"),
            scheme.get("category_type", "Central Govt"), scheme.get("funding_type", "Grant"),
            scheme.get("stage", "Pre-Seed / Seed"), scheme.get("amount", ""), scheme.get("brief", ""),
            scheme.get("description", ""), json.dumps(scheme.get("sectors", [])),
            json.dumps(scheme.get("eligibility", [])), json.dumps(scheme.get("terms", [])),
            json.dumps(scheme.get("hidden_agenda", [])), json.dumps(scheme.get("red_flags", [])),
            scheme.get("process", ""), scheme.get("timeline", ""), scheme.get("success_rate", ""),
            scheme.get("contact", ""), scheme.get("state_scope", "All India"), scheme.get("geography", "National"),
            scheme.get("application_url", ""), scheme.get("last_verified", "August 2026"),
            scheme.get("application_prompt", ""), scheme.get("source_dataset", "Founder AI Digital Playbook 2026"),
            scheme.get("status", "active"), 1 if scheme.get("is_active", True) else 0,
            scheme.get("display_order", 9999),
            now_iso, now_iso
        ))
        conn.commit()
        conn.close()
        return True

    def delete_scheme(self, scheme_id: str) -> bool:
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM schemes WHERE id = ? OR source_id = ?", (scheme_id, scheme_id))
        conn.commit()
        conn.close()
        return True

    # ── ACTIVITY LOG ──
    def log_activity(self, user_id: Optional[str], action: str, entity: str, entity_id: Optional[str] = None, details: Optional[Dict] = None):
        conn = self._get_conn()
        cur = conn.cursor()
        import uuid
        now_iso = datetime.now(timezone.utc).isoformat()
        cur.execute("""
        INSERT INTO activity_log (id, user_id, action, entity, entity_id, details, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (str(uuid.uuid4()), user_id, action, entity, entity_id, json.dumps(details or {}), now_iso))
        conn.commit()
        conn.close()

    # ── USER ROLES ──
    def upsert_user_role(self, r: Dict) -> bool:
        conn = self._get_conn()
        cur = conn.cursor()
        now_iso = datetime.now(timezone.utc).isoformat()
        import uuid
        role_id = r.get("id") or str(uuid.uuid4())
        cur.execute("""
        INSERT INTO user_roles (id, user_id, role, status, granted_by, granted_at, activated_at, suspended_at, revoked_at, revocation_reason, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(user_id, role) DO UPDATE SET
            status = excluded.status,
            activated_at = COALESCE(excluded.activated_at, user_roles.activated_at),
            suspended_at = excluded.suspended_at,
            revoked_at = excluded.revoked_at,
            revocation_reason = excluded.revocation_reason,
            updated_at = excluded.updated_at
        """, (
            role_id, r["user_id"], r["role"], r.get("status", "active"),
            r.get("granted_by"), r.get("granted_at", now_iso), r.get("activated_at"),
            r.get("suspended_at"), r.get("revoked_at"), r.get("revocation_reason"),
            r.get("created_at", now_iso), r.get("updated_at", now_iso)
        ))
        conn.commit()
        conn.close()
        return True

    def get_user_roles(self, user_id: str) -> List[Dict]:
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM user_roles WHERE user_id = ?", (user_id,))
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        return rows

    def update_role_status(self, user_id: str, role: str, status: str, activated_at: Optional[str] = None, suspended_at: Optional[str] = None, revoked_at: Optional[str] = None, revocation_reason: Optional[str] = None) -> bool:
        conn = self._get_conn()
        cur = conn.cursor()
        now_iso = datetime.now(timezone.utc).isoformat()
        cur.execute("""
        UPDATE user_roles
        SET status = ?, activated_at = COALESCE(?, activated_at), suspended_at = ?, revoked_at = ?, revocation_reason = ?, updated_at = ?
        WHERE user_id = ? AND role = ?
        """, (status, activated_at, suspended_at, revoked_at, revocation_reason, now_iso, user_id, role))
        conn.commit()
        conn.close()
        return True

    def list_all_user_roles(self) -> List[Dict]:
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM user_roles ORDER BY created_at DESC")
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        return rows

    # ── LEGAL DOCUMENTS & ACCEPTANCES ──
    def get_legal_document(self, doc_type_or_id: str) -> Optional[Dict]:
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM legal_documents WHERE doc_type = ? OR id = ? ORDER BY created_at DESC LIMIT 1", (doc_type_or_id, doc_type_or_id))
        row = cur.fetchone()
        conn.close()
        if not row:
            return None
        d = dict(row)
        if isinstance(d.get("roles_covered"), str):
            try: d["roles_covered"] = json.loads(d["roles_covered"])
            except Exception: pass
        return d

    def upsert_legal_document(self, d: Dict) -> bool:
        conn = self._get_conn()
        cur = conn.cursor()
        now_iso = datetime.now(timezone.utc).isoformat()
        cur.execute("""
        INSERT INTO legal_documents (id, doc_type, version, title, content, content_hash, roles_covered, effective_date, is_mandatory, is_active, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            version = excluded.version,
            title = excluded.title,
            content = excluded.content,
            content_hash = excluded.content_hash,
            roles_covered = excluded.roles_covered,
            is_active = excluded.is_active
        """, (
            d["id"], d["doc_type"], d["version"], d["title"], d["content"],
            d["content_hash"], json.dumps(d.get("roles_covered", [])),
            d.get("effective_date"), 1 if d.get("is_mandatory", True) else 0,
            1 if d.get("is_active", True) else 0, d.get("created_at", now_iso)
        ))
        conn.commit()
        conn.close()
        return True

    def record_legal_acceptance(self, a: Dict) -> bool:
        conn = self._get_conn()
        cur = conn.cursor()
        import uuid
        acc_id = a.get("id") or str(uuid.uuid4())
        now_iso = datetime.now(timezone.utc).isoformat()
        cur.execute("""
        INSERT INTO legal_acceptances (
            id, user_id, document_id, doc_type, doc_version, doc_hash, user_email_snapshot,
            typed_legal_name, typed_acceptance_phrase, checkbox_confirmed, roles_covered,
            ip_address, user_agent, status, accepted_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            acc_id, a["user_id"], a.get("document_id", "doc_default"), a["doc_type"],
            a.get("doc_version", "1.0.0"), a.get("doc_hash", ""), a["user_email_snapshot"],
            a["typed_legal_name"], a["typed_acceptance_phrase"],
            1 if a.get("checkbox_confirmed", True) else 0,
            json.dumps(a.get("roles_covered", [])), a.get("ip_address", "127.0.0.1"),
            a.get("user_agent", "LocalApp"), a.get("status", "ACCEPTED"),
            a.get("accepted_at", now_iso)
        ))
        conn.commit()
        conn.close()
        return True

    def get_legal_acceptances(self, user_id: Optional[str] = None, doc_type: Optional[str] = None) -> List[Dict]:
        conn = self._get_conn()
        cur = conn.cursor()
        sql = "SELECT * FROM legal_acceptances WHERE 1=1"
        params = []
        if user_id:
            sql += " AND user_id = ?"
            params.append(user_id)
        if doc_type:
            sql += " AND doc_type = ?"
            params.append(doc_type)
        sql += " ORDER BY accepted_at DESC"
        cur.execute(sql, tuple(params))
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        for r in rows:
            if isinstance(r.get("roles_covered"), str):
                try: r["roles_covered"] = json.loads(r["roles_covered"])
                except Exception: pass
        return rows

    def check_legal_acceptance(self, user_id: str, doc_type_or_role: str) -> bool:
        conn = self._get_conn()
        cur = conn.cursor()
        if doc_type_or_role == "terms_and_conditions":
            cur.execute("SELECT id FROM legal_acceptances WHERE user_id = ? AND doc_type = 'terms_and_conditions' LIMIT 1", (user_id,))
        else:
            cur.execute("SELECT roles_covered, doc_type FROM legal_acceptances WHERE user_id = ?", (user_id,))
            rows = cur.fetchall()
            conn.close()
            for r in rows:
                if doc_type_or_role in str(r[0]) or r[1] == "nda_dual" or r[1] == f"nda_{doc_type_or_role}":
                    return True
            return False
        row = cur.fetchone()
        conn.close()
        return bool(row)

    # ── COMPLAINTS ──
    def insert_guide_complaint(self, c: Dict) -> bool:
        conn = self._get_conn()
        cur = conn.cursor()
        import uuid
        cid = c.get("id") or str(uuid.uuid4())
        now_iso = datetime.now(timezone.utc).isoformat()
        cur.execute("""
        INSERT INTO guide_complaints (id, aspirant_id, guide_id, reason, details, status, resolution_notes, resolved_by, resolved_at, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            cid, c["aspirant_id"], c["guide_id"], c["reason"], c.get("details", ""),
            c.get("status", "PENDING"), c.get("resolution_notes"), c.get("resolved_by"),
            c.get("resolved_at"), c.get("created_at", now_iso)
        ))
        conn.commit()
        conn.close()
        return True

    def list_guide_complaints(self, aspirant_id: Optional[str] = None, status: Optional[str] = None) -> List[Dict]:
        conn = self._get_conn()
        cur = conn.cursor()
        sql = "SELECT * FROM guide_complaints WHERE 1=1"
        params = []
        if aspirant_id:
            sql += " AND aspirant_id = ?"
            params.append(aspirant_id)
        if status:
            sql += " AND status = ?"
            params.append(status)
        sql += " ORDER BY created_at DESC"
        cur.execute(sql, tuple(params))
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        return rows

    def update_guide_complaint(self, cid: str, status: str, resolution_notes: str = "", resolved_by: Optional[str] = None) -> bool:
        conn = self._get_conn()
        cur = conn.cursor()
        now_iso = datetime.now(timezone.utc).isoformat()
        cur.execute("""
        UPDATE guide_complaints
        SET status = ?, resolution_notes = ?, resolved_by = ?, resolved_at = ?
        WHERE id = ?
        """, (status, resolution_notes, resolved_by, now_iso, cid))
        conn.commit()
        conn.close()
        return True

    # ── SME CONFLICTS ──
    def insert_sme_conflict(self, c: Dict) -> bool:
        conn = self._get_conn()
        cur = conn.cursor()
        import uuid
        cid = c.get("id") or str(uuid.uuid4())
        now_iso = datetime.now(timezone.utc).isoformat()
        cur.execute("""
        INSERT INTO sme_conflict_declarations (id, sme_id, aspirant_id, has_conflict, conflict_details, status, reviewed_by, reviewed_at, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            cid, c["sme_id"], c["aspirant_id"], 1 if c.get("has_conflict") else 0,
            c.get("conflict_details", ""), c.get("status", "DECLARED"),
            c.get("reviewed_by"), c.get("reviewed_at"), c.get("created_at", now_iso)
        ))
        conn.commit()
        conn.close()
        return True

    def list_sme_conflicts(self, sme_id: Optional[str] = None, aspirant_id: Optional[str] = None) -> List[Dict]:
        conn = self._get_conn()
        cur = conn.cursor()
        sql = "SELECT * FROM sme_conflict_declarations WHERE 1=1"
        params = []
        if sme_id:
            sql += " AND sme_id = ?"
            params.append(sme_id)
        if aspirant_id:
            sql += " AND aspirant_id = ?"
            params.append(aspirant_id)
        sql += " ORDER BY created_at DESC"
        cur.execute(sql, tuple(params))
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        for r in rows:
            r["has_conflict"] = bool(r.get("has_conflict"))
        return rows

    def update_sme_conflict(self, cid: str, status: str, reviewed_by: Optional[str] = None) -> bool:
        conn = self._get_conn()
        cur = conn.cursor()
        now_iso = datetime.now(timezone.utc).isoformat()
        cur.execute("""
        UPDATE sme_conflict_declarations
        SET status = ?, reviewed_by = ?, reviewed_at = ?
        WHERE id = ?
        """, (status, reviewed_by, now_iso, cid))
        conn.commit()
        conn.close()
        return True

    # ── CASE DISCUSSIONS ──
    def insert_case_discussion(self, d: Dict) -> bool:
        conn = self._get_conn()
        cur = conn.cursor()
        import uuid
        mid = d.get("id") or str(uuid.uuid4())
        now_iso = datetime.now(timezone.utc).isoformat()
        cur.execute("""
        INSERT INTO case_discussions (id, aspirant_id, author_id, author_role, title, message, attachments, is_private_mentor_note, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            mid, d["aspirant_id"], d["author_id"], d["author_role"], d["title"],
            d["message"], json.dumps(d.get("attachments", [])),
            1 if d.get("is_private_mentor_note") else 0, d.get("created_at", now_iso)
        ))
        conn.commit()
        conn.close()
        return True

    def list_case_discussions(self, aspirant_id: str, include_private: bool = True) -> List[Dict]:
        conn = self._get_conn()
        cur = conn.cursor()
        if include_private:
            cur.execute("SELECT * FROM case_discussions WHERE aspirant_id = ? ORDER BY created_at ASC", (aspirant_id,))
        else:
            cur.execute("SELECT * FROM case_discussions WHERE aspirant_id = ? AND is_private_mentor_note = 0 ORDER BY created_at ASC", (aspirant_id,))
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        for r in rows:
            r["is_private_mentor_note"] = bool(r.get("is_private_mentor_note"))
            if isinstance(r.get("attachments"), str):
                try: r["attachments"] = json.loads(r["attachments"])
                except Exception: pass
        return rows

    # ── INACTIVITY LOGS ──
    def insert_inactivity_log(self, l: Dict) -> bool:
        conn = self._get_conn()
        cur = conn.cursor()
        import uuid
        lid = l.get("id") or str(uuid.uuid4())
        now_iso = datetime.now(timezone.utc).isoformat()
        mentor_id = l.get("mentor_id") or l.get("guide_id")
        mentor_role = l.get("mentor_role", "guide")
        episode = l.get("inactivity_episode")
        stage = l["escalation_stage"]
        asp_id = l["aspirant_id"]

        try:
            # Episode-aware deduplication check
            if episode:
                cur.execute("""
                SELECT id FROM inactivity_logs
                WHERE (mentor_id = ? OR guide_id = ?)
                  AND aspirant_id = ?
                  AND escalation_stage = ?
                  AND inactivity_episode = ?
                """, (mentor_id, mentor_id, asp_id, stage, episode))
                if cur.fetchone():
                    conn.close()
                    return False
            else:
                cur.execute("""
                SELECT id FROM inactivity_logs
                WHERE (mentor_id = ? OR guide_id = ?)
                  AND aspirant_id = ?
                  AND escalation_stage = ?
                """, (mentor_id, mentor_id, asp_id, stage))
                if cur.fetchone():
                    conn.close()
                    return False

            cur.execute("""
            INSERT INTO inactivity_logs (
                id, relationship_id, guide_id, aspirant_id, days_inactive,
                escalation_stage, notification_sent_at, created_at,
                mentor_id, mentor_role, inactivity_episode, status,
                follow_up_channel, follow_up_sent_at, follow_up_notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                lid, l.get("relationship_id"), l.get("guide_id") or mentor_id, asp_id,
                l["days_inactive"], stage, l.get("notification_sent_at", now_iso),
                l.get("created_at", now_iso), mentor_id, mentor_role, episode,
                l.get("status", "ACTIVE"), l.get("follow_up_channel"),
                l.get("follow_up_sent_at"), l.get("follow_up_notes")
            ))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            conn.close()
            return False
        except Exception as e:
            print(f"[LocalDB] insert_inactivity_log error: {e}")
            conn.close()
            return False

    def update_inactivity_log_followup(
        self,
        log_id: str,
        channel: str,
        notes: Optional[str] = None
    ) -> bool:
        conn = self._get_conn()
        cur = conn.cursor()
        now_iso = datetime.now(timezone.utc).isoformat()
        try:
            cur.execute("""
            UPDATE inactivity_logs
            SET status = 'FOLLOW_UP_INITIATED',
                follow_up_channel = ?,
                follow_up_sent_at = ?,
                follow_up_notes = ?
            WHERE id = ?
            """, (channel, now_iso, notes or "", log_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"[LocalDB] update_inactivity_log_followup error: {e}")
            conn.close()
            return False

    def list_inactivity_logs(
        self,
        guide_id: Optional[str] = None,
        aspirant_id: Optional[str] = None,
        mentor_id: Optional[str] = None,
        mentor_role: Optional[str] = None
    ) -> List[Dict]:
        conn = self._get_conn()
        cur = conn.cursor()
        sql = "SELECT * FROM inactivity_logs WHERE 1=1"
        params = []
        if mentor_id:
            sql += " AND (mentor_id = ? OR guide_id = ?)"
            params.extend([mentor_id, mentor_id])
        elif guide_id:
            sql += " AND (guide_id = ? OR mentor_id = ?)"
            params.extend([guide_id, guide_id])

        if aspirant_id:
            sql += " AND aspirant_id = ?"
            params.append(aspirant_id)
        if mentor_role:
            sql += " AND mentor_role = ?"
            params.append(mentor_role)

        sql += " ORDER BY created_at DESC"
        cur.execute(sql, tuple(params))
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        return rows

    # ── EXTERNAL CONTACT LOGS ──
    def insert_external_contact_log(self, record: Dict) -> bool:
        conn = self._get_conn()
        cur = conn.cursor()
        import uuid
        cid = record.get("id") or str(uuid.uuid4())
        now_iso = datetime.now(timezone.utc).isoformat()
        try:
            cur.execute("""
            INSERT INTO external_contact_logs (
                id, admin_id, recipient_id, recipient_role, aspirant_id,
                inactivity_record_id, channel, purpose, status, notes, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                cid, record["admin_id"], record["recipient_id"], record["recipient_role"],
                record["aspirant_id"], record.get("inactivity_record_id"),
                record["channel"], record.get("purpose", "General check-in"),
                record.get("status", "SENT_CONFIRMED"), record.get("notes"),
                record.get("created_at", now_iso)
            ))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"[LocalDB] insert_external_contact_log error: {e}")
            conn.close()
            return False

    def list_external_contact_logs(
        self,
        recipient_id: Optional[str] = None,
        aspirant_id: Optional[str] = None,
        inactivity_record_id: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict]:
        conn = self._get_conn()
        cur = conn.cursor()
        sql = "SELECT * FROM external_contact_logs WHERE 1=1"
        params = []
        if recipient_id:
            sql += " AND recipient_id = ?"
            params.append(recipient_id)
        if aspirant_id:
            sql += " AND aspirant_id = ?"
            params.append(aspirant_id)
        if inactivity_record_id:
            sql += " AND inactivity_record_id = ?"
            params.append(inactivity_record_id)
        sql += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)
        cur.execute(sql, tuple(params))
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        return rows

    # ── ASPIRANT PHOTOS ──
    def get_aspirant_photo(self, user_id: str) -> Optional[Dict]:
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM aspirant_photos WHERE user_id = ?", (user_id,))
        row = cur.fetchone()
        conn.close()
        return dict(row) if row else None

    def upsert_aspirant_photo(self, photo_data: Dict) -> bool:
        conn = self._get_conn()
        cur = conn.cursor()
        import uuid
        pid = photo_data.get("id") or str(uuid.uuid4())
        now_iso = datetime.now(timezone.utc).isoformat()
        cur.execute("""
        INSERT OR REPLACE INTO aspirant_photos (
            id, user_id, storage_bucket, storage_path, content_type,
            file_size_bytes, width, height, data_blob, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            pid, photo_data["user_id"], photo_data.get("storage_bucket", "aspirant-profile-photos"),
            photo_data["storage_path"], photo_data.get("content_type", "image/webp"),
            photo_data["file_size_bytes"], photo_data.get("width"), photo_data.get("height"),
            photo_data.get("data_blob"), photo_data.get("created_at", now_iso), now_iso
        ))
        conn.commit()
        conn.close()
        return True

    def delete_aspirant_photo(self, user_id: str) -> bool:
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM aspirant_photos WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()
        return True

# Singleton accessor
_LOCAL_DB_INSTANCE = None
def get_local_db() -> LocalDatabase:
    global _LOCAL_DB_INSTANCE
    if _LOCAL_DB_INSTANCE is None:
        _LOCAL_DB_INSTANCE = LocalDatabase()
    return _LOCAL_DB_INSTANCE
