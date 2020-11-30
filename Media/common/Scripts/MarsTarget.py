"""This module contains the various methods for dealing with the target."""

import ClientAPI

import MarsUnit

#
# TargetAPI Methods
#

def AttackTarget():
    global _currentTarget
    if _currentTarget is None:
        ClientAPI.Write("No target selected")
        return
    if MarsUnit.UnitAffectingCombat("player"):
        ClientAPI.Network.SendAttackMessage(_currentTarget.OID, "strike", False)
    else:
        ClientAPI.Network.SendAttackMessage(_currentTarget.OID, "strike", True)

def ClearTarget():
    _UpdateTarget(None)

def TargetByName(name):
    _UpdateTarget(ClientAPI.World.GetObjectByName(name))

def TargetUnit(unit):
    _UpdateTarget(MarsUnit._GetUnit(unit))
    
def TargetLastEnemy():
    global _lastEnemy
    _UpdateTarget(_lastEnemy)

def TargetLastTarget():
    global _lastTarget
    _UpdateTarget(_lastTarget)

def TargetNearestEnemy(reverse=False):
    global _currentTarget, _lastTarget
    worldObjOIDs = ClientAPI.World.WorldObjectOIDs
    worldObjects = []
    for worldObjOID in worldObjOIDs:
        worldObj = ClientAPI.World.GetObjectByOID(worldObjOID)
        if worldObj is not None and worldObj.CheckBooleanProperty("attackable"):
            worldObjects.append(worldObj)
    playerPos = ClientAPI.GetPlayerObject().Position
    worldObjects.sort((lambda x, y: _DistanceComparerHelper(playerPos, x, y)), reverse=reverse)
    # I now have a list of world objects, sorted based on their distance from the player
    last = None
    if _currentTarget is not None and _currentTarget.CheckBooleanProperty("attackable"):
        last = _currentTarget
    else:
        last = _lastEnemy
    index = -1
    if last in worldObjects:
        index = worldObjects.index(last)
    else:
        last = None
    if last is None:
        if len(worldObjects) > 0:
            _UpdateTarget(worldObjects[0])
        return
    if len(worldObjects) > index + 1:
        _UpdateTarget(worldObjects[index + 1])
    else:
        _UpdateTarget(worldObjects[0])

def _DistanceComparerHelper(pos, x, y):
    xDistSquared = (pos - x.Position).LengthSquared
    yDistSquared = (pos - y.Position).LengthSquared
    if xDistSquared < yDistSquared:
        return -1
    elif xDistSquared > yDistSquared:
        return 1
    return 0

def TargetByOID(oid):
    _UpdateTarget(ClientAPI.World.GetObjectByOID(oid))

def GetCurrentTarget():
    global _currentTarget
    return _currentTarget

#
# Variables to keep track of state
#

# info about the current target, the last target, the last enemy target, and the mouseover object
_currentTarget = None
_lastTarget = None
_lastEnemy = None
_mouseoverTarget = None

#
# Helper methods
#

def _UpdateTarget(obj):
    global _currentTarget, _lastTarget, _lastEnemy
    if _currentTarget != obj:
        if _currentTarget is not None:
            _lastTarget = _currentTarget
            if _currentTarget.CheckBooleanProperty("attackable"):
                _lastEnemy = _currentTarget
        _currentTarget = obj
        ClientAPI.Interface.DispatchEvent("PLAYER_TARGET_CHANGED", [])

def _HandleObjectRemoved(worldObj):
    global _currentTarget, _lastTarget, _lastEnemy, _mouseoverTarget
    if _currentTarget == worldObj:
        _UpdateTarget(None)
    if _lastTarget == worldObj:
        _lastTarget = None
    if _lastEnemy == worldObj:
        _lastEnemy = None
    if _mouseoverTarget == worldObj:
        _mouseoverTarget = None
        ClientAPI.Interface.DispatchEvent("MOUSEOVER_TARGET_CHANGED", [])

def _UpdateMouseoverTarget(sender, event):
    global _mouseoverTarget
    target = ClientAPI.GetMouseoverTarget()
    if target != _mouseoverTarget:
        _mouseoverTarget = target
        ClientAPI.Interface.DispatchEvent("MOUSEOVER_TARGET_CHANGED", [])

# Register for frame started events, so we can update our mouseover target
ClientAPI.RegisterEventHandler('FrameStarted', _UpdateMouseoverTarget)

# Register for object removed messages, so we can clear our target if needed
ClientAPI.World.RegisterEventHandler('ObjectRemoved', _HandleObjectRemoved)
