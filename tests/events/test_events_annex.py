##########################
# Test script to check for events with invalid title/desc
# By Pelmen, https://github.com/Pelmen323
##########################
import re
import glob

from test_classes.events_class import Events
from test_classes.generic_test_class import ResultsReporter, FileOpener


def test_check_annex_events(test_runner: object):
    results = []
    events_code = Events.get_all_events(test_runner=test_runner, filepath_should_contain='Annexation', filepath_should_not_contain='Core')
    replacement_dict = {}
    filepath_to_events = f'{test_runner.full_path_to_mod}events\\'

    for event in events_code:
        event_id = re.findall(r'^\tid = ([^ \n\t]+)', event, flags=re.MULTILINE)[0]
        options = re.findall(r'(^\toption = \{.*?^\t\})', event, flags=re.DOTALL | re.MULTILINE)
        event_options = []

        for option in options:
            name = re.findall(r'^\t\tname = ([^ \n\t]+)', option, flags=re.MULTILINE)[0]
            event_options.append(name)
            trigger = re.findall(r'(^\t\ttrigger = \{.*?^\t\t\})', option, flags=re.DOTALL | re.MULTILINE)[0] if "trigger = {" in option else False
            if trigger:
                event_target = False
                if "has_event_target" in trigger:
                    event_target = re.findall(r'has_event_target = ([^ \n\t]+)', trigger, flags=re.MULTILINE)[0]

            try:
                ai_chance = re.findall(r'(^\t\tai_chance = \{.*?\})', option, flags=re.MULTILINE)[0] if "ai_chance = {" in option else False
            except IndexError:
                ai_chance = re.findall(r'(^\t\tai_chance = \{.*?^\t\t\})', option, flags=re.DOTALL | re.MULTILINE)[0] if "ai_chance = {" in option else False

            # 2 All options with name = annex.give_to_overlord should have annexations_should_give_lands_to_overlord = yes in the trigger
            if name == "annex.give_to_overlord":
                if not trigger or "annexations_should_give_lands_to_overlord = yes" not in trigger:
                    results.append(f'{event_id} - annex.give_to_overlord option does not have annexations_should_give_lands_to_overlord = yes in trigger')

            # 3 All options with name = annex.integration should have annexations_can_annex = yes in the trigger
            elif name == "annex.integration":
                try:
                    trigger = re.findall(r'(^\t\ttrigger = \{.*?^\t\t\})', option, flags=re.DOTALL | re.MULTILINE)[0]
                    if "annexations_can_annex = yes" not in trigger:
                        results.append(f'{event_id} - annex.integration option does not have annexations_can_annex = yes in trigger')
                except IndexError:
                    results.append(f'{event_id} - annex.integration option does not have annexations_can_annex = yes in trigger - trigger block is missing')

            # 4 All annexation event options that are named give_to_britain, give_to_france, give_to_portugal, give_to_spain, give_to_belgium or give_to_japan that do not have this in the ai_chance
            elif name in ["annex.give_to_britain", "annex.give_to_france", "annex.give_to_portugal", "annex.give_to_spain", "annex.give_to_belgium", "annex.give_to_japan"]:
                if "modifier = {\n\t\t\t\tfactor = 0\n\t\t\t\tannexations_ai_will_consider_returning_colonies = no\n\t\t\t}" not in option and "modifier = {\n\t\t\t\tbase = 0\n\t\t\t\tannexations_ai_will_consider_returning_colonies = no\n\t\t\t}" not in option:
                    results.append(f'{event_id} - {name} option does not have annexations_AI_will_consider_returning_colonies = no in ai_chance')

            #  5. all annexation_can_annex = yes modifiers that have any other triggers within them?
            if ai_chance and "annexations_can_annex = yes" in ai_chance:
                ai_chance_expected = ai_chance.count("modifier = {\n\t\t\t\tfactor = 0\n\t\t\t\tannexations_can_annex = yes\n\t\t\t}")
                ai_chance_all_matches = ai_chance.count("annexations_can_annex = yes")
                if ai_chance_expected != ai_chance_all_matches:
                    results.append(f'{event_id} - {name} - contains "annexations_can_annex = yes" with other modifiers')

            # 5 REPLACEMENT CODE - RULE NO LONGER EXISTS all annexation options that have a defined ai_chance (i.e., ignore base = 0 or give_to_overlord) should have this as their last modifier
            # if "modifier = {" in option and event_target:
            #     if "NOT = { has_event_target" not in trigger:
            #         if not ai_chance.endswith("modifier = {\n\t\t\t\tfactor = 0.5\n\t\t\t\tevent_target:" + event_target + " = { is_subject = yes }\n\t\t\t}\n\t\t}"):
            #             # results.append(f'{event_id} - {name} option modifier does not end with ' + "event_target:" + event_target + ' = { is_subject = yes }')
            #             ai_chance_new = ai_chance[:-3] + '\t\t\tmodifier = {\n\t\t\t\tfactor = 0.5\n\t\t\t\tevent_target:' + event_target + ' = { is_subject = yes }\n\t\t\t}\n\t\t}'
            #             option_new = option.replace(ai_chance, ai_chance_new)
            #             replacement_dict[option] = option_new

        # 1 All events in the five annexation files should have an option with name = annex.give_to_overlord
        if "annex.give_to_overlord" not in event_options:
            results.append(f'{event_id} - missing option name annex.give_to_overlord')

    # for filename in glob.iglob(filepath_to_events + "**/*.txt", recursive=True):
    #     text_file = FileOpener.open_text_file(filename, lowercase=False)
    #     for i in replacement_dict:
    #         if i in text_file:
    #             text_file = FileOpener.open_text_file(filename, lowercase=False)
    #             text_file_new = text_file.replace(i, replacement_dict[i])
    #             with open(filename, 'w', encoding="utf-8-sig") as text_file_write:
    #                 text_file_write.write(text_file_new)

    ResultsReporter.report_results(results=results, message="Annex events - issues encountered.")
