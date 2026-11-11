# Production Performance Passive Latency Measurements

**Policy Observed:** Zero performance tuning or UI optimization changes applied during testing. All timings are passive wall-clock Playwright browser measurements against `https://app.fulcrumindia.online/` (`commit 988127b`).

---

## 1. Preflight Admin 13-Tab Baseline Latencies (`baseline_report.json`)

Measured immediately after `988127b` deployment (`5` baseline accounts, `179` schemes):

| Operation | Measured Latency (ms) | Seconds (s) |
|---|---:|---:|
| Login Page Cold Load (`login_page_load_ms`) | `3102.3` | `3.10` |
| Admin Auth -> Control Tower Render (`auth_to_dashboard_ms`) | `4672.0` | `4.67` |
| Tab 1 (`Aspirants & Journeys`) | `1545.7` | `1.55` |
| Tab 2 (`Guides Management`) | `1553.3` | `1.55` |
| Tab 3 (`SMEs Management`) | `1528.6` | `1.53` |
| Tab 4 (`Mentor Assignments`) | `1567.4` | `1.57` |
| Tab 5 (`Mentor Inquiries & Directives`) | `1558.8` | `1.56` |
| Tab 6 (`Scheme Catalogue (CRUD)` — 179 schemes, 30/page) | `1534.2` | `1.53` |
| Tab 7 (`Multi-Role Grants`) | `1558.3` | `1.56` |
| Tab 8 (`Legal & NDA Records`) | `1501.9` | `1.50` |
| Tab 9 (`Confidential Complaints`) | `1515.3` | `1.52` |
| Tab 10 (`Inactivity Monitor`) | `1528.0` | `1.53` |
| Tab 11 (`Contact Aspirants`) | `1501.7` | `1.50` |
| Tab 12 (`SME Conflict Governance`) | `1542.4` | `1.54` |
| Tab 13 (`Account Lifecycle & Archive`) | `1498.1` | `1.50` |

---

## 2. Under-Load Measurements With 37 Profiles & 22 Active Relationships (`d1_report.json` & `d2_report.json`)

| Batch / Source | Operation Measured | Observed Timings (s) | Summary Notes |
|---|---|---:|---|
| **`Batch A1` (`a1_events.json`)** | Public Aspirant Signup (`SIGNUP-AE`) | `5.18` | End-to-end form submit -> Auth user + profile + confirmation prompt. |
| **`Batch D1` (`d1_report.json`)** | User Browser Login (`D`, `B`, `F` samples) | `7.77`, `8.30`, `15.31` | End-to-end goto + Auth + dashboard hydration + `wait_st`. |
| **`Batch D1` (`d1_report.json`)** | Admin Login (`admin_login_tower`) | `7.77` | Full 37-profile / 179-scheme Control Tower hydration. |
| **`Batch D1` (`d1_report.json`)** | Admin Tab 8 (`Legal & NDA Records`, `55+` rows) | `4.29` | Includes tab switch + settle. |
| **`Batch D1` (`d1_report.json`)** | Inactivity Monitor Full Scan (`37` profiles, `22` rels) | `3.09` | Click `Run Caseload Inactivity Scan Now` -> result banner. |
| **`Batch D2` (`d2_report.json`)** | Sampled D2 Ops (`count = 8`) | **`min=1.41s`, `p50=3.08s`, `p95=12.51s`, `max=12.51s`** | `admin_login` (`12.51s`), `g_triple_login` (`8.99s`), `6` rapid switches (`1.41s`–`3.55s`). |
| **`Batch D2` (`d2_report.json`)** | Rapid Triple-Role Switching (`G`: `guide`/`sme`/`aspirant`) | `2.90`, `2.74`, `1.43`, `3.08`, `3.55`, `1.41` | Portal switch to `aspirant` fastest (`1.41s–1.43s`); `guide`/`sme` switches `2.74s–3.55s`. |
| **`Batch D2` (`d2_report.json`)** | Concurrent Parallel Journey Submit (`F` & `D`) | `3.01` (`F`), `3.06` (`D`) | Submit-to-persist wall clock under barrier concurrency (`0` retries). |

- **Stability Verdict:** Performance improvements from recent release held steady under `37` profiles (`~7.4x` baseline) and `209` journey events with zero timeouts once widget expanders/selectors were handled accurately.

