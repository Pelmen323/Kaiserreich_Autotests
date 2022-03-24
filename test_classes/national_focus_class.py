import glob
import re
import os
from ..test_classes.generic_test_class import FileOpener, DataCleaner, ResultsReporter


class National_focus:

    @classmethod
    def get_all_national_focuses(cls, test_runner, lowercase: bool) -> list[str]:
        """Parse all files and return the list with all national focuses code

        Args:
            test_runner (test_runner): Contains filepaths

        Returns:
            list: all national focuses code captured for each focus present in files
        """
        filepath = f'{test_runner.full_path_to_mod}common\\national_focus\\'
        focuses = []
        
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

        return focuses



    @classmethod
    def get_all_national_focuses_with_paths(cls, test_runner, lowercase: bool) -> list[str]:
        """Parse all files and return the list with all national focuses code

        Args:
            test_runner (test_runner): Contains filepaths

        Returns:
            list: all national focuses code captured for each focus present in files
            dict: paths to focuses
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

        return (focuses, paths)
