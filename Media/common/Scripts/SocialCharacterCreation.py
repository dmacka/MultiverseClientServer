from System.Math import PI
from Axiom.Core import ColorEx
from Axiom.Graphics import LightType
from Axiom.MathLib import *

import ClientAPI
import CharacterCreation
import Input
import WorldObject
import Animation
import Light

class SocialCharacterCreationContext(CharacterCreation.CharacterCreationContext):
    #
    # Constructor
    #
    def __init__(self):
        CharacterCreation.CharacterCreationContext.__init__(self)
        self._male_models = [ 'casual04_m_mediumpoly.mesh', 'casual07_m_mediumpoly.mesh', 'casual10_m_mediumpoly.mesh', 'casual16_m_mediumpoly.mesh', 'casual21_m_mediumpoly.mesh', 'business03_m_mediumpoly.mesh', 'business05_m_mediumpoly.mesh', 'sportive01_m_mediumpoly.mesh', 'sportive09_m_mediumpoly.mesh' ]
        self._female_models = [ 'casual07_f_mediumpoly.mesh', 'casual06_f_mediumpoly.mesh', 'casual15_f_mediumpoly.mesh', 'casual19_f_mediumpoly.mesh', 'casual21_f_mediumpoly.mesh', 'business04_f_mediumpoly.mesh', 'sportive01_f_mediumpoly.mesh', 'sportive02_f_mediumpoly.mesh', 'sportive05_f_mediumpoly.mesh', 'sportive07_f_mediumpoly.mesh' ]
	# put some initial data in the create context, so that when we change attributes, we have a valid starting point
        self.SetAttributes("characterName", {"characterName":"", "model":"casual04_m_mediumpoly.mesh", "sex":"male"})

    #
    # Methods
    #
    def GetValidAttributeValues(self, attr):
        """Get the possible attribute values for attr, given the state of the
           other attributes in the _attrs dictionary"""
        print "In GetValidAttributeValues('%s')" % attr
        if attr == 'sex':
            rv = []
            if self._listContains(self._male_models, self._attrs['model']):
                rv.append('male')
            if self._listContains(self._female_models, self._attrs['model']):
                rv.append('female')
            return rv
        elif attr == 'model':
            rv = []
            if self._attrs['sex'] == 'male':
                rv.extend(self._male_models)
            elif self._attrs['sex'] == 'female':
                rv.extend(self._female_models)
            return rv
        else:
            raise "Invalid attribute %s" % attr
        return None

    def _setAttributes(self, primaryAttr, attrs):
        """This method requires primaryAttr to be a valid attribute name,
           and requires the entry for primaryAttr in the attrs dictionary to be valid.
           There must be a legitimate value for each other attribute.
           There must be an entry for each attribute in the attrs dictionary."""

        # we can always copy the name, since there are no real limitations on that
        if attrs.has_key('characterName'):
            self._attrs['characterName'] = attrs['characterName']

        if primaryAttr == 'sex':
            # setting the sex requires us to check the model
            self._attrs['sex'] = attrs['sex']
            possibleVals = self.GetValidAttributeValues('model')
            if attrs.has_key('model') and self._listContains(possibleVals, attrs['model']):
                self._attrs['model'] = attrs['model']
                # the combination of attributes is legal
                return True
            # the combination of attributes is illegal
            # if we don't have any possible values, throwing is fine
            self._attrs['model'] = possibleVals[0]
            return False
        else:
            # either the model was the primary attribute, or
            # some other non-sex attribute was.  Treat both
            # cases the same
            self._attrs['model'] = attrs['model']
            possibleVals = self.GetValidAttributeValues('sex')
            if attrs.has_key('sex') and self._listContains(possibleVals, attrs['sex']):
                self._attrs['sex'] = attrs['sex']
                # the combination of attributes is legal
                return True
            # the combination of attributes is illegal
            # if we don't have any possible values, throwing is fine
            self._attrs['sex'] = possibleVals[0]
            return False

    def OnAttributesUpdated(self):
        # Destroy the old model
        avatar = ClientAPI.World.GetObjectByName("avatar")
        if not avatar is None:
            avatar.Dispose()
        # Set up the new avatar model
        avatar = WorldObject.WorldObject(-10, "avatar", self._attrs['model'], Vector3(0, 23000, 0), False)
        avatar.QueueAnimation("idle_01")

class SocialCharacterSelectionContext(CharacterCreation.CharacterSelectionContext):
    def __init__(self):
        self.selectedCharacterId = None

    def SetAvatarDisplayContext(self, displayContextString):
        meshEntries = displayContextString.split('')
        submeshEntries = meshEntries[0].split('')
        ClientAPI.Log('Display Context contains %s submesh entries' % len(submeshEntries))
        meshName = submeshEntries[0]
        submeshNames = []
        materialNames = []
        submeshEntries = submeshEntries[1:]
        for j in range(0, len(submeshEntries) / 2):
            submeshNames.append(submeshEntries[2 * j])
            materialNames.append(submeshEntries[2 * j + 1])

        attachedEntries = meshEntries[1:]
        for i in range(0, len(attachedEntries)):
            submeshEntries = attachedEntries[i].split('')
            attachPoint = submeshEntries[0]
            attachedMeshName = submeshEntries[1]
            print '  Attachment Point: %s' % attachPoint
            print '    Mesh: %s' % attachedMeshName
            submeshEntries = submeshEntries[2:]
            for j in range(0, len(submeshEntries) / 2):
                print '      Submesh: %s' % submeshEntries[2 * j]
                print '      Material: %s' % submeshEntries[2 * j + 1]

        # Destroy the old model
        avatar = ClientAPI.World.GetObjectByName("avatar")
        if not avatar is None:
            avatar.Dispose()
        # Set up the new avatar model
        avatar = WorldObject.WorldObject(-10, "avatar", meshName, Vector3(0, 23000, 0), False)
        # Special handling for the case where we don't have any submesh info
        # This will just show all the meshes
        if len(submeshNames) == 0:
            avatar.QueueAnimation("idle_01")
            return
        for submeshName in avatar.Model.SubMeshNames:
            avatar.Model.HideSubMesh(submeshName)
        for i in range(0, len(submeshNames)):
            ClientAPI.Log('Submesh name and material: %s, %s' % (submeshNames[i], materialNames[i]))
            avatar.Model.SetSubMeshMaterial(submeshNames[i], materialNames[i])
            avatar.Model.ShowSubMesh(submeshNames[i])
        avatar.QueueAnimation("idle_01")

    def OnSelectionUpdated(self, characterId):
        displayContext = self.GetCharacterAttribute(characterId, 'displayContext')
        self.SetAvatarDisplayContext(displayContext)
        self.selectedCharacterId = characterId
        
    def DeleteSelectedCharacter(self):
        self.Delete(self.selectedCharacterId)


def CreateSpinAnimation(obj):
    """This is a utility method that produce a one second animation on the
       given object to rotate it."""
    animation = Animation.Animation("spinning", 1.0)
    animation_nodetrack = animation.CreateNodeTrack(obj.SceneNode)
    animation_nodetrack_kf0 = animation_nodetrack.CreateKeyFrame(0)
    animation_nodetrack_kf0.Translate = obj.Position
    animation_nodetrack_kf0.Orientation = obj.Orientation
    animation_nodetrack_kf1 = animation_nodetrack.CreateKeyFrame(.25)
    animation_nodetrack_kf1.Translate = obj.Position
    animation_nodetrack_kf1.Orientation = Quaternion.FromAngleAxis(.5 * PI, Vector3.UnitY) * obj.Orientation
    animation_nodetrack_kf2 = animation_nodetrack.CreateKeyFrame(.5)
    animation_nodetrack_kf2.Translate = obj.Position
    animation_nodetrack_kf2.Orientation = Quaternion.FromAngleAxis(PI, Vector3.UnitY) * obj.Orientation
    animation_nodetrack_kf3 = animation_nodetrack.CreateKeyFrame(.75)
    animation_nodetrack_kf3.Translate = obj.Position
    animation_nodetrack_kf3.Orientation = Quaternion.FromAngleAxis(1.5 * PI, Vector3.UnitY) * obj.Orientation
    animation_nodetrack_kf4 = animation_nodetrack.CreateKeyFrame(1)
    animation_nodetrack_kf4.Translate = obj.Position
    animation_nodetrack_kf4.Orientation = Quaternion.FromAngleAxis(2 * PI, Vector3.UnitY) * obj.Orientation
    return animation


def BuildInitialScene():
    """This method sets up the world objects for the character creation and
       character selection interface.  We aren't talking to the world server
       yet, so we can't get the information from there."""
    # Set up the ambient light color
    ClientAPI.AmbientLight.Color = ColorEx(0.2156863, 0.2588235, 0.2588235)
    # Throw in a directional light as well
    dirlight = Light.Light("dirlight")
    dirlight.Type = LightType.Directional
    dirlight.Direction = Vector3(.9100, 0, .4147)
    dirlight.Diffuse = ColorEx(0.7098039, 0.3568628, 0.654902)
    dirlight.Specular = ColorEx(0.6745098, 0.2431373, 0.6352941)
    # Put in a point light
    pointlight = Light.Light("pointlight")
    pointlight.Type = LightType.Point
    pointlight.Position = Vector3(100, 25300, 2200)
    pointlight.Diffuse = ColorEx(0.8117647, 0.7882353, 0.8705882)
    pointlight.Specular = ColorEx(0.8431373, 0.9058824, 0.9254902)
    pointlight.AttenuationRange = 5500
    # Set up the Gazebo
    platform = WorldObject.WorldObject(-1, "creation_gazebo_platform", "creation_gazebo.mesh", Vector3(0, 23000, 0), False)
    # Set up the sky cylinder
    skycyl = WorldObject.WorldObject(-2, "creation_skycyl", "creation_gazebo_skycyl.mesh", Vector3(0, 23000, 0), False)
    skycyl_anim = CreateSpinAnimation(skycyl)
    skycyl_anim.Play(.003, True)
    # For our startup world, we want to set the camera in a specific spot
    camera = ClientAPI.GetPlayerCamera()
    camera.Position = Vector3(0, 24500, 3000)
    camera.Orientation = Quaternion.FromAngleAxis(-.15, Vector3.UnitX)
    # Now set up the avatar model
    avatar = WorldObject.WorldObject(-10, "avatar", "tiny_cube.mesh", Vector3(0, 23000, 0), False)

   
# This function is an event handler that runs when the world has been initialized.
def WorldInitHandler(sender, args):
    """This method is intended to be called when the world is initialized.
       At that point, the world is fully prepared, and has the player object
       and terrain initialized."""
    if ClientAPI.World.IsWorldLocal:
        BuildInitialScene()

def WorldConnectHandler(sender, args):
    """This is intended to be called when we connect to a world.  This
       happens before the world is initialized."""
    if ClientAPI.World.IsWorldLocal:
        ClientAPI.Log("Connected to character selection world")
        # We skipped the rdp world connection, so inject the messages
        # we need to create the world
        CharacterCreation.InitializeStartupWorld()
        # Use our custom input handler that will handle gui events,
        # but doesn't control the camera or character.
        ClientAPI.InputHandler = ClientAPI.Input.GuiInputHandler()
    else:
        # This time we are really connected to the world
        ClientAPI.Log("Connected to real world")
        # Use the standard game input handler that will handle gui events,
        # as well as move the camera and character.
        ClientAPI.InputHandler = ClientAPI.Input.DefaultInputHandler()
    
# Register an event handler that will run when the world has been initialized.
ClientAPI.RegisterEventHandler('WorldConnect', WorldConnectHandler)

# Register an event handler that will run when the world has been initialized.
ClientAPI.World.RegisterEventHandler('WorldInitialized', WorldInitHandler)

# When the client connects to the world, skip the rdp world connection.
# When they click on the login widget, I will set this flag back to
# false, and send a portal message, which will initiate this connection
# again.
ClientAPI.World.IsWorldLocal = True

