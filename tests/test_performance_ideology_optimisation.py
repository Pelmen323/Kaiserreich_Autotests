##########################
# Test script to check for possible replacement of separate ideology triggers with scripted triggers
# By Pelmen, https://github.com/Pelmen323
##########################
import re

from ..data.ideologies import ideology_bundles
from ..test_classes.decisions_class import Decisions
from ..test_classes.events_class import Events
from ..test_classes.generic_test_class import ResultsReporter


def test_check_events_ideology_optimisations(test_runner: object):
    events, paths = Events.get_all_events(test_runner=test_runner, lowercase=True, return_paths=True)
    results = []
    false_positives = ('austral.35',)

    for event in events:
        if "is_triggered_only = yes" in event:
            continue        # Low prio
        event_name = re.findall('\\bid = (\\b.*\\b)', event)[0]
        if event_name in false_positives:
            continue
        trigger_part = re.findall('((?<=\n)\\ttrigger = \\{.*\n(.|\n*?)*\n\\t\\})', event)
        if trigger_part != []:
            # if "tag = " not in trigger_part[0][0]:
            #     results.append((event_name, paths[event], 'For some reason this event a tag defined in trigger part'))
            for bundle in ideology_bundles:
                is_valid_candidate = len([i for i in ideology_bundles[bundle] if i in trigger_part[0][0]]) == len(ideology_bundles[bundle])
                if is_valid_candidate:
                    results.append((event_name, paths[event], f'{bundle} can be used here'))

        else:
            results.append((event_name, paths[event], 'For some reason this event doesnt have a trigger part'))

    ResultsReporter.report_results(results=results, message="Events - possible candidates for has_xxx_government scripted triggers usage found. Check console output")


def test_check_decisions_ideology_optimisations(test_runner: object):
    decisions, paths = Decisions.get_all_decisions(test_runner=test_runner, lowercase=True, return_paths=True)
    results = []
    false_positives = ('bul_join_reichspakt', 'can_support_government', 'lat_visit_to_rus', 'wif_combat_illegal_french_activity',)
    for decision in decisions:
        available_part = None
        visible_part = None
        is_valid_candidate_available = False
        is_valid_candidate_visible = False
        try:
            decision_name = re.findall('^\\t(\\b.*\\b) = \\{', decision)[0]
        except IndexError:
            results.append(decision, "Missing decision name?")
            continue

        if decision_name in false_positives:
            continue

        try:
            if "available = {" in decision:
                available_part = re.findall('((?<=\n)\\t\\tavailable = \\{.*\n(.|\n*?)*\n\\t\\t\\})', decision)[0][0]
            if "visible = {" in decision:
                visible_part = re.findall('((?<=\n)\\t\\tvisible = \\{.*\n(.|\n*?)*\n\\t\\t\\})', decision)[0][0]
            for bundle in ideology_bundles:
                if available_part is not None:
                    is_valid_candidate_available = len([i for i in ideology_bundles[bundle] if i in available_part]) == len(ideology_bundles[bundle])
                if visible_part is not None:
                    is_valid_candidate_visible = len([i for i in ideology_bundles[bundle] if i in visible_part]) == len(ideology_bundles[bundle])
                if any([is_valid_candidate_available, is_valid_candidate_visible]):
                    results.append((decision_name, paths[decision], f'{bundle} can be used here'))
        except IndexError:
            results.append((decision_name, paths[decision], 'Visible/available parts are commented or empty'))
            continue

    ResultsReporter.report_results(results=results, message="Decisions - possible candidates for has_xxx_government scripted triggers usage found. Check console output")
