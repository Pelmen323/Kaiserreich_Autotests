import glob
import re

from ..test_classes.characters_class import Advisors, Characters
from ..test_classes.generic_test_class import FileOpener


def test_add_code_to_sic(test_runner):
    results_dict = {}
    advisors = Characters.get_all_advisors(test_runner=test_runner, lowercase=False)
    characters = Characters.get_all_characters(test_runner=test_runner, lowercase=False)
    activate_advisor_effect = Characters.get_all_add_advisor_effects(test_runner=test_runner, lowercase=False)

    for advisor_code in advisors:
        adv = Advisors(adv=advisor_code)
        char_id = None
        if adv.sic_role:
            for item in characters:
                if advisor_code in item:
                    char_id = re.findall('^\\t(.+) =', item)[0]
                    break

            if char_id is None:
                for item in activate_advisor_effect:
                    if advisor_code in item:
                        try:
                            char_id = re.findall('\\t+character = (.+)', item)[0]
                        except Exception:
                            char_id = adv.token
                        break

            # if char_id is None:
            #     print(advisor_code)
            tabs_to_extract = re.findall("(\\t+)removal_cost = -1", advisor_code)[0]
            line_to_insert = "removal_cost = -1\n" + tabs_to_extract + "on_add = {\n" \
                                                   + tabs_to_extract + "\trandom_character = {\n" \
                                                   + tabs_to_extract + "\t\tlimit = { is_character = " + char_id + " }\n" \
                                                   + tabs_to_extract + "\t\tset_character_flag = is_second_in_command\n" \
                                                   + tabs_to_extract + "\t\tset_variable = { PREV.current_second_in_command_character = THIS }\n" \
                                                   + tabs_to_extract + "\t}\n" \
                                                   + tabs_to_extract + "}\n" \
                                                   + tabs_to_extract + "on_remove = {\n" \
                                                   + tabs_to_extract + "\t" + char_id + " = { clr_character_flag = is_second_in_command }\n" \
                                                   + tabs_to_extract + "\tclear_variable = current_second_in_command_character\n" \
                                                   + tabs_to_extract + "}"
            advisor_code_new = advisor_code.replace("removal_cost = -1", line_to_insert)
            results_dict[advisor_code] = advisor_code_new

    for filename in glob.iglob(test_runner.full_path_to_mod + "**/*.txt", recursive=True):
        text_file = FileOpener.open_text_file(filename, lowercase=False)
        for i in results_dict:
            if i in text_file:
                text_file = FileOpener.open_text_file(filename, lowercase=False)
                text_file_new = text_file.replace(i, results_dict[i])
                with open(filename, 'w', encoding="utf-8") as text_file_write:
                    text_file_write.write(text_file_new)
