---
title: "Season 3 Changes"
nav_order: 1.4
has_children: true
has_toc: false
description: "Season 2 CL-516586 → S3 / 0.3 CL-533731: saved-export values, before and after."
---

# Season 2 → Season 3 Changes

Compare the saved Season 2 data with the S3 / 0.3 asset snapshot, CL-533731 / hotfix 533689. Start with the [readable notes](../_wiki/patch-notes/season-3.md), or search the complete exported-field comparison below.

This is a comparison of the available exports. A file appearing in only one snapshot does not establish an addition or removal from the game. The newer export still has three UI parsing failures; water-field meanings and wager categories remain unresolved. Changes to internal labels are included literally rather than guessed as gameplay changes.

The pinned public snapshots contain **6,866 S2 files and 7,086 S3 files**. Of 6,770 shared paths, **868 have changed stored data and 5,902 compare equal**. There are **316 S3-only paths and 96 S2-only paths**, with 376,270 field-change operations in common files. Nine files also change export order, which is recorded separately. These counts describe the compared JSON snapshots, not a count of balance changes.

<div class="sd-totals" data-sd-totals data-sd-snapshot data-sd-base="{{ '/assets/data/season3-diff/' | relative_url }}" markdown="0">
  <p class="sd-note">Loading totals…</p>
</div>

<a class="wd-btn wd-btn-primary" href="{{ '/season-3-changes/all-changes.html' | relative_url }}">Browse S2 → S3 differences</a>

## Areas

{% include category-cards.html parent=page.title %}

The [Season 2 comparison](season-2-changes.md) remains the separate historical Season 1→2 dataset.

<script src="{{ '/assets/js/season-diff.js' | relative_url }}?v={{ site.time | date: '%s' }}" defer></script>
