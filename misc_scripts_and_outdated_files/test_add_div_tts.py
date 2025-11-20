##########################
# Test script to parse division templates
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
import re
from collections import Counter
from pathlib import Path
from charset_normalizer import detect

from test_classes.generic_test_class import FileOpener, ResultsReporter

def detect_encoding(filename):
    with open(filename, 'rb') as f:
        raw_data = f.read()
        return detect(raw_data)['encoding']

# TODO - Add duplicated recon check
class RegimentsSection:
    def __init__(self, text_line: str, is_support_section=False) -> None:
        try:
            if is_support_section:
                self.regiments_section = re.findall("^(\\t*?)support = \\{.*?\\n(.*?)\\n^\\1\\}", text_line, flags=re.DOTALL | re.MULTILINE)[0][1].split('\n')
            else:
                self.regiments_section = re.findall("^(\\t*?)regiments = \\{.*?\\n(.*?)\\n^\\1\\}", text_line, flags=re.DOTALL | re.MULTILINE)[0][1].split('\n')
            self.regiments_list = []

            for i in self.regiments_section:
                if len(i) > 4:
                    self.regiments_list.append(Regiment(i))

            self.regiments_coodrs_list = [(i.x, i.y) for i in self.regiments_list]
        except Exception:
            print(text_line)
            raise


class Regiment:
    def __init__(self, text_line: str):
        self.battalion_type = re.findall("\t([^\t]*?) = \\{", text_line)[0]
        self.x = int(re.findall(" x = (.)", text_line)[0])
        self.y = int(re.findall(" y = (.)", text_line)[0])


def test_division_composition_parser(test_runner: object):
    filepath = str(Path(test_runner.full_path_to_mod) / "common" / "decisions") + "/"
    #filepath = test_runner.full_path_to_mod
    #lst = ["ASY", "BRA", "BUL", "CAN", "CYP", "DOM", "ETH", "JBS", "KUR", "LBA", "PRU", "SER", "SYR", "XSM"]

    for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
        # if any([i for i in lst if i in filename]) is True:
        #     continue
        text_file = FileOpener.open_text_file(filename, lowercase=False)

        if "division_template = {" in text_file:
            text_file_new = text_file
            pattern_matches = re.findall(r"^((\t*?)division_template = (\{.*?^\2\}))", text_file, flags=re.DOTALL | re.MULTILINE)
            if len(pattern_matches) > 0:
                #file_encoding = detect_encoding(filename)
                for match in pattern_matches:
                    whole_match = match[0]
                    t = match[1]
                    match = match[2]
                    division_name = re.findall('name = "(.*)"', match)[0]
                    initial_tt_part = t + 'custom_effect_tooltip = {\n' + t + '\tlocalization_key = tooltip_create_division_template\n' + t + '\tNAME = "' + division_name + '"\n'
                    tooltip_parts = []
                    tooltip_parts.append(initial_tt_part)

                    # 1. Check the regiments section
                    if "regiments = {" in match:
                        r = RegimentsSection(match)
                        list_of_battalions = [i.battalion_type for i in r.regiments_list]
                        counter_obj = Counter(list_of_battalions)
                        i = 0
                        for key, value in counter_obj.items():
                            i += 1
                            tooltip_parts.append(t+'\t'+'LINE_'+str(i)+' = {' + f' localization_key = line_battalion_tt NAME = {key} ICON = GFX_unit_{key}_icon_small COUNT = {value} ' + '}\n')

                    if "support = {" in match:
                        r = RegimentsSection(match, is_support_section=True)
                        list_of_battalions = [i.battalion_type for i in r.regiments_list]
                        counter_obj = Counter(list_of_battalions)
                        i = 0
                        for key, value in counter_obj.items():
                            i += 1
                            tooltip_parts.append(t+'\t'+'SUPPORT_'+str(i)+' = {' + f' localization_key = support_battalion_tt NAME = {key} ICON = GFX_unit_{key}_icon_small ' + '}\n')

                    assembled_tt = ''.join(tooltip_parts) + t + '}'
                    if whole_match + '\n' + assembled_tt not in text_file_new:
                        override = True
                        text_file_new = text_file_new.replace(whole_match,  whole_match + '\n' + assembled_tt)

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
