def open_text_file(filename: str) -> str:
    with open(filename, 'r', encoding='utf-8-sig') as text_file:      # 'utf-8-sig' is mandatory for UTF-8 w/BOM
        return text_file.read()


def clear_false_positives_flags(flags_dict: dict, false_positives: list = []):
    if len(false_positives) > 0:
        for key in false_positives:
            try:
                flags_dict.pop(key)
            except KeyError:
                continue

    false_keys = [key for key in flags_dict if '@' in key]
    for key in false_keys:
        flags_dict.pop(key)
