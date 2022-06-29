##########################
# Test script to check if 'limit' is not used in if/elif conditions
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
import re

from ..test_classes.generic_test_class import (
    DataCleaner,
    FileOpener,
    ResultsReporter,
)

FILES_TO_SKIP = ['\\history\\', '\\tanks\\', '_rename_scripted_effects.txt', '00_renaming_toggle.txt', 'MAF effects']
re.DOTALL


def test_check_syntax_limits(test_runner: object):
    filepath = test_runner.full_path_to_mod
    results = {}
    container = {}
    os.chdir(filepath)

    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        if DataCleaner.skip_files(files_to_skip=FILES_TO_SKIP, filename=filename):
            continue
        text_file = FileOpener.open_text_file(filename)

        if_count = re.findall('(\\bif = \\{.*\n(.|\n*?)*\n\t+\\})', text_file)
        if len(if_count) > 0:
            for match in if_count:
                match = match[0]                                            # Counter empty capture groups
                container[match] = os.path.basename(filename)

        else_if_count = re.findall('(\\belse_if = \\{.*\n(.|\n*?)*\n\t+\\})', text_file)
        if len(else_if_count) > 0:
            for match in else_if_count:
                match = match[0]                                            # Counter empty capture groups
                container[match] = os.path.basename(filename)

        every_state_count = re.findall('(\\bevery_state = \\{.*\n(.|\n*?)*\n\t+\\})', text_file)
        if len(every_state_count) > 0:
            for match in every_state_count:
                match = match[0]                                            # Counter empty capture groups
                container[match] = os.path.basename(filename)

        every_country_count = re.findall('(\\bevery_country = \\{.*\n(.|\n*?)*\n\t+\\})', text_file)
        if len(every_country_count) > 0:
            for match in every_country_count:
                match = match[0]                                            # Counter empty capture groups
                if 'reverse_add_opinion_modifier' in match:
                    continue
                if '#unit limits setup' in match:
                    continue
                if 'former_reichspakt_member' in match:
                    continue
                container[match] = os.path.basename(filename)

        every_other_country_count = re.findall('(\\bevery_other_country = \\{.*\n(.|\n*?)*\n\t+\\})', text_file)
        if len(every_country_count) > 0:
            for match in every_other_country_count:
                match = match[0]                                            # Counter empty capture groups
                if 'kr_similar_ideology_close' in match:
                    continue
                if 'ai_events.100' in match:
                    continue
                if 'ai_events.101' in match:
                    continue
                container[match] = os.path.basename(filename)

    for effect in container.keys():
        if 'limit = {' not in effect:
            results[effect] = container[effect]

    ResultsReporter.report_results(results=results, message="Issues with ifs/elifs limit syntax were encountered. Check console output")
