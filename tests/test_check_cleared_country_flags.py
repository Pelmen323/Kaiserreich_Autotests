##########################
# Test script to check for unused global flags
# If flag is not used via "has_global_flag" at least once, it will appear in test results
# Flags with values or variables (ROOT/THIS/FROM) should be added to false positives
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re
from .imports.file_functions import open_text_file, clear_false_positives_flags
FALSE_POSITIVES = ('annexation_window_open')    # Commented functionality


def test_check_cleared_country_flags(test_runner: object):
    filepath = test_runner.full_path_to_mod
    country_flags = {}
# Part 1 - get the dict of all global flags
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        try:
            text_file = open_text_file(filename)
        except Exception as ex:
            print(f'Skipping the file {filename}')
            print(ex)
            continue

        if 'clr_country_flag =' in text_file:
            country_flags_in_file = re.findall('clr_country_flag = \\b\\w*\\b', text_file)
            if len(country_flags_in_file) > 0:
                for flag in country_flags_in_file:
                    flag = flag[19:]
                    flag = flag.strip()
                    country_flags[flag] = 0


# Part 2 - clear false positives and flags with variables:
    clear_false_positives_flags(flags_dict=country_flags, false_positives=FALSE_POSITIVES)

# Part 3 - count the number of flag occurrences
    print(f'{len(country_flags)} state flags cleared at least once')
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        try:
            text_file = open_text_file(filename)
        except Exception as ex:
            print(f'Skipping the file {filename}')
            print(ex)
            continue

        if 'set_country_flag =' in text_file:
            for flag in country_flags.keys():
                country_flags[flag] += text_file.count(f'set_country_flag = {flag}')
                country_flags[flag] += text_file.count(f'set_country_flag = {{ flag = {flag}')
                if flag[-4] == '_':
                    country_flags[flag] += text_file.count(f'set_country_flag = {flag[:-4]}_@ROOT')

# Part 4 - throw the error if flag is not used
    results = [i for i in country_flags if country_flags[i] == 0]
    if results != []:
        print("Following cleared country flags are not set via set_country_flag! Recheck them")
        for i in results:
            print(f'- [ ] {i}')
        print(f'{len(results)} unset country flags found.')
        raise AssertionError("Unset country flags were encountered! Check console output")