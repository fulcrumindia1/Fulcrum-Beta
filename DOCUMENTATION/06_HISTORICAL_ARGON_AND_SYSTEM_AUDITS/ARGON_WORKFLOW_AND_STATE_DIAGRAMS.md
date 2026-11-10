# FULCRUM-BETA → AGY ARGON: WORKFLOW & STATE-TRANSITION DIAGRAMS
**Deliverable 7 of 10 | Mode: Read-Only Architectural & State Modeling**

---

## 1. Workflow A: Aspirant Onboarding to First Value (`flowchart TD`)

```mermaid
flowchart TD
    Signup["1. Aspirant Signs Up\n(views/login.py -> signup_aspirant)"] --> TermsGate{"2. Accepted Platform\nTerms v1.0.0?"}
    TermsGate -- "No" --> BlockTerms["Render Unskippable T&C Gate\n(views/legal_ui.py:L19)"]
    BlockTerms -->|"Types 'I ACCEPT' + Checkbox"| RecordTerms["Save SHA-256 Acceptance\n(legal_acceptances)"]
    RecordTerms --> PortalEntry
    TermsGate -- "Yes" --> PortalEntry["3. Enter Aspirant Portal\n(views/aspirant.py)"]

    PortalEntry --> ProfileEdit["4. Complete 4-Section Venture Dossier\n+ Strategic Assistance Need + Photo"]
    ProfileEdit -->|"save_aspirant_photo()"| PhotoBug["⚠️ BUG: views/aspirant.py:L209\ncalls get_aspirant_photo(uid)\nwithout viewer_id -> Returns None!"]
    ProfileEdit -->|"update_aspirant_profile()"| CalcScore["Calculate completion_pct (0-100%)\nUpdate journeys + Log 'profile_updated'"]

    CalcScore --> Gap1["⚠️ MISSING LOGIC:\nNo notification sent to Admin (if unassigned)\nor Guide (when profile reaches >=70%)"]
    CalcScore --> AdminAssign["5. Admin Assigns Primary Guide & SMEs\n(views/admin.py Tab 3)"]
    AdminAssign --> GuideEval["6. Guide Evaluates 179 Schemes\n(views/guide.py Subtab 2)"]
    GuideEval --> Release["7. Guide Releases Curated Schemes\n(scheme_releases.status = 'RELEASED')"]
    Release --> FirstValue["8. Aspirant Views Released Schemes\n& Initiates Consultations"]
```

---

## 2. Workflow B: Scheme Matching, Gatekeeper Review & Release State Machine (`stateDiagram-v2`)

```mermaid
stateDiagram-v2
    [*] --> CatalogueActive: "Admin Seeds / Upserts Scheme (179 Active)"
    CatalogueActive --> CatalogueArchived: "Admin Clicks Archive (toggle_archive_scheme)"
    CatalogueArchived --> CatalogueActive: "Admin Clicks Activate"

    CatalogueActive --> MatchedEligible: "match_schemes_for_aspirant() Score >= 60% & Not Disqualified"
    CatalogueActive --> MatchedDisqualified: "match_schemes_for_aspirant() Fails Mandatory Statutory Gate"

    MatchedDisqualified --> SupportReviewPending: "Guide Submits Scheme Support Review (PENDING)"
    SupportReviewPending --> SupportReviewApproved: "Admin Approves Review (APPROVED)"
    SupportReviewPending --> SupportReviewRejected: "Admin Rejects Review (REJECTED)"

    MatchedEligible --> ReleasedToAspirant: "Primary Guide Clicks Release (status = RELEASED)"
    MatchedDisqualified --> ReleasedToAspirant: "Primary Guide Checks Override Box & Releases"
    SupportReviewApproved --> ReleasedToAspirant: "Guide Releases Scheme (⚠️ Still requires manual override checkbox)"

    ReleasedToAspirant --> WithdrawnByGuide: "Guide Clicks Withdraw (status = WITHDRAWN)"
    WithdrawnByGuide --> ReleasedToAspirant: "Guide Re-Releases Scheme"

    state "⚠️ MISSING POST-RELEASE STATES" as MissingPostRelease {
        PreparingDPR: "PREPARING_APPLICATION (Missing)"
        SubmittedPortal: "APPLIED_ON_NODAL_PORTAL (Missing)"
        Sanctioned: "SANCTIONED / FUNDED (Missing)"
        RejectedByAgency: "REJECTED_BY_AGENCY (Missing)"
    }
    ReleasedToAspirant --> MissingPostRelease: "Currently Dead-Ends at RELEASED"
```

---

## 3. Workflow C: Consultation & Ticket State Machine (`stateDiagram-v2`)

This diagram highlights the **critical dead-end bug** in [`views/sme.py:L475`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/sme.py#L475) and [`L623`](file:///c:/Users/hp/Desktop/Fulcrum-Alpha/fulcrum-cluster-b/views/sme.py#L623) when an Aspirant replies (`WAITING_ON_GUIDE_SME`):

```mermaid
stateDiagram-v2
    [*] --> OPEN: "Aspirant Creates Request (create_request)\nOR Mentor Issues Directive (create_mentor_consultation)"

    OPEN --> IN_PROGRESS: "Guide or SME Replies (IN_PROGRESS)"
    OPEN --> WAITING_ON_ASPIRANT: "Guide Replies (WAITING_ON_ASPIRANT)\n⚠️ SME lacks this option in views/sme.py"
    OPEN --> RESOLVED: "Guide or SME Resolves (RESOLVED)"

    IN_PROGRESS --> WAITING_ON_ASPIRANT: "Guide Requests Info from Aspirant"
    IN_PROGRESS --> WAITING_ON_GUIDE_SME: "Aspirant Replies (aspirant_respond_request)"
    WAITING_ON_ASPIRANT --> WAITING_ON_GUIDE_SME: "Aspirant Replies (aspirant_respond_request)"
    OPEN --> WAITING_ON_GUIDE_SME: "Aspirant Replies to Mentor Directive"

    WAITING_ON_GUIDE_SME --> IN_PROGRESS: "Guide Replies (views/guide.py allows t_status != RESOLVED)"
    WAITING_ON_GUIDE_SME --> RESOLVED: "Guide Resolves Ticket"
    WAITING_ON_GUIDE_SME --> SME_DEAD_END: "⚠️ BUG in views/sme.py:L475 & L623!\nSME form only renders for OPEN / IN_PROGRESS / REPLIED.\nSME is LOCKED OUT of replying to WAITING_ON_GUIDE_SME!"

    RESOLVED --> [*]
```

---

## 4. Workflow D: Mentor Assignment, Co-Guides & Replacement Sequence (`sequenceDiagram`)

```mermaid
sequenceDiagram
    autonumber
    actor Admin as "Single Admin (Fulcrum Support)"
    participant RelSvc as "services/relationships.py"
    participant DB as "Supabase (relationships / assignment_history / help_requests)"
    actor OldGuide as "Outgoing Guide A"
    actor NewGuide as "Incoming Guide B"
    actor Aspirant as "Entrepreneur (Aspirant)"

    Admin->>RelSvc: assign_guide(aspirant_id, guide_b_id, mode="replace" or "add")
    RelSvc->>RelSvc: Verify guide_b_id != aspirant_id & user_has_active_role("guide")
    RelSvc->>DB: UPSERT relationships (guide_id, guide_ids)
    RelSvc->>DB: INSERT assignment_history (action="REPLACED" or "ASSIGNED")
    alt mode == "replace"
        RelSvc->>DB: UPDATE help_requests SET assigned_guide_id = guide_b_id WHERE status IN ('OPEN', 'IN_PROGRESS')
        Note over RelSvc,DB: ⚠️ GAP: Tickets in WAITING_ON_ASPIRANT or WAITING_ON_GUIDE_SME are NOT transferred!
        RelSvc->>OldGuide: Notification: "Mentee Reassigned"
        RelSvc->>NewGuide: Notification: "New Mentee Assigned (Reassignment)"
        RelSvc->>Aspirant: Notification: "Dedicated Guide Updated"
    else mode == "add" (Co-Guide)
        RelSvc->>NewGuide: Notification: "New Mentee Assigned"
        RelSvc->>Aspirant: Notification: "Dedicated Guide Assigned"
        Note over NewGuide,Aspirant: ⚠️ GAP: Co-Guide is hidden in Guidance Team UI (aspirant.py:L642) & blocked from releasing schemes (schemes.py:L390)!
    end
```

---

## 5. Workflow E: Multi-Role Grant, NDA Execution, Suspension & Revocation (`stateDiagram-v2`)

```mermaid
stateDiagram-v2
    [*] --> BaseAspirant: "User Registers (profiles.role = 'aspirant')"
    [*] --> StandaloneMentor: "Admin Provisions Guide/SME in Tab 1 (profiles.role = 'guide'/'sme')"

    BaseAspirant --> PendingNDA: "Admin Grants Secondary Guide or SME Role (status = 'pending_nda')"
    StandaloneMentor --> PendingNDA: "Initial Role Grant Created (status = 'pending_nda')"

    PendingNDA --> Cancelled: "Admin Cancels Pending Grant (cancel_grant)"
    PendingNDA --> ActiveRole: "User Switches to Role & Signs NDA (record_legal_acceptance -> activate_role)"

    ActiveRole --> SuspendedRole: "Admin Clicks Suspend (suspend_role)\n⚠️ Blocked in UI for StandaloneMentor due to admin_governance.py:L138!"
    SuspendedRole --> ActiveRole: "Admin Clicks Reinstate (reinstate_role)"

    ActiveRole --> RevokedRole: "Admin Clicks Revoke (revoke_role)\nAuto-unassigns active caseload via unassign_guide / unassign_sme"
    SuspendedRole --> RevokedRole: "Admin Clicks Revoke (revoke_role)"
```

---

## 6. Workflow F: Two-Tier Escalation, Inactivity & External Contact (`flowchart TD`)

```mermaid
flowchart TD
    subgraph CaseloadScanner["1. Independent Mentor Inactivity Scanner (services/inactivity.py)"]
        Scan["check_and_process_caseload_inactivity()"] --> Clock["Compute get_last_interaction_date(mentor_id, aspirant_id, role)\nIgnores Aspirant replies; starts from effective assignment date"]
        Clock --> Day7{"Days >= 7?"}
        Day7 -- "7-9 Days" --> Alert7["Stage: DAY_7_REMINDER\nIn-App Notification to Guide/SME"]
        Day7 -- "10-13 Days" --> Alert10["Stage: DAY_10_ADMIN_ALERT\nIn-App Notification to Single Admin"]
        Day7 -- ">= 14 Days" --> Alert14["Stage: DAY_14_ADMIN_REVIEW\nCritical Escalation to Single Admin"]
    end

    subgraph AdminFollowup["2. Manual External Outreach (services/external_contact.py)"]
        Alert10 & Alert14 --> AdminTab6["Admin Tab 6: Inactivity Monitor"]
        AdminTab6 --> DraftLink["Generate wa.me WhatsApp or Gmail Compose URL\n(Signed as 'Fulcrum Support')"]
        DraftLink --> ConfirmSent["Admin Clicks 'Mark Follow-up Sent'\n(record_external_contact -> status='FOLLOW_UP_INITIATED')"]
        ConfirmSent --> MentorActs["Mentor Logs Journey Entry / Replies to Ticket / Releases Scheme"]
        MentorActs --> LiveStatus["compute_alert_live_status() -> 'Mentor Active Again' 🟢"]
    end
```
