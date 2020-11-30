import ClientAPI
import SAUtil
                    
class DelayAnimEffect:

    def __init__(self, oid):
        self.OID = oid
        
    def CancelEffect(self):
        pass
        
    def UpdateEffect(self):
        pass
        
    def ExecuteEffect(self, target, delay, anim, loop=True):
        if delay > 0:
            yield delay
        target.SetProperty('client.animationoverride', True)
        target.QueueAnimation(anim, 1.0, loop)

# register the effect
ClientAPI.World.RegisterEffect("DelayAnimEffect", DelayAnimEffect)
