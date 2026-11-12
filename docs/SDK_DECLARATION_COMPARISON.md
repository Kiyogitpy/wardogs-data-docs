# Supplied SDK declaration comparison (build unverified)

This note compares a supplied UEDumper SDK with the CL-516586-labelled Dumper-7 reference. The supplied SDK has not been independently tied to the exact Patch 03 executable. Treat this as a declaration comparison pending provenance review.

The supplied declarations expose ranged-bow item-extension and projectile-parameter validation types, projectile impact-cue helpers, and an active-reload mistake reporting function. Their presence does not establish live activation or damage or rate-of-fire values.

Compared with the reference, the supplied free-vehicle declarations include condition, selector, effect, rule and signal families. The old WDFreeVehicleRule identity is absent from these headers. This records a difference between generated declaration sets; spawn timing, selection and match policy require separate implementation or data evidence.

Progression-related identities present only in the supplied declarations include wager signal adapters and additional count and failure condition classes, vendor-discount and XP-modifier definitions, XP-boost UI data, reward contexts and freefall reward types. No reward amount, discount percentage or backend deployment is established.

The supplied BHWater headers declare BHWaterHeightGridAsset and BHWaterHeightSubsystem. The old WDGame water-grid identities are absent from the supplied headers. Exact identities differ; the comparison does not prove a rename, migration contract or compatible cooked serialization.

Header generators represent qualifiers, inheritance, enums, text and object references differently. Unmatched obfuscated member names and missing enum definitions remain unresolved. Reported memory layouts are not cooked schema slots, numeric balance data or native runtime proof. No runtime behavior or package-decoding result is claimed here.
