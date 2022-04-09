import glob
import re
import os
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

            pattern_matches = re.findall('((?<=\n)country_event = \\{.*\n(.|\n*?)*\n\\})', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[0]
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
        filepath_to_events = f'{test_runner.full_path_to_mod}events\\'
        events = []

        for filename in glob.iglob(filepath_to_events + '**/*.txt', recursive=True):
            if '\\categories' in filename:
                continue
            if lowercase:
                text_file = FileOpener.open_text_file(filename)
            else:
                text_file = FileOpener.open_text_file(filename, lowercase=False)

            text_file_splitted = text_file.split('\n')[1:]
            for line in range(len(text_file_splitted)):
                current_line = text_file_splitted[line]
                pattern_matches = re.findall('^\\tid = [\\w+\\.*\\-*]+', current_line)
                if len(pattern_matches) > 0:
                    for match in pattern_matches:
                        match = match[6:].strip()
                        events.append(match)

        return events

    @classmethod
    def get_all_triggered_events_names(cls, test_runner, lowercase: bool = True) -> list:
        """Parse all files and return the list of all events that are directly triggered

        Args:
            test_runner (test_runner): Contains filepaths

        Returns:
            list: all events in mod folder that are triggered by something
        """
        filepath_global = test_runner.full_path_to_mod
        filepath_history = f'{test_runner.full_path_to_mod}history\\'
        events = []

        for filename in glob.iglob(filepath_global + '**/*.txt', recursive=True):
            if '\\history\\' in filename:
                continue
            if lowercase:
                text_file = FileOpener.open_text_file(filename)
            else:
                text_file = FileOpener.open_text_file(filename, lowercase=False)

            if "country_event =" in text_file:
                # 3.0 One-liners w/o brackets
                pattern_matches = re.findall('([\t| ]country_event = ((?!\\{).)*\n)', text_file)
                if len(pattern_matches) > 0:
                    for match in pattern_matches:
                        match = match[0]
                        match = match[16:].strip().strip('}').strip().strip('}').strip()
                        if '#' in match:
                            match = match[:match.index('#')].strip().strip('}').strip()    # Clean up comments
                        events.append(match)

                # 3.1 One-liners with brackets
                pattern_matches = re.findall('[\t| ]country_event = \\{.*\\}', text_file)
                if len(pattern_matches) > 0:
                    for match in pattern_matches:
                        event_id_match = re.findall('id = [a-zA-Z0-9\\._]*', match)
                        match = ''.join(event_id_match)[4:].strip()
                        events.append(match)

                # 3.2 Multiliners
                pattern_matches = re.findall('([\t| ]country_event = \\{((?!\\}).)*\n(.|\n*?)*\n\t*\\})', text_file)
                if len(pattern_matches) > 0:
                    for match in pattern_matches:
                        if '' in match:
                            match = match[0]                                            # Counter empty capture groups
                        event_id_match = re.findall('id = [a-zA-Z0-9\\._]*', match)
                        match = ''.join(event_id_match)[4:].strip()
                        events.append(match)

        for filename in glob.iglob(filepath_history + '**/*.txt', recursive=True):
            text_file = FileOpener.open_text_file(filename)

            if "country_event =" in text_file:
                # 4.0 One-liners w/o brackets
                pattern_matches = re.findall('(country_event = ((?!\\{).)*\n)', text_file)
                if len(pattern_matches) > 0:
                    for match in pattern_matches:
                        match = match[0]
                        match = match[16:].strip().strip('}').strip().strip('}').strip()
                        if '#' in match:
                            match = match[:match.index('#')].strip().strip('}').strip()    # Clean up comments
                        events.append(match)

                # 4.1 One-liners with brackets
                pattern_matches = re.findall('country_event = \\{.*\\}', text_file)
                if len(pattern_matches) > 0:
                    for match in pattern_matches:
                        event_id_match = re.findall('id = [a-zA-Z0-9\\._]*', match)
                        match = ''.join(event_id_match)[4:].strip()
                        events.append(match)

                # 4.2 Multiliners
                pattern_matches = re.findall('(country_event = \\{((?!\\}).)*\n(.|\n*?)*\n\t*\\})', text_file)
                if len(pattern_matches) > 0:
                    for match in pattern_matches:
                        if '' in match:
                            match = match[0]                                            # Counter empty capture groups
                        event_id_match = re.findall('id = [a-zA-Z0-9\\._]*', match)
                        match = ''.join(event_id_match)[4:].strip()
                        events.append(match)

        events = [i for i in events if '[' not in i and i != '']
        return events