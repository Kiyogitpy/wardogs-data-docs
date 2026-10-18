---
title: "Weapon Loadout Calculator"
parent: "Content"
---

# Weapon Loadout Calculator

*Data: [`assets/data/weapon-loadouts.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-loadouts.json), built by `python _tools/weapon_attributes.py --json`*

Pick a weapon, fill each of its sub-slots with any attachment the slot accepts, and choose a sight, a stance and a bipod state. The calculator shows every `Attribute.Gameplay.Weapon.*` value with its base, each modifier that reaches it and the final value, and lists the effects that go to the character instead. It is the browser version of `python _tools/weapon_attributes.py`, and the rules are the ones on [Weapon Attributes](Wardogs_WeaponAttributes_v1.md#rules): what applies to a weapon, the stance and bipod lists, and the current-value formula of the [Gameplay Effects Pipeline](Wardogs_GameplayEffectsPipeline_v1.md#44-current-value) §4.4.

<div class="vv lc" id="lc" markdown="0" data-json="{{ '/assets/data/weapon-loadouts.json' | relative_url }}?v={{ site.time | date: '%s' }}">
  <div class="vv-controls lc-controls">
    <div class="vv-field lc-field-weapon">
      <label for="lc-weapon">Weapon</label>
      <select id="lc-weapon" disabled><option>Loading weapons…</option></select>
    </div>
    <div class="lc-actions">
      <button type="button" class="lc-btn" id="lc-reset" disabled>Reset to default loadout</button>
    </div>
  </div>
  <p class="lc-status" id="lc-status" role="status"></p>
  <div class="lc-layout">
    <section class="lc-card lc-loadout" aria-labelledby="lc-loadout-title">
      <h2 class="lc-card-title no_anchor" id="lc-loadout-title">Loadout</h2>
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
<script src="{{ '/assets/js/loadout-calculator.js' | relative_url }}?v={{ site.time | date: '%s' }}" defer></script>

<div class="vv-nojs" markdown="1">

**The calculator needs JavaScript.** The same values for each weapon's default loadout (Stand stance, bipod folded) are in the tables on the Weapon Attributes page: [final values](Wardogs_WeaponAttributes_v1.md#1-final-values) for every weapon, the [modifiers per weapon](Wardogs_WeaponAttributes_v1.md#2-weapons), and [what every attachment changes](Wardogs_WeaponAttributes_v1.md#3-attachments). Other loadouts: `python -I _tools/weapon_attributes.py --weapon ID_WEPN_037 --with ID_FGRP_006 --stance Prone`.

</div>
