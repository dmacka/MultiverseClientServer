import ClientAPI

displayGroups = { }

shownGroups = {}

def HideDisplayGroup(groupName):
    shownGroups[groupName] = False
    for worldObj in displayGroups[groupName]:
        worldObj.Model.IsVisible = False

def ShowDisplayGroup(groupName):
    shownGroups[groupName] = True
    for worldObj in displayGroups[groupName]:
        worldObj.Model.IsVisible = True
        
def SetDisplayGroup(newGroupName):
    if newGroupName is None:
        for groupName in displayGroups.keys():
            ShowDisplayGroup(groupName)
    else:
        for groupName in displayGroups.keys():
            if groupName == newGroupName:
                ShowDisplayGroup(groupName)
            else:
                HideDisplayGroup(groupName)

def SetDisplayGroups(newGroups):
    for groupName in displayGroups.keys():
        if groupName in newGroups:
            ShowDisplayGroup(groupName)
        else:
            HideDisplayGroup(groupName)
                
def RemoveFromDisplayGroups(worldObj):
    for groupName in displayGroups.keys():
        if worldObj in displayGroups[groupName]:
            displayGroups[groupName].remove(worldObj)
            worldObj.Model.IsVisible = True
            
def ObjectDisposedHandler(worldObj):
    RemoveFromDisplayGroups(worldObj)

def DisplayGroupHandler(sender, args):
    worldObj = ClientAPI.World.GetObjectByOID(args.Oid)
    RemoveFromDisplayGroups(worldObj)
    displayGroup = worldObj.GetProperty('DisplayGroup')
    if not displayGroup is None:
        if not displayGroup in displayGroups:
            displayGroups[displayGroup] = []
            shownGroups[displayGroup] = True
        displayGroups[displayGroup].append(worldObj)
        # if the object is in a hidden group, hide it
        if not shownGroups[displayGroup]:
            worldObj.Model.IsVisible = False
        worldObj.RegisterEventHandler('Disposed', ObjectDisposedHandler)
    
ClientAPI.World.RegisterObjectPropertyChangeHandler("DisplayGroup", DisplayGroupHandler)
