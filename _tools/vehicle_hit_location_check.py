"""Compare exported hit locations and compiler boundaries with a native receipt."""
import argparse,json
from pathlib import Path
import damage_tables as d

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--native',type=Path,required=True)
    args=parser.parse_args()
    native=json.loads(args.native.read_text(encoding='utf-8'))
    if not native.get('passed'):
        raise SystemExit('Native receipt did not pass')
    catalog=json.loads(Path(d.JSON_OUT).read_text(encoding='utf-8'))
    vehicles={vehicle['id']:vehicle for vehicle in catalog['vehicles']}
    assert len(native['catalog_cases'])==sum(len(v['slots']) for v in vehicles.values())
    for case in native['catalog_cases']:
        slot=vehicles[case['vehicle']]['slots'][case['slot_index']]
        assert (slot['group'],slot['slot'],slot['section'])==(case['group'],case['slot'],case['section'])
        assert (slot['hit_location'] or 'None')==case['result']['hit_location']
    original=d.exports
    boundaries=0
    try:
        for case in native['owned_cases']:
            # Runtime registration is outside the static export compiler's contract.
            if case['unregistered'] or len(case['sections'])!=1:
                continue
            owner={'Type':'ModularVehiclePlatform','Properties':{'Fragments':[{'Value':{'Fragment':{'ObjectName':"MVF_HealthSections'Owned:Health'"}}}]}}
            fragment={'Type':'MVF_HealthSections','Name':'Health','Properties':{'HealthSections':[{'Key':{'TagName':name},'Value':{'MaxHealth':100,'Tags':[tag or 'None' for tag in tags]}} for name,tags in case['sections'].items()]}}
            d.exports=lambda path:[owner,fragment]
            sections=d.sections(['owned'])
            assert len(sections)==1
            assert (next(iter(sections.values()))[1] or 'None')==case['result']['hit_location'],case['name']
            boundaries+=1
    finally:
        d.exports=original
    print(json.dumps(dict(passed=True,catalog_slots=len(native['catalog_cases']),compiler_boundaries=boundaries)))

if __name__=='__main__':
    main()
