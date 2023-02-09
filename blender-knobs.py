
bl_info = {
    "name": "Blender Knobs",
    "description": "Example of setting and using some float/integer values",
    "author": "Scott James",
    "version": (0, 0, 1),
    "blender": (2, 92, 0),
    "location": "3D View > Tools",
    "warning": "", # used for warning icon and text in addons panel
    "wiki_url": "https://blender.stackexchange.com/questions/57306/how-to-create-a-custom-ui/57332#57332",
    "tracker_url": "",
    "category": "Development"
}

import bpy

from bpy.props import (
    IntProperty,
    FloatProperty,
    PointerProperty, # need to be able to access the *global* values
    )

from bpy.types import (
    Panel,
    Operator,
    PropertyGroup, # store values *globally* here
    )

class Knob_Values(PropertyGroup):

    # Panels cannot have properties!  Otherwise we wouldn't need this
    # This makes a global container which stores the value

    int_knob: IntProperty(
        name = "An Integer",
        description="An integer",
        default = 2,
        min = 1,
        max = 100,
        )

    float_knob: FloatProperty(
        name = "A Float",
        description = "A float",
        default = 2.,
        min = 0.01,
        max = 100.0
        )

class OBJECT_PT_Knob_Panel(Panel):
    bl_label = "Knobs"
    bl_idname = "OBJECT_PT_knob_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "More Tools"
    bl_context = "objectmode"

    @classmethod
    def poll(cls, context): # need this else it will not fire
        return context.object is not None

    def draw(self, context): # note that here we are accessing the instance
        layout = self.layout
        values = context.scene.knob_values
        layout.prop(values, "float_knob", slider=True)
        layout.prop(values, "int_knob")

knob_classes = (
    Knob_Values,
    OBJECT_PT_Knob_Panel,
)

def register():
    for cls in knob_classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.knob_values = PointerProperty(type=Knob_Values)

def unregister():
    for cls in reversed(knob_classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.knob_values # because we created it above

if __name__ == "__main__":
    register()
