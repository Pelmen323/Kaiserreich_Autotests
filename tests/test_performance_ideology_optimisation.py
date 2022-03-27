##########################
# Test script to check for possible replacement of separate ideology triggers with scripted triggers
# By Pelmen, https://github.com/Pelmen323
##########################
import re
from ..test_classes.generic_test_class import ResultsReporter
from ..test_classes.national_focus_class import National_focus
from ..test_classes.events_class import Events
from ..test_classes.decisions_class import Decisions
from ..data.ideologies import ideology_bundles


def test_check_focuses_ideology_optimisations(test_runner: object):
    focuses, paths = National_focus.get_all_national_focuses_with_paths(test_runner=test_runner, lowercase=True, return_paths=True)
    results = []

    for focus in focuses:
        focus_name = re.findall('\\bid = (\\w*)', focus)[0]
        for bundle in ideology_bundles:
            is_valid_candidate = len([i for i in ideology_bundles[bundle] if i in focus]) == len(ideology_bundles[bundle])
            if is_valid_candidate:
                results.append((focus_name, paths[focus], f'{bundle} can be used here'))

    ResultsReporter.report_results(results=results, message="Focuses - possible candidates for has_xxx_government scripted triggers usage found. Check console output")


def test_check_events_ideology_optimisations(test_runner: object):
    events, paths = Events.get_all_events(test_runner=test_runner, lowercase=True, return_paths=True)
    results = []

    for event in events:
        event_name = re.findall('\\bid = (\\b.*\\b)', event)[0]
        trigger_part = re.findall('((?<=\n)\\ttrigger = \\{.*\n(.|\n*?)*\n\\t\\})', event)
        if trigger_part != []:
            for bundle in ideology_bundles:
                is_valid_candidate = len([i for i in ideology_bundles[bundle] if i in trigger_part[0][0]]) == len(ideology_bundles[bundle])
                if is_valid_candidate:
                    results.append((event_name, paths[event], f'{bundle} can be used here'))

    ResultsReporter.report_results(results=results, message="Events - possible candidates for has_xxx_government scripted triggers usage found. Check console output")


def test_check_decisions_ideology_optimisations(test_runner: object):
    decisions, paths = Decisions.get_all_decisions_with_paths(test_runner=test_runner, lowercase=True, return_paths=True)
    results = []
    print(len(decisions))
    for decision in decisions:
        try:
            decision_name = re.findall('^\\t(\\b.*\\b) = \\{', decision)[0]
        except IndexError:
            results.append(decision, "Missing decision name?")
            continue
        for bundle in ideology_bundles:
            is_valid_candidate = len([i for i in ideology_bundles[bundle] if i in decision]) == len(ideology_bundles[bundle])
            if is_valid_candidate:
                results.append((decision_name, paths[decision], f'{bundle} can be used here'))

    ResultsReporter.report_results(results=results, message="Decisions - possible candidates for has_xxx_government scripted triggers usage found. Check console output")
