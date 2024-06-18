##########################
# Test script to check if `set_autonomy` has `end_wars = no` statement
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re

from ..test_classes.generic_test_class import FileOpener

FALSE_POSITIVES = ("target = nat")


def test_check_syntax_set_autonomy(test_runner: object):
    filepath = test_runner.full_path_to_mod
    override_dict = {}

    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename, lowercase=False)

        if 'custom_trigger_tooltip' in text_file:
            pattern_matches = re.findall(r"^((\t*?)custom_trigger_tooltip = \{\n\t+tooltip = [^\n]+\n\t+check_variable = {.*?\}\n\2\})", text_file, flags=re.DOTALL | re.MULTILINE)
            # pattern_matches = re.findall(r"^((\t*?)custom_trigger_tooltip = \{\n\t+check_variable = {[^\n]+}\n\t+tooltip = [^\n]+\n\2\})", text_file, flags=re.DOTALL | re.MULTILINE)
            # pattern_matches = re.findall(r"^((\t*?)custom_effect_tooltip = \{\n\t+tooltip = [^\n]+\n\t+check_variable = {[^\n]+}\n\2\})", text_file, flags=re.DOTALL | re.MULTILINE)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    if "compare" not in match[0]:
                        replacement = match[0].replace('check_variable = { ', '').replace(' }', '').replace('custom_trigger_tooltip', 'check_variable')
                        override_dict[match[0]] = replacement
                        # if "check_variable" in match[1]:
                        #     results.append((match[1].replace('\t', '').replace('\n', '  '), os.path.basename(filename)))

    for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
        text_file = FileOpener.open_text_file(filename, lowercase=False)
        text_file_new = text_file
        override = False
        for key, value in override_dict.items():
            if key in text_file:
                override = True
                text_file_new = text_file_new.replace(key, value)

        if override:
            with open(filename, 'w', encoding="utf-8") as text_file_write:
                text_file_write.write(text_file_new)

    # ResultsReporter.report_results(results=results, message="Add `end_wars = no` to this statement. Check console output")
