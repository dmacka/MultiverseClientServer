import MarsCursor
import MarsTrade

from Axiom.Input import MouseButtons

def SecureTradeFrame_OnLoad(frame):
    frame.RegisterEvent("TRADE_START")
    frame.RegisterEvent("TRADE_OFFER_UPDATE")
    frame.RegisterEvent("TRADE_COMPLETE")
        
def SecureTradeFrame_OnShow(frame):
    name = frame.GetName()
    for i in range(0, 6):
        button = getglobal("%sOffer1Item%d" % (name, i))
        button.Properties["readonly"] = 1
        button = getglobal("%sOffer2Item%d" % (name, i))
        button.Properties["readonly"] = 0
    parentName = None
    if frame.GetParent():
        parentName = frame.GetParent().GetName()
    frame.SetPoint("LEFT", parentName, "LEFT", 80, 40)
    MySecureTradeFrameTexture.SetVertexColor(0.1, 0.1, 0.1)
    MySecureTradeFrameTexture.SetAlpha(0.3)
    SecureTradeFrame_Update(frame)

def SecureTradeFrame_Update(frame):
    name = frame.GetName()
    slots = 6

    for i in range(1, 3):
        for j in range(0, slots):
            button = getglobal("%sOffer%dItem%d" % (name, i, j))
            item = MarsTrade.GetTradeItemInfo(i, j)
            if item == None or item.itemId == -1:
                SetItemButtonTexture(button, "Interface/Icons/INV_empty")
                SetItemButtonName(button, None)
                SetItemButtonAlpha(button, 0.2)
            else:
                SetItemButtonTexture(button, item.icon)
                SetItemButtonName(button, item.name)
                SetItemButtonAlpha(button, 0.8)
            button.Show()

def SecureTradeFrame_OnEvent(frame, event):
    if event.eventType == "TRADE_START":
        SecureTradeFrame_Start(frame, event)
    if event.eventType == "TRADE_OFFER_UPDATE":
        SecureTradeFrame_OfferUpdate(frame, event)
    if event.eventType == "TRADE_COMPLETE":
        SecureTradeFrame_Complete(frame, event)
    SecureTradeFrame_Update(frame)

def SecureTradeFrame_Start(frame, event):
    playerId = long(event.eventArgs[0])
    if playerId != ClientAPI.GetPlayerObject().OID:
        ClientAPI.LogError("Invalid player id in SecureTradeFrame_Start")
        return
    partnerId = long(event.eventArgs[1])
    frame.Properties["partner"] = partnerId
    playerName = ClientAPI.World.GetObjectByOID(playerId).Name
    partnerName = ClientAPI.World.GetObjectByOID(partnerId).Name
    MySecureTradeFrameOffer1Name.SetText(partnerName)
    MySecureTradeFrameOffer2Name.SetText(playerName)
    MySecureTradeFrame.Show()

def SecureTradeFrame_Complete(frame, event):
    MySecureTradeFrame.Hide()

def SecureTradeFrame_OfferUpdate(frame, event):
    name = frame.GetName()
    slots = 6
    for i in range(1, 3):
        for j in range(0, slots):
            button = getglobal("%sOffer%dItem%d" % (name, 3-i, j))
            item = MarsTrade.GetTradeItemInfo(i, j)
            if item == None or item.itemId == -1:
                SetItemButtonTexture(button, "Interface/Icons/INV_empty")
                SetItemButtonName(button, None)
                SetItemButtonAlpha(button, 0.2)
            else:
                SetItemButtonTexture(button, item.icon)
                SetItemButtonName(button, item.name)
                SetItemButtonAlpha(button, 0.8)
            button.Show()
    accepted2 = event.eventArgs[2]
    accepted1 = event.eventArgs[3]
    if accepted2 == "True":
        MySecureTradeFrameOffer2Check.SetChecked(True)
    else:
        MySecureTradeFrameOffer2Check.SetChecked(False)
    if accepted1 == "True":
        MySecureTradeFrameOffer1Check.SetChecked(True)
    else:
        MySecureTradeFrameOffer1Check.SetChecked(False)

def SecureTradeFrame_OnAccept(frame):
    if MySecureTradeFrameOffer2Check.GetChecked():
        MySecureTradeFrameOffer2Check.SetChecked(False)
    else:
        MySecureTradeFrameOffer2Check.SetChecked(True)
    SecureTradeFrame_SendUpdate(MySecureTradeFrame)

def SecureTradeFrame_OnCancel(frame):
    partnerId = MySecureTradeFrame.Properties["partner"]
    MarsTrade.SendTradeOffer(partnerId, False, True)

def SecureTradeFrame_SendUpdate(frame):
    name = frame.GetName()
    partnerId = frame.Properties["partner"]
    accepted = MySecureTradeFrameOffer2Check.GetChecked()
    MarsTrade.SendTradeOffer(partnerId, accepted, False)

def SecureTradeItem_OnClick(frame, args):
    if frame.Properties["readonly"] == 1:
        return
    
    if args.Button == MouseButtons.Left:
        MarsTrade.ClickTradeButton(frame.GetID())
        # If we have added an item, clear the accepted flag
        MySecureTradeFrameOffer2Check.SetChecked(False)
        SecureTradeFrame_SendUpdate(MySecureTradeFrame)
        SecureTradeFrame_Update(MySecureTradeFrame)
    
def SecureTradeItem_OnEnter(frame):
    pass

def SecureTradeItem_OnLeave(frame):
    pass

def SetItemButtonName(button, name):
    nameWidget = getglobal(button.GetName() + "Name")
    if name:
        nameWidget.Show()
    else:
        nameWidget.Hide()
    nameWidget.SetText(name)

def SetItemButtonTexture(button, texture):
    iconTexture = getglobal(button.GetName() + "IconTexture")
    if texture:
        iconTexture.Show()
    else:
        iconTexture.Hide()
    iconTexture.SetTexture(texture)

def SetItemButtonAlpha(button, alpha):
    iconTexture = getglobal(button.GetName() + "IconTexture")
    iconTexture.SetAlpha(alpha)

