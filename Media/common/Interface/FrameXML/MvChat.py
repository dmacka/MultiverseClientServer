import ClientAPI

import MarsCommand

_currentOutputFrame = 0

def MvChatFrame_OnLoad(frame):
    MvChatSelectOutput(0)
    MvChatFrameOutputSelectFrame.Show()
    MvChatFrameOutputSelectFrameButton0.Show()
    MvChatFrameOutputTexture.SetAlpha(0.0)
    MvChatFrameOutput.Show()
    MvChatFrameInputFrameTexture.SetAlpha(0.7)

def MvChatSelectOutput(tab):
    global _currentOutputFrame
    
    for j in range(0, 5):
        texture = getglobal("MvChatFrameOutputSelectFrameButton%dTexture" % (j))
        texture.SetVertexColor(0.1, 0.1, 0.1)
        if (j == tab):
            texture.SetAlpha(0.5)
        else:
            texture.SetAlpha(0.3)

    if(_currentOutputFrame == tab):
        return
    
    #Hide current, show new
    curFrame = getglobal("MvChatFrameOutputScrollingMessageFrame%d" % (_currentOutputFrame))
    if curFrame != None:
        curFrame.Hide()

    _currentOutputFrame = tab

    newFrame = getglobal("MvChatFrameOutputScrollingMessageFrame%d" % (tab))
    if newFrame != None:
        newFrame.Show()

def MvChatFrame_OnEnter(frame):
    global _currentOutputFrame
    MvChatFrameOutputTexture.SetAlpha(0.6)
    for j in range(0, 5):
        if j != _currentOutputFrame:
            button = getglobal("MvChatFrameOutputSelectFrameButton%d" % (j))
            button.Show()

def MvChatFrame_OnLeave(frame):
    global _currentOutputFrame
    MvChatFrameOutputTexture.SetAlpha(0.0)
    for j in range(0, 5):
        if j != _currentOutputFrame:
            button = getglobal("MvChatFrameOutputSelectFrameButton%d" % (j))
            button.Hide()

def MvChatFrameInputFrame_OnMouseDown(frame):
    editBox = getglobal(frame.Name + "EditBox")
    editBox.Show()
    editBox.SetFocus()

def MvChatFrameInputFrameEditBox_OnEnterPressed(frame):
    global _currentOutputFrame
    text = frame.GetText()
    if _currentOutputFrame == 2 and not text.startswith("/"):
        text = "/group " + text
    MarsCommand.HandleCommand(text)
    if len(text) > 0:
        frame.AddHistoryLine(text)
    MvChatFrameInputFrameEditBox_OnEscapePressed(frame)
    
def MvChatFrameInputFrameEditBox_OnEscapePressed(frame):
    frame.SetText("")
    # I should make Hide automatically clear the focus
    frame.ClearFocus()
    frame.Hide()

def MvChatFrameOutputScrollingMessageFrame_OnLoad(frame):
    if frame.GetID() == 2: #Group Chat is only special case right now
        frame.RegisterEvent("CHAT_MSG_GROUP")
    else:
        frame.RegisterEvent("CHAT_MSG_SAY")
        frame.RegisterEvent("CHAT_MSG_SYSTEM")
        frame.RegisterEvent("CHAT_MSG_COMBAT_MISC_INFO")
        frame.RegisterEvent("CHAT_MSG_COMBAT_CREATURE_VS_SELF_HITS")
        frame.RegisterEvent("CHAT_MSG_COMBAT_CREATURE_VS_CREATURE_HITS")
        frame.RegisterEvent("CHAT_MSG_CHANNEL")
        # frame.RegisterEvent("CHAT_MSG_GROUP")
        # frame.RegisterEvent("CHAT_MSG_GUILD")
        frame.RegisterEvent("CHAT_MSG_TELL")
        frame.RegisterEvent("TRAINING_INFO")
        frame.RegisterEvent("CLASSABILITY_REPORT")
        frame.RegisterEvent("CHAT_MSG_COMBAT_ABILITY_MISSED")

def MvChatFrameOutputScrollingMessageFrame_OnEvent(frame, args):
    if frame.GetID() == 0:
        if args.eventType == "CHAT_MSG_SAY":
            text = "[%s]: %s" % (args.eventArgs[1], args.eventArgs[0])
            frame.AddMessage(text, 1.0, 1.0, 1.0, 1)
        elif args.eventType == "CHAT_MSG_SYSTEM":
            text = args.eventArgs[0]
            frame.AddMessage(text, 0.3, 0.9, 0.3, 2)
        elif args.eventType == "CHAT_MSG_COMBAT_MISC_INFO":
            text = args.eventArgs[0]
            frame.AddMessage(text, 0.3, 0.3, 0.9, 3)
        elif args.eventType == "CHAT_MSG_COMBAT_CREATURE_VS_SELF_HITS":
            text = args.eventArgs[0]
            frame.AddMessage(text, 0.9, 0.3, 0.3, 4)
        elif args.eventType == "CHAT_MSG_COMBAT_CREATURE_VS_CREATURE_HITS":
            text = args.eventArgs[0]
            frame.AddMessage(text, 0.8, 0.8, 0.4, 5)
        elif args.eventType == "CLASSABILITY_REPORT":
            text = args.eventArgs[0]
            frame.AddMessage(text, 0.9, 0.9, 0.9, 2)
        elif args.eventType == "CHAT_MSG_GROUP":
            text = args.eventArgs[0]
            # frame.AddMessage(text, 1.0, 1.0, 1.0, 1)
        elif args.eventType == "CHAT_MSG_GUILD":
            text = args.eventArgs[0]
            # frame.AddMessage(text, 1.0, 1.0, 1.0, 1)
        elif args.eventType == "CHAT_MSG_TELL":
            text = args.eventArgs[0]
            frame.AddMessage(text, 1.0, 1.0, 1.0, 1)
        elif args.eventType == "CHAT_MSG_CHANNEL":
            if args.eventArgs[6] == "0":
                # this is an internally generated message
                text = args.eventArgs[0]
                frame.AddMessage(text, 1.0, 1.0, 1.0, 0)
            else:
                # this is a message on some special channel
                text = "[%s] [%s]: %s" % (args.eventArgs[6], args.eventArgs[1], args.eventArgs[2])
                frame.AddMessage(text, 1.0, 1.0, 1.0, int(args.eventArgs[6]))
        elif args.eventType == "TRAINING_INFO":
            text = args.eventArgs[0]
            frame.AddMessage(text, 0.3, 0.3, 0.9, 2)
    elif frame.GetID() == 2: # Group Chat
        if args.eventType == "CHAT_MSG_GROUP":
            text = args.eventArgs[0]
            frame.AddMessage(text, 1.0, 1.0, 1.0, 1)        
 
def MvChatOutputSelectButton_OnClick(frame):
    MvChatSelectOutput(frame.GetID())

def MvChatFrameOutputScrollingMessageFrame_ScrollUp():
    curFrame = getglobal("MvChatFrameOutputScrollingMessageFrame%d" % (_currentOutputFrame))
    curFrame.ScrollUp()

def MvChatFrameOutputScrollingMessageFrame_ScrollDown():
    curFrame = getglobal("MvChatFrameOutputScrollingMessageFrame%d" % (_currentOutputFrame))
    curFrame.ScrollDown()
