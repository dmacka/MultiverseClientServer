def PlayerFrame_OnLoad(frame):
    PlayerLevelText.SetText(UnitLevel("player").ToString())
    PlayerFrame_UpdatePartyLeader()
    PlayerFrame_UpdatePvpStatus()
    # frame.RegisterEvent("UNIT_COMBAT")
    # frame.RegisterEvent("UNIT_LEVEL")
    frame.RegisterEvent("UNIT_PVP_UPDATE")
    frame.RegisterEvent("PLAYER_ENTER_COMBAT")
    frame.RegisterEvent("PLAYER_LEAVE_COMBAT")
    frame.RegisterEvent("PLAYER_REGEN_DISABLED")
    frame.RegisterEvent("PLAYER_REGEN_ENABLED")
    frame.RegisterEvent("PARTY_LEADER_CHANGED")
    frame.RegisterEvent("PLAYER_ENTERING_WORLD")
    # Set up these properties
    PlayerFrame.Properties["inCombat"] = False
    PlayerFrame.Properties["onHateList"] = False
    # Set the background
    PlayerAttackBackground.SetVertexColor(.8, .1, .1, .4)
    

def PlayerFrame_UpdatePartyLeader():
    if IsPartyLeader():
        PlayerLeaderIcon.Show()
    else:
        PlayerLeaderIcon.Hide()

def PlayerFrame_UpdatePvpStatus():
    if UnitIsPVP("player"):
        PlayerPVPIcon.Show()
    else:
        PlayerPVPIcon.Hide()

def PlayerFrame_OnEvent(frame, event):
    UnitFrame_OnEvent(frame, event)
    
    if event.eventType == "UNIT_LEVEL":
        unit = event.eventArgs[0]
        if unit == "player":
            PlayerLevelText.SetText(UnitLevel("player").ToString())
    elif event.eventType == "UNIT_PVP_UPDATE":
        unit = event.eventArgs[0]
        if unit == "player":
            PlayerFrame_UpdatePvPStatus()
    elif event.eventType == "PLAYER_ENTERING_WORLD":
        PlayerFrame.Properties["inCombat"] = False
        PlayerFrame.Properties["onHateList"] = False
        UnitFrame_Update(PlayerFrame)
        PlayerFrame_UpdateStatus()
    elif event.eventType == "PLAYER_ENTER_COMBAT":
        PlayerFrame.Properties["inCombat"] = True
        PlayerFrame_UpdateStatus()
    elif event.eventType == "PLAYER_LEAVE_COMBAT":
        PlayerFrame.Properties["inCombat"] = False
        PlayerFrame_UpdateStatus()
    elif event.eventType == "PLAYER_REGEN_DISABLED":
        PlayerFrame.Properties["onHateList"] = True
        PlayerFrame_UpdateStatus()
    elif event.eventType == "PLAYER_REGEN_ENABLED":
        PlayerFrame.Properties["onHateList"] = False
        PlayerFrame_UpdateStatus()
    elif event.eventType == "PARTY_LEADER_CHANGED":
        PlayerFrame_UpdatePartyLeader()
    # handle enter world?

def PlayerFrame_UpdateStatus():
    if PlayerFrame.Properties["inCombat"]:
        PlayerStatusTexture.SetVertexColor(1, 0, 0, 1)
        PlayerStatusTexture.Show()
        PlayerAttackIcon.Show()
        PlayerAttackGlow.Show()
        PlayerStatusGlow.Show()
        PlayerAttackBackground.Show()
    elif PlayerFrame.Properties["onHateList"]:
        PlayerAttackIcon.Show()
        PlayerStatusGlow.Hide()
        PlayerAttackBackground.Hide()
    else:
        PlayerStatusTexture.Hide()
        PlayerAttackIcon.Hide()
        PlayerStatusGlow.Hide()
        PlayerAttackBackground.Hide()
            
PlayerRestIcon.Hide()
PlayerRestGlow.Hide()
PlayerAttackIcon.Hide()
PlayerAttackGlow.Hide()
PlayerAttackBackground.Hide()
PlayerStatusTexture.Hide()
PlayerStatusGlow.Hide()

