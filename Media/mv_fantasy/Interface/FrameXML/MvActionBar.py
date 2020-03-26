import MarsAction
import MarsCursor

from Axiom.Input import MouseButtons

def SetActionButtonTexture(button, texture):
    ClientAPI.Log("Setting button %s to texture %s" % (button.GetName(), texture))
    iconTexture = getglobal(button.GetName() + "IconTexture")
    if texture:
        iconTexture.Show()
    else:
        iconTexture.Hide()
    iconTexture.SetTexture(texture)
    iconTexture.SetWidth(37)
    iconTexture.SetHeight(37)

def SetActionButtonAlpha(button, alpha):
    ClientAPI.Log("Setting button %s to alpha %d" % (button.GetName(), alpha))
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
    pass

def ActionBar_OnShow(frame):
    parentName = None
    if frame.GetParent():
        parentName = frame.GetParent().GetName()
    frame.SetPoint("BOTTOM", parentName, "BOTTOM", 0, 1)
    MvActionBarTexture.SetVertexColor(0.1, 0.1, 0.1)
    MvActionBarTexture.SetAlpha(0.3)

    name = frame.GetName()
    slots = 12

    for j in range(1, slots +1 ):
        button = getglobal("%sItem%d" % (name, j))
        button.SetID(j)

    ActionBar_Update(frame)

def ActionBar_Update(frame):
    name = frame.GetName()
    slots = 12

    for j in range(1, slots + 1):
        button = getglobal("%sItem%d" % (name, j))
        slotId = button.GetID()
        if MarsAction.HasAction(slotId):
            SetActionButtonTexture(button, MarsAction.GetActionTexture(slotId))
            SetActionButtonAlpha(button, 0.8)
            SetActionButtonHotKey(button, "%d" % (j))
        else:
            SetActionButtonTexture(button, "Interface/Icons/INV_empty")
            SetActionButtonAlpha(button, 0.2)
            SetActionButtonHotKey(button, "")
        button.Show()

def ActionBar_OnEvent(frame, args):
    ActionBar_Update(frame)

def ToggleActionBar():
    if MvActionBar.IsVisible():
        MvActionBar.Hide()
    else:
        MvActionBar.Show()

def ActionBarButton_OnClick(frame, args):
    slot = frame.GetID()

    if args.Button == MouseButtons.Right:
        MarsAction.PickupAction(slot)
        ActionBar_Update(frame.GetParent())
        return

    if MarsCursor.CursorHasAbility() or MarsCursor.CursorHasItem():
        MarsAction.PlaceAction(slot)
        ActionBar_Update(frame.GetParent())
        return
    
    MarsAction.UseAction(slot, False, False)

def ActionBarButton_OnEnter(frame):
    slot = frame.GetID()
    actionText = MarsAction.GetActionText(slot)
    if actionText is None:
        return
    tooltipText = actionText
    ItemTooltip.SetPoint("BOTTOMRIGHT", frame.Name, "TOPLEFT")
    ItemTooltipTextLeft1.SetText(tooltipText)
    ItemTooltip.Show()

def ActionBarButton_OnLeave(frame):
    ItemTooltip.Hide()


