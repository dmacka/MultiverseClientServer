import ClientAPI
import SAUtil
import FastScreenshot
import SAScene

class SceneEffect:

    def __init__(self, oid):
        self.OID = oid
        
    def CancelEffect(self):
        pass
        
    def UpdateEffect(self):
        pass
        
    def ExecuteEffect(self):
        yield 100
        try:
            SAUtil.SetCameraAtMarker(SAScene.machinima.Scene.CameraMarker)
            player = ClientAPI.GetPlayerObject()
            if player is not None:
                player.SceneNode.Visible = False
    
            ClientAPI.Write("Before InvokeEffect")
            
            maxAnimLen = 0
            for sceneObj in SAScene.machinima.Scene.MobileObjects:
                for anim in sceneObj.Animations:
                    animDelay = int(anim.delay * 1000)
                    worldObj = SAUtil.MobileObjects[sceneObj]
                    animLen = animDelay + worldObj.Model.AnimationLength(anim.name)
                    ClientAPI.LogInfo("About to invoke DelayAnimEffect for %s %s %s %s" %  (worldObj.OID, animDelay, anim.name, anim.loop))
                    ClientAPI.World.InvokeEffect("DelayAnimEffect", worldObj.OID, {'target': worldObj, 'delay' : animDelay, 'anim' : anim.name, 'loop' : anim.loop })
                    if animLen > maxAnimLen:
                        maxAnimLen = animLen
    
            ClientAPI.Write("After InvokeEffect")

            lengthSec = 0
            try:
                lengthSec = SAScene.machinima.Scene.length
            except:
                ClientAPI.LogError("SAScene.machinima.Scene.length = '%s'" % SAScene.machinima.Scene.length)
                
            lengthMS = lengthSec * 1000
            if lengthMS < animLen:
                ClientAPI.LogWarn("LengthMS of %s is less than AnimLen of %s" % (lengthMS, animLen))
                
            ClientAPI.Write("Before Recording")

            fps = 15
            try:
                fps = SAScene.machinima.Render.FPS
            except:
                ClientAPI.LogError("SAScene.machinima.Render.FPS = '%s'" % SAScene.machinima.Render.FPS)

            yield int(1000 / fps + 1) # make sure a full frame has elapsed
            
            animLen = maxAnimLen
            
            FastScreenshot.Screenshots(lengthSec * fps)
            ClientAPI.Write("Taking %s Screenshots" % int(lengthSec * fps))
            while not FastScreenshot.ScreenshotsDone():
                yield 1
                
            ClientAPI.Write("After Recording")

            SAUtil.PositionPlayerFromCamera()
            ClientAPI.ReleasePlayerCamera()
            ClientAPI.Write("Scene Done")
        except Exception, e:
           ClientAPI.LogError("Failed to run effect: %s" % str(e))
           # Ugh, I'd like to get this stack trace, but it's more important
           # that the client exit on failure
           # raise
        except:
           ClientAPI.LogError("Failed to run effect")
           # raise
        # Perhaps we should actually set a flag, and exit from the main flow instead
        if not SAScene.machinima.Interactive:
            ClientAPI.Exit()
        
# register the effect
ClientAPI.World.RegisterEffect("SceneEffect", SceneEffect)
