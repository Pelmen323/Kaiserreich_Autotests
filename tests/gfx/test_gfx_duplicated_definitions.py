##########################
# Test script to check if gfx objects are defined more than once
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re
from pathlib import Path

from test_classes.generic_test_class import (
    FileOpener,
    ResultsReporter,
)


def test_check_duplicated_gfx(test_runner: object):
    gfx_path = str(Path(test_runner.full_path_to_mod) / "interface") + "/"
    gfx_entities = []
    results = []

    for filename in glob.iglob(gfx_path + '**/*.gfx', recursive=True):
        text_file = FileOpener.open_text_file(filename, lowercase=False)

        matches = re.findall(r'name = \"GFX_(.*?)\"', text_file)
        if len(matches) > 0:
            for match in matches:
                gfx_entities.append(match)

    for i in gfx_entities:
        if gfx_entities.count(i) > 1:
            results.append(f"GFX_{i} - is defined more than once")

    results = sorted(set(results))
    ResultsReporter.report_results(results=results, message="Images with duplicated definitions are found.")
