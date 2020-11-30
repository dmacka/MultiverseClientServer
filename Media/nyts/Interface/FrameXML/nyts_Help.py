def nyts_Help_fMain_OnLoad(frame):
    nyts_Help_fMain_txMain.SetVertexColor(0.8, 0.8, 0.6)
    nyts_Help_fMain_bOK_txButton.SetVertexColor(0.8, 0.8, 0.6)
    nyts_Help_fMain.Show()

def nyts_Help_fMain_OnShow(f):
    pass

def nyts_Help_Scale(xScale, yScale):
    nyts_Help_fMain.SetWidth(nyts_Help_fMain.GetWidth() * xScale)
    nyts_Help_fMain.SetHeight(nyts_Help_fMain.GetHeight() * yScale)

    nyts_Help_fMain_fsName.SetWidth(nyts_Help_fMain_fsName.GetWidth() * xScale)
    nyts_Help_fMain_fsName.SetHeight(nyts_Help_fMain_fsName.GetHeight() * yScale)
    nyts_Help_fMain_fsName.SetTextHeight(12)

    nyts_Help_fMain_fsMovement.SetWidth(nyts_Help_fMain_fsMovement.GetWidth() * xScale)
    nyts_Help_fMain_fsMovement.SetHeight(nyts_Help_fMain_fsMovement.GetHeight() * yScale)
    nyts_Help_fMain_fsMovement.SetTextHeight(12)

    nyts_Help_fMain_fsCamera.SetWidth(nyts_Help_fMain_fsCamera.GetWidth() * xScale)
    nyts_Help_fMain_fsCamera.SetHeight(nyts_Help_fMain_fsCamera.GetHeight() * yScale)
    nyts_Help_fMain_fsCamera.SetTextHeight(12)

    nyts_Help_fMain_fsChat.SetWidth(nyts_Help_fMain_fsChat.GetWidth() * xScale)
    nyts_Help_fMain_fsChat.SetHeight(nyts_Help_fMain_fsChat.GetHeight() * yScale)
    nyts_Help_fMain_fsChat.SetTextHeight(12)
