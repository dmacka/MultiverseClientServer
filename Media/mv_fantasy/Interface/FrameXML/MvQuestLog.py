import MarsQuest

def QuestLog_OnLoad(frame):
    frame.RegisterEvent("QUEST_LOG_UPDATE")

def QuestLog_OnEvent(frame, args):
    QuestLog_Update()

def QuestLog_SetText(frame, text):
    frame.SetText(text)
    textHeight = frame.window.GetTextHeight(False)
    frame.SetHeight(int(textHeight))

def QuestLog_Update():
    QuestLogMoneyFrame.Hide()
    maxNumDisplayQuests = 6
    startIndex = 1
    numQuests, numEntries = MarsQuest.GetNumQuestLogEntries()
    # Build the list at the top
    QuestLogHighlightFrame.Hide()
    for questId in range(startIndex, maxNumDisplayQuests + 1):
        questLogTitle = getglobal("QuestLogTitle%d" % questId)
        if questLogTitle != None:
            questLogTitle.SetText(MarsQuest.GetQuestLogTitle(questId))
            questLogTitle.Show()
        if questId <= numEntries:
            if questId == MarsQuest.GetQuestLogSelection():
                questLogTitle.SetTextColor(1.0, 1.0, 1.0)
                questLogTitle.LockHighlight()
                QuestLogHighlightFrame.SetPoint("TOPLEFT", "QuestLogTitle%d" % questId, "TOPLEFT", 5, 0)
                QuestLogHighlightFrame.Show()
            else:
                questLogTitle.SetTextColor(1.0, 0.82, 0.0)
                questLogTitle.UnlockHighlight()
        else:
            questLogTitle.Hide()
    # Build the description area
    if MarsQuest.GetQuestLogSelection() <= 0:
#        QuestLogFrameAbandonButton.Disable()
#        QuestFramePushQuestButton.Disable()
        QuestLogDetailScrollChildFrame.Hide()
        return
    QuestLogDetailScrollChildFrame.Show()
    questIndex = MarsQuest.GetQuestLogSelection()
    questTitle = MarsQuest.GetQuestLogTitle(questIndex)
    QuestLog_SetText(QuestLogQuestTitle, questTitle)
    questDescription, questObjective = MarsQuest.GetQuestLogQuestText()
    QuestLog_SetText(QuestLogQuestDescription, questDescription)
    QuestLog_SetText(QuestLogObjectivesText, questObjective)
    QuestLogQuestDescription.Show()
    QuestLogObjectivesText.Show()
#    if GetQuestLogPushable():
#        QuestFramePushQuestButton.Enable()
#    else:
#        QuestFramePushQuestButton.Disable()
    if MarsQuest.GetQuestMoneyToGet() > 0:
        QuestLogRequiredMoneyText.Show()
        QuestLogRequiredMoneyFrame.Show()
    else:
        QuestLogRequiredMoneyText.Hide()
        QuestLogRequiredMoneyFrame.Hide()
    # Build the objectives area
    maxObjectives = 10
    for j in range(1, maxObjectives + 1):
        objective = getglobal("QuestLogObjective%d" % j)
        if j <= MarsQuest.GetNumQuestLeaderBoards(questIndex):
            title, type, done = MarsQuest.GetQuestLogLeaderBoard(j, questIndex)
            QuestLog_SetText(objective, title)
            objective.Show()
        else:
            objective.SetText("")
            objective.SetHeight(1)
            objective.Hide()
    maxNumItems = 10
    for j in range(1, maxNumItems + 1):
        rewardItem = getglobal("QuestLogItem%d" % j)
        if j <= MarsQuest.GetNumQuestLogRewards():
            rewardItem.Show()
            name, icon, count, _, _ = MarsQuest.GetQuestLogRewardInfo(j)
            getglobal("QuestLogItem%dName" % j).SetText(name)
            getglobal("QuestLogItem%dIconTexture" %j).SetTexture(icon)
        else:
            rewardItem.Hide()
    # If you update the contents of the QuestLogDetailScrollFrame,
    # you need to update the scroll child rect.
    QuestLogDetailScrollFrame.UpdateScrollChildRect()
    QuestLogDetailScrollFrame.SetVerticalScroll(0)
#    QuestFrameItems_Update("QuestLog")

def QuestLogTitleButton_OnClick(frame):
    questIndex = frame.GetID()
    QuestLog_SetSelection(questIndex)
    QuestLog_Update()

def QuestLog_SetSelection(questId):
    MarsQuest.SelectQuestLogEntry(questId)
    # Make sure the selection was valid
    if MarsQuest.GetQuestLogSelection() <= 0:
        return
    
    titleButton = getglobal("QuestLogTitle%d" % questId)

    # titleButtonTag.SetTextColor(HIGHLIGHT_FONT_COLOR.r, HIGHLIGHT_FONT_COLOR.g, HIGHLIGHT_FONT_COLOR.b)
    # QuestLogSkillHighlight.SetVertexColor(titleButton.r, titleButton.g, titleButton.b)

def ToggleQuestLog():
    if QuestLogFrame.IsVisible():
        QuestLogFrame.Hide()
    else:
        QuestLogFrame.Show()
