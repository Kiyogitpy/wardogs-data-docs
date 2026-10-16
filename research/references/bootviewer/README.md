# BootViewer — Local Reference
Source: https://github.com/TheCruZ/BootViewer
Fetched: 2026-10-16

## What It Is

Windows Measured Boot viewer and TPM verifier. Reads the TCG event log
(Windows Boot Configuration Log / WBCL), replays PCRs against the real
TPM, and reports mismatches.

**Author**: TheCruZ (same as kdmapper; this one 3 commits, created 2026-09)
**Language**: Go (via Wails UI framework)
**Dependencies**: Zero — no C compiler, no Node.js, no runtime
**Runs as**: unprivileged user (admin only needed for EFI partition
re-hashing)
**License**: MIT (except embedded Microsoft TBSLogGenerator binaries)

## What It Shows

For every event in the boot log:
- Firmware volumes measured
- Secure Boot variables (PK/KEK/db/dbx) with certificate subjects
- Boot options, device paths, GPT layout
- EFI applications launched (which, in what order, from what media)
- BitLocker PCR 11 locks
- Windows-specific **SIPA events**:
  - Boot manager + OS loader trust boundaries
  - Every module loaded with Authenticode hash + signer + version
  - ELAM registration
  - VBS / HVCI state
  - Code Integrity policy
  - **Kernel debugger / test signing flags** ← important for Pass C

## Why We Use It (Pass C context)

Three cross-checks per boot:

### 1. Did `prep_hyperdbg.ps1` actually land?

After reboot, `logdump` can confirm:
- `hypervisorlaunchtype = off` reflected in boot config
- `VBS = disabled` reflected in SIPA events
- `test signing = disabled` (we want this OFF per Elytra constraint)

If prep didn't take effect or user forgot to reboot, BootViewer shows
the LAST boot's actual state — ground truth, not registry-at-current-time
state (which might differ if a reboot pending).

### 2. Is any OTHER hypervisor present we don't know about?

BootViewer surfaces vendor-driver boot entries. If Elytra installed a
boot-time hypervisor driver (e.g., something hooking VT-x at boot) it
would show in the SIPA driver list before our HyperDbg attempt.

Checked during Pass C: no unknown HV drivers in boot path. Elytra's
`lighthouse_driver.sys` is loaded by `Elytra.Service` at run-time, not
at boot — so it won't contend with HyperDbg for VT-x ownership during
boot, only after the game launches.

### 3. Did anything tamper with our loaded modules?

> every file the boot chain measured with an Authenticode hash is
> hashed again *now* and compared with the value recorded at boot.
> A difference turns the verdict yellow: the file was modified after
> boot, or a tampered version booted and was restored afterwards.

If Elytra or Defender modified our kdmapper-produced driver image on
disk between boot and current run, BootViewer catches it.

## Command-Line Tools

```powershell
go run ./cmd/logdump              # current boot, replay + compare with TPM
go run ./cmd/logdump -v file.log  # verbose dump of an archived boot
go run ./cmd/logdump -files       # also re-hash the measured files on disk
go run ./cmd/tbsdump              # TPM properties, banks, PCR values
```

For Pass C we use the pre-built `logdump.exe` from Releases:

```
E:\Reverse_Engineer\tools\BootViewer\logdump.exe
```

Just run it, pipe output through Select-String to find relevant flags:

```powershell
.\logdump.exe | Select-String "testsigning|hypervisor|VBS|HVCI|CodeIntegrity"
```

## Technical Depth (why it's trustworthy)

### PCR Replay Algorithm

For each event in the log, extend into virtual PCR:
```
PCR[n]_new = HASH( PCR[n]_old || event_digest )
```

After replaying all events, every virtual PCR[0..23] is compared to
real `TPM2_PCR_Read` results. If any mismatch:
- Log is incomplete, OR
- Log was tampered, OR
- Something extended a PCR outside the log (bootkit indicator)

### Digest Re-Verification

For event types where the digest is defined as `HASH(event_data)`,
BootViewer recomputes the hash and compares to the one in the log.
Flags any event where the recorded digest doesn't match recomputed —
smoking gun for log tampering.

### Microsoft's Second Opinion

BootViewer bundles Microsoft's `TBSLogGenerator.exe` (from Windows
Hardware Lab Kit) and runs it independently. Shows the MATCH/MISMATCH
table side-by-side. If BootViewer's own analysis conflicts with
Microsoft's HLK tool, trust neither until you understand why.

## Measured-Boot Primer (background from docs)

### PCR Allocation (Trusted Computing Group spec)

| PCR | Contents |
|---|---|
| 0 | Firmware code (CRTM, BIOS, platform extensions) |
| 1 | Firmware configuration + platform data |
| 2 | Option ROM code (add-in cards) |
| 3 | Option ROM configuration |
| 4 | Boot manager + boot attempts (EV_EFI_BOOT_SERVICES_APPLICATION) |
| 5 | GPT / partition table |
| 6 | Platform-specific / resume events |
| **7** | **Secure Boot policy — SecureBoot/PK/KEK/db/dbx values** |
| 8-10 | OS-specific |
| 11 | BitLocker / Windows-specific measurements |
| 12-14 | SIPA (Windows-specific driver/boot state) |
| 15-23 | Reserved / dynamic |

PCR 7 is load-bearing for policy enforcement and is what BitLocker
uses to decide whether to auto-unlock.

### Why PCRs Are Trustworthy

> PCRs cannot be written, only extended, and they reset only on
> platform reset. You cannot remove a measurement you have already
> made. A bootkit that runs, gets measured, and then erases every
> on-disk trace of itself has still permanently altered the PCR chain
> for that boot.

The entire TPM-based attestation story depends on this: writes to PCRs
are "monotonically chained hashes" and tamper-evident post-boot.

### What Secure Boot vs Measured Boot Actually Do

> Secure Boot **enforces**. Measured Boot **records**. They are
> independent, and for detection purposes the recording is worth more.

Secure Boot's enforcement is useful if you trust the Secure Boot db.
Measured Boot's logging is useful whether or not you trust anything —
you can audit the chain after the fact.

## Related Tools

- **TBSLogGenerator.exe** (Microsoft, in Hardware Lab Kit) — official
  log decoder. BootViewer bundles and runs it as a second opinion.
- **TCGLogTools** (mattifestation) — PowerShell parser for TCG logs,
  older but still useful: https://github.com/mattifestation/TCGLogTools
- **tpmtool.exe** (Windows built-in) — basic TPM operations
  (`tpmtool getdeviceinformation`, `tpmtool gatherlogs`).
- **attestation readiness verifier** (Microsoft 2024+) — Microsoft's own
  simulator for the measured-boot attestation path. See Event Viewer
  TPM-WMI Event ID 1041 for boot health.

## Attestation Readiness States (Microsoft's taxonomy)

Three possible health states BootViewer / Microsoft's tool reports:

| State | Meaning |
|---|---|
| **Attestable** | All checks passed; attestation reports accurate state |
| **Possibly attestable** | PCR issue detected during boot; may need vendor fix |
| **Not attestable** | Critical check failed; device booted unhealthy |

For Pass C our target is **Not attestable** by design — we're
intentionally disabling VBS, running unsigned drivers, etc. Enterprise
VALORANT-tier anticheats refuse to run on not-attestable systems, so
this is actually a Elytra concern: if Elytra uses TPM attestation (not
observed in our Pass A survey but possible in deeper tiers), our prep
breaks it.

## Resume Protocol for Future Pass C

1. Boot normally (no prep)
2. `logdump.exe > boot_baseline.txt` — baseline attestation state
3. Run `prep_hyperdbg.ps1` → reboot
4. `logdump.exe > boot_hyperdbg_prep.txt` — post-prep state
5. Diff the two: expected changes are VBS off, HVCI off, Hyper-V off
6. Confirm `test signing = off` in both (invariant per Elytra)
7. Confirm no new boot-time drivers (would indicate persistence we don't
   want)
8. Only then: proceed with kdmapper chain
