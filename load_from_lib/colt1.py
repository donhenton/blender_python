# https://www.youtube.com/watch?v=XqX5wh4YeRw

import bpy
from math import radians

bpy.ops.mesh.primitive_cube_add()
currentObj = bpy.context.active_object

#move_object
currentObj.location = [ 1,3,0]

degrees =  45

currentObj.rotation_euler[1] += radians(degrees)

mod_subsurf = currentObj.modifiers.new("sub1", 'SUBSURF')
mod_subsurf.levels = 2

#smooth the object
#bpy.ops.object.shade_smooth()


#loop thru the faces
mesh = currentObj.data
# same as currentObj.data.polygons
print(len(mesh.polygons)) 
ctr = 0
for face in currentObj.data.polygons:
    ctr += 1
    if ctr % 2 == 0:
        face.use_smooth = True
        print(ctr)
    
#create a disp_modifier

mod_displace = currentObj.modifiers.new("disp1",'DISPLACE');

new_tex = bpy.data.textures.new("mytex",'DISTORTED_NOISE')    

#    bpy.ops.mesh.delete(type='FACE')
#https://docs.blender.org/api/current/bpy.types.Texture.html

new_tex.noise_scale = 2.0
mod_displace.texture = new_tex