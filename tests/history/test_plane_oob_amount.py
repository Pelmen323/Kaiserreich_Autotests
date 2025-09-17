##########################
# Test script to check that scripted airwings size is <=100
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
import re

from test_classes.generic_test_class import FileOpener, ResultsReporter


def test_advisors_removal(test_runner: object):
    filepath = f'{test_runner.full_path_to_mod}history\\units'
    results = []

    for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
        if 'air' not in filename:
            continue
        text_file = FileOpener.open_text_file(filename)

        if "amount =" in text_file:
            pattern_matches = re.findall("amount = (\S+)", text_file, flags=re.DOTALL | re.MULTILINE)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    if int(match) > 100:
                        results.append((int(match), os.path.basename(filename)))

    ResultsReporter.report_results(results=results, message="Wings with >100 planes were encountered.")
