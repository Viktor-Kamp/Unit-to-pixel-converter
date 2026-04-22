import bpy

bl_info = {
    "name": "Unit to pixel converter",
    "author": "Viktor Kamp",
    "version": (1, 2, 1),
    "blender": (4, 2, 0),
    "location": "Properties > Output > Unit to pixel converter",
    "description": "Calculates render resolution from different units, including inch, centimeter and millimeter while also taking PPI/DPI into account.",
    "category": "Render",
}

# Helper
UNIT_DATA = {
    'MM': ("Millimeter", 25.4),
    'CM': ("Centimeter", 2.54),
    'INCH': ("Inch", 1.0),
    'BANANA': ("Banana", 25.4 / 178.0),
}
PRESET_DATA = {
    # --- Allgemein ---
    'CUSTOM': ("--- EIGENE MAẞE ---", (0.0, 0.0)),
    
    # --- DIN A-REIHE ---
    'HEADER_A': ("--- DIN A (Standard) ---", (0.0, 0.0)),
    'A0': ("A0", (841.0, 1189.0)),
    'A1': ("A1", (594.0, 841.0)),
    'A2': ("A2", (420.0, 594.0)),
    'A3': ("A3", (297.0, 420.0)),
    'A4': ("A4", (210.0, 297.0)),
    'A5': ("A5", (148.0, 210.0)),
    'A6': ("A6", (105.0, 148.0)),
    'A7': ("A7", (74.0, 105.0)),
    'A8': ("A8", (52.0, 74.0)),
    'A9': ("A9", (37.0, 52.0)),
    'A10': ("A10", (26.0, 37.0)),

    # --- DIN B-REIHE ---
    'HEADER_B': ("--- DIN B (Plakate) ---", (0.0, 0.0)),
    'B0': ("B0", (1000.0, 1414.0)),
    'B1': ("B1", (707.0, 1000.0)),
    'B2': ("B2", (500.0, 707.0)),
    'B3': ("B3", (353.0, 500.0)),
    'B4': ("B4", (250.0, 353.0)),
    'B5': ("B5", (176.0, 250.0)),
    'B6': ("B6", (125.0, 176.0)),
    'B7': ("B7", (88.0, 125.0)),
    'B8': ("B8", (62.0, 88.0)),
    'B9': ("B9", (44.0, 62.0)),
    'B10': ("B10", (31.0, 44.0)),

    # --- DIN C-REIHE ---
    'HEADER_C': ("--- DIN C (Umschläge) ---", (0.0, 0.0)),
    'C0': ("C0", (917.0, 1297.0)),
    'C1': ("C1", (648.0, 917.0)),
    'C2': ("C2", (458.0, 648.0)),
    'C3': ("C3", (324.0, 458.0)),
    'C4': ("C4", (229.0, 324.0)),
    'C5': ("C5", (162.0, 229.0)),
    'C6': ("C6", (114.0, 162.0)),
    'C7': ("C7", (81.0, 114.0)),
    'C8': ("C8", (57.0, 81.0)),
    'C9': ("C9", (40.0, 57.0)),
    'C10': ("C10", (28.0, 40.0)),

    # --- US / ANSI STANDARDS ---
    'HEADER_US': ("--- US / ANSI ---", (0.0, 0.0)),
    'US_Letter': ("US Letter", (215.9, 279.4)),
    'US_Legal': ("US Legal", (215.9, 355.6)),
    'US_Tabloid': ("US Tabloid", (279.4, 431.8)),
    'ANSI_A': ("ANSI A", (215.9, 279.4)),
    'ANSI_B': ("ANSI B", (279.4, 431.8)),
    'ANSI_C': ("ANSI C", (431.8, 558.8)),
    'ANSI_D': ("ANSI D", (558.8, 863.6)),
    'ANSI_E': ("ANSI E", (863.6, 1117.6)),

    # --- ARCHITEKTUR ---
    'HEADER_ARCH': ("--- ARCH (Bauwesen) ---", (0.0, 0.0)),
    'ARCH_A': ("ARCH A", (228.6, 304.8)),
    'ARCH_B': ("ARCH B", (304.8, 457.2)),
    'ARCH_C': ("ARCH C", (457.2, 609.6)),
    'ARCH_D': ("ARCH D", (609.6, 914.4)),
    'ARCH_E': ("ARCH E", (914.4, 1219.2)),

    # --- PROFI-DRUCK (ROHBÖGEN) ---
    'HEADER_SRA': ("--- SRA (Druckerei) ---", (0.0, 0.0)),
    'SRA0': ("SRA0", (900.0, 1280.0)),
    'SRA1': ("SRA1", (640.0, 900.0)),
    'SRA2': ("SRA2", (450.0, 640.0)),
    'SRA3': ("SRA3", (320.0, 450.0)),
    'SRA4': ("SRA4", (225.0, 320.0)),

    # --- SPECIALS ---
    'HEADER_SPEC': ("--- Spezialformate ---", (0.0, 0.0)),
    'DL': ("DIN Lang", (110.0, 220.0)),
    'Env_Comm_10': ("#10 Business (US)", (104.8, 241.3)),
    'Business_Card_EU': ("Visitenkarte EU", (85.0, 55.0)),
    'Business_Card_US': ("Visitenkarte US", (88.9, 50.8)),
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
    if self.preset_selection == 'CUSTOM' or self.preset_selection.startswith('HEADER_'):
        return
    
    # Set a flag to ignore "update_to_custom"
    self["_no_update"] = True
    
    width_mm, height_mm = PRESET_DATA[self.preset_selection][1]
    target_factor = UNIT_DATA[self.unit_selection][1]
    
    self.unit_width = (width_mm / 25.4) * target_factor
    self.unit_height = (height_mm / 25.4) * target_factor
    
    self["_no_update"] = False

# Converts input values, when unit is changed
def update_unit_conversion(self, context):
    old_unit = self.get("old_unit_selection", 'MM')
    new_unit = self.unit_selection
    
    if old_unit != new_unit:
        old_factor = UNIT_DATA[old_unit][1]
        new_factor = UNIT_DATA[new_unit][1]
        
        self["_no_update"] = True

        self.unit_width = (self.unit_width / old_factor) * new_factor
        self.unit_height = (self.unit_height / old_factor) * new_factor
        
        if old_unit == 'INCH' or new_unit == 'INCH':
            if new_unit == 'INCH':
                self.bleed_amount = self.bleed_amount / 25.4
            else:
                self.bleed_amount = self.bleed_amount * 25.4
                
        self["_no_update"] = False
        
    self["old_unit_selection"] = new_unit

def calculate_res(scene):
    factor = UNIT_DATA[scene.unit_selection][1]
    
    width_inch = scene.unit_width / factor
    height_inch = scene.unit_height / factor
    
    if scene.unit_selection == 'INCH':
        bleed_inch = scene.bleed_amount * 2
    else:
        bleed_inch = (scene.bleed_amount * 2) / 25.4
    
    px_x = int((width_inch + bleed_inch) * scene.render_ppi)
    px_y = int((height_inch + bleed_inch) * scene.render_ppi)
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
        layout.use_property_split = True
        s = context.scene

        col = layout.column(align=True)
        col.prop(s, "preset_selection")
        col.separator()
        col.prop(s, "unit_selection")
        col.prop(s, "unit_width")
        col.prop(s, "unit_height")
        col.prop(s, "render_ppi")
        col.separator()

        bleed_label = "Bleed (inch)" if s.unit_selection == 'INCH' else "Bleed (mm)"
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

    bpy.types.Scene.preset_selection = bpy.props.EnumProperty(name="Preset",items=[(k, v[0], "") for k, v in PRESET_DATA.items()], default='A4', update=update_preset_values)
    bpy.types.Scene.unit_selection = bpy.props.EnumProperty(name="Unit", items=[(k, v[0], "") for k, v in UNIT_DATA.items()], default='MM', update=update_unit_conversion)

    bpy.types.Scene.unit_width = bpy.props.FloatProperty(name="Width", default=210.0, min=0.001, update=update_to_custom)
    bpy.types.Scene.unit_height = bpy.props.FloatProperty(name="Height", default=297.0, min=0.001, update=update_to_custom)
    bpy.types.Scene.render_ppi = bpy.props.IntProperty(name="PPI", default=300, min=1)
    bpy.types.Scene.bleed_amount = bpy.props.FloatProperty(name="Bleed", default=0.0, min=0.0)

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
