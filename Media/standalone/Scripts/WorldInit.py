import System
import ClientAPI
import SAUtil

# This function is an event handler that runs when the world has been initialized.
def WorldInitHandler(sender, args):
    ClientAPI.Log("Running WorldInitHandler")
    #if ClientAPI.World.WorldName != "standalone":
    ClientAPI.World.DisplayTerrain = False
    ClientAPI.OceanConfig.ShowOcean = False
    ClientAPI.ShadowConfig.ShadowTechnique = ClientAPI.ShadowTechnique.None
    
    SAUtil.SetupWorld()
    
    ClientAPI.Log("Done running WorldInitHandler")
    
# Register an event handler that will run when the world has been initialized.
ClientAPI.World.RegisterEventHandler('WorldInitialized', WorldInitHandler)
