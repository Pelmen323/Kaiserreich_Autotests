inputstr = """
	SpriteType = {
		name = "GFX_JAP_medium_1_chi_ha_120mm_medium"
		texturefile = "gfx/interface/equipmentdesigner/tanks/designer/Japan/medium_1/jap_chi_ha_120mm.png"
	}
	SpriteType = {
		name = "GFX_JAP_medium_1_chi_ha_command_medium"
		texturefile = "gfx/interface/equipmentdesigner/tanks/designer/Japan/medium_1/jap_chi_ha_command.png"
	}
	SpriteType = {
		name = "GFX_JAP_medium_1_chi_ha_dozer_medium"
		texturefile = "gfx/interface/equipmentdesigner/tanks/designer/Japan/medium_1/jap_chi_ha_dozer.png"
	}
	SpriteType = {
		name = "GFX_JAP_medium_1_chi_ha_kai_medium"
		texturefile = "gfx/interface/equipmentdesigner/tanks/designer/Japan/medium_1/jap_chi_ha_kai.png"
	}
	SpriteType = {
		name = "GFX_JAP_medium_1_chi_ni_medium"
		texturefile = "gfx/interface/equipmentdesigner/tanks/designer/Japan/medium_1/jap_chi_ni.png"
	}
	SpriteType = {
		name = "GFX_JAP_medium_1_chi_nu_kai_medium"
		texturefile = "gfx/interface/equipmentdesigner/tanks/designer/Japan/medium_1/jap_chi_nu_kai.png"
	}
	SpriteType = {
		name = "GFX_JAP_medium_1_chi_nu_medium"
		texturefile = "gfx/interface/equipmentdesigner/tanks/designer/Japan/medium_1/jap_chi_nu.png"
	}
	SpriteType = {
		name = "GFX_JAP_medium_1_ho_i_medium"
		texturefile = "gfx/interface/equipmentdesigner/tanks/designer/Japan/medium_1/jap_ho_i.png"
	}
"""

x = []
for i in inputstr.split('\n'):
    if 'GFX_JAP' in i:
        x.append(i[10:-1])

for i in x.__reversed__():
    print(i)