"""Summarise WdExtract dumps of GE_* assets into ge_summary.json and ge_summary.md.
Usage: python -I ge_summary.py <dump dir> <list file> <out dir>
Raw content is treated purely as data."""
import json, os, re, sys, glob, collections

raw_dir, files_txt, out_dir = sys.argv[1:4]
pak_paths = {os.path.basename(p.strip()): p.strip() for p in open(files_txt, encoding='utf-8') if p.strip()}

def enum(v):
    return v.split('::', 1)[1] if isinstance(v, str) and '::' in v else v

def tag(t):
    return t.get('TagName') if isinstance(t, dict) else t

def objref(o):
    if not o: return None
    p = o.get('ObjectPath', '')
    return re.sub(r'\.\d+$', '', p) or o.get('ObjectName')

def curve(c):
    if not c or not c.get('CurveTable'): return None
    return {'table': objref(c['CurveTable']), 'row': c.get('RowName')}

def scalable(s):
    r = {'value': s.get('Value')}
    c = curve(s.get('Curve'))
    if c: r['curve'] = c
    reg = (s.get('RegistryType') or {}).get('Name')
    if reg and reg != 'None': r['registry_type'] = reg
    return r

EXPR = {1: 'AnyTagsMatch', 2: 'AllTagsMatch', 3: 'NoTagsMatch', 4: 'AnyExprMatch', 5: 'AllExprMatch', 6: 'NoExprMatch',
        7: 'AnyTagsExactMatch', 8: 'AllTagsExactMatch'}

def decode_query(q):
    """Decode FGameplayTagQuery token stream: [version, hasRoot, expr...]; expr = type, count, (tag idx | sub-expr)*count."""
    s, d = q.get('QueryTokenStream') or [], [tag(t) for t in q.get('TagDictionary') or []]
    if not s: return None
    pos = [2]
    def rd():
        v = s[pos[0]]; pos[0] += 1; return v
    def expr():
        t = rd(); n = rd(); name = EXPR.get(t, f'Expr{t}')
        if t in (1, 2, 3, 7, 8): return f"{name}({', '.join(d[rd()] for _ in range(n))})"
        return f"{name}({', '.join(expr() for _ in range(n))})"
    try:
        return expr() if len(s) > 1 and s[1] else None
    except Exception as e:
        return f'<undecoded: {e}>'

def reqs(r):
    if not r: return None
    out = {}
    if r.get('RequireTags'): out['require'] = r['RequireTags']
    if r.get('IgnoreTags'): out['ignore'] = r['IgnoreTags']
    q = r.get('TagQuery')
    if q and q.get('QueryTokenStream'):
        out['query'] = decode_query(q)
        if q.get('UserDescription'): out['query_description'] = q['UserDescription']
    return out or None

def modifier(m):
    mm = m.get('Modifier') or {}
    rec = {'attribute': tag(m.get('Attribute')), 'op': enum(m.get('Operation')), 'channel': enum(m.get('Channel'))}
    # FInstancedStruct type name is not emitted by CUE4Parse's JSON; kind is inferred from the (disjoint) property sets.
    if 'Scalar' in mm:
        rec['kind'] = 'Scalar'; rec.update(scalable(mm['Scalar'])); rec['curve_indexing'] = enum(mm.get('CurveIndexing'))
    elif 'BackingAttribute' in mm:
        rec['kind'] = 'Attribute'; rec['backing_attribute'] = tag(mm['BackingAttribute']); rec['attribute_mode'] = enum(mm.get('AttributeMode'))
        c = curve(mm.get('CurveTable'))
        if c: rec['curve'] = c
        rec['scale_by_duration'] = mm.get('bScaleByDuration'); rec['scale_duration_end'] = mm.get('ScaleDurationEnd')
    elif 'DataTag' in mm:
        rec['kind'] = 'SetByCaller'; rec['set_by_caller_tag'] = tag(mm['DataTag']); rec['coefficient'] = scalable(mm.get('Coefficient') or {})
        rec['allow_fallback'] = mm.get('bAllowFallback'); rec['fallback_value'] = mm.get('FallbackValue')
        rec['scale_by_duration'] = mm.get('bScaleByDuration'); rec['scale_duration_end'] = mm.get('ScaleDurationEnd')
    else:
        rec['kind'] = 'Unknown' if mm else 'None'; rec['raw'] = mm
    f = reqs(m.get('Filter'))
    if f: rec['filter'] = f
    return rec

records = []
for fpath in sorted(glob.glob(os.path.join(raw_dir, 'GE_*.json')), key=lambda p: os.path.basename(p).lower()):
    name = os.path.basename(fpath)[:-5]
    exports = json.load(open(fpath, encoding='utf-8'))
    cls = next(e for e in exports if e.get('Type') == 'BlueprintGeneratedClass')
    cdo = next(e for e in exports if e.get('Name', '').startswith('Default__'))
    P = cdo.get('Properties', {})
    rec = {
        'name': name, 'class': cls['Name'], 'package': cdo.get('Package'), 'pak_path': pak_paths.get(name),
        'parent_class': (cls.get('SuperStruct') or {}).get('ObjectName'),
        'serialized_properties': sorted(P.keys()),
        'duration': P.get('Duration'),
        'max_stacks': P.get('MaxStacks'),
        'stack_duration_refresh_policy': enum(P.get('StackDurationRefreshPolicy')),
        'stack_expiration_policy': enum(P.get('StackExpirationPolicy')),
        'modifiers': [modifier(m) for m in P.get('Modifiers', [])],
        'granted_tags': P.get('GrantedTags', []),
        'tags': P.get('Tags', []),
        'application_requirements': reqs(P.get('ApplicationRequirements')),
        'ongoing_requirements': reqs(P.get('OngoingRequirements')),
        'removal_requirements': reqs(P.get('RemovalRequirements')),
        'allow_client_predicted_application': P.get('bAllowClientPredictedApplication'),
        'allow_client_predicted_modification': P.get('bAllowClientPredictedModification'),
        'client_instigated_application_policy': enum(P.get('ClientInstigatedApplicationPolicy')),
        'client_instigated_modify_policy': enum(P.get('ClientInstigatedModifyPolicy')),
    }
    records.append(rec)

meta = {
    'source': 'Static CUE4Parse export of cooked GE_* BlueprintGeneratedClass CDOs (Default__GE_X_C), Wardogs UE 5.7 IoStore paks.',
    'count': len(records),
    'null_means': 'Property not serialized in the CDO = equals the native UBHGameplayEffect default (cooked unversioned delta vs. archetype). '
                  'Native default values are not in the paks; tracked fields are null rather than guessed.',
    'modifier_kind_note': 'kind inferred from FInstancedStruct property set: Scalar=FBHAttributeMod_Scalar, Attribute=FBHAttributeMod_Attribute, SetByCaller=FBHAttributeMod_SetByCaller.',
    'name_mapping_note': 'Obfuscated usmap names mapped by property index to sdk/raw BHGameplayEffects/BHGameplayTag/BHFramework SDK layouts; see ge_raw/_usmap_patches.txt.',
}
os.makedirs(out_dir, exist_ok=True)
json.dump({'meta': meta, 'effects': records}, open(os.path.join(out_dir, 'ge_summary.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)

# ---- markdown ----
OPS = {'Add': '+', 'Multiply': 'x', 'Divide': '/', 'MultiplyCompound': 'xc', 'AddFinal': '+f', 'Override': '='}
def short(t):
    return re.sub(r'^Attribute\.Gameplay\.', '', t or '?')
def num(v):
    return ('%g' % v) if isinstance(v, (int, float)) else str(v)
def curve_s(c):
    return f"{os.path.basename(c['table'] or '?')}[{c['row']}]"
def mod_s(m):
    op = OPS.get(m['op'], m['op'])
    if m['kind'] == 'Scalar':
        v = num(m['value'])
        if 'curve' in m: v = f"{v}*{curve_s(m['curve'])}@{m['curve_indexing']}"
        elif m.get('curve_indexing') not in (None, 'Fixed'): v += f"@{m['curve_indexing']}"
    elif m['kind'] == 'Attribute':
        v = f"attr({short(m['backing_attribute'])}.{m['attribute_mode']})"
        if 'curve' in m: v += f"->{curve_s(m['curve'])}"
    elif m['kind'] == 'SetByCaller':
        c = m['coefficient']; v = f"SBC({short(m['set_by_caller_tag'])})"
        if c.get('value') != 1.0 or 'curve' in c: v += f"*{num(c.get('value'))}"
        if 'curve' in c: v += f"*{curve_s(c['curve'])}"
        if m.get('allow_fallback'): v += f" fb {num(m['fallback_value'])}"
    else:
        v = '?'
    s = f"{short(m['attribute'])} {op} {v}"
    if m.get('channel') not in (None, 'Default'): s += f" [{m['channel']}]"
    if m.get('filter'): s += f" {{if {json.dumps(m['filter'], ensure_ascii=False)}}}"
    return s.replace('|', '\\|')

counts = collections.Counter(r['name'].split('_')[1] for r in records)
def group(n):
    p = n.split('_')[1]
    return f'GE_{p}_' if counts[p] >= 3 else 'GE_ (other)'
groups = collections.defaultdict(list)
for r in records: groups[group(r['name'])].append(r)
order = sorted(groups, key=lambda g: (g == 'GE_ (other)', -len(groups[g]), g))

L = ['# Wardogs Gameplay Effects (GE_*) - CDO summary', '',
     f'{len(records)} GE_* Blueprint assets, statically exported from the cooked paks (class default objects). '
     'Attribute names drop the `Attribute.Gameplay.` prefix. Ops: `+` Add, `x` Multiply, `/` Divide, `xc` MultiplyCompound, '
     '`+f` AddFinal, `=` Override. `@X` = curve indexing (Fixed omitted); `attr(A.Mode)->CT[row]` = FBHAttributeMod_Attribute; '
     '`SBC(tag) fb v` = SetByCaller with fallback. Duration blank = not serialized (native default, typically infinite/0 - unverified). '
     'Stacks shown only when serialized. Requirements are in ge_summary.json.', '',
     '| Group | Count |', '|---|---|'] + [f'| {g} | {len(groups[g])} |' for g in order] + ['']
for g in order:
    L += [f'## {g}', '', '| GE | Modifiers | Duration | Stacks | Granted tags |', '|---|---|---|---|---|']
    for r in groups[g]:
        mods = '<br>'.join(mod_s(m) for m in r['modifiers']) or '-'
        gt = '<br>'.join(r['granted_tags']) or ''
        L.append(f"| {r['name']} | {mods} | {num(r['duration']) if r['duration'] is not None else ''} | "
                 f"{r['max_stacks'] if r['max_stacks'] is not None else ''} | {gt} |")
    L.append('')
open(os.path.join(out_dir, 'ge_summary.md'), 'w', encoding='utf-8').write('\n'.join(L))
print(f'records={len(records)} modifiers={sum(len(r["modifiers"]) for r in records)} '
      f'kinds={dict(collections.Counter(m["kind"] for r in records for m in r["modifiers"]))} groups={len(order)}')
