import ClientAPI

from Axiom.Input import MouseEventHandler
from Axiom.Input import MouseButtons

def MvClickExample_OnLoad(frame):
    frame.RegisterEvent("PROPERTY_clickCommand")

def MvClickExample_OnEvent(frame, event):
    if event.eventType == "PROPERTY_clickCommand":
        if event.eventArgs[0] == "any":
            oid = long(event.eventArgs[1])
            objNode = ClientAPI.World.GetObjectByOID(oid)
            objNode.SetProperty("click_handler", MvClickExample_OnClick)

def MvClickExample_OnClick(sender, args):
    ClientAPI.Network.SendTargetedCommand(sender.OID, "/click")
