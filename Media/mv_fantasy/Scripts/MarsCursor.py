"""This module handles the cursor."""

import ClientAPI

import MarsUnit
import MarsTarget
import MarsTraining

#
# CursorAPI Methods
#

def CursorHasItem():
    return _cursorItem is not None

def CursorHasAbility():
    # WoW calls this CursorHasSpell
    return _cursorAbility is not None

def CursorHasSpell():
    # in case anyone cares about the WoW API
    return CursorHasAbility()

# This implementation doesn't really delete the item in the cursor.
# Instead, it simply clears the cursor and logs a message
def DeleteCursorItem():
    global _cursorItem
    _cursorItem = None
    ClientAPI.Log("Called delete cursor item")

# Reset the cursor to its initial state (point)
def ResetCursor():
    global _cursorItem, _cursorAbility
    ClientAPI.Log("Setting cursor to point")
    # reset our state
    _cursorItem = None
    _cursorAbility = None
    _contextCursor = None
    # Reset the UI cursors
    # Clear the inventory cursor
    ClientAPI.Interface.SetCursor(0, None)
    # Clear the context cursor
    ClientAPI.Interface.SetCursor(1, None)

_cursorMap = {
    "CAST_CURSOR" : "Interface\\Cursor\\Cast",
    "CAST_ERROR_CURSOR" : "Interface\\Cursor\\UnableCast",
    "SPEAK_CURSOR" : "Interface\\Cursor\\Speak",
    "SPEAK_ERROR_CURSOR" : "Interface\\Cursor\\UnableSpeak",
    "ATTACK_CURSOR" : "Interface\\Cursor\\Attack",
    "ATTACK_ERROR_CURSOR" : "Interface\\Cursor\\UnableAttack",
    "LOOT_CURSOR" : "Interface\\Cursor\\Pickup",
    "LOOT_ERROR_CURSOR" : "Interface\\Cursor\\UnablePickup",
    "CAST_ERROR_CURSOR" : "Interface\\Cursor\\UnableCast",
    }
_contextCursor = None

def RegisterCursor(cursorName, cursorImage):
    _cursorMap[cursorName] = cursorImage

def UnregisterCursor(cursorName):
    if cursorName in _cursorMap:
        del cursorMap[cursorName]

# Sets the cursor (currently sets the context cursor)
# This method provides a mapping from a symbolic cursor name to the
# actual cursor image that will be used.
def SetCursor(cursor):
    global _contextCursor
    if _contextCursor == cursor:
        return
    if cursor in _cursorMap:
        ClientAPI.Interface.SetCursor(1, _cursorMap[cursor])
        _contextCursor = cursor
    else:
        ClientAPI.Log("Setting cursor to unknown: %s" % str(cursor))
        ClientAPI.Interface.SetCursor(1, None)
        _contextCursor = None

#
# Variables to keep track of state
#

_cursorItem = None
_cursorAbility = None

#
# Helper Methods
#

def _UpdateCursor():
    """Update the cursor based on the _cursorItem or _cursorAbility fields."""
    global _cursorItem, _cursorAbility
    if _cursorItem is not None:
        # Set the item/ability cursor
        ClientAPI.Interface.SetCursor(0, _cursorItem.icon)
    elif _cursorAbility is not None:
        # Set the item/ability cursor
        ClientAPI.Interface.SetCursor(0, _cursorAbility.icon)
    else:
        # Clear the item/ability cursor
        ClientAPI.Interface.SetCursor(0, None)

def _UpdateContextCursor(a, b):
    """Update the context cursor based on what object it is currently over."""
    if ClientAPI.InputHandler is None:
        # Not yet initialized
        return
    if ClientAPI.InputHandler.IsMouseLook:
        return
    objNode = MarsUnit._GetUnit("mouseover")
    if objNode is None:
        SetCursor(None)
        #ClientAPI.Interface.SetCursor(1, None)
        return
    else:
        dist = (objNode.Position - ClientAPI.GetPlayerObject().Position).Length
        dist = dist / 1000 # I prefer to deal in meters, but the distance was in mm.
        if objNode.PropertyExists("context_cursor"):
            SetCursor(objNode.GetProperty("context_cursor"))
        elif objNode.CheckBooleanProperty("lootable"):
            if dist < 4.0:
                SetCursor("LOOT_CURSOR")
            else:
                SetCursor("LOOT_ERROR_CURSOR")
        elif objNode.CheckBooleanProperty("questconcludable"):
            ClientAPI.Log("questconcludable");
            if dist < 6.0:
                SetCursor("SPEAK_CURSOR")
            else:
                SetCursor("SPEAK_ERROR_CURSOR")
        elif objNode.CheckBooleanProperty("questavailable"):
            ClientAPI.Log("questavailable");
            if dist < 6.0:
                SetCursor("SPEAK_CURSOR")
            else:
                SetCursor("SPEAK_ERROR_CURSOR")
        elif objNode.CheckBooleanProperty("attackable"):
            if dist < 4.0:
                SetCursor("ATTACK_CURSOR")
            else:
                SetCursor("ATTACK_ERROR_CURSOR")

_mouseDownObject1 = None
_mouseDownObject2 = None

def OnLeftClick(down):
    """Handle the left click event (perhaps over an object)."""
    global _mouseDownObject1
    worldObj = MarsUnit._GetUnit("mouseover")
    if down:
        # ClientAPI.DebugWrite("Mouse down object = " + str(worldObj))
        # store the mouse down object
        _mouseDownObject1 = worldObj
        return
    if worldObj is None:
        return
    # ClientAPI.DebugWrite("Mouse up object = " + str(worldObj))
    if worldObj != _mouseDownObject1:
        return
    # mouse up over the same object as the mouse down
    # that means this is a 'click' on the object
    MarsTarget.TargetByOID(worldObj.OID)

def OnRightClick(down):
    """Handle the right click event (perhaps over an object)."""
    global _mouseDownObject2
    # For now, we can just always reset the cursor on a right click.
    # At some point, perhaps picking up an item or ability and right clicking
    # on an object in the world will do something, but it doesn't now.
    # Make right mouse up reset the cursor
    if not down:
        ResetCursor()
    worldObj = MarsUnit._GetUnit("mouseover")
    if down:
        # ClientAPI.DebugWrite("Mouse down object = " + str(objNode))
        # store the mouse down object
        _mouseDownObject2 = worldObj
        return
    if worldObj is None:
        return
    if worldObj != _mouseDownObject2:
        return
    ClientAPI.DebugWrite("MouseOver unit: " + worldObj.Name)
    dist = (worldObj.Position - ClientAPI.GetPlayerObject().Position).Length
    dist = dist / 1000 # I prefer to deal in meters, but the distance was in mm.
    # On a right click, do the context sensitive action
    if worldObj.PropertyExists("istrainer"):
        if worldObj.CheckBooleanProperty("istrainer"):   
            if dist < 6.0:
                MarsTraining.SendTrainingInfoRequestMessage(worldObj.OID)
            else:
                ClientAPI.Write("That object is too far away (%f meters)" % dist)		
    elif worldObj.PropertyExists("click_handler"):
        ClientAPI.DebugWrite("Invoking custom click handler for object")
        worldObj.GetProperty("click_handler")(worldObj, None)
    elif worldObj.CheckBooleanProperty("lootable"):
        if dist < 4.0:
            ClientAPI.Network.SendTargetedCommand(worldObj.OID, "/lootall")
        else:
            ClientAPI.Write("That object is too far away (%f meters)" % dist)
    elif worldObj.CheckBooleanProperty("questconcludable"):
        ClientAPI.Log("questconcludable")
        if dist < 6.0:
            ClientAPI.Network.SendQuestConcludeRequestMessage(worldObj.OID);
        else:
            ClientAPI.Write("That object is too far away (%f meters)" % dist)
    elif worldObj.CheckBooleanProperty("questavailable"):
        ClientAPI.Log("questavailable")
        if dist < 6.0:
            ClientAPI.Network.SendQuestInfoRequestMessage(worldObj.OID)
        else:
            ClientAPI.Write("That object is too far away (%f meters)" % dist)
    elif worldObj.CheckBooleanProperty("attackable"):
        if dist < 4.0:
            ClientAPI.Network.SendAttackMessage(worldObj.OID, "strike", True)
            ClientAPI.Write("Sent 'strike' attack for %d" % worldObj.OID)
        else:
            ClientAPI.Write("That object is too far away (%f meters)" % dist)
    else:
        ClientAPI.Write("That object has no action")
                        
ClientAPI.RegisterEventHandler("FrameStarted", _UpdateContextCursor)
