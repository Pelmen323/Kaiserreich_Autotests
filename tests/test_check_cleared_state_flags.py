##########################
# Test script to check for state flags that are cleared but not set
# If flag is not set via "set_state_flag" at least once, it will appear in test results
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import pytest
import re
from timeit import default_timer as timer
from .imports.file_functions import open_text_file
FILEPATH = "C:\\Users\\VADIM\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\Kaiserreich Dev Build\\"


@pytest.mark.parametrize("filepath", [FILEPATH])
def test_check_cleared_state_flags(filepath: str):
    print("The test is started. Please wait...")
    start = timer()
    state_flags = {}
# Part 1 - get the dict of all global flags
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        try:
            text_file = open_text_file(filename)
        except Exception as ex:
            print(f'Skipping the file {filename}')
            print(ex)
            continue

        if 'clr_state_flag =' in text_file:
            state_flags_in_file = re.findall('clr_state_flag = \\b\\w*\\b', text_file)
            if len(state_flags_in_file) > 0:
                for flag in state_flags_in_file:
                    flag = flag[17:]
                    flag = flag.strip()
                    state_flags[flag] = 0


# Part 2 - count the number of flag occurrences
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        try:
            text_file = open_text_file(filename)
        except Exception as ex:
            print(f'Skipping the file {filename}')
            print(ex)
            continue

        if 'set_state_flag =' in text_file:
            for flag in state_flags.keys():
                state_flags[flag] += text_file.count(f'set_state_flag = {flag}')
                state_flags[flag] += text_file.count(f'set_state_flag = {{ flag = {flag}')

# Part 4 - throw the error if flag is not used
    results = [i for i in state_flags if state_flags[i] == 0]
    if results != []:
        print("Following state flags are cleared but not set via set_state_flag! Recheck them")
        for i in results:
            print(i)
        raise AssertionError("State flags that are cleared but not set were encountered! Check console output")
    end = timer()
    print(f"The test is finished in {round(end-start, 3)} seconds!")
