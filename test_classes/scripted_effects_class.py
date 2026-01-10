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

    @classmethod
    def get_all_scripted_effects_names(cls, test_runner, lowercase: bool = True, exclude_files: list = []) -> list[str]:
        """Parse all files in triggers and return the list with all effects names

        Args:
            test_runner (_type_): test runner obj
            lowercase (bool, optional): defines if returned list contains lowercase str or not. Defaults to True.

        Returns:
            list: list with effects names
        """
        all_effects_code, paths = ScriptedEffects.get_all_scripted_effects(test_runner=test_runner, lowercase=lowercase, return_paths=True)
        all_effects_names = []
        skipfiles = len(exclude_files) > 0
        for effect in all_effects_code:
            current_filepath = paths[effect]
            if skipfiles:
                if any([path for path in exclude_files if path in current_filepath]):
                    continue
            all_effects_names.append(ScriptedEffectFactory(effect).id)

        assert len(all_effects_names) > 0
        return all_effects_names


class ScriptedEffectFactory:
    def __init__(self, effect: str) -> None:
        self.id = re.findall(r'^(\S+) = \{', effect, flags=re.MULTILINE)[0]
