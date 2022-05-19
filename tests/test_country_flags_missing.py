##########################
# Test script to check for missing country flags
# If flag is not set via "set_country_flag" at least once, it will appear in test results
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re
import os
from ..test_classes.generic_test_class import FileOpener, DataCleaner, ResultsReporter
FALSE_POSITIVES = ('chi_soong_control',        # Currently unused flags
                   'chi_mingshu_control',
                   'dei_ins_coup_avoided',
                   'chi_mingshu_lkmt',
                   'dei_koninkrijksstatuut_signed',
                   'annexation_window_open',
                   'liang_refused',
                   'enrique_lister_forjan_dead',
                   'buenaventura_durruti_dumange_dead',
                   'francisco_ascaso_budria_dead',
                   'vicente_rojo_lluch_dead',
                   'juan_lopez_sanchez_dead',
                   'juan_peiro_belis_dead',
                   'lit_factory_opened',
                   )


def test_check_missing_country_flags(test_runner: object):
    filepath = test_runner.full_path_to_mod
    country_flags = {}
    paths = {}
# Part 1 - get the dict of entities
    for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
        text_file = FileOpener.open_text_file(filename)

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
    country_flags = DataCleaner.clear_false_positives(input_iter=country_flags, false_positives=FALSE_POSITIVES)

# Part 3 - count the number of entity occurrences
    for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
        text_file = FileOpener.open_text_file(filename)

        not_encountered_flags = [i for i in country_flags.keys() if country_flags[i] == 0]

        if "set_country_flag =" in text_file:
            for flag in not_encountered_flags:
                if flag in text_file:
                    country_flags[flag] += text_file.count(f"set_country_flag = {flag}")
                    country_flags[flag] += text_file.count(f"set_country_flag = {{ flag = {flag}")
                if len(flag) > 3:
                    if flag[-4] == "_":
                        country_flags[flag] += text_file.count(f"set_country_flag = {flag[:-4]}_@root")
                        country_flags[flag] += text_file.count(f"set_country_flag = {flag[:-4]}_@from")
                        country_flags[flag] += text_file.count(f"set_country_flag = {flag[:-4]}_@var:revolter")
                        country_flags[flag] += text_file.count(f"set_country_flag = {{ flag = {flag[:-4]}_@root")
                        country_flags[flag] += text_file.count(f"set_country_flag = {{ flag = {flag[:-4]}_@from")


# Part 4 - throw the error if entity is not used
    results = [i for i in country_flags if country_flags[i] == 0]
    ResultsReporter.report_results(results=results, paths=paths, message="Missing country flags were encountered - they are not set via 'set_country_flag'. Check console output")
