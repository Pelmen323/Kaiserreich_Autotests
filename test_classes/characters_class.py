import glob
import re
import os
from ..test_classes.generic_test_class import FileOpener


class Characters:

    @classmethod
    def get_all_characters(cls, test_runner, lowercase: bool = True, return_paths: bool = False) -> tuple[list, dict]:
        """Parse all files in common/characters and return the list with all characters code

        Args:
            test_runner (_type_): test runner obj
            lowercase (bool, optional): defines if returned list contains lowercase str or not. Defaults to True.
            return_paths (bool, optional): defines if characters code is returned with dict that contains their filenames. Defaults to False.

        Returns:
            if lowercase - tuple[list, dict]: list with characters code and dict with characters filenames
            else - list: list with characters code
        """
        filepath_to_characters = f'{test_runner.full_path_to_mod}common\\characters\\'
        characters = []
        paths = {}

        for filename in glob.iglob(filepath_to_characters + '**/*.txt', recursive=True):
            if lowercase:
                text_file = FileOpener.open_text_file(filename)
            else:
                text_file = FileOpener.open_text_file_non_lower(filename)

            pattern_matches = re.findall('((?<=\n)\t\\w.* = \\{.*\n(.|\n*?)*\n\t\\})', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[0]
                    characters.append(match)
                    paths[match] = os.path.basename(filename)

        if return_paths:
            return (characters, paths)
        else:
            return characters

    @classmethod
    def get_all_advisors(cls, test_runner, lowercase: bool = True, return_paths: bool = False) -> tuple[list, dict]:
        """Parse all files in common/characters and return the list with all advisors code

        Args:
            test_runner (_type_): test runner obj
            lowercase (bool, optional): defines if returned list contains lowercase str or not. Defaults to True.
            return_paths (bool, optional): defines if advisors code is returned with dict that contains their filenames. Defaults to False.

        Returns:
            if lowercase - tuple[list, dict]: list with advisors code and dict with advisors filenames
            else - list: list with advisors code
        """
        filepath_to_characters = f'{test_runner.full_path_to_mod}common\\characters\\'
        advisors = []
        paths = {}

        for filename in glob.iglob(filepath_to_characters + '**/*.txt', recursive=True):
            if lowercase:
                text_file = FileOpener.open_text_file(filename)
            else:
                text_file = FileOpener.open_text_file_non_lower(filename)

            pattern_matches = re.findall('((?<=\n)\t\tadvisor = \\{.*\n(.|\n*?)*\n\t\t\\})', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[0]
                    advisors.append(match)
                    paths[match] = os.path.basename(filename)

        if return_paths:
            return (advisors, paths)
        else:
            return advisors

    @classmethod
    def get_advisors_traits(cls, test_runner, trait_type: str, lowercase: bool = True) -> list[str]:
        """Parse common\\country_leader\\xxx.txt and return the list with all advisor traits

        Args:
            test_runner (_type_): Contains filepaths
            trait_type (str): Str - any of (second_in_command, political_advisor, high_command, theorist, air_chief, army_chief, navy_chief)
            lowercase (bool): if returned str is lowercase or not

        Returns:
            list[str]: all traits from a file (only traits names)
        """
        filepath_to_traits = f'{test_runner.full_path_to_mod}common\\country_leader\\KR_{trait_type}_traits.txt'
        traits = []

        if lowercase:
            text_file = FileOpener.open_text_file(filepath_to_traits)
        else:
            text_file = FileOpener.open_text_file_non_lower(filepath_to_traits)

        pattern_matches = re.findall('((?<=\n)\t\\w* = \\{)', text_file)
        if len(pattern_matches) > 0:
            for match in pattern_matches:
                match = match[1:-4]
                traits.append(match)

        if trait_type == "second_in_command":
            traits.append('second_in_command_trait')
        return traits
