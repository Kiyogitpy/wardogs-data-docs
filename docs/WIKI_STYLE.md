# Wardogs Wiki: writing rules

The wiki (`_wiki/`, served at `/wiki/`) turns the data pages into articles a player can read. The data pages stay the source of truth; the wiki explains them. These rules keep every article consistent no matter who writes it.

## Files and front matter

- Hub page for an area: `_wiki/<area>.md` (served at `/wiki/<area>/`). Articles in that area: `_wiki/<area>/<slug>.md`, with lowercase hyphenated slugs (`ak-74m.md`, `body-armor.md`).
- Hub front matter:

  ```yaml
  ---
  title: Weapons
  nav_order: 1
  wiki_hub: true
  has_children: true
  description: "One line saying what the hub covers."
  ---
  ```

- Article front matter: `title`, `parent` (exactly the hub title), `description` (one sentence, shown on cards). Add `has_children: true` and use `grand_parent` only if an article really has sub-articles.
- Hub order: Weapons 1, Equipment 2, Vehicles 3, Game Mechanics 4, Game Modes & Maps 5, Progression & Economy 6, Guides 7, Patch Notes 8.
- A hub page has a short intro, a sortable overview table of everything it covers (one row per article, linking to it), then `{% include wiki-cards.html parent="<hub title>" %}`.

## Voice

- Write for players, not reverse engineers. No RVAs, addresses, function names, class names like `UWDWeaponComponent`, or asset paths in the article text.
- **Always call things by the name a player knows**: the in-game display name or the common real-world name ("UH-72 Lakota", "AK-74M", "Bandage"), never the internal code (`ROT_03`, `WEPN_028`, `BP_Item_Bandage`). This applies to titles, slugs, headings, prose, tables and links. Find display names on the Item Shop, Weapon Shop, Vehicles, Tag Display Text and Season 01 cosmetic pages and in the item data under `data/`. The internal code may appear only once, in the infobox row "Internal name", so people can search for it. If no display name exists anywhere, describe the thing in plain words ("unnamed test rifle") and keep the code in the infobox.
- Plain, encyclopedic, third person. Short paragraphs. Explain what a number means for play ("kills an unarmored player in 4 body shots up to 40 m").
- Units always: m, s, rounds/min, HP, cash. Round sensibly (1 decimal for metres and seconds, whole numbers for damage unless the decimal matters).
- Only state what the data pages or `assets/data/*.json` say. If something is unknown or not modeled, say so plainly ("not yet known"), never guess. Do not invent lore, release history or tips that the data doesn't support.
- Do not copy whole data tables. Pick the numbers a player needs and link to the data page for the rest.

## Article layout (game wiki convention)

1. `# Title`
2. Infobox: a two-column markdown table directly under the title, followed by `{: .wiki-infobox }` on the next line. Header row `| | |` can be left blank-labelled, e.g.

   ```markdown
   | AK-74M | |
   |---|---|
   | Class | Assault rifle |
   | Caliber | 5.45x39mm |
   | Fire rate | 600 rounds/min |
   {: .wiki-infobox }
   ```

3. Lead paragraph (2–4 sentences): what it is and its role.
4. Sections with `##` headings, in this order where they apply:
   - Weapons: Overview, Stats, Damage (body parts, range falloff, armor), Ammunition, Attachments, Cost and unlocking, Season 2 changes, See also, Sources.
   - Equipment/items: Overview, Effects, Use and timing, Cost, Season 2 changes, See also, Sources.
   - Vehicles: Overview, Stats, Armor and damage, Weapons and seats, Handling, Season 2 changes, See also, Sources.
   - Mechanics: Overview, How it works, Numbers, Tips that follow from the numbers, See also, Sources.
   - Modes/maps: Overview, Rules and objectives, Rewards, See also, Sources.
5. `## Sources`: bullet list of the data pages (relative `.md` links) and JSON files used. JSON files and anything under `data/`, `docs/`, `_tools/` are linked by absolute GitHub URL (`https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/...`) because they are not on the site.

## Links

- Link other wiki articles and data pages with relative `.md` links (from `_wiki/weapons/ak-74m.md`, the data page is `../../game-features/Wardogs_WeaponDamage_v1.md`, a sibling article is `ak-74m.md`, another area is `../equipment/body-armor.md`).
- Check with `python _tools/check_links.py` (it covers `_wiki/`).
- Liquid is live in these files: never write `{{` or `{%` in prose.
