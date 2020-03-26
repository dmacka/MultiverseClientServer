def TargetFrame_OnLoad(frame):
    frame.RegisterEvent("UNIT_HEALTH")
    frame.RegisterEvent("PLAYER_TARGET_CHANGED")
    
def TargetFrame_Update(frame):
    if UnitExists("target"):
        frame.Show()
        UnitFrame_Update(frame)
        TargetFrame_CheckDead()
    else:
        frame.Hide()

def TargetFrame_OnEvent(frame, event):
    UnitFrame_OnEvent(frame, event)
    if event.eventType == "UNIT_HEALTH":
        TargetFrame_CheckDead()
    elif event.eventType == "PLAYER_TARGET_CHANGED":
        TargetFrame_Update(frame)
        
def TargetFrame_CheckDead():
    if UnitHealth("target") <= 0:
        TargetDeadText.Show()
    else:
        TargetDeadText.Hide()

TargetFrame.Hide()
PlayerName.SetJustifyH("CENTER")
TargetName.SetJustifyH("CENTER")
PlayerFrameHealthBar.SetStatusBarColor(1, 0, 0)
PlayerFrameHealthBar.Show()
PlayerFrameManaBar.Show()
TargetFrameHealthBar.SetStatusBarColor(1, 0, 0)
TargetFrameHealthBar.Show()
TargetFrameManaBar.Show()

