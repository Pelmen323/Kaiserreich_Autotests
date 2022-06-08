##########################
# Test script to check if invalid traits are used for corps commanders
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re
import os
from ..test_classes.generic_test_class import FileOpener, ResultsReporter
from ..data.fm_only_traits import fm_traits


def test_check_corps_commanders_with_unsupported_traits(test_runner: object):
    filepath = test_runner.full_path_to_mod
    results = []

    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if 'corps_commander = {' in text_file:
            pattern_matches = re.findall("^(\\t*?)corps_commander = (\\{.*?^\\1\\})", text_file, flags=re.DOTALL | re.MULTILINE)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    for trait in fm_traits:
                        if trait in match[1]:
                            results.append((match[1].replace('\t', '').replace('\n', '  '), trait, os.path.basename(filename)))

        if 'add_corps_commander_role = {' in text_file:
            pattern_matches = re.findall("^(\\t*?)add_corps_commander_role = (\\{.*?^\\1\\})", text_file, flags=re.DOTALL | re.MULTILINE)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    for trait in fm_traits:
                        if trait in match[1]:
                            results.append((match[1].replace('\t', '').replace('\n', '  '), trait, os.path.basename(filename)))

    ResultsReporter.report_results(results=results, message="Corps commanders with unsupported traits encountered. Check console output")
