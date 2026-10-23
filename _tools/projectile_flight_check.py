"""Verify the constants cited by pipelines/Wardogs_ProjectileFlight_v1.md against the executable.

    python _tools/projectile_flight_check.py
    WARDOGS_ANALYSIS_EXE=<path> python _tools/projectile_flight_check.py   # also compare function bytes

Reads only the flat restored executable (capstone + pefile). No decompilation corpus and no IDA
database is opened. Checks:

1. the .rdata constants the drag, wind and gravity code loads (pi/8 * 1e-4, 1e-4, -100, 1.2, 0.75, 0.01);
2. the FWDProjectileStats constructor defaults (ctor 0x699DEE0): replays every immediate store to
   [rdi+disp] and compares the fields the flight model reads;
3. that the thrust, gravity and integrator functions read the stats offsets the page names (displacement scan);
4. with WARDOGS_ANALYSIS_EXE set, whether each cited function is byte-identical in that image.
   A differing function starts with, or contains, a dispatch stub, and the page reads it from the
   restored image only.

Exit 1 on any mismatch; exit 0 with a message if the executable or the libraries are missing.
"""
import os
import struct
import sys

EXE = r"E:/Reverse_Engineer/wardogs_analysis/WardogsClient-Win64-Shipping.restored.exe"
ALT = os.environ.get("WARDOGS_ANALYSIS_EXE")

# (rva, kind, expected, label)
CONSTS = [
    (0xB440AF0, "f32", 3.92699076e-05, "pi/8 * 1e-4 (drag: 0.5 * pi/4 * 1e-4 cm^2 -> m^2)"),
    (0x9C083B0, "f64", 9.99999955297e-05, "1e-4 (cm/s -> m/s squared)"),
    (0xA4E07F8, "f64", -100.0, "-100 (m/s^2 -> cm/s^2, and direction)"),
    (0xA3BEF68, "f32", 1.2, "default air density kg/m^3"),
    (0xCED2C4C, "f32", 1.2, "air density returned by the weather subsystem getter 0x6F77F90"),
    (0x9AD4640, "f64", 0.00999999977648, "0.01 (cm/s -> m/s for the drag-curve level)"),
    (0x9AAFD68, "f32", 0.001, "minimum mass kg"),
    (0xCED1BA8, "f32", 0.75, "wind scale (global float)"),
    (0x9AADA78, "f64", 1.0, "1.0 (unit-direction numerator)"),
]

# FWDProjectileStats ctor 0x699DEE0: stats-relative offset -> expected value (name, fmt, value)
DEFAULTS = {
    0x68: ("Length", "f", 1.5), 0x6C: ("Diameter", "f", 0.9), 0x78: ("DragModel.Value", "f", 1.0),
    0x180: ("bHasArmingDelay", "B", 0), 0x184: ("ArmingDelay", "f", 0.0),
    0x188: ("MaxProjectileLifetime", "f", 10.0), 0x1FC: ("TypicalSpeed", "f", 60000.0),
    0x219: ("bShouldThrust", "B", 0), 0x21C: ("TotalFuel", "f", 1000.0), 0x220: ("FuelBurnRate", "f", 10.0),
    0x2B0: ("ThrustSpeed", "f", 0.0), 0x2B4: ("ThrustStartDelay", "f", 0.0), 0x2CC: ("MaxSpeed", "f", 0.0),
    0x2E0: ("bAffectedByGravity", "B", 1),
}

# function -> stats displacements it must contain (as disp32 in its bytes)
READS = {
    0x6F30280: ("thrust", [0x219, 0x2B4, 0x2B0, 0x2BC, 0x2C4]),
    0x6F2E4B0: ("gravity + fuel curve", [0x2E0, 0x219, 0x2B4, 0x228, 0x21C]),
    0x6F3C060: ("integrator", [0x219, 0x2B4, 0x228, 0x220, 0x2CC, 0x2E0]),
}

# cited functions compared against ALT (rva, size)
CITED = [
    (0x6F3BC70, 870), (0x6F3CB80, 1449), (0x6F3C060, 2840), (0x6F2E240, 0x270), (0x6F2E4B0, 0x170),
    (0x6F30280, 1022), (0x6F30680, 0x13A), (0x6F30E50, 555), (0x6F37510, 572), (0x6F39940, 5116),
    (0x6F3D130, 0x94), (0x6BBA8A0, 0x40), (0x6BBA900, 618), (0x6BBAB70, 1243), (0x6BBD500, 8),
    (0x6BBD420, 17), (0x76E07D0, 36), (0x76D8A00, 986), (0x76D9110, 2727), (0x76CC730, 140),
    (0x6F77F90, 9), (0x48AA830, 0x90), (0x48A8480, 430), (0x165ED30, 0xE0), (0x699DEE0, 0x395),
    (0x6F1DDC0, 1075), (0x6F3B0E0, 2949),
    (0x6F78270, 0x20),  # weather wind getter: expected to differ (dispatch stub in the analysis image)
]


def main():
    if not os.path.exists(EXE):
        print(f"exe not found ({EXE}); skipping projectile flight check")
        return 0
    try:
        import pefile
        from capstone import Cs, CS_ARCH_X86, CS_MODE_64
        from capstone.x86 import X86_OP_IMM, X86_OP_MEM
    except ImportError as e:
        print(f"{e}; skipping projectile flight check")
        return 0
    pe = pefile.PE(EXE, fast_load=True)
    img = pe.get_memory_mapped_image()
    bad = 0

    for rva, kind, want, label in CONSTS:
        got = struct.unpack("<f" if kind == "f32" else "<d", img[rva:rva + (4 if kind == "f32" else 8)])[0]
        ok = abs(got - want) <= abs(want) * 1e-6 + 1e-30
        bad += not ok
        print(f"{'ok ' if ok else 'BAD'} const {rva:#x} {kind} {got!r:<24} {label}")

    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    base = pe.OPTIONAL_HEADER.ImageBase
    stores = {}
    for i in md.disasm(img[0x699DEE0:0x699DEE0 + 0x395], base + 0x699DEE0):
        if i.mnemonic != "mov" or len(i.operands) != 2:
            continue
        d, s = i.operands
        if d.type == X86_OP_MEM and s.type == X86_OP_IMM and d.mem.base != 0:
            width = d.size
            val = s.imm & ((1 << (8 * width)) - 1)
            for k in range(width):
                stores[d.mem.disp + k] = (val >> (8 * k)) & 0xFF
        if i.mnemonic == "ret":
            break
    for off, (name, fmt, want) in sorted(DEFAULTS.items()):
        n = struct.calcsize("<" + fmt)
        raw = bytes(stores.get(off + k, 0) for k in range(n))
        got = struct.unpack("<" + fmt, raw)[0]
        ok = abs(got - want) < 1e-6
        bad += not ok
        print(f"{'ok ' if ok else 'BAD'} default FWDProjectileStats+{off:#x} {name:<24} {got}")

    for rva, (name, disps) in READS.items():
        size = 0x400 if rva != 0x6F3C060 else 2840
        blob = img[rva:rva + size]
        missing = [hex(d) for d in disps if struct.pack("<I", d) not in blob]
        bad += bool(missing)
        print(f"{'ok ' if not missing else 'BAD'} reads  {rva:#x} {name:<20} missing disp32 {missing or '-'}")

    if ALT and os.path.exists(ALT):
        alt = pefile.PE(ALT, fast_load=True).get_memory_mapped_image()
        for rva, size in CITED:
            same = img[rva:rva + size] == alt[rva:rva + size]
            print(f"{'same' if same else 'DIFF'} analysis image {rva:#x} +{size:#x}")
    else:
        print("analysis image not given (set WARDOGS_ANALYSIS_EXE); byte comparison skipped")
    print("FAILED" if bad else "all checks passed")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
