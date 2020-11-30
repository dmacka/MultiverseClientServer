import ClientAPI
import Multiverse.Base
import Multiverse.Network

from Multiverse.Network import *

attachments = {}

def AttachHandler(m):
    oid = m.Oid
    attachOid = m.ObjectId
    if oid not in attachments:
        attachments[oid] = []
    attachments[oid].append(attachOid)

def DetachHandler(m):
    oid = m.Oid
    attachOid = m.ObjectId
    if oid not in attachments:
        return
    attachments[oid].remove(attachOid)
    if len(attachments[oid]) == 0:
        del attachments[oid]
    
MessageDispatcher.Instance.RegisterHandler(WorldMessageType.Attach, AttachHandler)
MessageDispatcher.Instance.RegisterHandler(WorldMessageType.Detach, DetachHandler)

def ObjectRemovedHandler(worldObj):
    oid = worldObj.OID
    if oid not in attachments:
        return
    for attachOid in attachments[oid]:
        detachMessage = DetachMessage()
        detachMessage.Oid = oid
        detachMessage.ObjectId = attachOid
        Multiverse.Base.Client.Instance.WorldManager.HandleDetach(detachMessage)
    del attachments[oid]

ClientAPI.World.RegisterEventHandler('ObjectRemoved', ObjectRemovedHandler)
