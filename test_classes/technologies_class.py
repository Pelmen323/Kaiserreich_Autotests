import glob
import os
import re
from pathlib import Path

from test_classes.generic_test_class import FileOpener


class Technologies:
    @classmethod
    def get_code(cls, test_runner, lowercase: bool = True, return_paths: bool = False) -> list[str]:
        """Parse all files return the list with all vars
        Args:
            test_runner (_type_): test runner obj
            lowercase (bool, optional): defines if returned list contains lowercase str or not. Defaults to True.
            return_paths (bool, optional): defines if vars code is returned with dict that contains their filenames. Defaults to False.

        Returns:
            if return_paths - tuple[list, dict]: list with vars and dict with filenames
            else - list: list with vars code
        """
        filepath = str(Path(test_runner.full_path_to_mod) / "common" / "technologies") + "/"
        lst = []
        paths = {}
        pattern = re.compile(r"^\t.*? = \{.*?^\t\}", flags=re.MULTILINE | re.DOTALL)

        for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
            text_file = FileOpener.open_text_file(filename, lowercase=lowercase)
            pattern_matches = re.findall(pattern, text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    lst.append(match)
                    paths[match] = os.path.basename(filename)

        if return_paths:
            return (lst, paths)
        else:
            return lst


class TechFactory:
    def __init__(self, tech: str) -> None:
        try:
            self.token = re.findall(r'^\t([^# \t]+) = \{', tech, flags=re.MULTILINE)[0]
        except Exception:
            print(tech)
            raise
