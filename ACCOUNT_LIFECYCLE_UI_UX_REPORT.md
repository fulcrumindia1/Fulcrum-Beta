# FULCRUM-BETA — ACCOUNT LIFECYCLE UI & UX DESIGN REPORT

**Author:** Fulcrum Product & UX Engineering  
**Date:** November 2026  
**Status:** IMPLEMENTED & VERIFIED  
**Target:** Sole Platform Administrator (`fulcrumindia1@gmail.com`)

---

## 1. Executive Summary & Design System Consistency

The Account Lifecycle & Archive interface is implemented as the 13th administrative tab in `views/admin.py` and `views/admin_account_lifecycle.py`:
**`🗄️ Account Lifecycle & Archive`**

### Core Design Principles:
1. **Preservation of Existing Workflows:** All existing 12 Admin tabs (Overview, Entrepreneurs, Guides, SMEs, Matching, etc.) remain untouched in order, style, and responsiveness.
2. **Visual Hierarchy & Contrast:** Built using Fulcrum's signature institutional styling: slate background (`#0F172A`), deep navy cards (`#1E293B`), rose accent badges (`#F43F5E`), amber alert cards (`#F59E0B`), and emerald confirmation states (`#10B981`).
3. **No Silent Destructive Actions:** Every major lifecycle transition (Suspension, Archival, Deletion) requires a detailed pre-action confirmation with impact analysis.
4. **Instant Visual Feedback:** Clean status pills and progress indicators immediately reflect the operational state of every user.

---

## 2. Administrative Subtab Structure

```
+-----------------------------------------------------------------------------------------+
|                        🏛️ FULCRUM PLATFORM ADMINISTRATION                               |
| [1. Overview] [2. Entrepreneurs] ... [12. SME Governance] [13. 🗄️ Account Lifecycle]   |
+-----------------------------------------------------------------------------------------+
|                                                                                         |
|  [ 🟢 Active Accounts (42) ] [ 📦 Archived (6) ] [ ⏳ Pending Deletion (2) ] [ 📜 History ] |
|                                                                                         |
+-----------------------------------------------------------------------------------------+
```

### Subtab 1: Active Accounts
- **Search & Filters:** Real-time search by user full name or email; filter by Role (All, Entrepreneur, Guide, SME, Multiple Roles) and District.
- **Card Overview:**
  - Profile Photo avatar (Founder photo or Professional photo) or initial fallback avatar.
  - Name, Email, District, Role Badges, NDA status pill.
  - Active assignment metrics (Assigned Guides, SMEs, or Mentees).
  - Open consultation ticket count.
- **Pre-Action Impact Preview:** Clicking "Review Impact & Actions" expands a detailed assessment:
  - Total active mentees affected.
  - Co-mentor promotion candidates.
  - Open consultation tickets requiring transfer or admin queuing.
  - Legal hold status.
- **Action Buttons:**
  - `[⏸️ Pause Account]` — Prompts for reason; initiates temporary suspension.
  - `[📦 Archive Account]` — Requires confirmation of handover instructions; safely archives account.
  - `[⏳ Schedule Closure]` — Sets 30-day grace review period.
  - `[🔒 Toggle Legal Hold]` — Immediately toggles institutional legal hold protection.

### Subtab 2: Archived Accounts
- **List & Metrics:** Shows all accounts currently in `ARCHIVED` status.
- **Archival Metadata:**
  - Date and time archived.
  - Archiving Administrator.
  - Institutional justification / reason.
  - Preserved historical caseload counts.
- **Safe Restoration:**
  - One-click `[♻️ Restore Account]` button.
  - Prompts for reactivation reason.
  - Confirms account will be restored under the **exact same Supabase Auth UUID**.
  - Clearly informs admin that previously revoked roles or prior caseloads will **NOT** be automatically reinstated, preventing accidental privilege restoration.

### Subtab 3: Pending Deletion (30-Day Cancellation Grace)
- **Countdown Tracker:** Prominently displays days remaining in the 30-day review period.
- **Retention & Blocker Checks:**
  - Active legal hold indicator (blocks erasure).
  - Outstanding cases or compliance investigations.
- **Actions:**
  - `[↩️ Cancel Closure Request]` — Immediately halts scheduled deletion and returns account to `ACTIVE`.
  - `[🔒 Enforce Legal Hold]` — Freezes account against purge.
  - **Notice:** Clarifies that automatic permanent purging is disabled; actual erasure requires separate signed approval.

### Subtab 4: Account Action History
- **Audit Timeline:** Chronological, tamper-evident log of all lifecycle events.
- **Table Columns:**
  - Timestamp (UTC & local format).
  - Target Account (Name & Email).
  - Action Taken (`SUSPEND`, `RESUME`, `ARCHIVE`, `RESTORE`, `SCHEDULE_DELETION`, `CANCEL_DELETION`, `LEGAL_HOLD_APPLIED`, `LEGAL_HOLD_RELEASED`).
  - Authorized Actor (Admin email or UUID).
  - State Change (`PREVIOUS_STATE -> NEW_STATE`).
  - Institutional Reason.

---

## 3. End-User Session Experiences

### A. Suspended Account Experience
When a user whose account is `TEMPORARILY_SUSPENDED` logs in or interacts with the platform:
- The page halts execution immediately.
- A high-contrast alert card is displayed:
  > **⚠️ Account Temporarily Suspended**  
  > Your account access has been temporarily suspended by Fulcrum Platform Administration.  
  > **Reason:** *[Institutional reason provided by Admin]*  
  > All your data, submissions, and historical records remain fully preserved.  
  > For questions or reinstatement reviews, please contact **fulcrumindia1@gmail.com**.  
  > `[ Sign Out ]`

### B. Archived Account Experience
When an archived user attempts to log in:
- Sign-in fails with:
  > **📦 Account Archived**  
  > This account has been archived. All historical case files and milestones are preserved. Please contact platform administration to request account restoration.

### C. Pending Deletion Grace Experience
When an account with a pending deletion logs into their dashboard:
- Full access to their workspace is maintained during the grace period.
- A prominent alert banner is displayed at the top of every page:
  > **⏳ Account Scheduled for Closure**  
  > This account is scheduled for closure review on **[Scheduled Date]** (Grace period active).  
  > If this was requested in error or you wish to maintain your account, you may cancel this request at any time:  
  > `[ Cancel Closure Request ]`
- Clicking the button cancels the pending closure in real-time, resets status to `ACTIVE`, and reloads the page.
