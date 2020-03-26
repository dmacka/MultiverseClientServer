import ClientAPI

CurrentCompositor = ''

class TestCompositorEffect:

    def __init__(self, oid):
        self.OID = oid
        
    def CancelEffect(self):
        pass
        
    def UpdateEffect(self):
        pass
        
    def ExecuteEffect(self):
        global CurrentCompositor
        
        waitTime = 3000
        
        CurrentCompositor = 'Embossed'
        compositor = ClientAPI.Compositor.Compositor(CurrentCompositor)
        compositor.Enabled = True
        ClientAPI.Write('Activating compositor: ' + CurrentCompositor)
        yield waitTime
        compositor.Dispose()

        CurrentCompositor = 'Invert'
        compositor = ClientAPI.Compositor.Compositor(CurrentCompositor)
        compositor.Enabled = True
        ClientAPI.Write('Activating compositor: ' + CurrentCompositor)
        yield waitTime
        compositor.Dispose()        

        CurrentCompositor = 'Laplace'
        compositor = ClientAPI.Compositor.Compositor(CurrentCompositor)
        compositor.Enabled = True
        ClientAPI.Write('Activating compositor: ' + CurrentCompositor)
        yield waitTime
        compositor.Dispose()

        CurrentCompositor = 'Posterize'
        compositor = ClientAPI.Compositor.Compositor(CurrentCompositor)
        compositor.Enabled = True
        ClientAPI.Write('Activating compositor: ' + CurrentCompositor)
        yield waitTime
        compositor.Dispose()
                
        CurrentCompositor = 'Old Movie'
        compositor = ClientAPI.Compositor.Compositor(CurrentCompositor)
        compositor.Enabled = True
        ClientAPI.Write('Activating compositor: ' + CurrentCompositor)
        yield waitTime
        compositor.Dispose()
        
        CurrentCompositor = 'Old TV'
        compositor = ClientAPI.Compositor.Compositor(CurrentCompositor)
        compositor.Enabled = True
        ClientAPI.Write('Activating compositor: ' + CurrentCompositor)
        yield waitTime
        compositor.Dispose()
        
        CurrentCompositor = 'Bloom'
        compositor = ClientAPI.Compositor.Compositor(CurrentCompositor)
        compositor.Enabled = True
        ClientAPI.Write('Activating compositor: ' + CurrentCompositor)
        yield waitTime
        compositor.Dispose()
        
        CurrentCompositor = 'BlackAndWhite'
        compositor = ClientAPI.Compositor.Compositor(CurrentCompositor)
        compositor.Enabled = True
        ClientAPI.Write('Activating compositor: ' + CurrentCompositor)
        yield waitTime
        compositor.Dispose()
        
        CurrentCompositor = 'Glass'
        compositor = ClientAPI.Compositor.Compositor(CurrentCompositor)
        compositor.Enabled = True
        ClientAPI.Write('Activating compositor: ' + CurrentCompositor)
        yield waitTime
        compositor.Dispose()
        
        CurrentCompositor = 'Sharpen Edges'
        compositor = ClientAPI.Compositor.Compositor(CurrentCompositor)
        compositor.Enabled = True
        ClientAPI.Write('Activating compositor: ' + CurrentCompositor)
        yield waitTime
        compositor.Dispose()
        
        CurrentCompositor = 'Tiling'
        compositor = ClientAPI.Compositor.Compositor(CurrentCompositor)
        compositor.Enabled = True
        ClientAPI.Write('Activating compositor: ' + CurrentCompositor)
        yield waitTime
        compositor.Dispose()
        
        CurrentCompositor = 'Gaussian Blur'
        compositor = ClientAPI.Compositor.Compositor(CurrentCompositor)
        # Gaussian Blur needs a special listener
        ClientAPI.Compositor.SetupGaussianListener(compositor)
        compositor.Enabled = True
        ClientAPI.Write('Activating compositor: ' + CurrentCompositor)
        yield waitTime
        compositor.Dispose()
        
        CurrentCompositor = 'Heat Vision'
        compositor = ClientAPI.Compositor.Compositor(CurrentCompositor)
        # Head Vision needs a special listener
        compositor.AddListener(ClientAPI.Compositor.HeatVisionListener())
        compositor.Enabled = True
        ClientAPI.Write('Activating compositor: ' + CurrentCompositor)
        yield waitTime
        compositor.Dispose()
        
        CurrentCompositor = 'Motion Blur'
        compositor = ClientAPI.Compositor.Compositor(CurrentCompositor)
        compositor.Enabled = True
        ClientAPI.Write('Activating compositor: ' + CurrentCompositor)
        yield waitTime
        compositor.Dispose()
        
        CurrentCompositor = 'HDR'
        compositor = ClientAPI.Compositor.Compositor(CurrentCompositor)
        # HDR needs a special listener
        ClientAPI.Compositor.SetupHDRListener(compositor)
        compositor.Enabled = True
        ClientAPI.Write('Activating compositor: ' + CurrentCompositor)
        yield waitTime
        compositor.Dispose()
        
        ClientAPI.Write('Compositor test finished.')
                
                
# register the effect
ClientAPI.World.RegisterEffect("TestCompositorEffect", TestCompositorEffect)
