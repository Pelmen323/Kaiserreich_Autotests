##########################
# Test script to check for possible replacement of separate ideology triggers with scripted triggers
# By Pelmen, https://github.com/Pelmen323
##########################
import re

from ..data.ideologies import ideology_bundles
from ..test_classes.decisions_class import Decisions, DecisionsFactory
from ..test_classes.events_class import Events
from ..test_classes.national_focus_class import National_focus, NationalFocusFactory
from ..test_classes.generic_test_class import ResultsReporter


def test_check_events_ideology_optimisations(test_runner: object):
    events, paths = Events.get_all_events(test_runner=test_runner, lowercase=True, return_paths=True)
    results = []
    false_positives = ('austral.35', 'russoc.120')

    for event in events:
        event_name = re.findall('\\bid = (\\b.*\\b)', event)[0]
        if event_name in false_positives:
            continue
        trigger_part = re.findall('^\\ttrigger = \\{.*?^\\t\\}', event, flags=re.MULTILINE | re.DOTALL)
        if trigger_part != [] and "has_government =" in trigger_part[0]:
            for bundle in ideology_bundles:
                is_valid_candidate = len([i for i in ideology_bundles[bundle] if i in trigger_part[0]]) == len(ideology_bundles[bundle])
                if is_valid_candidate:
                    results.append((event_name, paths[event], f'{bundle} can be used here instead of {ideology_bundles[bundle]}'))

    ResultsReporter.report_results(results=results, message="Events - possible candidates for has_xxx_government scripted triggers usage found. Check console output")


def test_check_focuses_ideology_optimisations(test_runner: object):
    focuses = National_focus.get_all_national_focuses(test_runner=test_runner, lowercase=False)
    results = []
    false_positives = ('ARG_Neutralize_The_Threat', 'SAF_native_trust_and_land_act', 'SWE_gyllenkrok_regime', 'NATFRA_Privatisation_Madness', 'NATFRA_Create_New_Elite')

    for i in focuses:
        focus = NationalFocusFactory(focus=i)
        if focus.id in false_positives:
            continue

        if focus.available and "has_government =" in focus.available:
            for bundle in ideology_bundles:
                is_valid_candidate = len([i for i in ideology_bundles[bundle] if i in focus.available]) == len(ideology_bundles[bundle])
                if is_valid_candidate:
                    results.append((focus.id, f'{bundle} can be used here instead of {ideology_bundles[bundle]}'))

        if focus.bypass and "has_government =" in focus.bypass:
            for bundle in ideology_bundles:
                is_valid_candidate = len([i for i in ideology_bundles[bundle] if i in focus.bypass]) == len(ideology_bundles[bundle])
                if is_valid_candidate:
                    results.append((focus.id, f'bypass - {bundle} can be used here instead of {ideology_bundles[bundle]}'))

    ResultsReporter.report_results(results=results, message="Focuses - possible candidates for has_xxx_government scripted triggers usage found. Check console output")


def test_check_decisions_ideology_optimisations(test_runner: object):
    decisions = Decisions.get_all_decisions(test_runner=test_runner, lowercase=True, return_paths=False)
    results = []
    false_positives = ('bul_join_reichspakt', 'can_support_government', 'lat_visit_to_rus', 'wif_combat_illegal_french_activity', 'ukr_galician_negotiations')
    for i in decisions:
        decision = DecisionsFactory(dec=i)
        available_part = None
        visible_part = None
        is_valid_candidate_available = False
        is_valid_candidate_visible = False

        if decision.token in false_positives:
            continue

        if decision.available:
            available_part = decision.available
        if decision.visible:
            visible_part = decision.visible
        if decision.target_root_trigger:
            target_root_trigger_part = decision.target_root_trigger
        if decision.target_trigger:
            target_trigger_part = decision.target_trigger

        for bundle in ideology_bundles:
            if decision.available:
                is_valid_candidate_available = len([i for i in ideology_bundles[bundle] if i in available_part]) == len(ideology_bundles[bundle])
                if is_valid_candidate_available:
                    results.append((decision.token, f'available - {bundle} can be used here instead of {ideology_bundles[bundle]}'))
            if decision.visible:
                is_valid_candidate_visible = len([i for i in ideology_bundles[bundle] if i in visible_part]) == len(ideology_bundles[bundle])
                if is_valid_candidate_visible:
                    results.append((decision.token, f'visible - {bundle} can be used here instead of {ideology_bundles[bundle]}'))
            if decision.target_root_trigger:
                is_valid_candidate_target_root_trigger = len([i for i in ideology_bundles[bundle] if i in target_root_trigger_part]) == len(ideology_bundles[bundle])
                if is_valid_candidate_target_root_trigger:
                    results.append((decision.token, f'target_root_trigger - {bundle} can be used here instead of {ideology_bundles[bundle]}'))
            if decision.target_trigger:
                is_valid_candidate_target_trigger = len([i for i in ideology_bundles[bundle] if i in target_trigger_part]) == len(ideology_bundles[bundle])
                if is_valid_candidate_target_trigger:
                    results.append((decision.token, f'target_trigger - {bundle} can be used here instead of {ideology_bundles[bundle]}'))

    ResultsReporter.report_results(results=results, message="Decisions - possible candidates for has_xxx_government scripted triggers usage found. Check console output")
