import glob
import re
import os
from ..test_classes.generic_test_class import FileOpener, DataCleaner, ResultsReporter


class Characters:

    @classmethod
    def get_all_characters(cls, test_runner, lowercase: bool) -> list[str]:
        """Parse all files and return the list with all characters code

        Args:
            test_runner (test_runner): Contains filepaths

        Returns:
            list: all characters code captured for each character
        """
        filepath_to_characters = f'{test_runner.full_path_to_mod}common\\characters\\'
        characters = []
        
        for filename in glob.iglob(filepath_to_characters + '**/*.txt', recursive=True):
            if lowercase:
                text_file = FileOpener.open_text_file(filename)
            else:
                text_file = FileOpener.open_text_file_non_lower(filename)

            pattern_matches = re.findall('((?<=\n)\t\w.* = \{.*\n(.|\n*?)*\n\t\})', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[0]
                    characters.append(match)

        return characters
    
    
    @classmethod
    def get_all_characters_with_paths(cls, test_runner, lowercase: bool) -> tuple[list, dict]:
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
            if lowercase:
                text_file = FileOpener.open_text_file(filename)
            else:
                text_file = FileOpener.open_text_file_non_lower(filename)

            pattern_matches = re.findall('((?<=\n)\t\w.* = \{.*\n(.|\n*?)*\n\t\})', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[0]
                    characters.append(match)
                    paths[match] = os.path.basename(filename)

        return (characters, paths)
    

    @classmethod
    def get_all_advisors(cls, test_runner, lowercase: bool) -> list[str]:
        """Parse all files and return the list with all advisors code

        Args:
            test_runner (test_runner): Contains filepaths

        Returns:
            list: all advisors roles captured for each character (not including non-advisor code)
        """
        filepath_to_characters = f'{test_runner.full_path_to_mod}common\\characters\\'
        advisors = []
        
        for filename in glob.iglob(filepath_to_characters + '**/*.txt', recursive=True):
            if lowercase:
                text_file = FileOpener.open_text_file(filename)
            else:
                text_file = FileOpener.open_text_file_non_lower(filename)

            pattern_matches = re.findall('((?<=\n)\t\tadvisor = \{.*\n(.|\n*?)*\n\t\t\})', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[0]
                    advisors.append(match)

        return advisors

   
    @classmethod
    def get_all_advisors_with_paths(cls, test_runner, lowercase: bool) -> tuple[list, dict]:
        """Parse all files and return the list with all advisors code anjd their paths

        Args:
            test_runner (test_runner): Contains filepaths

        Returns:
            list: all advisors roles captured for each character (not including non-advisor code) and their paths
        """
        filepath_to_characters = f'{test_runner.full_path_to_mod}common\\characters\\'
        advisors = []
        paths = {}
        
        for filename in glob.iglob(filepath_to_characters + '**/*.txt', recursive=True):
            if lowercase:
                text_file = FileOpener.open_text_file(filename)
            else:
                text_file = FileOpener.open_text_file_non_lower(filename)

            pattern_matches = re.findall('((?<=\n)\t\tadvisor = \{.*\n(.|\n*?)*\n\t\t\})', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[0]
                    advisors.append(match)
                    paths[match] = os.path.basename(filename)

        return (advisors, paths)
    
    @classmethod
    def get_all_sic_traits(cls, test_runner, lowercase: bool) -> list[str]:
        """Parse common\country_leader\KR_second_in_command_traits.txt and return the list with all sic traits

        Args:
            test_runner (test_runner): Contains filepaths

        Returns:
            list: all sic traits
        """
        filepath_to_traits = f'{test_runner.full_path_to_mod}common\\country_leader\\KR_second_in_command_traits.txt'
        traits = []
        
        if lowercase:
            text_file = FileOpener.open_text_file(filepath_to_traits)
        else:
            text_file = FileOpener.open_text_file_non_lower(filepath_to_traits)

        pattern_matches = re.findall('((?<=\n)\t\w* = \{)', text_file)
        if len(pattern_matches) > 0:
            for match in pattern_matches:
                match = match[1:-4]
                traits.append(match)

        traits.append('second_in_command_trait')
        return traits
    
    @classmethod
    def get_all_political_traits(cls, test_runner, lowercase: bool) -> list[str]:
        """Parse common\country_leader\KR_political_advisor_traits.txt and return the list with all political traits

        Args:
            test_runner (test_runner): Contains filepaths

        Returns:
            list: all political traits
        """
        filepath_to_traits = f'{test_runner.full_path_to_mod}common\\country_leader\\KR_political_advisor_traits.txt'
        traits = []
        
        if lowercase:
            text_file = FileOpener.open_text_file(filepath_to_traits)
        else:
            text_file = FileOpener.open_text_file_non_lower(filepath_to_traits)

        pattern_matches = re.findall('((?<=\n)\t\w* = \{)', text_file)
        if len(pattern_matches) > 0:
            for match in pattern_matches:
                match = match[1:-4]
                traits.append(match)

        return traits
    
    @classmethod
    def get_all_military_traits(cls, test_runner, lowercase: bool) -> list[str]:
        """Parse common\country_leader\KR_military_advisor_traits.txt and return the list with all political traits

        Args:
            test_runner (test_runner): Contains filepaths

        Returns:
            list: all military traits
        """
        filepath_to_traits = f'{test_runner.full_path_to_mod}common\\country_leader\\KR_military_advisor_traits.txt'
        traits = []
        
        if lowercase:
            text_file = FileOpener.open_text_file(filepath_to_traits)
        else:
            text_file = FileOpener.open_text_file_non_lower(filepath_to_traits)

        pattern_matches = re.findall('((?<=\n)\t\w* = \{)', text_file)
        if len(pattern_matches) > 0:
            for match in pattern_matches:
                match = match[1:-4]
                traits.append(match)

        return traits
