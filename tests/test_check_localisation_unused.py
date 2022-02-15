##########################
# Test script to check for unused loc keys
# Takes around 1.5h for KR
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
from ..test_classes.generic_test_class import TestClass
import logging
import pytest
FILES_TO_SKIP = ["KR_Vanilla_Override_l_english", "ideas_l_english", "music", "lar_operations", "autonomy_l", "decisions_l_english"
                 "events_l_english", "factions_l_english", "focus_l_english", "technology_sharing", "00_General_l_english",
                 "War_l_english", "war_l_english", "00_Map_Victory", "00_Map_States", "_Equip", "_Adjacency", "st_manager",
                 "Loading_Tips"]

DIRECTORIES_TO_SKIP = ['\\gfx\\', '\\history\\', '\\music\\', '\\portraits\\', '\\ai_', '\\defines\\', '\\events\\', '\\decisions\\']


@pytest.mark.skip(reason="Takes 1.5h per run")
def test_check_unused_loc_keys(test_runner: object):
    test = TestClass()
    filepath = f'{test_runner.full_path_to_mod}localisation\\'
    filepath_general = test_runner.full_path_to_mod
    filepath_events = f'{test_runner.full_path_to_mod}events\\'
    filepath_decisions = f'{test_runner.full_path_to_mod}common\\decisions\\'
    loc_keys = {}
    # Prepare the dict with all loc keys
    for filename in glob.iglob(filepath + '**/*.yml', recursive=True):
        if test.skip_files(files_to_skip=FILES_TO_SKIP, filename=filename):
            continue

        text_file = test.open_text_file(filename)

        text_file_splitted = text_file.lower().split('\n')[1:]
        for line in range(len(text_file_splitted)):
            current_line = text_file_splitted[line]
            if "#" not in current_line and [i for i in ['', ' ', 'l_english:'] if i == current_line] == []:
                if [i for i in ['_adj:', '_def:', '_liberal:', '_democrat:', '_syndicalist:', '_totalist:',
                                '_conservative:', '_autocrat:', '_populist:', '_socialist:', '_party_long:', '_party:',
                                '_tooltip:', '_blocked:', '_not:', '_desc:'] if i in current_line] == []:
                    if '_desc:' not in current_line:
                        loc_keys[current_line.split(':')[0].strip()] = 0

    logging.debug(f'{len(loc_keys)} loc keys found (excluding _desc ones)')
    not_encountered_keys = loc_keys.copy()
    # Check events first
    for filename in glob.iglob(filepath_events + '**/*.txt', recursive=True):
        text_file = test.open_text_file(filename)

        for key in not_encountered_keys:
            if key in text_file.lower():
                loc_keys.pop(key)
        not_encountered_keys = loc_keys.copy()
    # Then check decisions
    for filename in glob.iglob(filepath_decisions + '**/*.txt', recursive=True):
        text_file = test.open_text_file(filename)

        for key in not_encountered_keys:
            if key in text_file.lower():
                loc_keys.pop(key)
        not_encountered_keys = loc_keys.copy()
    # Then check other files
    for filename in glob.iglob(filepath_general + '**/*.txt', recursive=True):
        if test.skip_files(files_to_skip=FILES_TO_SKIP, filename=filename):
            continue

        text_file = test.open_text_file(filename)

        for key in not_encountered_keys:
            if key in text_file.lower():
                loc_keys.pop(key)
        not_encountered_keys = loc_keys.copy()

    # The report is created in external file on the desktop since 5k+ lines for log is a bit too much
    unused_loc_keys = [i for i in loc_keys.keys() if loc_keys[i] == 0]
    if unused_loc_keys != {}:
        logging.warning("There are unused loc keys, check 'loc_files_issues.txt' on desktop")
        with open(f"C:\\Users\\{test_runner.username}\\Desktop\\loc_files_issues.txt", "a") as create_var:
            for i in unused_loc_keys:
                create_var.write(f"\n- [ ] {i}")
        logging.warning(f'{len(unused_loc_keys)} unused loc keys.')
        raise AssertionError("There are unused loc keys, check 'loc_files_issues.txt' on desktop")
