import bpy



'''
Collection Handling Routines
'''


'''
recurLayerCollection
 
Recursively transverse layer_collection for a particular name

Parameters --
layerColl: the layer collection to use as the start point 
collName: collection name you are searching for
'''
def recurLayerCollection(layerColl, collName):
    found = None
    if (layerColl.name == collName):
        return layerColl
    for layer in layerColl.children:
        found = recurLayerCollection(layer, collName)
        if found:
            return found
        
'''
selectLayer

select the pieces Collection via selecting its wrapping
LayerCollection

Parameters --
layerName: name of the layer you wish to select

Returns: --
a reference to the layerCollection ref.collection is the 
wrapped collection
 
'''
 
def selectLayer(layerName):
    # get the current collection's wrapping layer collection
    layer_collection = bpy.context.view_layer.layer_collection
    # layer collections wrap collections you need to find the layer collection
    # that wraps your item to set it active

    piecesLayer = recurLayerCollection(layer_collection,layerName) 
    
    # make active
    bpy.context.view_layer.active_layer_collection = piecesLayer
    return piecesLayer

'''
removes all meshes, objects and collections
'''
def removeAll():
    
    
    for m in bpy.data.meshes:
        #print(m.name)
        bpy.data.meshes.remove(m)
    
    for o in bpy.data.objects:
        #print(o.name)
        bpy.data.objects.remove(o)
    
    
    
    for c in bpy.data.collections:
        #print(c.name)
        bpy.data.collections.remove(c)   
'''
addLayer Collection

Parameters: --
layerName the name of the layer wrapper

Returns: --
a reference to the layerCollection ref.collection is the 
wrapped collection

'''
def addLayerCollection(layerName):
    lv = bpy.data.collections.new(name=layerName)
    bpy.context.scene.collection.children.link(lv)
    return lv
'''
def main():

    removeAll()
    
    layerName = "pieces"
    addLayerCollection(layerName)
    piecesLayer= selectLayer(layerName) 

    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    main_sphere = bpy.context.active_object
    
    

#    addLayerCollection(layerName)
    
    
    

main()

'''