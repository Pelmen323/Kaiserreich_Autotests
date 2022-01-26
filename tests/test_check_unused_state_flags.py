##########################
# Test script to check for unused state flags
# If flag is not used via "has_state_flag" at least once, it will appear in test results
# Flags with values or variables (ROOT/THIS/FROM) should be added to false positives
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import pytest
import re
from .imports.file_functions import open_text_file, clear_false_positives_flags
from .imports.decorators import util_decorator
FILEPATH = "C:\\Users\\VADIM\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\Kaiserreich Dev Build\\"
FALSE_POSITIVES = ('ACW_important_state_CSA',     # Wavering momentum flags that are currently unused
                   'ACW_important_state_USA',
                   'ACW_important_state_TEX',
                   'ACW_important_state_PSA',
                   'ACW_important_state_NEE',
                   'was_core_of_ROM')             # ROM annex event


@pytest.mark.parametrize("false_positives", [FALSE_POSITIVES])
@pytest.mark.parametrize("filepath", [FILEPATH])
@util_decorator
def test_check_unused_state_flags(filepath: str, false_positives: tuple):
    state_flags = {}
# Part 1 - get the dict of all global flags
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        try:
            text_file = open_text_file(filename)
        except Exception as ex:
            print(f'Skipping the file {filename}')
            print(ex)
            continue

        if 'set_state_flag =' in text_file:
            state_flags_in_file = re.findall('set_state_flag = \\b\\w*\\b', text_file)
            if len(state_flags_in_file) > 0:
                for flag in state_flags_in_file:
                    flag = flag[17:]
                    flag = flag.strip()
                    state_flags[flag] = 0

            state_flags_in_file = re.findall('set_state_flag = \\{ flag = \\b\\w*\\b', text_file)
            if len(state_flags_in_file) > 0:
                for flag in state_flags_in_file:
                    flag = flag[26:]
                    flag = flag.strip()
                    state_flags[flag] = 0

# Part 2 - clear false positives and flags with variables:
    clear_false_positives_flags(flags_dict=state_flags, false_positives=false_positives)

# Part 3 - count the number of flag occurrences
    print(f'{len(state_flags)} set state flags were found')
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        try:
            text_file = open_text_file(filename)
        except Exception as ex:
            print(f'Skipping the file {filename}')
            print(ex)
            continue

        if 'has_state_flag =' in text_file:
            for flag in state_flags.keys():
                state_flags[flag] += text_file.count(f'has_state_flag = {flag}')
                state_flags[flag] += text_file.count(f'has_state_flag = {{ flag = {flag}')

# Part 4 - throw the error if flag is not used
    results = [i for i in state_flags if state_flags[i] == 0]
    if results != []:
        print("Following state flags are not checked via has_state_flag! Recheck them")
        for i in results:
            print(f'- [ ] {i}')
        print(f'{len(results)} unused state flags found.')
        raise AssertionError("Unused state flags were encountered! Check console output")
