"""Exact field associations for the CL516586 and direct CL533731 exports.

These apply only to WDArchetypeCaliberDamageModifierData rows and
WDInventoryFragment_Armor properties respectively, not to arbitrary structs.
"""


def _field(properties, names):
    present = [name for name in names if name in properties]
    if len(present) != 1:
        raise ValueError(f"Expected exactly one of {names}; found {present}")
    return properties[present[0]]


def caliber_modifiers(row):
    return _field(row, ("CaliberModifiers", "_aaabapbnbhiopifeenjml"))


def armor_damage_context(properties):
    return _field(properties, ("DamageContextTag", "_aaabapigngpcfjdppejoi"))
