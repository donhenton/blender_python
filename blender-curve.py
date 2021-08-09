
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
    FloatVectorProperty,
    FloatProperty,
    PointerProperty, # need to be able to access the *global* values
    )

from bpy.types import (
    Panel,
    Operator,
    PropertyGroup, # store values *globally* here
    )

class Twisty_Curve():

    def __init__(self):
        self.seed = 0
        self.twists = 20
        self.sizer = (2, 2, 3)
        self.extrude = 0.125
        self.bevel = 0.125
        self.tapers = 3
        self.curve = None

    def resize(self):
        # self.curve.select_set(True)
        self.curve.scale = self.sizer
        self.curve.data.extrude = self.extrude
        self.curve.data.bevel_depth = self.bevel
        self.curve.data.resolution_u = 20
        self.curve.data.render_resolution_u = 32

    def draw(self):
        bpy.ops.curve.primitive_bezier_circle_add(radius=1.0,
                                            location=(0.0, 0.0, 0.0),
                                            enter_editmode=True)

        bpy.ops.curve.subdivide(number_cuts=self.twists)
        bpy.ops.transform.vertex_random(
            offset=1.0,
            uniform=0.1,
            normal=0.0,
            seed=self.seed,
            )
        bpy.ops.object.mode_set(mode='OBJECT')
        self.curve = bpy.context.active_object
        obj_data = self.curve.data
        self.resize()

        # Store a shortcut to the curve object's data.
        obj_data.fill_mode = 'FULL'

        # Create bevel control curve.

        bpy.ops.curve.primitive_bezier_circle_add(
            radius=0.25, enter_editmode=True)
        bpy.ops.curve.subdivide(number_cuts=4)
        bpy.ops.transform.vertex_random(
            offset=1.0,
            uniform=0.1,
            normal=1.0,
            seed=self.seed
            )
        bevel_control = bpy.context.active_object
        bevel_control.data.name = bevel_control.name = 'Bevel Control'
        obj_data.bevel_object = bevel_control
        bpy.ops.object.mode_set(mode='OBJECT')
        bevel_control.hide_viewport = True

        # Create taper control curve.
        bpy.ops.curve.primitive_bezier_curve_add(enter_editmode=True)
        bpy.ops.curve.subdivide(number_cuts=self.tapers)
        bpy.ops.transform.vertex_random(
            offset=1.0,
            uniform=0.1,
            normal=1.0,
            seed=self.seed
            )
        taper_control = bpy.context.active_object
        taper_control.data.name = taper_control.name = 'Taper Control'
        taper_control.hide_viewport = True

        # Set the main curve's taper control to the taper control curve.
        obj_data.taper_object = taper_control
        bpy.ops.object.mode_set(mode='OBJECT')

tc = Twisty_Curve()
def update_twist(self, context):
    tc.twists = self.twist_knob
    tc.tapers = self.taper_knob
    tc.bevel = self.bevel_knob
    tc.seed = self.seed_knob
    tc.sizer = self.sizer_knob
    tc.extrude = self.extrude_knob
    tc.resize()

class WM_OT_Twisty_Curve(Operator):
    bl_label = "draw a twisty curve"
    bl_idname = "wm.draw_a_twisty_curve"

    def execute(self, context):
        tc.draw()
        return {'FINISHED'}

class WM_OT_Delete_Curves(Operator):
    bl_label = "clear  curves"
    bl_idname = "wm.delete_my_curves"

    def execute(self, context):
        for thing in ['CURVE', 'MESH']:
            bpy.ops.object.select_by_type(type=thing)
            bpy.ops.object.delete(use_global=False, confirm=False)
        return {'FINISHED'}

class Knob_Values(PropertyGroup):

    twist_knob: IntProperty(
        name = "Number of Twists",
        description="Number of Twists",
        default = 16,
        min = 0,
        max = 100,
        update=update_twist,
        )

    taper_knob: IntProperty(
        name = "Number of Tapers",
        description="Number of Tapers",
        default = 3,
        min = 0,
        max = 100,
        update=update_twist,
        )

    extrude_knob: FloatProperty(
        name = "Extrusion Amount",
        description="Curve Thickness",
        default = .1,
        min = 0,
        max = 10,
        update=update_twist,
        )

    bevel_knob: FloatProperty(
        name = "Bevel Amount",
        description="Beveliicious",
        default = .1,
        min = -1,
        max = 1,
        update=update_twist,
        )


    seed_knob: IntProperty(
        name = "Random Seed",
        description="Random Seed",
        default = 0,
        min = 0,
        max = 1000,
        update=update_twist,
        )

    sizer_knob: FloatVectorProperty(
        name = "Sizing Vector",
        description = "Sizing Vector",
        default = (2, 2, 3),
        min = 0.01,
        max = 100.0,
        update=update_twist,
        )

class OBJECT_PT_Knob_Panel(Panel):
    bl_label = "Twisty Curve"
    bl_idname = "OBJECT_PT_twisty_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "More Tools"
    bl_context = "objectmode"

    def draw(self, context): # note that here we are accessing the instance
        layout = self.layout
        values = context.scene.knob_values
        layout.prop(values, "twist_knob")
        layout.prop(values, "taper_knob")
        layout.prop(values, "sizer_knob")
        layout.prop(values, "extrude_knob")
        layout.prop(values, "bevel_knob")
        layout.prop(values, "seed_knob")
        layout.operator("wm.draw_a_twisty_curve")
        layout.operator("wm.delete_my_curves")

knob_classes = (
    Knob_Values,
    WM_OT_Twisty_Curve,
    WM_OT_Delete_Curves,
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
