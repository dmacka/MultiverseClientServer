import ClientAPI

class SpellCastingEffect:

    def __init__(self, oid):
        self.OID = oid
        
    def CancelEffect(self):
        pass
        
    def UpdateEffect(self):
        pass
        
    def ExecuteEffect(self, sourceOID, castingTime, decalTexture):
        caster = ClientAPI.World.GetObjectByOID(sourceOID)
    
        # load glow particle effects
        glowPrimaryParticle = ClientAPI.ParticleSystem.ParticleSystem('glowPrimary' + str(ClientAPI.GetLocalOID()), 'glow')
        glowSecondaryParticle = ClientAPI.ParticleSystem.ParticleSystem('glowSecondary' + str(ClientAPI.GetLocalOID()), 'glow')

        # add particle effects
        caster.AttachObject('primaryWeapon', glowPrimaryParticle)
        caster.AttachObject('secondaryWeapon', glowSecondaryParticle)
    
        casterLoc = caster.Position
    
        # play casting animation
        caster.QueueAnimation("combat_idle", 1.0, True)
    
        # create the decal
        decal = ClientAPI.Decal.Decal(decalTexture, casterLoc.x, casterLoc.z, 2000, 2000)

        # Animate the decal by yielding for a single frame, and updating the decal
        # rotation and position each time we wake up.
        # Continue animating in a loop until the time has expired.
        startTime = ClientAPI.GetCurrentTime()
        currentTime = startTime
        singleRotation = 2200.0
        totalRotation = castingTime
    
        while ( currentTime - startTime ) < totalRotation:
            rot = ( currentTime - startTime ) * 360.0 / singleRotation
            decal.Rotation = rot
            casterLoc = caster.Position
            decal.PosX = casterLoc.x
            decal.PosZ = casterLoc.z
            yield 1
            currentTime = ClientAPI.GetCurrentTime()
    
        # get rid of the decal
        decal.Dispose()
    
        # reset the animation
        animName = None
        if "attack" in caster.Model.AnimationNames:
            animName = "attack"
        elif "strike" in caster.Model.AnimationNames:
            animName = "strike"
        elif "combat_strike_rh" in caster.Model.AnimationNames:
            animName = "combat_strike_rh"
        caster.SetProperty('client.animationoverride', True)
        caster.QueueAnimation(animName)

        # wait while attack animation completes
        # wait for the duration of the animation to turn off the animation override   
        yield int(caster.Model.AnimationLength(animName) * 1000)
        
        caster.SetProperty('client.animationoverride', False)
    
        # get rid of the particles
        caster.DetachObject(glowPrimaryParticle)
        caster.DetachObject(glowSecondaryParticle)

# register the effect
ClientAPI.World.RegisterEffect("SpellCastingEffect", SpellCastingEffect)
