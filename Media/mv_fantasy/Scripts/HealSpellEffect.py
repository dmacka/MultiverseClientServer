import ClientAPI

class HealSpellEffect:

    def __init__(self, oid):
        self.OID = oid
        
    def CancelEffect(self):
        pass
        
    def UpdateEffect(self):
        pass
        
    def ExecuteEffect(self, targetOID, sourceOID):
 
        target = ClientAPI.World.GetObjectByOID(targetOID)
        caster = ClientAPI.World.GetObjectByOID(sourceOID)
        
        # load heal particle effects
        healParticleHearts = ClientAPI.ParticleSystem.ParticleSystem('healHearts' + str(ClientAPI.GetLocalOID()), 'heal-spell')
        healParticleSparkles = ClientAPI.ParticleSystem.ParticleSystem('healSparkles' + str(ClientAPI.GetLocalOID()), 'heal-spell-fountain')
        
        # add particle effects
        target.AttachObject('base', healParticleHearts)
        target.AttachObject('base', healParticleSparkles)
        
        targetLoc = target.Position
        casterLoc = caster.Position
        
        # play casting animation
        caster.QueueAnimation("attack")
        
        # attach and play the sound
        sound = ClientAPI.GetSoundSource('DoneWet.wav', targetLoc)
        target.AttachSound(sound)
        sound.Play()
        
        # create the decal
        decal = ClientAPI.Decal.Decal("eight-hearts.png", casterLoc.x, casterLoc.z, 2000, 2000)

        # Animate the decal by yielding for a single frame, and updating the decal
        # rotation and position each time we wake up.
        # Continue animating in a loop until the time has expired.
        startTime = ClientAPI.GetCurrentTime()
        currentTime = startTime
        singleRotation = 2000.0
        totalRotation = 2000
        
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
        
        # wait for one second for the particles to peter out
        yield 1000
        target.DetachObject(healParticleHearts)
        target.DetachObject(healParticleSparkles)
        
        # clean up sounds
        target.ClearSounds()
    
# register the effect
ClientAPI.World.RegisterEffect("HealSpellEffect", HealSpellEffect)
