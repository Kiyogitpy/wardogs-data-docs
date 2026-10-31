# Local native decompilation corpus

The restored CL-516586 executable has two local, searchable research
corpora. The [DeepExtract corpus](#deepextract-corpus-2026-10-31) was
exported on 2026-10-31 and is the larger one: 987,571 functions, against
437,174 candidates in the IDA 9.3 corpus. The two counts use different
definitions. The IDA 9.3 corpus is described after the DeepExtract section.
The artifacts are C-like pseudocode and static-analysis metadata, not
original source or a buildable game project. They remain outside the
checkout; do not publish the raw corpus with the data wiki. Security
findings follow [SECURITY.md](../SECURITY.md).

## DeepExtract corpus (2026-10-31)

A second corpus for the same input. The input is the file described in
[Location and identity](#location-and-identity) below: SHA-256
`a5c3db107c29bfd92c3b5f317033f698a0c3a84dad712f32990ae302b4f0cc37`,
231,695,256 bytes, MD5 `47322a0b0be8d0d11b39ba0816c86b3c`.

Work directory: `E:/Reverse_Engineer/wardogs_analysis/deepextract_cl516586`.
The run log is in `logs/`. `extraction_report.json` records the driver
result: 1 completed, 0 failed.

Tool: IDA Professional 9.5 with Hex-Rays 9.5.0.261026, run headless through
the DeepExtract driver (plugin v1.0.0). The run log also shows the RUST,
AVXLifter, VMXLifter and gooMBA plugins loading.

Timing from the run log, 2026-10-31:

| Phase | Duration |
|---|---|
| Auto-analysis | about 21 min (07:41 to 08:02) |
| Function extraction | 4 h 47 min 12 s |
| C++ file generation | 5 min 1 s |
| Total after auto-analysis | 4 h 55 min 16 s |

Packing the `.i64` on exit took about 1 h 20 min. This is the time from the
IDA exit line (12:57:40) to the file's last write (14:18). The log has no
line for the pack step.

Scale, from the `scale` object in
`extracted_code/WardogsClient-Win64-Shipping.restored_exe/module_profile.json`:

- 987,571 functions, of which 76,111 are named.
- 966,847 have pseudocode. The other 20,724 hold the text
  `Decompiler returned None`.
- All 987,571 have assembly.
- 68,166 grouped C++ files in the same `extracted_code/` directory.

Outputs:

- `extracted_dbs/wardogsclient-win64-shipping_restored_exe_47322a0b0b.db`,
  SQLite, 10.8 GB.
- `idb_cache/wardogsclient-win64-shipping_restored_exe_47322a0b0b.i64`,
  packed IDA database, 9.9 GB.
- `extracted_code/`, grouped C++ files, 1.5 GB.

The main `functions` table holds address, size, signature, assembly,
pseudocode, xrefs, strings, stack frame and loop analysis. Other tables
are `function_xrefs`, `imports` and `globals`.

Addresses in the database are virtual addresses. Subtract the image base
`0x140000000` to get the file RVA that the IDA 9.3 section cites. For
example, RVA `0x6F06540` is stored as `0x146F06540`.

The `functions` table has no index on `function_address`, so an address
lookup scans the table. Use `function_id`, or a sidecar index. The table is
indexed on name, mangled name and signature.

Most game functions are unnamed (`sub_...`). The database has no `aliases`
table. Reflected names and vtable aliases still come from the IDA 9.3
corpus's `aliases` table.

The [evidence limits](#evidence-limits) of the IDA 9.3 corpus apply here
too. Pseudocode needs review before it is cited. No Blueprint bytecode is
recovered, and no server behavior is established. The raw corpus is not
published.

The sections after this one describe the IDA 9.3 corpus.

## Location and identity

Work directory:
`E:/Reverse_Engineer/wardogs_analysis/decompiled_cl516586_20261017_mmvpuc__`.
Its `README.md` describes searches, tables and checkpoint recovery.
`final_verification.json` is the completion gate; an intermediate batch's
`complete` flag alone does not establish completion of the whole corpus.

Input: `E:/Reverse_Engineer/wardogs_analysis/WardogsClient-Win64-Shipping.restored.exe`.
SHA-256:
`a5c3db107c29bfd92c3b5f317033f698a0c3a84dad712f32990ae302b4f0cc37`.
IDA 9.3, embedded IDAPython 3.13.7, Hex-Rays 9.3.0.260213.

The only map is the [designated external `.idmap`](../mappings/README.md).
It is read directly; no duplicate `.idmap` is created. The owned IDA
databases are analysis outputs, not alternative mapping inputs.

## Scope

The initial database inventory contains 415,176 function candidates.
The supplied vtables and reflected native-name/code-pointer pairs identify
another 21,998 distinct entry candidates missing from that inventory.
The export accounts for all 437,174 candidates with an output or an
explicit failure. This finite scope is not proof that every native
function, instruction, or hidden entry point has been discovered.

The mapping decoder follows Dumper-7's
[packed binary layout](https://github.com/Encryqed/Dumper-7/blob/main/Dumper/Generator/Public/Generators/IDAMappingLayouts.h).
It preserves 21,282 structure records, including duplicate names, and
3,225 enums. SDK field names are associated by matching offset and size;
ambiguous matches are retained without inventing a name. Fourteen selected
damage-related storage layouts are imported and checked for exact size
and member offsets. Uncertain container internals remain opaque bytes.
These are not complete C++ ABI declarations for the whole SDK.

The importer accepts 9,134 vtable labels and three global labels. The
mapping's lone native exec record is rejected because its RVA falls
outside executable sections in this input. Native registration discovery
adds searchable candidates; a matching reflected name alone does not
prove unique class ownership.

## Outputs and search

`code/*.c` and `workers/*/code/*.c` contain sharded pseudocode with function
RVAs and unreviewed-output markers. `corpus.sqlite` merges:

| Table | Contents |
|---|---|
| `functions` | RVA, name, status, reason, code file and byte range |
| `search` | FTS5 index over function names and pseudocode |
| `calls` | Direct calls, outgoing jumps and unresolved indirect calls |
| `aliases` | Mapping labels, vtable slots and reflection candidates |
| `types`, `members`, `enum_values` | Declarations and SDK source references |
| `traits`, `failures` | Inline assembly, jump-containing output and failure records |

For example, run `rg -n 'GlobalDamage_evaluate' code workers -g '*.c'`
from the work directory. A caller query against SQLite is:

```sql
SELECT caller_rva, site_rva, kind
FROM calls
WHERE target_rva = 0x6F02EC0;
```

All addresses are file RVAs for the recorded hash. Outgoing jumps can
cross loader-fragment boundaries and are not automatically tail calls.
Indirect calls have no invented target. A vtable-slot alias records
membership, not exclusive ownership of a shared implementation.

## Evidence limits

The corrected pilot analyzed functions before decompiling: 191 of 201
candidates yielded pseudocode without `JUMPOUT`, nine retained jumps, and
one failed. The earlier unanalysed pilot mostly emitted misleading stubs;
those indexed outputs were removed before the corrected export.

Each worker has an isolated owned database and commits its corpus index
every 25 functions. Failed boundaries, decompiler errors and any timeouts
remain visible. Pseudocode can contain guessed types, compiler artifacts,
inline assembly or jumps even when decompilation succeeds. It requires
review before being cited as implementation behavior.

The [damage trace](evidence/damage.md#23-restored-executable-trace) remains the reviewed behavioral
slice. This export does not recover Blueprint bytecode from the cooked
assets or establish final health application or server behavior. No game
execution, live attachment or service testing is part of this work.
