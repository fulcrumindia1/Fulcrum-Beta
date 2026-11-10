# 01 — VM INFRASTRUCTURE INVENTORY (`10.44.155.57`)
**Phase A Read-Only Audit Deliverable | Target: `pravin@10.44.155.57` (`pravin-server`)**

> [!IMPORTANT]
> **SSH Authentication Security Note:**  
> Passwordless Ed25519 SSH key authentication (`~/.ssh/id_ed25519` / `~/.ssh/pithros_sim_ed25519`) is **already configured and verified** between this workstation and `pravin@10.44.155.57`. No password was stored in shell history, scripts, or logs. **Owner Action Recommended:** Rotate the temporary SSH password on the VM (`passwd`) and disable `PasswordAuthentication` in `/etc/ssh/sshd_config` once key access is confirmed.

---

## 1. Executive Answer: Critical Infrastructure Question
- **Is `10.44.155.57` the live Hostinger KVM 2 production VPS or a simulation VM?**  
  It is a **local Oracle VirtualBox / KVM simulation VM (`pravin-server`)** provisioned to mirror the exact **Hostinger KVM 2 CPU and RAM envelope** (`2 vCPUs`, `7.8 GiB RAM`), with a `60 GB` virtual disk (`31 GB` free) instead of Hostinger KVM 2's `100 GB` NVMe disk.
- **Is Fulcrum-Beta already deployed on `10.44.155.57`?**  
  **No.** Fulcrum is not yet deployed on this VM.
- **Does the VM host other applications?**  
  **Yes.** It currently runs 5 Docker containers for an unrelated staging stack (`pairdo-staging-*` on ports `8000`, `8080`, `5432`, `6379`) consuming `~411.5 MiB` of active RAM. Ports `80`, `443`, and `8501` are unoccupied.

---

## 2. Measured Hardware, OS & Storage Specifications

| Component | Measured Value on `10.44.155.57` | Hostinger KVM 2 Equivalent Spec | Status |
| :--- | :--- | :--- | :---: |
| **Hostname** | `pravin-server` | VPS Node | Healthy |
| **Hypervisor / Chassis** | Oracle VirtualBox (`KVM` full virtualization) | Hostinger KVM Hypervisor | Matches CPU/RAM |
| **Operating System** | Ubuntu `24.04.5 LTS` (`x86_64`) | Ubuntu 24.04 LTS | Healthy |
| **Kernel Version** | `Linux 6.8.0-146-generic #146-Ubuntu SMP PREEMPT_DYNAMIC` | Linux 6.8.x | Healthy |
| **CPU Model** | `Intel(R) Core(TM) i3-3240 CPU @ 3.40GHz` | AMD EPYC / Intel Xeon vCPU | Healthy |
| **Available vCPUs** | **`2 vCPUs`** (`2 cores, 1 thread/core, NUMA node0: 0,1`) | **`2 vCPUs`** | Exact Match |
| **CPU Load Average** | `0.07` (1m), `0.26` (5m), `0.32` (15m) | — | Idle (`~3.5%` load) |
| **Physical / Virtual RAM** | **`7.8 GiB`** (`1.1 GiB` used, `4.2 GiB` free, `2.8 GiB` cache) | **`8.0 GB`** | Exact Match |
| **Available RAM** | **`6.7 GiB` available** without swapping | `~6.8 GB` available | Healthy |
| **Swap Space** | **`4.0 GiB`** (`/swap.img`, **`0 B` used**) | `2–4 GB` swap | Healthy (`0%` used) |
| **Root Filesystem (`/`)** | `/dev/mapper/ubuntu--vg-ubuntu--lv` (`ext4`, LVM on `60 GB` `sda`) | `100 GB` NVMe | Healthy |
| **Disk Capacity & Free Space** | **`57 GB` total**, `25 GB` used, **`31 GB` available (`45%` used)** | `100 GB` | Sufficient (`31 GB` free) |
| **Inode Utilization (`/`)** | `554,727` used / `3,801,088` total (**`15%` used**) | — | Healthy |
| **Docker Engine** | `29.9.3` (API `1.56`, containerd `v2.4.2`, runc `1.5.2`) | Docker CE | Healthy |
| **Docker Compose** | `v5.7.0` | Docker Compose v2+ | Healthy |

---

## 3. Existing Running Containers & Port Bindings on `10.44.155.57`

| Container Name | Image | Status | CPU % | Active RAM / Hard Limit | Host Port Mapping |
| :--- | :--- | :--- | :---: | :---: | :--- |
| `pairdo-staging-frontend-1` | `pairdo-staging-frontend` | Up (35m) | `0.00%` | `9.76 MiB / 256 MiB` | `0.0.0.0:8080 -> 80/tcp` |
| `pairdo-staging-backend-1` | `pairdo-backend:staging` | Up (healthy) | `0.29%` | `281.10 MiB / 1.465 GiB` | `0.0.0.0:8000 -> 8000/tcp` |
| `pairdo-staging-db-1` | `postgres:15-alpine` | Up (healthy) | `0.00%` | `54.02 MiB / 1.953 GiB` | `0.0.0.0:5432 -> 5432/tcp` |
| `pairdo-staging-redis-1` | `redis:7-alpine` | Up (healthy) | `0.63%` | `3.48 MiB / 256 MiB` | `127.0.0.1:6379 -> 6379/tcp` |
| `pairdo-staging-worker-dna-1` | `pairdo-backend:staging` | Up (35m) | `0.19%` | `63.18 MiB / 1000 MiB` | Internal `8000/tcp` |
| **Total Co-Hosted Usage** | — | **5 Containers** | **`1.11%`** | **`411.5 MiB` active** | Ports `8000, 8080, 5432, 6379` |

### Listening Host Ports (`ss -lntp`)
- **Occupied Ports:** `22` (SSH), `53` (systemd-resolved / libvirt dnsmasq), `2377` & `7946` (Docker Swarm), `5432` (Pairdo Postgres), `6379` (Pairdo Redis), `8000` (Pairdo Backend), `8080` (Pairdo Frontend), `48692` (Tailscale).
- **Available Ports for Isolated Fulcrum Staging:** `8501` (Streamlit direct), `8443` / `8081` (Staging Caddy HTTP/HTTPS), or `80` / `443`.
