---
title: "Weapon Spray Viewer"
redirect_from: ["/spray-viewer.html", "/spray-viewer"]
parent: "Weapons & Ammo"
description: "Every weapon's recoil spray pattern, shot by shot, Season 1 against Season 2, with a fire-rate timeline and an all-weapons overview"
---

# Weapon Spray Viewer

*Data: [`assets/data/spray-patterns.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/spray-patterns.json)*

The recoil spray of every weapon: where the view ends up after each shot of a sustained burst. Pick a weapon, then Season 1, Season 2 or Compare to overlay both. Stance, focus and default-attachment multipliers rescale the spray, and a distance turns degrees into metres on a target. The overview at the bottom shows all the sprays at once; click a tile to open it. The recoil rules are in [Weapons §5a](../content/Wardogs_Weapons_v2.md#5a-recoil), and each weapon's inputs are in the [spread and recoil data](../content/Wardogs_WeaponSpreadRecoilData_v1.md).

<div class="vv sv" id="sv" markdown="0" data-json="{{ '/assets/data/spray-patterns.json' | relative_url }}?v={{ site.time | date: '%s' }}" data-base="{{ '/' | relative_url }}">
  <p class="sv-provisional" id="sv-prov" role="note" hidden>Provisional data: Season 1 values are not loaded yet, so only Season 2 is shown.</p>
  <div class="vv-controls sv-controls">
    <div class="vv-field sv-field-weapon">
      <label for="sv-weapon">Weapon</label>
      <select id="sv-weapon" disabled><option>Loading weapons…</option></select>
    </div>
    <div class="vv-field sv-field-category">
      <label for="sv-category">Category</label>
      <select id="sv-category" disabled><option>Infantry</option></select>
    </div>
    <div class="vv-field vv-field-mode sv-field-season">
      <span class="vv-label" id="sv-season-label">Season</span>
      <div class="wd-segmented vv-mode" id="sv-season" role="radiogroup" aria-labelledby="sv-season-label">
        <button type="button" role="radio" value="s1" aria-checked="false" tabindex="-1">Season 1</button>
        <button type="button" role="radio" value="s2" aria-checked="true">Season 2</button>
        <button type="button" role="radio" value="compare" aria-checked="false" tabindex="-1">Compare</button>
      </div>
    </div>
    <div class="vv-field vv-field-mode sv-field-stance">
      <span class="vv-label" id="sv-stance-label">Stance</span>
      <div class="wd-segmented vv-mode" id="sv-stance" role="radiogroup" aria-labelledby="sv-stance-label">
        <button type="button" role="radio" value="stand" aria-checked="true">Stand</button>
        <button type="button" role="radio" value="crouch" aria-checked="false" tabindex="-1">Crouch</button>
        <button type="button" role="radio" value="prone" aria-checked="false" tabindex="-1">Prone</button>
      </div>
    </div>
  </div>
  <div class="vv-layout">
    <div class="vv-stage" id="sv-stage">
      <div class="sv-box sv-plot" id="sv-plot"></div>
      <p class="vv-status" id="sv-status" role="status"></p>
      <div class="sv-controls-2">
        <label class="vv-check"><input type="checkbox" id="sv-c-focus"> Focus (reduced recoil)</label>
        <label class="vv-check"><input type="checkbox" id="sv-c-attachments"> Default attachment multipliers</label>
        <label class="vv-check"><input type="checkbox" id="sv-c-fan" checked> Random-turn fan</label>
        <label class="vv-check"><input type="checkbox" id="sv-c-band" checked> Random-section band</label>
        <label class="vv-check"><input type="checkbox" id="sv-c-metres"> Metres at</label>
        <label class="sv-range"><input type="number" id="sv-dist" min="1" max="2000" step="1" value="100" disabled aria-label="Target distance in metres"> m</label>
        <label class="sv-range">Shots <input type="range" id="sv-shots" min="1" max="30" value="30" aria-describedby="sv-shots-out"> <output id="sv-shots-out">30</output></label>
        <label class="sv-range">Inspect shot <input type="range" id="sv-inspect" min="1" max="30" value="1"></label>
        <span class="vv-hint">Arrow keys on the plot step through the shots; hovering the plot picks the nearest one. The vertical axis is up, the horizontal axis is right.</span>
      </div>
    </div>
    <aside class="vv-panel" id="sv-panel" aria-label="Selected weapon" aria-live="polite"></aside>
  </div>
  <div class="vv-legend" id="sv-legend"></div>
  <h2 class="vv-slots-title no_anchor">Fire rate</h2>
  <p>Each marker is a shot at the weapon's rounds per minute. The shaded block after the last shot is the pattern reset time: pause longer than that and the pattern starts again from shot 1. A dashed tick marks where the fixed pattern ends and the random section begins.</p>
  <div class="sv-tl-box" id="sv-timeline"></div>
  <h2 class="vv-slots-title no_anchor">All weapons</h2>
  <p>Every weapon's spray in the selected category, grouped by class, using the season choice above. <label class="vv-check"><input type="checkbox" id="sv-c-sameScale" checked> Same scale for every tile</label></p>
  <div id="sv-grid"></div>
</div>

<script src="{{ '/assets/js/spray-viewer.js' | relative_url }}?v={{ site.time | date: '%s' }}" defer></script>

<div class="vv-nojs" markdown="1">

The viewer needs JavaScript. The same numbers are in [`spray-patterns.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/spray-patterns.json) and, per weapon, in the [spread and recoil data](../content/Wardogs_WeaponSpreadRecoilData_v1.md).

</div>

## How to read it

- **The plot** is the view offset in degrees after each shot, starting from the aim point (white dot). Firearms do not pull the view back by themselves, so the sprays only keep climbing until you pull down.
- **Pattern shots** are filled markers; once the fixed pattern ends, each shot's kick is random inside a yaw range and a pitch range. Those shots are hollow markers on a path through the middle of the ranges, with a box around each (10th to 90th percentile).
- **Random-turn fan.** Each shot inside the pattern is turned by a random angle up to the weapon's deviation setting; the wedge shows that spread.
- **Multipliers.** Stance scales the whole kick (stand, crouch, prone). Focus removes the weapon's focus reduction percentage. Default attachments apply the weapon's horizontal and vertical recoil multipliers with its default attachments fitted. The weapon's own view-kick magnitude multiplier always applies.
- **Metres.** The extra axis converts a view offset to the sideways or upward miss on a target at the chosen distance, distance × tan(angle).
- **Compare.** Season 1 is blue with round markers and a dashed line; Season 2 is green with square markers and a solid line. A weapon missing from one season is shown with the other only.
- Evidence and method: [Weapons §5a](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/content/Wardogs_Weapons_v2.md#5a-recoil) and the [spread and recoil data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/content/Wardogs_WeaponSpreadRecoilData_v1.md).
