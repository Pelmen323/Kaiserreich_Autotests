##########################
# Test script to parse division templates
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re
from pathlib import Path

from test_classes.generic_test_class import FileOpener

invalid_targets = [
    'can_annex',
    'AI_dont_annex',
    'CHN_can_annex_fareast',
    'controls_rhine_east_bank',
    'controls_rhine_west_bank',
    'has_french_ally',
    'has_italian_ally',
    'owns_persian_kurdistan',
    'owns_turkish_kurdistan',
    'wants_to_release_lebanon'
]


def test_division_composition_parser(test_runner: object):
    filepath = str(Path(test_runner.full_path_to_mod) / "events") + "/"

    for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
        if "Annexation" in filename and "events 0" not in filename:
            text_file = FileOpener.open_text_file(filename, lowercase=False)
            text_file_new = text_file
            override = False
            immediate_blocks = re.findall(r'\timmediate = \{.*?^\t\}', text_file, flags=re.MULTILINE | re.DOTALL)
            for b in immediate_blocks:
                immediate_block_override = b
                if "save_event_target_as" in b:
                    save_targets = re.findall(r'save_event_target_as = ([^\s\t]+)', b)
                    for save_target in set(save_targets):
                        if "can_offer_" not in save_target and not any([i for i in invalid_targets if i == save_target]):
                            override = True
                            ptn = r'save_event_target_as = ' + save_target + r'\b'
                            immediate_block_override = re.sub(ptn, 'save_event_target_as = ' + save_target + ' add_to_array = { ROOT.potential_grant_targets = THIS }', immediate_block_override)

                if override:
                    text_file_new = text_file_new.replace(b, immediate_block_override)

            if override:
                with open(filename, 'w', encoding='utf-8') as text_file_write:
                    text_file_write.write(text_file_new)
