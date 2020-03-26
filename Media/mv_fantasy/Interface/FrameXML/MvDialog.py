import MarsQuest

MvAction_Func = [ lambda: 0,  lambda: 1,  lambda: 2,  lambda: 3,  lambda: 4,  lambda: 5,  lambda: 6,  lambda: 7,  lambda: 8,  lambda: 9]

def MvAction_OnEnter(frame):
	frame.SetTextColor(0,1,0)

def MvAction_OnLeave(frame):
	frame.SetTextColor(0,0,0)

def MvAction_OnClick(frame):
	i = int(frame.GetID())
	MvAction_Func[i-1]()
	frame.SetTextColor(0,0,1)

#
#
#

def MvInfoCloseButton_OnClick():
	MvInfoFrame.Hide()

def MvInfo_ShowFunc(name, icon, desc):
	"""Returns a function that calls MvInfo_Show().  Forces evaluation of the parameters."""
	return lambda: MvInfo_Show(name, icon, desc)

def MvInfo_Show(name, icon, desc=""):
	MvInfoFrame.Hide()
	MvInfoCaption.SetText(name)
	MvInfoIconTexture.SetTexture(icon)
#	MvInfoDescription.SetText(("This is the description of the %s %s." % (name, desc))*2)
	MvInfoFrame.Show()

#
#
#

def MvDialog_fMain_OnLoad_PreHook(frame):
	pass

def MvDialog_fMain_OnLoad_PostHook(frame):
	pass

def MvDialog_OnLoad(frame):
	MvDialog_fMain_OnLoad_PreHook(frame)
	frame.RegisterEvent("QUEST_DETAIL")
#	frame.RegisterEvent("QUEST_COMPLETE")
	MvDialog_fMain_OnLoad_PostHook(frame)

def MvDialog_OnEvent(frame, args):
	if args.eventType == "QUEST_DETAIL":
		MvDialog_QuestDetail_Update()
	if args.eventType == "QUEST_LOG_UPDATE":
		MvDialog_QuestLog_Update()
#	if args.eventType == "QUEST_COMPLETE":
#		MvDialog_QuestComplete_Update()

def MvDialog_OnShow():
	pass

def MvDialog_OnHide():
	MvInfoFrame.Hide()

def MvDialog_SetText(frame, text):
    frame.SetText(text)
    textHeight = frame.window.GetTextHeight(False)
    frame.SetHeight(int(textHeight))

def MvDialog_Init():
	for i in range(1, 6):

		header = getglobal("MvHeader%d" % i)
		header.SetText("")
		header.Hide()
		body = getglobal("MvBody%d" % i)
		body.SetText("")
		body.Hide()
	for i in range(1, 11):
		action = getglobal("MvAction%d" % i)
		action.SetText("")
		action.Hide()

def MvDialog_Attach(parent, child, place="BOTTOM"):
	child.SetPoint("TOPLEFT",  parent.GetName(), "%sLEFT"  % place, 0, 0)
	child.SetPoint("TOPRIGHT", parent.GetName(), "%sRIGHT" % place, 0, 0)

def MvDialog_QuestLog_Update():
	pass

def accept_Click():
	MvDialogFrame.Hide()
	MarsQuest.AcceptQuest()

def decline_Click():
	MvDialogFrame.Hide()
	MarsQuest.DeclineQuest()

def MvDialog_QuestDetail_Update():
	MvDialogFrame.Hide()
	MvDialog_Init()

	MvHeader1.SetText(MarsQuest.GetTitleText())
	MvDialog_Attach(MvDialogScrollChildFrame, MvHeader1, "TOP")
	MvHeader1.Show()

#	MvBody1.SetText(GetQuestText())
	MvDialog_SetText(MvBody1, MarsQuest.GetQuestText())
	MvDialog_Attach(MvHeader1, MvBody1)
	MvBody1.Show()

	MvHeader2.SetText("Quest Objective")
	MvDialog_Attach(MvBody1, MvHeader2)
	MvHeader2.Show()

#	MvBody2.SetText(GetObjectiveText())
	MvDialog_SetText(MvBody2, MarsQuest.GetObjectiveText())
	MvDialog_Attach(MvHeader2, MvBody2)
	MvBody2.Show()

	MvHeader3.SetText("Quest Rewards")
	MvDialog_Attach(MvBody2, MvHeader3)
#	MvHeader3.Show()
	MvHeader3.Hide()

#	MvBody3.SetText("You will receive:")
	MvDialog_SetText(MvBody3, "You will receive:")
	MvDialog_Attach(MvHeader3, MvBody3)
#	MvBody3.Show()
	MvBody3.Hide()

	previous = MvBody3
	i = 0
	for i in range(1, MarsQuest.GetNumQuestRewards()+1):
		name, texture, count, quality, usable = MarsQuest.GetQuestItemInfo("reward", i)
		action = getglobal("MvAction%d" % i)
		if usable:
			action.SetText("%s (%d)" % (name, count))
			getglobal("%sBulletTexture" % action.GetName()).SetVertexColor(0,0,1)
		else:
			action.SetText("%s (%d) [not usable]" % (name, count))
			getglobal("%sBulletTexture" % action.GetName()).SetVertexColor(1,0,0)
		MvDialog_Attach(previous, action)
		action.Show()
		MvAction_Func[i-1] = MvInfo_ShowFunc(name, texture, str(i))
		previous = action

	MvHeader4.SetText("Actions")
	MvDialog_Attach(previous, MvHeader4)
	MvHeader4.Show()

	MvBody4.SetText("What will you do?")
	MvDialog_SetText(MvBody4, "What will you do?")
	MvDialog_Attach(MvHeader4, MvBody4)
	MvBody4.Show()

	i = i+1
	accept = getglobal("MvAction%d" % i)
	accept.SetText("I accept this quest.")
	MvDialog_Attach(MvBody4, accept)
	MvAction_Func[i-1] = accept_Click
#	getglobal("%sBulletTexture" % accept.GetName()).SetVertexColor(0,1,0)
	accept.Show()

	i = i+1
	decline = getglobal("MvAction%d" % i)
	decline.SetText("I decline this quest.")
	MvDialog_Attach(accept, decline)
	MvAction_Func[i-1] = decline_Click
#	getglobal("%sBulletTexture" % decline.GetName()).SetVertexColor(0,1,0)
	decline.Show()

	MvDialogFrame.Show()

def MvScrollUpButton_OnClick(frame, args):
	scrollFrame = frame.GetParent().GetParent()
	offset = scrollFrame.GetVerticalScroll()
	if offset > 0:
		offset = offset - 10
	if offset < 0:
		offset = 0
	scrollFrame.SetVerticalScroll(offset)

def MvScrollDownButton_OnClick(frame, args):
	scrollFrame = frame.GetParent().GetParent()
	offset = scrollFrame.GetVerticalScroll()
	range = scrollFrame.GetVerticalScrollRange()
	if range > offset:
		offset = offset + 10
	if offset > range:
		offset = range
	scrollFrame.SetVerticalScroll(offset)
	
def MvScrollFrame_OnScrollRangeChanged(frame, args):
	scrollrange = 0
	if args:
		scrollrange = args.data[1]
	else:
		scrollrange = this.GetVerticalScrollRange()
	scrollbar = getglobal(frame.GetName() + "ScrollBar")
	val = scrollbar.GetValue()
	if val > scrollrange:
		val = scrollrange
	scrollbar.SetMinMaxValues(0, scrollrange)
	scrollbar.SetValue(val)

def MvScrollFrame_OnMouseWheel(frame, args):
	scrollbar = getglobal(frame.GetName() + "ScrollBar")
	if args.data > 0.0:
		scrollbar.SetValue(scrollbar.GetValue() - (scrollbar.GetHeight() / 2))
	else:
		scrollbar.SetValue(scrollbar.GetValue() + (scrollbar.GetHeight() / 2))
