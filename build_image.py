#!/usr/bin/env python3
"""Render the front page for Monday 23 November 2026.

This script draws the whole newspaper page — nameplate, lead story,
seven further stories and a closing news tape — and saves it as
``entry.png`` next to this file (or to the path given with ``--out``).

It is fully self-contained and deterministic: the only input is the
story text written below, the only libraries are the standard library
and Pillow, and there is no network access, no clock reading and no
randomness. Running it twice therefore produces byte-identical PNGs.

    python3 build_image.py
"""

import argparse
import os
import sys

from PIL import Image, ImageDraw, ImageFont

# --- page geometry -------------------------------------------------------
WIDTH = 1024
HEIGHT = 1024
MARGIN = 36
TEXT_WIDTH = WIDTH - 2 * MARGIN  # 952

# --- palette -------------------------------------------------------------
PAPER = (248, 244, 232)
INK = (17, 17, 17)
RED = (138, 20, 20)
GREY = (98, 92, 82)
TAPE_BG = (26, 26, 26)
TAPE_FG = (241, 239, 231)

FONT_DIR = "/usr/share/fonts/truetype/liberation"


def font(filename, size):
    """Load one Liberation font at the requested point size."""
    return ImageFont.truetype(os.path.join(FONT_DIR, filename), size)


FONTS = {
    "nameplate": font("LiberationSerif-Bold.ttf", 80),
    "dateline": font("LiberationSans-Bold.ttf", 26),
    "strap": font("LiberationSans-Regular.ttf", 14),
    "kicker": font("LiberationSans-Bold.ttf", 19),
    "lead_head": font("LiberationSerif-Bold.ttf", 48),
    "lead_dek": font("LiberationSerif-Italic.ttf", 22),
    "lead_body": font("LiberationSerif-Regular.ttf", 16),
    "ticker": font("LiberationSans-Bold.ttf", 14),
    "head": font("LiberationSerif-Bold.ttf", 29),
    "head_small": font("LiberationSerif-Bold.ttf", 23),
    "body": font("LiberationSerif-Regular.ttf", 16),
    "body_small": font("LiberationSerif-Regular.ttf", 15),
    "tape": font("LiberationSans-Bold.ttf", 15),
    "footer": font("LiberationSans-Regular.ttf", 13),
}


# --- text helpers --------------------------------------------------------


def wrap(draw, text, face, width):
    """Split *text* greedily into lines that fit *width* pixels."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            candidate = current + " " + word
            if draw.textlength(candidate, font=face) <= width:
                current = candidate
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def paragraph(draw, x, y, width, text, face, leading, colour=INK):
    """Draw a wrapped paragraph; return the y just below its last line."""
    for line in wrap(draw, text, face, width):
        draw.text((x, y), line, font=face, fill=colour)
        y += leading
    return y


def rule(draw, y, weight=2, x0=None, x1=None):
    """Draw a horizontal rule; return the y just below it."""
    left = MARGIN if x0 is None else x0
    right = WIDTH - MARGIN if x1 is None else x1
    draw.line([(left, y), (right, y)], fill=INK, width=weight)
    return y + weight


def double_rule(draw, y):
    """The thick-plus-thin rule under the nameplate."""
    rule(draw, y, 3)
    rule(draw, y + 6, 1)
    return y + 10


def kicker(draw, x, y, text):
    """Draw a red section label; return the y below it."""
    draw.text((x, y), text, font=FONTS["kicker"], fill=RED)
    return y + 26


def story(draw, x, y, width, label, headline, body,
          head_face, head_leading, body_face=None, body_leading=20):
    """Draw one story block (label, headline, body); return the y below."""
    y = kicker(draw, x, y, label)
    for line in wrap(draw, headline, head_face, width):
        draw.text((x, y), line, font=head_face, fill=INK)
        y += head_leading
    y += 2
    face = body_face if body_face is not None else FONTS["body"]
    return paragraph(draw, x, y, width, body, face, body_leading)


def centred(draw, y, text, face, colour):
    """Draw *text* centred on the page at height *y*."""
    width = draw.textlength(text, font=face)
    draw.text(((WIDTH - width) / 2, y), text, font=face, fill=colour)


# --- the stories ---------------------------------------------------------
# Every fact below was checked against several independent sources on
# the morning of 23 November 2026; see NOTES.md for the sources.

LEAD = {
    "label": "BENGHAZI, LIBYA  —  THE WAR AT SEA SPREADS",
    "headline": "UKRAINE SINKS RUSSIAN WARSHIP",
    "dek": ("Kyiv's sea drones strike the corvette Merkury at anchor in "
            "Benghazi — a day after the Sparta II blaze in the Baltic."),
    "left": ("BENGHAZI — Ukrainian sea drones struck the Russian corvette "
             "Merkury at the Benghazi naval base on Sunday, setting it "
             "ablaze. Satellite images show most of the ship capsized "
             "and sunk."),
    "right": ("Libyan officials said six unmanned boats were launched and "
              "two hit the corvette. A second Russian-linked cargo ship, "
              "the Ascalon, was also struck off the coast."),
    "strip": ("6 SEA DRONES LAUNCHED  ·  2 HITS ON MERKURY  ·  "
              "CORVETTE CAPSIZED  ·  2ND SHIP HIT TOO"),
}

ROW_TWO = [
    {
        "label": "ANTALYA",
        "headline": "COP31 ENDS WITH NO DEAL",
        "body": ("The UN climate summit ended on Sunday without a pact after "
                 "two days of overtime, as the EU and others rejected a "
                 "draft that dropped all mention of fossil fuels. "
                 "Guterres: “deeply disappointed”."),
    },
    {
        "label": "WASHINGTON",
        "headline": "DEMOCRATS WIN 258 SEATS",
        "body": ("Democrats secured their biggest House majority since 1992, "
                 "clinched on Sunday when Chuck Hubbard beat Rep. Virginia "
                 "Foxx in North Carolina. They gained 44 seats; four races "
                 "remain uncalled."),
    },
]

ROW_THREE = [
    {
        "label": "DYMER",
        "headline": "14 MISSING IN DYMER",
        "body": ("A Russian drone collapsed part of a five-storey block in "
                 "Dymer, north of Kyiv, on Sunday. Nine people were "
                 "evacuated; rescuers searched the rubble for 14 "
                 "unaccounted for, including two children."),
    },
    {
        "label": "SERANG",
        "headline": "CANDY FACTORY INFERNO",
        "body": ("At least three people were killed and dozens are missing "
                 "after a fire tore through a candy factory in Serang, "
                 "Indonesia, on Saturday. Rescuers pulled 24 body bags "
                 "from the ruins on Sunday."),
    },
    {
        "label": "GULF OF FINLAND",
        "headline": "SPARTA II TOWED AWAY",
        "body": ("Russia began towing the stricken Sparta II out of Finnish "
                 "waters on Sunday, after Finnish, Estonian and Russian "
                 "crews fought its fire together. One crew member was "
                 "slightly hurt."),
    },
]

ROW_FOUR = [
    {
        "label": "SEOUL",
        "headline": "MINISTER QUITS OVER EXAMS",
        "body": ("South Korea's education minister resigned on Sunday after a "
                 "cheating scandal rocked the college entrance exam: a top "
                 "scorer had used a hidden camera and AI, and 111 cases of "
                 "device misconduct were found."),
    },
    {
        "label": "GENEVA",
        "headline": "KILLER-ROBOT TALKS STALL",
        "body": ("UN talks on lethal autonomous weapons ended on Saturday "
                 "with agreement to keep talking for two more years — but "
                 "no binding rules, despite pleas from the UN chief and the "
                 "Red Cross."),
    },
]

TAPE = [
    "ATLANTA · Delta's weight-and-balance system fails on Sunday; "
    "over half its flights delayed at the start of Thanksgiving week",
    "LISBON · Thousands march in the rain over living costs and "
    "housing — “many thousands”, say organisers",
    "LAS VEGAS · Verstappen wins a chaotic Grand Prix ahead of "
    "Norris and Piastri; Russell crashes late",
    "MYANMAR · Army-backed government calls ASEAN decision "
    "“unfair and imbalanced”",
]

FOOTER = ("REPORTED 22–23 NOVEMBER 2026  ·  SOURCES: ISW, UN NEWS, "
          "AP, REUTERS, CNN, AFP, YONHAP")


# --- layout --------------------------------------------------------------


def build_page():
    page = Image.new("RGB", (WIDTH, HEIGHT), PAPER)
    draw = ImageDraw.Draw(page)

    # Nameplate -----------------------------------------------------------
    y = 20
    centred(draw, y, "THE WORLD", FONTS["nameplate"], INK)
    y += 86
    centred(draw, y, "MONDAY  23  NOVEMBER  2026", FONTS["dateline"], RED)
    y += 34
    centred(draw, y, "THE DAY’S WORLD NEWS IN ONE PAGE",
            FONTS["strap"], GREY)
    y += 18
    y = double_rule(draw, y)
    y += 4

    # Lead story ----------------------------------------------------------
    y = kicker(draw, MARGIN, y, LEAD["label"])
    for line in wrap(draw, LEAD["headline"], FONTS["lead_head"], TEXT_WIDTH):
        draw.text((MARGIN, y), line, font=FONTS["lead_head"], fill=INK)
        y += 54
    y += 2
    y = paragraph(draw, MARGIN, y, TEXT_WIDTH, LEAD["dek"],
                  FONTS["lead_dek"], 27)
    y += 6
    column = (TEXT_WIDTH - 24) // 2
    left_end = paragraph(draw, MARGIN, y, column, LEAD["left"],
                         FONTS["lead_body"], 20)
    right_end = paragraph(draw, MARGIN + column + 24, y, column,
                          LEAD["right"], FONTS["lead_body"], 20)
    y = max(left_end, right_end) + 5
    centred(draw, y, LEAD["strip"], FONTS["ticker"], RED)
    y += 20
    y = rule(draw, y, 2)
    y += 6

    # Two stories ---------------------------------------------------------
    column = (TEXT_WIDTH - 28) // 2
    first = story(draw, MARGIN, y, column,
                  ROW_TWO[0]["label"], ROW_TWO[0]["headline"],
                  ROW_TWO[0]["body"], FONTS["head"], 33)
    second = story(draw, MARGIN + column + 28, y, column,
                   ROW_TWO[1]["label"], ROW_TWO[1]["headline"],
                   ROW_TWO[1]["body"], FONTS["head"], 33)
    y = max(first, second) + 3
    y = rule(draw, y, 1)
    y += 6

    # Three stories -------------------------------------------------------
    third = (TEXT_WIDTH - 2 * 24) // 3
    ends = []
    for i, item in enumerate(ROW_THREE):
        x = MARGIN + i * (third + 24)
        ends.append(story(draw, x, y, third,
                          item["label"], item["headline"], item["body"],
                          FONTS["head_small"], 27,
                          FONTS["body_small"], 18))
    y = max(ends) + 3
    y = rule(draw, y, 1)
    y += 6

    # Two stories ---------------------------------------------------------
    column = (TEXT_WIDTH - 28) // 2
    first = story(draw, MARGIN, y, column,
                  ROW_FOUR[0]["label"], ROW_FOUR[0]["headline"],
                  ROW_FOUR[0]["body"], FONTS["head"], 33,
                  FONTS["body"], 19)
    second = story(draw, MARGIN + column + 28, y, column,
                   ROW_FOUR[1]["label"], ROW_FOUR[1]["headline"],
                   ROW_FOUR[1]["body"], FONTS["head"], 33,
                   FONTS["body"], 19)
    y = max(first, second) + 4

    # News tape -----------------------------------------------------------
    band_top = y
    band_height = 104
    draw.rectangle([(MARGIN, band_top),
                    (WIDTH - MARGIN, band_top + band_height)],
                   fill=TAPE_BG)
    text_y = band_top + 8
    for item in TAPE:
        for line in wrap(draw, item, FONTS["tape"], TEXT_WIDTH - 20):
            draw.text((MARGIN + 10, text_y), line,
                      font=FONTS["tape"], fill=TAPE_FG)
            text_y += 20
    y = band_top + band_height + 6

    # Footer --------------------------------------------------------------
    centred(draw, y, FOOTER, FONTS["footer"], GREY)
    y += 14

    if y > HEIGHT - 8:
        raise SystemExit("layout overflow: content ends at y=%d" % y)
    return page


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=None)
    args = parser.parse_args(argv)
    if args.out:
        out_path = args.out
    else:
        out_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "entry.png")
    page = build_page()
    page.save(out_path, format="PNG", optimize=True)
    print("wrote %s (%dx%d)" % (out_path, WIDTH, HEIGHT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
