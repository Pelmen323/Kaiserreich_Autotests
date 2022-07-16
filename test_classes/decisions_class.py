import glob
import logging
import os
import re

from ..test_classes.generic_test_class import FileOpener


class Decisions:
    @classmethod
    def get_all_decisions(cls, test_runner, lowercase: bool = True, return_paths: bool = False) -> list:
        """Parse all files in common/decisions and return the list with all decisions code

        Args:
            test_runner (_type_): test runner obj
            lowercase (bool, optional): defines if returned list contains lowercase str or not. Defaults to True.
            return_paths (bool, optional): defines if decisions code is returned with dict that contains their filenames. Defaults to False.

        Returns:
            if return_paths - tuple[list, dict]: list with decisions code and dict with decisions filenames
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
                text_file = FileOpener.open_text_file(filename, lowercase=False)

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
                text_file = FileOpener.open_text_file(filename, lowercase=False)

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
                text_file = FileOpener.open_text_file(filename, lowercase=False)

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


class DecisionsFactory:
    def __init__(self, dec: str) -> None:
        # Decision token
        try:
            self.token = re.findall('^\\t*(.+) = \\{', dec, flags=re.MULTILINE)[0]
        except AttributeError:
            self.token = None
            logging.error(f"Missing decision token, {dec}")

        try:
            self.icon = re.findall('icon = (.+)', dec)[0]
        except IndexError:
            self.icon = None
            logging.error(f"Missing decision icon, {self.token}")

        self.allowed = re.findall('(\\t+)allowed = \\{([^\\n]*|.*?^\\1)\\}', dec, flags=re.DOTALL | re.MULTILINE)[0][1] if '	allowed =' in dec else False
        self.available = re.findall('(\\t+)available = \\{([^\\n]*|.*?^\\1)\\}', dec, flags=re.DOTALL | re.MULTILINE)[0][1] if '	available =' in dec else False
        self.visible = re.findall('(\\t+)visible = \\{([^\\n]*|.*?^\\1)\\}', dec, flags=re.DOTALL | re.MULTILINE)[0][1] if '	visible =' in dec else False

        self.cancel_effect = re.findall('(\\t+)cancel_effect = \\{([^\\n]*|.*?^\\1)\\}', dec, flags=re.DOTALL | re.MULTILINE)[0][1] if 'cancel_effect =' in dec else False
        self.complete_effect = re.findall('(\\t+)complete_effect = \\{([^\\n]*|.*?^\\1)\\}', dec, flags=re.DOTALL | re.MULTILINE)[0][1] if 'complete_effect =' in dec else False
        self.remove_effect = re.findall('(\\t+)remove_effect = \\{([^\\n]*|.*?^\\1)\\}', dec, flags=re.DOTALL | re.MULTILINE)[0][1] if 'remove_effect =' in dec else False

        self.cancel_if_not_visible = "cancel_if_not_visible = yes" in dec
        self.cancel_trigger = re.findall('(\\t+)cancel_trigger = \\{([^\\n]*|.*?^\\1)\\}', dec, flags=re.DOTALL | re.MULTILINE)[0][1] if 'cancel_trigger =' in dec else False

        self.war_with_on_remove = "war_with_on_remove =" in dec
        self.war_with_target_on_remove = "war_with_target_on_remove = yes" in dec

        self.mission_subtype = "\tdays_mission_timeout =" in dec
        self.selectable_mission = "\tdays_mission_timeout =" in dec and "selectable_mission = yes" in dec
        self.has_ai_factor = "\tai_will_do =" in dec
