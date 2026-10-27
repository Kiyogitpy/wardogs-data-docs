# Security Policy

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

This repository documents the game data of **Wardogs** (Bulkhead,
published by Team17). Reading a game's data and the code that uses it
can turn up things that look like security problems: values the
server takes from the client without checking, missing validation, or
crashes from malformed input. This page says what happens to those.

## How findings are handled

1. **Kept out of this repository.** A possible security issue is not
   written up in the docs, an issue or a pull request while it is open.
2. **Reported to the developer** through the security or support
   contact Bulkhead or Team17 publishes, or the Steam support form if
   there is none. If there is no reply in 7 days, through a different
   channel.
3. **Coordinated disclosure.** 90 days from the report by default,
   longer on request for a hard fix, shorter if the issue is being
   exploited (agreed with the developer).
4. **After the fix ships**, a write-up may be added, crediting the
   developer's fix.

Balance observations (damage, time to kill, prices) and how the game
works in general are not security issues; they belong in the docs.

## What this repository does not publish

- Exploit code, for a disclosed issue or an open one
- Tools that act on a running game: loaders, injectors, memory
  readers, overlays
- Anything that affects accounts, payments or other players' progress

## Found something by reading the docs?

Please do **not** open a public issue or pull request about it. Either:

- email the repository author (contact on the GitHub profile), and
  we will report it to the developer together, or
- report it to the developer yourself and leave this repository out
  of it.

Both are fine. The developer should hear about it before the internet
does. Reporters are credited in any later write-up unless they ask
to stay anonymous.
