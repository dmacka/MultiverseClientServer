import ClientAPI

def ToggleShadows():
    shadowTechnique = ClientAPI.ShadowConfig.ShadowTechnique
    if shadowTechnique == ClientAPI.ShadowTechnique.None:
        ClientAPI.ShadowConfig.ShadowTechnique = ClientAPI.ShadowTechnique.Depth
    else:
        ClientAPI.ShadowConfig.ShadowTechnique = ClientAPI.ShadowTechnique.None
        