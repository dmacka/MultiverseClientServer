_MvDisplayList_Buttons = 0
_MvDisplayList_Button_Height = 20
_MvDisplayList_Func_List = []

def MvDisplayList_bEntry_Add():
    global _MvDisplayList_Buttons
    _MvDisplayList_Buttons += 1
    prevFrameName = "MvDisplayList_fMain_sfBody_scList_bEntry%s" % (_MvDisplayList_Buttons - 1)
    newFrameName  = "MvDisplayList_fMain_sfBody_scList_bEntry%s" % (_MvDisplayList_Buttons)
    scrollchild   = MvDisplayList_fMain_sfBody_scList
    newFrame      = ClientAPI.Interface.CreateFrame("Button", newFrameName, scrollchild, "MvDisplayList_bEntry_Template")
    newFrame.SetPoint("TOPLEFT",  prevFrameName, "BOTTOMLEFT",  0, 0)
    newFrame.SetPoint("TOPRIGHT", prevFrameName, "BOTTOMRIGHT", 0, 0)
    newFrame.SetText("label %s" % _MvDisplayList_Buttons)
    newFrame.SetID(_MvDisplayList_Buttons)
    newFrame.Hide()

def MvDisplayList_DisplayEntries(entryList):
    n = len(entryList)
    if _MvDisplayList_Buttons < n:
        numToMake = n - _MvDisplayList_Buttons
        for i in range(numToMake):
            MvDisplayList_bEntry_Add()
    global _MvDisplayList_Func_List
    for i in range(_MvDisplayList_Buttons):
        entry = getglobal("MvDisplayList_fMain_sfBody_scList_bEntry%s" % (i+1))
        if i < n:
            label, callback = entryList[i]
            entry.SetText(label)
#            entry.SetScript("OnClick", callback) # cannot use SetScript on a lambda function
            if i < len(_MvDisplayList_Func_List):
                _MvDisplayList_Func_List[i] = callback
            else:
                _MvDisplayList_Func_List.append(callback)
            entry.Show()
        else:
            entry.Hide()
    scrollframe = MvDisplayList_fMain_sfBody
    scrollbar   = MvDisplayList_fMain_sfBody_slBar
    scrollchild = MvDisplayList_fMain_sfBody_scList
    scrollchild.SetHeight(n * _MvDisplayList_Button_Height)
    scrollrange = scrollchild.GetHeight() - scrollframe.GetHeight()
    if scrollrange < 0:
        scrollrange = 0
    scrollbar.SetMinMaxValues(0, scrollrange)
    offset = scrollbar.GetValue()
    if offset > float(scrollrange):
        offset = scrollrange
        scrollbar.SetValue(offset)

def MvDisplayList_bEntry_OnClick(frame, args):
    id = frame.GetID()
    global _MvDisplayList_Func_List
    _MvDisplayList_Func_List[id-1](frame, args)

def MvDisplayList_Scroll(up):
    scrollbar = MvDisplayList_fMain_sfBody_slBar
    if up:
        scrollbar.SetValue(scrollbar.GetValue() - 20)
    else:
        scrollbar.SetValue(scrollbar.GetValue() + 20)

def MvDisplayList_bDirection_OnClick(frame, args):
    MvDisplayList_Scroll(frame.GetID() == 0)

def MvDisplayList_fMain_sfBody_slBar_OnValueChanged(frame, args):
    MvDisplayList_fMain_sfBody.SetVerticalScroll(args.data)

def MvDisplayList_fMain_sfBody_OnScrollRangeChanged(frame, args):
    return
#     scrollrange = 0
#     if args:
#         scrollrange = args.data[1]
#     else:
#         scrollrange = frame.GetVerticalScrollRange()
#     scrollbar = MvDisplayList_fMain_sfBody_slBar
#     offset = scrollbar.GetValue()
#     if offset > scrollrange:
#         offset = scrollrange
#     scrollbar.SetMinMaxValues(0, scrollrange)
#     scrollbar.SetValue(offset)

def MvDisplayList_fMain_sfBody_OnVerticalScroll(frame, args):
    scrollbar = MvDisplayList_fMain_sfBody_slBar
    scrollbar.SetValue(args.data)

def MvDisplayList_fMain_sfBody_OnMouseWheel(frame, args):
    MvDisplayList_Scroll(args.data > 0.0)

def MvDisplayList_fMain_sfBody_OnShow(frame):
    frame.UpdateScrollChildRect()

def MvDisplayList_fMain_sfBody_OnLoad(frame):
    scrollbar   = MvDisplayList_fMain_sfBody_slBar
    scrollchild = MvDisplayList_fMain_sfBody_scList
    scrollrange = scrollchild.GetHeight() - frame.GetHeight()
    if scrollrange < 0:
        scrollrange = 0
    scrollbar.SetMinMaxValues(0, scrollrange)
    scrollbar.SetValue(0)

def MvDisplayList_Show():
    MvDisplayList_fMain.Show()

def MvDisplayList_Hide():
    MvDisplayList_fMain.Hide()
