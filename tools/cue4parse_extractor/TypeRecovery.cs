using CUE4Parse.MappingsProvider;
using CUE4Parse.MappingsProvider.Usmap;

static class TypeRecovery
{
    public static bool Complete(PropertyType type, TypeMappings mappings)
    {
        if (type == null || !Enum.TryParse<EPropertyType>(type.Type, out var kind) || kind == EPropertyType.Unknown) return false;
        if (kind == EPropertyType.StructProperty && (type.StructType == null || !mappings.Types.ContainsKey(type.StructType))) return false;
        if (kind == EPropertyType.EnumProperty && (type.EnumName == null || !mappings.Enums.ContainsKey(type.EnumName))) return false;
        if (kind is EPropertyType.ArrayProperty or EPropertyType.SetProperty or EPropertyType.OptionalProperty or EPropertyType.EnumProperty)
            return Complete(type.InnerType, mappings);
        if (kind == EPropertyType.MapProperty) return Complete(type.InnerType, mappings) && Complete(type.ValueType, mappings);
        return true;
    }

    public static bool CompatibleKnown(PropertyType existing, PropertyType recovered)
    {
        if (existing == null || recovered == null) return existing == null && recovered == null;
        if (existing.Type == "Unknown") return true;
        return existing.Type == recovered.Type && existing.StructType == recovered.StructType
            && existing.EnumName == recovered.EnumName
            && CompatibleKnown(existing.InnerType, recovered.InnerType)
            && CompatibleKnown(existing.ValueType, recovered.ValueType);
    }

    public static string Describe(PropertyType type) => type.Type
        + (type.StructType == null ? "" : ":" + type.StructType)
        + (type.EnumName == null ? "" : ":" + type.EnumName)
        + (type.InnerType == null ? "" : "<" + Describe(type.InnerType) + ">")
        + (type.ValueType == null ? "" : "[" + Describe(type.ValueType) + "]");
}
