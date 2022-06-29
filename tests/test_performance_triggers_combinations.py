##########################
# Test script to check is unoptimised combination of conditions is used
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import pytest
import re
import os
from ..test_classes.generic_test_class import FileOpener, ResultsReporter
from itertools import permutations


def test_check_conditions_is_ally_with(test_runner: object):
    filepath = test_runner.full_path_to_mod
    results = []
    paths = {}

# Part 1 - prepare the list of patterns
    possible_parts_of_pattern = ['\\t+tag =.*\\n', '\\t+is_in_faction_with.*\\n', '\\t+is_subject_of.*\\n']
    all_regex_patterns_raw = list(permutations(possible_parts_of_pattern))
    all_regex_patterns = []
    for pattern in all_regex_patterns_raw:
        all_regex_patterns.append(''.join(pattern))
    all_regex_patterns.append('.*\\{.*\\n\\t+is_in_faction_with.*\\n\\t+is_subject_of.*\\n.*\\}')
    all_regex_patterns.append('.*\\{.*\\n\\t+is_subject_of.*\\n\\t+is_in_faction_with.*\\n.*\\}')

# Part 2 - perform search
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if 'is_subject_of' in text_file:
            for pattern in all_regex_patterns:
                pattern_matches = re.findall(pattern, text_file)
                if len(pattern_matches) > 0:
                    for match in pattern_matches:
                        results.append(match)
                        paths[match] = os.path.basename(filename)

# Part 3 - throw the error if those combinations are encountered
    ResultsReporter.report_results(results=results, paths=paths, message="'is_ally_with' condition can be used in the mentioned files instead. Check console output")


def test_check_conditions_is_faction_leader(test_runner: object):
    filepath = test_runner.full_path_to_mod
    results = []

# Part 1 - prepare the list of patterns
    all_regex_patterns = []
    all_regex_patterns.append('\\t+is_faction_leader = yes.*\\n\\t+exists = yes.*\\n')
    all_regex_patterns.append('\\t+exists = yes.*\\n\\t+is_faction_leader = yes.*\\n')
    all_regex_patterns.append('\\t+is_faction_leader = yes.*\\n\\t+is_subject = no.*\\n')
    all_regex_patterns.append('\\t+is_subject = no.*\\n\\t+is_faction_leader = yes.*\\n')
    all_regex_patterns.append('\\t+is_faction_leader = yes.*\\n\\t+is_in_faction = yes.*\\n')
    all_regex_patterns.append('\\t+is_in_faction = yes.*\\n\\t+is_faction_leader = yes.*\\n')


# Part 2 - perform search
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if 'is_faction_leader = yes' in text_file:
            for pattern in all_regex_patterns:
                pattern_matches = re.findall(pattern, text_file)
                if len(pattern_matches) > 0:
                    for match in pattern_matches:
                        results.append((match.replace('\t', '').replace('\n', '  '), os.path.basename(filename)))

# Part 3 - throw the error if those combinations are encountered
    ResultsReporter.report_results(results=results, message="is_faction_leader = yes necessarily means exists = yes and is_subject = no, so checking for the other two is redundant. Check console output")


def test_check_conditions_exists_yes(test_runner: object):
    filepath = test_runner.full_path_to_mod
    results = []

# Part 1 - prepare the list of patterns
    list1 = ['is_in_faction = yes', 'is_in_faction_with', 'has_war_with', 'has_war = yes', 'owns_state', 'is_subject = yes', 'is_subject_of', 'is_in_tech_sharing_group', 'is_ally_of_root = yes']
    all_regex_patterns = []
    for i in list1:
        all_regex_patterns.append(f'\\t+{i}.*\\n\\t+exists = yes.*\\n')
        all_regex_patterns.append(f'\\t+exists = yes.*\\n\\t+{i}.*\\n')

# Part 2 - perform search
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if 'exists = yes' in text_file:
            for pattern in all_regex_patterns:
                pattern_matches = re.findall(pattern, text_file)
                if len(pattern_matches) > 0:
                    for match in pattern_matches:
                        results.append((match.replace('\t', '').replace('\n', '  '), os.path.basename(filename)))

# Part 3 - throw the error if those combinations are encountered
    ResultsReporter.report_results(results=results, message="Usage of triggers that include 'exists = yes', and 'exists = yes' at the same time is encountered. Check console output")


def test_check_conditions_surrender_progress(test_runner: object):
    filepath = test_runner.full_path_to_mod
    results = []

# Part 1 - prepare the list of patterns
    list1 = ['has_capitulated', 'has_war =']
    all_regex_patterns = []
    for i in list1:
        all_regex_patterns.append(f'\\t+{i}.*\\n\\t+surrender_progress.*\\n')
        all_regex_patterns.append(f'\\t+surrender_progress.*\\n\\t+{i}.*\\n')

# Part 2 - perform search
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if 'surrender_progress' in text_file:
            for pattern in all_regex_patterns:
                pattern_matches = re.findall(pattern, text_file)
                if len(pattern_matches) > 0:
                    for match in pattern_matches:
                        results.append((match.replace('\t', '').replace('\n', '  '), os.path.basename(filename)))

# Part 3 - throw the error if those combinations are encountered
    ResultsReporter.report_results(results=results, message="Usage of triggers that include 'has_capitulated', 'has_war', and 'surrender_progress' at the same time is encountered. Check console output")


def test_check_syntax_every_other_country(test_runner: object):
    filepath = test_runner.full_path_to_mod
    results = []

    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if 'every_other_country' in text_file:
            pattern_matches = re.findall("^(\\t*?)every_other_country = (\\{.*?^\\1\\})", text_file, flags=re.DOTALL | re.MULTILINE)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    if "\thas_war_with = root" in match[1]:
                        results.append((match[1], os.path.basename(filename)))

    ResultsReporter.report_results(results=results, message="This part can be replaced with every_enemy_country. Check console output")


list_of_triggers = [
    "every_owned_state",
    "all_owned_state",
    "any_owned_state",
    "random_owned_state",
]


@pytest.mark.parametrize("trigger", list_of_triggers)
def test_check_syntax_xxx_owned_state(test_runner: object, trigger):
    filepath = test_runner.full_path_to_mod
    results = []

    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if trigger in text_file:
            pattern = f'^(\\t*?){trigger}'+' = (\\{\n.*?^\\1\\})'
            pattern_matches = re.findall(pattern, text_file, flags=re.DOTALL | re.MULTILINE)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    if "\tis_owned_by = root" in match[1]:
                        results.append((match[1], os.path.basename(filename)))

    ResultsReporter.report_results(results=results, message="Is owned by root is redundant here. Check console output")


@pytest.mark.skip(reason="Disabled for now")
def test_check_is_ally_with(test_runner: object):
    filepath = test_runner.full_path_to_mod
    results = []

# Part 1 - prepare the list of patterns
    list1 = ['has_capitulated', 'has_war =']
    all_regex_patterns = []
    for i in list1:
        all_regex_patterns.append(f'\\t+{i}.*\\n\\t+surrender_progress.*\\n')
        all_regex_patterns.append(f'\\t+surrender_progress.*\\n\\t+{i}.*\\n')

# Part 2 - perform search
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if 'is_ally_with' in text_file:
            pattern_matches = re.findall('.*\\n.*is_ally_with.*\\n.*', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    if 'country_exists =' not in match and 'exists = yes' not in match:
                        results.append((match.replace('\t', '').replace('\n', '  '), os.path.basename(filename)))

# Part 3 - throw the error if those combinations are encountered
    ResultsReporter.report_results(results=results, message="is_ally_with w/o 'country_exists =' or 'exists = yes' is encountered. Check console output")


def test_check_set_state_category(test_runner: object):
    filepath = test_runner.full_path_to_mod
    results = []

# Part 1 - perform search
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        if '00_useful_scripted_effects' in filename:
            continue
        text_file = FileOpener.open_text_file(filename)

        if 'set_state_category' in text_file:
            pattern_matches = re.findall('.*set_state_category.*', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    results.append((match.replace('\t', '').replace('\n', '  '), os.path.basename(filename)))

# Part 2 - throw the error if those combinations are encountered
    ResultsReporter.report_results(results=results, message="set_state_category is encountered - use 'increase_state_category_by_one_level = yes' instead. Check console output")


def test_non_targeted_decisions(test_runner: object):
    filepath = test_runner.full_path_to_mod
    results = []

# Part 1 - perform search
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if 'unlock_decision' in text_file:
            pattern_matches = re.findall('.*unlock_decision.*', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    results.append((match.replace('\t', ''), os.path.basename(filename)))

# Part 2 - throw the error if those combinations are encountered
    ResultsReporter.report_results(results=results, message="Recheck the piece of code and convert to targeted decision if possible. Check console output")
