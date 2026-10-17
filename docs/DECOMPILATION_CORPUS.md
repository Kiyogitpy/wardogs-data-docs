# Local native decompilation corpus

The restored CL-516586 executable is being exported into a local,
searchable research corpus. The artifacts are C-like pseudocode and
static-analysis metadata, not original source or a buildable game project.
They remain outside the checkout; do not publish the raw corpus with the
data wiki. Security findings follow [SECURITY.md](../SECURITY.md).

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
