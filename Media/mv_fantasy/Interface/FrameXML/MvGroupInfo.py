import ClientAPI
import MarsTarget

_voiceEnabled = False

def MvGroupMember_OnClick(frame):
    if not frame.IsEnabled():
        return

    if frame.GetChecked():
        frame.SetChecked(0)
        frame.SetTextColor(1.0,1.0,1.0)
    else:
        for i in range(1, 8):
            skillButton = getglobal("GroupMember%d" % i)
            if skillButton.IsEnabled():                
                skillButton.SetChecked(0)    
                skillButton.SetTextColor(1.0,1.0,1.0)
        frame.SetChecked(1)
        frame.SetTextColor(1.0,0.0,0.0)
        ## Set current target to group member selected
        MarsTarget.TargetByOID(MarsGroup.GetGroupMemberOid(frame.GetID()))

    return    

def MvGroupInfoFrame_OnLoad(frame):
    frame.RegisterEvent("GROUP_UPDATE")
    frame.RegisterEvent("GROUP_PROPERTY_UPDATE")
    frame.RegisterEvent("VOICE_ALLOCATION")
    frame.RegisterEvent("VOICE_DEALLOCATION")

def MvGroupInfoFrame_OnShow(this):
    SetButtonDisplay()

def MvGroupInfoFrame_OnEvent(this, event):
    if(event.eventType == "GROUP_UPDATE"):
        ClearGroupMembers()
        UpdateGroupInfo()
        SetButtonDisplay()
    elif(event.eventType == "GROUP_PROPERTY_UPDATE"):
        SetGroupMemberInfo(int(event.eventArgs[0]))
    elif(event.eventType == "VOICE_ALLOCATION"):
        if MarsGroup.GetNumGroupMembers()>0:
            SetVoiceIndicator(int(event.eventArgs[0]), True)
    elif(event.eventType == "VOICE_DEALLOCATION"):
        if MarsGroup.GetNumGroupMembers()>0:
            SetVoiceIndicator(int(event.eventArgs[0]), False)

# SetGroupMemberInfo - Set visual display for the MvGroupInfoFrame widget
def SetGroupMemberInfo(slotId):
    global _voiceEnabled
        
    playerFrame = getglobal("GroupMember%sFrame" % slotId)
    if not playerFrame.IsVisible():
        playerFrame.Show()
        
    playerName = getglobal("GroupMember%s" % slotId)
    playerName.SetText(MarsGroup.GetGroupMemberName(slotId))    
    playerHealth = getglobal("GroupMember%sHealthBar" % slotId)
    playerHealth.SetMinMaxValues(0,MarsGroup.GetGroupMemberMaxHealth(slotId))    
    playerHealth.SetValue(MarsGroup.GetGroupMemberHealth(slotId))    

    if not MarsGroup.GetGroupMemberVoiceEnabled(slotId):
        _voiceEnabled = False
        SetVoiceIcon(slotId, "disabled")
    elif not MarsGroup.GetGroupMemberAllowedSpeaker(slotId):    
        _voiceEnabled = False
        # if current player is being updated then make sure muted is checked    
        if ClientAPI.GetPlayerObject().OID == MarsGroup.GetGroupMemberOid(slotId):
            actionFrame = "MvGroupMemberFrame"
            if ClientAPI.GetPlayerObject().OID == MarsGroup.GetGroupLeaderOid():
                actionFrame = "MvGroupLeaderFrame"
            muteButton = getglobal(actionFrame + "PartyVoiceConfigMuteSelfButton")
            muteButton.SetChecked(1)
        SetVoiceIcon(slotId, "muted")       
    elif MarsGroup.GetGroupMemberVoiceEnabled(slotId) and not _voiceEnabled:
        _voiceEnabled = True
        SetVoiceIcon(slotId, "enabled")
        # if current player is being updated then make sure muted is not checked    
        if ClientAPI.GetPlayerObject().OID == MarsGroup.GetGroupMemberOid(slotId):
            actionFrame = "MvGroupMemberFrame"
            if ClientAPI.GetPlayerObject().OID == MarsGroup.GetGroupLeaderOid():
                actionFrame = "MvGroupLeaderFrame"
            muteButton = getglobal(actionFrame + "PartyVoiceConfigMuteSelfButton")
            muteButton.SetChecked(0)        
              
def ClearGroupMembers():
    for i in range(1, 8):
        playerFrame = getglobal("GroupMember%sFrame" % i)
        if playerFrame.IsVisible():
            playerFrame.Hide()
            playerName = getglobal("GroupMember%s" % i)
            playerName.SetText("")
            playerName.SetChecked(0)
            playerName.SetTextColor(1.0,1.0,1.0)
            playerHealth = getglobal("GroupMember%sHealthBar" % i)
            playerHealth.SetMinMaxValues(0,0)
            playerHealth.SetValue(0) 
            SetVoiceIcon(i,"")

def UpdateGroupInfo():
    numMembers = MarsGroup.GetNumGroupMembers()
    for i in range(1, numMembers+1):
        SetGroupMemberInfo(i)

#SetButtonDisplay - Determines which button grouping displays at the bottom of the frame
def SetButtonDisplay():
    MvUnGroupedFrame.Hide()
    MvGroupLeaderFrame.Hide()
    MvGroupMemberFrame.Hide()
    #Grouped or not?
    if MarsGroup.GetNumGroupMembers() > 0:
        # Group leader or not?
        if MarsGroup.GetGroupLeaderOid() == ClientAPI.GetPlayerObject().OID:
            MvGroupLeaderFrame.Show()
        else:
            MvGroupMemberFrame.Show()
    else:
        MvUnGroupedFrame.Show()        

# SetVoiceIndicator - sets the voice icon indicator next to each group member based on their voice status
def SetVoiceIndicator(playerOid, speaking):
    slotId = MarsGroup.GetGroupMemberSlotIndex(playerOid)
    if speaking:
        SetVoiceIcon(slotId, "talking")
    else:
        SetVoiceIcon(slotId, "enabled")

def MvInvitePlayerButton_OnClick(frame):
    target = MarsTarget.GetCurrentTarget()
    if target == None :
        ClientAPI.Write("No target")
        return
    
    if MarsGroup.CheckTarget(target):
        #Send message to server that we would like to invite the target
        MarsGroup.SendInviteRequestMessage(target.OID)
        
def MvRemovePlayerButton_OnClick(frame):
    buttonText = frame.GetText()

    for i in range(1, 8):
        button = getglobal("GroupMember%d" % i)
        if button.GetChecked():
            MarsGroup.RemoveGroupMember(i)
            return        
    ClientAPI.Write("You must select a group member to remove.")
    
def MvLeaveGroupButton_OnClick(frame):       
    MarsGroup.LeaveGroup()

def MvMuteSelectedButton_OnClick(frame):
    for i in range(1, 8):
        button = getglobal("GroupMember%d" % i)
        if button.GetChecked(): 
            MarsGroup.MuteTarget(i)

def MvMuteAllButton_OnClick(frame):
    MarsGroup.MuteGroup()
             
def MvMuteSelfButton_OnClick(frame):    
    # Find out which slot we are in and mute ourselves
    slotId = MarsGroup.GetGroupMemberSlotIndex(ClientAPI.GetPlayerObject().OID)
    MarsGroup.MuteTarget(slotId)

def MvJoinVoiceChatButton_OnClick(frame):
    if frame.GetChecked():
        # If not set to join party chat then enable it
        if not MarsGroup.GetAutoJoinPartyChat():
            MarsGroup.SetAutoJoinPartyChat(True)
    
        # Enable voice if not enabled and update voice config which should now auto-add us to the
        # party voice chat group
        if not MarsVoice.GetVoiceEnabled():
            # Need to set voice group here since SetVoiceEnabled re-configures voice client
            MarsVoice.SetVoiceGroupOid(MarsGroup.GetGroupOid())
            MarsVoice.SetVoiceEnabled(True)
        else:
            MarsVoice.JoinVoiceGroup(MarsGroup.GetGroupOid())
    else:
        # Leave voice group
        MarsGroup.SetAutoJoinPartyChat(False)
        MarsVoice.JoinVoiceGroup(0)

def SetVoiceIcon(slotId, state):
    voiceIndicatorEnabled = getglobal("GroupMemberVoiceIndicator%sEnabled" % slotId)
    voiceIndicatorDisabled = getglobal("GroupMemberVoiceIndicator%sDisabled" % slotId)
    voiceIndicatorTalking = getglobal("GroupMemberVoiceIndicator%sTalking" % slotId)
    voiceIndicatorMuted = getglobal("GroupMemberVoiceIndicator%sMuted" % slotId)
    
    if voiceIndicatorEnabled == None:
        return
    voiceIndicatorEnabled.Hide()
    voiceIndicatorDisabled.Hide()
    voiceIndicatorTalking.Hide()
    voiceIndicatorMuted.Hide()
    
    if state == "enabled":
        voiceIndicatorEnabled.Show()
    elif state == "disabled":
        voiceIndicatorDisabled.Show()
    elif state == "talking":
        voiceIndicatorTalking.Show()
    elif state == "muted":
        voiceIndicatorMuted.Show()    
