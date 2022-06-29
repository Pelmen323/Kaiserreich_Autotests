import glob
import os
import re

from ..test_classes.generic_test_class import FileOpener


class Events:
    @classmethod
    def get_all_events(cls, test_runner, lowercase: bool = True, return_paths: bool = False) -> list:
        """Parse all files in events and return the list with all events code

        Args:
            test_runner (_type_): test runner obj
            lowercase (bool, optional): defines if returned list contains lowercase str or not. Defaults to True.
            return_paths (bool, optional): defines if events code is returned with dict that contains their filenames. Defaults to False.

        Returns:
            if return_paths - tuple[list, dict]: list with events code and dict with events filenames
            else - list: list with events code
        """
        filepath_to_events = f'{test_runner.full_path_to_mod}events\\'
        events = []
        paths = {}

        for filename in glob.iglob(filepath_to_events + '**/*.txt', recursive=True):
            if '\\categories' in filename:
                continue
            if lowercase:
                text_file = FileOpener.open_text_file(filename)
            else:
                text_file = FileOpener.open_text_file(filename, lowercase=False)

            pattern_matches = re.findall('^country_event = \\{(.*?)^\\}', text_file, flags=re.DOTALL | re.MULTILINE)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    events.append(match)
                    paths[match] = os.path.basename(filename)

        if return_paths:
            return (events, paths)
        else:
            return events

    @classmethod
    def get_all_events_names(cls, test_runner, lowercase: bool = True) -> list:
        """Parse events file and return the list of all events

        Args:
            test_runner (test_runner): Contains filepaths

        Returns:
            list: all events in mod folder
        """
        events = Events.get_all_events(test_runner=test_runner, lowercase=lowercase)

        for event in events:
            pattern_matches = re.findall('^\\tid = ([^ \\n\\t]+)', event, flags=re.MULTILINE)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    events.append(match)

        return sorted(set(events))

    @classmethod
    def get_all_triggered_events_names(cls, test_runner, lowercase: bool = True) -> list:
        """Parse all files and return the list of all events that are directly triggered

        Args:
            test_runner (test_runner): Contains filepaths

        Returns:
            list: all events in mod folder that are triggered by something
        """
        filepath_global = test_runner.full_path_to_mod
        events = []

        for filename in glob.iglob(filepath_global + '**/*.txt', recursive=True):
            if lowercase:
                text_file = FileOpener.open_text_file(filename)
            else:
                text_file = FileOpener.open_text_file(filename, lowercase=False)

            if "country_event =" in text_file:
                # 3.0 One-liners w/o brackets
                pattern_matches = re.findall('country_event = ([^ \\{\\n\\t]+)', text_file, flags=re.MULTILINE)
                if len(pattern_matches) > 0:
                    for match in pattern_matches:
                        events.append(match)

                # 3.1 One-liners with brackets
                pattern_matches = re.findall('country_event = \\{ .*id = ([^ \\n\\t]+).*\\}', text_file, flags=re.MULTILINE)
                if len(pattern_matches) > 0:
                    for match in pattern_matches:
                        events.append(match)

                # 3.2 Multiliners
                pattern_matches = re.findall('^(\\t+)country_event = \\{([^\\}]*?)\\1\\}', text_file, flags=re.DOTALL | re.MULTILINE)
                if len(pattern_matches) > 0:
                    for match in pattern_matches:
                        event_id_match = re.findall('id = ([^ \\n\\t]+)', match[1])
                        events.append(event_id_match[0])

        return sorted(set(events))
