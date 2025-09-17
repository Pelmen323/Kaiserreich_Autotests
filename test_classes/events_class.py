import glob
import os
import re
from pathlib import Path

from test_classes.generic_test_class import FileOpener


class Events:
    @classmethod
    def get_all_events(cls, test_runner, lowercase: bool = True, return_paths: bool = False, filepath_should_contain: str = "", filepath_should_not_contain: str = "") -> list[str]:
        """Parse all files in events and return the list with all events code

        Args:
            test_runner (_type_): test runner obj
            lowercase (bool, optional): defines if returned list contains lowercase str or not. Defaults to True.
            return_paths (bool, optional): defines if events code is returned with dict that contains their filenames. Defaults to False.

        Returns:
            if return_paths - tuple[list, dict]: list with events code and dict with events filenames
            else - list: list with events code
        """
        filepath_to_events = str(Path(test_runner.full_path_to_mod) / "events") + "/"
        pattern = re.compile(r"^country_event = \{(.*?)^\}", flags=re.DOTALL | re.MULTILINE)
        events = []
        paths = {}

        for filename in glob.iglob(filepath_to_events + "**/*.txt", recursive=True):
            if "categories" in filename:
                continue
            if filepath_should_contain not in filename:
                continue
            if filepath_should_not_contain != "":
                if filepath_should_not_contain in filename:
                    continue
            text_file = FileOpener.open_text_file(filename, lowercase=lowercase)

            pattern_matches = pattern.findall(text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    events.append(match)
                    paths[match] = os.path.basename(filename)

        assert len(events) != 0
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
        pattern = re.compile(r"^\tid = (\S+)", flags=re.MULTILINE)

        for event in events:
            pattern_matches = pattern.findall(event)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    events.append(match)

        assert len(events) != 0
        return sorted(set(events))

    @classmethod
    def get_all_triggered_events_names(cls, test_runner, lowercase: bool = True, return_duplicates: bool = False) -> list:
        """Parse all files and return the list of all events that are directly triggered

        Args:
            test_runner (test_runner): Contains filepaths

        Returns:
            list: all events in mod folder that are triggered by something
        """
        filepath_global = test_runner.full_path_to_mod
        pattern_one_liner = re.compile(r"country_event = ([^\s\{]+)", flags=re.MULTILINE)
        pattern_one_liner_w_brackets = re.compile(r"country_event = \{ .*id = (\S+).*\}", flags=re.MULTILINE)
        pattern_multi_liner = re.compile(r"^(\t+)country_event = \{([^\}]*?)\1\}", flags=re.DOTALL | re.MULTILINE)
        pattern_id = re.compile(r"id = (\S+)")
        events = []

        for filename in glob.iglob(filepath_global + "**/*.txt", recursive=True):
            text_file = FileOpener.open_text_file(filename, lowercase=lowercase)

            if "country_event = {" in text_file:
                # 3.1 One-liners with brackets
                pattern_matches = pattern_one_liner_w_brackets.findall(text_file)
                if len(pattern_matches) > 0:
                    for match in pattern_matches:
                        events.append(match)

                # 3.2 Multiliners
                pattern_matches = pattern_multi_liner.findall(text_file)
                if len(pattern_matches) > 0:
                    for match in pattern_matches:
                        event_id_match = pattern_id.findall(match[1])
                        events.append(event_id_match[0])

            # 3.0 One-liners w/o brackets
            if "country_event =" in text_file:
                pattern_matches = pattern_one_liner.findall(text_file)
                if len(pattern_matches) > 0:
                    for match in pattern_matches:
                        events.append(match)

        assert len(events) != 0
        if return_duplicates:
            return sorted(events)
        return sorted(set(events))
