import os
import glob

# Specify input and output directories
OUTPUT_FILE = "technology_icons_planes_Germany.gfx"
INPUT_FOLDER = 'C:\\Users\\' + os.getlogin() + '\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\Kaiserreich Dev Build\\gfx\\interface\\equipmentdesigner\\planes\\Germany\\'


def batch_process(input_folder):
    # Ensure the output folder exists
    # os.makedirs(output_folder, exist_ok=True)
    output_list = []

    # Loop through all files in the input folder
    for file in glob.iglob(input_folder + "**/*.png", recursive=True):
        file_name = os.path.basename(file)
        # Check if the file is an image
        if not file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            continue

        # Extract the folder path containing the file
        folder_path = os.path.dirname(file)
        # Get the last folder in the path
        subfolder_name = os.path.basename(folder_path)
        new_file_name = file_name.replace("ger_", "GER_" + subfolder_name + "_")
        texturepath = "gfx/interface/equipmentdesigner/planes/Germany/" + subfolder_name + "/"

        output_str = '\tSpriteType = {\n\t\tname = "GFX_' + new_file_name[:-4] + '_medium"\n\t\ttexturefile = "' + texturepath + file_name + '"\n\t}\n'
        print('GFX_' + new_file_name[:-4] + '_medium')
        output_list.append(output_str)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as text_file_write:
        output_list = sorted(output_list)
        output_file = 'spriteTypes = {\n' + ''.join(output_list) + '}\n'
        text_file_write.write(output_file)


# Run batch processing
batch_process(INPUT_FOLDER)
