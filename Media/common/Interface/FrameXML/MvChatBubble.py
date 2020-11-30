from Axiom.MathLib import Vector3
from System.Drawing import Point
from System import DateTime

def MvChatBubble_Update(frame):
    worldObj = frame.Properties["worldObj"]
    if worldObj is None:
        return
    expire = frame.Properties["expire"]
    if expire is None:
        frame.Hide()
        return
    if DateTime.Now > expire:
        # update the expire time, so we don't have to check it again
        frame.Properties["expire"] = None
        frame.Hide()
        return
    attachment = frame.Properties["attachment"]
    widgetOffset = frame.Properties["widgetOffset"]
    pixelOffset = frame.Properties["pixelOffset"]
    pos = None
    try:
        if attachment is None:
            pos = worldObj.Position + widgetOffset
        else:
            pos = worldObj.AttachmentPointPosition(attachment) + widgetOffset
    except:
        ClientAPI.Log("Unable to determine bubble position for object with oid: %s" % str(worldObj.OID))
        return        
    screenPos = ClientAPI.GetScreenPosition(pos)
    if screenPos.z == 0:
        frame.Hide()
    else:
        cam = ClientAPI.GetPlayerCamera()
        dist = cam.Near + screenPos.z * (cam.Far - cam.Near)
        # constants to determine when bubbles fade out
        maxFade = 40000.0
        minFade = 20000.0
        minDistance = ClientAPI.InputHandler.MinPlayerVisibleDistance
        if dist > maxFade:
            frame.Hide()
            return
        if dist < minDistance and worldObj == ClientAPI.GetPlayerObject():
            # This is the player, and the camera is close enough to the player
            # that we are hiding the player.  Hide the player's bubble as well.
            frame.Hide()
            return
        if ClientAPI.HardwareCaps is None:
            return
        screenWidth, screenHeight = ClientAPI.HardwareCaps.WindowSize
        screenX = int(screenWidth* screenPos.x)
        screenY = -1 * int(screenHeight * screenPos.y)
        # Adjust so that the bottom center of the widget matches the node position
        screenX = screenX - int(frame.GetWidth() / 2) + pixelOffset.X
        screenY = screenY + frame.GetHeight() + pixelOffset.Y
        alpha = 1.0
        if dist > minFade:
            alpha = 1.0 - (dist - minFade) / (maxFade - minFade)
        frame.SetAlpha(alpha)
        frame.SetPoint("TOPLEFT", "UIParent", "TOPLEFT", screenX, screenY)
        frame.Show()

def MvFloatyName_Update(frame):
    worldObj = frame.Properties["worldObj"]
    if worldObj is None:
        return
    attachment = frame.Properties["attachment"]
    widgetOffset = frame.Properties["widgetOffset"]
    pixelOffset = frame.Properties["pixelOffset"]
    pos = None
    try:
        if attachment is None:
            pos = worldObj.Position + widgetOffset
        else:
            pos = worldObj.AttachmentPointPosition(attachment) + widgetOffset
    except:
        ClientAPI.Log("Unable to determine name position for object with oid: %s" % str(worldObj.OID))
        return
    screenPos = ClientAPI.GetScreenPosition(pos)
    if screenPos.z == 0:
        frame.Hide()
    else:
        cam = ClientAPI.GetPlayerCamera()
        dist = cam.Near + screenPos.z * (cam.Far - cam.Near)
        # constants to determine when names fade out
        maxFade = 40000.0
        minFade = 20000.0
        minDistance = ClientAPI.InputHandler.MinPlayerVisibleDistance
        if dist > maxFade:
            frame.Hide()
            return
        if dist < minDistance and worldObj == ClientAPI.GetPlayerObject():
            # This is the player, and the camera is close enough to the player
            # that we are hiding the player.  Hide the player's name as well.
            frame.Hide()
            return
        if ClientAPI.HardwareCaps is None:
            return
        screenWidth, screenHeight = ClientAPI.HardwareCaps.WindowSize
        screenX = int(screenWidth* screenPos.x)
        screenY = -1 * int(screenHeight * screenPos.y)
        # Adjust so that the bottom center of the widget matches the node position
        screenX = screenX - int(frame.GetWidth() / 2) + pixelOffset.X
        screenY = screenY + frame.GetHeight() + pixelOffset.Y
        alpha = 1.0
        if dist > minFade:
            alpha = 1.0 - (dist - minFade) / (maxFade - minFade)
        frame.SetAlpha(alpha)
        poid = worldObj.OID
        indicator = getglobal("_nameFrame_%s_tSpeakerIndicator" % str(poid))
        if ClientAPI.Voice.NowSpeaking(poid) or (worldObj == ClientAPI.GetPlayerObject() and ClientAPI.Voice.MicSpeaking()):
            indicator.Show()
        else:
            indicator.Hide()
        frame.SetPoint("TOPLEFT", "UIParent", "TOPLEFT", screenX, screenY)
        frame.Show()

def ObjectAddedHandler(worldObj):
    if worldObj == None:
        return
    if worldObj.ObjectType == ClientAPI.WorldObject.WorldObjectType.Npc or worldObj.ObjectType == ClientAPI.WorldObject.WorldObjectType.User:
        bubbleFrameName = "_bubbleFrame_%s" % worldObj.OID
        bubbleFrame = getglobal(bubbleFrameName)
        if bubbleFrame is None:
            bubbleFrame = ClientAPI.Interface.CreateFrame("Frame", bubbleFrameName, None, "MvChatBubble")
        bubbleFrame.Properties["worldObj"] = worldObj
        bubbleFrame.Properties["expire"] = None
        if "bubble" in worldObj.AttachmentPoints:
            bubbleFrame.Properties["attachment"] = "bubble"
            bubbleFrame.Properties["widgetOffset"] = Vector3.Zero
            bubbleFrame.Properties["pixelOffset"] = Point(0, 25)
        elif "name" in worldObj.AttachmentPoints:
            bubbleFrame.Properties["attachment"] = "name"
            bubbleFrame.Properties["widgetOffset"] = Vector3.Zero
            bubbleFrame.Properties["pixelOffset"] = Point(0, 35)
        else:
            bubbleFrame.Properties["attachment"] = None
            bubbleFrame.Properties["widgetOffset"] = Vector3(0, 1800, 0)
            bubbleFrame.Properties["pixelOffset"] = Point(0, 75)
        nameFrameName = "_nameFrame_%s" % worldObj.OID
        nameFrame = getglobal(nameFrameName)
        if nameFrame is None:
            nameFrame = ClientAPI.Interface.CreateFrame("Frame", nameFrameName, None, "MvFloatyName")
        nameFrame.Properties["worldObj"] = worldObj
        if "name" in worldObj.AttachmentPoints:
            nameFrame.Properties["attachment"] = "name"
            nameFrame.Properties["widgetOffset"] = Vector3.Zero
            nameFrame.Properties["pixelOffset"] = Point(0, 0)
        else:
            nameFrame.Properties["attachment"] = None
            nameFrame.Properties["widgetOffset"] = Vector3(0, 1800, 0)
            nameFrame.Properties["pixelOffset"] = Point(0, 0)
        nameTextFrameName = "_nameFrame_%sText" % worldObj.OID
        nameText = getglobal(nameTextFrameName)
        nameText.SetText(worldObj.Name)
        nameFrame.SetWidth(nameText.GetStringWidth() + 12)

def ObjectRemovedHandler(worldObj):
    if worldObj.ObjectType == ClientAPI.WorldObject.WorldObjectType.Npc or worldObj.ObjectType == ClientAPI.WorldObject.WorldObjectType.User:
        bubbleFrameName = "_bubbleFrame_%s" % worldObj.OID
        frame = getglobal(bubbleFrameName)
        if frame is not None:
            frame.Properties["worldObj"] = None
            frame.Hide()
        nameFrameName = "_nameFrame_%s" % worldObj.OID
        frame = getglobal(nameFrameName)
        if frame is not None:
            frame.Properties["worldObj"] = None
            frame.Hide()
            
def UiEventHandler(eventType, eventArgs):
    # the register for events causes us to register for all
    # ui events, but we are only interested in the ones with
    # event type of CHAT_MSG_SAY.
    if eventType != "CHAT_MSG_SAY":
        return
    text = eventArgs[0]
    worldObj = ClientAPI.World.GetObjectByName(eventArgs[1])
    bubbleFrameName = "_bubbleFrame_%s" % worldObj.OID
    frame = getglobal(bubbleFrameName)
    if frame is not None:
        expire = DateTime.Now.AddSeconds(5 + (1 * text.Length) / 5)
        frame.Properties["expire"] = expire
        frame.SetWidth(200)
        frame.SetHeight(200)
        textPart = getglobal(bubbleFrameName + "Text")
        textPart.SetText(text)
        # If I need to wrap, set the text width
        if textPart.GetStringWidth() > (200 - 12):
            # ClientAPI.Log("textpart string width = 200 - 12")
            textPart.SetWidth(200 - 12)
        else:
            # ClientAPI.Log("textpart string width = %s" % textPart.GetStringWidth())
            textPart.SetWidth(textPart.GetStringWidth())
        # ClientAPI.Log("textpart height = %s" % textPart.GetHeight())
        frame.SetWidth(textPart.GetWidth() + 12)
        frame.SetHeight(textPart.GetHeight() + 12)
    
# Register an event handler that will run when the world has been initialized.
ClientAPI.World.RegisterEventHandler('ObjectAdded', ObjectAddedHandler)
ClientAPI.World.RegisterEventHandler('ObjectRemoved', ObjectRemovedHandler)
ClientAPI.Interface.RegisterEventHandler('UiEvent', UiEventHandler)

# Unfortunately, the player may have already been added by the time we
# load our UI code (though this should probably change later).
# Use this method to add a bubble frame to the player
playerObj = ClientAPI.GetPlayerObject()
if playerObj is not None:
    ObjectAddedHandler(playerObj)
