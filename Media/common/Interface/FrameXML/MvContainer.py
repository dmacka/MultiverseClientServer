import MarsCursor
import MarsContainer

from Axiom.Input import MouseButtons

def SetItemButtonTexture(button, texture):
    iconTexture = getglobal(button.GetName() + "IconTexture")
    if texture:
        iconTexture.Show()
    else:
        iconTexture.Hide()
    iconTexture.SetTexture(texture)
    iconTexture.SetWidth(36)
    iconTexture.SetHeight(36)

def SetItemButtonCount(button, count):
    itemCount = getglobal(button.GetName() + "Count")
    if count > 0:
        itemCount.SetText(count.ToString())
        itemCount.Show()
    else:
        itemCount.Hide()

def Container_OnLoad(frame):
    frame.RegisterEvent("UNIT_INVENTORY_UPDATE")

def Container_OnShow(frame):
    columns = 4
    containerId = 0
    parentName = None
    if frame.GetParent():
        parentName = frame.GetParent().GetName()
    bgTexture = getglobal(frame.GetName() + "BackgroundTexture")
    bgTexture.SetTexture("Interface\\ContainerFrame\\UI-BackpackBackground")
    bgTexture.SetWidth(256)
    bgTexture.SetHeight(256)
    frame.SetWidth(192)
    frame.SetHeight(239)
    frame.SetPoint("BOTTOMRIGHT", parentName, "BOTTOMRIGHT", 0, 50)

    name = frame.GetName()
    slots = MarsContainer.GetContainerNumSlots(containerId)

    for j in range(1, slots + 1):
        button = getglobal("%sItem%d" % (name, j))
        button.SetID(slots - j + 1)

        if j == 1:
            # Anchor the first item differently if its the backpack frame
            button.SetPoint("BOTTOMRIGHT", parentName, "BOTTOMRIGHT", -11, 30)
            # button.SetPoint("BOTTOMRIGHT", parentName, "BOTTOMRIGHT", -11, 9)
        else:
            if (j - 1) % columns == 0:
                button.SetPoint("BOTTOMRIGHT", "%sItem%d" % (name, j - columns), "TOPRIGHT", 0, 4)
            else:
                button.SetPoint("BOTTOMRIGHT", "%sItem%d" % (name, j - 1), "BOTTOMLEFT", -5, 0)

    Container_Update(frame)

def Container_Update(frame):
    containerId = frame.GetID()
    name = frame.GetName()
    slots = MarsContainer.GetContainerNumSlots(containerId)

    for j in range(1, slots + 1):
        button = getglobal("%sItem%d" % (name, j))
        ClientAPI.Log("got button")
        slotId = button.GetID()
        ClientAPI.Log("SlotId = %d " % (slotId))
        ClientAPI.Log("In Container_Update with button %s and slotId %d" % (button, slotId))   
        if MarsContainer.GetContainerItemInfo(containerId, slotId):
            texture, itemCount, locked, quality, readable = MarsContainer.GetContainerItemInfo(containerId, slotId)
            SetItemButtonTexture(button, texture)
            button.Show()
        else:
            texture = None
            SetItemButtonTexture(button, texture)
            button.Show()

def Container_OnEvent(frame, args):
    Container_Update(frame)

def ToggleBackpack():
    Backpack.SetID(0)
    if Backpack.IsVisible():
        Backpack.Hide()
    else:
        Backpack.Show()

def ContainerItemButton_OnClick(frame, args):
    container = frame.GetParent()
    ClientAPI.Log("in container on click")
    if args.Button == MouseButtons.Left:
        MarsContainer.PickupContainerItem(container.GetID(), frame.GetID())
    elif args.Button == MouseButtons.Right:
        MarsContainer.UseContainerItem(container.GetID(), frame.GetID(), False)

def ContainerItemButton_OnEnter(frame):
    container = frame.GetParent()
    ItemTooltip.SetPoint("BOTTOMRIGHT", frame.Name, "TOPLEFT")
    _SetBagItem("ItemTooltip", container.GetID(), frame.GetID())
    # ItemTooltipTextLeft1.SetText('%d/%d' % (container.GetID(), frame.GetID()))
    if MarsContainer._GetContainerItem(container.GetID(), frame.GetID()) is not None:
        ItemTooltip.Show()
    else:
        ItemTooltip.Hide() 

def ContainerItemButton_OnLeave(frame):
    ItemTooltip.Hide()

def _SetBagItem(tooltipName, containerId, slotId):
    itemName = MarsContainer.GetContainerItemLink(containerId, slotId)
    if itemName is None:
        return
    frame = getglobal(tooltipName + "TextLeft1")
    frame.SetText(itemName)

