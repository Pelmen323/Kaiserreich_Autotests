import glob
import os
import re

from ..test_classes.generic_test_class import FileOpener


class National_focus:

    @classmethod
    def get_all_national_focuses(cls, test_runner, lowercase: bool = True, return_paths: bool = False) -> list[str]:
        """Parse all files in common/national_focus and return the list with all national_focus code

        Args:
            test_runner (_type_): test runner obj
            lowercase (bool, optional): defines if returned list contains lowercase str or not. Defaults to True.
            return_paths (bool, optional): defines if national_focus code is returned with dict that contains their filenames. Defaults to False.

        Returns:
            if return_paths - tuple[list, dict]: list with national_focus code and dict with national_focus filenames
            else - list: list with national_focus code
        """
        filepath = f'{test_runner.full_path_to_mod}common\\national_focus\\'
        focuses = []
        paths = {}

        for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
            if lowercase:
                text_file = FileOpener.open_text_file(filename)
            else:
                text_file = FileOpener.open_text_file(filename, lowercase=False)

            pattern_matches = re.findall('((?<=\n)\\tfocus = \\{.*\n(.|\n*?)*\n\\t\\})', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[0]
                    focuses.append(match)
                    paths[match] = os.path.basename(filename)

            pattern_matches = re.findall('((?<=\n)shared_focus = \\{.*\n(.|\n*?)*\n\\})', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[0]
                    focuses.append(match)
                    paths[match] = os.path.basename(filename)

        if return_paths:
            return (focuses, paths)
        else:
            return focuses

    @classmethod
    def get_all_national_focuses_names(cls, test_runner, lowercase: bool = True, return_paths: bool = False) -> list[str]:
        """Parse all files in common/national_focus and return the list with all national_focus names

        Args:
            test_runner (_type_): test runner obj
            lowercase (bool, optional): defines if returned list contains lowercase str or not. Defaults to True.
            return_paths (bool, optional): defines if national_focus code is returned with dict that contains their filenames. Defaults to False.

        Returns:
            if return_paths - tuple[list, dict]: list with national_focus IDs and dict with national_focus filenames
            else - list: list with national_focus IDs
        """
        focuses_names = []
        paths = {}

        if return_paths:
            focuses, paths_focus = National_focus.get_all_national_focuses(test_runner=test_runner, lowercase=lowercase, return_paths=return_paths)
        else:
            focuses = National_focus.get_all_national_focuses(test_runner=test_runner, lowercase=lowercase)

        for focus in focuses:
            focus_id = re.findall('\\t+?id = \\b([^ \\n\\t]+)\\b', focus)[0]
            focuses_names.append(focus_id)
            if return_paths:
                paths[focus_id] = paths_focus[focus]

        if return_paths:
            return (focuses_names, paths)
        else:
            return focuses_names
