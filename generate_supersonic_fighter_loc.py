##########################
# Test script to check if `set_autonomy` has `end_wars = no` statement
# By Pelmen, https://github.com/Pelmen323
##########################
import re
import os

from test_classes.generic_test_class import FileOpener
FILEPATH_TO_LOC = f"C:\\Users\\{os.getlogin()}\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\Kaiserreich Dev Build\\localisation\\english\\KR_common\\Equip Air l_english.yml"


def main():
    input_list = [
        ["jet_fighter_equipment_2_short", "small_plane_airframe_5_short"],
    ]
    text_file = FileOpener.open_text_file(FILEPATH_TO_LOC, lowercase=False)
    text_file_copy = text_file
    override = False
    for i in input_list:
        parent_str = i[0]
        child_str = i[1]
        tag_and_value_list = re.findall(' ((...)_'+parent_str+': "(.*?)")', text_file)

        for item in tag_and_value_list:
            base_string = item[0]
            tag = item[1]
            value = item[2]
            child_str_with_tag = tag + '_' + child_str + ':'
            if child_str_with_tag not in text_file:
                string_to_append = '\n ' + child_str_with_tag + '"' + value + '"'
                text_file_copy = text_file_copy.replace(base_string, base_string+string_to_append)
                override = True

    if override:
        with open(FILEPATH_TO_LOC, 'w', encoding="utf-8-sig") as text_file_write:
            text_file_write.write(text_file_copy)


if __name__ == '__main__':
    main()
