---
title: "Season 2 Changes"
nav_order: 1.5
has_children: true
description: "Every change between Season 1 and Season 2 (build ++Wardogs+Live-CL-516586, 2026-10-15), before and after."
---

# Season 2 Changes

{{ page.description }}

Each change is shown as **before → after**: the Season 1 value, then the Season 2 value, with the difference for numbers. The data is the same game files as the rest of this site, compared asset by asset and property by property.

Two terms appear in the totals. An asset is **noise-only** when the only differences are bookkeeping that does not change behaviour (for example a property renamed internally or an object reference that moved). An asset is an **inferred pairing** when its file was renamed or moved in Season 2 and the comparison matched it to its Season 1 copy by content rather than by a clear identifier, so treat that match as likely rather than certain.

<div class="sd-totals" data-sd-totals data-sd-base="{{ '/assets/data/season-diff/' | relative_url }}" markdown="0">
  <p class="sd-note">Loading totals…</p>
</div>

<a class="wd-btn wd-btn-primary" href="{{ '/season-2-changes/all-changes/' | relative_url }}">Browse every change</a>

## Areas

{% include category-cards.html parent=page.title %}

<!-- Highlight pages for each area go here: add them as children (parent: "Season 2 Changes") under season-2-changes/. -->

<script src="{{ '/assets/js/season-diff.js' | relative_url }}?v={{ site.time | date: '%s' }}" defer></script>
