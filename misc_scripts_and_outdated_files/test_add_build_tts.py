##########################
# Test script to parse division templates
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re
from charset_normalizer import detect

from test_classes.generic_test_class import FileOpener


def detect_encoding(filename):
    with open(filename, "rb") as f:
        raw_data = f.read()
        return detect(raw_data)["encoding"]


def test_division_composition_parser(test_runner: object):
    filepath = test_runner.full_path_to_mod

    for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
        # if any([i for i in lst if i in filename]) is True:
        #     continue
        text_file = FileOpener.open_text_file(filename, lowercase=False)

        if "add_building_construction = {" in text_file:
            text_file_new = text_file
            pattern_matches = re.findall(r"^((\t*?)add_building_construction = (\{.*?^\2\}))", text_file, flags=re.DOTALL | re.MULTILINE)
            if len(pattern_matches) > 0:
                file_encoding = detect_encoding(filename)
                for match in pattern_matches:
                    if "all_provinces" in match[0]:
                        whole_match = match[0]
                        t = match[1]
                        match = match[2]
                        building = re.findall(r"type = ([^\t\n]*)", match)[0]
                        level = re.findall(r"level = ([^\t\n]*)", match)[0]
                        limit_to_border = "limit_to_border = yes" in match
                        limit_to_border_country = '"[?' + re.findall(r'limit_to_border_country = (...)', match)[0] + '.GetTag]"' if "limit_to_border_country" in match else False
                        limit_to_coastal = "limit_to_coastal = yes" in match
                        limit_to_naval_base = "limit_to_naval_base = yes" in match
                        limit_to_victory_points = "limit_to_victory_point > 0" in match or "limit_to_victory_point = yes" in match
                        limit_to_victory_points_above = re.findall(r"limit_to_victory_point > (\d*)", match)[0] if "limit_to_victory_point >" in match and not limit_to_victory_points else False
                        loc_key_map = {
                            limit_to_border: "tooltip_add_building_on_border_provinces",
                            limit_to_border_country: "tooltip_add_building_on_border_provinces_with_tag",
                            limit_to_coastal: "tooltip_add_building_on_coastal_provinces",
                            limit_to_naval_base: "tooltip_add_building_on_naval_base",
                            limit_to_victory_points: "tooltip_add_building_on_victory_points",
                            limit_to_victory_points_above: "tooltip_add_building_on_victory_points_above_value",
                        }

                        m = False
                        for i in loc_key_map:
                            if i:
                                m = True
                                localisation_key = loc_key_map[i]

                        if not m:
                            localisation_key = "tooltip_add_building_on_all_provinces\t\t\t\t# TODO - validate if adding buildings to all provinces in expected"

                        # One additional tab compared to extracted code
                        tooltip = t + '\t' + 'tooltip = {\n'
                        tooltip_loc_key = t + '\t\t' + 'localization_key = ' + localisation_key + '\n'
                        tooltip_building = t + '\t\t' + 'BUILDING = ' + building + '\n'
                        tooltip_number = t + '\t\t' + 'NUMBER = ' + level + '\n'
                        tooltip_border_country = t + '\t\t' + 'TAG = ' + limit_to_border_country + '\n' if limit_to_border_country else ''
                        tooltip_value = t + '\t\t' + 'VALUE = ' + limit_to_victory_points_above + '\n' if limit_to_victory_points_above else ''
                        tooltip_value = t + '\t\t' + 'VALUE = ' + limit_to_victory_points_above + '\n' if limit_to_victory_points_above else ''
                        tooltip_end = t + '\t' + '}'

                        assembled_tooltip = tooltip + tooltip_loc_key + tooltip_building + tooltip_number + tooltip_border_country + tooltip_value + tooltip_end

                        match_with_added_tab = ''.join(['\t' + i + '\n' for i in whole_match.split('\n')])

                        assembled_override = t + 'custom_override_tooltip = {\n' + match_with_added_tab + assembled_tooltip + '\n' + t + '}'

                        text_file_new = text_file_new.replace(whole_match, assembled_override)
                        with open(filename, "w", encoding=file_encoding) as text_file_write:
                            text_file_write.write(text_file_new)
