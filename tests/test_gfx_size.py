##########################
# Test script to check GFX size. Pass relative filepath to gfx, target width and height and format of gfx
# By PPsyrius, refactored by Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
from PIL import Image
import pytest
import logging

from ..test_classes.generic_test_class import ResultsReporter

logging.getLogger('PIL').setLevel(logging.WARNING)                          # Counter PIL log pollution
input_list = [
    pytest.param({"filepath": "gfx\\interface\\terrains\\", "target_width": 413, "target_height": 70, "format": "png", "recursive": True}, id="Terrain GFX"),
    pytest.param({"filepath": "gfx\\leaders\\", "target_width": 156, "target_height": 210, "format": "png", "recursive": True}, id="Leaders GFX"),
    pytest.param({"filepath": "gfx\\event_news_pictures\\", "target_width": 397, "target_height": 153, "format": "png", "recursive": True}, id="News events GFX"),
    pytest.param({"filepath": "gfx\\flags\\", "target_width": 82, "target_height": 52, "format": "tga", "recursive": False}, id="Big flags GFX"),
    pytest.param({"filepath": "gfx\\flags\\medium\\", "target_width": 41, "target_height": 26, "format": "tga", "recursive": False}, id="Medium flags GFX"),
    pytest.param({"filepath": "gfx\\flags\\small\\", "target_width": 11, "target_height": 7, "format": "tga", "recursive": False}, id="Small flags GFX"),
]


@pytest.mark.parametrize("input_dict", input_list)
def test_gfx_size(test_runner: object, input_dict: dict):
    filepath = f'{test_runner.full_path_to_mod}{input_dict["filepath"]}'
    target_width = input_dict["target_width"]
    target_height = input_dict["target_height"]
    results = []
    glob_input = '**/*.' if input_dict["recursive"] is True else '*.'

    for filename in glob.iglob(filepath + glob_input + input_dict["format"], recursive=True):
        width, height = Image.open(filename).size
        if width != target_width:
            results.append(f"{os.path.basename(filename)} - Target width - {target_width}, actual width - {width}")
        if height != target_height:
            results.append(f"{os.path.basename(filename)} - Target height - {target_height}, actual height - {height}")

    ResultsReporter.report_results(results=results, message="Issues with image sizes were encountered.")
