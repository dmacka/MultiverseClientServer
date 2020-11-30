import ClientAPI
import StaticAnim
import DetachHack

# This function is an event handler that runs when the world has been initialized.
def WorldInitHandler(sender, args):
    # In the character selection world, I don't really want shadows until I 
    # can turn off the shadow receive on the sky cylinder.
    if not ClientAPI.World.IsWorldLocal:
        ClientAPI.ShadowConfig.ShadowTechnique = ClientAPI.ShadowTechnique.Depth

# Register an event handler that will run when the world has been initialized.
ClientAPI.World.RegisterEventHandler('WorldInitialized', WorldInitHandler)

# This function is an event handler for a loading state change event
def OnLoadingStateChange(msg, startingLoad):
    ClientAPI.LogDebug("WorldInit.py OnLoadingStateChange(): startingLoad %s" % str(startingLoad))
    renderNewTargets = not startingLoad
    if startingLoad:
        # Should either put up a loading screen, or not UpdateRenderTargets,
        # but not both, because stopping updating of render targets will 
        # prevent the loading screen from being visible.

        # We're starting the load process, so mark the loadWindow 
        # visible first, and whack static geometry last.
        ClientAPI.World.SetLoadingScreenVisible(startingLoad)
        #ClientAPI.World.SetUpdateRenderTargets(renderNewTargets)
        #ClientAPI.World.RebuildStaticGeometry(msg, startingLoad)
    else:
        # We're ending the load process, so mark the whack static 
        # geometry first, and make the loadWindow invisible last.
        #ClientAPI.World.RebuildStaticGeometry(msg, startingLoad)
        #ClientAPI.World.SetUpdateRenderTargets(renderNewTargets)
        ClientAPI.World.SetLoadingScreenVisible(startingLoad)


ClientAPI.World.RegisterEventHandler('LoadingStateChanged', OnLoadingStateChange)
