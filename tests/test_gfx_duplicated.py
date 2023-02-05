##########################
# Test script to check duplicated GFXs
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
from PIL import Image
import logging

from ..test_classes.generic_test_class import ResultsReporter
logging.getLogger('PIL').setLevel(logging.WARNING)                          # Counter PIL log pollution


def test_gfx_size(test_runner: object):
    filepath = f'{test_runner.full_path_to_mod}gfx\\'
    results = []
    images_list = []

    for filename in glob.iglob(filepath + '**/*.png', recursive=True):
        image_size = os.stat(filename).st_size
        images_list.append([filename, image_size])

    for name1, size1 in images_list:
        possible_duplicates = [i for i in images_list if size1 == i[1] and i[0] != name1]
        image1 = Image.open(name1)

        for name2, size2 in possible_duplicates:
            image2 = Image.open(name2)
            same_images = list(image1.getdata()) == list(image2.getdata())
            if same_images:
                path1 = os.path.basename(name1)
                path2 = os.path.basename(name2)
                if [path2, path1] not in results:
                    results.append([path1, path2])

    results = [f'{i} - images are duplicates' for i in results]

    ResultsReporter.report_results(results=results, message="Image duplicates were encountered.")
