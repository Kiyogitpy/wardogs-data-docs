---
title: Home
nav_order: 1
---

<div class="wd-hero" markdown="0">
<div class="wd-hero-text">
<h1>Every number in Wardogs, in one place</h1>
<p>Reference pages for the game's data: weapon and vehicle stats, rewards, items, challenges and more, read straight from the game files (build <code>++Wardogs+Live-CL-516586</code>, UE 5.7). Search any value, asset name or table name from the bar at the top.</p>
<div class="wd-actions">
<a class="wd-btn wd-btn-primary" href="#weapons-ammo">Browse categories</a>
<a class="wd-btn wd-btn-secondary" href="Wardogs_Rewards_and_Progression_v2.html">Rewards &amp; progression</a>
</div>
</div>
<div class="wd-hero-viewers">
<a class="wd-hero-viewer" href="pipelines/vehicle-viewer.html">
<img src="{{ '/assets/images/vehicle-viewer-preview.png' | relative_url }}" alt="3D collision mesh of the Havoc attack helicopter, coloured by health section" width="780" height="585">
<span class="wd-hero-viewer-name">Vehicle Hitbox Viewer</span>
<span class="wd-hero-viewer-desc">Every vehicle's collision mesh in 3D, coloured by health section. Pick a part to see how it routes damage and how many hits destroy the vehicle.</span>
</a>
<a class="wd-hero-viewer" href="pipelines/infantry-viewer.html">
<img src="{{ '/assets/images/infantry-viewer-preview.png' | relative_url }}" alt="3D physics bodies of the player character, coloured by hit location" width="780" height="585">
<span class="wd-hero-viewer-name">Infantry Hitbox Viewer</span>
<span class="wd-hero-viewer-desc">The player's physics bodies coloured by hit location. Pick a damage source, armor or helmet to see each body part's multiplier.</span>
</a>
</div>
</div>

## Finding things

- **Search** from the bar at the top of every page (press `/` or `Ctrl+K`). It covers the full text of every page, including tables, and opens the matching section.
- **Asset and table names match on their parts.** `PlayerKill` finds `DT_Reward_Cash_PlayerKill`, and `Havoc` finds every page that mentions the Havoc.
- **Items, Weapons and Vehicles appear in more than one category.** The base definitions and the per-item, per-weapon and per-vehicle data are separate pages, so check both.
- **Every page ends with its limitations:** what was inferred, and what the game files don't contain.

<div class="wd-kicker"><span class="wd-pill wd-pill-1">{{ site.pages | where_exp: "p", "p.parent" | size }} pages</span></div>
{% assign cats = site.pages | where: "has_children", true | where_exp: "p", "p.path contains 'categories/'" | sort: "nav_order" %}
{%- for c in cats %}

<h2 id="{{ c.title | slugify }}">{{ c.title }}</h2>

<p class="wd-section-intro">{{ c.description }}</p>

{% include category-cards.html parent=c.title %}
{%- endfor %}

<h2 id="balance-notes">Balance Notes</h2>

<p class="wd-section-intro">Worked damage comparisons between game versions, calculated from the values on these pages.</p>

<div class="wd-grid" markdown="0">
<a class="wd-card" href="balance-notes.html"><span class="wd-card-name">Balance Notes</span><span class="wd-card-desc">Before/after damage per bullet, hits to kill and the multipliers behind each change</span></a>
</div>
