##########################
# Test script to check if invalid traits are used for corps commanders
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
import re

from ..test_classes.generic_test_class import FileOpener, ResultsReporter
from ..test_classes.unit_leader_traits_class import Traits


def perform_trait_checks(test_runner: object, target_str: str, traits_to_verify: list, valid_traits: list, results: list):
    filepath = test_runner.full_path_to_mod

    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if target_str in text_file:
            pattern = "^(\\t*?)" + target_str + "(\\{.*?^\\1\\})"
            pattern_matches = re.findall(pattern, text_file, flags=re.DOTALL | re.MULTILINE)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    for trait in traits_to_verify:
                        if trait not in valid_traits:
                            if f'\t{trait}\n' in match[1] or f' {trait} ' in match[1]:
                                results.append((match[1].replace('\t', '').replace('\n', '  '), trait, os.path.basename(filename)))

    return results


def test_check_corps_commanders_with_unsupported_traits(test_runner: object):
    valid_traits = Traits.get_traits_names_from_specified_category(test_runner=test_runner, category="general")
    fm_traits = Traits.get_traits_names_from_specified_category(test_runner=test_runner, category="field_marshal")
    navy_traits = Traits.get_traits_names_from_specified_category(test_runner=test_runner, category="navy")
    operative_traits = Traits.get_traits_names_from_specified_category(test_runner=test_runner, category="operative")
    traits_to_verify = fm_traits + operative_traits + navy_traits
    results = []

    results = perform_trait_checks(test_runner=test_runner, target_str="corps_commander = ", traits_to_verify=traits_to_verify, valid_traits=valid_traits, results=results)
    results = perform_trait_checks(test_runner=test_runner, target_str="add_corps_commander_role = ", traits_to_verify=traits_to_verify, valid_traits=valid_traits, results=results)

    ResultsReporter.report_results(results=results, message="Corps commanders with unsupported traits encountered. Check console output")


def test_check_field_marshals_with_unsupported_traits(test_runner: object):
    valid_traits = Traits.get_traits_names_from_specified_category(test_runner=test_runner, category="all_land")
    navy_traits = Traits.get_traits_names_from_specified_category(test_runner=test_runner, category="navy")
    operative_traits = Traits.get_traits_names_from_specified_category(test_runner=test_runner, category="operative")
    traits_to_verify = operative_traits + navy_traits
    results = []

    results = perform_trait_checks(test_runner=test_runner, target_str="field_marshal = ", traits_to_verify=traits_to_verify, valid_traits=valid_traits, results=results)
    results = perform_trait_checks(test_runner=test_runner, target_str="add_field_marshal_role = ", traits_to_verify=traits_to_verify, valid_traits=valid_traits, results=results)

    ResultsReporter.report_results(results=results, message="Field marshals with unsupported traits encountered. Check console output")


def test_check_navy_leaders_with_unsupported_traits(test_runner: object):
    valid_traits = Traits.get_traits_names_from_specified_category(test_runner=test_runner, category="navy")
    all_land_traits = Traits.get_traits_names_from_specified_category(test_runner=test_runner, category="all_land")
    operative_traits = Traits.get_traits_names_from_specified_category(test_runner=test_runner, category="operative")
    traits_to_verify = all_land_traits + operative_traits
    results = []

    results = perform_trait_checks(test_runner=test_runner, target_str="navy_leader = ", traits_to_verify=traits_to_verify, valid_traits=valid_traits, results=results)

    ResultsReporter.report_results(results=results, message="Navy leaders with unsupported traits encountered. Check console output")
