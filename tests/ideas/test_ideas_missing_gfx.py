##########################
# Test script to check ideas with missing images
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re

from test_classes.generic_test_class import (
    FileOpener,
    ResultsReporter,
)
from test_classes.ideas_class import Ideas


def test_check_ideas_gfx(test_runner: object):
    gfx_path = f'{test_runner.full_path_to_mod}interface\\'
    gfx_entities = []
    results = []
    # Get the dict of all ideas
    ideas = Ideas.get_all_ideas(test_runner=test_runner, lowercase=False, include_hidden_ideas=False)

    # Get list of all image entities
    for filename in glob.iglob(gfx_path + '**/*.gfx', recursive=True):
        text_file = FileOpener.open_text_file(filename, lowercase=False)

        matches = re.findall('name = \\"GFX_idea_(.*)\\"', text_file)
        if len(matches) > 0:
            for match in matches:
                gfx_entities.append(match)

    # Check ideas and if they have proper pic defined
    for i in ideas:
        idea_token = re.findall('^([^ \\n]+) = \\{', i)[0].strip('\t')
        if "picture =" in i:
            idea_icon = re.findall('picture = ([^ \\n]+)', i)[0]
            if idea_icon not in gfx_entities:
                results.append(f"Idea {idea_token} - gfx passed to 'picture' doesn't exist")
        else:
            if idea_token not in gfx_entities:
                results.append(f"Idea {idea_token} - gfx_idea_token doesn't exist")

    ResultsReporter.report_results(results=results, message="Ideas that have image issues are detected. Check console output")
