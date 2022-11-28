"""Common hardcoded variables throughout the code."""

from .data import getAnnotationScoreDataset

# Number of decimals to the right of the decimal point
FLOATSCALE = 4

# Sixteenth notes
FRAMEBASENOTE = 32
FIXEDOFFSET = round(4.0 / FRAMEBASENOTE, FLOATSCALE)

DATASETSUMMARYFILE = "dataset_summary.tsv"

ANNOTATIONSCOREDUPLES, DATASPLITS = getAnnotationScoreDataset()
