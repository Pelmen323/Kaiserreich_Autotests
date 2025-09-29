##########################
# Test script to check if `add_resistance` has a valid tooltip
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
import re

from test_classes.generic_test_class import FileOpener, ResultsReporter
from test_classes.localization_class import Localization


def test_localisation_add_resistance_tooltip(test_runner: object):
    filepath = test_runner.full_path_to_mod
    loc_keys = Localization.get_all_loc_keys(test_runner=test_runner, lowercase=False)
    pattern = r'^(\t+)add_resistance_target = (\{\n.*?)^\1\}'
    results = []

    for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
        text_file = FileOpener.open_text_file(filename, lowercase=False)

        if "add_resistance_target = {" in text_file:
            pattern_matches = re.findall(pattern, text_file, flags=re.MULTILINE | re.DOTALL)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match_body = match[1]
                    if 'tooltip =' in match_body:
                        tt = re.findall(r'tooltip = ([^\t \n]+)', match_body)[0]
                        if tt in loc_keys:
                            value = loc_keys[tt]
                            if '$VALUE|=-%0$' not in value:
                                results.append(f"{tt} - {value} - missing $VALUE|=-%0$")
                        else:
                            results.append(f"{tt} - can't find the localisation key")
                    else:
                        x = match_body.replace('\n', ' ').replace('\t', '')
                        results.append(f"{x} - {os.path.basename(filename)} - missing tooltip")

    ResultsReporter.report_results(results=results, message="Add_resistance_target tooltip issues found")
