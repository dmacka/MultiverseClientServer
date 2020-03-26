def QuestLog_OnLoad(frame):
    frame.RegisterEvent("QUEST_LOG_UPDATE")

def QuestLog_OnEvent(frame, args):
    QuestLog_Update()
    
def QuestLog_Update():
    QuestLogMoneyFrame.Hide()
    maxNumDisplayQuests = 6
    startIndex = 1
    numQuests, numEntries = GetNumQuestLogEntries()
    # Build the list at the top
    QuestLogHighlightFrame.Hide()
    for questId in range(startIndex, maxNumDisplayQuests + 1):
        questLogTitle = getglobal("QuestLogTitle%d" % questId)
        questTitleTag = getglobal("QuestLogTitle%dTag" % questId)
        if questLogTitle != None:
            questLogTitle.SetText(GetQuestLogTitle(questId))
            questLogTitle.Show()
        if questId <= numEntries:
            if questId == GetQuestLogSelection():
                questTitleTag.SetTextColor(1.0, 1.0, 1.0)
                questLogTitle.SetTextColor(1.0, 1.0, 1.0)
                questLogTitle.LockHighlight()
                QuestLogHighlightFrame.SetPoint("TOPLEFT", "QuestLogTitle%d" % questId, "TOPLEFT", 5, 0)
                QuestLogHighlightFrame.Show()
            else:
                questTitleTag.SetTextColor(1.0, 0.82, 0.0)
                questLogTitle.SetTextColor(1.0, 0.82, 0.0)
                questLogTitle.UnlockHighlight()
        else:
            questLogTitle.Hide()
    # Build the description area
    if GetQuestLogSelection() <= 0:
        QuestLogFrameAbandonButton.Disable()
        QuestFramePushQuestButton.Disable()
        QuestLogDetailScrollChildFrame.Hide()
        return
    QuestLogDetailScrollChildFrame.Show()
    questIndex = GetQuestLogSelection()
    questTitle = GetQuestLogTitle(questIndex)
    QuestLogQuestTitle.SetText(questTitle)
    questDescription, questObjective = GetQuestLogQuestText()
    QuestLogQuestDescription.SetText(questDescription)
    QuestLogObjectivesText.SetText(questObjective)
    QuestLogQuestDescription.Show()
    QuestLogObjectivesText.Show()
    if GetQuestLogPushable():
        QuestFramePushQuestButton.Enable()
    else:
        QuestFramePushQuestButton.Disable()
    if GetQuestMoneyToGet() > 0:
        QuestLogRequiredMoneyText.Show()
        QuestLogRequiredMoneyFrame.Show()
    else:
        QuestLogRequiredMoneyText.Hide()
        QuestLogRequiredMoneyFrame.Hide()
    # Build the objectives area
    maxObjectives = 10
    for j in range(1, maxObjectives + 1):
        objective = getglobal("QuestLogObjective%d" % j)
        if j <= GetNumQuestLeaderBoards(questIndex):
            title, type, done = GetQuestLogLeaderBoard(j, questIndex)
            objective.SetText(title)
            objective.Show()
        else:
            objective.SetText("")
            objective.Hide()
    maxNumItems = 10
    for j in range(1, maxNumItems + 1):
        rewardItem = getglobal("QuestLogItem%d" % j)
        if j <= GetNumQuestLogRewards():
            rewardItem.Show()
        else:
            rewardItem.Hide()
    QuestFrameItems_Update("QuestLog")

def QuestLogTitleButton_OnClick(frame):
    questIndex = frame.GetID()
    QuestLog_SetSelection(questIndex)
    QuestLog_Update()

def QuestLog_SetSelection(questId):
    SelectQuestLogEntry(questId)
    # Make sure the selection was valid
    if GetQuestLogSelection() <= 0:
        return
    
    titleButton = getglobal("QuestLogTitle%d" % questId)
    titleButtonTag = getglobal("QuestLogTitle%dTag" % questId)

    # titleButtonTag.SetTextColor(HIGHLIGHT_FONT_COLOR.r, HIGHLIGHT_FONT_COLOR.g, HIGHLIGHT_FONT_COLOR.b)
    # QuestLogSkillHighlight.SetVertexColor(titleButton.r, titleButton.g, titleButton.b)

def ToggleQuestLog():
    if QuestLogFrame.IsVisible():
        HideUIPanel(QuestLogFrame)
    else:
        ShowUIPanel(QuestLogFrame)
