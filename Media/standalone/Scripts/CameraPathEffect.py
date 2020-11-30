import ClientAPI
import SAUtil
                    
class CameraPathEffect:

    def __init__(self, oid):
        self.OID = oid
        
    def CancelEffect(self):
        pass
        
    def UpdateEffect(self):
        pass
        
    def ExecuteEffect(self):

        # create scene node
        pathNode = ClientAPI.SceneNode.SceneNode(SAUtil.GetUniqueName('pathNode'))
        pathNode.Parent = ClientAPI.RootSceneNode
        
        # Grab the camera and attach it to the camera node.
        # Save the old position and direction so we can restore them later.
        camera = ClientAPI.GetPlayerCamera()
        oldCameraPos = camera.Position
        oldCameraOrient = camera.Orientation
        ClientAPI.GrabPlayerCamera()
        camera.Position = ClientAPI.Vector3.Zero
        camera.Direction = -ClientAPI.Vector3.UnitZ
        pathNode.AttachObject(camera)
        
        # create the node animation from a path
        anim = SAUtil.NodeAnimFromPath('camerapath', pathNode)
        
        # Play the node animation        
        anim.Play()
        
        # Wait for the animation to finish
        yield int(anim.Length * 1000)
           
        # Set the camera back
        pathNode.DetachObject(camera)
        ClientAPI.ReleasePlayerCamera()
        camera.AutoTrackingTarget = None
        camera.Position = oldCameraPos
        camera.Orientation = oldCameraOrient
        
# register the effect
ClientAPI.World.RegisterEffect("CameraPathEffect", CameraPathEffect)
