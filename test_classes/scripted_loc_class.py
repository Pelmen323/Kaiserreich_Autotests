import glob
import re
import os
from ..test_classes.generic_test_class import FileOpener


class Scripted_localisation:
    @classmethod
    def get_scripted_loc_names(cls, test_runner, lowercase: bool = True, return_paths: bool = False) -> list:
        """Parse all files in common/scripted_localisation and return the list with all scripted_localisation names

        Args:
            test_runner (_type_): test runner obj
            lowercase (bool, optional): defines if returned list contains lowercase str or not. Defaults to True.
            return_paths (bool, optional): defines if scripted_localisation code is returned with dict that contains their filenames. Defaults to False.

        Returns:
            if return_paths - tuple[list, dict]: list with scripted_localisation names and dict with filenames
            else - list: list with scripted_localisation code
        """
        filepath_to_decisions = f'{test_runner.full_path_to_mod}common\\scripted_localisation\\'
        container = []
        paths = {}
        for filename in glob.iglob(filepath_to_decisions + '**/*.txt', recursive=True):
            if lowercase:
                text_file = FileOpener.open_text_file(filename)
            else:
                text_file = FileOpener.open_text_file(filename, lowercase=False)

            text_file_splitted = text_file.split('\n')[1:]
            for line in range(len(text_file_splitted)):
                current_line = text_file_splitted[line]
                pattern_matches = re.findall('^\\tname = (\\w*)', current_line)
                if len(pattern_matches) > 0:
                    for match in pattern_matches:
                        container.append(match)
                        paths[match] = os.path.basename(filename)

        if return_paths:
            return (container, paths)
        else:
            return container
