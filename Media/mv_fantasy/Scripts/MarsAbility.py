"""This module contains the various methods for dealing with abilities.
   This was loosely based on World of Warcraft's Spell API."""

import ClientAPI

from Multiverse.Network import WorldMessageType
from Multiverse.Network import MessageDispatcher

import MarsCursor
import MarsTarget

class AbilityEntry:
    """This class holds information about an item in the inventory."""
    def __init__(self):
        self.name = ""
        self.icon = ""
        self.category = 0

    def __str__(self):
        return "<MarsAbility.AbilityEntry '%s' '%s' '%s'>" % (self.name, self.icon, self.category)

#
# AbilityAPI Methods
#

def GetNumAbilities():
    global _abilities
    return len(_abilities)

def GetAbilityName(slotId):
    global _abilities
    if not _abilities.has_key(slotId):
        return None
    return _abilities[slotId].name

def GetAbilityTexture(slotId):
    global _abilities
    if not _abilities.has_key(slotId):
        return None
    return _abilities[slotId].icon
    
def PickupAbility(slotId):
    """This places the ability that was in the slot in the cursor.  If the
       slot is empty, we do not do anything here."""
    global _abilities
    if not _abilities.has_key(slotId):
        return
    ability = _abilities[slotId]
    MarsCursor._cursorItem = None
    MarsCursor._cursorAbility = ability
    MarsCursor._UpdateCursor()

def UseAbilityByName(name, onSelf):
    targetOid = None
    if onSelf:
        targetOid = ClientAPI.GetPlayerObject().OID
    elif MarsTarget.GetCurrentTarget() is None:
        targetOid = ClientAPI.GetPlayerObject().OID
    else:
        targetOid = MarsTarget.GetCurrentTarget().OID
    ClientAPI.Network.SendTargetedCommand(targetOid, "/ability " + name)

#
# Variables to keep track of state
#

# info about the abilities we have available
_abilities = {}


#
# Helper methods
#

def _HandleAbilityUpdate(message):
    global _abilities
    _abilities.clear()
    ClientAPI.Log("Got AbilityUpdateMessage with %d entries" % len(message.Entries))
    for entry in message.Entries:
        ClientAPI.Log("AbilityUpdateEntry fields: %s, %s, %s" % (entry.name, entry.icon, entry.category))
        ability = AbilityEntry()
        ability.name = entry.name
        ability.icon = entry.icon
        ability.category = entry.category
        # I want these to start at 1, so add 1 to the length
        _abilities[len(_abilities) + 1] = ability
    #
    # dispatch a ui event to tell the rest of the system
    #
    ClientAPI.Interface.DispatchEvent("ABILITY_UPDATE", [])

# Register callback for ability update messages
# Ideally, these would not be using custom message types, but the
# current implementation does use these until we update the server.
MessageDispatcher.Instance.RegisterHandler(WorldMessageType.AbilityUpdate, _HandleAbilityUpdate)
