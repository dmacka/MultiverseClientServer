"""This module contains the various methods for dealing with actions."""

import ClientAPI

import MarsTarget
import MarsCursor

class ActionEntry:
    def __init__(self):
        self.item = None
        self.ability = None

#
# ActionAPI Methods
#

def GetActionInfo(slotId):
    global _actions
    if not _actions.has_key(slotId):
        return None
    action = _actions[slotId]
    if action.item is not None:
        return ["item", action.item.itemId, "item"]
    elif action.ability is not None:
        return ["ability", action.ability.name, "ability"]
    return None

def GetActionText(slotId):
    global _actions
    if not _actions.has_key(slotId):
        return None
    action = _actions[slotId]
    if action.item is not None:
        return action.item.name
    elif action.ability is not None:
        return action.ability.name
    return None

def GetActionTexture(slotId):
    global _actions
    if not _actions.has_key(slotId):
        return None
    action = _actions[slotId]
    if action.item is not None:
        return action.item.icon
    elif action.ability is not None:
        return action.ability.icon
    return None

def HasAction(slotId):
    global _actions
    return _actions.has_key(slotId)

def UseAction(slotId, checkCursor, onSelf):
    global _actions
    if not _actions.has_key(slotId):
        ClientAPI.Log("No matching action for slot %s" % slotId)
        return
    ClientAPI.Log("Using action: %s" % slotId)
    action = _actions[slotId]
    targetOid = None
    if onSelf:
        targetOid = ClientAPI.GetPlayerObject().OID
    elif MarsTarget.GetCurrentTarget() is None:
        targetOid = ClientAPI.GetPlayerObject().OID
    else:
        targetOid = MarsTarget.GetCurrentTarget().OID
    if action.ability is not None:
        ClientAPI.Network.SendTargetedCommand(targetOid, "/ability " + action.ability.name)
        # ClientAPI.Network.SendStartAbilityMessage(action.ability.name, targetOid);
    elif action.item is not None:
        ClientAPI.Network.SendActivateItemMessage(action.item.itemId, targetOid)

def PlaceAction(slotId):
    """This places the cursor action in the action slot, and the
       action that was in the slot in the cursor.  If the cursor was
       empty, we do not do anything here."""
    global _actions
    if MarsCursor._cursorItem is None and MarsCursor._cursorAbility is None:
        return
    oldAction = None
    if _actions.has_key(slotId):
        # store this, because we will want to put it in the cursor later
        oldAction = _actions[slotId]
    if MarsCursor._cursorItem is not None:
        action = ActionEntry()
        action.item = MarsCursor._cursorItem
        _actions[slotId] = action
    elif MarsCursor._cursorAbility is not None:
        action = ActionEntry()
        action.ability = MarsCursor._cursorAbility
        _actions[slotId] = action
    if oldAction is not None:
        MarsCursor._cursorItem = oldAction.item
        MarsCursor._cursorAbility = oldAction.ability
        MarsCursor._UpdateCursor()
    else:
        MarsCursor._cursorItem = None
        MarsCursor._cursorAbility = None
        MarsCursor._UpdateCursor()

def PickupAction(slotId):
    """This places the action that was in the slot in the cursor, and the action
       item that was in the cursor in the action slot.  If the slot is empty, we
       do not do anything here."""
    global _actions
    if not _actions.has_key(slotId):
        return
    action = _actions[slotId]
    if action.item is None and action.ability is None:
        ClientAPI.Log("Shouldn't have gotten here.  Action entry where item and ability are None.")
        return
    oldAction = None
    if MarsCursor._cursorItem is not None and MarsCursor._cursorAbility is not None:
        oldAction = ActionEntry()
        oldAction.item = MarsCursor._cursorItem
        oldAction.ability = MarsCursor._cursorAbility
    MarsCursor._cursorItem = action.item
    MarsCursor._cursorAbility = action.ability
    MarsCursor._UpdateCursor()
    if oldAction is not None:
        # we had an action in the cursor - put it in the action bar
        _actions[slotId] = oldAction
    elif _actions.has_key(slotId):
        # clear the action bar slot
        _actions.pop(slotId)

#
# Variables to keep track of state
#

# info about the actions we have available
_actions = {}

