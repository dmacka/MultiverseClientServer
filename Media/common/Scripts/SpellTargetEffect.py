import ClientAPI

class SpellTargetEffect:

    def __init__(self, oid):
        self.OID = oid
        
    def CancelEffect(self):
        pass
        
    def UpdateEffect(self):
        pass
        
    def ExecuteEffect(self, targetOID):
        target = ClientAPI.World.GetObjectByOID(targetOID)
    
        # load heal particle effects
        healParticleHearts = ClientAPI.ParticleSystem.ParticleSystem('healHearts' + str(ClientAPI.GetLocalOID()), 'heal-spell')
        healParticleSparkles = ClientAPI.ParticleSystem.ParticleSystem('healSparkles' + str(ClientAPI.GetLocalOID()), 'heal-spell-fountain')
    
        # add particle effects
        target.AttachObject('noattachpoint', healParticleHearts)
        target.AttachObject('noattachpoint', healParticleSparkles)
    
        targetLoc = target.Position
    
        # attach and play the sound
        #    sound = ClientAPI.GetSoundSource('DoneWet.wav', targetLoc)
        #    target.AttachSound(sound)
        #    sound.Play()

        # wait for one second for the particles to peter out
        yield 3000
        target.DetachObject(healParticleHearts)
        target.DetachObject(healParticleSparkles)
    
        # clean up sounds
        target.ClearSounds()
    
# register the effect
ClientAPI.World.RegisterEffect("SpellTargetEffect", SpellTargetEffect)
