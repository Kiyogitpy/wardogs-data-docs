---
title: Wiki Home
nav_order: 0
permalink: /wiki/
description: "Readable articles on Wardogs weapons, gear, vehicles, modes and mechanics."
---

<div class="wiki-top" markdown="0">
<section class="wiki-box wiki-welcome">
  <div class="wiki-box-body">
    <h1>Wardogs Wiki</h1>
    <p>Plain-language articles on every weapon, piece of gear, vehicle, mode and game rule in Wardogs, written from the numbers on the <a href="{{ '/' | relative_url }}">Wardogs Data Reference</a>. Every article lists the data pages it was written from, so any number can be checked at its source.</p>
    <dl class="wiki-facts">
      <div><dt>Articles</dt><dd>{{ site.wiki | where_exp: "p", "p.wiki_hub != true" | where_exp: "p", "p.permalink != '/wiki/'" | size }}</dd></div>
      <div><dt>Season</dt><dd>Season 2</dd></div>
      <div><dt>Game build</dt><dd>CL-516586</dd></div>
    </dl>
  </div>
</section>
<section class="wiki-box" aria-labelledby="season-band">
  <h2 class="wiki-band" id="season-band">Season 2</h2>
  <div class="wiki-box-body">
    <ul>
      <li>.308 Winchester base damage fell from 60 to 45, and 7.62x54 mm from 55 to 44.</li>
      <li>Heavy armor now reduces 50% (was 55%), Super heavy 60% (was 65%).</li>
      <li>The T-72B3 tank and the Wolf-110 joined the vehicle roster.</li>
      <li>Parachutes open only from 10 m above the ground.</li>
    </ul>
    <p><a href="{{ '/wiki/patch-notes/season-2/' | relative_url }}">Read the Season 2 patch notes</a></p>
  </div>
</section>
</div>

{% include wiki-portal.html %}
