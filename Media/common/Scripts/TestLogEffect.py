import ClientAPI

class TestLogEffect:

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
    def ExecuteEffect(self, message):
        # write the unique object ID of this effect instance, along with the 
        # message parameter to the client chat window and the log file
        ClientAPI.DebugWrite('Effect Instance: ' + str(self.OID) + ' Message: ' + message)
        
# register the effect
ClientAPI.World.RegisterEffect("TestLogEffect", TestLogEffect)

