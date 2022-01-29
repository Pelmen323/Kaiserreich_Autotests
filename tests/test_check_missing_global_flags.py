##########################
# Test script to check for non-assigned global flags
# If flag is not used via "set_global_flag" at least once, it will appear in test results
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re
from .imports.file_functions import open_text_file, clear_false_positives_flags
FALSE_POSITIVES = ('KR_Economy_Logging',)


def test_check_missing_global_flags(test_runner: object):
    filepath = test_runner.full_path_to_mod
    global_flags = {}
# Part 1 - get the dict of all global flags
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        try:
            text_file = open_text_file(filename)
        except Exception as ex:
            print(f'Skipping the file {filename}')
            print(ex)
            continue

        if 'has_global_flag =' in text_file:
            global_flags_in_file = re.findall('has_global_flag = \\b\\w*\\b', text_file)
            if len(global_flags_in_file) > 0:
                for flag in global_flags_in_file:
                    flag = flag[18:]
                    flag = flag.strip()
                    global_flags[flag] = 0

            global_flags_in_file = re.findall('has_global_flag = { flag = \\b\\w*\\b', text_file)
            if len(global_flags_in_file) > 0:
                for flag in global_flags_in_file:
                    flag = flag[27:]
                    flag = flag.strip()
                    global_flags[flag] = 0

# Part 2 - clear false positives and flags with variables:
    clear_false_positives_flags(flags_dict=global_flags, false_positives=FALSE_POSITIVES)

# Part 3 - count the number of flag occurrences
    print(f'{len(global_flags)} global flags used at least once')
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        try:
            text_file = open_text_file(filename)
        except Exception as ex:
            print(f'Skipping the file {filename}')
            print(ex)
            continue

        not_encountered_flags = [i for i in global_flags.keys() if global_flags[i] == 0]

        if 'set_global_flag =' in text_file:
            for flag in not_encountered_flags:
                global_flags[flag] += text_file.count(f'set_global_flag = {flag}')
                global_flags[flag] += text_file.count(f'set_global_flag = {{ flag = {flag}')
                if flag[-4] == '_':
                    global_flags[flag] += text_file.count(f'set_global_flag = {flag[:-4]}_@ROOT')

# Part 4 - throw the error if flag is not used
    results = [i for i in global_flags if global_flags[i] == 0]
    if results != []:
        print("Following global flags are not set via set_global_flag! Recheck them")
        for i in results:
            print(f'- [ ] {i}')
        print(f'{len(results)} missing global flags found.')
        raise AssertionError("Unassigned global flags were encountered! Check console output")
