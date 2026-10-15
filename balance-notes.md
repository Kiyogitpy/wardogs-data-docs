---
title: "Balance Notes"
nav_order: 6
has_children: true
---

# Balance Notes

Worked damage comparisons between game versions, calculated from the raw values on the data pages. Each note states its model (hit location, range, target health, armour state), shows the numbers that changed, and ends with what the result means in play. They are calculations, not live tests.

<div class="wd-note-list" markdown="0">
{%- assign notes = site.pages | where: "parent", page.title | sort: "date" | reverse -%}
{%- for p in notes %}
<a class="wd-note-card is-{{ p.note.tone | default: 'flat' }}" href="{{ p.url | relative_url }}">
  <span class="wd-note-card-figure">{{ p.note.figure }}</span>
  <span class="wd-note-card-body">
    <span class="wd-note-card-meta">{{ p.note.seasons }}{% if p.note.status %} · {{ p.note.status }}{% endif %}</span>
    <span class="wd-note-card-name">{{ p.title }}</span>
    <span class="wd-note-card-desc">{{ p.note.lede }}</span>
  </span>
</a>
{%- endfor %}
</div>

## Adding a note

Copy [`Note_Template.md`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/Note_Template.md) to a new file named `Note_<Subject>.md`, fill in the front matter and the prose, and open a pull request.

- **Front matter holds the numbers.** `note.compare.rows` gives the damage per bullet before and after; the page works out the percentage change and hits to kill from them, so those always agree.
- **Quote every number** (`"30.80"`, not `30.80`). The page prints it exactly as written, trailing zeros included.
- **`tone`** is `down`, `up` or `flat` and colours the headline figure.
- **`date`** orders the list above, newest first.
- **Link the data pages** the values come from, so readers can check them.
