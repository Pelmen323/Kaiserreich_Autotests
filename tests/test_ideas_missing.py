##########################
# Test script to check if there are opinion modifiers that are not used via "modifier = xx"
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
import re
from ..test_classes.generic_test_class import FileOpener, DataCleaner, ResultsReporter
from ..test_classes.ideas_class import Ideas
FILES_TO_SKIP = ["00 Generic ideas.txt", '01 Army Spirits.txt', '01 Air Spirits.txt', '01 Navy Spirits.txt']
FALSE_POSITIVES = ('hai_foreign_control_dummy', 'empowered_trade_unions_sic', 'empowered_executive_sic', 'empowered_legislative_sic')


def test_check_ideas_missing(test_runner: object):
    filepath = test_runner.full_path_to_mod
    paths = {}
    # 1. Get list of all ideas
    defined_ideas = Ideas.get_all_ideas_names(test_runner=test_runner, lowercase=True, return_paths=False, include_country_ideas=True, include_manufacturers=True, include_characters_tokens=True, include_laws=True, include_army_spirits=True)

    # 2. Get dict of ideas usages:
    used_ideas = []
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if 'add_ideas =' in text_file:
            pattern_matches = re.findall("add_ideas = ([\\w':-]+)", text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    used_ideas.append(match)
                    paths[match] = os.path.basename(filename)

        if 'remove_ideas =' in text_file:
            pattern_matches = re.findall("remove_ideas = ([\\w':-]+)", text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    used_ideas.append(match)
                    paths[match] = os.path.basename(filename)

        if 'has_idea =' in text_file:
            pattern_matches = re.findall("has_idea = ([\\w':-]+)", text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    used_ideas.append(match)
                    paths[match] = os.path.basename(filename)

        # if 'idea =' in text_file:
        #     pattern_matches = re.findall('idea = (\\w+)', text_file)
        #     if len(pattern_matches) > 0:
        #         for match in pattern_matches:
        #             match = match[0]
        #             used_ideas.append(match)
        #             paths[match] = os.path.basename(filename)

        # if 'add_ideas = {' in text_file:
        #     pattern_matches = re.findall('((?<=\n)[ |\t]*add_ideas = \\{.*\n(.|\n*?)*\n\\})', text_file)
        #     if len(pattern_matches) > 0:
        #         for match in pattern_matches:
        #             match = match[0].split('\n')
        #             for line in match:
        #                 if '}' not in line and '{' not in line:
        #                     line = line.strip('\t').strip()
        #                     match = line
        #                     used_ideas.append(match)
        #                     paths[match] = os.path.basename(filename)

    # 3. Report the results:
    results = [i for i in used_ideas if i not in defined_ideas and "var:" not in i]
    ResultsReporter.report_results(results=results, paths=paths, message="Unused ideas were encountered. Check console output")
