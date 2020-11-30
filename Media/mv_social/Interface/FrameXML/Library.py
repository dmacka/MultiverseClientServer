from Axiom.Core import ColorEx
from Axiom.MathLib import Vector3

import ClientAPI

def getglobal(frameName):
    if ClientAPI.Interface.FrameMap.ContainsKey(frameName):
        return ClientAPI.Interface.FrameMap[frameName]
    ClientAPI.LogWarn("Invalid frame name: %s" % frameName)
    return None

def _ERRORMESSAGE(message):
    scriptErrors = getglobal("ScriptErrors")
    scriptErrorsMessage = getglobal("ScriptErrors_Message")
    if scriptErrors is not None:
        if scriptErrorsMessage is not None:
            scriptErrorsMessage.SetText(message)
        scriptErrors.Show()
    ClientAPI.LogWarn(message)

def message(msg):
    _ERRORMESSAGE(msg)
