##########################
# Test script to check for advisors removal that are removed without special effect
# Causes crashes when removing roles that are not added to characters
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
import re

from test_classes.generic_test_class import FileOpener, ResultsReporter


def test_advisors_role_removal(test_runner: object):
    filepath = test_runner.full_path_to_mod
    pattern = re.compile(r"^(\t*?)remove_advisor_role = (\{.*?^\1\})", flags=re.DOTALL | re.MULTILINE)
    found_files = False
    results = []

    for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
        found_files = True
        if "00_character_scripted_effects" in filename:
            continue
        text_file = FileOpener.open_text_file(filename)

        if "remove_advisor_role" in text_file:
            pattern_matches = re.findall(pattern, text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[1].replace("\t", "").replace("\n", "  ")
                    results.append(f"remove_advisor_role = {match} - {os.path.basename(filename)}")

    assert found_files, f"No .txt files found matching pattern: {filepath}"
    ResultsReporter.report_results(results=results, message="Advisor role removal without special effect is encountered - use only effects from 00_character_scripted_effects.txt to remove advisors")
