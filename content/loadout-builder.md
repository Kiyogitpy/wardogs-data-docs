---
title: "Loadout Builder"
permalink: /loadout/
parent: "Interactive Tools"
description: "Use this to find the best setup: give it your Wardog and class level and it picks the attachments with the least vertical, horizontal or overall recoil, then shows sway, recoil, handling, the reticle and damage per body part and over distance"
---

# Loadout Builder

*Data: [`weapon-loadouts.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-loadouts.json), [`loadout-extras.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/loadout-extras.json), [`loadout-builder.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/loadout-builder.json) and [`spray-patterns.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/spray-patterns.json). The attribute tables and rules are the same as the [Weapon Loadout Calculator](loadout-calculator.html). Every sight with its numbers: [Sights and Optics](Wardogs_Sights_v1.md).*

<div class="lb" id="lb" markdown="0" data-base="{{ '/' | relative_url }}" data-builder="{{ '/assets/data/loadout-builder.json' | relative_url }}?v={{ site.time | date: '%s' }}" data-json="{{ '/assets/data/weapon-loadouts.json' | relative_url }}?v={{ site.time | date: '%s' }}" data-extras="{{ '/assets/data/loadout-extras.json' | relative_url }}?v={{ site.time | date: '%s' }}" data-spray="{{ '/assets/data/spray-patterns.json' | relative_url }}?v={{ site.time | date: '%s' }}">
  <div class="lb-bar">
    <div class="lb-field lb-field-level">
      <label for="lb-wardog">Wardog level</label>
      <input id="lb-wardog" type="number" min="1" max="150" step="1" inputmode="numeric" placeholder="Any" disabled>
    </div>
    <div class="lb-field">
      <label for="lb-role">Class</label>
      <select id="lb-role" disabled><option>Any class</option></select>
    </div>
    <div class="lb-field lb-field-level">
      <label for="lb-level">Class level</label>
      <input id="lb-level" type="number" min="1" max="150" step="1" inputmode="numeric" placeholder="Any" disabled>
    </div>
    <div class="lb-actions">
      <button type="button" class="lb-btn" id="lb-copy" disabled>Copy link</button>
      <button type="button" class="lb-btn" id="lb-reset" disabled>Reset</button>
    </div>
  </div>
  <p class="lb-hint" id="lb-gate-hint" aria-live="polite"></p>
  <p class="lb-status" id="lb-status" role="status">Loading the loadout data…</p>
  <div class="lb-layout" id="lb-layout" hidden>
    <div class="lb-side">
      <section class="lb-card" aria-labelledby="lb-eq-title">
        <h2 class="lb-card-title no_anchor" id="lb-eq-title">Equipment</h2>
        <div id="lb-equip"></div>
      </section>
      <section class="lb-card" aria-labelledby="lb-sum-title">
        <h2 class="lb-card-title no_anchor" id="lb-sum-title">Loadout summary</h2>
        <div id="lb-summary"></div>
      </section>
    </div>
    <div class="lb-main">
      <section class="lb-card" id="lb-weapon-card" aria-labelledby="lb-weapon-title">
        <h2 class="lb-card-title no_anchor" id="lb-weapon-title">Weapon</h2>
        <div id="lb-weapon"></div>
      </section>
      <section class="lb-card" id="lb-best-card" aria-labelledby="lb-best-title" hidden>
        <h2 class="lb-card-title no_anchor" id="lb-best-title">Best attachments</h2>
        <div id="lb-best"></div>
      </section>
      <section class="lb-card" id="lb-handling-card" aria-labelledby="lb-handling-title" hidden>
        <h2 class="lb-card-title no_anchor" id="lb-handling-title">Handling</h2>
        <p class="lb-lead" id="lb-handling-sum"></p>
        <div class="lb-scroll" tabindex="0" role="region" aria-label="Handling table">
          <table class="lb-table" id="lb-handling">
            <thead><tr><th scope="col">Attribute</th><th scope="col" class="lb-num">Base</th><th scope="col" class="lb-num">Fitted</th><th scope="col" class="lb-num">Change</th></tr></thead>
            <tbody id="lb-handling-rows"></tbody>
          </table>
        </div>
        <h3 class="lb-sub no_anchor">Sway and character effects</h3>
        <p class="lb-lead">Applied to the character while the weapon is held, so they are not in the table above. Multipliers start from 1.</p>
        <div class="lb-scroll" tabindex="0" role="region" aria-label="Sway and character effects">
          <table class="lb-table">
            <thead><tr><th scope="col">Effect</th><th scope="col" class="lb-num">Combined</th><th scope="col">From</th></tr></thead>
            <tbody id="lb-char-rows"></tbody>
          </table>
        </div>
        <ul class="lb-notes" id="lb-notes"></ul>
      </section>
      <section class="lb-card" id="lb-recoil-card" aria-labelledby="lb-recoil-title" hidden>
        <h2 class="lb-card-title no_anchor" id="lb-recoil-title">Recoil</h2>
        <p class="lb-lead" id="lb-recoil-lead"></p>
        <div id="lb-recoil"></div>
      </section>
      <section class="lb-card" id="lb-optics-card" aria-labelledby="lb-optics-title" hidden>
        <h2 class="lb-card-title no_anchor" id="lb-optics-title">Sight</h2>
        <div id="lb-optics"></div>
      </section>
      <section class="lb-card" id="lb-ballistics-card" aria-labelledby="lb-bal-title" hidden>
        <h2 class="lb-card-title no_anchor" id="lb-bal-title">Ammunition and damage</h2>
        <div class="lb-controls">
          <div class="lb-field"><label for="lb-ammo">Ammunition</label><select id="lb-ammo"></select></div>
          <div class="lb-field"><label for="lb-thelmet">Target helmet</label><select id="lb-thelmet"></select></div>
          <div class="lb-field"><label for="lb-tarmor">Target armor</label><select id="lb-tarmor"></select></div>
          <div class="lb-field"><label for="lb-range">Distance</label><select id="lb-range"></select></div>
        </div>
        <p class="lb-lead" id="lb-bal-summary"></p>
        <div class="lb-scroll" tabindex="0" role="region" aria-label="Damage per body part">
          <table class="lb-table">
            <thead><tr><th scope="col">Body part</th><th scope="col">Armor</th><th scope="col" class="lb-num">Damage</th><th scope="col" class="lb-num">Shots to kill</th><th scope="col" class="lb-num">Time to kill</th></tr></thead>
            <tbody id="lb-parts-rows"></tbody>
          </table>
        </div>
        <h3 class="lb-sub no_anchor">Damage drop-off</h3>
        <div class="lb-scroll" tabindex="0" role="region" aria-label="Damage drop-off by distance">
          <table class="lb-table">
            <thead id="lb-drop-head"></thead>
            <tbody id="lb-drop-rows"></tbody>
          </table>
        </div>
        <p class="lb-hint" id="lb-bal-note"></p>
      </section>
    </div>
  </div>
  <dialog class="lb-picker" id="lb-picker" aria-labelledby="lb-picker-title">
    <div class="lb-picker-head">
      <p class="lb-picker-title" id="lb-picker-title" role="heading" aria-level="2">Choose</p>
      <button type="button" class="lb-btn lb-picker-close" id="lb-picker-close" aria-label="Close">Close</button>
    </div>
    <div class="lb-field lb-picker-search">
      <label for="lb-picker-q">Search</label>
      <input id="lb-picker-q" type="search" autocomplete="off" placeholder="Name or type">
    </div>
    <p class="lb-hint" id="lb-picker-count" aria-live="polite"></p>
    <div class="lb-picker-body" id="lb-picker-list"></div>
  </dialog>
</div>

<script src="{{ '/assets/js/loadout-eval.js' | relative_url }}?v={{ site.time | date: '%s' }}" defer></script>
<script src="{{ '/assets/js/spray-viewer.js' | relative_url }}?v={{ site.time | date: '%s' }}" defer></script>
<script src="{{ '/assets/js/loadout-recoil.js' | relative_url }}?v={{ site.time | date: '%s' }}" defer></script>
<script src="{{ '/assets/js/loadout-builder.js' | relative_url }}?v={{ site.time | date: '%s' }}" defer></script>

<div class="lb-nojs" markdown="1">

**The builder needs JavaScript.** The same weapon values, without the picker, are in the tables on [Weapon Attributes](Wardogs_WeaponAttributes_v1.md#1-final-values).

</div>
