"""This module keeps track of inventory."""

import ClientAPI

from Multiverse.Network import WorldMessageType
from Multiverse.Network import MessageDispatcher

import MarsCursor
import MarsTarget

class InvItemInfo:
    """This class holds information about an item in the inventory."""
    def __init__(self):
        self.itemId = 0
        self.name = ""
        self.icon = ""
        self.count = 0

    def __str__(self):
        return "<MarsContainer.InvItemInfo %d '%s' '%s' %d>" % (self.itemId, self.name, self.icon, self.count)

#
# ContainerAPI Methods
#

def GetContainerItemInfo(containerId, slotId):
    item = _GetContainerItem(containerId, slotId)
    if item is None:
        return None
    # icon, count, locked, quality, readable
    return [item.icon, 1, False, 1, False]

def GetContainerItemLink(containerId, slotId):
    item = _GetContainerItem(containerId, slotId)
    if item is None:
        return None
    # icon, count, locked, quality, readable
    return item.name

def GetContainerNumSlots(containerId):
    # for now, hardcode all containers to 16 slots
    return 16

def GetInventoryItemCount(selection, slotId):
    # Obviously, this isn't right, but this dummy version provides an example
    # of what sort of value to return for the number of items equipped in a
    # slot (e.g. number of arrows in the quiver for a fantasy game).
    return 0

def GetInventoryItemTexture(selection, slotId):
    # Obviously, this isn't right, but this dummy version provides an example
    # of what sort of value to return so that we could display an icon for an
    # equipped item.
    return "Interface\\Icons\\" + "foobar"

def GetInventorySlotInfo(slotName):
    # Again, this isn't a real implementation, but this should provide a sample
    # of how to assign names to slots, and return the icon of the item equipped
    # in that slot.
    if slotName == "HeadSlot":
        return [1, "Interface\\Icons\\" + "foobar"]
    elif slotName == "ChestSlot":
        return [2, "Interface\\Icons\\" + "foobar"]
    elif slotName == "MainHandSlot":
        return [3, "Interface\\Icons\\" + "foobar"]
    return [0, "Interface\\Icons\\" + "foobar"]


# Pick up (or drop) an item from a given container and slot.
# This will set the cursor to the item.
def PickupContainerItem(containerId, slotId):
    ClientAPI.Log("Checking container " + str(containerId) + " and slot " + str(slotId))
    item = _GetContainerItem(containerId, slotId)
    if MarsCursor.CursorHasItem():
        # Place the item in the slot (possibly taking the item that was in the slot)
        ClientAPI.Log("Drop item to: %d, %d" % (containerId, slotId))
        ClientAPI.Log("Old item: %s" % str(MarsCursor._cursorItem))
        _SetContainerItem(containerId, slotId, MarsCursor._cursorItem, item)
        MarsCursor._cursorItem = None
        MarsCursor._UpdateCursor()
    elif MarsCursor.CursorHasAbility():
        ClientAPI.Log("Cannot currently use abilities on items")
    else:
         #Cursor is empty
        MarsCursor._cursorItem = item
        MarsCursor._cursorAbility = None
        MarsCursor._UpdateCursor()
        ClientAPI.Log("Pickup item: %s, %s" % (str(item), item.icon))

# Activate an item from a given container and slot.
# This sends the '/activate' message to the server.
def UseContainerItem(containerId, slotId, onSelf):
    item = _GetContainerItem(containerId, slotId)
    if item is not None:
        targetOid = None
        if onSelf:
            targetOid = ClientAPI.GetPlayerObject().OID
        elif MarsTarget.GetCurrentTarget() is None:
            targetOid = ClientAPI.GetPlayerObject().OID
        else:
            targetOid = MarsTarget.GetCurrentTarget().OID
        ClientAPI.Network.SendActivateItemMessage(item.itemId, targetOid)

#
# Variables to keep track of state
#

# info about the inventory
_inventory = {}

#
# Helper Methods
#
def _GetContainerItem(containerId, slotId):
    global _inventory
    # From the scripting interface, the ids are 1-5 and 1-16
    # Adjust this to be zero based;
    slotId = slotId - 1
    if not _inventory.has_key(containerId):
        return None
    container = _inventory[containerId]
    if not container.has_key(slotId):
        return None
    return container[slotId]

def _SetContainerItem(containerId, slotId, item, destination):
    # Currently, I can't actually move items around, because I don't
    # have the network and server machinery.  For now, just pretend
    # that we moved things, and inject the ui event.
    global _inventory
    # From the scripting interface, the ids are 1-5 and 1-16
    # Adjust this to be zero based;
    worldObj = ClientAPI.GetPlayerObject()
    slotId = slotId - 1
    if not _inventory.has_key(containerId):
        ClientAPI.Log("Attempted to place item in invalid container")
        return
    if destination is not None:
        destinationOid = destination.itemId
    else:
        destinationOid = None
    props = {"playerOid" : worldObj.OID, "containerId" : containerId, "slotId" : slotId, "itemOid" : item.itemId, "destinationOid" : destinationOid}
    ClientAPI.Network.SendExtensionMessage(0, False, "mv.SWAP_ITEM", props)

def _HandleInventoryUpdate(message):
    global _inventory
    for container in _inventory.values():
        container.clear()
    ClientAPI.Log("Got InventoryUpdateMessage with %d entries" % len(message.Inventory))
    for entry in message.Inventory:
        ClientAPI.Log("InventoryUpdateEntry fields: %d, %d, %d, %s" % (entry.itemId, entry.containerId, entry.slotId, entry.name))
        if not _inventory.has_key(entry.containerId):
            _inventory[entry.containerId] = {}
        invInfo = InvItemInfo()
        invInfo.icon = entry.icon
        invInfo.count = entry.count
        invInfo.itemId = entry.itemId
        invInfo.name = entry.name;
        _inventory[entry.containerId][entry.slotId] = invInfo
    #
    # dispatch a ui event to tell the rest of the system
    #
    ClientAPI.Interface.DispatchEvent("UNIT_INVENTORY_UPDATE", [])

# Register callbacks for inventory messages
# Ideally, these would not be using custom message types, but the
# current implementation does use these until we update the server.
MessageDispatcher.Instance.RegisterHandler(WorldMessageType.InventoryUpdate, _HandleInventoryUpdate)
