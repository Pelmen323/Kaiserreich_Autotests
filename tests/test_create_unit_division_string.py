##########################
# Test script to check if string passed in create_unit is valid
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
import re

from ..test_classes.generic_test_class import FileOpener, ResultsReporter


def test_check_create_unit_string(test_runner: object):
    filepath = test_runner.full_path_to_mod
    results = []
# Part 1 - get the list of entities
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if 'create_unit = {' in text_file:
            pattern_matches_basic = re.findall('^(\\t+)create_unit = \\{(.*?)\\n\\1\\}', text_file, flags=re.MULTILINE | re.DOTALL)
            pattern_matches = re.findall('^(\\t+)create_unit = \\{(.*?\t(division = [^\\n]+).*?)\\n\\1\\}', text_file, flags=re.MULTILINE | re.DOTALL)
            # Check if every effect contains division string
            if len(pattern_matches_basic) != len(pattern_matches):
                results.append(f'{os.path.basename(filename)} - one of the effects is missing division string')
                continue
            # Check if effect contains valid division string
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    pattern = r'division = \"(division_name = \{ is_name_ordered = yes name_order = \d+ \})*([ ]{0,1}(name = \\\"[^\"\t\n]+?\\\"|name = \[\w+\]))*([ ]{0,1}(division_template = \\\"[^\"\t\n]+?\\\"|division_template = \[\w+\]))+( start_experience_factor = (\d+(?:\.\d+)?))*?( start_equipment_factor = (\d+(?:\.\d+)?))*?( start_manpower_factor = (\d+(?:\.\d+)?))*?( force_equipment_variants = \{.*\})*?\"'
                    expected_pattern_encountered = re.findall(pattern, match[2], flags=re.MULTILINE)
                    if expected_pattern_encountered == []:
                        results.append(f'{match[2]} - {os.path.basename(filename)} - invalid division string encountered')

    ResultsReporter.report_results(results=results, message="Issues with create_unit strings were encountered. Check console output")
