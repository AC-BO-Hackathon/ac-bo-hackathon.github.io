"""Generate the graphical abstract for the Digital Discovery submission.

The graphical abstract reuses the hackathon world map (``latex/figures/world_map.png``)
but simplifies it for use as a stand-alone visual:

* the two inset bar charts (and their axis labels/titles) are cropped away, and
* the affiliation legend in the top-right corner is masked out,

so that only the clean world map with the participant locations remains. A
Bayesian-optimization surrogate model -- the predictive mean and a (mostly
transparent) uncertainty band of a Gaussian-process posterior -- is then
overlaid on top of the map to convey the theme of the hackathon: a global
community advancing Bayesian optimization. The surrogate is a *real* GP fit
with the Ax Platform (`ax-platform`); the observations are treated as
noiseless, so the band collapses at the measured points and widens away from
them, illustrating how Bayesian optimization reasons about uncertainty.

The output respects the Royal Society of Chemistry / Digital Discovery
graphical-abstract guidelines: it is a landscape image (graphical abstracts are
*not* required to be square; they are reproduced at up to 8 cm wide by 4 cm
high) saved well above the 300 dpi minimum.

Running the script writes ``latex/figures/graphical-abstract.png``.
"""

import os

import numpy as np
import torch
from ax.api.client import Client
from ax.api.configs import RangeParameterConfig
from PIL import Image, ImageFilter
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Resolve paths relative to the repository root so the script can be run from
# anywhere.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
SOURCE_MAP = os.path.join(ROOT_DIR, "latex", "figures", "world_map.png")
OUTPUT = os.path.join(ROOT_DIR, "latex", "figures", "graphical-abstract.png")

# Fraction of the image height kept from the top. The inset bar charts (and
# their titles/axis labels) live in the bottom portion of the figure, so
# cropping there removes them while keeping the populated world map.
CROP_BOTTOM_FRACTION = 0.595

# The legend sits in the top-right corner over the Siberian landmass. Its
# bounding box (fractions of width/height) is reconstructed by copying the
# adjacent terrain from its left so the land continues naturally.
LEGEND_BOX = (0.860, 0.020, 1.000, 0.130)


def load_simplified_map():
    """Return the world map as an RGB array with insets and legend removed."""
    image = Image.open(SOURCE_MAP).convert("RGB")
    width, height = image.size

    # Mask the legend before cropping so the box coordinates refer to the full
    # image. The patch immediately to the left of the legend (the same rows) is
    # copied over it, continuing the surrounding terrain, and the seams are
    # feathered with a light blur.
    pixels = np.asarray(image).copy()
    x0 = int(LEGEND_BOX[0] * width)
    y0 = int(LEGEND_BOX[1] * height)
    x1 = int(LEGEND_BOX[2] * width)
    y1 = int(LEGEND_BOX[3] * height)

    box_width = x1 - x0
    source = pixels[y0:y1, x0 - box_width : x0]
    pixels[y0:y1, x0:x1] = source

    # Feather only the two interior seams (left and bottom edges); the top and
    # right edges coincide with the image border. Blurring a thin band keeps the
    # copied terrain crisp while hiding the joins.
    band = max(2, int(0.004 * width))

    def blur_band(sx0, sy0, sx1, sy1):
        sx0, sy0 = max(0, sx0), max(0, sy0)
        sx1, sy1 = min(width, sx1), min(height, sy1)
        strip = Image.fromarray(pixels[sy0:sy1, sx0:sx1]).filter(
            ImageFilter.GaussianBlur(radius=band)
        )
        pixels[sy0:sy1, sx0:sx1] = np.asarray(strip)

    blur_band(x0 - band, y0, x0 + band, y1)  # left seam
    blur_band(x0 - band, y1 - band, x1, y1 + band)  # bottom seam

    crop_height = int(CROP_BOTTOM_FRACTION * height)
    return pixels[:crop_height, :, :]


def build_surrogate(seed=7):
    """Fit a real Gaussian-process surrogate with Ax and return its posterior.

    A handful of noiseless observations of a smooth latent function are
    attached to an :class:`ax.api.client.Client`. Ax fits a Gaussian-process
    surrogate (via BoTorch) which is then queried on a dense grid. Because the
    observations are reported with zero noise, the predictive standard
    deviation collapses at the measured points and grows away from them.

    Returns the test grid, posterior mean, and posterior standard deviation.
    """
    np.random.seed(seed)
    torch.manual_seed(seed)
    rng = np.random.default_rng(seed)

    def latent(x):
        return np.sin(2.6 * x) + 0.55 * np.sin(5.5 * x + 0.8)

    lower, upper = 0.0, 6.5
    x_train = np.array([0.4, 1.2, 2.1, 3.0, 3.9, 4.8, 5.6, 6.1])
    y_train = latent(x_train) + rng.normal(scale=0.05, size=x_train.shape)

    client = Client()
    client.configure_experiment(
        parameters=[
            RangeParameterConfig(
                name="x", bounds=(lower, upper), parameter_type="float"
            )
        ]
    )
    client.configure_optimization(objective="y")
    # Move past the random initialization phase immediately so the predictive
    # Gaussian-process node is used, and reuse our attached observations.
    client.configure_generation_strategy(
        initialization_budget=2,
        initialize_with_center=False,
        initialization_random_seed=seed,
    )

    for xi, yi in zip(x_train, y_train):
        trial_index = client.attach_trial(parameters={"x": float(xi)})
        # A standard error of 0 marks the observation as noiseless.
        client.complete_trial(
            trial_index=trial_index, raw_data={"y": (float(yi), 0.0)}
        )

    # Generating a trial fits the Gaussian-process surrogate that ``predict``
    # subsequently queries.
    client.get_next_trials(max_trials=1)

    x_test = np.linspace(lower, upper, 400)
    predictions = client.predict(points=[{"x": float(x)} for x in x_test])
    mean = np.array([p["y"][0] for p in predictions])
    std = np.array([p["y"][1] for p in predictions])
    return x_test, mean, std


def main():
    map_array = load_simplified_map()
    height, width, _ = map_array.shape

    fig = plt.figure(figsize=(width / 300, height / 300), dpi=300)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.imshow(map_array, aspect="auto")
    ax.set_axis_off()

    # Overlay axes spanning the full figure; the surrogate is drawn in a
    # horizontal band so it reads across the map without hiding it.
    overlay = fig.add_axes([0, 0, 1, 1])
    overlay.set_axis_off()
    overlay.set_xlim(0, 1)
    overlay.set_ylim(0, 1)
    overlay.patch.set_alpha(0)

    x_test, mean, std = build_surrogate()

    # Map model coordinates into the [0, 1] overlay frame. The band is centred
    # vertically and uses a moderate amplitude so it stays legible.
    def to_x(x):
        return (x - x_test.min()) / (x_test.max() - x_test.min())

    band_center = 0.52
    band_amplitude = 0.16

    def to_y(y):
        return band_center + band_amplitude * y

    accent = "#0b3d91"  # deep blue, harmonises with the ocean

    overlay.fill_between(
        to_x(x_test),
        to_y(mean - 2 * std),
        to_y(mean + 2 * std),
        color=accent,
        alpha=0.18,
        linewidth=0,
        zorder=2,
    )
    overlay.plot(
        to_x(x_test),
        to_y(mean),
        color=accent,
        alpha=0.85,
        linewidth=3.0,
        zorder=3,
    )

    fig.savefig(OUTPUT, dpi=300)
    plt.close(fig)
    print("Wrote", OUTPUT)


if __name__ == "__main__":
    main()
