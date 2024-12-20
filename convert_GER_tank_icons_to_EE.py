import os
from PIL import Image
import numpy as np

# Specify input and output directories
input_folder = "input_images"  # Folder containing input images
output_folder = "output_images"  # Folder to save the processed images
OUTPUT_FILE = "technology_icons_tanks_EE.gfx"  # Folder to save the processed images


def change_color(input_path, output_path):
    # Open the image
    img = Image.open(input_path).convert("RGBA")

    # Convert image to numpy array
    data = np.array(img)

    # Extract RGBA channels
    r, g, b, a = data[..., 0], data[..., 1], data[..., 2], data[..., 3]

    # Target tint values (blended average from Tank AA and TD)
    target_r = 56.73 * 0.5  # Average red
    target_g = 58.55 * 0.5  # Average green
    target_b = 35.68 * 0.5  # Average blue

    # Scale factors for applying the tint
    r_scale = target_r / np.mean(r[a > 0])  # Adjust red based on alpha mask
    g_scale = target_g / np.mean(g[a > 0])  # Adjust green
    b_scale = target_b / np.mean(b[a > 0])  # Adjust blue

    # Apply the transformation
    data[..., 0] = (r * r_scale).clip(0, 255).astype(np.uint8)
    data[..., 1] = (g * g_scale).clip(0, 255).astype(np.uint8)
    data[..., 2] = (b * b_scale).clip(0, 255).astype(np.uint8)

    # Recreate the image
    result_img = Image.fromarray(data, 'RGBA')

    # Save the result
    result_img.save(output_path)


def batch_process(input_folder, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
    output_list = []
    texturepath = "gfx/interface/technologies/EE/tanks/"

    # Loop through all files in the input folder
    for file_name in os.listdir(input_folder):
        input_path = os.path.join(input_folder, file_name)

        # Check if the file is an image
        if not file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            continue

        # Various naming fixes
        new_file_name = file_name.replace("GER_", "EE_")
        new_file_name = new_file_name.replace("adv_", "advanced_")
        new_file_name = new_file_name.replace("imp_", "improved_")
        new_file_name = new_file_name.replace("main_tank", "medium_tank")
        new_file_name = new_file_name.replace("superheavy", "super_heavy")
        new_file_name = new_file_name.replace("_spa", "_art")
        new_file_name = new_file_name.replace("_aa", "_spaa")
        new_file_name = new_file_name.replace("main_battle_tank_art", "modern_art")
        new_file_name = new_file_name.replace("main_battle_tank_spaa", "modern_spaa")
        new_file_name = new_file_name.replace("main_battle_tank_td", "modern_td")
        new_file_name = new_file_name.replace("tank_art", "art")
        new_file_name = new_file_name.replace("tank_spaa", "spaa")
        new_file_name = new_file_name.replace("tank_td", "td")

        output_path = os.path.join(output_folder, new_file_name)

        print(f"Processing {file_name} -> {new_file_name}...")
        try:
            change_color(input_path, output_path)
        except Exception as e:
            print(f"Failed to process {file_name}: {e}")

        output_str = '\tSpriteType = {\n\t\tname = "GFX_' + new_file_name[:-4] + '_medium"\n\t\ttexturefile = "' + texturepath + new_file_name + '"\n\t}\n'
        output_list.append(output_str)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as text_file_write:
        output_list = sorted(output_list)
        output_file = 'spriteTypes = {\n' + ''.join(output_list) + '}\n'
        text_file_write.write(output_file)


# Run batch processing
batch_process(input_folder, output_folder)
