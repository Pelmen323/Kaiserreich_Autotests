import glob
import os
import re

from test_classes.generic_test_class import FileOpener


class ScriptedTriggers:
    @classmethod
    def get_all_scripted_triggers(cls, test_runner, lowercase: bool = True, return_paths: bool = False) -> list[str]:
        """Parse all files in triggers and return the list with all triggers code

        Args:
            test_runner (_type_): test runner obj
            lowercase (bool, optional): defines if returned list contains lowercase str or not. Defaults to True.
            return_paths (bool, optional): defines if triggers code is returned with dict that contains their filenames. Defaults to False.

        Returns:
            if return_paths - tuple[list, dict]: list with triggers code and dict with triggers filenames
            else - list: list with triggers code
        """
        filepath_to_triggers = f'{test_runner.full_path_to_mod}common\\scripted_triggers\\'
        triggers = []
        paths = {}

        for filename in glob.iglob(filepath_to_triggers + '**/*.txt', recursive=True):
            if lowercase:
                text_file = FileOpener.open_text_file(filename)
            else:
                text_file = FileOpener.open_text_file(filename, lowercase=False)

            pattern_matches = re.findall('^[^ \\n]*? = \\{.*?^\\}', text_file, flags=re.DOTALL | re.MULTILINE)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    triggers.append(match)
                    paths[match] = os.path.basename(filename)

        if return_paths:
            return (triggers, paths)
        else:
            return triggers

    @classmethod
    def get_all_triggers_names(cls, test_runner, lowercase: bool = True) -> list:
        """Parse triggers file and return the list of all triggers

        Args:
            test_runner (test_runner): Contains filepaths

        Returns:
            list: all triggers in mod folder
        """
        triggers_code = ScriptedTriggers.get_all_scripted_triggers(test_runner=test_runner, lowercase=lowercase)
        triggers = []

        for trigger in triggers_code:
            pattern_matches = re.findall('^([^ \\n\\t]+) = \\{', trigger, flags=re.MULTILINE)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    triggers.append(match)

        return sorted(set(triggers))
