# FULCRUM-INDIA: AGY ARGON — GATE 0 CHANGED FILES AND DIFF INVENTORY

**Branch**: `security/phase0-containment`  
**Base Commit**: `a53d395` (from `origin/main`)  
**Scope**: Development & Staging Security Hardening Only. Zero live production changes.

---

## 1. File Modification Summary

| File Path | Action | Lines Changed | Primary Security Purpose |
| :--- | :---: | :---: | :--- |
| `.gitignore` | Modified | +7 | Block archives (`*.tar.gz`, `*.tgz`, `*.zip`, `*.dump`) & `.env*` from git tracking. |
| `fulcrum_deploy.tar.gz` | Deleted | -172 KB | Removed compromised historical archive containing secrets. |
| `services/auth.py` | Modified | +38 / -65 | Eliminated unauthenticated Admin API password bypass; enforced token & $\ge 8$ chars. |
| `views/login.py` | Modified | +12 / -7 | Gated recovery form to verified email tokens; removed unauthenticated form open button. |
| `services/collaboration.py` | Modified | +90 / -9 | Gated private mentor notes by verified assignment & NDA; eliminated role parameter tampering. |
| `services/external_contact.py` | Modified | +1 / -1 | Purged references to legacy `district_admin` and `operational_admin`. |
| `services/aspirant_photos.py` | Modified | +35 / -43 | Fail-closed photo retrieval (SEC-05); eliminated false success & silent fallback in Supabase mode. |
| `services/roles.py` | Modified | +42 / -24 | Fail-closed cloud writes in Supabase mode; excluded Platform Admin from mentor dropdowns. |
| `services/legal.py` | Modified | +11 / -11 | Fail-closed cloud writes in Supabase mode; prevented silent SQLite fallback. |
| `services/profiles.py` | Modified | +8 / -4 | Enforced owner authorization on profile updates; prevented unauthorized cross-user modifications. |
| `views/admin.py` | Modified | +8 / -4 | Replaced static default passwords with cryptographically secure `secrets.token_urlsafe(12)`. |
| `tests/test_single_admin_master_e2e.py` | Modified | +4 / -4 | Updated photo lifecycle test calls to pass owner `viewer_id`. |
| `tests/test_argon_security_remediation.py` | Added | +245 | Automated security test suite covering SEC-01 through SEC-16. |

---

## 2. Key Code Diff Highlights

### A. `services/auth.py` (CWE-640 Remediation)
```diff
-    # 2. Attempt Admin Client update by resolving registered email to user ID
-    if not updated and admin_client and clean_email:
-        prof_res = admin_client.table("profiles").select("id").ilike("email", clean_email).execute()
-        user_id = prof_res.data[0].get("id")
-        admin_client.auth.admin.update_user_by_id(user_id, {"password": new_password})
+    # Supabase Mode: STRICTLY REQUIRE VERIFIED RECOVERY SESSION
+    token = access_token or st.session_state.get("sb_access_token")
+    if not token or not client:
+        return False, "Invalid or missing recovery credentials. Please use the secure reset link."
+
+    # Platform Admin can NEVER be reset via public self-service flow
+    if clean_email == "fulcrumindia1@gmail.com":
+        return False, "Security Notice: Platform Administrator credentials cannot be reset through self-service recovery."
```

### B. `services/collaboration.py` (Private Notes Parameter Tampering Defense)
```diff
-    if requesting_role == "aspirant":
-        q = q.eq("is_private_mentor_note", False)
+    # Verify authenticated caller assignment and NDA status
+    can_view_private = False
+    if effective_viewer:
+        if is_admin:
+            can_view_private = (requesting_role != "aspirant")
+        elif str(effective_viewer) == str(aspirant_id):
+            can_view_private = False
+        elif is_assigned_mentor_with_nda:
+            can_view_private = (requesting_role != "aspirant")
+    if not can_view_private:
+        records = [r for r in records if not r.get("is_private_mentor_note")]
```

### C. `services/aspirant_photos.py` (Fail-Closed Photo Operations)
```diff
-    if hasattr(upload_res, "error") and upload_res.error:
-        # Supabase upload failed but local DB already has the photo — return success
-        return True, None
+    if hasattr(upload_res, "error") and upload_res.error:
+        return False, f"Failed to persist profile photo to cloud storage: {upload_res.error}"
```
