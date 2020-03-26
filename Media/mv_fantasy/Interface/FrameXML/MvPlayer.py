def PlayerFrame_OnLoad(frame):
    frame.RegisterEvent("PLAYER_ENTERING_WORLD")
    
def PlayerFrame_OnEvent(frame, event):
    UnitFrame_OnEvent(frame, event)
    
    if event.eventType == "PLAYER_ENTERING_WORLD":
        UnitFrame_Update(PlayerFrame)
