import bpy
from math import  pi

FRAME_COUNT = 250
CELL_COUNT = 200
#####################################################################################


#Recursively transverse layer_collection for a particular name
def recurLayerCollection(layerColl, collName):
    found = None
    if (layerColl.name == collName):
        return layerColl
    for layer in layerColl.children:
        found = recurLayerCollection(layer, collName)
        if found:
            return found


def addDriverExp(xyzIdx,mesh_obj):
    
    var = mesh_obj.location[xyzIdx]
    FRAME_COUNT = 250
    A = 1.5 # amplitude
    P = 0.2 #period
    Ps = 0 # phase shift
    Vs = 3.0 #vertical shift
    periodCalc = 2*pi/P
   
    
    # A*sin((2*PI()/P)*((current_frame/FRAME_COUNT))+Ps)+Vs

    
   
    drv_exp = "{0:.2f} *( {1:.2f}* sin({2:.4f}*((frame/{3:1f}  ))+{4:2f})+{5:2f})"
    
   # 
    ee = drv_exp.format(var,A,periodCalc,FRAME_COUNT,Ps,Vs)
    print(ee)
    x_curve = mesh_obj.driver_add("location",xyzIdx)
    x_curve.driver.expression =ee



def selectPiecesLayer():
    layer_collection = bpy.context.view_layer.layer_collection
    # layer collections wrap collections you need to find the layer collection
    # that wraps your item to set it active

    piecesLayer = recurLayerCollection(layer_collection,"pieces")
    bpy.context.view_layer.active_layer_collection = piecesLayer
    return piecesLayer.collection

#create the layers
def createFragments():
       #create the sphere
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

    main_sphere = bpy.context.active_object
    main_mesh = main_sphere.data
    mat = bpy.data.materials.new(name="Material")
    mat.diffuse_color = [0.0, 0.5, 1.0, 1.0]
    main_mesh.materials.append(mat)


    bpy.context.active_object.name = 'pt'
   

    # use the interactive window and tab to get the params
    bpy.ops.object.add_fracture_cell_objects( source_limit=CELL_COUNT,)
    bpy.ops.object.select_all(action='DESELECT')
    #select the original sphere and delete it
    bpy.data.objects[main_sphere.name].select_set(True)  
    bpy.context.view_layer.objects.active = main_sphere
    bpy.ops.object.delete()

#main_sphere is dead now
#pieces collection is active


def main():
    
    
    pieces = bpy.data.collections.new(name="pieces")
    bpy.context.scene.collection.children.link(pieces)
    piecesCollection= selectPiecesLayer() 
    



    createFragments()
    jj = range(0,CELL_COUNT)
    dataRange = range(0,3)
    

    for k in jj:
         for z in dataRange:
            addDriverExp(z,piecesCollection.all_objects[k])
         



main()

