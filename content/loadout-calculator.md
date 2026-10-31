---
title: "Weapon Loadout Calculator"
redirect_from: ["/loadout-calculator.html", "/loadout-calculator"]
parent: "Interactive Tools"
description: "Find the best compatible attachment builds for vertical, horizontal and overall recoil at your class level, compare the trade-offs, and apply a build or inspect every weapon attribute."
---

# Weapon Loadout Calculator

*Data: [`assets/data/weapon-loadouts.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-loadouts.json), built by `python _tools/weapon_attributes.py --json`; class levels, reticles and ballistics from [`assets/data/loadout-extras.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/loadout-extras.json), built by `python -I _tools/loadout_extras.py`*

Pick your weapon and progression below. Compare **best vertical**, **best horizontal** and **best overall recoil**, then apply the build you want. Recommendations search compatible attachment combinations, including the sub-slots opened by barrels and handguards. Your optic, stance and bipod setting stay yours.

The manual editor and full attribute breakdown remain below. Values follow [Weapon Attributes](Wardogs_WeaponAttributes_v1.md#rules) and the [Gameplay Effects Pipeline](../pipelines/Wardogs_GameplayEffectsPipeline_v1.md#44-current-value) §4.4; these are recoil multipliers, not a prediction of hit rate.

<div class="vv lc" id="lc" markdown="0" data-json="{{ '/assets/data/weapon-loadouts.json' | relative_url }}?v={{ site.time | date: '%s' }}" data-extras="{{ '/assets/data/loadout-extras.json' | relative_url }}?v={{ site.time | date: '%s' }}" data-base="{{ '/' | relative_url }}" data-optimizer-worker="{{ '/assets/js/loadout-optimize-worker.js' | relative_url }}?v={{ site.time | date: '%s' }}">
  <div class="vv-controls lc-controls">
    <div class="vv-field lc-field-weapon">
      <label for="lc-weapon">Weapon</label>
      <select id="lc-weapon" disabled><option>Loading weapons…</option></select>
    </div>
    <div class="vv-field lc-field-gate">
      <label for="lc-role">Class</label>
      <select id="lc-role" disabled><option value="">Any class</option></select>
    </div>
    <div class="vv-field lc-field-gate lc-field-level">
      <label for="lc-level">Class level</label>
      <input type="number" id="lc-level" min="1" max="150" step="1" inputmode="numeric" placeholder="No limit" disabled>
    </div>
    <div class="lc-actions">
      <button type="button" class="lc-btn" id="lc-reset" disabled>Reset to default loadout</button>
    </div>
  </div>
  <p class="lc-status" id="lc-status" role="status"></p>
  <p class="lc-hint lc-gate-hint" id="lc-gate-hint" aria-live="polite"></p>
  <section class="lc-card lc-recommendations" id="lc-recommendations" aria-labelledby="lc-recommendations-title" aria-busy="true">
    <h2 class="lc-card-title no_anchor" id="lc-recommendations-title">Choose your recoil build</h2>
    <p class="lc-card-lead" id="lc-recommendation-status" role="status">Loading recoil recommendations…</p>
    <div class="lc-recoil-current" id="lc-recoil-current"></div>
    <div class="lc-recoil-compare" id="lc-recoil-compare"></div>
    <details class="lc-scoring">
      <summary>How the builds are ranked</summary>
      <p>Lower is better. Vertical minimizes the final vertical recoil multiplier, breaking ties with horizontal. Horizontal does the reverse. Overall minimizes the equal-weight RMS of both multipliers relative to the default loadout at the same stance and bipod setting: √(((V / default V)² + (H / default H)²) / 2). This penalizes a large weakness on either axis; ADS time, spread, price and magazine capacity do not affect this score.</p>
      <p>Each build uses the same weapon, optic, sight entry, stance and bipod setting; bipod bonuses apply only if a bipod is equipped in that build. Default-fitted mechanical parts are not stripped. Unlocked parts can replace them; empty is considered for optional slots. Items absent from the unlock trees are treated as available, as in the manual editor. Ties prefer fewer equipment changes. Percentage changes compare with the default loadout in the same stance, not with bare weapon stats. This is attachment optimization for recoil multipliers, not the weapon's physical spray pattern or a guarantee of the best handling. Explicit zero-recoil overrides are excluded from recommendations because they erase every attachment trade-off; their exported effects are still shown unchanged in the manual editor.</p>
    </details>
  </section>
  <div class="lc-layout">
    <section class="lc-card lc-loadout" aria-labelledby="lc-loadout-title">
      <h2 class="lc-card-title no_anchor" id="lc-loadout-title">Manual loadout editor</h2>
      <p class="lc-card-lead">Each sub-slot lists the attachments it accepts. A barrel or handguard brings its own sub-slots, which open below it.</p>
      <div class="lc-slots" id="lc-slots"></div>
      <div class="lc-mods">
        <div class="vv-field lc-field-sight">
          <label for="lc-sight">Sight entry</label>
          <select id="lc-sight" disabled></select>
          <p class="lc-hint" id="lc-sight-hint"></p>
        </div>
        <div class="vv-field">
          <span class="vv-label" id="lc-stance-label">Stance</span>
          <div class="wd-segmented lc-seg" id="lc-stance" role="radiogroup" aria-labelledby="lc-stance-label">
            <button type="button" role="radio" value="Stand" aria-checked="true">Stand</button>
            <button type="button" role="radio" value="Crouch" aria-checked="false" tabindex="-1">Crouch</button>
            <button type="button" role="radio" value="Prone" aria-checked="false" tabindex="-1">Prone</button>
          </div>
        </div>
        <div class="vv-field">
          <span class="vv-label" id="lc-bipod-label">Bipod</span>
          <div class="wd-segmented lc-seg" id="lc-bipod" role="radiogroup" aria-labelledby="lc-bipod-label" aria-describedby="lc-bipod-hint">
            <button type="button" role="radio" value="folded" aria-checked="true">Folded</button>
            <button type="button" role="radio" value="unfolded" aria-checked="false" tabindex="-1">Unfolded</button>
            <button type="button" role="radio" value="mounted" aria-checked="false" tabindex="-1">Mounted</button>
          </div>
          <p class="lc-hint" id="lc-bipod-hint"></p>
        </div>
      </div>
    </section>
    <section class="lc-card lc-results" aria-labelledby="lc-results-title">
      <h2 class="lc-card-title no_anchor" id="lc-results-title">Weapon attributes</h2>
      <p class="lc-card-lead" id="lc-summary" aria-live="polite"></p>
      <div class="lc-table-wrap">
        <table class="lc-table" id="lc-table">
          <caption class="lc-sr">Each weapon attribute's base value, the modifiers that reach it and its final value</caption>
          <thead><tr><th scope="col">Attribute</th><th scope="col" class="lc-num">Base</th><th scope="col">Modifiers</th><th scope="col" class="lc-num">Final</th></tr></thead>
          <tbody id="lc-rows"></tbody>
        </table>
      </div>
      <p class="lc-legend">Operations: <code>+</code> Add, <code>×</code> Multiply, <code>÷</code> Divide, <code>×c</code> MultiplyCompound, <code>+f</code> AddFinal, <code>=</code> Override. A changed value is <span class="lc-changed-key">highlighted</span>; values are rounded to six significant digits (hover a value for full precision).</p>
    </section>
  </div>
  <section class="lc-card lc-optics" id="lc-optics-card" aria-labelledby="lc-optics-title" hidden>
    <h2 class="lc-card-title no_anchor" id="lc-optics-title">Sight and reticle</h2>
    <div class="lc-optics" id="lc-optics"></div>
  </section>
  <section class="lc-card lc-ballistics" id="lc-ballistics-card" aria-labelledby="lc-ballistics-title" hidden>
    <h2 class="lc-card-title no_anchor" id="lc-ballistics-title">Ammunition, body-part damage and drop-off</h2>
    <div class="vv-controls lc-bal-controls">
      <div class="vv-field"><label for="lc-ammo">Ammunition</label><select id="lc-ammo"></select></div>
      <div class="vv-field"><label for="lc-vest">Target vest</label><select id="lc-vest"></select></div>
      <div class="vv-field"><label for="lc-helmet">Target helmet</label><select id="lc-helmet"></select></div>
      <div class="vv-field"><label for="lc-range">Distance</label><select id="lc-range"></select></div>
    </div>
    <p class="lc-card-lead" id="lc-bal-summary" aria-live="polite"></p>
    <div class="lc-scroll" tabindex="0" role="region" aria-labelledby="lc-parts-cap">
      <table class="lc-btable" id="lc-parts">
        <caption class="lc-sr" id="lc-parts-cap">Damage per shot, shots to kill and time to kill for each body part at the chosen distance</caption>
        <thead><tr><th scope="col">Body part</th><th scope="col">Armor</th><th scope="col" class="lc-num">Damage per shot</th><th scope="col" class="lc-num">Shots to kill</th><th scope="col" class="lc-num">Time to kill</th></tr></thead>
        <tbody id="lc-parts-rows"></tbody>
      </table>
    </div>
    <h3 class="lc-sub no_anchor">Damage drop-off</h3>
    <div class="lc-scroll" tabindex="0" role="region" aria-labelledby="lc-drop-cap">
      <table class="lc-btable" id="lc-drop">
        <caption class="lc-sr" id="lc-drop-cap">Damage per shot by distance for the head, upper torso, upper arm and thigh, with shots and time to kill to the upper torso</caption>
        <thead id="lc-drop-head"></thead>
        <tbody id="lc-drop-rows"></tbody>
      </table>
    </div>
    <p class="lc-hint" id="lc-bal-note"></p>
  </section>
  <div class="lc-cards">
    <section class="lc-card" aria-labelledby="lc-char-title">
      <h2 class="lc-card-title no_anchor" id="lc-char-title">Character effects</h2>
      <p class="lc-card-lead">Applied to the character, not the weapon, so they never enter a value above.</p>
      <ul class="lc-list" id="lc-char"></ul>
    </section>
    <section class="lc-card" aria-labelledby="lc-notes-title">
      <h2 class="lc-card-title no_anchor" id="lc-notes-title">Notes</h2>
      <ul class="lc-list" id="lc-notes"></ul>
    </section>
  </div>
  <section class="lc-card lc-cli" aria-labelledby="lc-cli-title">
    <h2 class="lc-card-title no_anchor" id="lc-cli-title">Same loadout on the command line</h2>
    <div class="lc-cli-row">
      <pre class="lc-cli-code" id="lc-cli-code" tabindex="0" aria-label="Equivalent command"><code id="lc-cli"></code></pre>
      <button type="button" class="lc-btn" id="lc-copy" disabled>Copy command</button>
    </div>
    <p class="lc-hint" id="lc-cli-note" aria-live="polite"></p>
    <p class="lc-hint">The page address links to this loadout.</p>
  </section>
</div>

<script src="{{ '/assets/js/loadout-eval.js' | relative_url }}?v={{ site.time | date: '%s' }}" defer></script>
<script src="{{ '/assets/js/loadout-optimize.js' | relative_url }}?v={{ site.time | date: '%s' }}" defer></script>
<script src="{{ '/assets/js/loadout-calculator.js' | relative_url }}?v={{ site.time | date: '%s' }}" defer></script>

<div class="vv-nojs" markdown="1">

**The calculator needs JavaScript.** The same values for each weapon's default loadout (Stand stance, bipod folded) are in the tables on the Weapon Attributes page: [final values](Wardogs_WeaponAttributes_v1.md#1-final-values) for every weapon, the [modifiers per weapon](Wardogs_WeaponAttributes_v1.md#2-weapons), and [what every attachment changes](Wardogs_WeaponAttributes_v1.md#3-attachments). Other loadouts: `python -I _tools/weapon_attributes.py --weapon ID_WEPN_037 --with ID_FGRP_006 --stance Prone`.

</div>
