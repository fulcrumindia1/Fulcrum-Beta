# ARGON ACCOUNT AUTHORIZATION NEGATIVE TESTS
**Project:** FULCRUM-BETA  
**Module:** `services/account_lifecycle.py`  
**Security Domain:** Account-Level Authorization & Fail-Closed Gating  
**Test Suite:** `tests/test_argon_p0_negative_security.py`  
**Result:** 17 Passed, 0 Failed (100% Pass Rate)  

---

## 1. Architectural Mandate: Fail-Closed Authorization

The primary security flaw identified in earlier revisions was the tendency of `get_account_status()` to fall open:
1. Missing or empty user inputs resolved to active states.
2. A non-existent record in the database returned an empty dictionary that was subsequently evaluated as active.
3. Supabase network failures silently fell back to SQLite, creating potential cross-backend desynchronization.

The revised implementation strictly enforces:
$$\text{Account Status} \in \{\text{ACTIVE}\} \implies \text{Access Granted}$$
$$\text{Account Status} \in \{\text{TEMPORARILY\_SUSPENDED}, \text{ARCHIVED}, \text{PENDING\_DELETION}, \text{DENIED}\} \implies \text{Access Denied}$$
$$\text{Unknown / Error / Unreachable Backend} \implies \text{DENIED (Fail-Closed)}$$

---

## 2. Exhaustive Negative Test Matrix

The following table documents each negative test executed against `services/account_lifecycle.py`:

| Test ID | Test Function | Deliberate Failure Condition | Input Parameter | Expected Return | Actual Output | Result |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **NEG-01a** | `test_neg01` | Missing User ID (`None`) | `user_id = None` | `account_status: "DENIED"`, `is_active: False`, `exists: False` | `{"account_status": "DENIED", "is_active": False, "exists": False}` | **PASSED** |
| **NEG-01b** | `test_neg01` | Empty User ID (`""`) | `user_id = ""` | `account_status: "DENIED"`, `is_active: False`, `exists: False` | `{"account_status": "DENIED", "is_active": False, "exists": False}` | **PASSED** |
| **NEG-01c** | `test_neg01` | Whitespace User ID (`"   "`) | `user_id = "   "` | `account_status: "DENIED"`, `is_active: False`, `exists: False` | `{"account_status": "DENIED", "is_active": False, "exists": False}` | **PASSED** |
| **NEG-02** | `test_neg02` | Non-Existent Profile UUID | `user_id = "<random-uuid>"` | `account_status: "DENIED"`, `is_active: False`, `exists: False` | `{"account_status": "DENIED", "is_active": False, "exists": False, "error": "not found..."}` | **PASSED** |
| **NEG-03** | `test_neg03` | Supabase Service Down | `DATA_BACKEND=supabase`, client = `None` | `account_status: "DENIED"`, `is_active: False`, no SQLite fallback | `{"account_status": "DENIED", "is_active": False, "error": "unavailable..."}` | **PASSED** |
| **NEG-04** | `test_neg04` | PostgREST Connection Timeout | `DATA_BACKEND=supabase`, `ConnectionError` | `account_status: "DENIED"`, `is_active: False` | `{"account_status": "DENIED", "is_active": False, "error": "timeout..."}` | **PASSED** |
| **NEG-05** | `test_neg05` | Corrupted Database Status String | `account_status = "CORRUPT_UNKNOWN"` | `account_status: "DENIED"`, `is_active: False` | `{"account_status": "DENIED", "is_active": False, "error": "invalid..."}` | **PASSED** |
| **NEG-06** | `test_neg06` | Active Aspirant Spoofing Sole Admin | Active session = Aspirant, passes `SOLE_ADMIN_UUID` | `is_strict_admin() = False`, `require_sole_admin()` rejected | `(False, "Unauthorized: Actor spoofing detected...")` | **PASSED** |
| **NEG-07** | `test_neg07` | Active Guide Spoofing Sole Admin | Active session = Guide, attempts account suspension | Suspension rejected | `(False, "Unauthorized: Actor spoofing detected...")` | **PASSED** |
| **NEG-08** | `test_neg08` | Forged UUID with Admin Email | `email = SOLE_ADMIN_EMAIL`, forged UUID | Access denied | `(False, "Unauthorized: Only the Sole Platform Administrator...")` | **PASSED** |
| **NEG-09** | `test_neg09` | Forged Email with Admin UUID | `user_id = SOLE_ADMIN_UUID`, non-admin email | Access denied | `(False, "Unauthorized: Only the Sole Platform Administrator...")` | **PASSED** |
| **NEG-10** | `test_neg10` | Expired / Forged JWT Token | `token = "bad_token"`, Supabase Auth error | Access denied | `is_strict_admin() = False` | **PASSED** |
| **NEG-11** | `test_neg11` | Partial Handover Failure on Archival | `unassign_guide()` fails with lock timeout | Archival halted, profile remains `ACTIVE` | `(False, "Archival aborted: Handover incomplete...")`, status = `ACTIVE` | **PASSED** |
| **NEG-12** | `test_neg12` | Audit Log Persistence Failure | `log_account_lifecycle` throws exception | Profile status change rolled back to `ACTIVE` | `(False, "Failed to persist immutable lifecycle audit log...")` | **PASSED** |
| **NEG-13** | `test_neg13` | Legacy Inactive User Backfill | `is_active = 0`, `account_status = NULL` | Mapped to `TEMPORARILY_SUSPENDED` | `account_status: "TEMPORARILY_SUSPENDED"`, `is_active: False` | **PASSED** |
| **NEG-14** | `test_neg14` | Mutation during Pending Deletion | User in `PENDING_DELETION` raises ticket | Help request creation rejected | `(None, "Account is pending deletion review...")` | **PASSED** |
| **NEG-15** | `test_neg15` | Cancellation during Grace Period | User in `PENDING_DELETION` cancels request | Account restored to `ACTIVE` | `(True, None)`, `account_status: "ACTIVE"` | **PASSED** |
| **NEG-16** | `test_neg16` | Mentor Assignment Pending NDA | Mentor role grant = `pending_nda` | Mentor assignment rejected | `(False, "Selected mentor's GUIDE role grant is pending NDA...")` | **PASSED** |
| **NEG-17** | `test_neg17` | Aspirant Assigned as Mentor | User has no `user_roles` guide grant | Mentor assignment rejected | `(False, "Selected mentor does not hold an explicit GUIDE role grant...")` | **PASSED** |

---

## 3. Code Evidence: Implementation of Fail-Closed Resolution

```python
# Extract from services/account_lifecycle.py
def get_account_status(user_id: Optional[str]) -> Dict[str, Any]:
    if not user_id or not str(user_id).strip():
        return {
            "user_id": str(user_id or ""),
            "account_status": "DENIED",
            "is_active": False,
            "exists": False,
            "error": "Missing user ID."
        }

    clean_uid = str(user_id).strip()
    backend = get_data_backend()

    if backend == "supabase":
        admin = get_supabase_admin_client() or get_supabase_client()
        if not admin:
            # STRICT: No silent SQLite fallback in production!
            return {
                "user_id": clean_uid,
                "account_status": "DENIED",
                "is_active": False,
                "exists": False,
                "error": "Authentication backend unavailable: Supabase client is not configured."
            }
        try:
            res = admin.table("profiles").select("id, is_active, account_status, ...").eq("id", clean_uid).limit(1).execute()
            if not res.data or len(res.data) == 0:
                return {
                    "user_id": clean_uid,
                    "account_status": "DENIED",
                    "is_active": False,
                    "exists": False,
                    "error": f"Account profile record not found for user ID '{clean_uid}'."
                }
            status_dict = res.data[0]
        except Exception as e:
            return {
                "user_id": clean_uid,
                "account_status": "DENIED",
                "is_active": False,
                "exists": False,
                "error": f"Supabase backend communication failure: {e}"
            }
    else:
        db = get_local_db()
        p = db.get_profile_by_id(clean_uid)
        if not p:
            return {
                "user_id": clean_uid,
                "account_status": "DENIED",
                "is_active": False,
                "exists": False,
                "error": f"Account profile record not found in local database for user ID '{clean_uid}'."
            }
        status_dict = p

    # Lifecycle evaluation
    raw_status = str(status_dict.get("account_status") or "").strip().upper()
    if raw_status in VALID_ACCOUNT_STATUSES:
        final_status = raw_status
    elif not raw_status and "is_active" in status_dict:
        final_status = "ACTIVE" if bool(status_dict.get("is_active")) else "TEMPORARILY_SUSPENDED"
    else:
        # Corrupt or unknown -> FAIL-CLOSED DENIED
        return {
            "user_id": clean_uid,
            "account_status": "DENIED",
            "is_active": False,
            "exists": True,
            "error": f"Unknown or invalid account lifecycle state: '{raw_status}'."
        }

    is_act_flag = bool(status_dict.get("is_active", True))
    effective_is_active = (final_status == "ACTIVE") and is_act_flag

    return {
        "user_id": clean_uid,
        "account_status": final_status,
        "is_active": effective_is_active,
        "exists": True,
        ...
    }
```

---

## 4. Verification Conclusion
All failure paths in account status retrieval have been verified to fail closed. The system denies access by default upon any database error, missing record, corrupt status, or unauthenticated request.

