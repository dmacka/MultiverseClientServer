def PanelTemplates_TabResize(padding, tab, absoluteSize):
    tabName = tab.GetName()
    buttonMiddle = getglobal(tabName + "Middle")
    buttonMiddleDisabled = getglobal(tabName + "MiddleDisabled")
    sideWidths = 2 * getglobal(tabName + "Left").GetWidth()
    tabText = getglobal(tab.GetName() + "Text")
    width = 0
    tabWidth = 0
    
    # If there's an absolute size specified then use it
    if absoluteSize > 0:
        if absoluteSize < sideWidths:
            width = 1
            tabWidth = sideWidths
        else:
            width = absoluteSize - sideWidths
            tabWidth = absoluteSize
        tabText.SetWidth(width)
    else:
        # Otherwise try to use padding
        if padding:
            width = tabText.GetStringWidth() + padding
        else:
            width = tabText.GetStringWidth() + 24
        tabWidth = width + sideWidths
        # tabText.SetWidth(0)
        tabText.SetWidth(width)
    
    if buttonMiddle:
        buttonMiddle.SetWidth(width)
    if buttonMiddleDisabled:
        buttonMiddleDisabled.SetWidth(width)
    
    tab.SetWidth(tabWidth)
    highlightTexture = getglobal(tabName + "HighlightTexture")
    if highlightTexture:
        highlightTexture.SetWidth(tabWidth)
