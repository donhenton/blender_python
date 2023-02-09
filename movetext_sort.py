import bpy
from random import randrange
import math

rowCount =10
columnCount = 18
endFrame = 40
startFrame = 1
itemWidth = .1
itemHeight = .1
emptyLocation = bpy.data.objects["Empty"].location
print(emptyLocation)



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
selectCollection

select a Collection via selecting its wrapping
LayerCollection

Parameters:
    collectionName: name of the collection
 
'''
 
def selectCollection(collectionName):
    # get the current collection's wrapping layer collection
    layer_collection = bpy.context.view_layer.layer_collection
    # layer collections wrap collections you need to find the layer collection
    # that wraps your item to set it active

    piecesLayer = recurLayerCollection(layer_collection,collectionName) 
    
    # make active
    bpy.context.view_layer.active_layer_collection = piecesLayer
    return piecesLayer.collection

def setUp(stuffCollection,stuffCount):
#    context = bpy.context
#    for ob in context.selected_objects:
#        ob.animation_data_clear()
    bpy.ops.screen.frame_jump(end=True)     
    for k in range(0,stuffCount):
        ob = stuffCollection.all_objects[k]
        ob.animation_data_clear()

 
# https://blender.stackexchange.com/questions/260149/set-keyframe-interpolation-constant-while-setting-a-keyframe-in-blender-python 
 
def setConstantAction(t,idx):
    my_action = bpy.data.actions.get(t.animation_data.action.name)
    my_fcu = my_action.fcurves.find("location", index=idx)
    for pt in my_fcu.keyframe_points:
        pt.interpolation = 'BACK'


def main():
    # in console bpy.data.collections['stuff'].objects['Cube']
   
    
    col = selectCollection('parts') 
    
    stuffCollection = []
    
    for k in col.all_objects:
        stuffCollection.append(k)
    
    
    def sortFunc(o):
        ee = (emptyLocation[0] - o.location[0]) * (emptyLocation[0] - o.location[0])
        ee = ee + (emptyLocation[1] - o.location[1]) * (emptyLocation[1] - o.location[1])
        ee = math.sqrt(ee)
        
        return ee
    
    
    stuffCollection.sort(key=sortFunc)
    
    stuffCount = len(col.all_objects)
    setUp(col,stuffCount)
    debugit = "frame is {0:d} add is [{1:.2f},{2:.2f},{3:.2f}]"
    dirValue = 1
    
    
    #lock values at last frame
          
    for k in range(0,stuffCount):
        thg = stuffCollection[k]     
        thg.keyframe_insert(data_path="location", frame=endFrame)
        thg.keyframe_insert(data_path="rotation_euler",frame=endFrame)   
            
    
    
    
    for k in range(0,stuffCount):
        
        thg = stuffCollection[k]
        print(thg.name)
    
        bpy.data.objects[thg.name].select_set(True)  
        bpy.context.view_layer.objects.active = thg
         
        if (k % 2) == 0:
            dirValue = 1
        else:
            dirValue = -1
            
        dirValue = 1   
            
        
       #S thg.location[1] = thg.location[1] +(dirValue *(rowCount) *  itemHeight) *.4 #comment out
        thg.location[0] = thg.location[0] + dirValue * ( 3 * (k /stuffCount)) +.5
        thg.rotation_euler[1] = (3.1415*2) / ((stuffCount -k)/stuffCount) 
       # thg.rotation_euler[2] = thg.rotation_euler[2] + (randrange(2))  # comment out
       # thg.rotation_euler[2] = thg.rotation_euler[2] * dirValue # comment out
        thg.keyframe_insert(data_path="location", frame=1)
        thg.keyframe_insert(data_path="rotation_euler",frame=1)
        setConstantAction(thg,0)
        bpy.data.objects[thg.name].select_set(False) 
      
         
    

main()
    