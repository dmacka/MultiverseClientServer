def nyts_Custom():
    pass

###########

def ActionBar_OnLoad(frame):
    MvActionBar.Show()

Old_ActionBar_OnShow = ActionBar_OnShow
def ActionBar_OnShow(frame):
    Old_ActionBar_OnShow(frame)
    parentName = None
    if frame.GetParent():
        parentName = frame.GetParent().GetName()
    frame.ClearAllPoints()
    frame.SetPoint("BOTTOMRIGHT", parentName, "BOTTOMRIGHT", -1, 1)

ActionBar_Textures = [
    "Interface/ActionbarIcons/dance",
    "Interface/ActionbarIcons/wave",
    "Interface/ActionbarIcons/laugh",
    "Interface/ActionbarIcons/clap",
    "Interface/ActionbarIcons/cheer",
    "Interface/ActionbarIcons/cry",
    [],
    [],
    [],
    [],
    "Interface/ActionbarIcons/help",
    "Interface/ActionbarIcons/exit",
    ]

ActionBar_Tips = [
    "dance",
    "wave",
    "laugh",
    "clap hands",
    "cheer",
    "cry",
    [],
    [],
    [],
    [],
    "help",
    "exit",
    ]

ActionBar_Func = [
    lambda:ClientAPI.Network.SendTargetedCommand(ClientAPI.GetPlayerObject().OID, "/dance"),
    lambda:ClientAPI.Network.SendTargetedCommand(ClientAPI.GetPlayerObject().OID, "/playanimation wave"),
    lambda:ClientAPI.Network.SendTargetedCommand(ClientAPI.GetPlayerObject().OID, "/playanimation laugh"),
    lambda:ClientAPI.Network.SendTargetedCommand(ClientAPI.GetPlayerObject().OID, "/playanimation clap"),
    lambda:ClientAPI.Network.SendTargetedCommand(ClientAPI.GetPlayerObject().OID, "/playanimation cheer"),
    lambda:ClientAPI.Network.SendTargetedCommand(ClientAPI.GetPlayerObject().OID, "/playanimation cry"),
    lambda:7,
    lambda:8,
    lambda:9,
    lambda:10,
    nyts_Help_fMain.Show,
    ClientAPI.Exit,
    ]

def ActionBar_Update(frame):
    name = frame.GetName()
    slots = 12
    for j in range(1, slots + 1):
        button = getglobal("%sItem%d" % (name, j))
        if ActionBar_Textures[j-1]:
            SetActionButtonTexture(button, ActionBar_Textures[j-1])
            SetActionButtonAlpha(button, 0.8)
        else:
            SetActionButtonTexture(button, "Interface/ActionbarIcons/blank")
            SetActionButtonAlpha(button, 0.2)
        button.Show()

def ActionBarButton_OnEnter(frame):
    slot = frame.GetID()
    if ActionBar_Tips[slot-1]:
        ItemTooltip.SetPoint("BOTTOMRIGHT", frame.Name, "TOPLEFT")
        ItemTooltipTextLeft1.SetText(ActionBar_Tips[slot-1])
        ItemTooltip.Show()

def ActionBarButton_OnClick(frame, args):
    slot = int(frame.GetID())
    ActionBar_Func[slot-1]()
