---
title: "Weapon and ammo: hit location (template)"
parent: "Balance Notes"
date: 2026-10-15
note:
  seasons: "Season 1 → Season 2"
  status: "Calculated, not live-tested"
  tone: down
  figure: "−10.0%"
  figure_label: "Placeholder: the headline change, e.g. damage before armour"
  lede: "Placeholder lede. One sentence on what changed and what offsets it."
  subject: ["Weapon", "Ammo type", "Calibre", "Hit location"]
  assumptions: ["Hit location", "No range falloff", "100 HP", "Fresh armour"]
  compare:
    hp: 100
    from: "Season 1"
    to: "Season 2"
    label: "Armour"
    rows:
      - { label: "No armour", from: "30.00", to: "27.00" }
      - { label: "Tier 1", from: "21.00", to: "18.90" }
      - { label: "Tier 2", from: "18.00", to: "16.20" }
      - { label: "Tier 3", from: "13.50", to: "13.50" }
      - { label: "Tier 4", from: "10.50", to: "10.80" }
  formulas:
    - label: "Unarmoured, Season 2"
      terms:
        - { value: "30", label: "Base damage" }
        - { value: "1.0", label: "Location multiplier" }
        - { value: "0.9", was: "1.0", label: "Archetype multiplier" }
        - { value: "1.0", label: "New modifier", new: true }
      result: "27.00"
      result_label: "Damage per bullet"
      was_result: "30.00"
---

{% include note-head.html %}

> **Template.** Every number on this page is a placeholder that shows the layout. Copy this file to start a new note; see [Adding a note](balance-notes.html#adding-a-note).
{: .wd-note-placeholder }

## Damage per bullet

{% include note-compare.html %}

One or two sentences reading the table: which rows move, and which breakpoints change.

## The maths

{% include note-formula.html %}

Explain each multiplier and link the table it comes from on the data pages, e.g. [Bone Damage Multipliers](Wardogs_GameMechanics_v2.html#2c-bone-damage-multipliers-dt_infantrydata_bonedamagemodifiers).

## Bottom line

> Placeholder. The one thing a player should take away, and the limits of the model: what changes once armour degrades or shots land elsewhere.
{: .wd-bottomline }

Precision notes go here, e.g. where measured in-game values differ slightly from the raw-data calculation.
