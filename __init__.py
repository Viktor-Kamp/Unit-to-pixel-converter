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
    # --- CUSTOM / MANUELL ---
    'CUSTOM': ("Custom", (0.0, 0.0)),
    'SEP': (" ", (0.0, 0.0)),
    
    # --- DIN A-Reihe (Standard) ---
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
    'SEP': (" ", (0.0, 0.0)),
    
    # --- DIN B-Reihe (Plakate/Ordner) ---
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
    'SEP': (" ", (0.0, 0.0)),
    
    # --- DIN C-Reihe (Umschläge) ---
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
    'SEP': (" ", (0.0, 0.0)),
    
    # --- DIN D-Reihe (Spezialformate) ---
    'D0': ("DIN D0", (771.0, 1091.0)),
    'D1': ("DIN D1", (545.0, 771.0)),
    'D2': ("DIN D2", (385.0, 545.0)),
    'D3': ("DIN D3", (272.0, 385.0)),
    'D4': ("DIN D4", (192.0, 272.0)),
    'D5': ("DIN D5", (136.0, 192.0)),
    'D6': ("DIN D6", (96.0, 136.0)),
    'SEP': (" ", (0.0, 0.0)),
    
    # --- US / ANSI Standards ---
    'US_Letter': ("US Letter", (215.9, 279.4)),
    'US_Legal': ("US Legal", (215.9, 355.6)),
    'US_Tabloid': ("US Tabloid", (279.4, 431.8)),
    'US_Ledger': ("US Ledger", (431.8, 279.4)),
    'ANSI_A': ("ANSI A", (215.9, 279.4)),
    'ANSI_B': ("ANSI B", (279.4, 431.8)),
    'ANSI_C': ("ANSI C", (431.8, 558.8)),
    'ANSI_D': ("ANSI D", (558.8, 863.6)),
    'ANSI_E': ("ANSI E", (863.6, 1117.6)),
    'SEP': (" ", (0.0, 0.0)),
    
    # --- US ARCH (Architektur) ---
    'ARCH_A': ("ARCH A", (228.6, 304.8)),
    'ARCH_B': ("ARCH B", (304.8, 457.2)),
    'ARCH_C': ("ARCH C", (457.2, 609.6)),
    'ARCH_D': ("ARCH D", (609.6, 914.4)),
    'ARCH_E': ("ARCH E", (914.4, 1219.2)),
    'ARCH_E1': ("ARCH E1", (762.0, 1066.8)),
    'SEP': (" ", (0.0, 0.0)),
    # --- Druck-Rohformate (SRA) ---
    'SRA0': ("SRA0", (900.0, 1280.0)),
    'SRA1': ("SRA1", (640.0, 900.0)),
    'SRA2': ("SRA2", (450.0, 640.0)),
    'SRA3': ("SRA3", (320.0, 450.0)),
    'SRA4': ("SRA4", (225.0, 320.0)),
    'SEP': (" ", (0.0, 0.0)),
    
    # --- Japanische Standards (JIS B) ---
    'JIS_B0': ("JIS B0", (1030.0, 1456.0)),
    'JIS_B1': ("JIS B1", (728.0, 1030.0)),
    'JIS_B2': ("JIS B2", (515.0, 728.0)),
    'JIS_B4': ("JIS B4", (257.0, 364.0)),
    'JIS_B5': ("JIS B5", (182.0, 257.0)),
    'SEP': (" ", (0.0, 0.0)),
    
    # --- Gängige Umschläge & Sonstiges ---
    'DL': ("DIN Lang", (110.0, 220.0)),
    'Env_C65': ("C6/5 Umschlag", (114.0, 229.0)),
    'Env_Comm_10': ("#10 Envelope (US)", (104.8, 241.3)),
    'Env_Monarch': ("Monarch Env (US)", (98.4, 190.5)),
    'Business_Card_EU': ("Visitenkarte (EU)", (85.0, 55.0)),
    'Business_Card_US': ("Visitenkarte (US)", (88.9, 50.8)),
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
    # Verhindert Auswahl von Leerzeilen (Keys die mit SEP beginnen)
    if self.preset_selection.startswith('SEP'):
        self.preset_selection = self.get("old_preset_selection", 'A4')
        return

    # Speichere gültige Auswahl für den Rücksprung-Fall
    self["old_preset_selection"] = self.preset_selection

    if self.preset_selection == 'CUSTOM':
        return
    
    # Rest deiner Logik...
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
