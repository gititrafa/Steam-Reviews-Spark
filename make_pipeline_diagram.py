"""Draw Figure 1 of the Lab 2 report: the methodology pipeline.

The main notebook imports ``draw_pipeline`` and displays the saved image,
so the figure is regenerated whenever the notebook runs. Edit ``STEPS`` if
the methodology changes, so the diagram and Section 3.1 stay in sync.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

PRIMARY = '#2a78d6'  # same palette as the report figures
MUTED = '#52514e'
STAGE_FILL = '#f3f2ee'
BOX_FILL = '#ffffff'

# (step number, title, detail, x-center, y-center); coordinates in inches
STEPS = [
    (1, 'Load',
     'all_reviews.csv (42 GB)\nexplicit STRING schema,\nmultiLine CSV options',
     1.35, 3.0),
    (2, 'Stage',
     'one pass: try_cast types,\nreview length, English\nword sets -> Parquet',
     3.55, 3.0),
    (3, 'Explore',
     'profile all 24 columns,\nduplicates, flags,\ntime, games, languages',
     5.75, 3.0),
    (4, 'Clean and filter',
     'investigate nulls, keep one\nrow per review ID, drop\n'
     'missing appid / flag',
     7.95, 3.0),
    (5, 'RQ1: Games',
     'negative share for games\nwith >= 1,000 reviews;\ntop 15 and top 10',
     10.4, 4.4),
    (6, 'RQ2: Reviewer groups',
     'negative share by playtime\nband, review year, and\ntop 10 languages',
     10.4, 3.0),
    (7, 'RQ3: Complaint terms',
     'English reviews: ratio of\nnegative to positive share\n'
     'for words in >= 10,000',
     10.4, 1.6),
    (8, 'Report',
     'aggregated tables only\n-> pandas -> figures;\nanswer and recommend',
     12.85, 3.0),
]
STAGES = [
    ('Data preparation (Sections 4–6)', 0.25, 9.05),
    ('Analysis (Sections 7–9)', 9.2, 11.6),
    ('Reporting (Sections 10–12)', 11.75, 13.95),
]
BOX_WIDTH, BOX_HEIGHT = 2.0, 1.2


def _box(ax, number, title, detail, x, y):
    """Draw one step as a rounded box with a numbered title."""
    ax.add_patch(FancyBboxPatch(
        (x - BOX_WIDTH / 2, y - BOX_HEIGHT / 2), BOX_WIDTH, BOX_HEIGHT,
        boxstyle='round,pad=0.02,rounding_size=0.08',
        facecolor=BOX_FILL, edgecolor=PRIMARY, linewidth=1.4))
    ax.text(x, y + 0.36, f'{number}. {title}', ha='center', va='center',
            fontsize=9, fontweight='bold', color='#1d1d1b')
    ax.text(x, y - 0.13, detail, ha='center', va='center', fontsize=7.4,
            color=MUTED, linespacing=1.25)


def _arrow(ax, start, end):
    """Draw an arrow between two points."""
    ax.add_patch(FancyArrowPatch(
        start, end, arrowstyle='-|>', mutation_scale=11,
        color=MUTED, linewidth=1.1, shrinkA=0, shrinkB=0))


def draw_pipeline(path):
    """Draw the pipeline diagram and save it as a PNG image.

    Parameters
    ----------
    path : str
        Output file path, e.g. ``'figures/pipeline_overview.png'``.
    """
    fig, ax = plt.subplots(figsize=(14.2, 5.6))
    ax.set_xlim(0, 14.2)
    ax.set_ylim(0.3, 5.75)
    ax.axis('off')

    # Shaded background for each stage of the pipeline
    for label, left, right in STAGES:
        ax.add_patch(FancyBboxPatch(
            (left, 0.55), right - left, 4.9,
            boxstyle='round,pad=0.02,rounding_size=0.12',
            facecolor=STAGE_FILL, edgecolor='none'))
        ax.text((left + right) / 2, 5.22, label, ha='center', va='center',
                fontsize=9, fontweight='bold', color=MUTED)

    for number, title, detail, x, y in STEPS:
        _box(ax, number, title, detail, x, y)

    centers = {number: (x, y) for number, _, _, x, y in STEPS}
    half = BOX_WIDTH / 2
    # Steps 1 -> 4 run left to right
    for step in (1, 2, 3):
        (x0, y0), (x1, y1) = centers[step], centers[step + 1]
        _arrow(ax, (x0 + half, y0), (x1 - half, y1))
    # The cleaned table feeds the three research questions ...
    x4, y4 = centers[4]
    for step in (5, 6, 7):
        x, y = centers[step]
        _arrow(ax, (x4 + half, y4), (x - half, y))
    # ... whose aggregated results feed the report
    x8, y8 = centers[8]
    for step in (5, 6, 7):
        x, y = centers[step]
        _arrow(ax, (x + half, y), (x8 - half, y8))

    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)


if __name__ == '__main__':
    draw_pipeline('pipeline_overview.png')
