import ClientAPI

CompassDecal = None

def UpdateCompassPosition():
	global CompassDecal
	if CompassDecal != None :
		CompassDecal.PosX = ClientAPI.GetPlayerObject().Position.x
		CompassDecal.PosZ = ClientAPI.GetPlayerObject().Position.z
		
def ShowCompass():
	global CompassDecal
	playerPos = ClientAPI.GetPlayerObject().Position
	CompassDecal = ClientAPI.Decal.Decal("compass-rose.png", playerPos.x, playerPos.z, 2000, 2000, 0, 0, 0, 5)
	
def HideCompass():
	global CompassDecal
	if CompassDecal is not None:
		CompassDecal.Dispose()
	CompassDecal = None
	
def ToggleCompass():
	global CompassDecal
	if CompassDecal == None :
		ShowCompass()
	else:
		HideCompass()
		
		
