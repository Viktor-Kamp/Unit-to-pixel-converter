import bpy

bl_info = {
    "name": "Unit to pixel converter",
    "author": "Viktor Kamp",
    "version": (1, 2, 0),
    "blender": (4, 2, 0),
    "location": "Properties > Output > Unit to pixel converter",
    "description": "Calculates render resolution from different units, including inch, centimeter and millimeter.",
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
    'CUSTOM': ("Custom", (0.0, 0.0)),
    'A0': ("DIN A0", (841.0, 1189.0)),
    'A1': ("DIN A1", (594.0, 841.0)),
    'A2': ("DIN A2", (420.0, 594.0)),
    'A3': ("DIN A3", (297.0, 420.0)),
    'A4': ("DIN A4", (210.0, 297.0)),
    'A5': ("DIN A5", (148.0, 210.0)),
    'A6': ("DIN A6", (105.0, 148.0)),
    'US_LETTER': ("US Letter", (215.9, 279.4)),
    'US_LEGAL': ("US Legal", (215.9, 355.6)),
    'TABLOID': ("Tabloid", (279.4, 431.8)),
}

# Changes to "Preset" to "Custom" if manually changed
def update_to_custom(self, context):
    # Prevents an infinite loop whilst a preset is being loaded
    if self.get("_no_update", False):
        return
    if self.preset_selection != 'CUSTOM':
        self.preset_selection = 'CUSTOM'

# Updates if "Preset" is changed
def update_preset_values(self, context):
    if self.preset_selection == 'CUSTOM':
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
        self["_no_update"] = False
        
    self["old_unit_selection"] = new_unit

def calculate_res(scene):
    factor = UNIT_DATA[scene.unit_selection][1]
    # Konvertiere Grundmaße in Inch
    width_inch = scene.unit_width / factor
    height_inch = scene.unit_height / factor
    
    # Addiere Anschnitt (immer in MM angegeben, daher / 25.4 für Inch)
    bleed_w_inch = (scene.bleed_left + scene.bleed_right) / 25.4
    bleed_h_inch = (scene.bleed_top + scene.bleed_bottom) / 25.4
    
    px_x = int((width_inch + bleed_w_inch) * scene.render_ppi)
    px_y = int((height_inch + bleed_h_inch) * scene.render_ppi)
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
        col.prop(s, "preset_selection", text="Preset")
        col.separator()
        col.prop(s, "unit_selection", text="Unit")
        col.prop(s, "unit_width")
        col.prop(s, "unit_height")
        
        # Anschnitt Sektion
        col.separator()
        bleed_box = layout.box()
        bleed_box.label(text="Bleed (mm)")
        row = bleed_box.row(align=True)
        row.use_property_split = False # Kompakter für 4 Felder
        row.prop(s, "bleed_top", text="Top")
        row.prop(s, "bleed_bottom", text="Bot")
        row.prop(s, "bleed_left", text="L")
        row.prop(s, "bleed_right", text="R")

        layout.prop(s, "render_ppi")
        
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

        # Changes "Pixel Density" according to PPI from Add-On
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

    bpy.types.Scene.preset_selection = bpy.props.EnumProperty(
        name="Preset",
        items=[(k, v[0], "") for k, v in PRESET_DATA.items()],
        default='A4',
        update=update_preset_values
    )
    
    bpy.types.Scene.unit_selection = bpy.props.EnumProperty(
        name="Unit", 
        items=[(k, v[0], "") for k, v in UNIT_DATA.items()], 
        default='MM',
        update=update_unit_conversion
    )

    bpy.types.Scene.unit_width = bpy.props.FloatProperty(
        name="Width", default=210.0, min=0.001, update=update_to_custom)
    bpy.types.Scene.unit_height = bpy.props.FloatProperty(
        name="Height", default=297.0, min=0.001, update=update_to_custom)
    
    # Neue Bleed-Properties (Millimeter)
    bpy.types.Scene.bleed_top = bpy.props.FloatProperty(name="Top", default=3.0, min=0.0)
    bpy.types.Scene.bleed_bottom = bpy.props.FloatProperty(name="Bottom", default=3.0, min=0.0)
    bpy.types.Scene.bleed_left = bpy.props.FloatProperty(name="Left", default=3.0, min=0.0)
    bpy.types.Scene.bleed_right = bpy.props.FloatProperty(name="Right", default=3.0, min=0.0)
    
    bpy.types.Scene.render_ppi = bpy.props.IntProperty(name="PPI", default=300, min=1)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.preset_selection
    del bpy.types.Scene.unit_selection
    del bpy.types.Scene.unit_width
    del bpy.types.Scene.unit_height
    del bpy.types.Scene.bleed_top
    del bpy.types.Scene.bleed_bottom
    del bpy.types.Scene.bleed_left
    del bpy.types.Scene.bleed_right
    del bpy.types.Scene.render_ppi

if __name__ == "__main__":
    register()
