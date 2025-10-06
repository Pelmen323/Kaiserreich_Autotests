##########################
# Test script to check ideas with missing images
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re
from pathlib import Path

from test_classes.generic_test_class import (
    FileOpener,
    ResultsReporter,
)
from test_classes.ideas_class import Ideas


def test_check_ideas_gfx(test_runner: object):
    gfx_path = str(Path(test_runner.full_path_to_mod) / "interface") + "/"
    gfx_entities = []
    results = []
    ideas = Ideas.get_all_ideas(test_runner=test_runner, lowercase=False, include_hidden_ideas=False)

    # Get list of all idea image entities
    for filename in glob.iglob(gfx_path + "**/*.gfx", recursive=True):
        text_file = FileOpener.open_text_file(filename, lowercase=False)

        matches = re.findall(r"name = \"GFX_idea_(.*)\"", text_file)
        if len(matches) > 0:
            for match in matches:
                gfx_entities.append(match)

    # Check ideas and if they have proper pic defined
    for i in ideas:
        if "#fake" in i:
            continue
        idea_token = re.findall(r"^([^ \n]+) = \{", i)[0].strip("\t")
        if "picture =" in i:
            idea_icon = re.findall(r"picture = ([^ \n]+)", i)[0]
            if idea_icon not in gfx_entities:
                results.append(f"Idea {idea_token} - {idea_icon} gfx passed to 'picture' does not exist")
        else:
            if idea_token not in gfx_entities:
                results.append(f"Idea {idea_token} - idea doesn't have gfx defined")

    ResultsReporter.report_results(results=results, message="Ideas that have image issues are detected.")
