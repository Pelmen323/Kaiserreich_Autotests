##########################
# Test script to check for possible replacement of separate ideology triggers with scripted triggers
# By Pelmen, https://github.com/Pelmen323
##########################

from data.ideologies import ideology_bundles
from test_classes.decisions_class import Decisions, DecisionsFactory
from test_classes.events_class import Events, EventFactory
from test_classes.national_focus_class import National_focus, NationalFocusFactory
from test_classes.generic_test_class import ResultsReporter


def test_check_events_ideology_optimisations(test_runner: object):
    events, paths = Events.get_all_events(test_runner=test_runner, lowercase=True, return_paths=True)
    results = []
    false_positives = ('austral.35', 'russoc.120')

    for event in events:
        e = EventFactory(event)
        if e.token in false_positives:
            continue
        if e.trigger and "has_government =" in e.trigger:
            for bundle in ideology_bundles:
                is_valid_candidate = len([i for i in ideology_bundles[bundle] if i in e.trigger]) == len(ideology_bundles[bundle])
                if is_valid_candidate:
                    results.append((e.token, paths[event], f'{bundle} can be used here instead of {ideology_bundles[bundle]}'))

    ResultsReporter.report_results(results=results, message="Events - possible candidates for has_xxx_government scripted triggers usage found.")


def test_check_focuses_ideology_optimisations(test_runner: object):
    focuses = National_focus.get_all_national_focuses(test_runner=test_runner, lowercase=False)
    results = []
    false_positives = ('ARG_Neutralize_The_Threat', 'SAF_native_trust_and_land_act', 'SWE_gyllenkrok_regime', 'NATFRA_Privatisation_Madness',
                       'NATFRA_Create_New_Elite', 'SAF_asiatic_land_tenure_act', 'SAF_natives_consolidation_act', )

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

    ResultsReporter.report_results(results=results, message="Focuses - possible candidates for has_xxx_government scripted triggers usage found.")


def test_check_decisions_ideology_optimisations(test_runner: object):
    decisions = Decisions.get_all_decisions(test_runner=test_runner, lowercase=True, return_paths=False)
    results = []
    false_positives = ('bul_join_reichspakt', 'can_support_government', 'lat_visit_to_rus', 'wif_combat_illegal_french_activity', 'ukr_galician_negotiations')
    for i in decisions:
        decision = DecisionsFactory(dec=i)
        is_valid_candidate = False

        if decision.token in false_positives:
            continue

        test_map = [
            decision.available,
            decision.visible,
            decision.target_root_trigger,
            decision.target_trigger,
        ]

        for bundle in ideology_bundles:
            for m in test_map:
                if m:
                    is_valid_candidate = len([i for i in ideology_bundles[bundle] if i in m]) == len(ideology_bundles[bundle])
                    if is_valid_candidate:
                        results.append((decision.token, f'available - {bundle} can be used here instead of {ideology_bundles[bundle]}'))

    ResultsReporter.report_results(results=results, message="Decisions - possible candidates for has_xxx_government scripted triggers usage found.")
