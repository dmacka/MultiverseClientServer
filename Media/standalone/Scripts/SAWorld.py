import sys
import xml.dom
import xml.dom.minidom
import ClientAPI

class WorldState:
    """
    This class keeps track of the world state.  It maintains fields based on
    the contents of the xml that is parsed, but does not actually have any
    real game objects.
    """
    def __init__(self):
        # SetupWorld properties
        self.skybox = None
        self.ambientColor = ClientAPI.ColorEx.White
        self.fogNear = 500000.0
        self.fogFar = 1000000.0
        self.fogColor = ClientAPI.ColorEx.White
        
        # SetupCamera properties
        self.cameraPosition = ClientAPI.Vector3.Zero
        self.cameraOrientation = ClientAPI.Quaternion.Identity
        
        # SetupTerrain properties
        self.terrain = None
        self.terrainDisplay = None

        # SetupObjects properties
        self.staticObjects = []
        
        # SetupParticles properties
        self.objectParticles = []
        self.markerParticles = []

        # SetLights properties
        self.dirLightDiffuse = ClientAPI.ColorEx.White
        self.dirLightSpecular = ClientAPI.ColorEx.Black
        self.dirLightDir = ClientAPI.Vector3.UnitX
        self.pointLights = []

        # Markers
        self.markers = {}
        # Regions
        self.regions = {}

    def addStaticObject(self, node):
        name = node.getAttribute('Name')
        mesh = node.getAttribute('Mesh')
    
        pos = parseVector(node.getElementsByTagName('Position')[0])
        scale = parseVector(node.getElementsByTagName('Scale')[0])
        orient = parseQuaternion(node.getElementsByTagName('Orientation')[0])

        # collect object info into a tuple
        oid = ClientAPI.GetLocalOID()
        objInfo = (oid, name, mesh, pos, orient, scale)
    
        # save object info
        self.staticObjects.append(objInfo)
    
        # collect any particle effects that are attached to the object
        for childNode in node.getElementsByTagName('ParticleEffect'):
            self.objectParticles.append((oid,
                                         childNode.getAttribute('ParticleEffectName'),
                                         float(childNode.getAttribute('VelocityScale')),
                                         float(childNode.getAttribute('ParticleScale')),
                                         childNode.getAttribute('AttachmentPoint')))
    def addPointLight(self, node):
        name = node.getAttribute('Name')
        attenuation = (float(node.getAttribute('AttenuationRange')),
                       float(node.getAttribute('AttenuationConstant')),
                       float(node.getAttribute('AttenuationLinear')),
                       float(node.getAttribute('AttenuationQuadratic')))
        
        pos = parseVector(node.getElementsByTagName('Position')[0])
        specular = parseColor(node.getElementsByTagName('Specular')[0])
        diffuse = parseColor(node.getElementsByTagName('Diffuse')[0])
        
        # collect object info into a tuple
        objInfo = (name, pos, specular, diffuse, attenuation)

        # save object info
        self.pointLights.append(objInfo)

    def addMarker(self, node):
        name = node.getAttribute('Name')
    
        pos = parseVector(node.getElementsByTagName('Position')[0])
        orient = parseQuaternion(node.getElementsByTagName('Orientation')[0])
        
        nvpDict = {}
        for childNode in node.getElementsByTagName('NameValuePair'):
            nvpDict[childNode.getAttribute('Name')] = childNode.getAttribute('Value')
    
        # collect marker info into a tuple
        markerInfo = (name, pos, orient, nvpDict)
    
        # save marker info
        self.markers[name] = (pos, orient, nvpDict)
    
        # collect any particle effects that are attached to markers
        for childNode in node.getElementsByTagName('ParticleEffect'):
            self.markerParticles.append((name,
                                    childNode.getAttribute('ParticleEffectName'),
                                    float(childNode.getAttribute('VelocityScale')),
                                    float(childNode.getAttribute('ParticleScale'))))

    def addRegion(self, node):
        name = node.getAttribute('Name')
        points = []
        for pointNode in node.getElementsByTagName('Point'):
            pos = parseVector(pointNode)
            points.append(pos)
        
        self.regions[name] = points

    def addSkybox(self, node):
        self.skybox = node.getAttribute('Name')

    def addGlobalAmbient(self, node):
        self.ambientColor = parseColor(node.getElementsByTagName('Color')[0])

    def addGlobalFog(self, node):
        self.fogNear = float(node.getAttribute('Near'))
        self.fogFar = float(node.getAttribute('Far'))
        self.fogColor = parseColor(node.getElementsByTagName('Color')[0])

    def addGlobalDirectional(self, node):
        self.dirLightDiffuse = parseColor(node.getElementsByTagName('Diffuse')[0])
        self.dirLightSpecular = parseColor(node.getElementsByTagName('Specular')[0])
        self.dirLightDir = parseVector(node.getElementsByTagName('Direction')[0])

    def addCameraPosition(self, node):
        self.cameraPosition = parseVector(node)

    def addCameraOrientation(self, node):
        self.cameraOrientation = parseQuaternion(node)
    
    def addTerrain(self, node):
        xml_str = ''
        for terrainNode in node.childNodes:
            if terrainNode.nodeType == xml.dom.Node.ELEMENT_NODE:
                xml_str = xml_str + '<%s>%s</%s>' % (terrainNode.tagName, terrainNode.firstChild.nodeValue, terrainNode.tagName)
        self.terrain = '<Terrain>' + xml_str + '</Terrain>'
    
    def addTerrainDisplay(self, node):
        xml_str = ''
        for i in range(node.attributes.length):
            attrNode = node.attributes.item(i)
            xml_str = xml_str + '%s=\"%s\" ' % (attrNode.name, attrNode.value)
        self.terrainDisplay = '<TerrainDisplay ' + xml_str + '/>'

class WorldHelper:
    def __init__(self, worldState):
        # Keep track of these so we can clean them up later
        self.StaticObjects = {}
        self.Lights = []
        self.ParticleSystems = []
        self.SceneNodes = []
        if worldState is not None:
            self.Setup(worldState)

    def Reset(self):
        # SetupWorld properties
        self.skybox = None
        self.ambientColor = ClientAPI.ColorEx.White
        self.dirLightDiffuse = ClientAPI.ColorEx.Black
        self.dirLightSpecular = ClientAPI.ColorEx.Black
        self.dirLightDir = ClientAPI.Vector3.UnitX
        self.fogNear = 500000.0
        self.fogFar = 1000000.0
        self.fogColor = ClientAPI.ColorEx.White
        
        # SetupCamera properties
        self.cameraPosition = ClientAPI.Vector3.Zero
        self.cameraOrientation = ClientAPI.Quaternion.Identity
        
        # SetupTerrain properties
        self.terrain = None
        self.terrainDisplay = None

    def Setup(self, worldState):
        self.SetupTerrain(worldState)
        self.SetupWorld(worldState)
        self.SetupObjects(worldState)
        self.SetupLights(worldState)
        self.SetupParticles(worldState)

    def Cleanup(self):
        self.CleanupTerrain()
        self.CleanupWorld()
        self.CleanupObjects()
        self.CleanupLights()
        self.CleanupParticles()
    
    def SetupTerrain(self, worldState):
        TerrainString = "%s%s" % (worldState.terrain, worldState.terrainDisplay)
        
    def SetupWorld(self, worldState):
        # Skybox
        if worldState.skybox is not None:
            ClientAPI.World.SetSkyBox(worldState.skybox)
        else:
            ClientAPI.World.SetSkyBox("Default", False)
        # Global Fog
        ClientAPI.FogConfig.FogColor = worldState.fogColor
        ClientAPI.FogConfig.FogNear = worldState.fogNear
        ClientAPI.FogConfig.FogFar = worldState.fogFar

    def CleanupWorld(self):
        # Skybox
        ClientAPI.World.SetSkyBox(False, "Default")
        # Global Fog
        ClientAPI.FogConfig.FogColor = ClientAPI.ColorEx.White
        ClientAPI.FogConfig.FogNear = 500000.0
        ClientAPI.FogConfig.FogFar = 1000000.0

    def SetupWorldObject(self, objInfo):
        return self.SetupWorldObject(objInfo[0], objInfo[1], objInfo[2], objInfo[3], objInfo[4], objInfo[5])
        
    def SetupWorldObject(self, oid, name, meshName, location, orientation, scale):
        obj = ClientAPI.WorldObject.WorldObject(oid, name, meshName, location, followTerrain=False, orientation=orientation, scale=scale)
        self.StaticObjects[oid] = obj
        return oid
        
    def SetupObjects(self, worldState):
        for objInfo in worldState.staticObjects:
            self.SetupWorldObject(objInfo)

    def CleanupObjects(self):
        for obj in self.StaticObjects.values():
            obj.Dispose()
        self.StaticObjects = {}

    def RemoveWorldObject(self, oid):
        self.StaticObjects[oid].Dispose()
        del self.StaticObjects[oid]

    def SetupParticles(self, worldState):
        #
        # Object Particles
        #
        for oid, particleName, velocityScale, particleScale, attachmentPoint in worldState.objectParticles:
            # get object to which we will attach the particle
            obj = self.StaticObjects[oid]
            
            # set up particle system
            particleSystem = ClientAPI.ParticleSystem.ParticleSystem(GetUniqueName('Particle'), particleName)
            particleSystem.ScaleVelocity(velocityScale)
            particleSystem.DefaultWidth = particleSystem.DefaultWidth * particleScale
            particleSystem.DefaultHeight = particleSystem.DefaultHeight * particleScale
            
            # attach the particle
            obj.AttachObject(attachmentPoint, particleSystem)

            # keep track of this, so we can clean it up later
            self.ParticleSystems.append(particleSystem)

        for markerName, particleName, velocityScale, particleScale in worldState.markerParticles:
            # get marker location and orientation
            loc, orient, props = worldState.markers[markerName]
            # set up scene node
            obj = ClientAPI.SceneNode.SceneNode(GetUniqueName('SceneNode'))
            obj.Parent = ClientAPI.RootSceneNode
            obj.Position = loc
            obj.Orientation = orient
            # keep track of this, so we can clean it up later
            self.SceneNodes.append(obj)
        
            # set up particle system
            particleSystem = ClientAPI.ParticleSystem.ParticleSystem(GetUniqueName('Particle'), particleName)
            particleSystem.ScaleVelocity(velocityScale)
            particleSystem.DefaultWidth = particleSystem.DefaultWidth * particleScale
            particleSystem.DefaultHeight = particleSystem.DefaultHeight * particleScale
        
            # attach the particle
            obj.AttachObject(particleSystem)
            
            # keep track of this, so we can clean it up later
            self.ParticleSystems.append(particleSystem)


    def CleanupParticles(self):
        for obj in self.ParticleSystems:
            obj.Dispose()
        self.ParticleSystems = []
        for obj in self.SceneNodes:
            obj.Dispose()
        self.SceneNodes = []
        
    def SetupLights(self, worldState):
        self.SetupGlobalLights(worldState)
        # Point Lights
        for objInfo in worldState.pointLights:
            self.SetupWorldLight(objInfo)
        
    def SetupGlobalLights(self, worldState):
        # Global Ambient Light
        ClientAPI.AmbientLight.Color = worldState.ambientColor
        # Global Directional Light
        # Right now, the world editor always adds a directional light, but I
        # want to limit the number of lights so I can support more point lights
        # If the color is black, just ignore it.
        black = ClientAPI.ColorEx.Black
        if (worldState.dirLightDiffuse.CompareTo(black) != 0 or worldState.dirLightSpecular.CompareTo(black) != 0):
            obj = ClientAPI.Light.Light("globalDirLight")
            obj.Type = ClientAPI.Light.LightType.Directional
            obj.Direction = worldState.dirLightDir
            obj.Diffuse = worldState.dirLightDiffuse
            obj.Specular = worldState.dirLightSpecular
            ClientAPI.LogInfo("Created global directional light with diffuse component %s" % obj.Diffuse)
            # Track the light for later cleanup
            self.Lights.append(obj)
        else:
            ClientAPI.LogInfo("Excluding global directional light with diffuse component %s" % worldState.dirLightDiffuse)

    def SetupWorldLight(self, objInfo):
        obj = ClientAPI.Light.Light(objInfo[0])
        obj.Position = objInfo[1]
        obj.Specular = objInfo[2]
        obj.Diffuse = objInfo[3]
        obj.AttenuationRange = objInfo[4][0]
        obj.AttenuationConstant = objInfo[4][1]
        obj.AttenuationLinear = objInfo[4][2]
        obj.AttenuationQuadratic = objInfo[4][3]
        self.Lights.append(obj)
        
    def CleanupLights(self):
        ClientAPI.AmbientLight.Color = ClientAPI.ColorEx.White
        for obj in Lights:
            obj.Dispose()
        self.Lights = []

    def SetupCamera(self, worldState):
        # Camera
        camera = ClientAPI.GetPlayerCamera()
        camera.Position = worldState.cameraPosition
        camera.Orientation = worldState.cameraOrientation


uniqueID = 0

# some helper methods
def parseVector(node):
    return ClientAPI.Vector3(float(node.getAttribute('x')), float(node.getAttribute('y')), float(node.getAttribute('z')))

def parseQuaternion(node):
    return ClientAPI.Quaternion(float(node.getAttribute('w')), float(node.getAttribute('x')), float(node.getAttribute('y')), float(node.getAttribute('z')))

def parseColor(node):
    return ClientAPI.ColorEx(float(node.getAttribute('R')), float(node.getAttribute('G')), float(node.getAttribute('B')))

def GetUniqueID():
    global uniqueID
    ret = uniqueID
    uniqueID = uniqueID + 1
    return ret
    
def GetUniqueName(system):
    return 'SAWorld%s%d' % (system, GetUniqueID())

def parseWorld(worldFile):
    worldState = WorldState()
    ClientAPI.LogInfo("Loading world file %s" % worldFile)
    worldFile = ClientAPI.GetAssetPath(worldFile)
    ClientAPI.LogInfo("Loading world file %s" % worldFile)
    worldXml = open(worldFile).read()
    worldDom = xml.dom.minidom.parseString(worldXml)
    collectionFiles = []
    for node in worldDom.documentElement.childNodes:
        if node.nodeType == xml.dom.Node.ELEMENT_NODE:
            if node.tagName == 'GlobalFog':
                worldState.addGlobalFog(node)
            elif node.tagName == 'GlobalAmbientLight':
                worldState.addGlobalAmbient(node)
            elif node.tagName == 'GlobalDirectionalLight':
                worldState.addGlobalDirectional(node)
            elif node.tagName == 'Skybox':
                worldState.addSkybox(node)
            elif node.tagName == 'CameraPosition':
                worldState.addCameraPosition(node)
            elif node.tagName == 'CameraOrientation':
                worldState.addCameraOrientation(node)
            elif node.tagName == 'Terrain':
                worldState.addTerrain(node)
            elif node.tagName == 'TerrainDisplay':
                worldState.addTerrainDisplay(node)
            elif node.tagName == 'WorldCollection':
                collectionFiles.append(node.getAttribute('Filename'))
            else:
                pass
                # print "Error parsing top level world tag: %s" % node.tagName

    for collectionFile in collectionFiles:
        collectionFile = ClientAPI.GetAssetPath(collectionFile)
        collectionXml = open(collectionFile).read()
        collectionDom = xml.dom.minidom.parseString(collectionXml)
        for node in collectionDom.documentElement.childNodes:
            if node.nodeType == xml.dom.Node.ELEMENT_NODE:
                if node.tagName == 'StaticObject':
                    worldState.addStaticObject(node)
                if node.tagName == 'PointLight':
                    worldState.addPointLight(node)
                elif node.tagName == 'Waypoint':
                    worldState.addMarker(node)
                elif node.tagName == 'Boundary':
                    worldState.addRegion(node)

    return worldState
