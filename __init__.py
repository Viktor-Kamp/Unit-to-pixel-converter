import bpy

bl_info = {
    "name": "Unit to pixel converter",
    "author": "Viktor Kamp",
    "version": (1, 3, 2),
    "blender": (4, 2, 0),
    "location": "Properties > Output > Unit to pixel converter",
    "description": "Calculates render resolution from different measurement units, including inch, centimeter and millimeter while also taking PPI/DPI into account.",
    "category": "Render",
}

# Helper
UNIT_DATA = {
    'MM': ("Millimeter", 25.4),
    'CM': ("Centimeter", 2.54),
    'INCH': ("Inch", 1.0),
    'BANANA': ("Banana", 25.4 / 178.0),
}
#UNIT_LABELS = {
#    'MM': 'mm',
#    'CM': 'cm',
#    'INCH': 'inch',
#    'BANANA': 'Banana',
}
PRESET_DATA = {
    'CUSTOM': ("Custom", (0.0, 0.0)),
    'SEP1': (" ", (0.0, 0.0)),
    
    # DIN A (Standard)
    'A0': ("DIN A0", (841.0, 1189.0)),
    'A1': ("DIN A1", (594.0, 841.0)),
    'A2': ("DIN A2", (420.0, 594.0)),
    'A3': ("DIN A3", (297.0, 420.0)),
    'A4': ("DIN A4", (210.0, 297.0)),
    'A5': ("DIN A5", (148.0, 210.0)),
    'A6': ("DIN A6", (105.0, 148.0)),
    'A7': ("DIN A7", (74.0, 105.0)),
    'A8': ("DIN A8", (52.0, 74.0)),
    'A9': ("DIN A9", (37.0, 52.0)),
    'A10': ("DIN A10", (26.0, 37.0)),
    'SEP2': (" ", (0.0, 0.0)),
    
    # DIN B (Posters/Folders)
    'B0': ("DIN B0", (1000.0, 1414.0)),
    'B1': ("DIN B1", (707.0, 1000.0)),
    'B2': ("DIN B2", (500.0, 707.0)),
    'B3': ("DIN B3", (353.0, 500.0)),
    'B4': ("DIN B4", (250.0, 353.0)),
    'B5': ("DIN B5", (176.0, 250.0)),
    'B6': ("DIN B6", (125.0, 176.0)),
    'B7': ("DIN B7", (88.0, 125.0)),
    'B8': ("DIN B8", (62.0, 88.0)),
    'B9': ("DIN B9", (44.0, 62.0)),
    'B10': ("DIN B10", (31.0, 44.0)),
    'SEP3': (" ", (0.0, 0.0)),
    
    # DIN C (Envelopes)
    'C0': ("DIN C0", (917.0, 1297.0)),
    'C1': ("DIN C1", (648.0, 917.0)),
    'C2': ("DIN C2", (458.0, 648.0)),
    'C3': ("DIN C3", (324.0, 458.0)),
    'C4': ("DIN C4", (229.0, 324.0)),
    'C5': ("DIN C5", (162.0, 229.0)),
    'C6': ("DIN C6", (114.0, 162.0)),
    'C7': ("DIN C7", (81.0, 114.0)),
    'C8': ("DIN C8", (57.0, 81.0)),
    'C9': ("DIN C9", (40.0, 57.0)),
    'C10': ("DIN C10", (28.0, 40.0)),
    'SEP4': (" ", (0.0, 0.0)),

    # DE / EU special
    'DL': ("DIN Long", (110.0, 220.0)),
    'DLE': ("DIN Long Extra", (115.0, 220.0)),
    'C6_5': ("Envelop C6/5", (114.0, 229.0)),
    'Business_Card_EU': ("Business card (EU)", (85.0, 55.0)),
    'SEP5': (" ", (0.0, 0.0)),

    # Japanese standards (JIS B)
    'JIS_B0': ("JIS B0", (1030.0, 1456.0)),
    'JIS_B1': ("JIS B1", (728.0, 1030.0)),
    'JIS_B2': ("JIS B2", (515.0, 728.0)),
    'JIS_B3': ("JIS B3", (364.0, 515.0)),
    'JIS_B4': ("JIS B4", (257.0, 364.0)),
    'JIS_B5': ("JIS B5", (182.0, 257.0)),
    'JIS_B6': ("JIS B6", (128.0, 182.0)),
    'JIS_B7': ("JIS B7", (91.0, 128.0)),
    'JIS_B8': ("JIS B8", (64.0, 91.0)),
    'JIS_B9': ("JIS B9", (45.0, 64.0)),
    'JIS_B10': ("JIS B10", (32.0, 45.0)),
    'SEP6': (" ", (0.0, 0.0)),
    
    # US / ANSI standards
    'US_Letter': ("US Letter", (215.9, 279.4)),
    'US_Half_Letter': ("US Half Letter", (139.7, 215.9)),
    'US_Legal': ("US Legal", (215.9, 355.6)),
    'US_Tabloid': ("US Tabloid", (279.4, 431.8)),
    'US_Ledger': ("US Ledger", (431.8, 279.4)),
    'US_Executive': ("US Executive", (184.15, 266.7)),
    'US_Statement': ("US Statement", (139.7, 215.9)),
    'Env_Comm_10': ("US #10 Envelope", (104.775, 241.3)),
    'Business_Card_US': ("US Business card", (88.9, 50.8)),
}

# Changes "Preset" to "Custom" if manually changed
def update_to_custom(self, context):
    # Prevents an infinite loop whilst a preset is being loaded
    if self.get("_no_update", False):
        return
    if self.preset_selection != 'CUSTOM':
        self.preset_selection = 'CUSTOM'

# Updates if "Preset" is changed
def update_preset_values(self, context):
    # Prevents selection of blank lines
    if self.preset_selection.startswith('SEP'):
        self.preset_selection = self.get("old_preset_selection", 'A4')
        return

    # Save valid selection for the case where the user returns
    self["old_preset_selection"] = self.preset_selection

    if self.preset_selection == 'CUSTOM':
        return
    
    self["_no_update"] = True
    try:    
        width_mm, height_mm = PRESET_DATA[self.preset_selection][1]
        target_factor = UNIT_DATA[self.unit_selection][1]
        self.unit_width = (width_mm / 25.4) * target_factor
        self.unit_height = (height_mm / 25.4) * target_factor
    finally:    
        self["_no_update"] = False

# Converts input values, when unit is changed
def update_unit_conversion(self, context):
    old_unit = self.get("old_unit_selection", 'MM')
    new_unit = self.unit_selection
    
    if old_unit != new_unit:
        old_factor = UNIT_DATA[old_unit][1]
        new_factor = UNIT_DATA[new_unit][1]
        
        self["_no_update"] = True
        try:
            self.unit_width = (self.unit_width / old_factor) * new_factor
            self.unit_height = (self.unit_height / old_factor) * new_factor
            bleed_in_inch = self.bleed_amount / old_factor
            self.bleed_amount = bleed_in_inch * new_factor
        finally:        
            self["_no_update"] = False
        
    self["old_unit_selection"] = new_unit

def calculate_res(scene):
    factor = UNIT_DATA[scene.unit_selection][1]
    
    width_inch = scene.unit_width / factor
    height_inch = scene.unit_height / factor
    
    bleed_inch = (scene.bleed_amount / factor) * 2
    
    px_x = int(round((width_inch + bleed_inch) * scene.render_ppi))
    px_y = int(round((height_inch + bleed_inch) * scene.render_ppi))
    return px_x, px_y

# UI panel
class RENDER_PT_unit_to_px(bpy.types.Panel):
    bl_label = "Unit to pixel converter"
    bl_idname = "RENDER_PT_unit_to_px"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "output"

    def draw(self, context):
        layout = self.layout
        s = context.scene
        
        layout.use_property_split = True
        layout.use_property_decorate = False

        col = layout.column(align=True)
        col.prop(s, "preset_selection")
        col.separator()
        col.prop(s, "unit_selection")
        col.prop(s, "unit_width")
        col.prop(s, "unit_height")
        col.prop(s, "render_ppi")
        #bleed_label = f"Bleed ({UNIT_LABELS[s.unit_selection]})"
        col.prop(s, "bleed_amount", text=bleed_label)
        
        px_x, px_y = calculate_res(s)
        box = layout.box()
        box.label(text=f"Preview: {px_x} x {px_y} px", icon='INFO')
        layout.operator("render.apply_unit_to_px", text="Apply Resolution", icon='CHECKMARK')

# Operator
class RENDER_OT_apply_unit_to_px(bpy.types.Operator):
    bl_idname = "render.apply_unit_to_px"
    bl_label = "Apply Unit to Pixel"
    bl_options = {'UNDO'}

    def execute(self, context):
        s = context.scene
        res_x, res_y = calculate_res(s)
        s.render.resolution_x = res_x
        s.render.resolution_y = res_y

        # Changes "Pixels" in "Pixel Density" panel according to PPI from Add-On
        if hasattr(s.render, "ppm_factor"):
            current_base = s.render.ppm_base
            s.render.ppm_factor = (s.render_ppi / 0.0254) * current_base

        self.report({'INFO'}, f"Resolution set to: {res_x}x{res_y} px and {s.render_ppi} PPI")
        return {'FINISHED'}
        
# Registration
classes = (RENDER_PT_unit_to_px, RENDER_OT_apply_unit_to_px)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.preset_selection = bpy.props.EnumProperty(name="Preset",items=[(k, v[0], "") for k, v in PRESET_DATA.items()], default='A4', update=update_preset_values, options=set())
    bpy.types.Scene.unit_selection = bpy.props.EnumProperty(name="Unit", items=[(k, v[0], "") for k, v in UNIT_DATA.items()], default='MM', update=update_unit_conversion, options=set())

    bpy.types.Scene.unit_width = bpy.props.FloatProperty(name="Width", default=210.0, min=0.001, update=update_to_custom, options=set())
    bpy.types.Scene.unit_height = bpy.props.FloatProperty(name="Height", default=297.0, min=0.001, update=update_to_custom, options=set())
    bpy.types.Scene.render_ppi = bpy.props.IntProperty(name="PPI", default=300, min=1, options=set())
    bpy.types.Scene.bleed_amount = bpy.props.FloatProperty(name="Bleed", default=0.0, min=0.0, options=set())

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.preset_selection
    del bpy.types.Scene.unit_selection
    del bpy.types.Scene.unit_width
    del bpy.types.Scene.unit_height
    del bpy.types.Scene.render_ppi
    del bpy.types.Scene.bleed_amount
    
if __name__ == "__main__":
    register()
