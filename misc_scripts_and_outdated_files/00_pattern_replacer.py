input_patterns = r"""
(?<! )(SOV_heavy_armor_entity)
SOV_heavy_armor_alt_entity\n\t\t\t\t$1

\{ (SOV_heavy_armor_entity) \}
{\n\t\t\t\tSOV_heavy_armor_alt_entity\n\t\t\t\t$1\n\t\t\t}
"""

str_to_replace = "SOV_heavy_armor"
str_to_replace_with = "EE_medium_armor"

print(input_patterns.replace(str_to_replace, str_to_replace_with))
