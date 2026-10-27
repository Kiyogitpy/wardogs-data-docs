"""Render CUE4Parse Kismet JSON (ScriptBytecode) as line-per-statement pseudocode.
Usage: python -I kismet_listing.py <in.json> <out.txt>"""
import json, sys

def pname(v):
    p = v.get('Variable', v)
    if isinstance(p, dict) and 'Property' in p:
        return p['Property'].get('Name', '?')
    if isinstance(p, dict) and 'Path' in p:
        return '.'.join(p['Path'])
    if isinstance(p, dict) and 'New' in p:  # FKismetPropertyPointer variants
        return str(p['New'])
    return str(p)

def obj(o):
    if o is None: return 'null'
    if isinstance(o, dict):
        n = o.get('ObjectName', ''); path = o.get('ObjectPath', '')
        return f"{n}@{path}" if path else n
    return str(o)

def fn(o):
    n = o.get('ObjectName', '') if isinstance(o, dict) else str(o)
    # "Class'KismetSystemLibrary:IsValid'" -> KismetSystemLibrary::IsValid
    if "'" in n: n = n.split("'")[1]
    return n.replace(':', '::')

def e(x):
    if x is None: return '<none>'
    t = x.get('Token')
    if t in ('EX_LocalVariable', 'EX_InstanceVariable', 'EX_LocalOutVariable', 'EX_DefaultVariable'):
        pre = {'EX_InstanceVariable': 'this.', 'EX_LocalOutVariable': 'out.'}.get(t, '')
        return pre + pname(x['Variable'])
    if t in ('EX_CallMath', 'EX_FinalFunction', 'EX_VirtualFunction', 'EX_LocalFinalFunction', 'EX_LocalVirtualFunction'):
        f = fn(x['Function']) if 'Function' in x else x.get('VirtualFunctionName', '?')
        return f"{f}({', '.join(e(p) for p in x.get('Parameters', []))})"
    if t == 'EX_Context' or t == 'EX_Context_FailSilent':
        o = e(x['ObjectExpression'])
        if o.startswith("Class'Default__"): return e(x['ContextExpression'])  # static lib CDO
        c = e(x['ContextExpression'])
        if c.startswith('this.'): c = c[5:]
        return f"{o}->{c}"
    if t == 'EX_StructMemberContext':
        return f"{e(x['StructExpression'])}.{pname(x['Property'])}"
    if t in ('EX_FloatConst', 'EX_DoubleConst', 'EX_IntConst', 'EX_ByteConst', 'EX_Int64Const'):
        return repr(x['Value'])
    if t == 'EX_NameConst': return f"Name('{x['Value']}')"
    if t == 'EX_StringConst': return repr(x['Value'])
    if t == 'EX_ObjectConst': return obj(x['Value'])
    if t == 'EX_True': return 'true'
    if t == 'EX_False': return 'false'
    if t == 'EX_Self': return 'self'
    if t == 'EX_NoObject': return 'nullptr'
    if t == 'EX_Cast': return f"({x['ConversionType']})({e(x['Target'])})"
    if t == 'EX_DynamicCast': return f"Cast<{fn(x.get('InterfaceClass') or x.get('ClassPtr'))}>({e(x['Target'])})"
    if t == 'EX_StructConst':
        s = fn(x['Struct']) if isinstance(x['Struct'], dict) else x['Struct']
        return f"{s}{{{', '.join(e(p) for p in x['Properties'])}}}"
    if t == 'EX_ArrayConst':
        return f"[{', '.join(e(p) for p in x['Values'])}]"
    if t == 'EX_ArrayGetByRef':
        return f"{e(x['ArrayVariable'])}[{e(x['ArrayIndex'])}]"
    return f"<{t} {json.dumps({k: v for k, v in x.items() if k != 'Token'})[:200]}>"

def stmt(x):
    t = x['Token']
    if t in ('EX_Let', 'EX_LetBool', 'EX_LetObj', 'EX_LetWeakObjPtr', 'EX_LetDelegate', 'EX_LetMulticastDelegate') and 'Variable' in x:
        return f"{e(x['Variable'])} = {e(x['Expression'])}"
    if t == 'EX_LetValueOnPersistentFrame':
        dp = x['DestinationProperty']
        return f"frame.{dp.get('Property', {}).get('Name', '?')} = {e(x['AssignmentExpression'])}"
    if t == 'EX_ComputedJump': return f"goto_computed({e(x['CodeOffsetExpression'])})"
    if t == 'EX_BindDelegate': return f"bind {e(x['Delegate'])} -> {x['FunctionName']}({e(x['ObjectTerm'])})"
    if t in ('EX_AddMulticastDelegate', 'EX_RemoveMulticastDelegate'):
        return f"{t[3:-17]} {e(x['MulticastDelegate'])} <- {e(x['Delegate'])}"
    if t == 'EX_SetArray':
        return f"{e(x['AssigningProperty'])} = [{', '.join(e(p) for p in x['Elements'])}]"
    if t == 'EX_PushExecutionFlow': return f"push_flow -> @{x['PushingAddress']}"
    if t == 'EX_PopExecutionFlow': return "pop_flow"
    if t == 'EX_PopExecutionFlowIfNot': return f"if not ({e(x['BooleanExpression'])}): pop_flow"
    if t == 'EX_Jump': return f"goto @{x['CodeOffset']}"
    if t == 'EX_JumpIfNot': return f"if not ({e(x['BooleanExpression'])}): goto @{x['CodeOffset']}"
    if t == 'EX_Return': return f"return {e(x['Expression'])}"
    if t == 'EX_EndOfScript': return "end_of_script"
    return e(x)

d = json.load(open(sys.argv[1], encoding='utf-8'))
out = []
for ex in d:
    if 'ScriptBytecode' not in ex: continue
    out.append(f"=== {ex['Type']} {ex['Name']}  flags={ex.get('FunctionFlags')}")
    out.append("--- params/locals:")
    for p in ex.get('ChildProperties', []):
        st = p.get('Struct') or p.get('PropertyClass') or (p.get('Inner') or {}).get('Struct')
        out.append(f"    {p['Type']:<16} {p['Name']}  {fn(st) if st else ''}  [{p.get('PropertyFlags','')}]")
    out.append("--- bytecode (offset: statement):")
    for s in ex['ScriptBytecode']:
        try: txt = stmt(s)
        except (KeyError, TypeError): txt = '<' + s['Token'] + ' ' + json.dumps({k: v for k, v in s.items() if k != 'Token'})[:200] + '>'
        out.append(f"@{s.get('StatementIndex'):>5}: {txt}")
open(sys.argv[2], 'w', encoding='utf-8').write('\n'.join(out) + '\n')
