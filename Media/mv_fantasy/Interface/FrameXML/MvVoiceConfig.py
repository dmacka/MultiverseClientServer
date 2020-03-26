import Voice
import MarsVoice
import MarsGroup

_VC_popupOptions = None
_VC_popupCallback = None

def VCPopup(options, callback):
    global _VC_popupOptions
    global _VC_popupCallback

    _VC_popupOptions = options
    _VC_popupCallback = callback
    mouseX, mouseY = ClientAPI.GetMousePosition()
    VoiceConfigPopup.SetPoint("TOP", "VoiceConfigPopupTop", "TOPLEFT", int(mouseX), int(-mouseY+8))
    for i in range(0, 8):
        item = getglobal("VoiceConfigPopupItem" + str(i))
        if i < len(options):
            item.SetText(options[i])
            item.Show()
        else:
            item.SetText("")
            item.Hide()
    VoiceConfigPopup.SetHeight(7 + 17 * len(options))
    VoiceConfigPopupTop.Show()

def VCPopupClick(id):
    global _VC_popupOptions
    global _VC_popupCallback

    if _VC_popupCallback != None:
        _VC_popupCallback(id, _VC_popupOptions[id])
    VoiceConfigPopupTop.Hide()

def VCInputCallback(id, dev):
    VoiceConfigFrameInputDevice.SetText(dev)
    MarsVoice.SetInputDevice(id)

def VCOutputCallback(id, dev):
    VoiceConfigFrameOutputDevice.SetText(dev)
    MarsVoice.SetOutputDevice(id)

# Initialize panel widgets with values from MarsVoice module
def VCInit():
    VoiceConfigFrameOutputDevice.SetText(MarsVoice.GetOutputDeviceName())
    VoiceConfigFrameOutputLevel.SetValue(MarsVoice.GetOutputLevel())
    VoiceConfigFrameInputDevice.SetText(MarsVoice.GetInputDeviceName())
    VoiceConfigFrameInputLevel.SetValue(MarsVoice.GetInputLevel())
    VoiceConfigFrameEnableVoice.SetChecked(MarsVoice.GetVoiceEnabled())
    VoiceConfigFrameEnableInput.SetChecked(MarsVoice.GetInputEnabled())
    _, pttLocked, _ = MarsVoice.GetPushToTalkState()
    VoiceConfigFrameEnablePPT.SetChecked(not pttLocked)
    VoiceConfigFrameEnableVA.SetChecked(pttLocked)
    VoiceConfigFrameEnableTest.SetChecked(MarsVoice.GetTestMode())
    VoiceConfigFramePartyVoice.SetChecked(MarsGroup.GetAutoJoinPartyChat())      
    UpdateServerIndicator()

def UpdateServerIndicator():
    if Voice.ConnectedToVoiceServer():
        VoiceConfigFrameServerIndicatorTexture.SetVertexColor(0.0, 1.0, 0.0)
    else:
        VoiceConfigFrameServerIndicatorTexture.SetVertexColor(1.0, 0.0, 0.0)

def ToggleVoiceConfig():
    if VoiceConfigFrame.IsVisible():
        MarsVoice.SaveConfigSettings()
        VoiceConfigFrame.Hide()
    else:
        VoiceConfigFrame.Show()

def VCClickPPT():
    VoiceConfigFrameEnablePPT.SetChecked(True)
    VoiceConfigFrameEnableVA.SetChecked(False)
    MarsVoice.UnlockPushToTalk()

def VCClickVA():
    VoiceConfigFrameEnablePPT.SetChecked(False)
    VoiceConfigFrameEnableVA.SetChecked(True)
    MarsVoice.LockPushToTalk(True)

def VCClickInputEnable():
    enabled = not MarsVoice.GetInputEnabled()
    MarsVoice.SetInputEnabled(enabled)
    VoiceConfigFrameEnableInput.SetChecked(enabled)

def VCSetAutoJoinPartyChat(frame):
    MarsGroup.SetAutoJoinPartyChat(not frame.GetChecked())
    frame.SetChecked(not frame.GetChecked())
    MarsVoice.UpdateVoiceConfig()             

def VCTestRecording():
    if MarsVoice.GetVoiceEnabled() == True:
        MarsVoice.SetVoiceEnabled(False)
    VoiceConfigFrameEnableVoice.SetChecked(False)
    #VoiceConfigFrameRecordButtonNormalText.SetJustifyH("CENTER")
    if VoiceConfigFrameRecordButton.GetText() == "Start Record":
        MarsVoice._StartTestRecording()
        VoiceConfigFrameRecordButton.SetText("Stop Record")
    else:
        MarsVoice._StopVoiceManager()
        VoiceConfigFrameRecordButton.SetText("Start Record")

def VCTestPlayback():
    if MarsVoice.GetVoiceEnabled() == True:
        MarsVoice.SetVoiceEnabled(False)
    VoiceConfigFrameEnableVoice.SetChecked(False)
    #VoiceConfigFramePlaybackButtonNormalText.SetJustifyH("CENTER")
    if VoiceConfigFramePlaybackButton.GetText() == "Start Playback":
        MarsVoice._PlaybackTestRecording()
        VoiceConfigFramePlaybackButton.SetText("Stop Playback")
    else:
        MarsVoice._StopVoiceManager()
        VoiceConfigFramePlaybackButton.SetText("Start Playback")
