##########################
# Test script to check if invalid traits are used for corps commanders
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re
import os
from ..test_classes.generic_test_class import FileOpener, ResultsReporter
from ..test_classes.unit_leader_traits_class import Traits


def test_check_corps_commanders_with_unsupported_traits(test_runner: object):
    filepath = test_runner.full_path_to_mod
    valid_traits = Traits.get_traits_names_from_specified_category(test_runner=test_runner, category="general")
    fm_traits = Traits.get_traits_names_from_specified_category(test_runner=test_runner, category="field_marshal")
    navy_traits = Traits.get_traits_names_from_specified_category(test_runner=test_runner, category="navy")
    operative_traits = Traits.get_traits_names_from_specified_category(test_runner=test_runner, category="operative")
    traits_to_verify = fm_traits + operative_traits + navy_traits
    results = []

    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if 'corps_commander = {' in text_file:
            pattern_matches = re.findall("^(\\t*?)corps_commander = (\\{.*?^\\1\\})", text_file, flags=re.DOTALL | re.MULTILINE)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    for trait in traits_to_verify:
                        if trait not in valid_traits:
                            if f'\t{trait}\n' in match[1] or f' {trait} ' in match[1]:
                                results.append((match[1].replace('\t', '').replace('\n', '  '), trait, os.path.basename(filename)))

        if 'add_corps_commander_role = {' in text_file:
            pattern_matches = re.findall("^(\\t*?)add_corps_commander_role = (\\{.*?^\\1\\})", text_file, flags=re.DOTALL | re.MULTILINE)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    for trait in traits_to_verify:
                        if trait not in valid_traits:
                            if f'\t{trait}\n' in match[1] or f' {trait} ' in match[1]:
                                results.append((match[1].replace('\t', '').replace('\n', '  '), trait, os.path.basename(filename)))

    ResultsReporter.report_results(results=results, message="Corps commanders with unsupported traits encountered. Check console output")


def test_check_field_marshals_with_unsupported_traits(test_runner: object):
    filepath = test_runner.full_path_to_mod
    valid_traits = Traits.get_traits_names_from_specified_category(test_runner=test_runner, category="all_land")
    navy_traits = Traits.get_traits_names_from_specified_category(test_runner=test_runner, category="navy")
    operative_traits = Traits.get_traits_names_from_specified_category(test_runner=test_runner, category="operative")
    traits_to_verify = operative_traits + navy_traits
    results = []

    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if 'field_marshal = {' in text_file:
            pattern_matches = re.findall("^(\\t*?)field_marshal = (\\{.*?^\\1\\})", text_file, flags=re.DOTALL | re.MULTILINE)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    for trait in traits_to_verify:
                        if trait not in valid_traits:
                            if f'\t{trait}\n' in match[1] or f' {trait} ' in match[1]:
                                results.append((match[1].replace('\t', '').replace('\n', '  '), trait, os.path.basename(filename)))

        if 'add_field_marshal_role = {' in text_file:
            pattern_matches = re.findall("^(\\t*?)add_field_marshal_role = (\\{.*?^\\1\\})", text_file, flags=re.DOTALL | re.MULTILINE)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    for trait in traits_to_verify:
                        if trait not in valid_traits:
                            if f'\t{trait}\n' in match[1] or f' {trait} ' in match[1]:
                                results.append((match[1].replace('\t', '').replace('\n', '  '), trait, os.path.basename(filename)))

    ResultsReporter.report_results(results=results, message="Field marshals with unsupported traits encountered. Check console output")


def test_check_navy_leaders_with_unsupported_traits(test_runner: object):
    filepath = test_runner.full_path_to_mod
    navy_traits = Traits.get_traits_names_from_specified_category(test_runner=test_runner, category="navy")
    all_land_traits = Traits.get_traits_names_from_specified_category(test_runner=test_runner, category="all_land")
    operative_traits = Traits.get_traits_names_from_specified_category(test_runner=test_runner, category="operative")
    traits_to_verify = all_land_traits + operative_traits
    results = []

    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if 'navy_leader = {' in text_file:
            pattern_matches = re.findall("^(\\t*?)navy_leader = (\\{.*?^\\1\\})", text_file, flags=re.DOTALL | re.MULTILINE)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    for trait in traits_to_verify:
                        if trait not in navy_traits:
                            if f'\t{trait}\n' in match[1] or f' {trait} ' in match[1]:
                                results.append((match[1].replace('\t', '').replace('\n', '  '), trait, os.path.basename(filename)))

    ResultsReporter.report_results(results=results, message="Navy leaders with unsupported traits encountered. Check console output")
