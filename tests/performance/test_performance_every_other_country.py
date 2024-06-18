##########################
# Test script to check if `every_other_country` is used with `has_war_with = root` (this can be replaced with `every_enemy_country`)
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
import re

from test_classes.generic_test_class import FileOpener, ResultsReporter


def test_check_syntax_every_other_country(test_runner: object):
    filepath = test_runner.full_path_to_mod
    results = []

    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if 'every_other_country' in text_file:
            pattern_matches = re.findall("^(\\t*?)every_other_country = (\\{.*?^\\1\\})", text_file, flags=re.DOTALL | re.MULTILINE)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    if "\thas_war_with = root" in match[1]:
                        results.append((match[1], os.path.basename(filename)))

    ResultsReporter.report_results(results=results, message="This part can be replaced with every_enemy_country. Check console output")
