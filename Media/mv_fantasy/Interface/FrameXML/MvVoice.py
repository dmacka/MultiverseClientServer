loggedIn = False

def MvVoice_fMain_fFooter_bOption_OnClick(frame, event):
    global loggedIn
    if loggedIn:
        # mvVoice.mvVoiceOff()
        MvVoice_fMain_fHeader_fsDialog.SetText("Voice Chat DISABLED")
        MvVoice_fMain_fFooter_bOption.SetText("ENABLE")
    else:
        # mvVoice.mvVoiceOn()
        MvVoice_fMain_fHeader_fsDialog.SetText("Push '\\' to TALK")
        MvVoice_fMain_fFooter_bOption.SetText("DISABLE")
    loggedIn = not loggedIn

def MvVoice_fMain_OnLoad(frame):
    MvVoice_fMain_fHeader_fsDialog.SetText("Voice Chat DISABLED")
    MvVoice_fMain_fFooter_bOption.SetText("ENABLE")
    MvVoice_fMain_fFooter_bOption.SetScript("OnClick", MvVoice_fMain_fFooter_bOption_OnClick)
    # mvVoice.mvVoiceInit()
    MvVoice_fMain.Hide()
    
def PushToTalk(pushed):
    if (pushed):
        ClientAPI.DebugWrite("Pushed")
        # mvVoice.mvVoicePushToTalk(pushed)
    else:
        ClientAPI.DebugWrite("Released")
        # mvVoice.mvVoicePushToTalk(pushed)
