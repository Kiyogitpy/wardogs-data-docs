"""Verify assets/data/native-defaults.json against the class constructors in the restored exe.

    python _tools/native_defaults_check.py

For each distinct ctor_rva the constructor is disassembled (capstone + pefile), every store of a known
immediate or loaded constant to [reg+disp] is applied to a byte map, and each JSON entry is compared
with the bytes at its offset. Exit 1 on any mismatch; exit 0 with a message if the exe is absent or the
disassembler libraries are missing.
"""
import json
import os
import struct
import sys

EXE = r"E:/Reverse_Engineer/wardogs_analysis/WardogsClient-Win64-Shipping.restored.exe"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "assets", "data", "native-defaults.json")


def main():
    if not os.path.exists(EXE):
        print(f"exe not found ({EXE}); skipping native defaults check")
        return 0
    try:
        import pefile
        from capstone import Cs, CS_ARCH_X86, CS_MODE_64
        from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_OP_REG, X86_REG_RIP, X86_REG_RSP
        from capstone.x86 import X86_REG_RAX, X86_REG_RCX, X86_REG_RDX, X86_REG_R8, X86_REG_R9
        from capstone.x86 import X86_REG_XMM0, X86_REG_XMM1
    except ImportError as e:
        print(f"{e}; skipping native defaults check")
        return 0
    pe = pefile.PE(EXE, fast_load=True)
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True

    def rd(rva, n):
        return pe.__data__[pe.get_offset_from_rva(rva):][:n]

    def ctor_bytes(rva):
        vals, mem = {}, {}
        for i in md.disasm(rd(rva, 0x1200), rva):
            if i.mnemonic == "ret":
                break
            ops = i.operands
            if i.mnemonic == "call":
                for r in (X86_REG_RAX, X86_REG_RCX, X86_REG_RDX, X86_REG_R8, X86_REG_R9, X86_REG_XMM0, X86_REG_XMM1):
                    vals.pop(r, None)
                continue
            if i.mnemonic not in ("mov", "movss", "movsd", "movaps", "movups", "movq", "movd", "xorps", "pxor", "xor") or len(ops) != 2:
                continue
            a, b = ops
            if i.mnemonic in ("xorps", "pxor", "xor") and a.type == X86_OP_REG and b.type == X86_OP_REG and a.reg == b.reg:
                vals[a.reg] = 0
            elif a.type == X86_OP_REG:
                if b.type == X86_OP_IMM:
                    vals[a.reg] = b.imm & 0xFFFFFFFFFFFFFFFF
                elif b.type == X86_OP_MEM and b.mem.base == X86_REG_RIP and i.mnemonic in ("movss", "movsd", "mov"):
                    t = i.address + i.size + b.mem.disp
                    try:
                        d = rd(t, 8)
                        vals[a.reg] = struct.unpack("<I", d[:4])[0] if (i.mnemonic == "movss" or b.size == 4) else struct.unpack("<Q", d)[0]
                    except Exception:
                        vals.pop(a.reg, None)
                elif b.type == X86_OP_REG and b.reg in vals:
                    vals[a.reg] = vals[b.reg]
                else:
                    vals.pop(a.reg, None)
            elif a.type == X86_OP_MEM and a.mem.base not in (0, X86_REG_RIP, X86_REG_RSP) and a.size <= 8:
                v = None
                if b.type == X86_OP_IMM:
                    v = b.imm & ((1 << (8 * a.size)) - 1)
                elif b.type == X86_OP_REG and b.reg in vals:
                    v = vals[b.reg] & ((1 << (8 * a.size)) - 1)
                if v is not None:
                    for k in range(a.size):
                        mem[a.mem.disp + k] = ((v >> (8 * k)) & 0xFF, i.address)
        return mem

    entries = json.load(open(DATA, encoding="utf-8"))["entries"]
    cache, bad = {}, []
    for e in entries:
        ctor = int(e["ctor_rva"], 16)
        if ctor not in cache:
            cache[ctor] = ctor_bytes(ctor)
        mem, off, size = cache[ctor], int(e["offset"], 16), e["size"]
        if not all(off + k in mem for k in range(size)):
            bad.append((e["class"], e["property"], e["offset"], "no store", e["value"]))
            continue
        raw = int.from_bytes(bytes(mem[off + k][0] for k in range(size)), "little")
        t = e["type"]
        if t == "float":
            got = float(f"{struct.unpack('<f', struct.pack('<I', raw))[0]:.7g}")
        elif t == "double":
            got = float(f"{struct.unpack('<d', struct.pack('<Q', raw))[0]:.7g}")
        elif t == "bool":
            got = bool(raw)
        elif t == "int32":
            got = raw - (1 << 32) if raw >> 31 else raw
        else:
            got = raw
        if got != e["value"] or hex(mem[off][1]) != e["store_rva"]:
            bad.append((e["class"], e["property"], e["offset"], got, e["value"], hex(mem[off][1]), e["store_rva"]))
    print(f"{len(entries)} native defaults checked across {len(cache)} constructors, {len(bad)} mismatches")
    for b in bad:
        print("  mismatch", *b)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
