import glob
import re
import os
from ..test_classes.generic_test_class import FileOpener


class Decisions:
    @classmethod
    def get_all_decisions_with_paths(cls, test_runner, lowercase: bool = True, return_paths: bool = False) -> list:
        """Parse all files in common/decisions and return the list with all decisions code

        Args:
            test_runner (_type_): test runner obj
            lowercase (bool, optional): defines if returned list contains lowercase str or not. Defaults to True.
            return_paths (bool, optional): defines if decisions code is returned with dict that contains their filenames. Defaults to False.

        Returns:
            if lowercase - tuple[list, dict]: list with decisions code and dict with decisions filenames
            else - list: list with decisions code
        """
        filepath_to_events = f'{test_runner.full_path_to_mod}common\\decisions\\'
        decisions = []
        paths = {}

        for filename in glob.iglob(filepath_to_events + '**/*.txt', recursive=True):
            if '\\categories' in filename:
                continue
            if lowercase:
                text_file = FileOpener.open_text_file(filename)
            else:
                text_file = FileOpener.open_text_file_non_lower(filename)

            pattern_matches = re.findall('((?<=\n)\\t\\w* = \\{.*\n(.|\n*?)*\n\\t\\})', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[0]
                    decisions.append(match)
                    paths[match] = os.path.basename(filename)

        if return_paths:
            return (decisions, paths)
        else:
            return decisions

    @classmethod
    def get_all_decisions_names(cls, test_runner, lowercase: bool = True) -> list:
        """Parse mod files and and return the list of all decisions names
        Args:
            test_runner (_type_): test runner obj
            lowercase (bool, optional): defines if returned list contains lowercase str or not. Defaults to True

        Returns:
            list:  all decisions names in mod folder
        """
        filepath_to_decisions = f'{test_runner.full_path_to_mod}common\\decisions\\'
        decisions = []

        for filename in glob.iglob(filepath_to_decisions + '**/*.txt', recursive=True):
            if '\\categories' in filename:
                continue
            if lowercase:
                text_file = FileOpener.open_text_file(filename)
            else:
                text_file = FileOpener.open_text_file_non_lower(filename)

            text_file_splitted = text_file.split('\n')[1:]
            for line in range(len(text_file_splitted)):
                current_line = text_file_splitted[line]
                pattern_matches = re.findall('^\\t[\\w+\\-*]+ =', current_line)
                if len(pattern_matches) > 0:
                    for match in pattern_matches:
                        match = match[:-1].strip('\t').strip()
                        decisions.append(match)

        return decisions

    @classmethod
    def get_all_activated_decisions_names(cls, test_runner, lowercase: bool = True) -> list:
        """Parse mod files and and return the list of all activated decisions names
        Args:
            test_runner (_type_): test runner obj
            lowercase (bool, optional): defines if returned list contains lowercase str or not. Defaults to True

        Returns:
            list:  all activated decisions names in mod folder
        """
        filepath = test_runner.full_path_to_mod
        decisions = []

        for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
            if lowercase:
                text_file = FileOpener.open_text_file(filename)
            else:
                text_file = FileOpener.open_text_file_non_lower(filename)

            if 'decision =' in text_file:
                text_file_splitted = text_file.split('\n')[1:]
                for line in range(len(text_file_splitted)):
                    current_line = text_file_splitted[line]
                    pattern_matches = re.findall('\\bdecision = [\\w+\\-*]+', current_line)
                    if len(pattern_matches) > 0:
                        for match in pattern_matches:
                            match = match[10:].strip()
                            decisions.append(match)
        return decisions
