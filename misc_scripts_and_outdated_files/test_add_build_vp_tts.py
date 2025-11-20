##########################
# Test script to parse division templates
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re
from charset_normalizer import detect

from test_classes.generic_test_class import FileOpener
from test_classes.states_class import States


def detect_encoding(filename):
    with open(filename, "rb") as f:
        raw_data = f.read()
        return detect(raw_data)["encoding"]


def test_division_composition_parser(test_runner: object):
    filepath = test_runner.full_path_to_mod
    vps_dict = States.get_states_vps_dict(test_runner)
    all_vps = []
    for i in vps_dict:
        all_vps.extend(vps_dict[i])

    for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
        # if any([i for i in lst if i in filename]) is True:
        #     continue
        text_file = FileOpener.open_text_file(filename, lowercase=False)

        if "add_building_construction = {" in text_file:
            text_file_new = text_file

            ### Multiline
            pattern_matches = re.findall(r"^((\t*?)add_building_construction = (\{[^}\n]*\n.*?^\2\}))", text_file, flags=re.DOTALL | re.MULTILINE)
            pattern_matches.extend(re.findall(r"((\t*?)add_building_construction = (\{.*?\}))", text_file))
            if len(pattern_matches) > 0:
                file_encoding = detect_encoding(filename)
                for match in pattern_matches:
                    if "province =" in match[0]:
                        whole_match = match[0]
                        t = match[1]
                        match = match[2]
                        building = re.findall(r"type = ([^\t\n ]*)", match)[0]
                        level = re.findall(r"level = ([^\t\n ]*)", match)[0]
                        province = re.findall(r"province = (\d*)", match)[0]
                        localisation_key = "tooltip_add_building_on_victory_point"

                        if province in all_vps:

                            # One additional tab compared to extracted code
                            tooltip = t + '\t' + 'tooltip = {\n'
                            tooltip_loc_key = t + '\t\t' + 'localization_key = ' + localisation_key + '\n'
                            tooltip_building = t + '\t\t' + 'BUILDING = ' + building + '\n'
                            tooltip_number = t + '\t\t' + 'NUMBER = ' + level + '\n'
                            tooltip_victory_point = t + '\t\t' + 'VP = ' + province + '\n'
                            tooltip_end = t + '\t' + '}'

                            assembled_tooltip = tooltip + tooltip_loc_key + tooltip_building + tooltip_number + tooltip_victory_point + tooltip_end

                            match_with_added_tab = ''.join(['\t' + i + '\n' for i in whole_match.split('\n')])

                            assembled_override = t + 'custom_override_tooltip = {\n' + match_with_added_tab + assembled_tooltip + '\n' + t + '}'

                            text_file_new = text_file_new.replace(whole_match, assembled_override)
                            with open(filename, "w", encoding=file_encoding) as text_file_write:
                                text_file_write.write(text_file_new)

                        else:
                            print("skip")
