import glob
import re
import os
from ..test_classes.generic_test_class import FileOpener, DataCleaner, ResultsReporter


class Characters:

    @classmethod
    def get_all_characters(cls, test_runner) -> list[str]:
        """Parse all files and return the list with all characters code

        Args:
            test_runner (test_runner): Contains filepaths

        Returns:
            list: all characters code captured for each character
        """
        filepath_to_characters = f'{test_runner.full_path_to_mod}common\\characters\\'
        characters = []
        
        for filename in glob.iglob(filepath_to_characters + '**/*.txt', recursive=True):
            text_file = FileOpener.open_text_file(filename)

            pattern_matches = re.findall('((?<=\n)\t\w.* = \{.*\n(.|\n*?)*\n\t\})', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[0]
                    characters.append(match)

        return characters
    
    
    @classmethod
    def get_all_characters_with_paths(cls, test_runner) -> tuple[list, dict]:
        """Parse all files and return the list with all characters code

        Args:
            test_runner (test_runner): Contains filepaths

        Returns:
            list: all characters code captured for each character and dict with their filenames in a tuple
        """
        filepath_to_characters = f'{test_runner.full_path_to_mod}common\\characters\\'
        characters = []
        paths = {}
        
        for filename in glob.iglob(filepath_to_characters + '**/*.txt', recursive=True):
            text_file = FileOpener.open_text_file(filename)

            pattern_matches = re.findall('((?<=\n)\t\w.* = \{.*\n(.|\n*?)*\n\t\})', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[0]
                    characters.append(match)
                    paths[match] = os.path.basename(filename)

        return (characters, paths)
    

    @classmethod
    def get_all_advisors(cls, test_runner) -> list[str]:
        """Parse all files and return the list with all advisors code

        Args:
            test_runner (test_runner): Contains filepaths

        Returns:
            list: all advisors roles captured for each character (not including non-advisor code)
        """
        filepath_to_characters = f'{test_runner.full_path_to_mod}common\\characters\\'
        advisors = []
        
        for filename in glob.iglob(filepath_to_characters + '**/*.txt', recursive=True):
            text_file = FileOpener.open_text_file(filename)

            pattern_matches = re.findall('((?<=\n)\t\tadvisor = \{.*\n(.|\n*?)*\n\t\t\})', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[0]
                    advisors.append(match)

        return advisors
