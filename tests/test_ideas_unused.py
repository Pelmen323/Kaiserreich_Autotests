##########################
# Test script to check if there are opinion modifiers that are not used via "modifier = xx"
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re

from ..test_classes.generic_test_class import (
    DataCleaner,
    FileOpener,
    ResultsReporter,
)
from ..test_classes.ideas_class import Ideas

FILES_TO_SKIP = ["00 Generic ideas.txt", '01 Army Spirits.txt', '01 Air Spirits.txt', '01 Navy Spirits.txt']
FALSE_POSITIVES = ('hai_foreign_control_dummy', 'maf_colonial_budget_idea_dummy',)


def test_check_ideas_unused(test_runner: object):
    filepath = test_runner.full_path_to_mod
    results_dict = {}
    paths = {}
    # 1. Get the dict of all ideas
    ideas, paths = Ideas.get_all_ideas_names(test_runner=test_runner, lowercase=True, return_paths=True, include_country_ideas=True, include_manufacturers=False, include_characters_tokens=False)
    for i in ideas:
        if paths[i] in FILES_TO_SKIP:
            continue
        results_dict[i] = 0

    # 2. Find if ideas are used:
    results_dict = DataCleaner.clear_false_positives(input_iter=results_dict, false_positives=FALSE_POSITIVES)
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        not_encountered_dict = [i for i in results_dict.keys() if results_dict[i] == 0]
        if 'add_ideas =' in text_file:
            for key in not_encountered_dict:
                if f'add_ideas = {key}' in text_file:
                    results_dict[key] += 1

        if 'idea =' in text_file:
            for key in not_encountered_dict:
                if f'idea = {key}' in text_file:
                    results_dict[key] += 1

        if 'token:' in text_file:
            for key in not_encountered_dict:
                if f'token:{key}' in text_file:
                    results_dict[key] += 1

        if 'add_ideas = {' in text_file:
            pattern_matches = re.findall('((?<=\n)[ |\t]*add_ideas = \\{.*\n(.|\n*?)*\n\\})', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[0].split('\n')
                    for line in match:
                        if '}' not in line and '{' not in line:
                            line = line.strip('\t').strip()
                            for key in not_encountered_dict:
                                if key == line:
                                    results_dict[key] += 1

    # 3. Report the results:
    results = [i for i in results_dict.keys() if results_dict[i] == 0]
    ResultsReporter.report_results(results=results, paths=paths, message="Unused ideas were encountered. Check console output")
