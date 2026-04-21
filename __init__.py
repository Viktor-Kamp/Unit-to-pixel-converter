import bpy

bl_info = {
    "name": "Unit to pixel converter",
    "author": "Viktor Kamp",
    "version": (1, 1, 0),
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

# Calculates pixel dimensions based on scene properties
def calculate_res(scene):
    _, factor = UNIT_DATA.get(scene.unit_selection, ("Inch", 1.0))
    px_x = int(scene.unit_width / factor * scene.render_ppi)
    px_y = int(scene.unit_height / factor * scene.render_ppi)
    return px_x, px_y

# Converts input values, when unit is changed
def update_unit_conversion(self, context):
    old_unit = self.get("old_unit_selection", 'MM')
    new_unit = self.unit_selection
    
    if old_unit is not None and old_unit != new_unit:
        old_factor = UNIT_DATA[old_unit][1]
        new_factor = UNIT_DATA[new_unit][1]
        
        self.unit_width = (self.unit_width / old_factor) * new_factor
        self.unit_height = (self.unit_height / old_factor) * new_factor
        
    self["old_unit_selection"] = new_unit

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
        layout.use_property_decorate = False 
        
        s = context.scene

        col = layout.column(align=True)
        col.prop(s, "unit_selection", text="Unit")
        col.separator()
        col.prop(s, "unit_width")
        col.prop(s, "unit_height")
        col.prop(s, "render_ppi")
        
        px_x, px_y = calculate_res(s)

        sub = layout.column()
        sub.use_property_split = False
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
        
        if hasattr(s.render, "ppm_factor"):
            s.render.ppm_base = 0.0254 
            s.render.ppm_factor = float(s.render_ppi)
            
        if hasattr(s.render, "pixel_density"):
            s.render.pixel_density = s.render_ppi

        self.report({'INFO'}, f"Resolution: {res_x}x{res_y} px | {s.render_ppi} PPI angewandt")
        return {'FINISHED'}

# Registration
classes = (RENDER_PT_unit_to_px, RENDER_OT_apply_unit_to_px)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
    bpy.types.Scene.unit_selection = bpy.props.EnumProperty(
        name="Unit", 
        items=[(k, v[0], "") for k, v in UNIT_DATA.items()], 
        default='MM',
        update=update_unit_conversion
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
