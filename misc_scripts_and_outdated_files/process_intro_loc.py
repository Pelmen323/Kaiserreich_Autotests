import re
import os
import glob

INPUT_FILE_PATH = 'C:\\Users\\' + os.getlogin() + '\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\Kaiserreich Dev Build\\interface\\kaiserreich\\welcome_splash.gfx'
OUTPUT_FILE_PATH = 'C:\\Users\\' + os.getlogin() + '\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\Kaiserreich Dev Build\\localisation\\english\\KR_country_specific\\'


def main():
    '''
    This script autogenerates chassis icons based on tank icons
    Input - List
    Input[0] - chassis icon
    Input[1] - tank icon
    Script generates chassis icons for all tags that have relevant tank icons
    '''
    loc_entries = {}
    results = []

    with open(INPUT_FILE_PATH, 'r', encoding='utf-8') as text_file:
        input_file = text_file.read()

    name_objects = re.findall(r'name = "(GFX_(...)_intro)"', input_file)
    for i in name_objects:
        loc_entries[i[1]] = i[0]

    for filename in glob.iglob(OUTPUT_FILE_PATH + "**/*.yml", recursive=True):
        OVERRIDE = False
        with open(filename, 'r', encoding='utf-8-sig') as text_file:
            input_file = text_file.read()
            file_name = os.path.basename(filename)
            tag = file_name[:3]
            if tag in loc_entries.keys():
                input_file_new = input_file
                matching_value = loc_entries[tag]

                ## Grab anchor
                try:
                    anchor = re.findall(tag + r'_country_intro_header:.*', input_file)[0]
                    added_line = f'{tag}_country_intro_background: "{matching_value}"\n ' + anchor
                    OVERRIDE = True
                    input_file_new = input_file_new.replace(anchor, added_line)
                except IndexError:
                    results.append(f'{tag}_country_intro_header line not found in {file_name}, add {tag}_country_intro_background: "{matching_value}" manually')
                    continue

        if OVERRIDE:
            with open(filename, 'w', encoding='utf-8-sig') as text_file_write:
                text_file_write.write(input_file_new)



    # for item in input_list:
    #     i = item[0]
    #     chassis = item[1]
    #     tank_icon_pattern = 'GFX_..._' + i
    #     tank_tech_icons = re.findall(tank_icon_pattern, input_file)

    #     for tank_icon in tank_tech_icons:
    #         tag = re.findall(r'GFX_(...)_', tank_icon)[0]
    #         tank_icon_path = re.findall(tank_icon + '.*?\n.*?texturefile.*?=.*?"(.*?)"', input_file)[0]
    #         output_str = '\tSpriteType = {\n\t\tname = "GFX_' + tag + '_' + chassis + '"\n\t\ttexturefile = "' + tank_icon_path + '"\n\t}\n'
    #         output_list.append(output_str)

    # with open(OUTPUT_FILE_PATH, 'w', encoding='utf-8') as text_file_write:
    #     output_list = sorted(output_list)
    #     output_file = HEADER_STR + 'spriteTypes = {\n' + ''.join(output_list) + '}\n'
    #     text_file_write.write(output_file)
    for i in results:
        print(i)

if __name__ == '__main__':
    main()
