##########################
# Test script to check unused GFXs
# By Pelmen, https://github.com/Pelmen323
##########################
import glob

from ..test_classes.generic_test_class import FileOpener, ResultsReporter


def test_gfx_unused(test_runner: object):
    filepath_gfx = f'{test_runner.full_path_to_mod}gfx\\'
    filepath_interface = f'{test_runner.full_path_to_mod}interface\\'
    filepath_characters = f'{test_runner.full_path_to_mod}common\\characters\\'
    filepath_db = f'{test_runner.full_path_to_mod}gfx\\interface\\equipmentdesigner\\'
    images_list = []

    for filename in glob.iglob(filepath_gfx + '**/*.png', recursive=True):
        images_list.append('gfx' + filename.split("gfx", maxsplit=1)[1].replace('\\', '/'))

    images_dict = {i: 0 for i in images_list}

    sources_list = [
        glob.iglob(filepath_interface + '**/*.gfx', recursive=True),
        glob.iglob(filepath_characters + '**/*.txt', recursive=True),
        glob.iglob(filepath_db + '**/*.txt', recursive=True)
    ]

    for source in sources_list:
        for filename in source:
            text_file = FileOpener.open_text_file(filename, lowercase=False)

            unused_images = [i for i in images_dict.keys() if images_dict[i] == 0]
            for image in unused_images:
                if image in text_file:
                    images_dict[image] += 1

    unused_images = [i for i in images_dict.keys() if images_dict[i] == 0]
    print(len(images_list))

    ResultsReporter.report_results(results=unused_images, message="Unused images were encountered.")
