##########################
# Test script to check that scripted airwings size is <=100
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
import re
from pathlib import Path

from test_classes.generic_test_class import FileOpener, ResultsReporter


def test_oob_airwing_size(test_runner: object):
    filepath = str(Path(test_runner.full_path_to_mod) / "history" / "units") + "/"
    results = []

    for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
        if "air" not in filename:
            continue
        text_file = FileOpener.open_text_file(filename)

        if "amount =" in text_file:
            pattern_matches = re.findall(r"amount = (\S+)", text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    if int(match) > 100:
                        results.append(f"{os.path.basename(filename)} - airwing with {int(match)} planes found")

    ResultsReporter.report_results(results=results, message="Wings with >100 planes were encountered. Airwings in hoi4 are limited to 100 planes")
