inputstr = """
	SpriteType = {
		name = "GFX_POL_light_1_7tp_dw_medium"
		texturefile = "gfx/interface/equipmentdesigner/tanks/designer/Poland/light_1/pol_7tp_dw.png"
	}
	SpriteType = {
		name = "GFX_POL_light_1_7tp_jw_early_medium"
		texturefile = "gfx/interface/equipmentdesigner/tanks/designer/Poland/light_1/pol_7tp_jw_early.png"
	}
	SpriteType = {
		name = "GFX_POL_light_1_7tp_jw_late_medium"
		texturefile = "gfx/interface/equipmentdesigner/tanks/designer/Poland/light_1/pol_7tp_jw_late.png"
	}
	SpriteType = {
		name = "GFX_POL_light_1_7tp_jw_tranmissions_medium"
		texturefile = "gfx/interface/equipmentdesigner/tanks/designer/Poland/light_1/pol_7tp_jw_tranmissions.png"
	}
"""

x = []
for i in inputstr.split('\n'):
    if 'GFX_POL' in i:
        x.append(i[10:-1])

for i in x.__reversed__():
    print(i)