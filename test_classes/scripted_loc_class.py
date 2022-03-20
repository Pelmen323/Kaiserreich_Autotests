import glob
import re
import os
from ..test_classes.generic_test_class import FileOpener, DataCleaner, ResultsReporter


class Scripted_localisation:
    @classmethod
    def get_scripted_loc_names_with_paths(cls, test_runner, lowercase: bool) -> list:
        """Parse scripted loc files and and return the list of all scripted loc

        Args:
            test_runner (test_runner): Contains filepaths

        Returns:
            list: all scripted loc names in mod folder
        """
        filepath_to_decisions = f'{test_runner.full_path_to_mod}common\\scripted_localisation\\'
        container = []
        paths = {}
        for filename in glob.iglob(filepath_to_decisions + '**/*.txt', recursive=True):
            if lowercase:
                text_file = FileOpener.open_text_file(filename)
            else:
                text_file = FileOpener.open_text_file_non_lower(filename)

            text_file_splitted = text_file.split('\n')[1:]
            for line in range(len(text_file_splitted)):
                current_line = text_file_splitted[line]
                pattern_matches = re.findall('^\\tname = (\w*)', current_line)
                if len(pattern_matches) > 0:
                    for match in pattern_matches:
                        container.append(match)
                        paths[match] = os.path.basename(filename)

        return (container, paths)
