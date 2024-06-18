##########################
# Test script to check if state usage contains correct reference to loc
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
import re
import pytest

from difflib import SequenceMatcher

from test_classes.generic_test_class import FileOpener, ResultsReporter
from test_classes.localization_class import Localization


@pytest.mark.skip(reason="Backlog work")
def test_check_state_reference(test_runner: object):
    filepath = test_runner.full_path_to_mod
    filepath_to_states_loc = f'{test_runner.full_path_to_mod}localisation\\KR_common\\00 Map States l_english.yml'
    loc_keys = Localization.get_all_loc_keys(test_runner=test_runner, lowercase=False)
    results = []

# Part 1 - get the list of entities
    text_file = FileOpener.open_text_file(filepath_to_states_loc, lowercase=False)
    states_loc = {}
    target_lines = re.findall("STATE_\\d+: .*", text_file)
    for line in target_lines:
        state_id = line.split(':')[0].split("_")[1]
        state_name = line.split(':')[1].strip().strip('"')
        if "$" in state_name:
            state_name = loc_keys[state_name.strip("$")].strip('"')
        states_loc[state_id] = state_name

    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        if "Endonyms" in filename:
            continue
        text_file = FileOpener.open_text_file(filename, lowercase=False)

        if 'state = ' in text_file:
            pattern = r'\bstate = \d+.*'
            pattern_matches = re.findall(pattern, text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    if '#' in match:
                        state = re.findall(r'state = (\d+)', match)[0]
                        comment = re.findall(r'#.*', match)[0][1:].strip()
                        if states_loc[state].lower() not in comment.lower():
                            if SequenceMatcher(None, comment, states_loc[state]).ratio() > 0.5 and states_loc[state] == states_loc[state].encode(encoding='UTF-8').decode("utf-8"):
                                continue
                                # match_new = match.replace(comment, states_loc[state])
                                # text_file_new = text_file.replace(match, match_new)
                                # with open(filename, 'w', encoding="utf-8") as text_file_write:
                                #     text_file_write.write(text_file_new)
                            else:
                                results.append(f'{comment} - expected {states_loc[state]} - {match} - {os.path.basename(filename)}')

    ResultsReporter.report_results(results=sorted(results), message="Issues with state comments were encountered. Check console output")
