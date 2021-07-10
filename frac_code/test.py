import bpy
from math import  pi

FRAME_COUNT = 250
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


def addDriver(obj):
    
    A = 1 # amplitude
    P = 0.2 
    
    # A*sin((2*PI()/P)*((current_frame/FRAME_COUNT))+P)+V
   # drv_exp = "{0:.2f} * cos(tau * ({1} - {2}) / ({3} - {2} + 1))"
    drv_exp = "{0:.2f} * sin((2*{0:4f}/{0:.4f})*((  ))"
  #  return drv_exp.format(A,pi,P



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
    bpy.ops.object.add_fracture_cell_objects( source_limit=125,)
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

    print(piecesCollection)
    #jj = range(0,10)

    #for k in jj:
        #print(piecesCollection.all_objects[k].location[0])
 
 




main()

