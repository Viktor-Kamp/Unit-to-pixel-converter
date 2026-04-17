import bpy

bl_info = {
    "name": "Unit to pixel converter",
    "author": "Viktor Kamp",
    "version": (1, 0, 1),
    "blender": (4, 2, 0),
    "location": "Properties > Output > Unit to pixel",
    "description": "Calculates render resolution from different units, including inch, centimeter or millimeter.",
    "category": "Render",
}

class RENDER_PT_unit_to_px(bpy.types.Panel):
    bl_label = "Unit to pixel converter"
    bl_idname = "RENDER_PT_unit_to_px"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "output"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        col = layout.column(align=True)
        col.prop(scene, "unit_selection", text="Unit")
        col.separator()
        col.prop(scene, "unit_width", text="Width")
        col.prop(scene, "unit_height", text="Height")
        col.prop(scene, "render_ppi", text="PPI")
        
        unit = scene.unit_selection
   
        if unit == 'MM': factor = 25.4
        elif unit == 'CM': factor = 2.54
        elif unit == 'BANANA': factor = 25.4 / 178.0
        else: factor = 1.0
        
        px_x = int((scene.unit_width / factor) * scene.render_ppi)
        px_y = int((scene.unit_height / factor) * scene.render_ppi)
        
        box = layout.box()
        box.label(text=f"Preview: {px_x} x {px_y} px", icon='INFO')
        
        layout.operator("render.apply_unit_to_px", text="Apply resolution", icon='CHECKMARK')

class RENDER_OT_apply_unit_to_px(bpy.types.Operator):
    bl_idname = "render.apply_unit_to_px"
    bl_label = "Apply Unit to Pixel"
    bl_description = "Sets the render resolution based on the units and PPI above"

    def execute(self, context):
        s = context.scene
        unit = s.unit_selection
        
        if unit == 'MM': factor = 25.4
        elif unit == 'CM': factor = 2.54
        elif unit == 'BANANA': factor = 25.4 / 178.0
        else: factor = 1.0

        s.render.resolution_x = int((s.unit_width / factor) * s.render_ppi)
        s.render.resolution_y = int((s.unit_height / factor) * s.render_ppi)
        return {'FINISHED'}

def register():
    bpy.types.Scene.unit_selection = bpy.props.EnumProperty(
        items=[
            ('MM', "Millimeter", ""), 
            ('CM', "Centimeter", ""), 
            ('INCH', "Inch", ""),
            ('BANANA', "Banana", "")
        ],
        default='MM'
    )
    bpy.types.Scene.unit_width = bpy.props.FloatProperty(name="Width", default=210.0, min=0.001)
    bpy.types.Scene.unit_height = bpy.props.FloatProperty(name="Height", default=297.0, min=0.001)
    bpy.types.Scene.render_ppi = bpy.props.IntProperty(name="PPI", default=300, min=1)
    
    bpy.utils.register_class(RENDER_PT_unit_to_px)
    bpy.utils.register_class(RENDER_OT_apply_unit_to_px)

def unregister():
    bpy.utils.unregister_class(RENDER_PT_unit_to_px)
    bpy.utils.unregister_class(RENDER_OT_apply_unit_to_px)
    del bpy.types.Scene.unit_selection
    del bpy.types.Scene.unit_width
    del bpy.types.Scene.unit_height
    del bpy.types.Scene.render_ppi
