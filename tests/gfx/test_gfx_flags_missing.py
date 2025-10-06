##########################
# Test script to check if all 3 flag versions are present in flags folder
##########################
import glob
import os
from pathlib import Path
from test_classes.generic_test_class import ResultsReporter


def test_gfx_flags_missing(test_runner: object):
    filepath = str(Path(test_runner.full_path_to_mod) / "gfx" / "flags") + "/"
    results = []

    for filename in glob.iglob(filepath + "**/*.tga", recursive=True):
        results.append(os.path.basename(filename))

    results = list(set([i for i in results if results.count(i) != 3]))

    ResultsReporter.report_results(results=results, message="Missing flags were encountered.")
