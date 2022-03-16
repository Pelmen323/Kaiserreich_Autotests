import glob
import re
from ..test_classes.generic_test_class import FileOpener, DataCleaner, ResultsReporter


class Decisions:
    @classmethod
    def get_all_decisions_names(cls, test_runner, lowercase: bool) -> list:
        """Parse decisions file and and return the list of all decisions

        Args:
            test_runner (test_runner): Contains filepaths

        Returns:
            list: all decisions in mod folder
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
    def get_all_activated_decisions_names(cls, test_runner, lowercase: bool) -> list:
        """Parse mod files and and return the list of all activated decisions

        Args:
            test_runner (test_runner): Contains filepaths

        Returns:
            list: all activated decisions in mod folder
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
