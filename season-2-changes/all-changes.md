---
title: "All Changes"
parent: "Season 2 Changes"
nav_order: 99
description: "Full Season 1 to Season 2 change browser: every asset and property, before and after, filterable by area, status and text."
---

# All Changes

{{ page.description }}

Deep links work: `#area=vehicles&q=Humvee` opens an area with a text filter, and `&s=modified,added` limits the status.

<div class="sd" id="sd" data-sd-browser data-sd-base="{{ '/assets/data/season-diff/' | relative_url }}" data-gh="https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/" markdown="0">
  <p class="sd-note">Loading changes…</p>
</div>

<noscript><p>The change browser needs JavaScript. The source data is in <code>assets/data/season-diff/</code>.</p></noscript>

<script src="{{ '/assets/js/season-diff.js' | relative_url }}?v={{ site.time | date: '%s' }}" defer></script>
