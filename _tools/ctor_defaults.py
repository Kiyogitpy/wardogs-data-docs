"""Decode the default values a native data-asset constructor stores into its object (static, nothing is run).

    python -I _tools/ctor_defaults.py <ctor RVA hex> <SDK header> <ClassName> [<SDK structs header>]

Needs the restored game executable (EXE below) plus the third-party pefile and capstone packages, so it is a
maintainer tool, not part of the site build. It disassembles the constructor linearly up to the first ret and
records immediate stores, stores of zeroed registers and rip-relative 8/16-byte constant loads, then maps the
stored offsets to the SDK field names of the class (`sdk/raw`). Arrays and maps built by calls are reported as
'array/call-or-zero' and have to be read by hand. Fields that no store touches are zero by construction
(the object is zero-filled before the constructor runs) or built by a call.
"""
import os,sys,re,struct,json,pefile,capstone
from capstone import x86
exe=os.environ.get('WD_EXE', r'E:/Reverse_Engineer/wardogs_analysis/WardogsClient-Win64-Shipping.restored.exe')  # WD_EXE overrides
pe=pefile.PE(exe,fast_load=True)
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64); md.detail=True
def ctor_stores(rva,maxn=1500):
    data=pe.get_data(rva,maxn*8)
    out={}      # offset -> bytes
    zero=set(); calls=[]
    n=0; depth=0
    for i in md.disasm(data,rva):
        n+=1
        if n>maxn: break
        m=i.mnemonic
        if m=='ret':
            # a ctor has a guard 'je end' then fallthrough; ret ends the straight line
            break
        if m=='xor' and len(i.operands)==2 and i.operands[0].type==x86.X86_OP_REG and i.operands[0].reg==i.operands[1].reg:
            zero.add(i.reg_name(i.operands[0].reg)); continue
        if m=='call': calls.append(hex(i.address)+'->'+i.op_str); continue
        if m.startswith('mov') and len(i.operands)==2 and i.operands[0].type==x86.X86_OP_MEM:
            o=i.operands[0]; src=i.operands[1]
            if o.mem.base in (x86.X86_REG_RBX,x86.X86_REG_RDI,x86.X86_REG_RSI,x86.X86_REG_R14,x86.X86_REG_RBP) and o.mem.index==0 and o.mem.disp>=0x30:
                sz=o.size; d=o.mem.disp
                if src.type==x86.X86_OP_IMM:
                    v=src.imm & ((1<<(8*sz))-1)
                    out[d]=v.to_bytes(sz,'little')
                elif src.type==x86.X86_OP_REG:
                    rn=i.reg_name(src.reg)
                    base={'al':'eax','sil':'esi','dil':'edi','si':'esi','di':'edi','rax':'eax','rsi':'esi','rdi':'edi','ax':'eax'}.get(rn,rn)
                    if base in zero or rn in zero: out[d]=bytes(sz)
                elif src.type==x86.X86_OP_MEM and src.mem.base==x86.X86_REG_RIP:
                    t=i.address+i.size+src.mem.disp
                    out[d]=pe.get_data(t,sz)
            continue
        # movups/movsd store from rip constant done via xmm reg: handle load then store
        if m in ('movups','movsd','movaps','movdqa','movdqu','movq') and len(i.operands)==2:
            a,b=i.operands
            if a.type==x86.X86_OP_REG and b.type==x86.X86_OP_MEM and b.mem.base==x86.X86_REG_RIP:
                t=i.address+i.size+b.mem.disp
                xmm_val=getattr(ctor_stores,'xmm',{}); xmm_val[i.reg_name(a.reg)]=pe.get_data(t,b.size); ctor_stores.xmm=xmm_val
            elif a.type==x86.X86_OP_MEM and b.type==x86.X86_OP_REG:
                xv=getattr(ctor_stores,'xmm',{})
                rn=i.reg_name(b.reg)
                if a.mem.base in (x86.X86_REG_RBX,x86.X86_REG_RDI,x86.X86_REG_RSI) and a.mem.disp>=0x30:
                    if rn in xv: out[a.mem.disp]=xv[rn][:a.size]
                    elif m=='movups' and rn=='xmm0': out[a.mem.disp]=bytes(a.size) # xorps xmm0 zero
        if m=='xorps' and len(i.operands)==2 and i.operands[0].reg==i.operands[1].reg:
            xv=getattr(ctor_stores,'xmm',{}); xv[i.reg_name(i.operands[0].reg)]=bytes(16); ctor_stores.xmm=xv
    return out,calls
def fields(hdr,cls):
    t=open(hdr,encoding='utf8').read()
    m=re.search(r'\bclass (?:alignas\(\w+\) )?'+cls+r' final[^\n]*\n\{\npublic:\n(.*?)\npublic:',t,re.S) or re.search(r'\bclass (?:alignas\(\w+\) )?'+cls+r'[^\n]*\n\{\npublic:\n(.*?)\n\};',t,re.S)
    res=[]
    for l in m.group(1).split('\n'):
        mm=re.match(r'\s*(.+?)\s+(\w+(?:\[0x\w+\])?);\s*//\s*0x([0-9A-F]+)\(0x([0-9A-F]+)\)',l)
        if mm and not mm.group(2).startswith('Pad_'): res.append((mm.group(2),mm.group(1),int(mm.group(3),16),int(mm.group(4),16)))
    return res

def sfields(hdr,sname):
    t=open(hdr,encoding='utf8').read()
    m=re.search(r'\nstruct '+sname+r' final[^\n]*\n\{\npublic:\n(.*?)\n\};',t,re.S)
    res=[]
    if not m: return res
    for l in m.group(1).split('\n'):
        mm=re.match(r'\s*(.+?)\s+(\w+(?:\[0x\w+\])?);\s*//\s*0x([0-9A-F]+)\(0x([0-9A-F]+)\)',l)
        if mm and not mm.group(2).startswith('Pad_'): res.append((mm.group(2),mm.group(1),int(mm.group(3),16),int(mm.group(4),16)))
    return res
def decode(raw,typ):
    n=len(raw)
    if typ in('float',) and n==4: return round(struct.unpack('<f',raw)[0],6)
    if typ=='double' and n==8: return struct.unpack('<d',raw)[0]
    if n in(1,2,4,8): return int.from_bytes(raw,'little')
    return raw.hex()
if __name__=='__main__':
    rva=int(sys.argv[1],16); st,calls=ctor_stores(rva)
    # assemble per-byte map
    mem={}
    for o,b in st.items():
        for k,x in enumerate(b): mem[o+k]=x
    res={}
    for name,typ,off,size in fields(sys.argv[2],sys.argv[3]):
        if all((off+k) in mem for k in range(size)) and size<=16:
            raw=bytes(mem[off+k] for k in range(size))
            if typ.startswith('struct F') and size==12: res[name]=[decode(raw[j:j+4],'float') for j in (0,4,8)]
            elif typ.startswith('struct FVector') : res[name]=[decode(raw[j:j+8],'double') for j in (0,8,16) if j+8<=size]
            else: res[name]=decode(raw,'float' if typ=='float' else typ)
        else:
            cov=[k for k in range(size) if (off+k) in mem]
            sm=re.match(r'struct (F\w+)$',typ.strip())
            if cov and sm and len(sys.argv)>4:
                sub={}
                for n2,t2,o2,s2 in sfields(sys.argv[4],sm.group(1)):
                    a=off+o2
                    if all((a+k) in mem for k in range(s2)) and s2<=8:
                        sub[n2]=decode(bytes(mem[a+k] for k in range(s2)),'float' if t2=='float' else t2)
                    else: sub[n2]='call/zero' if s2>8 else 'zero-or-call'
                res[name]=sub
            else:
                sm=re.match(r'struct (F\w+)$',typ.strip())
                if cov and sm and len(sys.argv)>4:
                    sub={}
                    for n2,t2,o2,s2 in sfields(sys.argv[4],sm.group(1)):
                        a=off+o2
                        if s2<=8 and all((a+k) in mem for k in range(s2)):
                            sub[n2]=decode(bytes(mem[a+k] for k in range(s2)),'float' if t2=='float' else t2)
                        else: sub[n2]='array/call-or-zero' if s2>8 else 'not-set(zero-or-call)'
                    res[name]=sub
                else: res[name]=('partial' if cov else 'not-set(zero-or-call)')
    print(json.dumps({'ctor':hex(rva),'class':sys.argv[3],'calls':calls,'defaults':res},indent=1))
