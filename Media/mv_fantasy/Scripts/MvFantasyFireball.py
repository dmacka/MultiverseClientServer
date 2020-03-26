import ClientAPI

def OrientBetweenPoints(startPoint, endPoint):
    axis = endPoint - startPoint
    zVec = -axis
    zVec.Normalize()
    xVec = ClientAPI.Vector3.UnitY.Cross(zVec)
    xVec.Normalize()
    yVec = zVec.Cross(xVec)
    yVec.Normalize()
    quat = ClientAPI.Quaternion(0,0,0,0)
    quat.FromAxes(xVec, yVec, zVec)
    return quat

class MvFantasyFireball:

    #
    # Class constructor
    #
    def __init__(self, oid):
        # save the instance oid for this instance of the effect
        self.OID = oid
        
    #
    # This method is called to cancel the effect.
    #  XXX - Not supported in Multiverse Platform Beta 2
    #
    def CancelEffect(self):
        pass

    #
    # This method is called to update the effect.
    #  XXX - Not supported in Multiverse Platform Beta 2
    #        
    def UpdateEffect(self):
        pass
        
    #
    # This method is called to execute the effect.
    #              
    def ExecuteEffect(self, targetOID, sourceOID):
        targetSlot = 'primaryWeapon'
    
        # convert the object IDs sent from the server to the actual WorldObjects
        target = ClientAPI.World.GetObjectByOID(targetOID)
        caster = ClientAPI.World.GetObjectByOID(sourceOID)
                
        # create a unique name for the projectile particle system
        projectileParticlesName = 'projectileParticles' + str(self.OID)
        tailParticlesName = 'tailParticles' + str(self.OID)
        
        # create a particle system instance of the 'fireball-projectile' particle system
        projectileParticles = ClientAPI.ParticleSystem.ParticleSystem(projectileParticlesName, 'fireball-projectile')
        tailParticles = ClientAPI.ParticleSystem.ParticleSystem(tailParticlesName, 'fireball-tail')

        # create a point light to go along with the particle effect
        light = ClientAPI.Light.Light('movingLight' + str(self.OID))
        light.Diffuse = ClientAPI.ColorEx.Red
        light.AttenuationRange = 1000000
        light.AttenuationConstant = 0
        light.AttenuationLinear = 0.001
        light.Type = ClientAPI.Light.LightType.Point

        # compute the start and end points of the projectile path
        startLoc = caster.AttachmentPointPosition(targetSlot)
        endLoc = target.AttachmentPointPosition(targetSlot)

        orient = OrientBetweenPoints(startLoc, endLoc)
        
        # create new scene node for the projectile, which will move from the caster to the target
        projectileNodeName = 'projectileNode' + str(self.OID)
        projectileNode = ClientAPI.SceneNode.SceneNode(projectileNodeName)
        projectileNode.Parent = ClientAPI.RootSceneNode
        projectileNode.Position = startLoc
        projectileNode.Orientation = orient
        
        # now attach the particle system and the light to the node that we will animate
#        axe = ClientAPI.Model.Model('projectileAxe' + str(self.OID), 'axe.mesh')
#        projectileNode.AttachObject(axe)
        projectileNode.AttachObject(projectileParticles)
        projectileNode.AttachObject(tailParticles)
        projectileNode.AttachObject(light)
        
        # specify the length of the projectile flight in seconds
        animationLength = 1
        
        # create a new animation for the path of the projectile
        animName = 'projectilePath' + str(self.OID)
        anim = ClientAPI.Animation.Animation(animName, animationLength)
        
        # enable the animation
        anim.Enabled = True
        
        # create an animation track for the SceneNode
        track = anim.CreateNodeTrack(projectileNode)
        
        # create the starting key frame, which is at time 0, and the starting 
        # location of the projectile path
        k1 = track.CreateKeyFrame(0)
        k1.Translate = startLoc
        k1.Orientation = orient
        
        # create the ending key frame, which is at the end time, and the ending
        # location of the projectile
        k2 = track.CreateKeyFrame(animationLength)
        k2.Translate = endLoc
        k2.Orientation = orient

        # save the ending key frame in the object instance so that it is accessible
        # by the movement event handler
        self.targetKeyFrame = k2
        
        # create a node at the target attachment point
        targetNode = target.AttachNode(targetSlot)
        
        # Register an event handler to track the movements of the target node.
        # The event handler will update the ending keyframe of the animation
        # as the target moves around, so that the projectile will end up
        # hitting the target even if it moves.
        targetNode.RegisterEventHandler('Updated', self.targetMoveHandler)

        # run the animation
        anim.Play()
                
        # wait for the animation to move the projectile to the target
        yield animationLength * 1000
        
        # remove the event handler
        targetNode.RemoveEventHandler('Updated', self.targetMoveHandler)
        
        # remove the temporary target node
        target.DetachNode(targetNode)
        
        # free the animation
        anim.Dispose()
        
        # detach the particle system and light from the projectile node
        projectileNode.DetachObject(projectileParticles)
        projectileNode.DetachObject(tailParticles)
        projectileNode.DetachObject(light)
        
        # free the projectile node
        projectileNode.Dispose()

        # attach the particle system and light to the target attachment point
        target.AttachObject(targetSlot, projectileParticles)
#        target.AttachObject(targetSlot, tailParticles)
        target.AttachObject(targetSlot, light)
        
        # create a new particle system 
        blastName = 'blastParticles' + str(self.OID)
        blastParticles = ClientAPI.ParticleSystem.ParticleSystem(blastName, 'fireball-blast')
        target.AttachObject(targetSlot, blastParticles)
        
        # check to see which animation is available for the target being hit.
        # we have to do this because the current Multiverse models don't have consistent
        # animation names.
#        if 'recoil' in target.Model.AnimationNames:
#            target.QueueAnimation('recoil')
#        elif 'hurt' in target.Model.AnimationNames:
#            target.QueueAnimation('hurt')
            
        # Create a property animation to change the light attenuation and color.
        # This will change the color of the light and increase the area that it
        # affects during the final blast effect.
        lightAnimLength = 1.0
        lightAnim = ClientAPI.Animation.Animation('light' + str(self.OID), lightAnimLength)
        lightAnim.InterpolationMode = ClientAPI.Animation.InterpolationMode.Linear
        lightAnim.Enabled = True
        
        # create animation tracks for the two properties we want to animate
        lightColorTrack = lightAnim.CreatePropertyTrack(light.CreateAnimableValue('Diffuse'))
        lightAttenuationTrack = lightAnim.CreatePropertyTrack(light.CreateAnimableValue('AttenuationLinear'))
        
        # create key frames for color animation track
        keyFrame = lightColorTrack.CreateKeyFrame(0)
        keyFrame.PropertyValue = light.Diffuse
        keyFrame = lightColorTrack.CreateKeyFrame(lightAnimLength/2)
        keyFrame.PropertyValue = ClientAPI.ColorEx.Orange
        keyFrame = lightColorTrack.CreateKeyFrame(lightAnimLength)
        keyFrame.PropertyValue = ClientAPI.ColorEx.Black

        # create key frames for attenuation animation track
        keyFrame = lightAttenuationTrack.CreateKeyFrame(0)
        keyFrame.PropertyValue = light.AttenuationLinear
        keyFrame = lightAttenuationTrack.CreateKeyFrame(lightAnimLength/2.0)
        keyFrame.PropertyValue = 0.0001
        keyFrame = lightAttenuationTrack.CreateKeyFrame(lightAnimLength*0.8)
        keyFrame.PropertyValue = 0.001
        keyFrame = lightAttenuationTrack.CreateKeyFrame(lightAnimLength)
        keyFrame.PropertyValue = 1
        
        # play the light property animation
        lightAnim.Play()
        
        # wait for the explosion to dissipate            
        yield 1000
        
        # remove both particle effects
        target.DetachObject(projectileParticles)
#        target.DetachObject(tailParticles)
        target.DetachObject(blastParticles)
        target.DetachObject(light)
        
        # free the light, its animation, and the particle systems
        lightAnim.Dispose()
        light.Dispose()
        projectileParticles.Dispose()
        blastParticles.Dispose()
        
    def targetMoveHandler(self, position, orientation, scale):
        self.targetKeyFrame.Translate = position
    
# register the effect
ClientAPI.World.RegisterEffect("MvFantasyFireball", MvFantasyFireball)
