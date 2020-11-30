from Axiom.Input import MouseButtons

def AbilitiesFrame_OnLoad(frame):
    frame.RegisterEvent("ABILITY_UPDATE")

def AbilitiesFrame_OnShow(frame):
    parentName = None
    if frame.GetParent():
        parentName = frame.GetParent().GetName()
    frame.SetPoint("RIGHT", parentName, "RIGHT", -20, 60)
    MyAbilitiesFrameTexture.SetVertexColor(0.1, 0.1, 0.1)
    MyAbilitiesFrameTexture.SetAlpha(0.3)

    name = frame.GetName()
    slots = 12

    for j in range(1, slots +1 ):
        button = getglobal("%sItem%d" % (name, j))
        button.SetID(j)
        nameFrame = getglobal("%sItem%dNameFrame" %(name, j))
        nameFrame.SetVertexColor(0.1, 0.1, 0.1)
        nameFrame.SetAlpha(0.3)

    AbilitiesFrame_Update(frame)

def AbilitiesFrame_Update(frame):
    name = frame.GetName()
    slots = 12
    numAbilities = MarsAbility.GetNumAbilities()
    for j in range(1, slots+1 ):
        abilityName = ""
        iconName = ""
        if (j <= numAbilities):
            abilityName = MarsAbility.GetAbilityName(j)
            iconName = MarsAbility.GetAbilityTexture(j)
        icon = getglobal("%sItem%dIconTexture" % (name, j))
        icon.SetTexture(iconName)
        label = getglobal("%sItem%dName" % (name, j))
        label.SetText(abilityName)

def AbilitiesFrame_OnEvent(frame, args):
    AbilitiesFrame_Update(frame)

def ToggleAbilitiesFrame():
    if MyAbilitiesFrame.IsVisible():
        MyAbilitiesFrame.Hide()
    else:
        MyAbilitiesFrame.Show()

def AbilitiesFrameButton_OnClick(frame, args):
    slot = frame.GetID()
    if (slot > MarsAbility.GetNumAbilities()):
        return
    if (args.Button == MouseButtons.Right):
        MarsAbility.PickupAbility(slot)
        return
    MarsAbility.UseAbilityByName(MarsAbility.GetAbilityName(slot), False)

def AbilitiesFrameButton_OnEnter(frame):
    pass

def AbilitiesFrameButton_OnLeave(frame):
    pass

