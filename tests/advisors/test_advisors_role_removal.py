##########################
# Test script to check for advisors removal that are removed without special effect
# Causes crashes when removing roles that are not added to characters
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
import re
import pytest

from test_classes.generic_test_class import FileOpener, ResultsReporter


@pytest.mark.smoke
@pytest.mark.kr_specific
def test_advisors_role_removal(test_runner: object):
    filepath = test_runner.full_path_to_mod
    results = []

    for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
        if '00_character_scripted_effects' in filename:
            continue
        text_file = FileOpener.open_text_file(filename)

        if "remove_advisor_role" in text_file:
            pattern_matches = re.findall(r'^(\t*?)remove_advisor_role = (\{.*?^\1\})', text_file, flags=re.DOTALL | re.MULTILINE)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[1].replace('\t', '').replace('\n', '  ')
                    results.append(f"remove_advisor_role = {match} - {os.path.basename(filename)}")

    ResultsReporter.report_results(results=results, message="Advisor role removal without special effect is encountered, please use only special effects from 00_character_scripted_effects.txt to remove advisors")
