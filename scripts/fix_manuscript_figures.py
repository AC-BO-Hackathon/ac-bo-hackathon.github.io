"""Apply the figure corrections requested by the Digital Discovery data reviewer.

Three fixes are applied, all regenerated from the committed source images so the
result is reproducible:

1. ``world_map.png`` (Fig. 2) -- "the black text which falls above the map can be
   difficult to read".  The two inset histograms are drawn on top of the world
   map, so their axis labels and panel titles sit directly on the map imagery.
   We add a thin white stroke around those black glyphs.

   The text drawn over the map -- the two panel titles, the "Frequency" axis
   labels and the y-axis tick numbers -- is outlined *typographically* rather
   than by tracing dark pixels.  Each of those labels is a known string set in
   the figure's own face (DejaVu Sans, matplotlib's default), so we re-set it,
   fit it to the image by cross-correlation to recover its size and position,
   and snap each glyph onto the ink it matches.  The letterform itself then
   defines the halo.  This is what tracing could not do: a coastline running
   through the "o" of "Distribution", or the Antarctic coastline running into
   the left panel's "0", is indistinguishable from the letter when all you have
   is a mask of dark pixels -- the letter goes unoutlined and the map line gets
   an outline of its own.  Working from the typography, only the characters are
   haloed, dots over "i" included, and the dashed country border that happens to
   place a dot above the "n" of "Distribution" is not mistaken for one.

   The x-axis category labels sit on the white Antarctic band rather than on
   imagery, so they are found as dark connected components, sized against the
   median component of the band.  The halo is opaque white with no feathering,
   so the outline cannot read as gray.  The map underneath is otherwise
   untouched, and the plot is not regenerated (the underlying survey data are
   not redistributable at participant granularity).

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

# The text that is drawn over the map, as typography: the string, its rotation,
# a fractional (x0, y0, x1, y1) box to look for it in, and the range of font
# sizes to try (source pixels).  Boxes are fractional so the script keeps
# working if the figure is re-exported at a different resolution; each is
# searched with MAP_FIT_MARGIN px of slack, so they only need to be roughly
# right.  Every string here is set by matplotlib in DejaVu Sans, the same face
# the script re-sets it in.
MAP_TEXT_LABELS = (
    # Panel titles.
    ("Country Distribution", 0, (0.180, 0.575, 0.345, 0.635), (92, 110)),
    ("Affiliation Distribution", 0, (0.678, 0.575, 0.855, 0.635), (92, 110)),
    # Left panel: y-axis label and tick numbers.
    ("Frequency", 90, (0.0097, 0.6866, 0.0204, 0.7900), (78, 100)),
    ("40", 0, (0.0244, 0.6555, 0.0378, 0.6712), (78, 96)),
    ("30", 0, (0.0248, 0.7002, 0.0378, 0.7160), (78, 96)),
    ("20", 0, (0.0247, 0.7452, 0.0376, 0.7607), (78, 96)),
    ("10", 0, (0.0252, 0.7900, 0.0378, 0.8056), (78, 96)),
    ("0", 0, (0.0321, 0.8339, 0.0390, 0.8503), (78, 96)),
    # Right panel.
    ("Frequency", 90, (0.5052, 0.6866, 0.5158, 0.7900), (78, 100)),
    ("100", 0, (0.5213, 0.6590, 0.5410, 0.6748), (78, 96)),
    ("75", 0, (0.5284, 0.7035, 0.5410, 0.7189), (78, 96)),
    ("50", 0, (0.5281, 0.7468, 0.5410, 0.7624), (78, 96)),
    ("25", 0, (0.5281, 0.7910, 0.5408, 0.8066), (78, 96)),
    ("0", 0, (0.5352, 0.8348, 0.5412, 0.8503), (78, 96)),
)

# The x-axis category labels underneath both panels.  These are set over the
# white Antarctic band rather than over imagery, so a plain ink trace is enough
# and there is no need to enumerate the country and affiliation names.
X_LABEL_BAND = (0.000, 0.848, 1.000, 1.000)

# Where to find the face the figure was set in.
FONT_CANDIDATES = (
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/matplotlib/mpl-data/fonts/ttf/DejaVuSans.ttf",
    "/Library/Fonts/DejaVuSans.ttf",
)

# Fitting a label: how far outside its box to search, how far each glyph may
# then be nudged to snap onto its ink, and how good the final overlap must be.
# The score is 1.0 for a perfect match and 0.0 when half the re-set glyph falls
# on background; every label in the committed figure scores above 0.90, so the
# floor only fires if the figure is re-exported in another face or at another
# aspect ratio, rather than letting a misplaced halo through unnoticed.
MAP_FIT_MARGIN = 50
GLYPH_SNAP = 3
MIN_FIT_SCORE = 0.85
# A glyph in the x-axis band is a dark connected component of roughly this size
# (source pixels at the committed 7290x4113 resolution; the figure is ~1000 dpi,
# so a 62 px glyph is about 4.5 pt on the page).  The axis spine and the panel
# frames are far wider and are left alone.
INK_CUTOFF = 110  # luminance below which a pixel counts as glyph ink
GLYPH_MIN_H, GLYPH_MAX_H = 12, 95
GLYPH_MIN_W, GLYPH_MAX_W = 6, 130
# The band is set in one size, so the median accepted component is a good
# yardstick; anything much shorter is a speck rather than a letter.
MIN_REL_HEIGHT = 0.40
# The label text is pure black.  Only pixels darker than AA_LIGHT are treated as
# (partial) ink, which keeps the background out of the coverage map; without
# this the background itself was picked up at low opacity and re-composited as a
# gray ring around the text.
AA_LIGHT = 130
AA_DARK = 20
AA_MARGIN = 3  # px around a glyph core searched for its anti-aliased edge
# Halo half-width in source pixels.  About 15% of the glyph height: enough to
# separate the ink from the imagery at print size, small enough that the counters
# of "0"/"o"/"e" stay open and the outline does not read as a filled plate.
STROKE_RADIUS = 9


def _font_path() -> str:
    for candidate in FONT_CANDIDATES:
        if Path(candidate).exists():
            return candidate
    try:  # matplotlib ships the same face
        import matplotlib

        mpl = Path(matplotlib.get_data_path()) / "fonts" / "ttf" / "DejaVuSans.ttf"
        if mpl.exists():
            return str(mpl)
    except ImportError:
        pass
    raise SystemExit(
        "DejaVuSans.ttf not found -- install fonts-dejavu-core (or matplotlib); "
        "the Fig. 2 text is outlined from its own typography, not traced."
    )


def _render_text(text: str, size: int, angle: int, font_path: str):
    """Set ``text`` as an anti-aliased coverage map, rotated by ``angle``."""
    import numpy as np
    from PIL import ImageDraw, ImageFont

    font = ImageFont.truetype(font_path, size)
    x0, y0, x1, y1 = font.getbbox(text)
    pad = GLYPH_SNAP + 3  # room for the per-glyph snap below
    canvas = Image.new("L", (x1 - x0 + 2 * pad, y1 - y0 + 2 * pad), 0)
    ImageDraw.Draw(canvas).text((pad - x0, pad - y0), text, fill=255, font=font)
    coverage = np.asarray(canvas).astype(np.float32) / 255.0
    if angle:
        coverage = np.ascontiguousarray(np.rot90(coverage, k=angle // 90))
    return coverage


def _place(coverage, ink, box, margin: int):
    """Slide ``coverage`` over ``box`` and return its best (y, x) and score.

    The score rewards a re-set pixel that lands on ink and penalises one that
    lands on background, so it is maximal for the true position and size rather
    than for whichever candidate simply covers the most ink.
    """
    import numpy as np
    from scipy.signal import fftconvolve

    h, w = ink.shape
    y0, x0, y1, x1 = box
    y0 = max(0, y0 - margin)
    x0 = max(0, x0 - margin)
    y1 = min(h, y1 + margin)
    x1 = min(w, x1 + margin)
    region = ink[y0:y1, x0:x1]
    glyph = (coverage > 0.5).astype(np.float32)
    if glyph.shape[0] > region.shape[0] or glyph.shape[1] > region.shape[1]:
        return None, -1.0
    overlap = fftconvolve(region, glyph[::-1, ::-1], mode="valid")
    score = (2.0 * overlap - glyph.sum()) / glyph.sum()
    flat = int(np.argmax(score))
    dy, dx = np.unravel_index(flat, score.shape)
    return (y0 + int(dy), x0 + int(dx)), float(score.flat[flat])


def _snap_glyphs(coverage, origin, ink):
    """Nudge each re-set glyph by a few px onto the ink it corresponds to.

    A whole string is placed as one rigid block, so kerning differences between
    matplotlib's layout and ours accumulate over a long label.  Each glyph is
    therefore allowed a small independent shift.  Dots and accents are too small
    to localise on their own -- a dot from a dashed country border sits within a
    few px of the "i" of "Distribution" -- so they take the shift of the nearest
    full-size glyph instead of searching for their own.
    """
    import numpy as np
    from scipy import ndimage

    core = coverage > 0.5
    labelled, _ = ndimage.label(core)
    parts = ndimage.find_objects(labelled)
    areas = np.array([float((labelled[sl] == i + 1).sum()) for i, sl in enumerate(parts)])
    if not areas.size:
        return coverage
    full_size = areas >= 0.25 * float(np.median(areas))

    snapped = np.zeros_like(coverage)
    shifts: list[tuple[float, float, int, int]] = []  # cy, cx, dy, dx
    for i in np.argsort(-areas):  # biggest first, so dots can follow a letter
        sl = parts[i]
        glyph = labelled[sl] == i + 1
        gy, gx = origin[0] + sl[0].start, origin[1] + sl[1].start
        gh, gw = glyph.shape
        if full_size[i]:
            best, shift = -np.inf, (0, 0)
            for dy in range(-GLYPH_SNAP, GLYPH_SNAP + 1):
                for dx in range(-GLYPH_SNAP, GLYPH_SNAP + 1):
                    patch = ink[gy + dy : gy + dy + gh, gx + dx : gx + dx + gw]
                    if patch.shape != glyph.shape:
                        continue
                    hit = float((patch * glyph).sum())
                    if 2.0 * hit - glyph.sum() > best:
                        best, shift = 2.0 * hit - glyph.sum(), (dy, dx)
            shifts.append((gy + gh / 2, gx + gw / 2, *shift))
        else:
            cy, cx = gy + gh / 2, gx + gw / 2
            shift = min(
                shifts, key=lambda s: (s[0] - cy) ** 2 + (s[1] - cx) ** 2, default=(0, 0, 0, 0)
            )[2:]

        ys = min(max(sl[0].start + shift[0], 0), coverage.shape[0] - gh)
        xs = min(max(sl[1].start + shift[1], 0), coverage.shape[1] - gw)
        patch = snapped[ys : ys + gh, xs : xs + gw]
        np.maximum(patch, coverage[sl] * glyph, out=patch)
    return snapped


def _typeset_coverage(ink, shape, font_path: str):
    """Coverage map of the labels drawn over the map, re-set from typography."""
    import numpy as np

    h, w = shape
    coverage = np.zeros(shape, np.float32)
    for text, angle, (fx0, fy0, fx1, fy1), (lo, hi) in MAP_TEXT_LABELS:
        box = (int(fy0 * h), int(fx0 * w), int(fy1 * h), int(fx1 * w))
        best = (-1.0, None, None)
        for size in range(lo, hi):
            rendered = _render_text(text, size, angle, font_path)
            origin, score = _place(rendered, ink, box, MAP_FIT_MARGIN)
            if score > best[0]:
                best = (score, origin, rendered)
        score, origin, rendered = best
        if origin is None or score < MIN_FIT_SCORE:
            raise SystemExit(
                f"could not locate {text!r} in the figure (best overlap {score:.2f} "
                f"< {MIN_FIT_SCORE}); check MAP_TEXT_LABELS against the source image"
            )
        rendered = _snap_glyphs(rendered, origin, ink)
        gh, gw = rendered.shape
        patch = coverage[origin[0] : origin[0] + gh, origin[1] : origin[1] + gw]
        np.maximum(patch, rendered, out=patch)
    return coverage


def _traced_glyphs(lum, band):
    """Glyph mask for a band of text that sits on a plain background."""
    import numpy as np
    from scipy import ndimage

    h, w = lum.shape
    x0, y0, x1, y1 = band
    sl_y = slice(int(y0 * h), int(y1 * h))
    sl_x = slice(int(x0 * w), int(x1 * w))
    band_lum = lum[sl_y, sl_x]
    labelled, _ = ndimage.label(band_lum < INK_CUTOFF)

    candidates = []
    for idx, sl in enumerate(ndimage.find_objects(labelled), start=1):
        if sl is None:
            continue
        gh = sl[0].stop - sl[0].start
        gw = sl[1].stop - sl[1].start
        if GLYPH_MIN_H <= gh <= GLYPH_MAX_H and GLYPH_MIN_W <= gw <= GLYPH_MAX_W:
            candidates.append((idx, sl, gh))

    glyphs = np.zeros((h, w), bool)
    if not candidates:
        return glyphs, 0
    median_h = float(np.median([c[2] for c in candidates]))
    band_glyphs = np.zeros_like(band_lum, bool)
    kept = 0
    for idx, sl, gh in candidates:
        if gh < MIN_REL_HEIGHT * median_h:
            continue  # a speck, not a glyph
        band_glyphs[sl] |= labelled[sl] == idx
        kept += 1
    glyphs[sl_y, sl_x] = band_glyphs
    return glyphs, kept


def fix_world_map(src: Path, dst: Path) -> None:
    import numpy as np
    from scipy import ndimage

    img = Image.open(src).convert("RGB")
    w, h = img.size
    rgb = np.asarray(img).astype(np.float32)
    lum = np.asarray(img.convert("L")).astype(np.float32)
    ink = (lum < INK_CUTOFF).astype(np.float32)

    # 1. The labels drawn over the map are re-set from their own typography and
    #    fitted to the image, so the halo follows the letterform even where a
    #    coastline or a country border runs through the character.
    coverage = _typeset_coverage(ink, (h, w), _font_path())

    # 2. The x-axis category labels sit on the white Antarctic band; trace them,
    #    and take their coverage from the image so the original anti-aliasing is
    #    preserved.
    traced, kept = _traced_glyphs(lum, X_LABEL_BAND)
    near = ndimage.binary_dilation(traced, structure=_disk(AA_MARGIN))
    np.maximum(
        coverage,
        np.clip((AA_LIGHT - lum) / (AA_LIGHT - AA_DARK), 0.0, 1.0) * near,
        out=coverage,
    )

    # 3. Grow the coverage into a halo, paint it opaque white -- no feathering,
    #    so the outline never reads as gray -- and lay the black text back over
    #    it at its own coverage.
    halo = ndimage.binary_dilation(coverage > 0.15, structure=_disk(STROKE_RADIUS))
    a = coverage[..., None]
    out = np.where(halo[..., None], 255.0, rgb) * (1.0 - a)

    Image.fromarray(np.clip(out, 0, 255).astype("uint8")).save(dst, optimize=True)
    print(
        f"wrote {dst.relative_to(REPO_ROOT)} ({w}x{h}); "
        f"{len(MAP_TEXT_LABELS)} labels re-set, {kept} traced glyphs, "
        f"{100 * float(halo.mean()):.2f}% of pixels touched"
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
