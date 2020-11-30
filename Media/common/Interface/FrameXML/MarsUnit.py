def UnitFrame_OnEvent(frame, event):
    if event.eventType == "UNIT_NAME_UPDATE":
        unit = event.eventArgs[0]
        if unit == frame.Properties["unit"]:
            frame.Properties["name"].SetText(MarsUnit.UnitName(unit))
    
def UnitFrame_Update(frame):
    unit = frame.Properties["unit"]
    if not MarsUnit.UnitExists(unit):
        frame.Hide()
    else:
        frame.Show()
        frame.Properties["name"].SetText(MarsUnit.UnitName(unit))
        UnitFrameHealthBar_Update(frame.Properties["healthbar"], unit)
        UnitFrameManaBar_Update(frame.Properties["manabar"], unit)

def UnitFrame_Initialize(frame, unit, name, portrait, healthbar, healthtext, manabar, manatext,
                         staminabar, staminatext):
    frame.Properties["unit"] = unit
    frame.Properties["name"] = name
    frame.Properties["portrait"] = portrait
    frame.Properties["healthbar"] = healthbar
    frame.Properties["manabar"] = manabar
    frame.Properties["staminabar"] = staminabar
    UnitFrameHealthBar_Initialize(unit, healthbar, healthtext)
    UnitFrameManaBar_Initialize(unit, manabar, manatext)
    UnitFrameStaminaBar_Initialize(unit, staminabar, staminatext)
    UnitFrame_Update(frame)
    frame.RegisterEvent("UNIT_NAME_UPDATE")
    
def UnitFrameHealthBar_Initialize(unit, statusbar, statustext):
    if not statusbar:
        return
    statusbar.Properties["unit"] = unit
    # SetTextStatusBarText(statusbar, statustext)
    statusbar.RegisterEvent("PROPERTY_health")
    statusbar.RegisterEvent("PROPERTY_health-max")
    statusbar.RegisterEvent("PROPERTY_level")

def UnitFrameManaBar_Initialize(unit, statusbar, statustext):
    if not statusbar:
        return
    statusbar.Properties["unit"] = unit
    # SetTextStatusBarText(statusbar, statustext)
    statusbar.RegisterEvent("PROPERTY_mana")
    statusbar.RegisterEvent("PROPERTY_mana-max")
    statusbar.RegisterEvent("PROPERTY_level")

def UnitFrameStaminaBar_Initialize(unit, statusbar, statustext):
    if not statusbar:
        return
    statusbar.Properties["unit"] = unit
    # SetTextStatusBarText(statusbar, statustext)
    statusbar.RegisterEvent("PROPERTY_stamina")
    statusbar.RegisterEvent("PROPERTY_stamina-max")
    statusbar.RegisterEvent("PROPERTY_level")

def UnitFrameHealthBar_Update(statusbar, unit):
    if not statusbar:
        return
    if unit == statusbar.Properties["unit"]:
        max_val = MarsUnit.UnitStat(unit, "health-max")
        cur_val = MarsUnit.UnitStat(unit, "health")
        if cur_val == 0 and max_val == 0:
            cur_val = 100 # units without the properties are full
        if max_val == 0:
            max_val = 100
        statusbar.SetMinMaxValues(0, max_val)
        statusbar.SetValue(cur_val)

def UnitFrameManaBar_Update(statusbar, unit):
    if not statusbar:
        return
    if unit == statusbar.Properties["unit"]:
        max_val = MarsUnit.UnitStat(unit, "mana-max")
        cur_val = MarsUnit.UnitStat(unit, "mana")
        if cur_val == 0 and max_val == 0:
            cur_val = 100 # units without the properties are full
        if max_val == 0:
            max_val = 100
        statusbar.SetMinMaxValues(0, max_val)
        statusbar.SetValue(cur_val)

def UnitFrameStaminaBar_Update(statusbar, unit):
    if not statusbar:
        return
    if unit == statusbar.Properties["unit"]:
        max_val = MarsUnit.UnitStat(unit, "stamina-max")
        cur_val = MarsUnit.UnitStat(unit, "stamina")
        if cur_val == 0 and max_val == 0:
            cur_val = 100 # units without the properties are full
        if max_val == 0:
            max_val = 100
        statusbar.SetMinMaxValues(0, max_val)
        statusbar.SetValue(cur_val)

