import ClientAPI
import MarsTarget
import MarsVoice

_groupMembers = {}
_groupOid = long(-1)
_autoJoinPartyChat = False
_existingGroupMember = False

# GetNumGroupMembers - Returns the number of players in the group
def GetNumGroupMembers():
    global _groupMembers
    return len(_groupMembers)

# GetGroupMemberName - Gets the name at the specific index
def GetGroupMemberName(slotId):
    global _groupMembers
    if not _groupMembers.has_key(slotId):
        ClientAPI.Log("MarsGroup key not found! : " + str(slotId))
        return ""
    return _groupMembers[slotId].memberName

# GetGroupMemberOid - Returns the player's unique OID at the given index
def GetGroupMemberOid(slotId):
    global _groupMembers
    if not _groupMembers.has_key(slotId):
        return 0
    return _groupMembers[slotId].memberOid

# GetGroupMemberMaxHealth - Get the player's maximum health value at the given index
def GetGroupMemberMaxHealth(slotId):
    global _groupMembers
    if not _groupMembers.has_key(slotId):
        return 0
    return _groupMembers[slotId].memberHealthMax

# GetGroupMemberHealth - Returns the player's current health vaue at the given index
def GetGroupMemberHealth(slotId):
    global _groupMembers
    if not _groupMembers.has_key(slotId):
        return 0
    return _groupMembers[slotId].memberHealth

# GetGroupOid - Returns the unique key associated with the group. Also used for the key for the voice group
def GetGroupOid():
    global _groupOid
    return _groupOid

# CheckTarget - Add validation checks to ensure the target being invited to the group is valid
def CheckTarget(target):
    global _groupMembers

    for groupIndex in _groupMembers:
        groupMember = _groupMembers[groupIndex]
        if groupMember.memberOid == target.OID:
            return False; # Target is already in the group
    return True

# RemoveGroupMember - Removes player from the group at the given index
def RemoveGroupMember(slotId):
    props = { "target" : long(GetGroupMemberOid(slotId)) }
    ClientAPI.Network.SendExtensionMessage(0, False, "mv.GROUP_REMOVE_MEMBER", props)

# SendInviteRequestMessage - Sends message to the server to send the targeted player an invite message
def SendInviteRequestMessage(targetOid):
    # Only allow player to invite if they are the gorup leader or not in a group
    if GetNumGroupMembers() == 0 or GetGroupMemberOid(1) == ClientAPI.GetPlayerObject().OID:
        props = { "target" : targetOid }
        ClientAPI.Network.SendExtensionMessage(0, False, "mv.GROUP_INVITE", props)

# SendInviteResponseMessage - Sends a message response advising if the group invite was accepted or not
def SendInviteResponseMessage(groupLeaderOid, response):
    groupVoiceEnabled = False
    if MarsVoice.GetVoiceEnabled() and GetAutoJoinPartyChat():
        groupVoiceEnabled = True

    props = {"groupLeaderOid" : groupLeaderOid,
             "response" : response,
             "groupVoiceEnabled" : groupVoiceEnabled}
    ClientAPI.Network.SendExtensionMessage(0, False, "mv.GROUP_INVITE_RESPONSE", props)

# SendGroupChatMessage - Sends a Group chat message to all group members
def SendGroupChatMessage(message):
    props = {"senderOid" : ClientAPI.GetPlayerObject().OID, "message" : message}
    ClientAPI.Network.SendExtensionMessage(0, False, "mv.GROUP_CHAT", props)

# LeaveGroup - Removes the local player form their group
def LeaveGroup():
    global _existingGroupMember
    _existingGroupMember = False
    if(GetNumGroupMembers() > 0):
        MarsVoice.JoinVoiceGroup(0) #Leave party voice chat
    props = { "target" : ClientAPI.GetPlayerObject().OID }
    ClientAPI.Network.SendExtensionMessage(0, False, "mv.GROUP_REMOVE_MEMBER", props)
    ClientAPI.Interface.DispatchEvent("CHAT_MSG_GROUP", ["You leave your group.", ""])

# GetGroupMemberSlotIndex - Retrieves a player's group index based on their OID
def GetGroupMemberSlotIndex(groupMemberOid):
    global _groupMembers

    for groupIndex in _groupMembers:
        if _groupMembers[groupIndex].memberOid == groupMemberOid:
            return groupIndex
    return 0

# GetGroupMemberVoiceEnabled - Returns if a group member at a given index has their voice enabled
def GetGroupMemberVoiceEnabled(slotId):
    global _groupMembers
    if _groupMembers.has_key(slotId):
        return _groupMembers[slotId].voiceEnabled
    return False

# GetGroupLeaderOid - Returns the OID for the gorup leader, which is always at index 1
def GetGroupLeaderOid():
    global _groupMembers
    # Group Leader should always be in the first position, this is set by the server
    return _groupMembers[1].memberOid

# MuteTarget - Mutes the player at the given index in the group
def MuteTarget(slotId):
    global _groupMembers
    if _groupMembers.has_key(slotId):
        groupMember = _groupMembers[slotId]
        props = {"target" : groupMember.memberOid,
                 "setter" : ClientAPI.GetPlayerObject().OID, # Used on server for validation
                 "groupOid" : GetGroupOid()}
        ClientAPI.Network.SendExtensionMessage(0, False, "mv.GROUP_SET_ALLOWED_SPEAKER", props)
        
# MuteGroup - Mutes all group members except for the group leader         
def MuteGroup():
    props = {"groupOid" : GetGroupOid(),
          "setter" : ClientAPI.GetPlayerObject().OID} # Used on server for validation
    ClientAPI.Network.SendExtensionMessage(0, False, "mv.GROUP_MUTE_VOICE_CHAT", props)

# GetAutoJoinPartyChat - Returns a value advising if the player is set to join group voice chat or not
def GetAutoJoinPartyChat():
    global _autoJoinPartyChat
    return _autoJoinPartyChat

# SetAutoJoinPartyChat - Sets system to join group voice chat if the voice client is enabled
def SetAutoJoinPartyChat(value):
    global _autoJoinPartyChat
    global _groupMembers
    
    _autoJoinPartyChat = value
    
    if len(_groupMembers) > 0:
        # Send message to server to update other group members on this player's voice status
        props = {"playerOid" : ClientAPI.GetPlayerObject().OID,
                 "groupOid" : GetGroupOid(),
                 "voiceEnabled" : _autoJoinPartyChat}
        ClientAPI.Network.SendExtensionMessage(0, False, "mv.GROUP_VOICE_CHAT_STATUS", props)

# GetGroupMemberAllowedSpeaker - Returns value that tells if a person is allowed to speak in voice chat or not. If this is false, the player is effectively muted.
def GetGroupMemberAllowedSpeaker(slotId):
    global _groupMembers
    if _groupMembers.has_key(slotId):
        return _groupMembers[slotId].allowedSpeaker
    return False
        
# GroupMember - Client side representation of each group member.
class GroupMember:
    def __init__(self):
        self.memberOid = long(0)
        self.memberName = ""
        self.memberHealth = 0
        self.memberHealthMax = 0
        self.voiceEnabled = False
        self.allowedSpeaker = True

    def __str__(self):
        return "MarsGroup.GroupEntry '%s' '%s' '%s' '%s'" % (self.memberOid, self.memberName, self.memberHealth, self.voiceEnabled)

#
# Handles group level updates. Occurs when a group is created, a member leaves or is added.
#
def _HandleGroupUpdate(props):
    global _groupMembers
    global _groupOid
    global _existingGroupMember

    _groupMembers.clear()
    _groupOid = long(0)

    keys = props.keys() ##numeric value defining group member's position in group. 1 = group leader

    for key in keys:
        memberInfo = props[key]
        if isinstance(memberInfo,dict):
            groupMember = GroupMember()
            groupMember.memberOid = long(memberInfo["memberOid"])
            groupMember.memberName = memberInfo["name"]
            groupMember.memberHealth = memberInfo["health"]
            groupMember.memberHealthMax = memberInfo["health-max"]
            groupMember.voiceEnabled = bool(memberInfo["voiceEnabled"])
            groupMember.allowedSpeaker = bool(memberInfo["allowedSpeaker"])
            _groupMembers[int(key)] = groupMember
            ClientAPI.Log("MarsGroup._HandleGroupUpdate : Group member info - " + str(groupMember))
    if len(_groupMembers) > 0:
        _groupOid = long(props["groupOid"])
        # If this client just joined the gorup then set existing flag and run JoinVoiceGroup
        #  We only wanted to run the JoinVoiceGroup once, if disabled then they can manually join later
        if not _existingGroupMember:
            _existingGroupMember = True
            if GetAutoJoinPartyChat():
                MarsVoice.JoinVoiceGroup(_groupOid)         

    ClientAPI.Interface.DispatchEvent("GROUP_UPDATE",[])

#
# Handles property updates for specific group members
#
def _HandleGroupPropertyUpdate(props):
    global _groupMembers

    memberOid = long(props["memberOid"])
    for groupIndex in _groupMembers:
        groupMember = _groupMembers[groupIndex]
        if groupMember.memberOid == memberOid:
            if props.has_key("health"):
                groupMember.memberHealth = int(props["health"])
            if props.has_key("health-max"):
                groupMember.memberHealthMax = int(props["health-max"])
            if props.has_key("allowedSpeaker"):
                groupMember.allowedSpeaker = bool(props["allowedSpeaker"])                 
            if props.has_key("voiceEnabled"):
                groupMember.voiceEnabled = bool(props["voiceEnabled"])                
            ClientAPI.Interface.DispatchEvent("GROUP_PROPERTY_UPDATE",[str(groupIndex)])
            return
        
#
# Handles group invite requests
#
def _HandleGroupInviteRequest(props):
    groupLeaderOid = props["groupLeaderOid"]
    groupLeaderName = props["groupLeaderName"]    
    ClientAPI.Interface.DispatchEvent("GROUP_INVITE_REQUEST",[str(groupLeaderOid), groupLeaderName])


ClientAPI.Network.RegisterExtensionMessageHandler("mv.GROUP_UPDATE", _HandleGroupUpdate)
ClientAPI.Network.RegisterExtensionMessageHandler("mv.GROUP_PROPERTY_UPDATE", _HandleGroupPropertyUpdate)
ClientAPI.Network.RegisterExtensionMessageHandler("mv.GROUP_INVITE_REQUEST", _HandleGroupInviteRequest)

