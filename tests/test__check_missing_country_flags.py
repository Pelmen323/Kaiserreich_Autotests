##########################
# Test script to check for unused global flags
# If flag is not used via "has_global_flag" at least once, it will appear in test results
# Flags with values or variables (ROOT/THIS/FROM) should be added to false positives
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re
from .imports.file_functions import open_text_file
import logging


def test_check_missing_country_flags(test_runner: object):
    filepath = test_runner.full_path_to_mod
    country_flags = {}
# Part 1 - get the dict of all global flags
    for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
        try:
            text_file = open_text_file(filename)
        except Exception as ex:
            logging.debug(f"Skipping the file {filename}")
            logging.warning(ex)
            continue

        if "has_country_flag =" in text_file:
            country_flags_in_file = re.findall("has_country_flag = [a-zA-Z0-9_']*", text_file)
            if len(country_flags_in_file) > 0:
                for flag in country_flags_in_file:
                    flag = flag[19:]
                    flag = flag.strip()
                    country_flags[flag] = 0

            country_flags_in_file = re.findall("has_country_flag = { flag = [a-zA-Z0-9_']*", text_file)
            if len(country_flags_in_file) > 0:
                for flag in country_flags_in_file:
                    flag = flag[27:]
                    flag = flag.strip()
                    country_flags[flag] = 0

# Part 2 - clear false positives and flags with variables:
    # clear_false_positives_flags(flags_dict=country_flags, false_positives=false_positives)
    # !-- In progress - remove after debug is finished
    # logging.debug(f"{len(country_flags)} unique used country flags were found")
    # debug = [i for i in country_flags]
    # with open(f"C:\\Users\\{test_runner.username}\\Desktop\\missing_country_flags_DEBUG.txt", "a") as create_var:
    #     for i in debug:
    #         create_var.write(f"\n- [ ] {i}")

    # TEMP REMOVAL UNTIL MINISTERS ARE NOT REMOVED #
    dead_flags = []
    for flag in country_flags:
        if "_dead" in flag:
            dead_flags.append(flag)
    for flag in dead_flags:
        country_flags.pop(flag)

# Part 3 - count the number of flag occurrences
    for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
        try:
            text_file = open_text_file(filename)
        except Exception as ex:
            logging.debug(f"Skipping the file {filename}")
            logging.warning(ex)
            continue

        not_encountered_flags = [i for i in country_flags.keys() if country_flags[i] == 0]

        if "set_country_flag =" in text_file:
            for flag in not_encountered_flags:
                if flag in text_file:
                    country_flags[flag] += text_file.count(f"set_country_flag = {flag}")
                    country_flags[flag] += text_file.count(f"set_country_flag = {{ flag = {flag}")
                if len(flag) > 3:
                    if flag[-4] == "_" and flag[-4:] != flag[-4:].lower():
                        country_flags[flag] += text_file.count(f"set_country_flag = {flag[:-4]}_@ROOT")
                        country_flags[flag] += text_file.count(f"set_country_flag = {flag[:-4]}_@FROM")
                        country_flags[flag] += text_file.count(f"set_country_flag = {flag[:-4]}_@var:revolter")
                        country_flags[flag] += text_file.count(f"set_country_flag = {{ flag = {flag[:-4]}_@ROOT")
                        country_flags[flag] += text_file.count(f"set_country_flag = {{ flag = {flag[:-4]}_@FROM")


# Part 4 - throw the error if flag is not used
    results = [i for i in country_flags if country_flags[i] == 0]
    if results != []:
        logging.warning("Following country flags are not set via set_country_flag! Recheck them")
        # with open(f"C:\\Users\\{test_runner.username}\\Desktop\\missing_country_flags.txt", "a") as create_var:
        for i in results:
            # create_var.write(f"\n- [ ] {i}")
            logging.error(f"- [ ] {i}")
        logging.warning(f"{len(results)} unset country flags found. Probably some of these are false positives, but they should be rechecked!")
        raise AssertionError("Unset country flags were encountered! Check console output")
