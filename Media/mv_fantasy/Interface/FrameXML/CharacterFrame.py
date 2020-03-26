def ToggleCharacter(tab):
    subFrame = getglobal(tab)
    if subFrame:
        # PanelTemplates_SetTab(CharacterFrame, subFrame.GetID())
        if CharacterFrame.IsVisible():
            if subFrame.IsVisible():
                HideUIPanel(CharacterFrame)    
            else:
                CharacterFrame_ShowSubFrame(tab)
        else:
            ShowUIPanel(CharacterFrame)
            CharacterFrame_ShowSubFrame(tab)

def CharacterFrame_ShowSubFrame(frameName):
    CHARACTERFRAME_SUBFRAMES = "PaperDollFrame", "PetPaperDollFrame", "SkillFrame", "ReputationFrame"
    for value in CHARACTERFRAME_SUBFRAMES:
        if value == frameName:
            getglobal(value).Show()
        else:
            getglobal(value).Hide()

