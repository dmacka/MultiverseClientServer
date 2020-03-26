# maps group name to list of buttons in that group
_RadioButton_Groups = {}
# maps group name to selection callback
_RadioButton_Callbacks = {}
# maps group name to currently selected ID
_RadioButton_Values = {}

def RadioButton_RegisterButton(button, groupName):
    global _RadioButton_Groups
    if _RadioButton_Groups.has_key(groupName):
        group = _RadioButton_Groups[groupName]
    else:
        group = {}
        _RadioButton_Groups[groupName] = group

    id = button.GetID()
    if id == 0:
        button.SetChecked(True)
    group[id] = button

def RadioButton_OnClickHandler(button, groupName):
    global _RadioButton_Groups
    global _RadioButton_Callbacks
    id = button.GetID()
    
    if _RadioButton_Groups.has_key(groupName):
        group = _RadioButton_Groups[groupName]
    else:
        return

    for f in group.values():
        if f == button:
            f.SetChecked(True)
        else:
            f.SetChecked(False)

    _RadioButton_Values[groupName] = id

    if _RadioButton_Callbacks.has_key(groupName):
        _RadioButton_Callbacks[groupName](groupName, id)

def RadioButton_RegisterGroup(groupName, callback):
    global _RadioButton_Callbacks

    _RadioButton_Callbacks[groupName] = callback
    _RadioButton_Values[groupName] = 0

def RadioButton_GetSelected(groupName):
    return _RadioButton_Values[groupName]

def RadioButton_SetSelected(groupName, id):
    if not _RadioButton_Values.has_key(groupName):
        return
    old_id = _RadioButton_Values[groupName]
    _RadioButton_Values[groupName] = id
    if (id != old_id) and _RadioButton_Callbacks.has_key(groupName):
        _RadioButton_Callbacks[groupName](groupName, id)
