# FULCRUM-BETA 2.1 — ROLLBACK CONTINGENCY PLAN & SLA GUARANTEES

**Document Status:** Operational Disaster Recovery Protocol  
**Date:** November 10, 2026  
**Auditor:** Independent Principal Systems Forensic Engineer & Release Architect  
**Rollback Time Objective (RTO):** < 45 seconds  
**Recovery Point Objective (RPO):** Zero data loss (Supabase cloud transactions immutable)  

---

## 1. Rollback Triggers

An immediate automated or manual rollback is mandated if any of the following conditions occur post-deployment:
1. Container fails health check (`/_stcore/health`) for > 60 seconds post-launch.
2. Production logs report any `SyntaxError`, `UnboundLocalError`, or `NameError`.
3. Memory consumption exceeds 4.5 GB (> 90% of the 5120M container limit).
4. Sole Admin (`fulcrumindia1@gmail.com`) is unable to authenticate or access the Admin portal.

---

## 2. One-Command Instant Rollback Protocol

If a rollback is required, execute the following single command in the VPS SSH terminal:

```bash
cd /opt/fulcrum && bash /opt/fulcrum/scripts/SAFE_FULCRUM_ONLY_ROLLBACK.sh
```

---

## 3. What the Rollback Script Does

1. **Reverts to Tagged Image:** Instantly points `docker-compose` back to `fulcrum-app:pre_deploy_backup`.
2. **Restarts Container:** Runs `docker compose up -d --no-deps --force-recreate fulcrum`.
3. **Restores Pre-Deploy State:** Restores configuration files from `/opt/fulcrum_backups/` if modified.
4. **Validates Health:** Polls the health endpoint until service availability is restored.
5. **Preserves Caddy:** Leaves reverse proxy and Let's Encrypt SSL certificates intact throughout.

---

## 4. Manual Rollback Fallback Procedure

If the automated script cannot be reached, run:

```bash
cd /opt/fulcrum
docker tag fulcrum-app:pre_deploy_backup fulcrum-fulcrum
docker compose up -d --no-deps --force-recreate fulcrum
```

