import MarsUnit

def PlayerFrame_OnLoad(frame, texture):
    frame.RegisterEvent("PLAYER_ENTERING_WORLD")
    frame.RegisterEvent("PROPERTY_combatstate")
    frame.Properties["texture"] = texture
    
def PlayerFrame_OnEvent(frame, event):
    UnitFrame_OnEvent(frame, event)
    
    if event.eventType == "PLAYER_ENTERING_WORLD":
        UnitFrame_Update(PlayerFrame)
    if event.eventType == "PROPERTY_combatstate":
        PlayerFrame_Update(PlayerFrame)

def PlayerFrame_Update(frame):
    texture = frame.Properties["texture"]
    if MarsUnit.UnitAffectingCombat("player"):
        texture.SetVertexColor(1.0, 0.5, 0.5)
    else:
        texture.SetVertexColor(1.0, 1.0, 1.0)
