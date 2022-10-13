##########################
# Test script to check for unused focus icons
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re

from ..test_classes.generic_test_class import FileOpener, ResultsReporter


def test_check_unused_focus_icons(test_runner: object):
    focus_icons_path = f'{test_runner.full_path_to_mod}interface\\KR_goals.gfx'
    focuses_path = f'{test_runner.full_path_to_mod}common\\national_focus\\'
    results = {}

    # Get list of all texticons
    text_file = FileOpener.open_text_file(focus_icons_path)

    matches = re.findall('name = \\"(gfx_.*)\\"', text_file)
    for match in matches:
        results[match] = 0

    for filename in glob.iglob(focuses_path + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename, lowercase=True)
        for i in results.keys():
            if f'icon = {i}' in text_file:
                results[i] += text_file.count(f'icon = {i}\n')

    print(sorted(results.items(), key=lambda x: -x[1]))
    results = [i for i in results.items() if i[1] == 0]
    ResultsReporter.report_results(results=results, message="Unused focus icons found. Check console output")
