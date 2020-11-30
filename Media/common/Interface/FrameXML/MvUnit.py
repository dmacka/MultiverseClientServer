def UnitFrame_OnEvent(frame, event):
    if event.eventType == "UNIT_NAME_UPDATE":
        unit = event.eventArgs[0]
        if unit == frame.Properties["unit"]:
            frame.Properties["name"].SetText(MarsUnit.UnitName(unit))
    
def UnitFrame_Update(frame):
    unit = frame.Properties["unit"]
    if not UnitExists(unit):
        frame.Hide()
    else:
        frame.Show()
        frame.Properties["name"].SetText(MarsUnit.UnitName(unit))
        UnitFrameHealthBar_Update(frame.Properties["healthbar"], unit)
        UnitFrameManaBar_Update(frame.Properties["manabar"], unit)

def UnitFrame_Initialize(frame, unit, name, portrait, healthbar, healthtext, manabar, manatext):
    frame.Properties["unit"] = unit
    frame.Properties["name"] = name
    frame.Properties["portrait"] = portrait
    frame.Properties["healthbar"] = healthbar
    frame.Properties["manabar"] = manabar
    UnitFrameHealthBar_Initialize(unit, healthbar, healthtext)
    UnitFrameManaBar_Initialize(unit, manabar, manatext)
    UnitFrame_Update(frame)
    frame.RegisterEvent("UNIT_NAME_UPDATE")
    
def UnitFrameHealthBar_Initialize(unit, statusbar, statustext):
    if not statusbar:
        return
    statusbar.Properties["unit"] = unit
    # SetTextStatusBarText(statusbar, statustext)
    statusbar.RegisterEvent("UNIT_HEALTH")
    statusbar.RegisterEvent("UNIT_MAXHEALTH")

def UnitFrameManaBar_Initialize(unit, statusbar, statustext):
    if not statusbar:
        return
    statusbar.Properties["unit"] = unit
    # SetTextStatusBarText(statusbar, statustext)
    statusbar.RegisterEvent("UNIT_MANA")
    statusbar.RegisterEvent("UNIT_MAXMANA")

def UnitFrameHealthBar_Update(statusbar, unit):
    if not statusbar:
        return
    if unit == statusbar.Properties["unit"]:
        statusbar.SetMinMaxValues(0, MarsUnit.UnitHealthMax(unit))
        statusbar.SetValue(MarsUnit.UnitHealth(unit))

def UnitFrameManaBar_Update(statusbar, unit):
    if not statusbar:
        return
    if unit == statusbar.Properties["unit"]:
        statusbar.SetMinMaxValues(0, MarsUnit.UnitManaMax(unit))
        statusbar.SetValue(MarsUnit.UnitMana(unit))
    
