import re

from core.runner import TestRunner
from test_classes.generic_test_class import FileOpener


def format_vp_endonym_file(username, mod_name):
    runner = TestRunner(username, mod_name)
    filename = f'{runner.full_path_to_mod}common\\scripted_localisation\\00 - Scripted VP Endonyms.txt'
    text_file = FileOpener.open_text_file(filename, lowercase=False)
    vp_loc_entries = re.findall("^defined_text = \\{.*?^\\}", text_file, flags=re.MULTILINE | re.DOTALL)
    results_dict = {}
    for i in vp_loc_entries:
        if i.count("localization_key =") > 1:       # Not touching entries with only 1 loc key
            x = re.findall("text = \\{\\n\\t*localization_key = (VICTORY_POINTS_.*)", i)[0]
            y = re.findall("name = GetVictoryPointName.*\\n", i)[0]
            z = y + '\ttext = {\n\t\ttrigger = { NOT = { has_global_flag = allowrenaming_flag } }\n\t\tlocalization_key = ' + x + '\n\t}\n'
            results_dict[y] = z

    for i in results_dict:
        text_file = FileOpener.open_text_file(filename, lowercase=False)
        text_file_new = text_file.replace(i, results_dict[i])
        with open(filename, 'w', encoding="utf-8") as text_file_write:
            text_file_write.write(text_file_new)


if __name__ == '__main__':
    format_vp_endonym_file(username="VADIM", mod_name="Kaiserreich Dev Build")
