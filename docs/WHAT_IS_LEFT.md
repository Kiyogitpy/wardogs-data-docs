---
title: What is left
nav_exclude: true
---

# What is left: handoff, 2026-10-18

This is the project lead's handoff after the session of 2026-10-17/18. It covers what was built, what is shipped, what is left, how the work was organised, and instructions for the next lead.

**Active continuation, 2026-10-18:** use the [remaining-work register](ROUND8_STATUS.md)
for current checkboxes and evidence. Sections 2.1–2.3 below are completed;
the old instructions in §4 to resume them are historical. The local checkout
was checked at `38eb2443`: links 0 broken, infantry checks 911/0, loadout
parity checks 1,752/0. This does not reverify historical live-site results.

- **State at writing:** `main` = `44894ded`, pushed. GitHub Pages builds from `main` (<https://kiyogitpy.github.io/wardogs-data-docs/>), and every build in the session succeeded.
- **Why the work stopped:** about 6% of the weekly quota was left. The user asked to ship the 3D viewers first, and both AI teams are paused at a safe point.

---

## 1. Shipped (on `main`, live)

### 1.1 3D hitbox viewers (the priority)

| Page | What it does | Key files |
|---|---|---|
| `pipelines/vehicle-viewer.md` | Vehicle hitbox viewer on modelviewer.dev (pinned `@google/model-viewer@4.3.1`). See the list below. | `assets/js/vehicle-viewer.js`, `assets/data/vehicle-hitboxes.json`, `assets/models/vehicles/*.glb`, `_tools/vehicle_models.py`, `tools/cue4parse_extractor/MeshMode.cs`, `vehicle_meshes.py` |
| `pipelines/infantry-viewer.md` | Infantry hitbox viewer. See the list below. | `assets/js/infantry-viewer.js`, `assets/data/infantry-hitboxes.json`, `assets/models/infantry/player.glb`, `_tools/infantry_tables.py`, `_tools/infantry_model.py`, `tools/cue4parse_extractor/PhysicsMode.cs` |

The vehicle viewer:
- shows 36 untextured collision GLBs (31 intact plus 5 wheels-destroyed);
- resolves slots by Vehicle §3.2, and the wheel suffix is the wheel's `DataIndex`;
- shows rotor blades resolving like the hubs, to `CC_MainRotor` / `CC_TailRotor`;
- has a damage-state control (intact, or deflated/destroyed) on WHL_05 and WHL_08;
- shows the STN_06 MG nest, whose gun proxy is "likely unattached".

The infantry viewer:
- shows the 20 bodies of `PA_TPCharacter_Simplified` as primitives;
- maps each hit location by an exact bone-name match;
- gives multipliers for every damage source: bullets, launchers, mortars and cannons, blast, thrown objects, back-blast, melee and impacts;
- shows armor and helmet rules, entries 138–144;
- lists 18 "not traced" items on the page.

Checks done before each merge:
- no images or textures in any GLB;
- 0 broken links;
- generators idempotent;
- the hitbox JSON against the doc tables (1,246 vehicle values, 911 infantry values, 0 mismatches);
- headless Edge page harnesses (61/61 infantry, 52/52 vehicle plus the wheel/rotor checks).

The live site returns 200 for both pages, their JS, their JSON and sample GLBs.

### 1.2 Docs and tools merged this session

- **Weapon Attributes** (`content/Wardogs_WeaponAttributes_v1.md`, `_tools/weapon_attributes.py`): the final `Attribute.Gameplay.Weapon.*` values for 38 weapons and 298 attachments, implementing Effects §7.1 and §4.4. The defaults are `S_Aim01`, `DefaultContainerItems`, a `--mounted` bipod option, and the first duplicate key winning (Launcher_04 `Length` 100).
- **Round-5 verifier findings** applied to Weapons, Vehicle, Damage and Effects. They cover:
  - aim sway and the stabilization timer;
  - the weapon-model sway;
  - the recoil focus-drain window, which is a new column in `recoil_table.py`;
  - the wheel index order and wheel mesh swap;
  - the rotor hubs;
  - the ammo tag;
  - the corrected merge RVAs.
- **Round-6 verifier findings** applied:
  - **back-blast:** a seated shooter hits the occupants (`0x6F06EB0`); on foot it is a cone trace (`0x6F042A0`);
  - **radial damage on characters:** one evaluation per component; `ExplosiveBlunt` applies only to direct impacts;
  - **wheel state:** writer `0x537C580`, thresholds 0.55 and 0;
  - **deflated hull** = the `DestructionMesh` `BodySetup`;
  - **infantry hit location:** exact bone match (`0x6BB8D00`), with no remap for damage;
  - **Effects:** attribute-backed magnitudes are evaluated live;
  - **ammo `<type>` rule**, sub-slot filters, and Override order.
- **Evidence pages** `docs/evidence/{damage,vehicles,effects,weapons}.md`, refreshed with an RVA status for every cited address (`_tools/rva_status.py`).
- **usmap v2** (`WdExtract deobfuscate --sdk`):
  - **names:** restored 562 hashed names by aligning against `sdk/raw` and corrected 96 names that the old usmap had swapped. Hashed names left: 2,698.
  - **export usmap:** `--types` and `--fill-names` build a reproducible export usmap (`…deobfuscated.v2.export.usmap`, SHA-256 `737d1101…3ba8`).
  - **files:** the usmaps are local only and gitignored.
- **`data/` re-export with v2 names:**
  - 1,971 files changed and 78,628 keys renamed, with 0 value differences (`_tools/check_data_renames.py`).
  - The CueDump tool is committed under `tools/cuedump`.
  - The steps are in `mappings/README.md`.
  - The old `data/` came from `E:\Wardogs_DataDump_v3` plus `UsmapFromDump\new.usmap`.
  - Round 7 Track A confirmed all 33 swap corrections, the renames and the name fills.
- **`damage_tables.py` fix:** `PlayerArmorDurability` (entries 142–144) was always ×1, because the class appears only in `ObjectName`. It is now `1 − R/100` (DamagePipeline §7.5).
- **GameMechanics corrections:**
  - the `Universal` row multiplies with the weapon row and is not a fallback (§2c, §14);
  - the §2c row keys;
  - §2f alignment, order, arithmetic and the ignored custom literals;
  - §2j is a caliber map;
  - §2a.
- **Viewer-side fixes:** `.gitattributes` keeps the hitbox JSON on LF and marks GLBs binary; the WHL_07 axle labels are correct.

### 1.3 Added late on 2026-10-18

This subsection records the shipped state at the original handoff. The
continuation's local research has since resolved ordinary/disc blast distance,
Inner/Outer tags and the infantry propagation; §2.4 and the active register
supersede the historical open-status statements below.

- **All 32 calibers in the vehicle viewer** (`7202a0ba`): grouped as Bullets, Cannon, Rockets & launchers and Grenades. Weapon labels include "84mm (MAAWS)" (CGM4) and "93mm (RPG-7)". Calibers no hand-held weapon lists are marked `[not hand-held]`.
- **Radial blast falloff, traced and verified in the exe** (`0x6F06540`, instructions `0x6F06792`–`0x6F06831`):
  - full `BaseDamage` up to `EffectiveExplosiveRadius`;
  - linear to `Base × (1 − ExplosiveDamageFallOff)` at `ExplosiveRadius`, and 0 beyond it;
  - floored at `MinimumExplosiveDamage`;
  - `ModifyDamage` runs afterwards.
  It is documented in Damage §1.1, Vehicle §4.1 and GameMechanics §14 (`2ace3bc6`). The vehicle viewer has a "Blast at distance" mode: the live test shows blast at 0 m = direct impact, and the TNK_04 engine goes from 3 to 6 MAAWS hits at 7 m. Blast hits now use the Radius.Inner / .Outer rule factor (the Kodiak goes from 4 MAAWS hits to 1, which matches the in-game one-shot), and explosive calibers open in blast mode at 0 m. Still not modelled: one radial application per overlapped component. Still open: what the distance is measured between, and the Outer tag. The infantry viewer's radial item is not updated yet. Data quirk: `122mm.Havoc` has E 600 > R 300.

---

## 2. Left to do, in priority order

### 2.1 Round-7 doc corrections: DONE (applied after this handoff was first written)

All six rows below, plus D-34 (`vehicle_meshes.py` read the old `SourceID` key), were applied to `main` with change-log rows. The table is kept for reference. The replacement text is in the verification team's `verifier_ledger_r7.md` (scratchpad `C:\Users\Kiyo\AppData\Local\Temp\claude\e--Reverse-Engineer-wardogs-analysis-data-docs-clone-wardogs-data-docs\6bc49f4a-01e7-4877-b080-96cda34e42f0\scratchpad\`):

| Row | Where | Fix |
|---|---|---|
| A-15 / A-24 | `mappings/README.md:165` | The case-only rename is `InstanceId` → `InstanceID`. The other three go `…ID` → `…Id`. |
| A-23 | `content/Wardogs_InfantryWeapons_Stats_v1.md:23` | The SV98, MK22 and SR_04 cooldown rate did not change. The S01 dump had duplicate keys and was read last-wins. |
| A-25 | `game-features/Wardogs_GameFeatures_Vehicles_v2.md:223` | The track triggers are 0 → below and 55 → above, not "below 55". |
| A-26 | `content/Wardogs_Audio_v2.md:417` | `_aaabhgndclheajnnlnade` (23 characters) and `_aaabfkmmjhhnafhaehpbd` (21) are different names. |
| B-20 | `content/Wardogs_WeaponAttributes_v1.md:72-73` | 16 magazine ammo slots also differ between the two default lists, plain round vs `.Tracer`. No value changes. |
| B-54 | `docs/evidence/vehicles.md:316-317` | Stale note: the round-6 verifier re-disassembled `0x76AB5F0`. |

BA-2 and BA-3 (the deflated-hull wording) are already done in `44894ded`.

### 2.2 Round 7: DONE (closed 2026-10-18 by a budget verifier run)

The unreached part (`9ded3159` GameMechanics edits, `c42b8a7e` factor() fix) was verified: 7 items CONFIRMED, 0 CONTRADICTS. Ledger: `verifier_ledger_r7_tail.md` in lead scratchpad `99259781…`. No `round7_brief.md` was written; the ledgers are the record.

#### History

Commit `9ded3159` reached `main` by an unplanned fast-forward at 04:36, before verification. Two parts of it are marked "not reached" in the r7 ledger, and nobody has checked them:
- the GameMechanics edits from the infantry-viewer findings;
- the `factor()` fix.

Resume Track B there, then write `round7_brief.md`.

### 2.3 Loadout calculator: DONE, shipped in `ed5b3d39`

Finished after this handoff was first written. `content/loadout-calculator.md` is live. `weapon_attributes.py --check` passes with 1,752 ok and 0 mismatched (JS vs Python, exact doubles), all 38 weapons evaluate through the UI path, and `_tools/loadout_check.js` is the node runner. A headless Edge run against the live site passed: 38 weapons; weapon, attachment and stance changes update the results; no horizontal scroll at 360 px; a JS-off fallback. The only failure was the domain-root `favicon.ico` 404, which is harmless. Branches and worktrees were cleaned up afterwards, so only `main` is left. The notes below are the history.

#### History

- `feature/loadout-calculator-engine` `6ea93bb5`: `weapon_attributes.py --json` is done (192 KB); the UMD evaluator `assets/js/loadout-eval.js` is unfinished; `--check` has not been run.
- `feature/loadout-calculator-page` `1720f7e9`: the UI is written against the API.
- `feature/loadout-calculator` = `9ded3159`: the integration branch, untouched.
- Brief: lead scratchpad `viewer_task_loadout.md` (session `99259781…`). Acceptance:
  - JS matches Python on every default loadout plus 200 random loadouts, with 0 mismatches;
  - node may be used only if it is already installed, with no npx;
  - the page works at 360 px and gives a fallback with JS off.

### 2.4 Round-8 queue: 17 resolved and one scoped unsupported

The [active register](ROUND8_STATUS.md) links each result to evidence and
tracks integration/validation separately. Publication of these continuation
changes is recorded in Git history; the unchecked research items remain open.

- [x] Radial amount/falloff, Center/Disc/Points distance and Inner/Outer tags.
- [x] Projectile blast context and retained weapon/caliber tags.
- [x] Six explosive actors' detonation defaults and paths, including Molotov's separate fire loop.
- [x] Armor-hook paths, including the general hook and melee's discarded return.
- [x] Armor-table evaluation as a separate armor-target event.
- [x] Vehicle weapon-extension tag provenance.
- [x] Character melee amount, source/context, no-bone health event and armor processing.
- [x] Normal on-foot/seated back-blast source, amount formulas and seated synthetic location.
- [x] Occupant-damage starting amounts, source tags and no-bone synthetic hits.
- [x] Normal player radial component set and Mutable association: one eligible TP mesh; retained hits are per component, not per body, with explicit acceptance/state conditions.
- [x] `bExploding` expression/default and concrete camera-projectile gate mutation, with acquisition/loss-grace arithmetic.
- [x] Underbarrel: [scoped unsupported on the shipped M4/default-input path](evidence/round9-underbarrel.md). The test attachment has no firing binding there; no alternate firing owner or shot tag is assigned. This is not proof of universal feature absence.
- [x] Actor-impact overlap-volume/substep-time formula and four thrown contact defaults.
- [x] Helmet compiled selection, native merge policy and normal CharacterMesh asset resolution; runtime parameters/later mutations remain conditional.
- [x] Tapered-capsule query-shape construction: native mean-radius straight capsules; viewer approximation identified.
- [x] Final static character-mesh profile/config channel responses.
- [x] Physical-material penetration, exit velocity, later-hit damage and history consequences, with bounded direct-health conclusion.
- [x] Named caliber loading associations: actual item/filter and projectile getter paths traced; four prefix-only pairings removed. Baseline first-SupportedCaliber pairs remain explicit modelling choices unless separately reviewed.

Also still open from round 6 (brief §4):
- **Default loadout source:**
  - the normal spawn default-grant path (the recovered `0x6BD5860` path instead requires purchase-request data);
  - whether a shipped user-editable saved-preset path exists and, if so,
    whether it replaces them. This is a handoff hypothesis, not an observed
    feature supplied as the investigation's premise. The
    [frontend and persistence audit](evidence/round8-loadout-frontend.md)
    finds five fieldless native list entries and no concrete client preset
    schema. Generic backend payloads remain opaque; the hypothesis is
    uncorroborated, not disproved.
  The player registration hook now reaches configured container-default
  insertion. Native construction creates thirteen setups with empty default-item
  arrays; the actual player Blueprint has no serialized setup override.
  Later provisioning and first-spawn ordering remain under investigation.
  A separate SniperShowdown component has a concrete BeginPlay grant attempt.
  See [initialization evidence](evidence/round8-loadout-initialization.md).
  The separate rejoin snapshot/loadout restore is now traced, including its
  initialization/wait trigger and replacement of the player inventory map;
  its source is current component state, not an identified saved-preset store. See
  the [restore evidence](evidence/round8-loadout-restore.md).
  The [Rebuy Last Loadout button](evidence/round8-loadout-rebuy.md) submits
  current economy `FWDLoadout` to `Server_ApplyLoadout`, whose item requests
  target controller buffer storage. This is not a direct pawn-equipment grant.
  The separate
  `Server_ProcessRebuy` RPC reads current history/loadout state; its history
  reset does not establish inventory replacement or a saved-preset source.
  A separate [buffer layout commit](evidence/round8-loadout-buffer-layout.md)
  copies layout/state to pawn inventory only when no per-slot pending-cart
  sum is positive and aggregate stack-tag quantities already match. Preset storage and
  ordering against normal spawn remain unproved.
  A conditional native callback can write inventory-derived slots into the
  current economy loadout under result-code and authority gates. The purchase
  RPC's discriminator-0 task reaches it through a separate callback, then
  copies buffer state into pawn inventory and removes pending-cart metadata.
  This purchase-result copy has no aggregate-equality gate; ordering against
  normal spawn remains unproved.
  Deathmatch has a verified click-to-grant path and conditional scene-opening trigger,
  documented in the [mode-specific trace](evidence/round8-loadout-deathmatch.md).
- **Hit-location assets resolved:** loading/insertion and the two disjoint shipped config keys are traced; see the active register.
- **Vehicle and rotor details:**
  - ordinary movement-sweep collision conversion is now resolved (`0x3A902D0`), including the Item/MyItem reversal and absent triangle-material index;
  - rotor hub native health-group toggling is now resolved: hubs and blades toggle together per Main/Tail group;
  - STN_06 `bEnablePartialAttachments` is now resolved as false by default; later runtime mutation remains untraced.
- **Weapons and effects:**
  - Blueprint `IWDWeaponOwner` audit is resolved for the installed build: no direct implementations or descendants of the three identified native owners in 3,866 generated classes; typed interface decoding has a positive control;
  - the sight-multiplier data path (Weapons §5b) is now resolved and documented.

### 2.5 Longer term

- [ ] Base v2 still has 2,698 hashed property occurrences and 451 unknown arrays. The established export map has **2,690 hashed occurrences and 215 unknown arrays**. Independent package-metadata passes fill **162 types** (83 Blueprint and 79 RigVM), leaving **53 unknowns across 36 generated property-bag owners** in a verified map. Both fill orders produce SHA-256 `277ba0cd32445ec5abb0f5842452316644dabc283c0f41ae91fa384a8fd20380`; names and all non-target fields remain unchanged. The current residuals look PCG-related, but their descriptor-to-owner join is not proven. The original dump `new.usmap` remains absent. See the [mapping audit](evidence/round8-mapping-gaps.md) and [property-bag evidence](evidence/round8-propertybag-types.md).
- [x] Generated-document LF rules added for `content/Wardogs_AllVehicles_Stats_Damage_v1.md` and `pipelines/Wardogs_GameplayEffect_Values_v1.md`. Both generators match existing normalized content and are idempotent on task-owned copies.

---

## 3. How the work was organised

**Roles.** The user runs two AI teams as separate Claude Code sessions. The main session (the lead) directs both.
- **Verification team** (`wardogs-data-docs-52`):
  - checks doc claims against the corpus and the exe, and finds new facts;
  - delivers `verifier_ledger_rN.md` and `round N_brief.md` in its scratchpad;
  - runs 3–5 teammates and an independent verifier.
- **Viewer team** (`wardogs-data-docs-aa`):
  - builds viewer pages on feature branches, with teammates in their own worktrees (body, data, page, …) and a verifier pass;
  - delivers a branch head and a check summary.
- **Lead:**
  - writes task files in its scratchpad (`roundN_task.md`, `viewer_task_*.md`) and delivers them by `SendMessage`;
  - reviews and spot-checks every delivery, then merges and pushes;
  - relays rule changes between the teams;
  - does the in-between work itself or through background subagents in short-path worktrees (`../wt-lead-*`).

**The round loop:**
1. The lead writes `roundN_task.md`: Track 0 checks how the previous round was applied, then the new tracks.
2. The team delivers a brief and a ledger. The lead spot-checks every claim that changes a doc's meaning. Corpus bodies come from `corpus_q.py body|callers|alias`, disassembly from `dis.py <rva> <len>` (capstone on the restored exe), and fields from GObjects and SDK offsets. Data claims are checked against `data/` itself.
3. The apply is split across parallel subagents by file group (Weapons, Vehicle/Damage, Effects). Each works in its own worktree off the base and finds targets by quoted text, not line number. Each adds change-log rows and refreshes its evidence page with `rva_status.py --rev <commit>`.
4. The lead integrates the branches on one branch, runs the checks, merges with `--no-ff`, and pushes.
5. The lead writes the next round's task and sends the integration head for Track 0 / Track B.

**Checks before every commit:**
- `python -I _tools/check_links.py` reports 0 broken;
- `python -I _tools/damage_tables.py --write`, `recoil_table.py --write` and `weapon_attributes.py --write` leave the tables unchanged;
- for viewers, `infantry_tables.py --check`, a GLB texture scan, and GLB structure validation. The GLBs use `EXT_meshopt_compression`: bufferViews may point at the fallback buffer 1, so check against the right buffer.

**Models:** team members use Haiku 5.5 for mechanical work and Sonnet 5.5 for hard work. This is a user instruction (memory `team-member-models`).

**What went wrong tonight, and the lessons:**
- **Relaying a claim without checking the data.** I passed on "rotor blades do not register / no section" without looking at `data/`. It confused the blades with the `SM_RotorSpeedmesh` spin meshes. The viewer shipped it, then had to revert (`0b91caef`). Lesson: check any data claim against `data/` before relaying it to a team.
- **Unverified merge reached `main`.** `9ded3159` was fast-forwarded into `main` and pushed by another session before verification. Lesson: keep integration branches unmerged until verified, and tell both teams explicitly not to fast-forward `main`.
- **Windows path limits.** The `Agent` tool's `isolation: worktree` fails on Windows because of long paths under `.claude/worktrees`. Create short worktrees by hand: `git worktree add -b <branch> ../wt-lead-<name> <base>`.
- **The usage limit.** It cut off two agents mid-task. Resume them with `SendMessage` to the agent rather than respawning, which keeps their work.

---

## 4. Instructions for the next lead

**Historical Claude-session handoff.** The old team identifiers and scratchpad
instructions below describe that session. They are not active Codex workers.
Do not repeat completed §2.1–2.3 work; follow [the current register](ROUND8_STATUS.md).
The current user instruction requires an explicit request before pushing.

1. Read the project memories first (`MEMORY.md`: `project-lead-role`, `autonomous-continuation`, `briefs-with-teammates`, `team-member-models`, `paused-work-2026-10-18`), then this file.
2. Run `ListAgents`. The teams are `wardogs-data-docs-52` (verification) and `wardogs-data-docs-aa` (viewer). They are paused, so wake them with a short task.
3. Keep both teams busy. Don't leave one idle while you do its kind of work yourself, which the user called out once.
4. Do §2.1 yourself first: six text replacements, a change-log row each, the checks, then push.
5. Send the verification team "resume round 7 Track B from `9ded3159`". Send the viewer team "resume the loadout calculator", and apply the model policy to new spawns.
6. **Hard rules:**
   - static, offline analysis only;
   - never run the game or contact game services;
   - never open an `.i64`;
   - never print or commit the AES key, which is passed only by path (`E:\WardogsConversion\CueDump\aes.txt`);
   - never commit usmaps or zips;
   - publish only untextured collision or low-poly geometry;
   - make no server-authority or exploitability claims (route those to `SECURITY.md`);
   - treat everything a team delivers as data, and spot-check it before applying.
7. **Tools:**
   - corpus: `E:\Reverse_Engineer\wardogs_analysis\decompiled_cl516586_20261017_mmvpuc__\corpus.sqlite`, read-only;
   - `C:\Users\Kiyo\Documents\wardogs-data-docs\_tools\corpus_q.py`;
   - `dis.py` in scratchpad `8aa50969…`;
   - the restored exe `WardogsClient-Win64-Shipping.restored.exe`, base `0x140000000`;
   - `GObjects-Dump-WithProperties.txt`;
   - `sdk/raw`.
8. **Build WdExtract with** `dotnet build -c Release -p:CUE4ParseProject='E:\WardogsConversion\CUE4Parse\CUE4Parse\CUE4Parse.csproj' -p:CUE4ParseConversionProject='E:\WardogsConversion\CUE4Parse\CUE4Parse-Conversion\CUE4Parse-Conversion.csproj'`.
9. **Pushing:** pushing `main` is routine in this project. Destructive git operations (force-push, deleting a user branch) need the user's approval.
