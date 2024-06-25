import re

from test_classes.national_focus_class import NationalFocusFactory
from test_classes.generic_test_class import FileOpener


def test_add_code_to_sia_focus(test_runner):
    results_dict = {}
    filename = f'{test_runner.full_path_to_mod}common\\national_focus\\SIA focus (Siam).txt'
    focuses = []

    text_file = FileOpener.open_text_file(filename, lowercase=False)

    pattern_matches = re.findall('((?<=\n)\\tfocus = \\{.*\n(.|\n*?)*\n\\t\\})', text_file)
    if len(pattern_matches) > 0:
        for match in pattern_matches:
            match = match[0]
            focuses.append(match)

    pattern_matches = re.findall('((?<=\n)shared_focus = \\{.*\n(.|\n*?)*\n\\})', text_file)
    if len(pattern_matches) > 0:
        for match in pattern_matches:
            match = match[0]
            focuses.append(match)

    for focus in focuses:
        f = NationalFocusFactory(focus)
        if "event_target:original_siam = { complete_national_focus" not in focus:
            try:
                completion_reward = re.findall(r'(completion_reward = \{.*?)\n\t\t}', focus, flags=re.DOTALL | re.MULTILINE)[0]
            except Exception:
                print(f.id)
                raise
            completion_reward_new = completion_reward + "\n\t\t\thidden_effect = {\n\t\t\t\tif = {\n\t\t\t\t\tlimit = {\n\t\t\t\t\t\tis_dynamic_country = yes\n\t\t\t\t\t\tNOT = { country_exists = event_target:original_siam }\n\t\t\t\t\t}\n\t\t\t\t\tevent_target:original_siam = { complete_national_focus = " + f.id + " }\n\t\t\t\t}\n\t\t\t}"
            results_dict[completion_reward] = completion_reward_new
        else:
            print(f.id)

    text_file = FileOpener.open_text_file(filename, lowercase=False)
    for i in results_dict:
        if i in text_file:
            text_file = FileOpener.open_text_file(filename, lowercase=False)
            text_file_new = text_file.replace(i, results_dict[i])
            with open(filename, 'w', encoding="utf-8") as text_file_write:
                text_file_write.write(text_file_new)
