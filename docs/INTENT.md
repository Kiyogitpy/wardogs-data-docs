# Intent

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

Why this project exists.

## Short answer

A shipped Unreal Engine game carries tens of thousands of DataAssets,
DataTables, curves and gameplay effects in its packaged files. How the
game plays (damage, recoil, prices, unlocks, spawn rules) comes from
that data together with the compiled code that reads it.

Developers rarely publish this. Players piece it together from patch
notes, forum posts and spreadsheets, so questions like "how does
damage fall off with range" or "what changed this season" get
guesses instead of numbers.

This project documents it end to end for one game, Wardogs, in a form
that is precise enough to be useful and public enough to be checked:
every value cites the asset it comes from.

## Why Wardogs

- **Current UE5 target** (5.7): the patterns here apply to other UE5
  titles
- **Live service**: the game patches regularly, so the docs track
  real changes between builds and seasons
- **The author plays it**: questions from playing turn into pages

## Why documentation

Documentation:

1. **Builds on itself**: each page makes the next one easier
2. **Serves many readers**: new players, theorycrafters, content
   creators, modders of other UE games, and the developers themselves
3. **Is static**: the output is pages and JSON, not a program to keep
   running
4. **Has an end state**: "every table documented" is a finish line

## Why public

1. **Checking**: a public site gets more corrections than a private
   spreadsheet
2. **Contributors**: readers notice things the author misses
3. **Reuse**: the generators in `_tools/` and the method in
   [`METHODOLOGY.md`](METHODOLOGY.md) carry over to other UE games

## What is published and what is not

The repository publishes the docs, the generated JSON, and the code
that produces them. The raw game exports and the class dump stay on
the author's machine; they are the game's own material, and the docs
cite them by asset name and path instead. See
[`SCOPE.md`](SCOPE.md).
