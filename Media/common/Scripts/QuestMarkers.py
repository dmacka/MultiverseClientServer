import ClientAPI

questMarkers = {}
QuestSocket     = "questavailable"
ConcludableMesh = "question.mesh"
AvailableMesh   = "exclamation.mesh"
    
def RemoveMarker(worldObj):
    # if there is a quest marker, remove it from the object
    # ClientAPI.DebugWrite("QuestMarkers:RemoveMarker: Name = " + worldObj.Name + ", OID = " + str(worldObj.OID))
    marker = questMarkers[worldObj.OID]
    if not marker is None:
        # ClientAPI.DebugWrite("QuestMarkers:RemoveMarker: Removing " + marker.Name)
        worldObj.DetachObject(marker)
        marker.Dispose()
        
    questMarkers[worldObj.OID] = None
    
def AddMarker(worldObj, markerMeshName):
    global QuestSocket
    # ClientAPI.DebugWrite("QuestMarkers:AddMarker: Name = " + worldObj.Name + ", OID = " + str(worldObj.OID) + ", mesh = " + markerMeshName)
    marker = questMarkers[worldObj.OID]
    if not marker is None:
        ClientAPI.DebugWrite("QuestMarkers: attempt to add a marker when one is already present")
    
    marker = ClientAPI.Model.Model("marker." + str(worldObj.OID), markerMeshName)
    worldObj.AttachObject(QuestSocket, marker)
    questMarkers[worldObj.OID] = marker

def PropertyChangeHandler(worldObj, propName):
    global ConcludableMesh
    global AvailableMesh
    if propName == "questavailable" or propName == "questconcludable":
        questAvailable = worldObj.CheckBooleanProperty('questavailable')
        questConcludable = worldObj.CheckBooleanProperty('questconcludable')
        
        # remove any previous marker
        RemoveMarker(worldObj)
        
        # if we need a marker now, add it
        if questConcludable:
            AddMarker(worldObj, ConcludableMesh)
        elif questAvailable:
            AddMarker(worldObj, AvailableMesh)

# This function is an event handler that runs when the world has been initialized.
def ObjectAddedHandler(worldObj):
    if worldObj.ObjectType == ClientAPI.WorldObject.WorldObjectType.Npc:
        # ClientAPI.DebugWrite("QuestMarkers: added npc object")
        
        questMarkers[worldObj.OID] = None
        
        # register event handlers for object
        worldObj.RegisterEventHandler('PropertyChange', PropertyChangeHandler)
               
        # ClientAPI.DebugWrite("QuestMarkers: Registered npc event handlers")
        
def ObjectRemovedHandler(worldObj):
    if worldObj.ObjectType == ClientAPI.WorldObject.WorldObjectType.Npc:
        #ClientAPI.DebugWrite("QuestMarkers: removing object")

        # Remove the marker from the object
        RemoveMarker(worldObj)
            
        # now remove the marker from our dictionary
        del questMarkers[worldObj.OID]
        
        # remove event handlers for object
        worldObj.RemoveEventHandler('PropertyChange', PropertyChangeHandler)

# Register an event handler that will run when the world has been initialized.
ClientAPI.World.RegisterEventHandler('ObjectAdded', ObjectAddedHandler)
ClientAPI.World.RegisterEventHandler('ObjectRemoved', ObjectRemovedHandler)
