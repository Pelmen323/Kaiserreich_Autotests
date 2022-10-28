##########################
# Test script to check for unused loc keys
# Takes around 1.5h for KR
# By Pelmen, https://github.com/Pelmen323
##########################
import glob

import pytest

from ..test_classes.generic_test_class import FileOpener, ResultsReporter
from ..test_classes.localization_class import Localization


@pytest.mark.skip(reason="Takes 1.5h per run")
def test_check_unused_loc_keys(test_runner: object):
    filepath_general = test_runner.full_path_to_mod
    loc_keys = Localization.get_all_loc_keys(test_runner=test_runner)
    results = {}
    exceptions = ['_adj', '_def', '_liberal', '_democrat', '_syndicalist', '_totalist',
                  '_conservative', '_autocrat', '_populist', '_socialist', '_party_long', '_party', '_blocked', '_not', '_desc']
    for key in loc_keys:
        if len([i for i in exceptions if i in key]) == 0:
            results[key] = 0

    for filename in glob.iglob(filepath_general + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)
        results_list = [i for i in results if results[i] == 0]
        print(len(results_list))

        for key in results_list:
            if key in text_file:
                results[key] = 1
                break

    results_to_report = [i for i in results if results[i] == 0]
    ResultsReporter.report_results(results=results_to_report, message="Unused loc keys were encountered. Check console output")
