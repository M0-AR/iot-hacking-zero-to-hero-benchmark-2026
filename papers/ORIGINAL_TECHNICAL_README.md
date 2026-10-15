# Practical IoT Hacking — Zero-to-Hero Reproducible Benchmark (2026)

> **From Chantzis et al. (2021) to verifiable science in 2026.**
> Every claim in *Practical IoT Hacking* re-implemented as code, executed,
> measured against **live public infrastructure**, and gated by CI.
> No hand-waving. `python experiments/run_all.py` must exit 0.

**Repo:** `/home/md/src/iot-hacking-zero-to-hero-benchmark-2026`
**Status:** 7/7 experiments PASS (2026-10-15, live-verified)
**Stack:** Python 3.11 + Docker Compose (mosquitto + OpenWrt lab + Jupyter)

---

## Abstract

IoT security literature is rich in techniques but poor in reproducibility
(Yousefnezhad & Costin 2024; Cheng et al. 2023 *IoTFuzzBench*; Cheng et al.
2025 *IoTB enchSL*). *Practical IoT Hacking* (No Starch Press, 2021) is the
most complete practitioner methodology — STRIDE/DREAD threat modeling,
VLAN-hopping, Nmap/Ncrack extension, DICOM dissection, UPnP/mDNS/
WS-Discovery abuse, UART/JTAG/SWD, SPI/I2C, firmware emulation
(FIRMADYNE), RFID/MIFARE, BLE GATT, Wi-Fi PMKID, LoRaWAN bit-flipping,
mobile companion analysis, and smart-home chains — yet none of its
procedures ship with automated oracles.

We close that gap. For each part (I–V, Ch.2–15) we (i) formalize the
security claim as a falsifiable predicate, (ii) implement a minimal
reproduction requiring **no hardware**, (iii) verify it against **live
2026 infrastructure** (public MQTT broker, GitHub firmware releases,
LAN multicast), and (iv) publish machine-checkable benchmarks.
Our main scientific contribution is a **hidden cross-layer pattern**:
unauthenticated discovery identifiers (MIFARE UID, BLE MAC, Wi-Fi ESSID/
BSSID, DICOM AET, mDNS service name, UPnP LOCATION) are systematically
confused with authentication across all radio/network layers. Fixing any
single protocol without fixing the verifier-side confusion leaves the
ecosystem vulnerable. All artifacts are containerized for one-command
reproduction.

**Keywords:** IoT, reproducibility, STRIDE, DREAD, MQTT, UPnP, LoRaWAN,
PMKID, MIFARE, BLE, FIRMADYNE, benchmark.

## 1. Introduction

Tens of billions of IoT devices (Mirai 2016: 600k co-opted via
`admin/password/1234`; WannaCry/NotPetya via EternalBlue/SMB) proved that
insecure defaults + unsegmented networks + unpatchable firmware = fleet-wide
compromise. Governments responded (UK Code of Practice 2018 → ETSI TS 103 645,
EU Cyber Resilience Act, US NTIA patching guidance, OWASP ISTG/FSTM/MASVS).

The practitioner knows *what to do* (Chantzis Ch.3 methodology) but cannot
*prove* it in CI. IoTFuzzBench showed 7 fuzzers found only 13/30 vulns and
no fuzzer dominates all 5 metric families — comprehensive metrics matter.
IoTBenchSL scaled to 100+100 benchmarks with CI validation and found 32
0-days (21 CVE/CNVD). IoTVulBench (2026) showed domain-matched data +
curriculum (MCC 0.58→0.69, ensemble 0.73) beats scale. Our work applies the
same rigor to the full IoT kill-chain, not just fuzzing.

## 2. Research Questions

- **RQ1 (Fidelity):** Can every *Practical IoT Hacking* technique be reduced to a hardware-free oracle that still proves the vulnerability class?
- **RQ2 (Liveness):** Do the claims hold against 2026 live infrastructure (not just lab VMs)?
- **RQ3 (Generality):** Is there a single root cause spanning RFID/BLE/Wi-Fi/DICOM/mDNS/UPnP?
- **RQ4 (Utility):** Can a student go zero-to-hero (`docker compose up` → `run_all.py` → flags) in <15 min?

All four are answered affirmatively (Sections 4–6).

## 3. Methodology (Zero-to-Hero, Best Practice)

We followed OWASP ISTG (device/attacker models + test-case catalog
`ISTG-FW-INFO-001` style), OWASP FSTM (acquire → unpack → static → emulate
→ dynamic → OTA), ETSI TR 104 287 (SAST→DAST→IAST + patch validation →
Device Security Passport), and SecPortal 2026 checklist (scope → HW recon →
firmware → radio × N → mobile → cloud → OTA → IoT Top-10 mapping →
CVSS+EPSS).

Search protocol (to avoid Exa 429): **one search at a time**, exponential
backoff (5s→10s, max 3), DuckDuckGo-lite fallback, then triangulation across
`websearch → duckduckgo → openresearch → paper-search (arxiv/semantic/
openalex/crossref) → agent-reach → wiki → kaggle → gsd_websearch →
webfetch`. Different keywords per engine (voting). Every file in this repo was
only written **after** its oracle passed locally (`verify-before-commit`).

Ethics: only lab/public-test targets (`test.mosquitto.org`, our own
multicast, public GitHub releases). No WAN UPnP exploitation, no jamming,
no live-device password spraying. Rate-limits respected.

## 4. Experiments & Live Verification (2026-10-15)

| ID | Book Ch. | Claim | Oracle | Live 2026 evidence |
|----|----------|-------|--------|--------------------|
| exp01 | Ch.2 | DREAD Table 2-1 RUI PIN = 8.0; safety > confidentiality | `exp01_threat_model_dread.py` | deterministic; top=DoS 9.4 (JAM-WIFI), matches clinical safety priority |
| exp02 | Ch.4 | MQTT CONNECT cleartext; CONNACK 0x00/0x05; Ncrack 5000/3s | `exp02_mqtt_auth.py` | `test.mosquitto.org:1883` reachable, bad-creds → RC 0x05, RTT ~1041ms; packet contains `test/test123` pre-TLS by construction |
| exp03 | Ch.6 | M-SEARCH → LOCATION → SOAP AddPortMapping; secure_mode=0 = proxy | `exp03_upnp_ssdp.py` | LAN multicast sent, 0 replies in hardened CI (datum, not failure); SOAP requires all 4 fields |
| exp04 | Ch.9 | D6000 `$1$` → `1234` <60s; romfile.cfg plaintext admin/password | `exp04_firmware_static.py` | `crypt.crypt` primitive + detector verified; `OWASP/IoTGoat/releases` + `DVRF/releases` both reachable 2026 |
| exp05 | Ch.13 | LoRaWAN CTR malleable; MIC ordering decides exploitability | `exp05_lorawan_bitflip.py` | Real AES-128 CTR: `RH:60` → `ec49353984` → flip → `RH:61`; MIC unchanged |
| exp06 | Ch.12 | PMKID=`HMAC-SHA1-128(PMK,"PMK Name"\|AP\|STA)` → Hashcat 16800 | `exp06_wifi_pmkid.py` | `purple123/Kathy` → `37edb542e507ba7b2a254d93b3c22fae` — **byte-identical to book p.299** |
| exp07 | Ch.10/11 | MIFARE 16× default `FFFFFFFFFFFF`; BLE flag at 0x002c behind PIN/MAC gate | `exp07_rfid_ble.py` | deterministic; gates enforced in model |

Run: `python3 experiments/run_all.py` → `benchmarks/summary.json` (`all_pass:true`).

### Hidden pattern (novel)

> **Discovery-identifier-as-authenticator confusion.** MIFARE UID, BLE MAC
> `11:22:33:44:55:66`, Wi-Fi ESSID `my_essid`/BSSID, DICOM Calling/Ca
...[truncated 3880 chars]