"""This module contains the various methods for secure trade."""

import ClientAPI

from Multiverse.Network import WorldMessageType
from Multiverse.Network import MessageDispatcher

# Make sure we have the container package loaded
import MarsContainer
import MarsCursor

#
# TradeAPI methods
#

def GetTradeItemInfo(offerId, slotId):
    global _tradeOffers
    if not _tradeOffers.has_key(offerId):
        ClientAPI.DebugWrite("Invalid offer id: " + str(offerId))
        return None
    if not _tradeOffers[offerId].has_key(slotId):
        return None
    return _tradeOffers[offerId][slotId]

def SendTradeOfferMessage(partnerId, itemIds, accepted, cancelled):
    playerOid = ClientAPI.GetPlayerObject().OID
    props = { "requesterOid" : playerOid,
              "partnerOid" : partnerId,
              "offerItems" : itemIds,
              "accepted" : accepted,
              "cancelled" : cancelled }
    ClientAPI.Network.SendExtensionMessage(0, False, "mv.TRADE_OFFER_REQ", props)

def SendTradeOffer(partnerId, accepted, cancelled):
    itemIds = []
    maxSlotId = 0
    offer = _tradeOffers[2]
    for slotId in offer.keys():
        if slotId > maxSlotId:
            maxSlotId = slotId
    for slotId in range(0, maxSlotId+1):
        if offer.has_key(slotId):
            itemIds.append(offer[slotId].itemId)
        else:
            itemIds.append(-1L)
    SendTradeOfferMessage(partnerId, itemIds, accepted, cancelled)

def ClickTradeButton(slotId):
    global _tradeOffers
    cursorItem = None
    for slot in _tradeOffers[2].keys():
        item = _tradeOffers[2][slot]
    if MarsCursor.CursorHasItem():
        cursorItem = MarsCursor._cursorItem
    if _tradeOffers[2].has_key(slotId):
        MarsCursor._cursorItem = _tradeOffers[2][slotId]
        del(_tradeOffers[2][slotId])
    else:
        MarsCursor._cursorItem = None
    if cursorItem:
        _tradeOffers[2][slotId] = cursorItem
    for slot in _tradeOffers[2].keys():
        item = _tradeOffers[2][slot]
    MarsCursor._UpdateCursor()

#
# Variables to keep track of state
#

# info about the current offers
_tradeOffers = {1:{}, 2:{}}

#
# Helper methods
#
def _ConvertList(itemList):
    rv = {}
    slotId = 0
    for item in itemList:
        invitem = MarsContainer.InvItemInfo()
        invitem.itemId = item[0]
        invitem.name = item[1]
        invitem.icon = item[2]
        # invitem.count = item.count
        if (invitem.itemId != -1):
            rv[slotId] = invitem
        slotId = slotId + 1
    return rv

def _HandleTradeStart(props):
    global _tradeOffers
    _tradeOffers = {1:{}, 2:{}}
    ClientAPI.Interface.DispatchEvent("TRADE_START", [str(props["ext_msg_target_oid"]), str(props["ext_msg_subject_oid"])])

def _HandleTradeOfferUpdate(props):
    global _tradeOffers
    _tradeOffers[1] = _ConvertList(props["offer2"]) # their offer
    _tradeOffers[2] = _ConvertList(props["offer1"]) # my offer
    ClientAPI.Interface.DispatchEvent("TRADE_OFFER_UPDATE", [str(props["ext_msg_target_oid"]), str(props["ext_msg_subject_oid"]), str(props["accepted1"]), str(props["accepted2"])])

def _HandleTradeComplete(props):
    ClientAPI.Interface.DispatchEvent("TRADE_COMPLETE", [str(props["ext_msg_target_oid"]),
                                                         str(props["ext_msg_subject_oid"]),
                                                         str(props["status"])])

# Register callbacks for trade messages
# Ideally, these would not be using custom message types, but the
# current implementation does use these until we update the server.
ClientAPI.Network.RegisterExtensionMessageHandler("mv.TRADE_START", _HandleTradeStart)
ClientAPI.Network.RegisterExtensionMessageHandler("mv.TRADE_COMPLETE", _HandleTradeComplete)
ClientAPI.Network.RegisterExtensionMessageHandler("mv.TRADE_OFFER_UPDATE", _HandleTradeOfferUpdate)
