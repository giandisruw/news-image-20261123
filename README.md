# THE WORLD — Monday 23 November 2026

[![make.fun bounty](https://img.shields.io/badge/make.fun-news--image--20261123-blue)](https://make.fun/bounty/news-image-20261123)
[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![python](https://img.shields.io/badge/python-3.13-blue)](main.py)

One day of world news, summed up in a single front page.

## The image

`entry.png` is a one-page newspaper — **THE WORLD, Monday 23 November
2026** — laid out like a broadsheet: a masthead, one lead story with a
large illustration, and the rest of the day's news in columns around it.

The lead: Ukraine's sinking of the Russian corvette **Merkury** off
Benghazi. Around it, the day's other stories — the COP31 talks ending
without a deal, the Democrats' 258 seats in the US House, a missing
Dymer drone crew, a candy-factory fire in Serang, the Sparta II being
towed, a minister resigning in Seoul, and the stalled Geneva talks on
killer robots — plus a ticker of smaller items (Delta delays in Atlanta,
a march in Lisbon, Verstappen's Las Vegas Grand Prix win, Myanmar and
ASEAN). Every story on the page happened on, or was reported on,
21–23 November 2026; the sources are listed in [NOTES.md](NOTES.md).

## How it runs

The finished image ships in this repository as `entry.png`. The entry
program is deliberately thin so its output can never drift:

```bash
python3 main.py
```

`main.py` (Python 3.13, standard library only, no network) copies the
bundled `entry.png` into the output directory — `$MAKEFUN_OUTPUT_DIR`,
or `/output` when that variable is unset — as `entry.png`, then checks
that the copy is complete by comparing its size with the source. Run it
twice and the two outputs are byte-identical.

## Files

| File | What it is |
| --- | --- |
| `main.py` | Entry program: copies the bundled image to the output directory and verifies the copy. |
| `entry.png` | The finished front page, 1024 × 1024. |
| `NOTES.md` | Story-by-story notes: what each item on the page is, and where it was reported. |
| `LICENSE` | MIT. |

## Bounty

Built for the make.fun bounty
[news-image-20261123](https://make.fun/bounty/news-image-20261123) —
"Sum up 23 November's world news in one image", $100.

---
*Referral: `0txwmf1m` — make.fun*
