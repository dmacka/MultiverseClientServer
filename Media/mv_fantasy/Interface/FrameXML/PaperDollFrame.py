def SetItemButtonTexture(button, texture):
    iconTexture = getglobal(button.GetName() + "IconTexture")
    if texture:
        iconTexture.Show()
    else:
        iconTexture.Hide()
    iconTexture.SetTexture(texture)
    iconTexture.SetWidth(36)
    iconTexture.SetHeight(36)
    # ClientAPI.LogInfo("Set icon texture for " + iconTexture.GetName() + " to " + texture)

def SetItemButtonCount(button, count):
    itemCount = getglobal(button.GetName() + "Count")
    if count > 0:
        itemCount.SetText(count.ToString())
        itemCount.Show()
    else:
        itemCount.Hide()

def SetActionButtonTexture(button, texture):
    iconTexture = getglobal(button.GetName() + "NormalTexture")
    if texture:
        iconTexture.Show()
    else:
        iconTexture.Hide()
    iconTexture.SetTexture(texture)
    iconTexture.SetWidth(36)
    iconTexture.SetHeight(36)
    Console.WriteLine("Set icon texture for " + iconTexture.GetName() + " to " + texture)

def PaperDollFrame_OnLoad(frame):
    print "In onload"
    # None of these stats are available from the server yet
    # CharacterAttackFrameLabel.SetText("Melee Attack")
    # CharacterDamageFrameLabel.SetText("Damage:")
    # CharacterAttackPowerFrameLabel.SetText("Attack:")
    # CharacterRangedAttackFrameLabel.SetText("Ranged Attack")
    # CharacterRangedDamageFrameLabel.SetText("Damage:")
    # CharacterRangedAttackPowerFrameLabel.SetText("Attack:")
    # CharacterArmorFrameLabel.SetText("Armor:")

def PaperDollFrame_OnShow(frame):
    print "Should show stats"
    #PaperDollFrame_SetGuild();
    #PaperDollFrame_SetLevel();
    PaperDollFrame_SetStats()
    #PaperDollFrame_SetResistances();
    # PaperDollFrame_SetArmor();
    # PaperDollFrame_SetDamage();
    #PaperDollFrame_SetAttackPower();
    #PaperDollFrame_SetAttackBothHands();
    #PaperDollFrame_SetRangedAttack();
    #PaperDollFrame_SetRangedDamage();
    #PaperDollFrame_SetRangedAttackPower();

def PaperDollFrame_SetStats():
    STATS = "Strength", "Dexterity", "Intelligence"
    for i in range(1, 4):
        label = getglobal("CharacterStatFrame%dLabel" % i)
        text = getglobal("CharacterStatFrame%dStatText" % i)
        frame = getglobal("CharacterStatFrame%d" % i)
        label.SetText(STATS[i - 1])
        base, stat, posBuff, negBuff = UnitStat("unit", i)
        text.SetText(stat)

def PaperDollFrame_OnHide(frame):
    print "Hide"

def PaperDollItemSlotButton_OnLoad(frame):
    slotName = frame.GetName()
    id, textureName = GetInventorySlotInfo(slotName.Substring(10))
    frame.SetID(id)
    texture = getglobal(slotName + "IconTexture")
    texture.SetTexture(textureName)
    # frame.backgroundTextureName = textureName
    PaperDollItemSlotButton_Update(frame)

def PaperDollItemSlotButton_OnClick(frame):
    print "Got click in inventory button: %d" % frame.GetID()

def PaperDollItemSlotButton_Update(frame):
    textureName = GetInventoryItemTexture("player", frame.GetID())
    if textureName:
        SetItemButtonTexture(frame, textureName)
        SetItemButtonCount(frame, GetInventoryItemCount("player", frame.GetID()))
    else:
        SetItemButtonTexture(frame, "default")
        SetItemButtonCount(frame, 0)
        # SetItemButtonTextureVertexColor(frame, 1.0, 1.0, 1.0)
        # SetItemButtonNormalTextureVertexColor(frame, 1.0, 1.0, 1.0)
        # cooldown:Hide();



