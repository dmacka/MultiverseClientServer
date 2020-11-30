import ClientAPI

import MarsEvent
import MarsTarget

TargetDecal = None
TargetOn = False
CurrentTarget = None

def TargetMoveHandler(pos, orient, scale):
    TargetDecal.PosX = pos.x
    TargetDecal.PosZ = pos.z
    
def ShowDecal():
    global TargetDecal
    global TargetOn
    TargetDecal = ClientAPI.Decal.Decal("yellow-circle-gradient.png", 0, 0, 2000, 2000)
    TargetOn = True

def HideDecal():
    global TargetDecal
    global TargetOn
    TargetDecal.Dispose()
    TargetDecal = None
    TargetOn = False

def TargetChangedHandler(eventName, eventArgs):
    global CurrentTarget
    global TargetDecal
    global TargetOn
    
    if TargetOn:
        # get rid of event handler on old target
        CurrentTarget.SceneNode.RemoveEventHandler('Updated', TargetMoveHandler)
    CurrentTarget = MarsTarget.GetCurrentTarget()
    if CurrentTarget is None:
        HideDecal()
    else:
        if not TargetOn:
            ShowDecal()
        TargetDecal.PosX = CurrentTarget.Position.x
        TargetDecal.PosZ = CurrentTarget.Position.z
        CurrentTarget.SceneNode.RegisterEventHandler('Updated', TargetMoveHandler)
        
MarsEvent.RegisterEventHandler('PLAYER_TARGET_CHANGED', TargetChangedHandler)
