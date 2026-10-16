# CppSDK — UE Class Hierarchy

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

Generated UE class hierarchy for Wardogs CL-516586, extracted via
UEDumper. This is the bridge between the per-category reference
docs (which document *data*) and the game binary (which contains
*code* that consumes that data).

## Status

**Not yet integrated.** The SDK dump exists in the author's local
workspace at `E:\Reverse_Engineer\wardogs_analysis\CppSDK\` but has
not been committed to this repository yet. See
[`../docs/METHODOLOGY.md`](../docs/METHODOLOGY.md) for how the SDK
fits into the pipeline.

Integration tasks (tracked in GitHub issues):

- [ ] Add raw UEDumper output under `sdk/raw/` (one `.h` + `.cpp` per package)
- [ ] Build an index page `sdk/README.md` linking the key classes to
      their per-category docs
- [ ] Produce `sdk/cross_ref.md` mapping SDK classes ↔ data docs
- [ ] Resolve the 26 "SDK gap" bullets in the data docs by linking
      hashed/unnamed fields to their SDK property names
- [ ] Resolve the ~100 unclassified `_aaa...` property hash gaps
      across the reference docs

## When this lands

The SDK gives you three capabilities the current data docs lack:

1. **Field name resolution.** The data docs have many bullets like
   *"the first flag column has no name"* — these are hashed Blueprint
   property names that UEDumper resolves to their actual symbolic
   names (`bOverrideExistingState`, `MaxLifeTimeBuyLimit`, etc.).
2. **Enum resolution.** Many fields currently export as
   `NewEnumeratorN` with just an index. UEDumper gives the enum type
   and the symbolic value name.
3. **Code↔data cross-reference.** With the SDK in hand, you can go
   from a function's `R15 + 0x4B8` memory access in IDA to a specific
   named property on a specific UClass, and from there to the data
   doc that documents what values that property holds.

## SDK generation methodology

See [`../docs/METHODOLOGY.md`](../docs/METHODOLOGY.md) for the full
pipeline. Short version:

1. Launch the game locally
2. Attach UEDumper to the process (requires kernel-level read, see
   [`../tools/README.md`](../tools/README.md))
3. UEDumper walks `GUObjectArray` and `GNames` to produce C++ headers
4. Validate against known offsets from `.idmap`
5. Commit the generated headers under `sdk/raw/`

The AES key for Wardogs's pak files is derivable per-build via
retoc — the author uses this for both CUE4Parse data extraction
and UEDumper sanity checks.

## Related

- Data reference docs (what the SDK structures contain at runtime):
  all `../Wardogs_*.md` files
- IDA mappings (what the compiled binary looks like):
  `../mappings/`
- Methodology (how SDK + data + IDA combine):
  `../docs/METHODOLOGY.md`
