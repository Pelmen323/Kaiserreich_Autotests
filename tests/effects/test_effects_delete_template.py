##########################
# Test script to check if `delete_unit_template_and_units` effect deletes template that is different than the one checked
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
import re

from test_classes.generic_test_class import FileOpener, ResultsReporter


def test_effects_delete_template(test_runner: object):
    filepath = test_runner.full_path_to_mod
    pattern = re.compile(r'(.*\n)\t+(delete_unit_template_and_units = .*?template = (".*?"))')
    results = []

    for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
        text_file = FileOpener.open_text_file(filename, lowercase=False)

        if "delete_unit_template_and_units" in text_file:
            pattern_matches = pattern.findall(text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    if f"has_template = {match[2]}" not in match[0] and "has_template" in match[0]:
                        results.append(f"{match[1]} - {os.path.basename(filename)}")

    ResultsReporter.report_results(results=results, message="delete_unit_template_and_units deletes template that is different than the one checked.")
