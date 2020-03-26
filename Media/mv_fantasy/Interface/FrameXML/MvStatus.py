import ClientAPI

def Status_OnLoad(frame):
    frame.SetPoint("TOPRIGHT", "UIParent", "TOPRIGHT", -13, -70)
    frame.SetHeight(95)
    frame.SetWidth(150)
    frame.SetBackdropColor(0, 0, 0)
    StatusTextLeft1.Show()
    StatusTextLeft2.Show()
    StatusTextLeft3.Show()
    StatusTextLeft4.Show()

def Status_OnUpdate(frame):
    if not frame.IsHidden:
        StatusTextLeft1.SetText("FPS: %d" % GetFramerate())
        StatusTextLeft2.SetText("Messages: %d/%d" % (GetMessageQueue(), GetMessagesPerSecond()))
        StatusTextLeft3.SetText("KBps: %s" % GetKBytesPerSecondString())
        StatusTextLeft4.SetText("Renders: %d" % GetLastFrameRenderCalls())

def ToggleStatus():
    if Status.IsVisible():
        Status.Hide()
    else:
        Status.Show()

def GetFramerate():
    return ClientAPI.SystemStatus.GetFramerate()

def GetMessageQueue():
    return ClientAPI.SystemStatus.GetMessageQueue()

def GetMessagesPerSecond():
    return ClientAPI.SystemStatus.GetMessagesPerSecond()

def GetBytesReceivedPerSecond():
    return ClientAPI.SystemStatus.GetBytesReceivedPerSecond()

def GetBytesSentPerSecond():
    return ClientAPI.SystemStatus.GetBytesSentPerSecond()

def GetKBytesPerSecondString():
    return "In %s/Out %s" % (_FormatKBytesPerSecond(GetBytesReceivedPerSecond()), _FormatKBytesPerSecond(GetBytesSentPerSecond))

def GetLastFrameRenderCalls():
    return ClientAPI.SystemStatus.GetLastFrameRenderCalls()

def _FormatKBytesPerSecond(bps):
    if bps < 100:
        return "0"
    fbps = float(bps)/1000
    if fbps < 10.0:
        return "%.1f" % fbps
    else:
        return str(int(fbps))

