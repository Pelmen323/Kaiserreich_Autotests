import glob
import re
import os
from ..test_classes.generic_test_class import FileOpener


class National_focus:

    @classmethod
    def get_all_national_focuses_with_paths(cls, test_runner, lowercase: bool = True, return_paths: bool = False) -> list[str]:
        """Parse all files in common/national_focus and return the list with all national_focus code

        Args:
            test_runner (_type_): test runner obj
            lowercase (bool, optional): defines if returned list contains lowercase str or not. Defaults to True.
            return_paths (bool, optional): defines if national_focus code is returned with dict that contains their filenames. Defaults to False.

        Returns:
            if lowercase - tuple[list, dict]: list with national_focus code and dict with national_focus filenames
            else - list: list with national_focus code
        """
        filepath = f'{test_runner.full_path_to_mod}common\\national_focus\\'
        focuses = []
        paths = {}

        for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
            if lowercase:
                text_file = FileOpener.open_text_file(filename)
            else:
                text_file = FileOpener.open_text_file_non_lower(filename)

            pattern_matches = re.findall('((?<=\n)\\tfocus = \\{.*\n(.|\n*?)*\n\\t\\})', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[0]
                    focuses.append(match)
                    paths[match] = os.path.basename(filename)

        if return_paths:
            return (focuses, paths)
        else:
            return focuses
