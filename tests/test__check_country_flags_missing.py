##########################
# Test script to check for unused global flags
# If flag is not used via "has_global_flag" at least once, it will appear in test results
# Flags with values or variables (ROOT/THIS/FROM) should be added to false positives
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re
import os
from ..test_classes.generic_test_class import TestClass
import logging
FALSE_POSITIVES = ('chi_soong_control',        # Currently unused flags
                   'chi_mingshu_control',
                   'dei_ins_coup_avoided',
                   'chi_mingshu_lkmt',
                   'dei_koninkrijksstatuut_signed',
                   'annexation_window_open',)


def test_check_missing_country_flags(test_runner: object):
    test = TestClass()
    filepath = test_runner.full_path_to_mod
    country_flags = {}
    paths = {}
# Part 1 - get the dict of all global flags
    for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
        text_file = test.open_text_file(filename).lower()

        if "has_country_flag =" in text_file:
            pattern_matches = re.findall("has_country_flag = [a-zA-Z0-9_']*", text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[19:].strip()
                    country_flags[match] = 0
                    paths[match] = os.path.basename(filename)

            pattern_matches = re.findall("has_country_flag = { flag = [a-zA-Z0-9_']*", text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[27:].strip()
                    country_flags[match] = 0
                    paths[match] = os.path.basename(filename)

# Part 2 - clear false positives and flags with variables:
    country_flags = test.clear_false_positives_dict(input_dict=country_flags, false_positives=FALSE_POSITIVES)
    # TEMP REMOVAL UNTIL MINISTERS ARE NOT REMOVED #
    dead_flags = []
    for flag in country_flags:
        if "_dead" in flag:
            dead_flags.append(flag)
    for flag in dead_flags:
        country_flags.pop(flag)

# Part 3 - count the number of flag occurrences
    for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
        text_file = test.open_text_file(filename).lower()

        not_encountered_flags = [i for i in country_flags.keys() if country_flags[i] == 0]

        if "set_country_flag =" in text_file:
            for flag in not_encountered_flags:
                if flag in text_file:
                    country_flags[flag] += text_file.count(f"set_country_flag = {flag}")
                    country_flags[flag] += text_file.count(f"set_country_flag = {{ flag = {flag}")
                if len(flag) > 3:
                    if flag[-4] == "_" and flag[-4:] != flag[-4:].lower():
                        country_flags[flag] += text_file.count(f"set_country_flag = {flag[:-4]}_@root")
                        country_flags[flag] += text_file.count(f"set_country_flag = {flag[:-4]}_@from")
                        country_flags[flag] += text_file.count(f"set_country_flag = {flag[:-4]}_@var:revolter")
                        country_flags[flag] += text_file.count(f"set_country_flag = {{ flag = {flag[:-4]}_@root")
                        country_flags[flag] += text_file.count(f"set_country_flag = {{ flag = {flag[:-4]}_@from")


# Part 4 - throw the error if flag is not used
    results = [i for i in country_flags if country_flags[i] == 0]
    if results != []:
        logging.warning("Following country flags are not set via set_country_flag! Recheck them")
        # with open(f"C:\\Users\\{test_runner.username}\\Desktop\\missing_country_flags.txt", "a") as create_var:
        for i in results:
            # create_var.write(f"\n- [ ] {i}")
            logging.error(f"- [ ] {i}, - '{paths[i]}'")
        logging.warning(f"{len(results)} unset country flags found. Probably some of these are false positives, but they should be rechecked!")
        raise AssertionError("Unset country flags were encountered! Check console output")
