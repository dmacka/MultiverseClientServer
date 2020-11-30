from System.Math import PI
from Axiom.Core import ColorEx
from Axiom.Graphics import LightType
from Axiom.MathLib import *
from Multiverse.Base import Client

import ClientAPI
import CharacterCreation
import WorldObject
import Animation
import Light
import WorldInit

newCharacterMeshInfo = { "casual06_f_mediumpoly.mesh"   : [[ "casual06_f_mediumpoly-mesh.0", "casual06_f_mediumpoly.body" ],
                                                           [ "casual06_f_mediumpoly-mesh.1", "casual06_f_mediumpoly.hair_transparent" ]],
                         "casual07_f_mediumpoly.mesh"   : [[ "casual07_f_mediumpoly-mesh.0", "casual07_f_mediumpoly.body" ],
                                                           [ "casual07_f_mediumpoly-mesh.1", "casual07_f_mediumpoly.hair_transparent" ]],
                         "casual13_f_mediumpoly.mesh"   : [[ "casual13_f_mediumpoly-mesh.0", "casual13_f_mediumpoly.body" ],
                                                           [ "casual13_f_mediumpoly-mesh.1", "casual13_f_mediumpoly.hair_transparent" ]],
                         "casual15_f_mediumpoly.mesh"   : [[ "casual15_f_mediumpoly-mesh.0", "casual15_f_mediumpoly.body" ],
                                                           [ "casual15_f_mediumpoly-mesh.1", "casual15_f_mediumpoly.hair_transparent" ]],
                         "casual19_f_mediumpoly.mesh"   : [[ "casual19_f_mediumpoly-mesh.0", "casual19_f_mediumpoly.body" ],
                                                           [ "casual19_f_mediumpoly-mesh.1", "casual19_f_mediumpoly.hair_transparent" ]],
                         "casual21_f_mediumpoly.mesh"   : [[ "casual21_f_mediumpoly-mesh.0", "casual21_f_mediumpoly.body" ],
                                                           [ "casual21_f_mediumpoly-mesh.1", "casual21_f_mediumpoly.hair_transparent" ]],
                         "business04_f_mediumpoly.mesh" : [[ "business04_mediumpoly-mesh.0", "business04_f_mediumpoly.body" ],
                                                           [ "business04_mediumpoly-mesh.1", "business04_f_mediumpoly.hair_transparent" ]],
                         "sportive01_f_mediumpoly.mesh" : [[ "sportive01_f_mediumpoly-mesh.0", "sportive01_f_mediumpoly.body" ],
                                                           [ "sportive01_f_mediumpoly-mesh.1", "sportive01_f_mediumpoly.hair_transparent" ]],
                         "sportive02_f_mediumpoly.mesh" : [[ "sportive02_f_mediumpoly-mesh.0", "sportive02_f_mediumpoly.body" ],
                                                           [ "sportive02_f_mediumpoly-mesh.1", "sportive02_f_mediumpoly.hair_transparent" ]],
                         "sportive05_f_mediumpoly.mesh" : [[ "sportive05_f_mediumpoly-mesh.0", "sportive05_f_mediumpoly.body" ],
                                                           [ "sportive05_f_mediumpoly-mesh.1", "sportive05_f_mediumpoly.hair_transparent" ]],
                         "sportive07_f_mediumpoly.mesh" : [[ "sportive07_f_mediumpoly-mesh.0", "sportive07_f_mediumpoly.body" ]],
                         "casual03_m_mediumpoly.mesh"   : [[ "casual03_m_medium-mesh.0", "casual03_m_mediumpoly.body" ]],
                         "casual04_m_mediumpoly.mesh"   : [[ "casual04_m_mediumpoly-mesh.0", "casual04_m_mediumpoly.body" ]],
                         "casual07_m_mediumpoly.mesh"   : [[ "casual07_m_mediumpoly-mesh.0", "casual07_m_mediumpoly.body" ]],
                         "casual10_m_mediumpoly.mesh"   : [[ "casual10_m_mediumpoly-mesh.0", "casual10_m_mediumpoly.body" ]],
                         "casual16_m_mediumpoly.mesh"   : [[ "casual16_m_mediumpoly-mesh.0", "casual16_m_mediumpoly.body" ]],
                         "casual21_m_mediumpoly.mesh"   : [[ "casual21_m_mediumpoly-mesh.0", "casual21_m_mediumpoly.body" ]],
                         "business03_m_mediumpoly.mesh" : [[ "business03_m_medium-mesh.0", "business03_m_mediumpoly.body" ]],
                         "business05_m_mediumpoly.mesh" : [[ "business05_m_mediumpoly-mesh.0", "business05_m_mediumpoly.body" ]],
                         "sportive01_m_mediumpoly.mesh" : [[ "sportive01_m_mediumpoly-mesh.0", "sportive01_m_mediumpoly.body" ]],
                         "sportive09_m_mediumpoly.mesh" : [[ "sportive09_m_mediumpoly-mesh.0", "sportive09_m_mediumpoly.body" ]], }


class nytsCharacterCreationContext(CharacterCreation.CharacterCreationContext):
    #
    # Constructor
    #
    def __init__(self):
        CharacterCreation.CharacterCreationContext.__init__(self)
        # set up some fields for convenience in later methods
        self._male_models   = [ 'casual03_m_mediumpoly.mesh',
                                'casual04_m_mediumpoly.mesh',
                                'casual07_m_mediumpoly.mesh',
                                'casual10_m_mediumpoly.mesh',
                                'casual16_m_mediumpoly.mesh',
                                'casual21_m_mediumpoly.mesh',
                                'business03_m_mediumpoly.mesh',
                                'business05_m_mediumpoly.mesh',
                                'sportive01_m_mediumpoly.mesh',
                                'sportive09_m_mediumpoly.mesh', ]
        self._female_models = [ 'casual06_f_mediumpoly.mesh',
                                'casual07_f_mediumpoly.mesh',
                                'casual13_f_mediumpoly.mesh',
                                'casual15_f_mediumpoly.mesh',
                                'casual19_f_mediumpoly.mesh', 
                                'casual21_f_mediumpoly.mesh', 
                                'business04_f_mediumpoly.mesh',
                                'sportive01_f_mediumpoly.mesh',
                                'sportive02_f_mediumpoly.mesh',
                                'sportive05_f_mediumpoly.mesh',
                                'sportive07_f_mediumpoly.mesh', ]
                                               
        # put some initial data in the create context, so that when we change attributes, we have a valid starting point
        self.SetAttributes("characterName", {"characterName":"", "model":"casual07_f_mediumpoly.mesh", "sex":"female"})

    #
    # Methods
    #
#    def GetAttribute(self, attr):
#        """Get the value of a current attribute."""
#        return self._attrs[attr]

#    def GetAttributes(self):
#        """Get a copy of the current attributes dictionary."""
#        return dict(self._attrs)

    def GetAttributeNames(self):
        """Get a list with the names of all the attribute names for our
           character creation system"""
        return ['characterName', 'sex', 'model']

    def GetPossibleAttributeValues(self, attr):
        """Get all the possible options for an attribute, or None
           if there is not a reasonably small set of valid attributes"""
        if attr == 'sex':
            return ['male', 'female']
        elif attr == 'model':
            rv = []
            rv.extend(self._male_models)
            rv.extend(self._female_models)
            return rv
        else:
            return None

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

#    def SetAttribute(self, attr, val):
#        """This method sets a single attribute.  Other attributes may end
#           up being altered by this change."""
#        attrs = self.GetAttributes()
#        attrs[attr] = val
#        return self.SetAttributes(attr, attrs)

#    def SetAttributes(self, primaryAttr, attrs):
#        """This method requires primaryAttr to be a valid attribute name,
#           and requires the entry for primaryAttr in the attrs dictionary to be valid.
#           There must be a legitimate value for each other attribute.
#           There must be an entry for each attribute in the attrs dictionary."""
#        ClientAPI.Log("Pre update attribute map: {%s}" % attrs)
#        rv = self._setAttributes(primaryAttr, attrs)
 #       ClientAPI.Log("Post update attribute map: {%s}" % self._attrs)
#        self.OnAttributesUpdated()
#        return rv

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
        if avatar is not None:
            avatar.Dispose()
        # Set up the new avatar model
        meshName = self._attrs['model']
        global newCharacterMeshInfo
        submeshInfo = newCharacterMeshInfo[meshName]
        # avatar = WorldObject.WorldObject(-10, "avatar", meshName, Vector3(0, 23000, 0), False)
        avatar = WorldObject.WorldObject(ClientAPI.GetLocalOID(), "avatar", meshName, Vector3(127098.7, 20660, -355373.9), False, Quaternion(0.6156615, 0, -0.7880107, 0), Vector3(1, 1, 1))
        for submeshName in avatar.Model.SubMeshNames:
            avatar.Model.HideSubMesh(submeshName)
        for i in range(0, len(submeshInfo)):
            ClientAPI.Log('Submesh name and material: %s, %s' % (submeshInfo[i][0], submeshInfo[i][1]))
            avatar.Model.SetSubMeshMaterial(submeshInfo[i][0], submeshInfo[i][1])
            avatar.Model.ShowSubMesh(submeshInfo[i][0])
        avatar.QueueAnimation("idle_01", 1.0, True)


class nytsCharacterSelectionContext(CharacterCreation.CharacterSelectionContext):
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
        if avatar is not None:
            avatar.Dispose()
        # Set up the new avatar model
        # avatar = WorldObject.WorldObject(-10, "avatar", meshName, Vector3(0, 23000, 0), False)
        avatar = WorldObject.WorldObject(ClientAPI.GetLocalOID(), "avatar", meshName, Vector3(127098.7, 20660, -355373.9), False, Quaternion(0.6156615, 0, -0.7880107, 0), Vector3(1, 1, 1))
        # Special handling for the case where we don't have any submesh info
        # This will just show all the meshes
        if len(submeshNames) == 0:
            avatar.QueueAnimation("idle_01", 1.0, True)
            return
        for submeshName in avatar.Model.SubMeshNames:
            avatar.Model.HideSubMesh(submeshName)
        for i in range(0, len(submeshNames)):
            ClientAPI.Log('Submesh name and material: %s, %s' % (submeshNames[i], materialNames[i]))
            avatar.Model.SetSubMeshMaterial(submeshNames[i], materialNames[i])
            avatar.Model.ShowSubMesh(submeshNames[i])
        avatar.QueueAnimation("idle_01", 1.0, True)

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
#     # Set up the ambient light color
#     ClientAPI.AmbientLight.Color = ColorEx(0.2156863, 0.2588235, 0.2588235)
#     # Throw in a directional light as well
#     dirlight = Light.Light("dirlight")
#     dirlight.Type = LightType.Directional
#     dirlight.Direction = Vector3(.9100, 0, .4147)
#     dirlight.Diffuse = ColorEx(0.7098039, 0.3568628, 0.654902)
#     dirlight.Specular = ColorEx(0.6745098, 0.2431373, 0.6352941)
#     # Put in a point light
#     pointlight = Light.Light("pointlight")
#     pointlight.Type = LightType.Point
#     pointlight.Position = Vector3(100, 25300, 2200)
#     pointlight.Diffuse = ColorEx(0.8117647, 0.7882353, 0.8705882)
#     pointlight.Specular = ColorEx(0.8431373, 0.9058824, 0.9254902)
#     pointlight.AttenuationRange = 5500
#     # Set up the Gazebo
#     platform = WorldObject.WorldObject(-1, "creation_gazebo_platform", "creation_gazebo.mesh", Vector3(0, 23000, 0), False)
#     # Set up the sky cylinder
#     skycyl = WorldObject.WorldObject(-2, "creation_skycyl", "creation_gazebo_skycyl.mesh", Vector3(0, 23000, 0), False)
#     skycyl_anim = CreateSpinAnimation(skycyl)
#     skycyl_anim.Play(.003, True)
#     # For our startup world, we want to set the camera in a specific spot
#     camera = ClientAPI.GetPlayerCamera()
#     camera.Position = Vector3(0, 24500, 3000)
#     camera.Orientation = Quaternion.FromAngleAxis(-.15, Vector3.UnitX)
#     # Now set up the avatar model
#     avatar = WorldObject.WorldObject(-10, "avatar", "tiny_cube.mesh", Vector3(0, 23000, 0), False)
    camera = ClientAPI.GetPlayerCamera()
    camera.Position = Vector3(124405.9, 22000, -356398.2)
    camera.Orientation = Quaternion(0.5660655, -0.01973991, -0.8236232, -0.02872216)
    ClientAPI.SetSkyBox("eve_skybox")
    ClientAPI.AmbientLight.Color = ColorEx(0.1333333, 0.145098, 0.1921569)
    dirlight = Light.Light("dirlight")
    dirlight.Type = LightType.Directional
    dirlight.Direction = Vector3(-0.01074477, -0.7880108, -0.6155677)
    dirlight.Diffuse = ColorEx(0.254902, 0.2117647, 0.3607843)
    dirlight.Specular = ColorEx(0.7372549, 0.7843137, 0.854902)
    obj0 = WorldObject.WorldObject(ClientAPI.GetLocalOID(), "streetProps", "nyts_props.mesh", Vector3(127070.5, 20005, -320026), False, Quaternion(1, 0, 0, 0), Vector3(1, 1, 1))
    pointlight = Light.Light("TS_44_01")
    pointlight.Type = LightType.Point
    pointlight.Position = Vector3(103198.8, 26651.29, -374254.2)
    pointlight.Specular = ColorEx(0.8392157, 0.8392157, 0.7058824)
    pointlight.Diffuse = ColorEx(0.7607843, 0.7529412, 0.4784314)
    pointlight.AttenuationRange = 15000
    pointlight = Light.Light("TS_44_02")
    pointlight.Type = LightType.Point
    pointlight.Position = Vector3(124852.2, 21651.29, -357154.2)
    pointlight.Specular = ColorEx(0.8392157, 0.8392157, 0.7058824)
    pointlight.Diffuse = ColorEx(0.7607843, 0.7529412, 0.4784314)
    pointlight.AttenuationRange = 15000
    pointlight = Light.Light("TS_44_03")
    pointlight.Type = LightType.Point
    pointlight.Position = Vector3(125782.9, 24651.29, -354154.2)
    pointlight.Specular = ColorEx(0.8392157, 0.8392157, 0.7058824)
    pointlight.Diffuse = ColorEx(0.7607843, 0.7529412, 0.4784314)
    pointlight.AttenuationRange = 15000
    pointlight = Light.Light("TS_44_04")
    pointlight.Type = LightType.Point
    pointlight.Position = Vector3(91640.05, 26651.29, -360475.2)
    pointlight.Specular = ColorEx(0.8392157, 0.8392157, 0.7058824)
    pointlight.Diffuse = ColorEx(0.7607843, 0.7529412, 0.4784314)
    pointlight.AttenuationRange = 15000
    obj1 = WorldObject.WorldObject(ClientAPI.GetLocalOID(), "skylineNear_01", "nyts_skylineNear.mesh", Vector3(225365.1, 20000, -325484.8), False, Quaternion(0.7071068, 0, 0.7071068, 0), Vector3(0.9, 0.9, 0.9))
    obj2 = WorldObject.WorldObject(ClientAPI.GetLocalOID(), "skylineFar_02", "nyts_skylineFar.mesh", Vector3(407511.5, 20000, -309208.5), False, Quaternion(-4.371139E-08, 0, 1, 0), Vector3(1, 1, 1))
    obj3 = WorldObject.WorldObject(ClientAPI.GetLocalOID(), "times square streets", "nyts_streets.mesh", Vector3(127105.6, 20000, -319948.4), False, Quaternion(1, 0, 0, 0), Vector3(1, 1, 1))
    obj4 = WorldObject.WorldObject(ClientAPI.GetLocalOID(), "edelmann", "nyts_edelmann.mesh", Vector3(173786.1, 20091, -325880.3), False, Quaternion(1, 0, 0, 0), Vector3(1, 1, 1))
    obj5 = WorldObject.WorldObject(ClientAPI.GetLocalOID(), "timesSquareTower", "nyts_timesSquareTower.mesh", Vector3(148463.6, 20000, -158562.4), False, Quaternion(1, 0, 0, 0), Vector3(1, 1, 1))
    obj6 = WorldObject.WorldObject(ClientAPI.GetLocalOID(), "streets_2Lane_02", "nyts_streets_2Lane.mesh", Vector3(19492.97, 20080, -445826.3), False, Quaternion(-4.371139E-08, 0, 1, 0), Vector3(1, 1, 1))
    obj7 = WorldObject.WorldObject(ClientAPI.GetLocalOID(), "streets_2Lane_03", "nyts_streets_2Lane.mesh", Vector3(-565.83, 20080, -365486.5), False, Quaternion(-4.371139E-08, 0, 1, 0), Vector3(1, 1, 1))
    obj8 = WorldObject.WorldObject(ClientAPI.GetLocalOID(), "streets_2Lane_05", "nyts_streets_2Lane.mesh", Vector3(254863.8, 20080, -285976.7), False, Quaternion(1, 0, 0, 0), Vector3(1, 1, 1))
    obj9 = WorldObject.WorldObject(ClientAPI.GetLocalOID(), "streets_2Lane_06", "nyts_streets_2Lane.mesh", Vector3(-607.05, 20080, -286301), False, Quaternion(-4.371139E-08, 0, 1, 0), Vector3(1, 1, 1))
    obj10 = WorldObject.WorldObject(ClientAPI.GetLocalOID(), "streets_2Lane_04", "nyts_streets_2Lane.mesh", Vector3(240997.2, 20080, -365483.2), False, Quaternion(1, 0, 0, 0), Vector3(1, 1, 1))
    obj11 = WorldObject.WorldObject(ClientAPI.GetLocalOID(), "avatar", "tiny_cube.mesh", Vector3(127098.7, 20660, -355373.9), False, Quaternion(0.6156615, 0, -0.7880107, 0), Vector3(1, 1, 1))
   

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
if ClientAPI.World.WorldName != "standalone":
    ClientAPI.World.IsWorldLocal = True
