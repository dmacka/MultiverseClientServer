import ClientAPI
import StaticAnim

# This function is an event handler that runs when the world has been initialized.
def WorldInitHandler(sender, args):
    pass
#    # In the character selection world, I don't really want shadows until I 
#    # can turn off the shadow receive on the sky cylinder.
#    if not ClientAPI.World.IsWorldLocal:
#        ClientAPI.ShadowConfig.ShadowTechnique = ClientAPI.ShadowTechnique.Depth

# Register an event handler that will run when the world has been initialized.
ClientAPI.World.RegisterEventHandler('WorldInitialized', WorldInitHandler)
