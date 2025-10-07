import glob
import os
import re

from test_classes.generic_test_class import FileOpener


class Event_Targets:
    @classmethod
    def get_all_used_targets(cls, test_runner, lowercase: bool = True, return_paths: bool = False) -> list[str]:
        """Parse all files return the list with all vars
        Args:
            test_runner (_type_): test runner obj
            lowercase (bool, optional): defines if returned list contains lowercase str or not. Defaults to True.
            return_paths (bool, optional): defines if vars code is returned with dict that contains their filenames. Defaults to False.

        Returns:
            if return_paths - tuple[list, dict]: list with vars and dict with filenames
            else - list: list with vars code
        """
        filepath = test_runner.full_path_to_mod
        targets = []
        paths = {}

        for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
            text_file = FileOpener.open_text_file(filename, lowercase=lowercase)
            if "tag_aliases" in filename:
                if 'global_event_target =' in text_file:
                    pattern_matches = re.findall(r'global_event_target = ([^ \n\t\#"]*)', text_file)
                    if len(pattern_matches) > 0:
                        for match in pattern_matches:
                            targets.append(match)
                            paths[match] = os.path.basename(filename)
            else:
                if 'event_target:' in text_file:
                    pattern_matches = re.findall(r'event_target:([^ \n\t\#"]*)', text_file)
                    if len(pattern_matches) > 0:
                        for match in pattern_matches:
                            targets.append(match)
                            paths[match] = os.path.basename(filename)

                if 'has_event_target =' in text_file:
                    pattern_matches = re.findall(r'has_event_target = ([^ \n\t"]*)', text_file)
                    if len(pattern_matches) > 0:
                        for match in pattern_matches:
                            targets.append(match)
                            paths[match] = os.path.basename(filename)

        if return_paths:
            return (targets, paths)
        else:
            return targets

    @classmethod
    def get_all_set_targets(cls, test_runner, lowercase: bool = True, return_paths: bool = False) -> list[str]:
        """Parse all files return the list with all vars
        Args:
            test_runner (_type_): test runner obj
            lowercase (bool, optional): defines if returned list contains lowercase str or not. Defaults to True.
            return_paths (bool, optional): defines if code is returned with dict that contains their filenames. Defaults to False.

        Returns:
            if return_paths - tuple[list, dict]: list with vars and dict with filenames
            else - list: list with vars code
        """
        filepath = test_runner.full_path_to_mod
        targets = []
        paths = {}

        for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
            if "tag_aliases" in filename:
                continue
            text_file = FileOpener.open_text_file(filename, lowercase=lowercase)

            if 'save_global_event_target_as =' in text_file:
                pattern_matches = re.findall(r'save_global_event_target_as = ([^ \n\t\#"]*)', text_file)
                if len(pattern_matches) > 0:
                    for match in pattern_matches:
                        targets.append(match)
                        paths[match] = os.path.basename(filename)

            if 'save_event_target_as =' in text_file:
                pattern_matches = re.findall(r'save_event_target_as = ([^ \n\t\#"]*)', text_file)
                if len(pattern_matches) > 0:
                    for match in pattern_matches:
                        targets.append(match)
                        paths[match] = os.path.basename(filename)

        if return_paths:
            return (targets, paths)
        else:
            return targets

    @classmethod
    def get_all_cleared_targets(cls, test_runner, lowercase: bool = True, flag_type: str = "country", return_paths: bool = False) -> list[str]:
        """Parse all files return the list with all vars
        Args:
            test_runner (_type_): test runner obj
            lowercase (bool, optional): defines if returned list contains lowercase str or not. Defaults to True.
            return_paths (bool, optional): defines if vars code is returned with dict that contains their filenames. Defaults to False.

        Returns:
            if return_paths - tuple[list, dict]: list with vars and dict with filenames
            else - list: list with vars code
        """
        filepath = test_runner.full_path_to_mod
        targets = []
        paths = {}

        for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
            text_file = FileOpener.open_text_file(filename, lowercase=lowercase)

            if 'clear_global_event_target =' in text_file:
                pattern_matches = re.findall(r'clear_global_event_target = ([^ \n\t\#"]*)', text_file)
                if len(pattern_matches) > 0:
                    for match in pattern_matches:
                        targets.append(match)
                        paths[match] = os.path.basename(filename)

        if return_paths:
            return (targets, paths)
        else:
            return targets
