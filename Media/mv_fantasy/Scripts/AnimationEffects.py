import ClientAPI

class PlayAnimation:

    def __init__(self, oid):
        self.OID = oid
        
    def CancelEffect(self):
        pass
        
    def UpdateEffect(self):
        pass
        
    def ExecuteEffect(self, sourceOID, animName):
 
        caster = ClientAPI.World.GetObjectByOID(sourceOID)
        casterLoc = caster.Position

        # attach and play the sound

        if not animName in caster.Model.AnimationNames:
            return

        # play animation
        caster.SetProperty('client.animationoverride', True)
        caster.QueueAnimation(animName)

        # wait for the duration of the animation to turn off the animation override        
        yield int(caster.Model.AnimationLength(animName) * 1000)
        
        caster.SetProperty('client.animationoverride', False)
        
        # clean up sounds
        #target.ClearSounds()

# register the effect
ClientAPI.World.RegisterEffect("PlayAnimation", PlayAnimation)

