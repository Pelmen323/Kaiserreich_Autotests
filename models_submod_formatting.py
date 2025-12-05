import re
from pathlib import Path
INPUT_FILE = 'C:\\Users\\VADIM\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\Kaiserreich Models Dev Build\\gfx\\entities\\z_units_KR_AMA.asset'


def format_models_submod(input_file: str):
    """Format entity definitions in asset files to have consistent spacing and ordering."""

    replacement_dict = {}
    file_path = Path(input_file)
    text_file = file_path.read_text(encoding='utf-8')
    entity_match = re.findall(r'entity = \{[^\}]+\}', text_file, flags=re.DOTALL | re.MULTILINE)
    if len(entity_match) > 0:
        for i in entity_match:
            if 'attach' not in i:
                try:
                    name_match = re.findall(r'name = ".*?"', i)[0]
                    pdxmesh_match = re.findall(r'pdxmesh = ".*?"', i)[0]
                    clone_match = re.findall(r'clone = ".*?"', i)[0]
                except IndexError:
                    continue

                assembled_replacement = f"entity = {{ {name_match:<55}{clone_match:<50}{pdxmesh_match} }}"
                replacement_dict[i] = assembled_replacement

    text_file_new = text_file
    for i in replacement_dict:
        text_file_new = text_file_new.replace(i, replacement_dict[i])

    file_path.write_text(text_file_new, encoding='utf-8')


if __name__ == '__main__':
    format_models_submod(INPUT_FILE)
