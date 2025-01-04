# Check vanilla and KR file and find differencess
from pathlib import Path
import re

VANILLA_INPUT_FILE = Path(r"C:\SteamLibrary\steamapps\common\Hearts of Iron IV\interface\Technologies.gfx")
KR_INPUT_FILE = Path(r"C:\Users\VADIM\Documents\Paradox Interactive\Hearts of Iron IV\mod\Kaiserreich Dev Build\interface\Technologies.gfx")
VANILLA_ADDITIONAL_TAGS = [
    "GFX_commonwealth_2d",
]


class SpriteType:
    def __init__(self, s: str):
        self.name = re.findall(r'name = "(.+)"', s)[0]
        self.texturefile = re.findall(r'texturefile = "(.+)"', s)[0]


def main():
    vanilla_gfx = []
    kr_gfx = []
    results = []
    sprite_pattern = r"SpriteType.*?\}"

    # Extract vanilla gfx
    with open(VANILLA_INPUT_FILE, 'r', encoding='utf-8') as text_file:
        input_file = text_file.read()
        spriteTypes = re.findall(sprite_pattern, input_file, flags=re.DOTALL | re.MULTILINE)
        for sprite in spriteTypes:
            vanilla_gfx.append(SpriteType(s=sprite))

    # Extract KR gfx
    with open(KR_INPUT_FILE, 'r', encoding='utf-8') as text_file:
        input_file = text_file.read()
        spriteTypes = re.findall(sprite_pattern, input_file, flags=re.DOTALL | re.MULTILINE)
        for sprite in spriteTypes:
            try:
                kr_gfx.append(SpriteType(s=sprite))
            except Exception:
                print(sprite)
                raise

    # Clean up vanilla gfx - remove tag-specific GFX
    vanilla_gfx_cleaned = []
    tag_pattern = r"GFX_[A-Z][A-Z][A-Z]_"
    for gfx in vanilla_gfx:
        tag_specific_gfx = re.findall(tag_pattern, gfx.name)
        if not tag_specific_gfx:
            for i in VANILLA_ADDITIONAL_TAGS:
                if i not in gfx.name:
                    vanilla_gfx_cleaned.append(gfx)

    # Check for duplicates in vanilla
    vanilla_gfx_names = [i.name for i in vanilla_gfx_cleaned]
    vanilla_duplicates = [i for i in vanilla_gfx_names if vanilla_gfx_names.count(i) > 1]
    if len(vanilla_duplicates) > 0:
        for i in vanilla_duplicates:
            results.append(f'Vanilla GFX `{i}` is duplicated')

    # Check for duplicates in KR
    kr_gfx_names = [i.name for i in kr_gfx]
    kr_duplicates = [i for i in kr_gfx_names if kr_gfx_names.count(i) > 1]
    if len(kr_duplicates) > 0:
        for i in kr_duplicates:
            results.append(f'KR GFX `{i}` is duplicated')

    for vanilla_gfx in vanilla_gfx_cleaned:
        # Vanilla GFX is not present in KR files
        if vanilla_gfx.name not in kr_gfx_names:
            results.append(f'Vanilla GFX `{vanilla_gfx.name}` is not present in KR GFX')

        # Vanilla GFX is present in KR files but texturefile is different (excluding .png)
        else:
            matching_kr_gfx = [i for i in kr_gfx if i.name == vanilla_gfx.name][0]
            if vanilla_gfx.texturefile != matching_kr_gfx.texturefile and ".png" not in matching_kr_gfx.texturefile:
                results.append(f'Vanilla GFX `{vanilla_gfx.name}` texturefile {vanilla_gfx.texturefile} != kr texturefile {matching_kr_gfx.texturefile}')

    # KR GFX is not present in vanilla files
    for i in kr_gfx:
        if i.name not in vanilla_gfx_names:
            results.append(f'KR GFX `{i.name}` is not present in vanilla GFX')

    if len(results) < 1:
        print("No issues found!")
    else:
        for i in results:
            print(i)


if __name__ == '__main__':
    main()
