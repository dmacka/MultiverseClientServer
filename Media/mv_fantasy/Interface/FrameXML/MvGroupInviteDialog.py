import ClientAPI
import MarsGroup

_groupLeaderOid = long(0)

def MvGroupInviteDialog_OnLoad(frame):
    frame.RegisterEvent("GROUP_INVITE_REQUEST")

def MvGroupInviteDialog_OnEvent(frame, event):
    global _groupLeaderOid
    ClientAPI.Log("*************Got " + event.eventType + " Message")
    if(event.eventType == "GROUP_INVITE_REQUEST"):
        inviteMessage = event.eventArgs[1] + " has invited you to join their group."
        _groupLeaderOid = long(event.eventArgs[0])
        MvGroupInviteMessage.SetText(inviteMessage)
        MvGroupInviteDialogFrame.Show()

def MvGroupInviteAcceptButton_OnClick(this):
    MarsGroup.SendInviteResponseMessage(_groupLeaderOid, "accept")
    MvGroupInviteDialogFrame.Hide()

def MvGroupInviteDeclineButton_OnClick(this):
    MarsGroup.SendInviteResponseMessage(_groupLeaderOid, "decline")    
    MvGroupInviteDialogFrame.Hide()
