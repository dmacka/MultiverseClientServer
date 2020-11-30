import ClientAPI
import SAUtil
import Crowd
import FastScreenshot

class SceneEffect:

    def __init__(self, oid):
        self.OID = oid
        
    def CancelEffect(self):
        pass
        
    def UpdateEffect(self):
        pass
        
    def ExecuteEffect(self):
        ClientAPI.Log('Before BuildCrowd')
        Crowd.BuildCrowd(100)
        ClientAPI.Log('After BuildCrowd')
        
        # wait for 5 seconds for crowd to spawn
        yield 5000
        
        # start the camera path
        ClientAPI.Write('Before CameraPathEffect')
        ClientAPI.InvokeEffect("CameraPathEffect", ClientAPI.GetLocalOID(), {})
        ClientAPI.Write('After CameraPathEffect')
        
        # wait for 2 seconds for the path to get going
        yield 2000
        
        
        FastScreenshot.Screenshots(300)
        
        yield 21000
        ClientAPI.Write("Scene Done")
        ClientAPI.Exit()
        
# register the effect
ClientAPI.RegisterEffect("SceneEffect", SceneEffect)