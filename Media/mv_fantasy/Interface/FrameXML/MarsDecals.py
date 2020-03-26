import ClientAPI

import MarsTarget

CompassDecal = None
CurrentTarget = None
TargetDecal = None
PlayerPosition = None
LastFootstepPosition = None
FootPrintSide = 0

def DecalFrame_OnLoad(frame):
    frame.RegisterEvent("PLAYER_TARGET_CHANGED")
    
def UpdateFootsteps():
    global PlayerPosition
    global LastFootstepPosition
    global FootPrintSide
    if ClientAPI.GetPlayerObject() == None:
        return
    PlayerPosition = ClientAPI.GetPlayerObject().Position
    if LastFootstepPosition == None :
        LastFootstepPosition = PlayerPosition 
    Distance = PlayerPosition - LastFootstepPosition
    if Distance.LengthSquared > 1000000.0 :
        pitch, yaw, roll = ClientAPI.GetPlayerObject().Orientation.ToEulerAnglesInDegrees()
        Rotation = yaw + 180
        if Rotation > 360 :
            Rotation = Rotation - 360
        if FootPrintSide == 0 :
            FootPrintImage = "footprint-left-25.png"
            FootPrintSide = 1
        else :
            FootPrintImage = "footprint-right-25.png"
            FootPrintSide = 0
        decal = ClientAPI.Decal.Decal(FootPrintImage, PlayerPosition.x, PlayerPosition.z, 200, 200, Rotation, 5, 0, 90)	
        LastFootstepPosition = PlayerPosition

def UpdateCompassPosition():
    global CompassDecal
    if CompassDecal != None and ClientAPI.GetPlayerObject() != None:
        CompassDecal.PosX = ClientAPI.GetPlayerObject().Position.x
        CompassDecal.PosZ = ClientAPI.GetPlayerObject().Position.z
		
def UpdateTargetPosition():
    global CurrentTarget
    global TargetDecal
    if TargetDecal != None and CurrentTarget != None:
        TargetDecal.PosX = CurrentTarget.Position.x
        TargetDecal.PosZ = CurrentTarget.Position.z
		
def ShowTarget():
    global TargetDecal
    TargetDecal = ClientAPI.Decal.Decal("yellow-circle-gradient.png", CurrentTarget.Position.x, CurrentTarget.Position.z, 2000, 2000, 0, 0, 0, 10)

def HideTarget():
    global TargetDecal
    if TargetDecal is not None:
        TargetDecal.Dispose()
    TargetDecal = None
		
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
		
def DecalFrame_OnEvent(frame, event):
    global CurrentTarget
    if event.eventType == "PLAYER_TARGET_CHANGED" :
        CurrentTarget = MarsTarget.GetCurrentTarget()
        if TargetDecal == None :
            ShowTarget()
        
def DecalFrame_Update():
    UpdateCompassPosition()
    UpdateTargetPosition()
    UpdateFootsteps()
