def InfoBar_OnLoad(frame):
    frame.SetBackdropColor(0, 0, 0)

def InfoBarButton_OnEnter(frame):
    buttonId = frame.GetID()
    if buttonId == 0:
        toolTipText = "Displays character statistical information."
    elif buttonId == 1:
        toolTipText = "Inventory"
    elif buttonId == 2:
        toolTipText = "Group Information"
    else:
        toolTipText = "N/A"
			
    ItemTooltipTextLeft1.SetText(toolTipText)
    ItemTooltip.SetWidth(ItemTooltipTextLeft1.GetStringWidth() + 20)
    ItemTooltip.SetPoint("BOTTOMRIGHT", frame.Name, "TOPLEFT", ItemTooltipTextLeft1.GetStringWidth(), -90)
    ItemTooltip.Show()

def InfoBarButton_OnLeave(frame):
    ItemTooltip.Hide()
    
def MvStatsButton_OnClick(frame):
    if MvPlayerInfoFrame.IsVisible():
        MvPlayerInfoFrame.Hide()
    else:
        MvPlayerInfoFrame.SetPoint("TOP", frame.GetParent().Name, "BOTTOM")
        MvPlayerInfoFrame.Show()

def MvInvButton_OnClick(frame):
    Backpack.SetID(0)
    if Backpack.IsVisible():
        Backpack.Hide()
    else:
        Backpack.SetPoint("TOP", frame.GetParent().Name, "BOTTOM")
        Backpack.Show()

def MvGroupInfoButton_OnClick(frame):
    if MvGroupInfoFrame.IsVisible():
        MvGroupInfoFrame.Hide()
    else:
        MvGroupInfoFrame.Show()
