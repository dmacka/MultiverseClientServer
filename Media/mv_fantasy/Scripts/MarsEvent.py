"""This module contains the various methods for registering for messages and
   generating the correct UI events in response.  If there is other custom logic
   for dealing with the information in the messages, the handlers will be in
   a different module.  Some trivial messages that only result in log messages
   are also handled in this module."""

import ClientAPI

from Multiverse.Network import WorldMessageType
from Multiverse.Network import MessageDispatcher

import MarsTarget

#
# EventAPI methods
#

def RegisterEventHandler(eventName, handler):
    global _eventHandlers
    handlers = []
    if _eventHandlers.has_key(eventName):
        handlers = _eventHandlers[eventName]
    else:
        _eventHandlers[eventName] = handlers
    handlers.append(handler)
    
def RemoveEventHandler(eventName, handler):
    global _eventHandlers
    if _eventHandlers.has_key(eventName):
        handlers = _eventHandlers[eventName]
        handlers.remove(handler)
        if len(handlers) == 0:
            del _eventHandlers[eventName]

#
# Variables
#

# keep a dictionary of which methods are registered for which events
_eventHandlers = {}


#
# Helper methods
#

def _HandleAcquireResponse(message):
    if message.Status:
        ClientAPI.Log("Acquired object: %d" % message.ObjectId)
    else:
        ClientAPI.Log("Failed to acquire object: %d" % message.ObjectId)

def _HandleEquipResponse(message):
    if message.Status:
        ClientAPI.Log("Equipped object %d to slot %s" % (message.ObjectId, message.SlotName))
    else:
        ClientAPI.Log("Failed to equip object %d to slot %s" % (message.ObjectId, message.SlotName))

def _HandleUnequipResponse(message):
    if message.Status:
        ClientAPI.Log("Unequipped object %d from slot %s" % (message.ObjectId, message.SlotName))
    else:
        ClientAPI.Log("Failed to unequip object %d from slot %s" % (message.ObjectId, message.SlotName))

def _HandleAttach(message):
    ClientAPI.Log("Attached object %d to socket %s" % (message.ObjectId, message.SlotName))

def _HandleDetach(message):
    ClientAPI.Log("Detached object %d from socket %s" % (message.ObjectId, message.SlotName))

def _HandleComm(message):
    # This will work with any widget that uses the event
    # registration system.  In the future, more cases should be handled here.
    # A better mechanism for this is to actually use server logic
    # instead to send these ui events directly
    node = ClientAPI.World.GetObjectByOID(message.Oid)
    nodeName = "Unknown entity"
    if node is not None:
        nodeName = node.Name
    if message.ChannelId == 1:
        # Say channel (1)
        ClientAPI.Interface.DispatchEvent("CHAT_MSG_SAY", [message.Message, nodeName, ""])
    elif message.ChannelId == 2:
        # ServerInfo channel (2)
        ClientAPI.Interface.DispatchEvent("CHAT_MSG_SYSTEM", [message.Message, ""])
    elif message.ChannelId == 3:
        # CombatInfo channel (3)
        ClientAPI.Interface.DispatchEvent("CHAT_MSG_COMBAT_MISC_INFO", [message.Message])
    elif message.ChannelId == 4:
	# Group channel (4)
	ClientAPI.Interface.DispatchEvent("CHAT_MSG_GROUP", [message.Message, ""])        
    elif message.ChannelId == 5:
	# Guild channel (5)
	ClientAPI.Interface.DispatchEvent("CHAT_MSG_GUILD", [message.Message, ""])        
    elif message.ChannelId == 6:
	# Tell/Private Message channel (6)
	ClientAPI.Interface.DispatchEvent("CHAT_MSG_TELL", [message.Message, ""])        
    else:
        channelName = "unknown"
        longChannel = "%d. %s" % (message.ChannelId, channelName)
        ClientAPI.Interface.DispatchEvent("CHAT_MSG_CHANNEL", [message.Message, nodeName, "", longChannel, "", "", str(message.ChannelId), str(message.ChannelId), channelName])

def _HandleDamage(message):
    damager = ClientAPI.World.GetObjectByOID(message.Oid)
    damagee = ClientAPI.World.GetObjectByOID(message.ObjectId)
    damagerName = "Unknown entity"
    damageeName = "Unknown entity"
    player = ClientAPI.GetPlayerObject()
    action = "strikes"
    if damager is not None:
        if damager.OID == player.OID:
            damagerName = "You"
        else:
            damagerName = damager.Name
    if damagee is not None:
        if damagee.OID == player.OID:
            damageeName = "you"
        else:
            damageeName = damagee.Name
    if damager is not None:
        if damager.OID == player.OID:
            action = "strike"
        else:
            action = "strikes"
    msg = "%s %s %s for %d points of %s damage." % (damagerName, action, damageeName, message.DamageAmount, message.DamageType)
    if damagee == player:
        ClientAPI.Interface.DispatchEvent("CHAT_MSG_COMBAT_CREATURE_VS_SELF_HITS", [msg])
    else:
        ClientAPI.Interface.DispatchEvent("CHAT_MSG_COMBAT_CREATURE_VS_CREATURE_HITS", [msg])
            
def _HandleCombatMiss(message):
    damager = ClientAPI.World.GetObjectByOID(int(message["attacker"]))
    damagee = ClientAPI.World.GetObjectByOID(int(message["target"]))
    damagerName = "Unknown entity"
    damageeName = "Unknown entity"
    player = ClientAPI.GetPlayerObject()
    action = "misses"
    if damager is not None:
        if damager.OID == player.OID:
            damagerName = "You"
        else:
            damagerName = damager.Name
    if damagee is not None:
        if damagee.OID == player.OID:
            damageeName = "you"
        else:
            damageeName = damagee.Name
    if damager is not None:
        if damager.OID == player.OID:
            action = "missed"
        else:
            action = "misses"
    msg = "%s %s %s." % (damagerName, action, damageeName)
    if damagee == player:
        ClientAPI.Interface.DispatchEvent("CHAT_MSG_COMBAT_CREATURE_VS_SELF_HITS", [msg])
    else:
        ClientAPI.Interface.DispatchEvent("CHAT_MSG_COMBAT_CREATURE_VS_CREATURE_HITS", [msg])

def _HandleObjectProperty(message):
    """Notify any interested widgets about any properties that have changed."""
    if message.Properties.Count <= 0:
        return
    target = MarsTarget.GetCurrentTarget()
    player = ClientAPI.GetPlayerObject()
    for prop in message.Properties.Keys:
        eventName = "PROPERTY_" + prop
        if target is not None and message.Oid == target.OID:
            ClientAPI.Interface.DispatchEvent(eventName, ["target"])
        if player is not None and message.Oid == player.OID:
            ClientAPI.Interface.DispatchEvent(eventName, ["player"])
        # Always post an "any" unit event.
        ClientAPI.Interface.DispatchEvent(eventName, ["any", str(message.Oid)])

# Register callback for ability update messages
# Ideally, these would not be using custom message types, but the
# current implementation does use these until we update the server.
MessageDispatcher.Instance.RegisterHandler(WorldMessageType.AcquireResponse, _HandleAcquireResponse)
MessageDispatcher.Instance.RegisterHandler(WorldMessageType.EquipResponse, _HandleEquipResponse)
MessageDispatcher.Instance.RegisterHandler(WorldMessageType.UnequipResponse, _HandleUnequipResponse)
MessageDispatcher.Instance.RegisterHandler(WorldMessageType.Attach, _HandleAttach)
MessageDispatcher.Instance.RegisterHandler(WorldMessageType.Detach, _HandleDetach)
MessageDispatcher.Instance.RegisterHandler(WorldMessageType.Comm, _HandleComm)
MessageDispatcher.Instance.RegisterHandler(WorldMessageType.Damage, _HandleDamage)
MessageDispatcher.Instance.RegisterHandler(WorldMessageType.ObjectProperty, _HandleObjectProperty)

def _HandleUiEvent(eventName, args):
    global _eventHandlers
    if _eventHandlers.has_key(eventName):
        for handler in _eventHandlers[eventName]:
            handler(eventName, args)
        
#
# Register with the ClientAPI to get all UI Events
#
ClientAPI.Interface.RegisterEventHandler('UiEvent', _HandleUiEvent)
ClientAPI.Network.RegisterExtensionMessageHandler("mv.COMBAT_ABILITY_MISSED", _HandleCombatMiss)
