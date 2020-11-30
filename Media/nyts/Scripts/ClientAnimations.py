import ClientAPI

import MarsTarget

AnimationStates = {}

class MobAnimationState:
    def __init__(self, worldObj):
        self.worldObj = worldObj
        self.Dead = False
        self.Dance = False
        self.Gesture = False
        self.Combat = False        
        self.MovementSpeed = 0.0
        self.Moving = False
        self.LoopIdle = True
        self.CurrentMoveAnim = 'run'
        self.LoopMove = True
        self.PlayingAnim = ''
        self.AnimOverride = False
        self.runSound = None
        self.walkAnimName = 'walk'
        self.runAnimName = 'run'
        self.idleAnimName = 'idle'
        self.deathAnimName = 'death'
        self.danceAnimName = 'dance'
        self.gestureAnimName = 'talk_02'
        self.combatIdleAnimName = 'combat_idle'

        if self.worldObj == None:
            return

        if not 'idle' in self.worldObj.Model.AnimationNames:
            # ClientAPI.DebugWrite('remapping idle to idle_01 for model ' + self.worldObj.Model.Name + ', ' + self.worldObj.Name)
            if 'idle_01' in self.worldObj.Model.AnimationNames:
                self.idleAnimName = 'idle_01'
            else:
                self.idleAnimName = None
                
        if not 'run' in self.worldObj.Model.AnimationNames:
            # ClientAPI.DebugWrite('remapping run to walk for model ' + self.worldObj.Model.Name + ', ' + self.worldObj.Name)
            if 'walk' in self.worldObj.Model.AnimationNames:
                self.runAnimName = 'walk'
            else:
                self.runAnimName = None
                
        self.CurrentIdleAnim = self.idleAnimName
        if not 'combat_idle' in self.worldObj.Model.AnimationNames:
            self.combatIdleAnimName = self.idleAnimName
        
        # start the character as idle
        self.updateIdleAnim()
        
        # deal with the case where the object is moving at the time that we get
        #  the object added event
        if (self.worldObj.Direction.Length > 0.0):
            self.DirectionChangeHandler()
        
    def Dispose(self):
        if not self.runSound is None:
            #self.worldObj.DetachSound(self.runSound)
            self.runSound = None
            
    def DirectionChangeHandler(self):
        if self.worldObj == None:
            return
        self.setSpeed(self.worldObj.Direction.Length)
    
    def setIdleAnim(self, anim, loop):
        # ClientAPI.DebugWrite('Setting Idle Anim to: ' + anim)
        self.CurrentIdleAnim = anim
        self.LoopIdle = loop
        
    def setMoveAnim(self, anim, loop):
        # ClientAPI.DebugWrite('Setting Move Anim to: ' + anim)
        self.CurrentMoveAnim = anim
        self.LoopMove = loop
        
    def playAnim(self):
        if self.worldObj == None:
            return

        # dont play the animation if the override property is set
        if self.AnimOverride == False:
            if self.Moving:
                anim = self.CurrentMoveAnim
                loop = self.LoopMove
            else:
                anim = self.CurrentIdleAnim
                loop = self.LoopIdle
            if anim != self.PlayingAnim and not anim is None and anim in self.worldObj.Model.AnimationNames:
                # ClientAPI.DebugWrite('Playing anim: ' + anim + ' Object: ' + self.worldObj.Name)
                self.worldObj.QueueAnimation(anim, 1.0, loop)
                self.PlayingAnim = anim
        
    def updateIdleAnim(self):
        if self.worldObj == None:
            return

        if self.Dead:
            self.setIdleAnim(self.deathAnimName, False)
        elif self.Gesture:
            self.Dance = False
            self.setIdleAnim(self.gestureAnimName, True)
        elif self.Dance:
            self.setIdleAnim(self.danceAnimName, True)
        elif self.Combat:
            self.setIdleAnim(self.combatIdleAnimName, True)
        else:
            self.setIdleAnim(self.idleAnimName, True)
            
        self.playAnim()
            
    def updateMoveAnim(self):
        if self.worldObj == None:
            return

        if self.worldObj.PropertyExists('runThreshold'):
            runThreshold = float(self.worldObj.GetProperty('runThreshold'))
        else:
            runThreshold = 1750.0
            
        if self.MovementSpeed < runThreshold:
            self.setMoveAnim(self.walkAnimName, True)
        else:
            self.setMoveAnim(self.runAnimName, True)
            
        self.playAnim()
            
    def setDead(self, propName):
        if self.worldObj == None:
            return

        self.Dead = self.worldObj.GetProperty(propName)

        self.updateIdleAnim()        
            
        # ClientAPI.DebugWrite("Setting Dead to " + str(self.Dead))
        
    def setGesture(self, propName):
        if self.worldObj == None:
            return

        self.Gesture = self.worldObj.GetProperty(propName)
        self.updateIdleAnim()
        # ClientAPI.DebugWrite("Setting Gesture to " + str(self.Gesture))

    def setDance(self, propName):
        if self.worldObj == None:
            return

        self.Dance = self.worldObj.GetProperty(propName)
        self.updateIdleAnim()
        # ClientAPI.DebugWrite("Setting Dance to " + str(self.Dance))
    
    def setCombat(self, propName):
        if self.worldObj == None:
            return

        self.Combat = self.worldObj.GetProperty(propName)
        self.updateIdleAnim()
        # ClientAPI.DebugWrite("Setting Combat to " + str(self.Combat))

    def setRunThreshold(self, propName):
        self.updateMoveAnim()
        
    def setAnimOverride(self, propName):
        if self.worldObj == None:
            return

        override = self.worldObj.GetProperty(propName)
        if self.AnimOverride != override:
            self.AnimOverride = override
            # ClientAPI.DebugWrite("Setting Animation Override to " + str(self.AnimOverride))
            
            # when the override is turned on, clear the currently playing animation
            # when the override is turned off, play the current animation
            if override:
                self.PlayingAnim = ''
            else:
                self.playAnim()
                
    def setSpeed(self, speed):
        if self.worldObj == None:
            return

        # we can't just check equality here because we are deriving the speed from the direction
        # vector, and due to lack of precision, we don't always get the exact same answer, so
        # we just check to see if the difference is below a threshold.
        if abs(speed - self.MovementSpeed) > 1:
            # ClientAPI.DebugWrite('New Speed: ' + str(int(speed)) + ' Old Speed: ' + str(int(self.MovementSpeed)))
            self.MovementSpeed = speed
            if speed == 0:
                # ClientAPI.DebugWrite("Player stop")
                self.Moving = False
                self.playAnim()
                if not self.runSound is None:
                    self.worldObj.DetachSound(self.runSound)
                    self.runSound = None
            else:
                # ClientAPI.DebugWrite("Player move")
                self.Moving = True
                self.updateMoveAnim()
                # self.runSound = ClientAPI.GetSoundSource('human_run_grass.ogg', self.worldObj.Position, True)
                # self.worldObj.AttachSound(self.runSound)
                # self.runSound.Play()

    def PropertyChangeHandler(self, propName):
        if propName in self._propHandlers :
            self._propHandlers[propName](self, propName)
        # else:
            # ClientAPI.DebugWrite("Setting Property: " + propName)
    
    _propHandlers = { 'deadstate': setDead, 'dancestate': setDance, 'gesturestate': setGesture, 'combatstate': setCombat, 'client.animationoverride': setAnimOverride, 'runThreshold': setRunThreshold }

def DirectionChangeDispatcher(worldObj):
    AnimationStates[worldObj.OID].DirectionChangeHandler()
    
def PropertyChangeDispatcher(worldObj, propName):
    AnimationStates[worldObj.OID].PropertyChangeHandler(propName)

numPedestrians = 0

# This function is an event handler that runs when the world has been initialized.
def ObjectAddedHandler(worldObj):
    if worldObj.ObjectType == ClientAPI.WorldObject.WorldObjectType.User:
        # ClientAPI.DebugWrite("added User object")
        
        # register event handlers for object
        worldObj.RegisterEventHandler('DirectionChange', DirectionChangeDispatcher)
        worldObj.RegisterEventHandler('PropertyChange', PropertyChangeDispatcher)
        
        # create object to track animation state and save it in the dictionary
        AnimationStates[worldObj.OID] = MobAnimationState(worldObj)
        
        # ClientAPI.DebugWrite("Registered user event handlers")
    elif worldObj.ObjectType == ClientAPI.WorldObject.WorldObjectType.Npc:
        # ClientAPI.DebugWrite("added npc object")
        
        # register event handlers for object
        worldObj.RegisterEventHandler('DirectionChange', DirectionChangeDispatcher)
        worldObj.RegisterEventHandler('PropertyChange', PropertyChangeDispatcher)
        
        if worldObj.Name == 'Pedestrian':
            global numPedestrians
            numPedestrians = numPedestrians + 1
            if (numPedestrians > 0):
                # create object to track animation state and save it in the dictionary
                AnimationStates[worldObj.OID] = MobAnimationState(worldObj)
            else:
                AnimationStates[worldObj.OID] = MobAnimationState(None)
                model = worldObj.Model
                for submesh in model.SubMeshNames:
                    model.HideSubMesh(submesh)
                # worldObj.Dispose()
                # worldObj = None
        else:
            # create object to track animation state and save it in the dictionary
            AnimationStates[worldObj.OID] = MobAnimationState(worldObj)
        
        # ClientAPI.DebugWrite("Registered npc event handlers")
        
def ObjectRemovedHandler(worldObj):
    if worldObj.ObjectType == ClientAPI.WorldObject.WorldObjectType.User or worldObj.ObjectType == ClientAPI.WorldObject.WorldObjectType.Npc:
        #ClientAPI.DebugWrite("ClientAnimation: removing object")
        # clean up the state object
        AnimationStates[worldObj.OID].Dispose()

        # remove event handlers for object
        worldObj.RemoveEventHandler('DirectionChange', DirectionChangeDispatcher)
        worldObj.RemoveEventHandler('PropertyChange', PropertyChangeDispatcher)
    
        del AnimationStates[worldObj.OID]
        
def ToggleCombat():
    worldObj = MarsTarget.GetCurrentTarget()
    combat = worldObj.CheckBooleanProperty('combatstate')
    worldObj.SetProperty('combatstate', not combat)
    
def ToggleGesture(oid):
    worldObj = MarsTarget.GetCurrentTarget()
    gesture = worldObj.CheckBooleanProperty('gesturestate')
    worldObj.SetProperty('gesturestate', not gesture)

def ToggleDance(oid):
    worldObj = MarsTarget.GetCurrentTarget()
    dance = worldObj.CheckBooleanProperty('dancestate')
    worldObj.SetProperty('dancestate', not dance)

def ToggleDead():
    worldObj = MarsTarget.GetCurrentTarget()
    dead = worldObj.CheckBooleanProperty('deadstate')
    worldObj.SetProperty('deadstate', not dead)
    
# Register an event handler that will run when the world has been initialized.
ClientAPI.World.RegisterEventHandler('ObjectAdded', ObjectAddedHandler)
ClientAPI.World.RegisterEventHandler('ObjectRemoved', ObjectRemovedHandler)
