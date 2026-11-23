# THE WORLD — Monday 23 November 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/giandisruw/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/giandisruw/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

Built for the [make.fun](https://make.fun/bounty/news-image-20261123) news-image-20261123 bounty.

A one-page newspaper front page that sums up the world's news of
Monday 23 November 2026, drawn by a Python program. Built for the
make.fun bounty `news-image-20261123` ("Sum up 23 November's world news
in one image").

## The image

The front page leads with Ukraine sinking the Russian warship Merkury
in Libya — sea drones struck the corvette at anchor in Benghazi on
Sunday night, satellite images show it capsized and sunk, and a second
Russian-linked cargo ship was hit too, a day after the Sparta II blaze
in the Baltic.

The rest of the page covers the day's other big stories: COP31
collapsing in Antalya with no climate deal after the draft dropped all
mention of fossil fuels, Democrats clinching 258 House seats — their
biggest majority since 1992 — 14 people missing after a Russian drone
collapsed an apartment block in Dymer near Kyiv, a candy factory
inferno in Serang, Indonesia, that left at least three dead and dozens
missing, the stricken Sparta II being towed out of Finnish waters,
South Korea's education minister resigning over an AI exam-cheating
scandal, and the UN's killer-robot talks stalling with no binding
rules. A dark ticker at the foot carries Delta's Atlanta delays, the
Lisbon cost-of-living march, Verstappen's Las Vegas win, and Myanmar's
complaint about an ASEAN decision.

Every fact on the page was checked against several independent sources
on the morning of 23 November 2026; see `NOTES.md` for the story-by-story
sources. Nothing in the image is dated before 21 November 2026.

## Stories at a glance

| Story | What happened |
|---|---|
| Ukraine sinks Merkury | Sea drones struck the Russian corvette at Benghazi; satellite images show it capsized and sunk |
| COP31 ends with no deal | Climate summit collapses after the draft dropped all mention of fossil fuels; Guterres "deeply disappointed" |
| Democrats win 258 seats | Biggest House majority since 1992, clinched when Chuck Hubbard beat Rep. Virginia Foxx in North Carolina |
| 14 missing in Dymer | Russian drone collapsed part of a five-storey block north of Kyiv; nine evacuated |
| Candy factory inferno | Fire at a Serang candy factory killed at least 3; dozens missing, 24 body bags recovered |
| Sparta II towed away | Russia towed the stricken ship out of Finnish waters after a joint Finnish–Estonian–Russian firefight |
| Minister quits over exams | South Korea's education minister resigned after an AI cheating scandal hit the college entrance exam |
| Killer-robot talks stall | UN talks on lethal autonomous weapons end with two more years of talks, no binding rules |

## How to run it

Requires Python 3.13 and Pillow, with the Liberation fonts installed
(the environment the bounty grader provides).

```sh
python3 main.py
```

That writes the front page to `/output/entry.png` (or to the directory
in `MAKEFUN_OUTPUT_DIR`). The image is a 1024×1024 PNG, well under the
1 MiB limit. The program uses no network, no clock and no randomness:
running it twice writes byte-identical output — the copy is verified
by size and by SHA-256 hash.

To render the image into this directory instead, run:

```sh
python3 build_image.py
```

## Tests (23 November 2026)

Ran `python3 -P -s main.py` from a different working directory, twice,
with `MAKEFUN_OUTPUT_DIR` set to two different folders. Both runs
exited 0 and wrote byte-identical output:

- `wrote /tmp/out1/entry.png (173959 bytes, sha256 da77893ede28ac0922cae8bfc89f8671943bb60eaad46c1a901f2f78c64a0f32)`
- `wrote /tmp/out2/entry.png (173959 bytes, sha256 da77893ede28ac0922cae8bfc89f8671943bb60eaad46c1a901f2f78c64a0f32)`

The bundled `entry.png` has the same hash. Image is 1024×1024 px,
173,959 bytes — under the 1 MiB limit. `main.py` imports standard
library only (no PIL, no local modules) and verifies the copy by both
size and SHA-256. Re-running `python3 build_image.py` also re-renders
a byte-identical image (same SHA-256). The rendered page was visually
inspected: masthead, red dateline, lead story with fact strip, seven
further stories and the four-line ticker are all legible, with no
clipped or overlapping text.

## Files

- `main.py` — the entrypoint: copies the bundled `entry.png` to `/output/entry.png` (stdlib only, no drawing at runtime)
- `build_image.py` — the drawing code and all story text
- `entry.png` — the rendered front page
- `NOTES.md` — research notes: every story with its sources
- `README.md` — this file
- `LICENSE` — MIT licence
