import re

input_str = """
 USA_motorbike_equipment_1: "Harley-Davidson WLA"
 USA_motorbike_equipment_1_short: "WLA"
 USA_motorized_equipment_0: "Class-B Standardized Military Truck"
 USA_motorized_equipment_0_short: "Class-B Truck"
 USA_super_heavy_artillery_equipment_1: "Howitzer, 203-mm, Model 1"
 USA_super_heavy_artillery_equipment_1_short: "203-mm M1 Howitzer"
 USA_railway_gun_equipment_1: "Railway Gun, 8-inch, Model 6"
 USA_railway_gun_equipment_1_short: "8-inch M6 Railway Gun"
 USA_super_heavy_railway_gun_equipment_1: "Railway Gun, 406-mm, Model 1936"
 USA_super_heavy_railway_gun_equipment_1_short: "406-mm M1936 Railway Gun"
"""

result = str(input_str)
for i in input_str.split('\n'):
    if len(i) == 0:
        continue
    key = re.findall(' (.*):', i)[0]
    value = re.findall('".*"', i)[0]
    modified_i = i.replace(value, f'"${key}$"')
    result = result.replace(i, modified_i)

print(result)

# pattern_matches = re.findall(r'\tname = "([^ ].*?)"', input_str)
# for i in sorted(pattern_matches):
#     print(f'{i}')
