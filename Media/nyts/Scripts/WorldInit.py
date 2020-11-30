import System
import ClientAPI
import StaticAnim

compositor = None
# This function is an event handler that runs when the world has been initialized.
def WorldInitHandler(sender, args):
    global compositor
    # In the character selection world, I don't really want shadows until I 
    # can turn off the shadow receive on the sky cylinder.
    ClientAPI.World.DisplayTerrain = False
    ClientAPI.ShadowConfig.ShadowTechnique = ClientAPI.ShadowTechnique.None

    if not ClientAPI.World.IsWorldLocal:
        ClientAPI.SetClientParameter("Camera.CameraDistance", "2200")
        ClientAPI.SetClientParameter("Camera.CameraPitch", "0")
        VPVersion = ClientAPI.HardwareCaps.MaxVertexProgramVersion.split('_')
        if (int(VPVersion[1]) >= 3):
            CurrentCompositor = 'HDR'
            compositor = ClientAPI.Compositor.Compositor(CurrentCompositor)
            # HDR needs a special listener
            ClientAPI.Compositor.SetupHDRListener(compositor)
            compositor.Enabled = True
            ClientAPI.DebugWrite("HDR *activated*: ALT-H to toggle")
        else:
            ClientAPI.DebugWrite("HDR not enabled")

# Register an event handler that will run when the world has been initialized.
ClientAPI.World.RegisterEventHandler('WorldInitialized', WorldInitHandler)

def ToggleHDR():
    global compositor
    # Check to see if we can enable HDRR
    VPVersion = ClientAPI.HardwareCaps.MaxVertexProgramVersion.split('_')
    if (int(VPVersion[1]) >= 3):
        compositor.Enabled = not compositor.Enabled
        if (compositor.Enabled):
            ClientAPI.DebugWrite("HDR *activated*: ALT-H to toggle")
        else:
            ClientAPI.DebugWrite("HDR deactivated: ALT-H to toggle")
    else:
        ClientAPI.DebugWrite("HDR not enabled")
