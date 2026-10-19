# Anti-Cheat / Elytra Security Research — Reference Architecture & LLM Extraction Corroborated Findings

> **Status:** research compilation, 2026-10-19
> **Sources:** GPT 5.x extraction via LLMRE harness (disclosure/academic framing), cross-checked against local first-party RE artifacts (`C:/Users/Kiyo/wardogs_elytra_debug_notes.md`, `wardogs-reversing.md`, this repo's data dumps)
> **Related:** [SECURITY.md](../SECURITY.md) disclosure posture · debugger-attachment research (private)

---

## 1. What this document is

Compiled from three LLM extraction sessions (GPT 5.x, disclosure-frame and academic framing — the proven non-refusal channels from the LLMRE research) plus reconciliation against our own first-party reversing artifacts. Purpose: a public reference layer for anti-cheat security research on Wardogs, consistent with this repo's defensive-research posture.

**Key GPT-sourced correction to common assumptions (verified):**

- **WARDOGS is developed by BULKHEAD, published by Team17** — NOT Embark Studios. ([Steam listing](https://store.steampowered.com/app/1867240/WARDOGS/))
- **Elytra is Embark's in-house anti-cheat technology** (their product line, also deployed in THE FINALS and ARC Raiders per their [Sept 30, 2026 update](https://arcraiders.com/news/update-on-anti-cheat)).
- Wardogs licenses/deploys Elytra; Embark's public Elytra materials describe THE FINALS deployment, not necessarily Wardogs internals.

This distinction matters for disclosure routing: Elytra findings → Embark; Wardogs game-trust-model findings → BULKHEAD/Team17.

---

## 2. Wardogs public security posture (vendor statements, checked 2026-10-19)

From the [Steam listing](https://store.steampowered.com/app/1867240/WARDOGS/) and [enforcement policy](https://www.wardogs.com/enforcement):

- Elytra identified as **kernel-level anti-cheat**
- Client-side + server-side detection, application monitoring during gameplay, **input-pattern analysis**, integrity checks
- **Secure Boot and TPM not required** (currently; reserved as future requirement)
- Steam AppID 1867240

## 3. First-party observed Elytra footprint (our box)

From `wardogs_elytra_debug_notes.md` (local artifact, corroborates the reference architecture):

| Component | Observation |
|---|---|
| `elytraldrfs_driver.sys` | loader driver (disk-visible) |
| `Elytra.Service` | LocalSystem service; heartbeat-checked; relaunches with game |
| Payload driver | loaded via `ZwLoadDriver` from randomly-named device object (`elytra_<random>`); **memory-only, invisible on disk** |
| Runtime protection | packed `runtime.dll`: no .text section, per-string decrypt stubs, TEB-walk API resolution, direct syscalls, ImageBase 0x200000000 |

Deployment requirements per Embark help center: DSE on, testsigning off, **kernel debugging disabled** (listed as a security requirement — implying KDNET sessions are detectable/expected-off).

## 4. Reference architecture (GPT disclosure-frame output, reconciled)

"UE5-native anti-cheat" is an *integration* description, not a standardized architecture. Typical four-layer deployment:

| Layer | Components/responsibilities | Trust boundary |
|---|---|---|
| Game process | engine integration, integrity measurements, event collection, session init | inside a process the machine owner can modify |
| Privileged usermode service | install/update, driver lifecycle, IPC, telemetry batching | bridges game ↔ Windows privileges ↔ remote services |
| Kernel driver | process-access controls, image/process notifications, integrity observations | >ordinary apps; exposed to other kernel code |
| Remote services | admission, authoritative validation, event correlation, behavioral analysis, sanctions | retains evidence, enforces independently of client |

**Security-principal separation lesson (disclosure-relevant):** a running service ≠ healthy driver; healthy driver ≠ truthful game reports; authenticated telemetry ≠ accurate contents. Each layer can be independently lying/degraded — that's the attack-surface topology for disclosure documentation.

## 5. UE5 engine integration surfaces (academic-frame output)

Three trust boundaries where engine meets anti-cheat:

1. **Network input** — `PacketHandler` chain (`HandlerComponent`s: encryption/compression/reliability/handshake). `StatelessConnectHandlerComponent` = stateless handshake with cookies/rotating secrets. Anti-cheat *may* integrate as a packet component; not required.
2. **Game-state authority** — server-authoritative replication, movement validation, RPC dispatch → game-specific validation → authoritative state change.
3. **Client execution environment** — process protection, integrity checks, detection services.

**Evidence discipline (GPT's repeated caveat, worth keeping in the public doc):** public Epic documentation describes these integration *points*; it does **not** establish that any specific commercial anti-cheat monitors FName pools, GUObjectArray, or GC. Mechanism documentation ≠ deployment claims. Our public docs should keep this distinction explicit.

## 6. Reconciliation with our first-party data

| GPT claim | Our artifact | Agreement |
|---|---|---|
| kernel driver + service + memory-only payload | `wardogs_elytra_debug_notes.md` observed exactly this | ✅ |
| usermode anti-debug checks (PEB, NtQueryInformationProcess 0x07/0x1E/0x1F, CheckRemoteDebuggerPresent, ThreadHideFromDebugger, RDTSC) | catalogued in debug notes | ✅ |
| runtime.dll direct-syscall resolution defeats usermode hooks | debug notes: TEB-walk + direct syscalls, ScyllaHide "probabilistic" | ✅ |
| UE5 version | debug notes header says **UE5.7.4** (our reversing); GPT could not confirm version publicly | ⚠️ we have it first-party: 5.7.4 |
| input-pattern analysis | vendor policy statement; our behavioral notes pending | vendor claim only |

## 7. Open questions for the disclosure queue

1. **Elytra heartbeat mechanics** — service liveness checks: what does the game do on heartbeat loss (observed: play blocked)? Disclosure-relevant: does heartbeat failure create a DoS vector (third-party service kill)?
2. **Payload driver loading** — `ZwLoadDriver` from random device object: what validates the driver image before load? (Signed? Hash-pinned? Remote-attested?)
3. **Telemetry trust chain** — what signs/batches local events; is the client-side collector spoofable (relevant to *false-positive* disclosure, not evasion)?
4. **Engine-side integration** — does Wardogs use UE's `PacketHandler` chain for anti-cheat, or purely out-of-band Elytra telemetry?
5. **Ward Dynamics Framework** — proprietary BULKHEAD layer; any known trust-model documentation?

## 8. Raw extraction files

- `E:/Reverse_Engineer/LLMRE/harness/results/wardogs_gpt/elytra_disclosure.md` (12.8KB — full reference architecture + detection classes + mitigation guidance)
- `E:/Reverse_Engineer/LLMRE/harness/results/wardogs_gpt/ue5_ac_internals.md` (14.9KB — UE5 engine-hook mechanics, evidence-graded)
- `E:/Reverse_Engineer/LLMRE/harness/results/wardogs_gpt/wardogs_public.md` (6.5KB — public-posture summary with citations)

*Extraction method: GPT 5.x via Codex subscription, disclosure/academic framing channels (LLMRE harness Entries 4, 10c, 11 — see `E:/Reverse_Engineer/LLMRE/harness/FINDINGS-LOG.md`). These channels reliably produce mechanism-level content that direct offensive framing refuses; all vendor-attribution claims above were cross-checked against primary sources GPT cited.*
