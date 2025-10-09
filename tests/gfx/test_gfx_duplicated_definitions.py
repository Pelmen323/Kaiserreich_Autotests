##########################
# Test script to check if gfx objects are defined more than once
# By Pelmen, https://github.com/Pelmen323
##########################
from collections import Counter
from test_classes.gfx_class import GFX, GFXFactory
from test_classes.generic_test_class import (
    ResultsReporter,
)


def test_duplicated_gfx_definitions(test_runner: object):
    GFX_code = GFX.get_all_gfx_objects_code(test_runner=test_runner, lowercase=False)
    gfx_names_counter = Counter()
    results = []

    for i in GFX_code:
        gfx = GFXFactory(i)
        gfx_names_counter[gfx.name] += 1

    for name in gfx_names_counter:
        cnt = gfx_names_counter[name]
        if cnt > 1:
            results.append(f"{name} - is defined {cnt} times")

    results = sorted(set(results))
    ResultsReporter.report_results(results=results, message="Images with duplicated definitions are found. Only latest instance will be used by the game, so it is safe to remove duplicates")
