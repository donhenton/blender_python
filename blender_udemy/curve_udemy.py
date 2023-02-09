import bpy




#-----------------------------------------
#   Create Material for the Curves
#-----------------------------------------
def createMaterials():
    # This list holds RGB color values
    color_list = [[0.8, 0.0, 0.04, 1.0],[0.234259, 0.8, 0.098736, 1.0],
    [0.076, 0.883, 0.906, 1.0],[0.017, 0.8, 0.0, 1.0]]

    mats = []
    iterator = 0
     
    # Test to see if a material already exists with this name
    curveMaterial = bpy.data.materials.get("M_curve_line")
 
    if curveMaterial is None:
        curveMaterial = bpy.data.materials.new(name="M_curve_line")
 
    # Set the use nodes argument True
    # This lets us change the surface type
    curveMaterial.use_nodes = True
 
    # For loop to check for any nodes and delete them
    curveNodes = curveMaterial.node_tree.nodes
    for node in curveNodes:
        curveNodes.remove(node)
 
    # Create a fresh output node
    mat_output = curveNodes.new(type="ShaderNodeOutputMaterial")
   
 
    # Create a new variable and assign it to the new material node
    emissionType = curveMaterial.node_tree.nodes.new("ShaderNodeEmission")
 
    # Set the color of the new material
    # NOTE: We use the iterator to cycle through different colors
    emissionType.inputs[0].default_value = (color_list[iterator])
 
    # Set the emission strength to a specified value
    emissionType.inputs[1].default_value = 20
 
    # Link the emission shader to the material
    # This is like drawing the line between
    # the boxes in the shader menu
    curveMaterial.node_tree.links.new(mat_output.inputs[0], emissionType.outputs[0])
    mats.append(curveMaterial)
 
    # Increase the iterator by one
    # so the next curve that gets created uses the next color set
    iterator += 1
#    
    for z in range(1,4):
         mat_temp = curveMaterial.copy()
         s = "zz_{a:2d}"
         mats.append(mat_temp)
         mat_temp.name = s.format(a=z)
        # if z == 0:
        #    mat_temp.name =  "M_crv_line"
       #  else :    
       #    
         emissionType.inputs[0].default_value = (color_list[z]) #set color  
      
    return mats
   
 
#-----------------------------------------
#   Create Lists to Store Values
#-----------------------------------------
 
# List of curviness coordinates for each curve. They will all be shaped the same
# They will just have different positions in space which we tweak elsewhere
coords_list = [[12,2,5],[9,6,4],[8,1,3],[0,4,2],[-7,-16,1]]
 
# This will hold our curves
curveList = [] # we will append curves into this list as we make them
 
 
mats = createMaterials() 
 
 
 
# For loop that creates four curves
for eachObjIdx in range(0,4):
    
   
    
    # Create a new curve to the main database
    theCurveObject = bpy.data.curves.new('CurveObject', 'CURVE')
 
    # Access the "3d" setting for the curve and ensure its 3d
    theCurveObject.dimensions = "3D"
 
    # Add a new spline to the curve. By default, it has 1 POINT
    splineObject = theCurveObject.splines.new(type='NURBS')
 
    # Add more points to this spline...enough for our list of coordinates
    # Since it already has one, we need one-less-than the length of our list
    splineObject.points.add(len(coords_list)-1)
 
    # Apply the curve coordinates to the curve
    # Remember, this isn't affecting the "position" of the curve object
    # Just the shape of it
    for vert in range(len(coords_list)):
        x,y,z = coords_list[vert]
        splineObject.points[vert].co = (x,y,z, 1) # the '1' is the "W" value (weight). re: "Soft physics"
        
    # Make a new object with the curve
    curve_obj = bpy.data.objects.new('crv_line', theCurveObject)
 
    # Link the curve object to the scene collection
    bpy.context.scene.collection.objects.link(curve_obj)
 
    # Make the curve the active object
    # When it was created, it was de-selected :S
    bpy.context.view_layer.objects.active = curve_obj
 
    # I want to append in any curve we create
    # so we can iterate over them later
    curveList.append(curve_obj)
    
    curve_obj.active_material = mats[eachObjIdx]
 
## Iterate through the curve list and
    ## moves each curve .05 relative to its x position
    for obj in curveList:
        obj.location.x +=0.5
 
    ## Give it some thickness    
    bpy.context.object.data.bevel_depth = 0.02
 
#-----------------------------------------
#   Setup the animation
#-----------------------------------------
 
    ## Sets the current frame to start of timeline
    bpy.context.scene.frame_set(1)
 
    ## Access devel data and set factor to 1
    ## This is the "bevel depth" variable
    bpy.context.object.data.bevel_factor_start = 1
 
    ## Access the object data of active object and
    ## place a key frame on its bevel start value
    bpy.context.object.data.keyframe_insert(data_path='bevel_factor_start')
 
    ## This is the end of our animation; frame 50
    bpy.context.scene.frame_set(50)
 
    bpy.context.object.data.bevel_factor_start = 0
    bpy.context.object.data.keyframe_insert(data_path='bevel_factor_start')
 
    ## Set the frame range on the timeline
    bpy.context.scene.frame_end = 50
 


 
# Make the background black
bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (0, 0, 0, 1)