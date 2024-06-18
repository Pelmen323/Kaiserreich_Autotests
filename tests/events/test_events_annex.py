##########################
# Test script to check for events with invalid title/desc
# By Pelmen, https://github.com/Pelmen323
##########################
import re

from ...test_classes.events_class import Events
from ...test_classes.generic_test_class import ResultsReporter


def test_check_unsupported_title_desc_combination(test_runner: object):
    results = []
    events_code = Events.get_all_events(test_runner=test_runner, lowercase=True, filepath_should_contain='Annexation', filepath_should_not_contain='Core')

    for event in events_code:
        event_id = re.findall(r'^\tid = ([^ \n\t]+)', event, flags=re.MULTILINE)[0]
        options = re.findall(r'(^\toption = \{.*?^\t\})', event, flags=re.DOTALL | re.MULTILINE)
        event_options = []

        for option in options:
            name = re.findall(r'^\t\tname = ([^ \n\t]+)', option, flags=re.MULTILINE)[0]
            event_options.append(name)

            # 2 All options with name = annex.give_to_overlord should have annexations_should_give_lands_to_overlord = yes in the trigger
            if name == "annex.give_to_overlord":
                trigger = re.findall(r'(^\t\ttrigger = \{.*?^\t\t\})', option, flags=re.DOTALL | re.MULTILINE)[0]
                if "annexations_should_give_lands_to_overlord = yes" not in trigger:
                    results.append(f'{event_id} - annex.give_to_overlord option does not have annexations_should_give_lands_to_overlord = yes in trigger')

            # 3 All options with name = annex.integration should have annexations_can_annex = yes in the trigger
            elif name == "annex.integration":
                try:
                    trigger = re.findall(r'(^\t\ttrigger = \{.*?^\t\t\})', option, flags=re.DOTALL | re.MULTILINE)[0]
                    if "annexations_can_annex = yes" not in trigger:
                        results.append(f'{event_id} - annex.integration option does not have annexations_can_annex = yes in trigger')
                except IndexError:
                    results.append(f'{event_id} - annex.integration option does not have annexations_can_annex = yes in trigger - trigger block is missing')

        # 1 All events in the five annexation files should have an option with name = annex.give_to_overlord
        if "annex.give_to_overlord" not in event_options:
            results.append(f'{event_id} - missing option name annex.give_to_overlord')

        # 4 The last option of each event should be named name = annex.occupation and have annexations_is_allowed_to_occupy = yes and nothing else as the trigger
        if event_options[-1] != "annex.occupation":
            results.append(f'{event_id} - The last option of each event should be named name = annex.occupation')

        else:
            try:
                trigger = re.findall(r'(^\t\ttrigger = \{.*?^\t\t\})', option, flags=re.DOTALL | re.MULTILINE)[0]
                if "annexations_is_allowed_to_occupy = yes" not in trigger:
                    results.append(f'{event_id} - last event option annex.occupation - should have annexations_is_allowed_to_occupy = yes as the trigger')
            except IndexError:
                results.append(f'{event_id} - last event option annex.occupation - should have annexations_is_allowed_to_occupy = yes as the trigger - trigger block is missing')

    ResultsReporter.report_results(results=results, message="Annex events - issues encountered.")
