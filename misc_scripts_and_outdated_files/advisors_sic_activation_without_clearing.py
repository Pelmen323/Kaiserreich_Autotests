##########################
# Test script to check for sic ativation without clearing slot
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re
import os
from ..test_classes.generic_test_class import ResultsReporter, FileOpener
from ..test_classes.characters_class import Characters, Advisors
from ..test_classes.events_class import Events


def test_check_advisors_activation_without_clearing_slot(test_runner: object):
    filepath = test_runner.full_path_to_mod
    advisors = Characters.get_all_advisors(test_runner=test_runner)
    sic = []
    results = []

    for advisor_code in advisors:
        adv = Advisors(adv=advisor_code)

        if adv.sic_role:
            sic.append(adv.token)

    for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
        if "history" in filename: continue
        if "effects" in filename: continue
        if "on_actions" in filename: continue
        if "events" in filename: continue
        text_file = FileOpener.open_text_file(filename)

        if 'activate_advisor' in text_file:
            for sic_advisor in sic:
                if f'	activate_advisor = {sic_advisor}' in text_file:
                    pattern = f'clear_sic_slot = yes.*\\n.*\\tactivate_advisor = {sic_advisor}\\b'
                    pattern_matches = re.findall(pattern, text_file)
                    if len(pattern_matches) < text_file.count(f'	activate_advisor = {sic_advisor}'):
                        results.append((f'activate_advisor = {sic_advisor}', os.path.basename(filename)))

    for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
        if "on_actions" not in filename and "effects" not in filename:
            continue
        text_file = FileOpener.open_text_file(filename)

        if 'activate_advisor' in text_file:
            for sic_advisor in sic:
                if f'	activate_advisor = {sic_advisor}' in text_file:
                    if "on_actions" in filename:
                        pattern_matches = re.findall('^\\ton_\\w+ = \\{.*?^\\t\\}', text_file, flags=re.DOTALL | re.MULTILINE)
                    elif "effects" in filename:
                        pattern_matches = re.findall('^\\w+ = \\{.*?^\\}', text_file, flags=re.DOTALL | re.MULTILINE)
                    if len(pattern_matches) > 0:
                        for match in pattern_matches:
                            if f'	activate_advisor = {sic_advisor}' in match:
                                if 'clear_sic_slot = yes' not in match:
                                    results.append((f'activate_advisor = {sic_advisor}', os.path.basename(filename)))

    events, paths = Events.get_all_events(test_runner=test_runner, lowercase=True, return_paths=True)
    for event in events:
        if 'activate_advisor' in event:
            for sic_advisor in sic:
                if f'	activate_advisor = {sic_advisor}' in event:
                    if 'clear_sic_slot = yes' not in event:
                        results.append((f'activate_advisor = {sic_advisor}', paths[event]))

    ResultsReporter.report_results(results=results, message="SIC Advisors activation without clearing sic slot encountered. Check console output")
