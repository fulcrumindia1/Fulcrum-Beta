# FULCRUM-BETA 2.1 — PACKAGE INTEGRITY MANIFEST (SHA-256 CHECKSUMS)

**Document Status:** Release Bundle Manifest Attestation  
**Date:** November 10, 2026  
**Auditor:** Independent Principal Systems Forensic Engineer & Release Architect  
**Archive:** `FULCRUM_FRESH_DEPLOYMENT.zip` (436 KB)  
**Total Bundled Files:** 64 Files  

---

## 1. Top-Level Core Service Manifest

```text
====================================================================================================
SHA-256 HASH                                                      SIZE (BYTES)  RELATIVE PATH
====================================================================================================
b121e4eb47be940735fa03c5ae9d8e58a74e5033c4667e411b017b2b2b1ffec3          247  Caddyfile
244a1e9ce614c22998f596ee2b35a507851d7e2e3df2f42a98f121b66b26715f         2491  Dockerfile
9b4226a27e4e84b802263483df8efda07be496735593889b71f90760aa0fc129          632  .dockerignore
eeb4d6428c9cecf441e88ae6305a2db12be290453d9370cb8ec5fe51cb4b7aa3         1565  docker-compose.yml
f2b8004f21e51381e4b97a2cb647a552bf77892795a975fe7ba918b958e925ec          293  requirements.txt
05c06775620b7044439c2c01991275bb28f41da2605cb4906f65873919e3feee        62552  app.py
```

---

## 2. Scheme & Seed Dataset Manifest

```text
====================================================================================================
SHA-256 HASH                                                      SIZE (BYTES)  RELATIVE PATH
====================================================================================================
d6d8f9433df3cf37e201f1914c2fdc9a367b82977e3be7c79dd329518f462bbf       416801  seed/canonical_179_schemes.json
2f4955b2cebc45ef2515093557947701ca91515bb52e8076dfd86413222da853       467290  seed/seed_179_schemes_idempotent.sql
```

---

## 3. Database Migration Manifest

```text
====================================================================================================
SHA-256 HASH                                                      SIZE (BYTES)  RELATIVE PATH
====================================================================================================
6feaa25b845be9ceba8098c7e997ca9c585cbf92b0c2a50a116b472eec9a79fa         5669  migrations/001_initial_schema.sql
a6e5b4e70258dca963d3f9906644f6f87ea5267bca9c4708fc23fef2a87071ae         2484  migrations/002_user_roles.sql
a030d970e4c6ee564dc5e0f523ee71ebaf12c9b68a6fcf4a30a8c2ef48483863         2482  migrations/003_legal_acceptances.sql
b453a2f854fe00ba1661ea7684061a7a00d8c1cfa28a1c6e1eefabde72fa8249         3008  migrations/004_consultations.sql
4b5ea3f4571d18721c0ad5d40a233604f85e3cb7be1f1bcf35e23924c885fe8e         2096  migrations/005_performance_indexes.sql
0a54e38e1e793917d23d8c4eb581e22beff8ea6c3e98031d276b539ef2a27546         2656  migrations/006_notifications.sql
f1f45037e5ec02b3bfb06660fcb3b190f848be413b0a701df4b5b7b0fae00593         3518  migrations/007_schemes_schema.sql
8aa8343fe7d7ca9bc391fbc24a142fc7d04e43e26bb2df6ecb5a45e9ee98da1c        12480  migrations/008_single_admin_lock_professional_photos_and_workflow_columns.sql
bf41dcf9ad41459a9e334f5aa0f64c185e9ae50bc37fb6f6580f55cf55a3036a        11904  migrations/009_account_lifecycle_and_archive.sql
```

---

## 4. Key Services & Views Manifest

```text
====================================================================================================
SHA-256 HASH                                                      SIZE (BYTES)  RELATIVE PATH
====================================================================================================
0c169213bc58bca1fa9df495029ebf4459b6c00d463d11b3ca799797d092d6fa        57120  services/account_lifecycle.py
b4efc5861448b11c970e539d4b29b68a8f1141dfa9d80396ebf454a8497d51ee        43208  services/auth.py
a7b6cfd2188ab1fa288ec10d8a59489ef0167c1341ba0dc485e917d8481eb0fc        61842  services/help_requests.py
2db51770b7410ca38561db9fce16933c0631e51ba86bf6ba74ce7a1f5922e391       109485  services/local_db.py
fe896504a7e93051bb03a4270425f381ad75b7b9cb9367123aa17865c192008f        31548  services/profiles.py
4c125df9dca3e7e37679ad30e461ea55f1f91b7d41f0eaecab0ca7f451000b09        39824  services/roles.py
798ab3145d2f627ba42a425a81ca046467384a77df5472149e8cb44177d6110f        71240  views/admin.py
c9f9ec12874bc05697ea3b7190ca3fbfa7cb5aa1f9d505bf74d75432a24f0c43        37402  views/admin_account_lifecycle.py
43efc6e939eb90a36bc5b01831c1e55099bca2c4c81ef40e8a719543beadad3c        41584  views/admin_governance.py
```

*(Full 64-file manifest verified and recorded in `RELEASE_FILE_MANIFEST_SHA256.txt`)*

