---
title: "All S2 to S3 Differences"
parent: "Season 3 Changes"
nav_order: 99
description: "Search saved S2 and S3 exports by asset, property and value, with separate Season 2 and Season 3 columns."
---

# Season 2 → Season 3: all exported differences

{{ page.description }}

The comparison pairs exact file paths and export identities. Arrays keep their stored order. Internal field names and object references are compared literally; a renamed field can therefore appear as one missing and one added field. No guessed field rename, array alignment or cross-file move is promoted into a gameplay change.

Large values link to their pinned S2/S3 source exports. Their exact source location and content hash remain in the JSON dataset; precise numeric text, including nested signed zero, is preserved in displayed inline values.

**Only in S2/S3 snapshot** describes export coverage, not deletion or release of content. Parsing coverage, changed packaging and source selection can all affect file presence. The S3 extraction still has three UI errors and five warnings. See [the notes and known gaps](../_wiki/patch-notes/season-3.md).

Filter by area, asset path, field name or value. Links such as `#area=vehicles&q=TNK_01` preserve the selected area and search.

<div class="sd" id="sd" data-sd-browser data-sd-snapshot data-sd-base="{{ '/assets/data/season3-diff/' | relative_url }}" markdown="0">
  <p class="sd-note">Loading S2 → S3 differences…</p>
</div>

<noscript><p>The browser needs JavaScript. The comparison is also available as JSON in <code>assets/data/season3-diff/</code>.</p></noscript>

<script src="{{ '/assets/js/season-diff.js' | relative_url }}?v={{ site.time | date: '%s' }}" defer></script>
