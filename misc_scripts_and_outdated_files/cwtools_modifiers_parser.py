import re

from test_classes.generic_test_class import FileOpener

filename = "C:\\SteamLibrary\\steamapps\\common\\Hearts of Iron IV\\documentation\\modifiers_documentation.md"
text_file = FileOpener.open_text_file(filename, lowercase=False)
results = []

modifiers_code = re.findall("### (.*?Categories:.*?\\n)", text_file, flags=re.DOTALL | re.MULTILINE)
for modifier in modifiers_code:
    modifier_name = re.findall("^(.*)", modifier)[0]
    modifier_categories = re.findall("Categories:(.*)", modifier)[0]
    if "," not in modifier_categories:
        results.append(f"	{modifier_name} = {modifier_categories}")
    else:
        categories = modifier_categories.split(", ")
        for i in categories:
            results.append(f"	{modifier_name} = {i}")

results_sorted = sorted(results, key=lambda x: x[x.index("=")+2:])
for i in results_sorted:
    print(i)
