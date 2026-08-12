"""Apply the figure corrections requested by the Digital Discovery data reviewer.

Three fixes are applied, all regenerated from the committed source images so the
result is reproducible:

1. ``world_map.png`` (Fig. 2) -- "the black text which falls above the map can be
   difficult to read".  The two inset histograms are drawn on top of the world
   map, so their axis labels and panel titles sit directly on the map imagery.
   We add a thin white stroke around those black glyphs: the glyph runs are found
   as connected components inside the label bands, the ink coverage is grown by a
   few pixels to make a halo, the halo is painted white, and the original ink is
   re-composited on top.  The map underneath is otherwise untouched, and the plot
   is not regenerated (the underlying survey data are not redistributable at
   participant granularity).

2. ``gathertown.png`` (Fig. 4) -- participant name labels in the plenary-room
   panel are redacted.  Participants were not asked to consent to publication of
   their display names, so every name label in the large group panel is
   pixelated.  As in Fig. 5, the redaction is done per label: the near-white
   glyphs are found by connected components, joined horizontally into one run
   per label, and only that run's tight bounding box is mosaicked, so the
   surrounding room (seats, avatars, floor) is left intact.  The two breakout
   panels on the right are untouched: those show only organizers/authors
   (Sterling Baird, Taylor Sparks, Ramsey Issa), who have consented, plus
   project names.

3. ``posters.png`` (Fig. 5) -- the same redaction for the poster-room panel.
   Here name labels and room labels ("Project NN") share the panel, so the two
   are separated by glyph height: the small name labels are pixelated and the
   larger room labels are preserved.

Usage::

    python scripts/fix_manuscript_figures.py

Outputs are written next to the sources as ``world_map_readable.png``,
``gathertown_redacted.png``, and ``posters_redacted.png``.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

REPO_ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = REPO_ROOT / "latex" / "figures"


# --------------------------------------------------------------------------
# Fig. 2 -- world map readability
# --------------------------------------------------------------------------

# Fractional (x0, y0, x1, y1) label bands, expressed relative to the image size
# so the script keeps working if the figure is re-exported at a different
# resolution.  Each band brackets text that is drawn over the map; nothing
# outside these bands is touched.
MAP_TEXT_BANDS = (
    # "Country Distribution" / "Affiliation Distribution" panel titles.
    (0.185, 0.583, 0.339, 0.629),
    (0.683, 0.583, 0.844, 0.629),
    # y-axis tick numbers + rotated "Frequency" label, left of each panel.
    (0.000, 0.644, 0.046, 0.853),
    (0.506, 0.644, 0.549, 0.853),
    # x-axis category labels underneath both panels.
    (0.000, 0.848, 1.000, 1.000),
)

# A glyph is a dark connected component of roughly this size (source pixels at
# the committed 7290x4113 resolution; the figure is ~1000 dpi, so a 62 px glyph
# is about 4.5 pt on the page).  Map ink that strays into a band -- coastlines,
# the dotted country borders, the axis rules -- falls outside these bounds and
# is left alone.
INK_CUTOFF = 110  # luminance below which a pixel counts as glyph ink
GLYPH_MIN_H, GLYPH_MAX_H = 12, 95
GLYPH_MIN_W, GLYPH_MAX_W = 6, 130
# Luminance ramp converting the flattened raster back into an ink-coverage map,
# so the anti-aliased glyph edges survive the re-composite.
INK_DARK = 90
INK_LIGHT = 175
# Halo half-width in source pixels.  About 15% of the glyph height: enough to
# separate the ink from the imagery at print size, small enough that the counters
# of "0"/"o"/"e" stay open and the outline does not read as a filled plate.
STROKE_RADIUS = 9


def fix_world_map(src: Path, dst: Path) -> None:
    import numpy as np
    from scipy import ndimage

    img = Image.open(src).convert("RGB")
    w, h = img.size
    rgb = np.asarray(img).astype(np.float32)
    lum = np.asarray(img.convert("L")).astype(np.float32)

    # 1. Locate the glyphs: dark connected components of glyph-like size that
    #    lie inside one of the label bands.
    bands = np.zeros((h, w), bool)
    for x0, y0, x1, y1 in MAP_TEXT_BANDS:
        bands[int(y0 * h) : int(y1 * h), int(x0 * w) : int(x1 * w)] = True

    dark = (lum < INK_CUTOFF) & bands
    labelled, _ = ndimage.label(dark)
    glyphs = np.zeros((h, w), bool)
    kept = 0
    for idx, sl in enumerate(ndimage.find_objects(labelled), start=1):
        if sl is None:
            continue
        gh = sl[0].stop - sl[0].start
        gw = sl[1].stop - sl[1].start
        if GLYPH_MIN_H <= gh <= GLYPH_MAX_H and GLYPH_MIN_W <= gw <= GLYPH_MAX_W:
            glyphs[sl] |= labelled[sl] == idx
            kept += 1

    # 2. Ink coverage, restricted to a neighbourhood of the accepted glyphs so
    #    the anti-aliased edges are included but unrelated map ink is not.
    zone = ndimage.binary_dilation(
        glyphs, structure=_disk(STROKE_RADIUS + 3)
    )
    alpha = np.clip((INK_LIGHT - lum) / (INK_LIGHT - INK_DARK), 0.0, 1.0) * zone

    # 3. Grow the coverage into a halo and paint it white, then put the original
    #    ink back on top.  The halo is opaque out to STROKE_RADIUS and feathered
    #    over the last pixel so its outer edge does not read as a hard cut.
    halo = ndimage.binary_dilation(
        alpha > 0.35, structure=_disk(STROKE_RADIUS)
    ).astype(np.float32)
    halo = ndimage.gaussian_filter(halo, sigma=1.0)[..., None]
    a = alpha[..., None]
    ink = np.median(rgb[alpha > 0.95], axis=0) if (alpha > 0.95).any() else np.zeros(3)

    backdrop = rgb * (1.0 - halo) + 255.0 * halo
    out = ink * a + backdrop * (1.0 - a)

    Image.fromarray(np.clip(out, 0, 255).astype("uint8")).save(dst, optimize=True)
    print(
        f"wrote {dst.relative_to(REPO_ROOT)} ({w}x{h}); {kept} glyphs stroked, "
        f"{100 * float((halo[..., 0] > 0.02).mean()):.2f}% of pixels touched"
    )


def _disk(radius: int):
    import numpy as np

    span = np.arange(-radius, radius + 1)
    yy, xx = np.meshgrid(span, span, indexing="ij")
    return (yy**2 + xx**2) <= radius**2


# --------------------------------------------------------------------------
# Fig. 4 -- Gather Town name redaction
# --------------------------------------------------------------------------

# The plenary panel occupies the left ~65% of the composite; the two breakout
# panels (organizers only) are to the right of this fraction and are preserved.
PLENARY_X_FRAC = 0.652
# Vertical extent that can contain name labels in the plenary panel.
PLENARY_Y_FRAC = (0.20, 0.78)

WHITE_CUTOFF = 210  # label glyphs are near-white on a dark pill
# Glyph geometry in the plenary panel (source pixels).  Every near-white
# component in the panel is a name-label glyph; nothing taller than ~23 px
# occurs, so the ceilings below only reject stray specks and joined runs that
# are too tall to be a single line of text.
GATHER_GLYPH_MAX_H = 26
GATHER_GLYPH_MAX_W = 34
GATHER_LABEL_MIN_W = 24  # a run narrower than this is not a name
GATHER_LABEL_MAX_H = 44  # one line of text, ascender to descender, plus slack
GATHER_PAD_X = 4  # padding around the redacted run, in source pixels
GATHER_PAD_Y = 3
GATHER_PIXEL_BLOCK = 10  # mosaic block size, ~half the glyph height


def _redact_label_runs(
    img: Image.Image,
    box: tuple[int, int, int, int],
    glyph_max_h: int,
    glyph_max_w: int,
    label_min_w: int,
    label_max_h: int,
    pad_x: int,
    pad_y: int,
    pixel_block: int,
) -> int:
    """Mosaic each near-white text run inside ``box``; return the run count.

    Glyphs are found as connected components, joined horizontally into one run
    per label, and only the run's tight bounding box (plus a few pixels of
    padding) is replaced, so the redaction stays confined to the text itself.
    """
    import numpy as np
    from scipy import ndimage

    region = img.crop(box)
    arr = np.asarray(region).astype(int)
    white = (
        (arr[:, :, 0] > WHITE_CUTOFF)
        & (arr[:, :, 1] > WHITE_CUTOFF)
        & (arr[:, :, 2] > WHITE_CUTOFF)
    )

    labelled, _ = ndimage.label(white)
    glyphs = np.zeros_like(white)
    for idx, sl in enumerate(ndimage.find_objects(labelled), start=1):
        if sl is None:
            continue
        gh = sl[0].stop - sl[0].start
        gw = sl[1].stop - sl[1].start
        if gh <= glyph_max_h and gw <= glyph_max_w:
            glyphs[sl] |= labelled[sl] == idx

    # Bridge the inter-glyph and inter-word gaps of one label without bridging
    # to the label on the line above or below.
    joined = ndimage.binary_dilation(glyphs, structure=np.ones((3, 15), bool), iterations=2)

    redact = np.zeros_like(white)
    runs, _ = ndimage.label(joined)
    kept = 0
    for sl in ndimage.find_objects(runs):
        if sl is None:
            continue
        rh = sl[0].stop - sl[0].start
        rw = sl[1].stop - sl[1].start
        if rw < label_min_w or rh > label_max_h:
            continue
        y0 = max(0, sl[0].start - pad_y)
        y1 = min(arr.shape[0], sl[0].stop + pad_y)
        x0 = max(0, sl[1].start - pad_x)
        x1 = min(arr.shape[1], sl[1].stop + pad_x)
        redact[y0:y1, x0:x1] = True
        kept += 1

    pixelated = region.resize(
        (max(1, region.width // pixel_block), max(1, region.height // pixel_block)),
        Image.BILINEAR,
    ).resize(region.size, Image.NEAREST)

    mask = Image.fromarray((redact * 255).astype("uint8"), mode="L")
    img.paste(Image.composite(pixelated, region, mask), box[:2])
    return kept


def fix_gathertown(src: Path, dst: Path) -> None:
    img = Image.open(src).convert("RGB")
    w, h = img.size

    box = (
        0,
        int(h * PLENARY_Y_FRAC[0]),
        int(w * PLENARY_X_FRAC),
        int(h * PLENARY_Y_FRAC[1]),
    )
    kept = _redact_label_runs(
        img,
        box,
        GATHER_GLYPH_MAX_H,
        GATHER_GLYPH_MAX_W,
        GATHER_LABEL_MIN_W,
        GATHER_LABEL_MAX_H,
        GATHER_PAD_X,
        GATHER_PAD_Y,
        GATHER_PIXEL_BLOCK,
    )
    img.save(dst, optimize=True)
    print(f"wrote {dst.relative_to(REPO_ROOT)} ({w}x{h}); {kept} name labels redacted")


# --------------------------------------------------------------------------
# Fig. 5 -- poster-room name redaction
# --------------------------------------------------------------------------

# In the poster-room panel the participant name labels are rendered in a much
# smaller face than the "Project NN" room labels, so glyph height cleanly
# separates the two: names are redacted, room labels are kept.
NAME_GLYPH_MAX_H = 6
NAME_GLYPH_MAX_W = 12
LABEL_MIN_W = 18
LABEL_MAX_H = 14
POSTER_PIXEL_BLOCK = 6

# Fractional (x0, y0, x1, y1) boxes around room labels that are rendered too
# faintly to be detected as large text; none of these contain a person's name.
PROTECTED_ROOM_LABELS = (
    (0.117, 0.198, 0.174, 0.230),  # "Project 2"
    (0.751, 0.671, 0.812, 0.704),  # "Project 7"
    (0.907, 0.888, 0.976, 0.921),  # "Project 31"
)


def fix_posters(src: Path, dst: Path) -> None:
    import numpy as np
    from scipy import ndimage

    img = Image.open(src).convert("RGB")
    arr = np.asarray(img).astype(int)
    white = (
        (arr[:, :, 0] > WHITE_CUTOFF)
        & (arr[:, :, 1] > WHITE_CUTOFF)
        & (arr[:, :, 2] > WHITE_CUTOFF)
    )

    labelled, count = ndimage.label(white)
    slices = ndimage.find_objects(labelled)

    small_ids = []
    for idx, sl in enumerate(slices, start=1):
        if sl is None:
            continue
        h = sl[0].stop - sl[0].start
        w = sl[1].stop - sl[1].start
        if h <= NAME_GLYPH_MAX_H and w <= NAME_GLYPH_MAX_W:
            small_ids.append((idx, sl))

    big = np.zeros_like(white)
    for idx, sl in enumerate(slices, start=1):
        if sl is None:
            continue
        h = sl[0].stop - sl[0].start
        if NAME_GLYPH_MAX_H < h <= LABEL_MAX_H * 2:
            big[sl] |= labelled[sl] == idx

    # A handful of room labels are rendered faintly enough that they fragment
    # into glyph-sized pieces; protect those explicitly.
    rows, cols = arr.shape[0], arr.shape[1]
    for x0, y0, x1, y1 in PROTECTED_ROOM_LABELS:
        big[int(y0 * rows) : int(y1 * rows), int(x0 * cols) : int(x1 * cols)] = True

    # Anti-aliasing splits the large "Project NN" room labels into a few
    # glyph-sized fragments.  Exclude any small component that sits inside a
    # room label's neighbourhood so those labels stay legible.
    near_big = ndimage.binary_dilation(big, structure=np.ones((9, 21), bool))

    small = np.zeros_like(white)
    for idx, sl in small_ids:
        component = labelled[sl] == idx
        if (component & near_big[sl]).any():
            continue
        small[sl] |= component

    # Join the glyphs of a single label into one run without bridging to the
    # (larger) room labels above and below.
    joined = ndimage.binary_dilation(small, structure=np.ones((3, 9), bool), iterations=2)

    redact = np.zeros_like(white)
    blobs, _ = ndimage.label(joined)
    for idx, sl in enumerate(ndimage.find_objects(blobs), start=1):
        if sl is None:
            continue
        h = sl[0].stop - sl[0].start
        w = sl[1].stop - sl[1].start
        if w >= LABEL_MIN_W and h <= LABEL_MAX_H:
            y0 = max(0, sl[0].start - 2)
            y1 = min(arr.shape[0], sl[0].stop + 2)
            x0 = max(0, sl[1].start - 3)
            x1 = min(arr.shape[1], sl[1].stop + 3)
            redact[y0:y1, x0:x1] = True

    pixelated = img.resize(
        (max(1, img.width // POSTER_PIXEL_BLOCK), max(1, img.height // POSTER_PIXEL_BLOCK)),
        Image.BILINEAR,
    ).resize(img.size, Image.NEAREST)

    mask = Image.fromarray((redact * 255).astype("uint8"), mode="L")
    out = Image.composite(pixelated, img, mask)
    out.save(dst, optimize=True)
    print(
        f"wrote {dst.relative_to(REPO_ROOT)} ({img.width}x{img.height}); "
        f"{int(redact.any(axis=1).sum())} redacted rows"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fig-dir", type=Path, default=FIG_DIR)
    args = parser.parse_args()

    fix_world_map(args.fig_dir / "world_map.png", args.fig_dir / "world_map_readable.png")
    fix_gathertown(
        args.fig_dir / "gathertown.png", args.fig_dir / "gathertown_redacted.png"
    )
    fix_posters(args.fig_dir / "posters.png", args.fig_dir / "posters_redacted.png")


if __name__ == "__main__":
    main()
