import glob
import re

from test_classes.generic_test_class import FileOpener, ResultsReporter
from test_classes.events_class import Events


def test_add_code_to_sic(test_runner):
    results_dict = {}
    results_dict2 = {}
    events = Events.get_all_events(test_runner=test_runner, lowercase=False, filepath_should_contain="Annex", filepath_should_not_contain="Core")
    key_string = "recheck_annexations = yes"
    pattern = r'(^(\t+)option = \{.*?^\2\})'

    filepath_to_events = f'{test_runner.full_path_to_mod}events\\'
    results = []

    for event in events:
        event_id = re.findall('^\\tid = (\\S+)', event, flags=re.MULTILINE)[0]
        if "annex" in event_id and event_id != "annex.1":
            pattern_matches = re.findall(pattern, event, flags=re.DOTALL | re.MULTILINE)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    option_code = match[0]
                    if key_string in option_code:
                        results.append(event_id)
                        option_code_new = option_code.replace("\t\trecheck_annexations = yes\n", "")
                        results_dict[option_code] = option_code_new

    for filename in glob.iglob(filepath_to_events + "**/*.txt", recursive=True):
        text_file = FileOpener.open_text_file(filename, lowercase=False)
        for i in results_dict:
            if i in text_file:
                text_file = FileOpener.open_text_file(filename, lowercase=False)
                text_file_new = text_file.replace(i, results_dict[i])
                with open(filename, 'w', encoding="utf-8") as text_file_write:
                    text_file_write.write(text_file_new)

    events = Events.get_all_events(test_runner=test_runner, lowercase=False, filepath_should_contain="Annex", filepath_should_not_contain="Core")
    results = sorted(list(set(results)))
    for event in events:
        event_id = re.findall('^\\tid = (\\S+)', event, flags=re.MULTILINE)[0]
        if event_id in results:
            event_new = event[:-1] + "\n\n\tafter = {\n\t\trecheck_annexations = yes\n\t}\n"
            results_dict2[event] = event_new

    for filename in glob.iglob(filepath_to_events + "**/*.txt", recursive=True):
        text_file = FileOpener.open_text_file(filename, lowercase=False)
        for i in results_dict2:
            if i in text_file:
                text_file = FileOpener.open_text_file(filename, lowercase=False)
                text_file_new = text_file.replace(i, results_dict2[i])
                with open(filename, 'w', encoding="utf-8") as text_file_write:
                    text_file_write.write(text_file_new)
    ResultsReporter.report_results(results=results, message="Affected events.")


# def test_add_code_to_sic(test_runner):
#     results_dict = {}
#     events = Events.get_all_events(test_runner=test_runner, lowercase=False, return_paths=False)
#     key_string = "recheck_annexations"
#     pattern = r'(^(\t+)option = \{.*?^\2\})'

#     filepath_to_events = f'{test_runner.full_path_to_mod}events\\'

#     results = []

#     for event in events:
#         event_id = re.findall('^\\tid = (\\S+)', event, flags=re.MULTILINE)[0]
#         if "annex" in event_id and event_id != "annex.1":
#             pattern_matches = re.findall(pattern, event, flags=re.DOTALL | re.MULTILINE)
#             if len(pattern_matches) > 0:
#                 for match in pattern_matches:
#                     option_code = match[0]
#                     if key_string not in option_code:
#                         results.append(event_id)
#                         option_code_new = option_code[:-1] + "\trecheck_annexations = yes\n\t}"
#                         results_dict[option_code] = option_code_new

#     for filename in glob.iglob(filepath_to_events + "**/*.txt", recursive=True):
#         text_file = FileOpener.open_text_file(filename, lowercase=False)
#         for i in results_dict:
#             if i in text_file:
#                 text_file = FileOpener.open_text_file(filename, lowercase=False)
#                 text_file_new = text_file.replace(i, results_dict[i])
#                 with open(filename, 'w', encoding="utf-8-sig") as text_file_write:
#                     text_file_write.write(text_file_new)

#     ResultsReporter.report_results(results=results, message="The annex event option doesn't have the recheck_annexations.")
