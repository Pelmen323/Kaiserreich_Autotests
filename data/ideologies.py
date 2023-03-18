# Used for performance tests to replace `has_government` lines with scripted triggers
ideology_bundles = {
    "has_socialist_government": ["has_government = totalist", "has_government = syndicalist", "has_government = radical_socialist"],
    "has_democratic_government": ["has_government = social_democrat", "has_government = social_liberal", "has_government = market_liberal", "has_government = social_conservative", "has_government = authoritarian_democrat"],
    "has_elected_government": ["has_government = social_democrat", "has_government = social_liberal", "has_government = market_liberal", "has_government = social_conservative"],
    "has_any_authoritarian_government": ["has_government = totalist", "has_government = authoritarian_democrat", "has_government = paternal_autocrat", "has_government = national_populist"],
    "has_liberal_government": ["has_government = social_liberal", "has_government = market_liberal", "has_government = social_democrat"],
    "has_authoritarian_government": ["has_government = authoritarian_democrat", "has_government = paternal_autocrat", "has_government = national_populist"],
    "has_dictatorship_government": ["has_government = paternal_autocrat", "has_government = national_populist"],
    "has_right_democratic_government": ["has_government = social_conservative", "has_government = market_liberal"],
    "has_left_democratic_government": ["has_government = social_liberal", "has_government = social_democrat"],
    "has_conservative_government": ["has_government = social_conservative", "has_government = authoritarian_democrat"], 
}
