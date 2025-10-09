##########################
# Test script to check if there are multiple gfx objects that refer to the same file
# For now - portraits only
# For tech icons this is acceptable because they have to be re-defined for every tag, and DLC/non-DLC textures will also overlap
# By Pelmen, https://github.com/Pelmen323
##########################
from collections import Counter
from test_classes.gfx_class import GFX, GFXFactory

from test_classes.generic_test_class import (
    ResultsReporter,
)

PATHS_TO_SKIP = ["/generic/", "/Generic/", "/gui/", "/aces/"]
PATHS_TO_INCLUDE = ["/leaders/", "/event_pictures/", "/advisors/"]
FALSE_POSITIVES = [
    "leader_unknown.dds",
]


def test_duplicated_gfx_texturefiles(test_runner: object):
    GFX_code = GFX.get_code(test_runner=test_runner, lowercase=False)
    gfx_texturefiles_counter = Counter()
    results = []
    for i in GFX_code:
        gfx = GFXFactory(i)
        if any([e for e in PATHS_TO_SKIP if e in gfx.texturefile]):
            continue
        if any([e for e in PATHS_TO_INCLUDE if e in gfx.texturefile]):
            gfx_texturefiles_counter[gfx.texturefile] += 1

    for t in gfx_texturefiles_counter:
        cnt = gfx_texturefiles_counter[t]
        if cnt > 1 and not any([i for i in FALSE_POSITIVES if i in t]):
            results.append(f"{t} - is referred to {cnt} times")

    ResultsReporter.report_results(results=results, message="Images with duplicated texturefiles are found. If possible, reuse GFX objects instead of duplicating them")
