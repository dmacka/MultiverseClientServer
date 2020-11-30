import ClientAPI
import SocialCharacterCreation
import System

# must be > 0
MaxNumChars = 6

createContext = SocialCharacterCreation.SocialCharacterCreationContext()
selectContext = SocialCharacterCreation.SocialCharacterSelectionContext()

# module scope variable to keep track of selected button
characterSlotID = 0

def MvSelectInitialize(f):
    global characterSlotID
    global MaxNumChars
    for i in range(0, MaxNumChars):
        createButton = getglobal("MvCharSelectionFrameButtonCreate%d" % i)
        createButton.Properties['characterID'] = None
    charEntries = ClientAPI.GetCharacterEntries()
    numCharsAvail = len(charEntries)
    if characterSlotID >= numCharsAvail:
        characterSlotID = numCharsAvail - 1
        ClientAPI.Log("Shifted character slot to %s" % characterSlotID) 
    if numCharsAvail < 1:
        return
    if numCharsAvail > MaxNumChars:
        numCharsAvail = MaxNumChars
    for i in range(0, numCharsAvail):
        createButton = getglobal("MvCharSelectionFrameButtonCreate%d" % i)
        createButton.SetText(charEntries[i]['characterName'])
        createButton.Properties['characterID'] = charEntries[i].CharacterId
    MvUpdateCharSelection()
        
def MvUpdateCharSelection():
    """Updates the character selection to match the global characterSlotID.
       This will update the highlight flags, and call
       selectContext.OnSelectionUpdated with the character id of that slot."""
    global characterSlotID
    global MaxNumChars
    charEntries = ClientAPI.GetCharacterEntries()
    numCharsAvail = len(charEntries)
    if numCharsAvail < 1:
        return
    if numCharsAvail > MaxNumChars:
        numCharsAvail = MaxNumChars
    for i in range(0, numCharsAvail):
        createButton = getglobal("MvCharSelectionFrameButtonCreate%d" % i)
        createButton.UnlockHighlight()
        if i == characterSlotID:
            createButton.LockHighlight()
    selectContext.OnSelectionUpdated(charEntries[characterSlotID].CharacterId)
    
def MvCreateInitialize(f):
    MvCharCreationNameCreateFrameNamedTextWidgetEditBox.SetText("")
    sex = createContext.GetAttribute('sex')
    if sex == "male":
        MvGenderSelectionMale_OnClick(f)
    else:
        MvGenderSelectionFemale_OnClick(f)
    _MvRotationSelectionDisplay()


def _MvRotationSelectionDisplay():
    possibleVals = createContext.GetValidAttributeValues('model')
    try:
        currentModel = createContext.GetAttribute('model')
        currentIndex = (possibleVals.index(currentModel)) + 1
    except:
        ClientAPI.Log("Caught exception in _MvRotationSelectionDisplay")
    label = getglobal("MvRotationSelectionFrameFrameSelectorsFontStringCurrent")
    label.SetText("%s of %s" % (currentIndex, possibleVals.Count))


def MvRotationSelectionNext_OnClick(f):
#    ClientAPI.Write("next")
    possibleVals = createContext.GetValidAttributeValues('model')
    newModel = possibleVals[0]
    currentIndex = 0
    try:
        currentModel = createContext.GetAttribute('model')
        ClientAPI.Log("Current Model: %s" % currentModel)
        currentIndex = possibleVals.index(currentModel)
        ClientAPI.Log("Current Index: %s" % currentIndex)
        newModel = possibleVals[(currentIndex + 1) % possibleVals.Count]
    except:
        ClientAPI.Log("Caught exception in MvRotationSelectionNext_OnClick")
    ClientAPI.Log("Selected %s from %s" % (newModel, possibleVals))
    createContext.SetAttribute('model', newModel)
    _MvRotationSelectionDisplay()


def MvRotationSelectionPrevious_OnClick(f):
#    ClientAPI.Write("previous")
    possibleVals = createContext.GetValidAttributeValues('model')
    newModel = possibleVals[0]
    currentIndex = 0
    try:
        currentModel = createContext.GetAttribute('model')
        currentIndex = possibleVals.index(currentModel)
        newModel = possibleVals[(currentIndex - 1) % possibleVals.Count]
    except:
        ClientAPI.Log("Caught exception in MvRotationSelectionNext_OnClick")
    ClientAPI.Log("Selected %s from %s" % (newModel, possibleVals))
    createContext.SetAttribute('model', newModel)
    _MvRotationSelectionDisplay()


def _reset_MvGenderSelection():
#    ClientAPI.Write("reset")
    button = getglobal("MvGenderSelectionFrameButtonFemale")
    # button.SetButtonState("NORMAL")
    button.UnlockHighlight()
    button = getglobal("MvGenderSelectionFrameButtonMale")
    # button.SetButtonState("NORMAL")
    button.UnlockHighlight()


def MvGenderSelectionFemale_OnClick(f):
    _reset_MvGenderSelection()
#    ClientAPI.Write("female")
    createContext.SetAttribute('sex', 'female')
    button = getglobal("MvGenderSelectionFrameButtonFemale")
    # button.SetButtonState("PUSHED", True)
    button.LockHighlight()
    _MvRotationSelectionDisplay()


def MvGenderSelectionMale_OnClick(f):
    _reset_MvGenderSelection()
#    ClientAPI.Write("male")
    createContext.SetAttribute('sex', 'male')
    button = getglobal("MvGenderSelectionFrameButtonMale")
    # button.SetButtonState("PUSHED", True)
    button.LockHighlight()
    _MvRotationSelectionDisplay()


def MvCharCreationCreate_OnClick(f):
    global characterSlotID
#    ClientAPI.Write("creation create")
    characterNameString = MvCharCreationNameCreateFrameNamedTextWidgetEditBox.GetText()
#    ClientAPI.Write("character name : '%s'" % characterNameString)
    createContext.SetAttribute('characterName', characterNameString)
    entry = None
    errorMessage = None
    try:
        ClientAPI.Log("Creating character for %s" % characterNameString)
        entry = createContext.CreateCharacter()
        ClientAPI.Log("Create call returned")
    except:
        errorMessage = "Exception thrown in CreateCharacter"
    if entry:
        if not entry.Status:
            errorMessage = "Server encountered an unknown error"
            if entry.ContainsKey('errorMessage'):
                errorMessage = entry['errorMessage']
                ClientAPI.Log("Server encountered error: '%s'" % errorMessage)
    else:
        if not errorMessage:
            errorMessage = "Unknown Error"
    if errorMessage:
        fontstring = getglobal("MvCharCreationDialogFrameFontString")
        fontstring.SetText(errorMessage)
        MvCCSDialog_Show()
        ClientAPI.Log("Create failed with error: %s" % errorMessage)
    else:
        ClientAPI.Log("Created character %s" % entry.CharacterId)
        # Set the character slot id to point to this character
        charEntries = ClientAPI.GetCharacterEntries()
        numCharsAvail = len(charEntries)
        characterSlotID = numCharsAvail - 1
        ClientAPI.Log("Selected character slot %s" % characterSlotID)
        MvSelectInitialize(f)
        MvCharSelection_Show()


def MvCharCreationCancel_OnClick(f):
#    ClientAPI.Write("cancel")
    charEntries = ClientAPI.GetCharacterEntries()
    numCharsAvail = len(charEntries)
    MvUpdateCharSelection()
    MvCharSelection_Show()


def MvCharSelectionPlay_OnClick(f):
#    ClientAPI.Write("play")
    global characterSlotID
    createButton = getglobal("MvCharSelectionFrameButtonCreate%d" % characterSlotID)
    characterId = createButton.Properties['characterID']
    if characterId is None:
        return
    # Display a status window
    fontstring = getglobal("MvCharCreationInfoFrameFontString")
    fontstring.SetText("Logging in ...")
    MvCharCreationInfoFrame.Show()
    try:
        selectContext.Login(characterId)
    except:
        MvCharCreationInfoFrame.Hide()
        fontstring = getglobal("MvCharCreationDialogFrameFontString")
        fontstring.SetText("Unknown Error")
        MvCharCreationDialogFrame.Show()


def MvCharSelectionQuit_OnClick(f):
    ClientAPI.Exit()


def MvCharSelectionAccept_OnClick(f):
#    ClientAPI.Write("accept")
    pass


def MvCharSelectionDelete_OnClick(f):
#    ClientAPI.Write("delete")
    pass


def MvCharSelectionCreate_OnClick(frame, id):
    global characterSlotID
    global MaxNumChars
    createButton = frame
    characterId = createButton.Properties['characterID']
    if characterId:
        characterSlotID = id
        ClientAPI.Log("Set character slot to %s" % characterSlotID) 
        MvUpdateCharSelection()
    else:
        MvCreateInitialize(frame)
        MvCharCreation_Show()


def MvCharCreationDialogOk_OnClick(f):
#    ClientAPI.Write("dialog ok")
    MvCharCreationDialogFrame.Hide()


def MvCharCreation_Show():
    MvCCSHideAll()
    MvCharCreationTitleFrame.Show()
    MvCharCreationNameCreateFrame.Show()
    MvCharCreationOptionsFrame.Show()
    MvCharCreationCancelBorderedButton.Show()
    MvCharCreationNameCreateFrameNamedTextWidgetEditBox.SetFocus()


def MvCharSelection_Show():
    MvCCSHideAll()
    MvCharSelectionTitleFrame.Show()
    MvCharSelectionFrame.Show()
    MvCharSelectionPlayQuitFrame.Show()
    MvCharCreationNameCreateFrameNamedTextWidgetEditBox.ClearFocus()


def MvCCSDialog_Show():
    MvCharCreationDialogFrame.Show()


def MvCCSHideAll():
    MvCharCreationTitleFrame.Hide()
    MvCharCreationNameCreateFrame.Hide()
    MvCharCreationOptionsFrame.Hide()
    MvCharCreationCancelBorderedButton.Hide()
    MvCharSelectionTitleFrame.Hide()
    MvCharSelectionFrame.Hide()
    MvCharSelectionPlayQuitFrame.Hide()
    MvCharCreationDialogFrame.Hide()


# ClientAPI.Write("MvCharCreation")


DialogBgTexture = getglobal("MvCharCreationDialogFrameTextureBackground")
DialogBgTexture.SetVertexColor(0.70588, 0.70588, 0.70588, 1.0)

DialogOkTexture = getglobal("MvCharCreationDialogFrameOkButtonTexture")
DialogOkTexture.SetVertexColor(0.81176, 0.81176, 0.81176, 1.0)

MvCharSelection_Show()
# MvChatFrame.Hide()

# ClientAPI.Write("MvCharCreation loaded")
