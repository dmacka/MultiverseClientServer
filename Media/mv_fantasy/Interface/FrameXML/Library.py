import ClientAPI

#
# Global Utility Methods
#
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

#
# Miscellaneous Methods
#
def HideUIPanel(frame):
    frame.Hide()
    # now check to see if we should show the party members  
    isPanelVisible = False
    UI_FRAMES = [ "MvDialogFrame" ]
    for panelName in UI_FRAMES:
        panel = getglobal(panelName)
        if panel.IsVisible():
            isPanelVisible = True
    # if not isPanelVisible:
    #    ShowPartyFrame()

def ShowUIPanel(frame):
    UI_FRAMES = [ "MvDialogFrame" ]
    for panelName in UI_FRAMES:
        panel = getglobal(panelName)
        panel.Hide()
    HidePartyFrame()
    frame.Show()

## Set up the default cursor
# ClientAPI.Interface.SetCursor("POINT_CURSOR")
