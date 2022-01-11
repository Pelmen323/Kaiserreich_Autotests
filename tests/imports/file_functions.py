import os


def change_current_directory(filepath):
    try:
        os.chdir(filepath)
    except Exception:
        print("Unable to open the folder")
        raise


def open_text_file(filename: str) -> str:
    with open(filename, 'r', encoding='utf-8-sig') as text_file:      # 'utf-8-sig' is mandatory for UTF-8 w/BOM
        return text_file.read()
