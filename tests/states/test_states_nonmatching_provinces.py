##########################
# Test script to check for constuctions in provinces that don't belong to target state
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
import re

from test_classes.generic_test_class import FileOpener, ResultsReporter
from test_classes.states_class import States


def test_states_nonmatching_provinces(test_runner: object):
    filepath = test_runner.full_path_to_mod
    states_provinces_dict = States.get_states_provinces_dict(test_runner=test_runner)
    results = []

    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if 'add_building_construction' in text_file:

            building_construction_matches = re.findall('^(\\t+)(\\d+) = \\{[^\\{]*?(add_building_construction = .*?^\\1\\})', string=text_file, flags=re.MULTILINE | re.DOTALL)
            if len(building_construction_matches) > 0:
                for i in building_construction_matches:
                    state = i[1]
                    effect_string = i[2]

                    effect_patterns = re.findall('add_building_construction = \\{.*?\\}', string=effect_string, flags=re.MULTILINE | re.DOTALL)
                    if len(effect_patterns) > 0:
                        if not isinstance(effect_patterns, list):
                            effect_patterns = [effect_patterns]
                        if len(effect_patterns) > 0:
                            for effect in effect_patterns:

                                if 'type = bunker' in effect and 'province = {' not in effect:
                                    try:
                                        province = re.findall('province = (\\d+)', effect)[0]
                                    except IndexError:
                                        results.append(f'{os.path.basename(filename)}: bunker construction - state {state} - target province is not defined')
                                        continue
                                    if province not in states_provinces_dict[state]:
                                        results.append(f'{os.path.basename(filename)}: bunker construction - target province {province} is not in the state {state} provinces list {states_provinces_dict[state]}')

                                elif 'type = coastal_bunker' in effect and 'province = {' not in effect:
                                    try:
                                        province = re.findall('province = (\\d+)', effect)[0]
                                    except IndexError:
                                        results.append(f'{os.path.basename(filename)}: coastal_bunker construction - state {state} - target province is not defined')
                                        continue
                                    if province not in states_provinces_dict[state]:
                                        results.append(f'{os.path.basename(filename)}: coastal_bunker construction - target province {province} is not in the state {state} provinces list {states_provinces_dict[state]}')

                                elif 'type = naval_base' in effect and 'province = {' not in effect:
                                    try:
                                        province = re.findall('province = (\\d+)', effect)[0]
                                    except IndexError:
                                        results.append(f'{os.path.basename(filename)}: naval_base construction - state {state} - target province is not defined')
                                        continue
                                    if province not in states_provinces_dict[state]:
                                        results.append(f'{os.path.basename(filename)}: naval_base construction - target province {province} is not in the state {state} provinces list {states_provinces_dict[state]}')

                                elif 'type = supply_node' in effect and 'province = {' not in effect:
                                    try:
                                        province = re.findall('province = (\\d+)', effect)[0]
                                    except IndexError:
                                        results.append(f'{os.path.basename(filename)}: supply_node construction - state {state} - target province is not defined')
                                        continue
                                    if province not in states_provinces_dict[state]:
                                        results.append(f'{os.path.basename(filename)}: supply_node construction - target province {province} is not in the state {state} provinces list {states_provinces_dict[state]}')

    ResultsReporter.report_results(results=results, message="Building constructions in mismatching provinces encountered. Check console output")
