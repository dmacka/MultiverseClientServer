import MarsUnit

def TargetFrame_OnLoad(frame):
    frame.RegisterEvent("PROPERTY_health")
    frame.RegisterEvent("PLAYER_TARGET_CHANGED")
    
def TargetFrame_Update(frame):
    if MarsUnit.UnitExists("target"):
        frame.Show()
        UnitFrame_Update(frame)
        TargetFrame_CheckDead()
    else:
        frame.Hide()

def TargetFrame_OnEvent(frame, event):
    UnitFrame_OnEvent(frame, event)
    if event.eventType == "PROPERTY_health":
        TargetFrame_CheckDead()
    elif event.eventType == "PLAYER_TARGET_CHANGED":
        TargetFrame_Update(frame)
        
def TargetFrame_CheckDead():
    if MarsUnit.UnitIsDead("target"):
        TargetDeadText.Show()
    else:
        TargetDeadText.Hide()

TargetFrame.Hide()
PlayerName.SetJustifyH("CENTER")
TargetName.SetJustifyH("CENTER")
PlayerFrameHealthBar.Show()
PlayerFrameManaBar.Show()
TargetFrameHealthBar.Show()
TargetFrameManaBar.Show()

