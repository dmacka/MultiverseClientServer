MvContextMenu_FuncList = [lambda:0, lambda:1, lambda:2, lambda:3, lambda:4, lambda:5, lambda:6, lambda:7, lambda:8, lambda:9]

# MvContextMenu_WorldObj = None
# MvContextMenu_Sender = None

def MvContextMenu_OnClick(frame, args):
    # MvContextMenu_FuncList[frame.GetID()](frame, args, MvContextMenu_WorldObj, MvContextMenu_Sender)
    MvContextMenu_FuncList[frame.GetID()](frame, args, frame.GetParent().properties['worldObj'], frame.GetParent().properties['sender'])

# context menu functions have the same signature as MvContextMenu_Close()
def MvContextMenu_Close(frame, args, worldObj, sender):
    # global MvContextMenu_WorldObj
    # MvContextMenu_WorldObj = None
    frame.GetParent().properties['worldObj'] = None
    # global MvContextMenu_Sender
    # MvContextMenu_Sender = None
    frame.GetParent().properties['sender'] = None
    MvContextMenu_fMain.SetPoint("TOPLEFT", "UIParent", "TOPLEFT", 0, 0)
    MvContextMenu_fMain.Hide()

# dictionary of array of single key-value map
MvContextMenu_Dictionary = {
    "default" : [
        {"close" : MvContextMenu_Close},
        ],
    }

def MvContextMenu_Dispatcher(worldObj, sender):
    MvContextMenu_fMain.Hide()
    ClickHookName = "default"
    if worldObj.PropertyExists("ClickHookName"):
        ClickHookName = worldObj.GetProperty("ClickHookName")
    # ClientAPI.DebugWrite("ClickHookName: " + ClickHookName)
    ClickHookList = MvContextMenu_Dictionary["default"]
    if ClickHookName in MvContextMenu_Dictionary.keys():
        ClickHookList = MvContextMenu_Dictionary[ClickHookName]
    # ClientAPI.DebugWrite("MvContextMenu_Dictionary.keys(): " + str(MvContextMenu_Dictionary.keys()))

    x, y = ClientAPI.GetMousePosition()
    MvContextMenu_fMain.SetPoint("TOPLEFT", "UIParent", "TOPLEFT", int(x+2), -int(y))
    MvContextMenu_fMain.SetHeight(20 * len(ClickHookList))

    for i in range(10):
        button = getglobal("MvContextMenu_fMain_bButton" + str(i))
        if (i < len(ClickHookList)):
            ClickMap = ClickHookList[i]
            keys = ClickMap.keys() # Should only be 1 key
            button.SetText(" " + keys[0])
            button.Show()
            MvContextMenu_FuncList[i] = ClickMap[keys[0]]
        else:
            button.SetText(" ")
            button.Hide()
            MvContextMenu_FuncList[i] = lambda:i

    # global MvContextMenu_WorldObj
    # MvContextMenu_WorldObj = worldObj
    MvContextMenu_fMain.properties['worldObj'] = worldObj
    # global MvContextMenu_Sender
    # MvContextMenu_Sender = sender
    MvContextMenu_fMain.properties['sender'] = sender
    MvContextMenu_fMain.Show()

def MvContextMenu_PropertyChange_Handler(worldObj, propName):
    if propName == "Targetable":
        prop = worldObj.GetProperty(propName)
        if prop == True:
            worldObj.Targetable = True
            worldObj.SetProperty('click_handler', MvContextMenu_Dispatcher)
        else:
            worldObj.Targetable = False

ClientAPI.World.RegisterEventHandler('ObjectAdded', lambda(worldObj):worldObj.RegisterEventHandler('PropertyChange', MvContextMenu_PropertyChange_Handler))
