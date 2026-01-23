##########################
# Test script to check if loc line has mandatory 'l_xxx:' line
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
from pathlib import Path

from test_classes.generic_test_class import FileOpener, ResultsReporter


def test_localisation_mandatory_line(test_runner: object):
    filepath = str(Path(test_runner.full_path_to_mod) / "localisation") + "/"
    results = []
    for filename in glob.iglob(filepath + "**/*.yml", recursive=True):
        text_file = FileOpener.open_text_file(filename).split("\n")
        # Empty file
        if text_file == [""]:
            continue
        elif "l_english:" not in text_file:
            if "play_in_english" not in os.path.basename(filename) and "KR_models_submod" not in filename:
                results.append(f"{os.path.basename(filename)} l_xxx: line is absent")

    ResultsReporter.report_results(results=results, message="l_xxx: line is absent in localisation file.")
