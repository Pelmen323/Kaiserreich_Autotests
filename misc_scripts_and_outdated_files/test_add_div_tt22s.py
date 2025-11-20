##########################
# Test script to parse division templates
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
import re
from collections import Counter
from pathlib import Path

from test_classes.generic_test_class import FileOpener, ResultsReporter


def test_division_composition_parser(test_runner: object):
    filepath = str(Path(test_runner.full_path_to_mod) / "history" / "countries") + "/"

    for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
        text_file = FileOpener.open_text_file(filename, lowercase=False)
        text_file_new = text_file_new.replace('### Navy - Non MtG ###\n', '')
        text_file_new = text_file_new.replace('### Navy - non MtG ###\n', '')

        # if "has_dlc_mtg = no" in text_file:
        #     text_file_new = text_file
        #     pattern_matches = re.findall(r"^(if = \{\n\tlimit = \{ has_dlc_mtg = no \}.*?^\})", text_file, flags=re.DOTALL | re.MULTILINE)
        #     if len(pattern_matches) > 0:
        #         override = True
        #         for match in pattern_matches:
        #             text_file_new = text_file_new.replace(match, '')
        #             text_file_new = text_file_new.replace('### Navy - Non MtG ###\n', '')
        #             text_file_new = text_file_new.replace('### Navy - non MtG ###\n', '')


        # if "has_dlc_mtg = yes" in text_file:
        #     text_file_new = text_file
        #     master_set_technology = re.findall(r"^set_technology = \{.*?\}", text_file, flags=re.DOTALL | re.MULTILINE)[0]
        #     pattern_matches = re.findall(r"^(if = \{\n\tlimit = \{ has_dlc_mtg = yes \}.*?^\})", text_file, flags=re.DOTALL | re.MULTILINE)
        #     if len(pattern_matches) > 0:
        #         for match in pattern_matches:
        #             if 'set_technology' in match:
        #                 override = True
        #                 tech_block = re.findall(r"^\tset_technology = \{(.*?)\}", match, flags=re.DOTALL | re.MULTILINE)[0]
        #                 updated_master_set_technology = master_set_technology.replace('}', '\n\t### Navy ###\n' + tech_block.strip('\t').replace('\t\t', '\t') + '}')
        #                 text_file_new = text_file_new.replace(master_set_technology, updated_master_set_technology)
        #                 text_file_new = text_file_new.replace(match, '')
        #                 text_file_new = text_file_new.replace('### Navy - MtG ###\n', '')
        #             else:
        #                 print(match)
        #                 raise

            if override:
                with open(filename, 'w', encoding='utf-8') as text_file_write:
                    text_file_write.write(text_file_new)


    #                 # 2. Check the support section
    #                 if "support = {" in match:
    #                     support_section = RegimentsSection(match, filepath, filepath_to_vanilla, is_support_section=True)

    #                     if x := len([i for i in support_section.regiments_coodrs_list if support_section.regiments_coodrs_list.count(i) > 1]) > 0:
    #                         results.append((os.path.basename(filename), f'{division_name} - duplicated support company coords'))

    #                     for i in support_section.regiments_coodrs_list:
    #                         x = i[0]
    #                         y = i[1]

    #                         # 2.1 Check if company is defined not in the 1st column
    #                         if x != 0:
    #                             results.append((os.path.basename(filename), f'{division_name} - Invalid support company coordinates {x, y}'))

    #                         # 2.2 Check y axis (row)
    #                         elif y != 0:
    #                             for i2 in range(0, y):
    #                                 if (x, i2) not in support_section.regiments_coodrs_list:
    #                                     results.append((os.path.basename(filename), f'{division_name} - Support company {x, i2} is missing'))

    #                     if len([i for i in support_section.regiments_list if "recon" in i.battalion_type]) > 1:
    #                         results.append((os.path.basename(filename), f'{division_name} - Division template has multiple recon companies assigned'))

    # ResultsReporter.report_results(results=results, message="Division templates with violations were encountered.")
