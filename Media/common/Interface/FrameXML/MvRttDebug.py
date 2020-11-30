import ClientAPI

class RttState:
    debugRttAtlases = []

def RttWidget_Update():
    # RttHighlightFrame.Hide()
    textureButtons = []
    for i in range(1, 10):
        buttonName = 'RttTextureButton%d' % i
        button = getglobal(buttonName):
        if button is not None:
            button.Hide()
            textureButtons.append(button)
        else:
            textureButtons.append(None)
    tex = getglobal('RttTexture')
    if tex:
        tex.Hide()
    chainInfo = Compositor.GetCompositorChainInfo()
    ClientAPI.Write("Chain has %d enabled instances" % len(chainInfo))
    i = 0
    for entry in chainInfo:
        ClientAPI.Write("Instance %s has %d defs" % (entry[0], len(entry[1])))
        for texDefInfo in entry[1]:
            instName = inst.GetTextureInstanceName(texDef.Name)
            ClientAPI.Write("tex.Name = %s\n" % texDefInfo[1])
            if i < len(textureButtons):
                button = textureButtons[i]
                button.SetText(texDefInfo[0])
                button.Properties['TextureImage'] = 'Interface\\%s\\RttImage' % texDefInfo[1]
                button.Show()
                i = i + 1

def RttTextureButton_OnClick(frame):
    RttUpdateTextureButtons(frame.GetID())

def RttDebug_OnLoad(frame):
    frame.SetPoint("TOPRIGHT", "UIParent", "TOPRIGHT", -13, -70)
    frame.SetHeight(300)
    frame.SetWidth(500)
    frame.SetBackdropColor(0, 0, 0)

def RttUpdateTextureButtons(id):
    ClientAPI.Write("click on %d" % id)
    for i in range(1, 10):
        button = getglobal('RttTextureButton%d' % i)
        if button:
            if button.GetID() == id:
                button.SetTextColor(1.0, 1.0, 1.0)
                button.LockHighlight()
                # RttHighlightFrame.SetPoint("TOPLEFT", button.GetName(), "TOPLEFT", -5, 0)
                # RttHighlightFrame.Show()
                if button.Properties.ContainsKey('TextureImage'):
                    textureFrame = getglobal('RttTexture')
                    if textureFrame:
                        ClientAPI.Write("Setting image to %s" % button.Properties['TextureImage'])
                        textureFrame.SetNormalTexture(button.Properties['TextureImage'])
                        textureFrame.Show()
                    else:
                        ClientAPI.Write("No frame named 'RttTexture'")
                else:
                    ClientAPI.Write("No frame property named 'TextureImage'")
            else:
                button.SetTextColor(1.0, 0.82, 0.0)
                button.UnlockHighlight()
