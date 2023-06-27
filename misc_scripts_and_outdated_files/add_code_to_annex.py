import glob
import re

from ..test_classes.generic_test_class import FileOpener, ResultsReporter
from ..test_classes.events_class import Events


def test_add_code_to_sic(test_runner):
    results_dict = {}
    events = Events.get_all_events(test_runner=test_runner, lowercase=False, return_paths=False)
    key_string = "recheck_annexations"
    pattern = r'(^(\t+)option = \{.*?^\2\})'

    filepath_to_annex_effects = f'{test_runner.full_path_to_mod}common\\scripted_effects\\01_Annexation effects.txt'
    filepath_to_events = f'{test_runner.full_path_to_mod}events\\'
    annex_effects_with_recheck = []

    text_file = FileOpener.open_text_file(filepath_to_annex_effects, lowercase=False)
    all_annex_effects = re.findall(r'^[^\t\n]*? = \{.*?^\}', text_file, flags=re.DOTALL | re.MULTILINE)
    for i in all_annex_effects:
        if "recheck_annexations" in i:
            annex_effects_with_recheck.append(re.findall(r'^([^\t\n]*?) = \{', i)[0])

    print(annex_effects_with_recheck)

    results = []

    for event in events:
        event_id = re.findall('^\\tid = ([^ \\n\\t]+)', event, flags=re.MULTILINE)[0]
        if "annex" in event_id and event_id != "annex.1":
            pattern_matches = re.findall(pattern, event, flags=re.DOTALL | re.MULTILINE)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    option_code = match[0]
                    if key_string not in option_code and [i for i in annex_effects_with_recheck if i in option_code] == []:
                        results.append(event_id)
                        option_code_new = option_code[:-1] + "\trecheck_annexations = yes\n\t}"
                        results_dict[option_code] = option_code_new

    for filename in glob.iglob(filepath_to_events + "**/*.txt", recursive=True):
        text_file = FileOpener.open_text_file(filename, lowercase=False)
        for i in results_dict:
            if i in text_file:
                text_file = FileOpener.open_text_file(filename, lowercase=False)
                text_file_new = text_file.replace(i, results_dict[i])
                with open(filename, 'w', encoding="utf-8-sig") as text_file_write:
                    text_file_write.write(text_file_new)

    ResultsReporter.report_results(results=results, message="The annex event option doesn't have the recheck_annexations.")
