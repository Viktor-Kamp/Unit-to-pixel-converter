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

def get_unit_items():
    return [(key, name, "") for key, (name, _) in UNIT_DATA.items()]

def unit_to_px(width, height, ppi, unit):
    name, factor = UNIT_DATA.get(unit, (None, 1.0))
    
    px_x = int(width / factor * ppi)
    px_y = int(height / factor * ppi)
    return px_x, px_y

# UI
class RENDER_PT_unit_to_px(bpy.types.Panel):
    bl_label = "Unit to pixel converter"
    bl_idname = "RENDER_PT_unit_to_px"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "output"

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
        px_x, px_y = unit_to_px(
            s.unit_width,
            s.unit_height,
            s.render_ppi,
            s.unit_selection,
        )
        
        box = layout.box()
        box.label(text=f"Preview: {px_x} x {px_y} px", icon='INFO')
        
        layout.operator("render.apply_unit_to_px", text="Apply resolution", icon='CHECKMARK')

# Operator
class RENDER_OT_apply_unit_to_px(bpy.types.Operator):
    bl_idname = "render.apply_unit_to_px"
    bl_label = "Apply Unit to Pixel"
    bl_description = "Sets the render resolution based on the units and PPI above"

    def execute(self, context):
        s = context.scene
        
        px_x, px_y = unit_to_px(
            s.unit_width,
            s.unit_height,
            s.render_ppi,
            s.unit_selection,
        )

        s.render.resolution_x = px_x
        s.render.resolution_y = px_y

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
        items=get_unit_items(),
        default='MM'
    )

    bpy.types.Scene.unit_width = bpy.props.FloatProperty(
        name="Width",
        default=210.0,
        min=0.001
    )

    bpy.types.Scene.unit_height = bpy.props.FloatProperty(
        name="Height",
        default=297.0,
        min=0.001
    )

    bpy.types.Scene.render_ppi = bpy.props.IntProperty(
        name="PPI",
        default=300,
        min=1
    )

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.unit_selection
    del bpy.types.Scene.unit_width
    del bpy.types.Scene.unit_height
    del bpy.types.Scene.render_ppi
