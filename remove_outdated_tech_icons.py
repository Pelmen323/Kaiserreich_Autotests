import re
import os

INPUT_FILE_PATH = 'C:\\Users\\' + os.getlogin() + '\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\Kaiserreich Dev Build\\interface\\Technologies.gfx'
INPUT_LIST = [
    'early_submarine_medium',
    'basic_submarine_medium',
    'improved_submarine_medium',
    'advanced_submarine_medium',
    'cruiser_submarine_medium',
    'early_destroyer_medium',
    'basic_destroyer_medium',
    'improved_destroyer_medium',
    'advanced_destroyer_medium',
    'early_light_cruiser_medium',
    'basic_light_cruiser_medium',
    'improved_light_cruiser_medium',
    'advanced_light_cruiser_medium',
    'early_light_cruiser_capital_medium',
    'early_heavy_cruiser_medium',
    'basic_light_cruiser_capital_medium',
    'basic_heavy_cruiser_medium',
    'improved_light_cruiser_capital_medium',
    'improved_heavy_cruiser_medium',
    'advanced_light_cruiser_capital_medium',
    'advanced_heavy_cruiser_medium',
    'armoured_cruiser_medium',
    'early_battlecruiser_medium',
    'basic_battlecruiser_medium',
    'early_battleship_medium',
    'basic_battleship_medium',
    'improved_battleship_medium',
    'advanced_battleship_medium',
    'heavy_battleship_medium',
    'SH_battleship_1_medium',
    'SH_battleship_2_medium',
    'heavy_battleship2_medium',
    'early_carrier_medium',
    'basic_carrier_medium',
    'improved_carrier_medium',
    'advanced_carrier_medium',
    'modern_battlecruiser_medium',
    'advanced_battlecruiser_medium',
    'improved_battlecruiser_medium',
    'modern_submarine_medium',
    'modern_heavy_cruiser_medium',
    'modern_light_cruiser_capital_medium',
    'modern_light_cruiser_medium',
    'modern_carrier_medium',
    'modern_battleship_medium',
    'modern_destroyer_medium',
]


def main(input_list: list[str, str]):
    '''
    This script removes listed icons from tech gfx file
    Input - List
    '''

    with open(INPUT_FILE_PATH, 'r', encoding='utf-8') as text_file:
        input_file = text_file.read()
        input_file_repl = input_file

    for item in input_list:
        pattern = r'\tSpriteType = \{[^\}]+' + item + r'[^\}]+\}\n'
        matches = re.findall(pattern=pattern, string=input_file, flags=re.DOTALL | re.MULTILINE)

        if len(matches) > 0:
            for match in matches:
                if 'hull' not in match:
                    input_file_repl = input_file_repl.replace(match, '')

    with open(INPUT_FILE_PATH, 'w', encoding='utf-8') as text_file_write:
        text_file_write.write(input_file_repl)


if __name__ == '__main__':
    main(INPUT_LIST)
