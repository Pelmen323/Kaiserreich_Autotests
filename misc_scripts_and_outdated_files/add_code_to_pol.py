import glob
import re

from ..test_classes.characters_class import Advisors, Characters
from ..test_classes.generic_test_class import FileOpener


def test_add_code_to_sic(test_runner):
    results_dict = {}
    advisors = Characters.get_all_advisors(test_runner=test_runner, lowercase=False)

    for advisor_code in advisors:
        adv = Advisors(adv=advisor_code)
        if adv.political_role:
            tabs_to_extract = re.findall("(\\t+)slot = political_advisor", advisor_code)[0]
            line_to_insert = "slot = political_advisor\n" + tabs_to_extract + "on_add = { add_to_variable = { amount_hired_political_advisors = 1 } }\n" + tabs_to_extract + "on_remove = { add_to_variable = { amount_hired_political_advisors = -1 } }"
            advisor_code_new = advisor_code.replace("slot = political_advisor", line_to_insert)
            results_dict[advisor_code] = advisor_code_new

    for filename in glob.iglob(test_runner.full_path_to_mod + "**/*.txt", recursive=True):
        text_file = FileOpener.open_text_file(filename, lowercase=False)
        for i in results_dict:
            if i in text_file:
                text_file = FileOpener.open_text_file(filename, lowercase=False)
                text_file_new = text_file.replace(i, results_dict[i])
                with open(filename, 'w', encoding="utf-8") as text_file_write:
                    text_file_write.write(text_file_new)
