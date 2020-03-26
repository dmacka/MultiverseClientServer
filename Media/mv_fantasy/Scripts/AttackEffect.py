import ClientAPI

class AttackEffect:

    def __init__(self, oid):
        self.OID = oid
        
    def CancelEffect(self):
        pass
        
    def UpdateEffect(self):
        pass

    def ExecuteEffect(self, targetOID, sourceOID):
 
        target = ClientAPI.World.GetObjectByOID(targetOID)
        caster = ClientAPI.World.GetObjectByOID(sourceOID)
        
        targetLoc = target.Position
        casterLoc = caster.Position

        animName = None
        if "attack" in caster.Model.AnimationNames:
            animName = "attack"
        elif "strike" in caster.Model.AnimationNames:
            animName = "strike"
        elif "combat_strike_rh" in caster.Model.AnimationNames:
            animName = "combat_strike_rh"

        # attach and play the sound
        sound = ClientAPI.GetSoundSource('swordhit.wav', targetLoc)
        target.AttachSound(sound)
        sound.Play()
        
        # play attack animation
        caster.SetProperty('client.animationoverride', True)
        caster.QueueAnimation(animName)

        # wait for the duration of the animation to turn off the animation override   
        yield int(caster.Model.AnimationLength(animName) * 1000)
        
        caster.SetProperty('client.animationoverride', False)
        
        # clean up sounds
        #target.ClearSounds()
    
# register the effect
ClientAPI.World.RegisterEffect("AttackEffect", AttackEffect)
