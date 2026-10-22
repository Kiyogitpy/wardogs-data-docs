# Intent

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

Why this project exists. Short answer first, then the long one.

## Short answer

Modern game engines ship enormous amounts of data embedded in their
packaged assets. For a shipped UE game, that's typically tens of
thousands of DataAssets, DataTables, Curves, GameplayEffects, and so
on. The gameplay semantics live in the interaction between that data
and the compiled code that reads it.

Game publishers almost never document this interaction publicly.
Community reverse engineers do, piecemeal, in forum posts and leaked
spreadsheets. The result is a messy ecosystem where:

- Players don't know how damage actually calculates
- Modders can't predict side effects of changing a value
- Security researchers can't audit the trust model
- Developers themselves lose track across patches

This project is one person's attempt to do the documentation
end-to-end for a specific target game (Wardogs), in a form that's
rigorous enough to be useful and public enough to be checked.

The security-disclosure path exists because any time you reverse
engineer a game's complete data model, you tend to find trust-model
bugs. Keeping them private until the developer can fix them is the
right thing to do.

## Long answer

### Why Wardogs specifically

- **Modern UE5 target** (5.7) — the engine is current, the patterns
  seen here apply to other UE5 titles
- **Live service** — the game ships patches regularly, so there's a
  live data pipeline to track
- **Author owns a copy** and has local hardware to run it
- **Author plays the game** — direct feedback loop between playing,
  noticing data questions, and documenting them

### Why documentation, not reskinning / modding / cheating

Documentation is the one output that:

1. **Compounds in value** — each new doc makes the next one easier
   to produce
2. **Is defensible** — "I'm writing a reference book" is a clear
   fair-use research posture
3. **Serves multiple audiences** — new players, speedrunners,
   theorycrafters, modders of related games, security researchers,
   the developers themselves
4. **Doesn't require persistence** — the output is static markdown,
   not a running tool
5. **Has a natural end state** — "I've documented everything"
   is a goal with a finish line

Cheating fails all five tests. Mod development for a live-service
multiplayer game fails most of them. Reskinning fails attribution.

### Why the security-disclosure path exists

When you fully document a game's data model and the code that
consumes it, you tend to find:

- Server-trusted-client math
- Serialization bugs where the client controls a value the server
  should
- Replication conditions that leak information
- Validator gaps
- Deserialization issues with array lengths or type-confused unions

Each of these is a potential cheat vector in the wild. The game's
security team almost certainly knows about some of them.
Publishing a complete code↔data cross-reference would surface the
ones they *don't* know about to the public internet in minutes.

The responsible path is to:

1. Find them during the documentation work
2. Report them privately to the responsible vendor
3. Give the vendor a reasonable fix window
4. Publish the write-up after the fix ships

That's the standard CVE process applied to a game security context.

### Why public

Three reasons:

1. **Checking:** publishing the data docs lets other researchers
   catch errors. A spreadsheet in a Discord DM gets fewer
   corrections than a GitHub Pages site.
2. **Compounding:** making the docs public attracts contributors
   who notice things the primary author misses.
3. **Trust signal:** a public, long-running, documentation-focused
   repository is itself an argument that the project is what it
   claims to be. Cheat developers don't maintain Jekyll sites.

### Why solo-operator for now

- The project is small enough that one person can hold the whole
  model in their head
- Security-relevant findings benefit from a tight circle until
  disclosed
- Contributors are welcome under the terms in
  [`../CONTRIBUTING.md`](../CONTRIBUTING.md), but there's no need
  to grow headcount artificially

### Why this document exists

Anyone reading this project — whether a human contributor, an AI
assistant, the vendor's security team, or someone wondering if this
is a cheat repository in disguise — should be able to understand
the intent from reading one document. This is that document.

If after reading this it still looks like cheat development to you,
I'd like to hear why. Open a discussion.
