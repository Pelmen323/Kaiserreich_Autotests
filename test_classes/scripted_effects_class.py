import glob
import os
import re
from pathlib import Path

from test_classes.generic_test_class import FileOpener


class ScriptedEffects:
    @classmethod
    def get_all_scripted_effects(cls, test_runner, lowercase: bool = True, return_paths: bool = False) -> list[str]:
        """Parse all files in effects and return the list with all effects code

        Args:
            test_runner (_type_): test runner obj
            lowercase (bool, optional): defines if returned list contains lowercase str or not. Defaults to True.
            return_paths (bool, optional): defines if effects code is returned with dict that contains their filenames. Defaults to False.

        Returns:
            if return_paths - tuple[list, dict]: list with effects code and dict with effects filenames
            else - list: list with effects code
        """
        filepath_to_effects = str(Path(test_runner.full_path_to_mod) / "common" / "scripted_effects") + "/"
        effects = []
        paths = {}

        for filename in glob.iglob(filepath_to_effects + '**/*.txt', recursive=True):
            text_file = FileOpener.open_text_file(filename, lowercase=lowercase)

            pattern_matches = re.findall(r'^[^ \n#]*? = \{.*?^\}', text_file, flags=re.DOTALL | re.MULTILINE)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    effects.append(match)
                    paths[match] = os.path.basename(filename)

        if return_paths:
            return (effects, paths)
        else:
            return effects


class ScriptedEffectFactory:
    def __init__(self, effect: str) -> None:
        self.id = re.findall(r'^(\S+) = \{', effect, flags=re.MULTILINE)[0]
