import glob
import os
import re
from pathlib import Path

from test_classes.generic_test_class import FileOpener


class ScriptedLocalisation:
    @classmethod
    def get_all_scripted_loc(cls, test_runner, lowercase: bool = True, return_paths: bool = False) -> list:
        """Parse all files in common/scripted_localisation and return the list with all scripted_localisation

        Args:
            test_runner (_type_): test runner obj
            lowercase (bool, optional): defines if returned list contains lowercase str or not. Defaults to True.
            return_paths (bool, optional): defines if scripted_localisation code is returned with dict that contains their filenames. Defaults to False.

        Returns:
            if return_paths - tuple[list, dict]: list with scripted_localisation and dict with filenames
            else - list: list with scripted_localisation code
        """
        filepath_to_loc = str(Path(test_runner.full_path_to_mod) / "common" / "scripted_localisation") + "/"
        container = []
        paths = {}
        for filename in glob.iglob(filepath_to_loc + '**/*.txt', recursive=True):
            text_file = FileOpener.open_text_file(filename, lowercase=lowercase)

            pattern_matches = re.findall(r'^[^ \n#]*? = \{.*?^\}', text_file, flags=re.DOTALL | re.MULTILINE)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    container.append(match)
                    paths[match] = os.path.basename(filename)

        if return_paths:
            return (container, paths)
        else:
            return container

    @classmethod
    def get_all_scripted_loc_names(cls, test_runner, lowercase: bool = True) -> list[str]:
        """Parse all files in triggers and return the list with all loc names

        Args:
            test_runner (_type_): test runner obj
            lowercase (bool, optional): defines if returned list contains lowercase str or not. Defaults to True.

        Returns:
            list: list with loc names
        """
        all_loc_code = ScriptedLocalisation.get_all_scripted_loc(test_runner=test_runner, lowercase=lowercase)
        all_loc_names = [ScriptedLocalisationFactory(i).name for i in all_loc_code]
        return all_loc_names


class ScriptedLocalisationFactory:
    def __init__(self, loc: str) -> None:
        self.name = re.findall(r'^\tname = (\S+)', loc, flags=re.MULTILINE)[0]
