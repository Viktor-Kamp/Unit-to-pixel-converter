import bpy

bl_info = {
    "name": "Unit to pixel converter",
    "author": "Viktor Kamp",
    "version": (1, 0, 2),
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

# Neue Logik für die Einheiten-Umrechnung
def update_unit_conversion(self, context):
    # Wir nutzen einen Hilfswert in der Scene, um die alte Einheit zu tracken
    old_unit = self.get("old_unit_selection", self.unit_selection)
    new_unit = self.unit_selection
    
    if old_unit != new_unit:
        _, old_factor = UNIT_DATA[old_unit]
        _, new_factor = UNIT_DATA[new_unit]
        
        # Umrechnung: Wert -> Inch -> neue Einheit
        self.unit_width = (self.unit_width / old_factor) * new_factor
        self.unit_height = (self.unit_height / old_factor) * new_factor
        
        # Aktuellen Stand für den nächsten Wechsel speichern
        self["old_unit_selection"] = new_unit

# UI Panel
class RENDER_PT_unit_to_px(bpy.types.Panel):
    bl_label = "Unit to pixel converter"
    bl_idname = "RENDER_PT_unit_to_px"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "output"

    # Input fields
    def draw(self, context):
        layout = self.layout
        s = context.scene

        col = layout.column(align=True)
        col.prop(s, "unit_selection", text="Unit")
        col.separator()
        col.prop(s, "unit_width")
        col.prop(s, "unit_height")
        col.prop(s, "render_ppi")
        
        # Preview
        px_x, px_y = calculate_res(s)
        
        box = layout.box()
        box.label(text=f"Preview: {px_x} x {px_y} px", icon='INFO')
        
        # Apply button
        layout.operator("render.apply_unit_to_px", text="Apply Resolution", icon='CHECKMARK')

# Operator
class RENDER_OT_apply_unit_to_px(bpy.types.Operator):
    bl_idname = "render.apply_unit_to_px"
    bl_label = "Apply Unit to Pixel"
    bl_options = {'UNDO'}

    def execute(self, context):
        s = context.scene
        
        # Direct assignment via tuple unpacking
        s.render.resolution_x, s.render.resolution_y = calculate_res(s)
        
        self.report({'INFO'}, f"Resolution set to {s.render.resolution_x}x{s.render.resolution_y}")
        return {'FINISHED'}

# Registration
classes = (
    RENDER_PT_unit_to_px,
    RENDER_OT_apply_unit_to_px,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
    bpy.types.Scene.unit_selection = bpy.props.EnumProperty(
        name="Unit", 
        items=[(k, v[0], "") for k, v in UNIT_DATA.items()], 
        default='MM'
    )
    bpy.types.Scene.unit_width = bpy.props.FloatProperty(name="Width", default=210.0, min=0.001)
    bpy.types.Scene.unit_height = bpy.props.FloatProperty(name="Height", default=297.0, min=0.001)
    bpy.types.Scene.render_ppi = bpy.props.IntProperty(name="PPI", default=300, min=1)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.unit_selection
    del bpy.types.Scene.unit_width
    del bpy.types.Scene.unit_height
    del bpy.types.Scene.render_ppi

if __name__ == "__main__":
    register()
