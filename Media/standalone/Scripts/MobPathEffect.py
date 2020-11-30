import ClientAPI
import SAUtil
                    
class MobPathEffect:

    def __init__(self, oid):
        self.OID = oid
        
    def CancelEffect(self):
        pass
        
    def UpdateEffect(self):
        pass
        
    def ExecuteEffect(self, targetOID, pathname):
        speed = 3000.0
        target = ClientAPI.World.GetObjectByOID(targetOID)
        path = SAUtil.Paths[pathname]
        
        # set mob position to start of path
        pathTime, pathLoc, pathOrient = path[3]
        target.Position = pathLoc
        
        # compute number of segments
        numSegments = len(path) - 1
        
        # iterate segments
        for segment in range(3, numSegments):
            pathTime, startLoc, pathOrient = path[segment]
            pathTime, endLoc, pathOrient = path[segment+1]
            
            # compute direction vector for this segment
            dirVector = endLoc - startLoc
            dirVector = ClientAPI.Vector3(dirVector.x, 0.0, dirVector.z)
            segmentLen = dirVector.Length
            dirVector.Normalize()
            ClientAPI.Write('MobPathEffect: dirVector = %s' % dirVector.ToString())
            dirVector = ClientAPI.Vector3(dirVector.x, 0.0, dirVector.z)
            speedVector = ClientAPI.Vector3(dirVector.x * speed, 0.0, dirVector.z * speed)
            ClientAPI.Write('MobPathEffect: dirVector w/speed = %s' % speedVector.ToString())
            
            # compute mob orientation
            orient = ClientAPI.Quaternion(1.0, 0.0, 0.0, 0.0)
            yaxis = ClientAPI.Vector3.UnitY
            xaxis = yaxis.Cross(dirVector)
            orient.FromAxes(xaxis, yaxis, dirVector)
            #target.Orientation = orient
            
            target.Direction = speedVector
            ClientAPI.Log('Before orientation change, pos = %s, dir = %s' % (target.Position.ToString(), target.Direction.ToString()))
            target.Orientation = orient
            ClientAPI.Log('After orientation change, pos = %s, dir = %s' % (target.Position.ToString(), target.Direction.ToString()))
            segmentTime = segmentLen / ( speed )
            ClientAPI.Write('MobPathEffect: segment %d: segmentLen = %f: segmentTime = %f: loc = %s' % (segment, segmentLen, segmentTime, target.Position.ToString()))
            yt =  int(segmentTime * 1000)
            ClientAPI.Write('Yielding for %s milliseconds' % yt)
            yield yt
        
# register the effect
ClientAPI.World.RegisterEffect("MobPathEffect", MobPathEffect)


def TestMobPathEffect():
    testProps = [
        ('SkinColor', 'caucasian'),
        ('HeadShape', 'caucasian_01'),
        ('HeadDetail', ''),
        ('HairStyle', 'bob'),
        ('HairColor', 'red'),
        ('ClothesTorso', 'strapless_purple'),
        ('ClothesLegs', 'short_skirt_red'),
        ('Tattoo', ''),
        ('AppearanceOverride', 'avatar')
    ]
    
    mob = ClientAPI.WorldObject.WorldObject(ClientAPI.GetLocalOID(), SAUtil.GetUniqueName('mob'), 'LES_avatar.mesh', ClientAPI.Vector3.Zero, True, ClientAPI.Quaternion.Identity, ClientAPI.Vector3.UnitScale, ClientAPI.WorldObject.WorldObjectType.Npc)
    for prop, value in testProps:
        mob.SetProperty(prop, value)
        
    #mob = ClientAPI.GetPlayerObject()
    #mob.SetProperty('world.nomove', True)
    #mob.SetProperty('world.noturn', True)
    ClientAPI.World.InvokeEffect("MobPathEffect", ClientAPI.GetLocalOID(), {'targetOID': mob.OID, 'pathname' : 'mobpath1'})
