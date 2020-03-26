import ClientAPI

CompassDecal = None
CompassOn = False
LastX = 0
LastZ = 0

def MoveHandler(pos, orient, scale):
    global CompassDecal
    global CompassOn
    
    global LastX
    global LastZ
    if CompassOn:
        x = pos.x
        z = pos.z
        if LastX != x or LastZ != z:
            #ClientAPI.DebugWrite('updating compass: ' + str(x) + ', ' + str(z))
            CompassDecal.PosX = x
            CompassDecal.PosZ = z
            LastX = x
            LastZ = z
        
def ShowCompass():
    global CompassDecal
    global CompassOn
    player = ClientAPI.GetPlayerObject()
    player.SceneNode.RegisterEventHandler('Updated', MoveHandler)
    CompassDecal = ClientAPI.Decal.Decal("compass-rose.png", player.Position.x, player.Position.z, 2000, 2000, 5)
    CompassOn = True
	
def HideCompass():
    global CompassDecal
    global CompassOn
    player = ClientAPI.GetPlayerObject()
    player.SceneNode.RemoveEventHandler('Updated', MoveHandler)
    CompassDecal.Dispose()
    CompassDecal = None
    CompassOn = False
	
def ToggleCompass():
    global CompassOn
    if CompassOn :
        HideCompass()
    else:
        ShowCompass()
