"""Verify the byte-level facts cited by pipelines/Wardogs_HitRegistration_v1.md against the executable.

    python -I _tools/hit_registration_check.py
    WARDOGS_ANALYSIS_EXE=<path> python -I _tools/hit_registration_check.py   # also compare function bytes

Reads only the flat restored executable (pefile; no corpus, no IDA database). Each check is an exact byte
pattern at a stated RVA, plus a few pointer-table reads. The patterns pin:

1. the projectile trace call (`mov dword [rsp+0x20],3` then call 0x3CAB670) and the query-parameter
   construction on the instance (`WeaponTrace`, trace-complex = 1, response container set to Block);
2. the instance's return-face-index / return-physical-material word and the trace-skip flag test;
3. the random-stream constants in the ricochet function;
4. the net-mode compare in the hit handler (`cmp eax,3`) and the proxy-component virtual slots
   (0x4F8, 0x500, 0x508..0x530) that its RPC thunks and helpers use, read from the vtable at 0xB1AF7A0;
5. the FWDProjectileStats constructor defaults the hit path reads (penetrate, effectiveness, ricochet angle);
6. with WARDOGS_ANALYSIS_EXE set, whether each cited function is byte-identical in that image
   (a differing function starts with a dispatch stub and is read from the restored image).

Exit 1 on any mismatch; exit 0 with a message if the executable or the library is missing.
"""
import os
import struct
import sys

try:
    import pefile
except ImportError:
    print("pefile not installed; skipping")
    sys.exit(0)

EXE = r"E:/Reverse_Engineer/wardogs_analysis/WardogsClient-Win64-Shipping.restored.exe"
ALT = os.environ.get("WARDOGS_ANALYSIS_EXE")
BASE = 0x140000000


class Image:
    def __init__(self, path):
        self.pe = pefile.PE(path, fast_load=True)
        self.f = open(path, "rb")
        self.secs = [(s.VirtualAddress, s.SizeOfRawData, s.PointerToRawData) for s in self.pe.sections]

    def read(self, rva, n):
        for va, rs, raw in self.secs:
            if va <= rva < va + rs:
                self.f.seek(raw + rva - va)
                return self.f.read(n)
        return b""


# (rva, expected bytes as hex, label)
PATTERNS = [
    (0x6F3C74B, "c744242003000000", "projectile trace: fifth argument (trace channel) = 3"),
    (0x6F3C75A, "e811efd6fc", "projectile trace: call 0x3CAB670 (line trace by channel)"),
    (0x6F3C713, "4438af5c020000", "integrator tests instance +0x25C (skip-trace flag) before tracing"),
    (0x6F3C8C1, "e87aa6ffff", "integrator: call 0x6F36F40 (impact) when bBlockingHit"),
    (0x6B8E2F4, "41b101", "instance ctor: bInTraceComplex = 1"),
    (0x6B8E301, "e82a7910fd", "instance ctor: call 0x3C95C30 (FCollisionQueryParams ctor)"),
    (0x6B8E312, "ba02000000", "instance ctor: response container set to 2 (Block) for every channel"),
    (0x6F30F70, "66c787520100000101", "instance init: return-face-index and return-physical-material = 1"),
    (0x6F36BD2, "6983d00000003584b30b", "ricochet: random stream seed * 196314165 (0xBB38435)"),
    (0x6F36BDF, "056b631936", "ricochet: + 907633515 (0x3619636B)"),
    (0x6B73F55, "83f803", "hit handler: net mode == 3 branch"),
    (0x699E17B, "66c787040200000100", "stats ctor: bShouldPenetrate = 1, bForcePenetrateThinSurfaces = 0"),
    (0x699E184, "48c787080200000000803f", "stats ctor: PenetrationEffectivenessMultiplier = 1.0, ExitSpeedMultiplier = 0"),
    (0x699E196, "c7871402000000002041", "stats ctor: MinImpactAngleForRicochet = 10.0"),
]

# (vtable rva, byte offset, expected target rva, label)
SLOTS = [
    (0xB1AF7A0, 0x4F8, 0x6B72370, "Client_ValidateClientHit_Response implementation slot"),
    (0xB1AF7A0, 0x500, 0x6B74770, "Server_ValidateClientHit implementation slot"),
    (0xB1AF7A0, 0x508, 0x6B73C20, "GetWeaponActorForId slot"),
    (0xB1AF7A0, 0x510, 0x6B73A60, "GetOwningCharacter slot"),
    (0xB1AF7A0, 0x518, 0x6B73B30, "GetOwningController slot"),
    (0xB1AF7A0, 0x520, 0x6B73DE0, "IsServerOwned slot"),
    (0xB1AF7A0, 0x528, 0x6B73940, "GetIgnoredComponents slot"),
    (0xB1AF7A0, 0x530, 0x6B73810, "GetIgnoredActors slot"),
]

# RPC thunks: vtable slot displacement loaded as `mov reg,[rax+disp32]`
THUNKS = [
    (0x69E93E0, 0x500, "Server_ValidateClientHit thunk calls slot 0x500"),
    (0x69E8E50, 0x4F8, "Client_ValidateClientHit_Response thunk calls slot 0x4F8"),
    (0x69E8F70, 0x530, "GetIgnoredActors thunk calls slot 0x530"),
    (0x69E8FF0, 0x528, "GetIgnoredComponents thunk calls slot 0x528"),
    (0x69E9070, 0x510, "GetOwningCharacter thunk calls slot 0x510"),
    (0x69E90A0, 0x518, "GetOwningController thunk calls slot 0x518"),
    (0x69E9140, 0x508, "GetWeaponActorForId thunk calls slot 0x508"),
    (0x69E91D0, 0x520, "IsServerOwned thunk calls slot 0x520"),
]

CITED = [
    (0x6F3C060, 2840), (0x6F3CB80, 1449), (0x6F36F40, 1486), (0x6F2F740, 1002), (0x6F2FC20, 1630),
    (0x6F36190, 1133), (0x6F36600, 2356), (0x6F353F0, 3481), (0x6F380A0, 700), (0x6F344D0, 288),
    (0x6F342B0, 323), (0x6F37510, 572), (0x6F30E50, 555), (0x6B8E100, 972), (0x6B73E90, 1284),
    (0x6B721B0, 913), (0x6B73500, 571), (0x6B725B0, 3780), (0x6B717C0, 1605), (0x6B72370, 465),
    (0x69E93E0, 288), (0x69E8E50, 158), (0x6E6BD70, 23), (0x6E71010, 172), (0x6EF8DE0, 1638),
    (0x6DAE470, 33), (0x76D9110, 2727), (0x3CAB670, 121), (0x3CAE910, 581), (0x3CB56B0, 449),
    (0x3C95C30, 130), (0x42D9770, 0x70), (0x42AF7C0, 0x19), (0x699DEE0, 914),
]


def main():
    if not os.path.exists(EXE):
        print("restored executable not found; skipping")
        return 0
    ref = Image(EXE)
    bad = 0
    for rva, hexs, label in PATTERNS:
        want = bytes.fromhex(hexs)
        got = ref.read(rva, len(want))
        ok = got == want
        bad += not ok
        print("%-5s 0x%X  %s" % ("ok" if ok else "FAIL", rva, label))
        if not ok:
            print("      want", want.hex(), "got", got.hex())
    for vt, off, want, label in SLOTS:
        got = struct.unpack("<Q", ref.read(vt + off, 8))[0] - BASE
        ok = got == want
        bad += not ok
        print("%-5s 0x%X+0x%X -> 0x%X  %s" % ("ok" if ok else "FAIL", vt, off, got, label))
    for rva, disp, label in THUNKS:
        code = ref.read(rva, 0x180)
        ok = struct.pack("<I", disp) in code
        bad += not ok
        print("%-5s 0x%X  %s" % ("ok" if ok else "FAIL", rva, label))
    if ALT and os.path.exists(ALT):
        alt = Image(ALT)
        for rva, n in CITED:
            same = alt.read(rva, n) == ref.read(rva, n)
            print("%-9s 0x%X (%d bytes) analysis image" % ("same" if same else "differs", rva, n))
    print("%d mismatches" % bad)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
