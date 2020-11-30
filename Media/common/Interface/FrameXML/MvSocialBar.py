textures = ["Interface/ActionbarIcons/compass",
            "Interface/ActionbarIcons/dance",
            "Interface/ActionbarIcons/wave",
            "Interface/ActionbarIcons/laugh",
            "Interface/ActionbarIcons/clap",
            "Interface/ActionbarIcons/cheer",
            "Interface/ActionbarIcons/cry",
            "Interface/ActionbarIcons/fight",
            [],
            [],
            "Interface/ActionbarIcons/help",
            "Interface/ActionbarIcons/exit"]

tips = ["minimap",
        "dance",
        "wave",
        "laugh",
        "clap hands",
        "cheer",
        "cry",
        "fight",
        [],
        [],
        "help",
        "exit"]

def SetActionButtonTexture(button, texture):
    iconTexture = getglobal(button.GetName() + "IconTexture")
    if texture:
        iconTexture.Show()
    else:
        iconTexture.Hide()
    iconTexture.SetTexture(texture)
    iconTexture.SetWidth(37)
    iconTexture.SetHeight(37)

def SetActionButtonAlpha(button, alpha):
    iconTexture = getglobal(button.GetName() + "IconTexture")
    iconTexture.SetAlpha(alpha)

def SetActionButtonHotKey(button, key):
    itemKey = getglobal(button.GetName() + "HotKey")
    if key:
        itemKey.SetText(key)
        itemKey.Show()
    else:
        itemKey.Hide()

def SetActionButtonCount(button, count):
    itemCount = getglobal(button.GetName() + "Count")
    if count > 0:
        itemCount.SetText(count.ToString())
        itemCount.Show()
    else:
        itemCount.Hide()

def ActionBar_OnLoad(frame):
    MyActionBar.Show()

def ActionBar_OnShow(frame):
    parentName = None
    if frame.GetParent():
        parentName = frame.GetParent().GetName()
    frame.SetPoint("BOTTOMRIGHT", parentName, "BOTTOMRIGHT", -1, 1)
    MyActionBarTexture.SetVertexColor(0.1, 0.1, 0.1)
    MyActionBarTexture.SetAlpha(0.3)

    name = frame.GetName()
    slots = 12

    for j in range(1, slots + 1 ):
        button = getglobal("%sItem%d" % (name, j))
        button.SetID(j)
        
    ActionBar_Update(frame)

def ActionBar_Update(frame):
    name = frame.GetName()
    slots = 12

    for j in range(1, slots + 1):
        button = getglobal("%sItem%d" % (name, j))
        if textures[j-1]:
            SetActionButtonTexture(button, textures[j-1])
            SetActionButtonAlpha(button, 0.8)
        else:
            SetActionButtonTexture(button, "Interface/Icons/INV_empty")
            SetActionButtonAlpha(button, 0.2)
        button.Show()

def ActionBar_OnEvent(frame, args):
    ActionBar_Update(frame)

def ToggleActionBar():
    if MyActionBar.IsVisible():
        MyActionBar.Hide()
    else:
        MyActionBar.Show()

def ActionBarButton_OnClick(frame, args):
    ClientAPI.LogInfo("In ActionBar_OnClick")

def ActionBarButton_OnEnter(frame):
    slot = frame.GetID()
    if tips[slot-1]:
        ItemTooltip.SetPoint("BOTTOMRIGHT", frame.Name, "TOPLEFT")
        ItemTooltipTextLeft1.SetText(tips[slot-1])
        ItemTooltip.Show()

def ActionBarButton_OnLeave(frame):
    ItemTooltip.Hide()
