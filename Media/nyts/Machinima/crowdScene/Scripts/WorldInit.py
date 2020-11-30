import System
import ClientAPI
import SAWorld
import SAUtil

def SetupPanorama():
    camera = ClientAPI.GetPlayerCamera()
    ClientAPI.GrabPlayerCamera()
    
    camera.FieldOfView = 90
    camera.Near = 15000
    camera.ProjectionType = ClientAPI.Camera.Projection.Orthographic
    
    pos, orient, props = SAWorld.Markers['panoramacam']
    upoffset = 8000.0
    camera.Position = ClientAPI.Vector3(pos.x, pos.y + upoffset, pos.z)
    camera.Orientation = orient
    camera.Pitch(-10)

# This function is an event handler that runs when the world has been initialized.
def WorldInitHandler(sender, args):
    ClientAPI.Log("Running WorldInitHandler")
    #if ClientAPI.World.WorldName != "standalone":
    ClientAPI.World.DisplayTerrain = False
    ClientAPI.ShadowConfig.ShadowTechnique = ClientAPI.ShadowTechnique.None
    
    SAUtil.SetupWorld()
    
    ClientAPI.Interface.ToggleVisibility()
    
    # SetupPanorama()
    
    ClientAPI.InvokeEffect("SceneEffect", ClientAPI.GetLocalOID(), {})
    
    ClientAPI.Log("Done running WorldInitHandler")
    
# Register an event handler that will run when the world has been initialized.
ClientAPI.World.RegisterEventHandler('WorldInitialized', WorldInitHandler)

