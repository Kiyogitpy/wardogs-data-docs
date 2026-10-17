# Damage IDA pass — input validation results

This report recorded the failed first IDA pass on the dump-reconstructed
`WardogsFullDump_fixed.exe` (SHA-256 `97ec9e0d…`), a different hash from
the restored executable. That pass recovered no usable damage code.

It has been merged into [the damage evidence page](evidence/damage.md):

- The pass, map inventory, vtable samples and capture coverage:
  [§2.2](evidence/damage.md#22-failed-pass-on-the-dump-reconstructed-pe).
- Hashes of the PE, the map, the capture and the result files:
  [§1](evidence/damage.md#1-binary-identity-and-hashes).
