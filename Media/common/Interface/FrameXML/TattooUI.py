from Axiom.Input import MouseButtons

# constants for the tattoos
global NO_TATTOO
NO_TATTOO = 0
global TATTOO1
TATTOO1 = 1
global TATTOO2
TATTOO2 = 2
global TATTOO3
TATTOO3 = 3

# constants for the tattoo areas
global SHOULDER
SHOULDER = "Shoulder"
global BACK
BACK = "Back"


# based on the given tattoo 'constant' (TATTOO1, 2, or 3), change the pc's material
# to have that tattoo on the right area (also based on above 'constants') 
# (client side)  
def ChangeTattoo(tattoo, area):
    global NO_TATTOO
    if tattoo == NO_TATTOO:
        pass
    else:
        pass

# based on the given tattoo 'constant' (TATTOO1, 2, or 3), change the pc's display context
# to have that tattoo on the right area (also based on above 'constants') 
# (server side) 
def ChangeDC(tattoo, area):
    global NO_TATTOO
    if tattoo == NO_TATTOO:
        pass
    else:
        pass

# Sets the oldTattoo and oldTattooArea based on what the character's mesh is when the method is called.
# This method is only called upon opening the tattoo interface
def GetCurrentMaterial():
    global oldTattoo
    global oldTattooArea
    global TATTOO1
    global TATTOO2
    global TATTOO3
    global NO_TATTOO
    global SHOULDER
    global BACK
    material = "human.blah.blah.blah" # MaterialAPI.getMaterial() or whatever it really is
    if material == "material name a":
        oldTattoo = TATTOO1
        oldTattooArea = SHOULDER
    elif material == "b":
        oldTattoo = TATTOO1
        oldTattooArea = BACK
    elif material == "c":
        oldTattoo = TATTOO2
        oldTattooArea = SHOULDER
    elif material == "d":
        oldTattoo = TATTOO2
        oldTattooArea = BACK
    elif material == "e":
        oldTattoo = TATTOO3
        oldTattooArea = SHOULDER
    elif material == "f":
        oldTattoo = TATTOO3
        oldTattooArea = BACK
    else:
        oldTattoo = NO_TATTOO
        oldTattooArea = None
        
        
        
# The material the character has before opening the tattoo interface
global oldTattoo
oldTattoo = NO_TATTOO

# The location the character's tattoo has before opening the tattoo interface
global oldTattooArea
oldTattooArea = None

# The Tattoo currently selected in the interface
global chosenTattoo
chosenTattoo = NO_TATTOO

# Where the tattoo will be applied
global tattooArea
tattooArea = SHOULDER
                
def DrawTattoo():
    global chosenTattoo
    global TATTOO1
    global TATTOO2
    global TATTOO3
    global NO_TATTOO
    if chosenTattoo == NO_TATTOO:
        LESTattooFrameInnerFrameTattooFrameTexture.SetAlpha(0)
        LESTattooFrameInnerFramePictureFrameTexture.SetAlpha(1)
        LESTattooFrameTattoo1ButtonTexture.SetVertexColor(0.93, 0.93, 0.73)
        LESTattooFrameTattoo2ButtonTexture.SetVertexColor(0.93, 0.93, 0.73)
        LESTattooFrameTattoo3ButtonTexture.SetVertexColor(0.93, 0.93, 0.73)
    else:
        LESTattooFrameInnerFrameTattooFrameTexture.SetTexture("Interface\MvChat\Mv-ChatFrame-Interior")
        LESTattooFrameInnerFrameTattooFrameTexture.SetVertexColor(1, 1, 1)
        LESTattooFrameInnerFrameTattooFrameTexture.SetAlpha(1)
        LESTattooFrameInnerFramePictureFrameTexture.SetAlpha(0)
        LESTattooFrameInnerFrameTattooFrameTexture.SetTexture("Interface\TattooImages\Tattoo" + str(chosenTattoo) + "_" + str(tattooArea))
        LESTattooFrameTattoo1ButtonTexture.SetVertexColor(0.93, 0.93, 0.73)
        LESTattooFrameTattoo2ButtonTexture.SetVertexColor(0.93, 0.93, 0.73)
        LESTattooFrameTattoo3ButtonTexture.SetVertexColor(0.93, 0.93, 0.73)
        if chosenTattoo == TATTOO1:
            LESTattooFrameTattoo1ButtonTexture.SetVertexColor(0.8, 0.8, 0.6)
        elif chosenTattoo == TATTOO2:
            LESTattooFrameTattoo2ButtonTexture.SetVertexColor(0.8, 0.8, 0.6)
        elif chosenTattoo == TATTOO3:
            LESTattooFrameTattoo3ButtonTexture.SetVertexColor(0.8, 0.8, 0.6)

def DrawRagdoll():
    global tattooArea
    global SHOULDER
    global BACK
    if tattooArea == SHOULDER:
        LESTattooFrameShoulderButtonTexture.SetVertexColor(0.8, 0.8, 0.6)
        LESTattooFrameBackButtonTexture.SetVertexColor(0.93, 0.93, 0.73)
        LESTattooFrameInnerFramePictureFrameTexture.SetTexture("Interface\TattooImages\Shoulder")
    elif tattooArea == BACK:
        LESTattooFrameBackButtonTexture.SetVertexColor(0.8, 0.8, 0.6)
        LESTattooFrameShoulderButtonTexture.SetVertexColor(0.93, 0.93, 0.73)
        LESTattooFrameInnerFramePictureFrameTexture.SetTexture("Interface\TattooImages\Back")

def Draw():
    DrawTattoo()
    DrawRagdoll()

def TattooFrame_OnShow():
    global oldTattoo
    global chosenTattoo
    global NO_TATTOO
    global tattooArea
    global SHOULDER
    GetCurrentMaterial()
    chosenTattoo = NO_TATTOO
    tattooArea = SHOULDER
    Draw()

def TattooUIShoulderButton_OnClick(this, args):
    global tattooArea
    global chosenTattoo
    global SHOULDER
    global NO_TATTOO
    if args.Button == MouseButtons.Left:
        tattooArea = SHOULDER
        DrawRagdoll()
        if chosenTattoo != NO_TATTOO:
            DrawTattoo()
    else:
        pass
        
def TattooUIBackButton_OnClick(this, args):
    global tattooArea
    global chosenTattoo
    global BACK
    global NO_TATTOO
    if args.Button == MouseButtons.Left:
        tattooArea = BACK
        DrawRagdoll()
        if chosenTattoo != NO_TATTOO:
            DrawTattoo()
    else:
        pass

def TattooUITattoo1Button_OnClick(button, args):
    global TATTOO1
    global chosenTattoo
    if args.Button == MouseButtons.Left:
        chosenTattoo = TATTOO1
        DrawTattoo()
    else:
        pass
        
def TattooUITattoo2Button_OnClick(button, args):
    global TATTOO2
    global chosenTattoo
    if args.Button == MouseButtons.Left:
        chosenTattoo = TATTOO2
        DrawTattoo()
    else:
        pass
        
def TattooUITattoo3Button_OnClick(button, args):
    global TATTOO3
    global chosenTattoo
    if args.Button == MouseButtons.Left:
        chosenTattoo = TATTOO3
        DrawTattoo()
    else:
        pass

def TattooUIBuyButton_OnClick(button, args):
    if args.Button == MouseButtons.Left:
        global chosenTattoo
        ChangeTattoo(chosenTattoo, tattooArea)
        ChangeDC(chosenTattoo, tattooArea)
        TattooFrame_Close()
    else:
        pass
        
def TattooUIPreviewButton_OnClick(button, args):
    global chosenTattoo
    global tattooArea
    if args.Button == MouseButtons.Left:
        ChangeTattoo(chosenTattoo, tattooArea)
    else:
        pass
        
def TattooUIRemoveButton_OnClick(button, args):
    if args.Button == MouseButtons.Left:
        ChangeTattoo(NO_TATTOO, None)
        ChangeDC(NO_TATTOO, None)
        TattooFrame_Close()
    else:
        pass

def TattooUIExitButton_OnClick(button, args):
    global oldTattoo
    global oldTattooArea
    if args.Button == MouseButtons.Left:
        ChangeTattoo(oldTattoo, oldTattooArea)    
        TattooFrame_Close()
    else:
        pass
        
def TattooFrame_OnLoad(frame):
    frame.RegisterEvent("PROPERTY_tattoo")
    LESTattooFrame.Hide()
    LESTattooFrameTitle.SetVertexColor(0.1, 0.1, 0.1)
    LESTattooFrameTitle.SetAlpha(0.7)
    LESTattooFrameTexture.SetVertexColor(0.36, 0.44, 0.29)
    LESTattooFrameTexture.SetAlpha(0.7)
    LESTattooFrameExitButtonTexture.SetVertexColor(0.93, 0.93, 0.73)
    LESTattooFramePreviewButtonTexture.SetVertexColor(0.93, 0.93, 0.73)
    LESTattooFrameBuyButtonTexture.SetVertexColor(0.93, 0.93, 0.73)
    LESTattooFrameRemoveButtonTexture.SetVertexColor(0.93, 0.93, 0.73)
    LESTattooFrameInnerFrameTexture.SetVertexColor(0.93, 0.93, 0.73)
        
def TattooFrame_Close():
    LESTattooFrame.Hide()

def TattooFrame_Open():
    LESTattooFrame.Show()

def TattooFrame_OnEvent(frame, event):
    if event.eventType == "PROPERTY_tattoo":
        if event.eventArgs[0] == "any":
            oid = long(event.eventArgs[1])
            tattooObj = ClientAPI.World.GetObjectByOID(oid)
            tattooObj.SetProperty("click_handler", TattooFrame_OnClick)

def TattooFrame_OnClick(sender, e):
    TattooFrame_Open()

def ToggleTattooFrame():
    if LESTattooFrame.IsVisible():
        TattooFrame_Close()
    else:
        TattooFrame_Open()
