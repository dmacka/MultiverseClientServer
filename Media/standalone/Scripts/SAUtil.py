import ClientAPI
import SAWorld
import Region
import SAScene
import SAPlayer
import FastScreenshot

Paths = {}
Regions = {}
MobileObjects = {}

worldState = None
world = None

# Set up the world file, calling methods and using data from the SAWorld module
def SetupWorld():
    global worldState
    global world
    world = SAWorld.WorldHelper(worldState)
    
    BuildPaths(worldState.markers)
    BuildRegions(worldState.regions)
    
# set up the player properties
def SetupPlayer():
    playerObj = ClientAPI.GetPlayerObject()
    if playerObj is None:
        ClientAPI.Log("SetupPlayer() when player is None")
    else:
        ClientAPI.Log("SetupPlayer() called")
        for name, val in SAPlayer.Props:    
            playerObj.SetProperty(name, val)

# this sets the camera indirectly (by setting properties for the player)        
def PositionPlayerFromCamera():
    camera = ClientAPI.GetPlayerCamera()
    cameraPosition = camera.Position
    cameraDirection = camera.Direction
    cameraOrientation = camera.DerivedOrientation
    PositionPlayerFromCameraHelper(cameraPosition, cameraDirection, cameraOrientation)
    
# this sets the camera indirectly (by setting properties for the player)        
def PositionPlayerFromCameraHelper(cameraPosition, cameraDirection, cameraOrientation):
    ClientAPI.Write("cameraPosition = %s; cameraOrientation = %s" % (cameraPosition, cameraOrientation))
    player = ClientAPI.GetPlayerObject()
    # this system is broken - since there is dumb cache code, we need to set it to something wrong first
    player.Direction = ClientAPI.Vector3.UnitZ
    player.Position = cameraPosition
    player.Orientation = cameraOrientation
    player.Direction = ClientAPI.Vector3.Zero
    ClientAPI.Write("player.Position = %s; player.Orientation = %s" % (player.Position, player.Orientation))
    # camera = ClientAPI.GetPlayerCamera()
    # ClientAPI.Write("camera.Position = %s; camera.Orientation = %s" % (camera.Position, camera.Orientation))
    # Set these, so the camera is simpler
    ClientAPI.InputHandler.FollowTerrain = False
    ClientAPI.InputHandler.CameraTargetOffset = ClientAPI.Vector3.Zero
    ClientAPI.InputHandler.CameraDistance = 0

#
# Scan markers for those that have path properties and build paths from them
#
def BuildPaths(markers):
    for loc, orient, props in markers.values():
        if 'Path' in props:
            # extract path properties
            pathName = props['Path']
            pathOffset = int(props['PathOffset'])
            if 'PathTime' in props:
                pathTime = float(props['PathTime'])            
            else:
                pathTime = 0.0
            # if path doesn't exist, create it and add to dictionary
            if pathName not in Paths:
                Paths[pathName] = []
                
            # fetch the path
            path = Paths[pathName]
            
            # expand the list if necessary
            while len(path) <= pathOffset:
                path.append(None)
                
            # add path point info to path
            path[pathOffset] = (pathTime, loc, orient)
    ClientAPI.Log('BuildPaths: ' + str(Paths))

def BuildRegions(regions):
    for regionName in regions.keys():
        points = regions[regionName]
        Regions[regionName] = Region.Region(points)
            
def NodeAnimFromPath(pathName, pathNode):
    # fetch the patch
    path = Paths[pathName]
    
    # fetch pathTime from last path element to get total animation time
    animTime = path[-1][0]
    
    # create the animation and set various modes
    anim = ClientAPI.Animation.Animation(SAWorld.GetUniqueName('nodePathAnim'), animTime)
    anim.Enabled = True
    anim.InterpolationMode = ClientAPI.Animation.InterpolationMode.Linear
    anim.RotationInterpolationMode = ClientAPI.Animation.RotationInterpolationMode.Spherical
    
    # Create the animation track
    track = anim.CreateNodeTrack(pathNode)
    
    # Build the keyframes based on the path values for time, location and orientation
    for pathTime, loc, orient in path:
        keyframe = track.CreateKeyFrame(pathTime)
        keyframe.Translate = loc
        keyframe.Orientation = orient
        
    return anim

def SetCameraAtMarker(markerName):
    loc, orient, props = GetWorldMarker(markerName)
    # Grab the camera and attach it to the camera node.
    # Save the old position and direction so we can restore them later.
    camera = ClientAPI.GetPlayerCamera()
    ClientAPI.GrabPlayerCamera()
    camera.Position = loc
    camera.Orientation = orient

def GetWorldMarker(markerName):
    global worldState
    if worldState.markers.has_key(markerName):
        return worldState.markers[markerName]
    ClientAPI.LogInfo("No match found for world marker: %s" % markerName)
    return (ClientAPI.Vector3.Zero, ClientAPI.Quaternion.Identity, {})

def GetTerrainString():
    global worldState
    if worldState:
        return '%s%s' % (worldState.terrain, worldState.terrainDisplay)
    return ''

# allow the scene to override the screenshot path
if SAScene.ScreenshotPath is not None:
    FastScreenshot.ScreenshotPath = SAScene.ScreenshotPath

# allow the scene to override the image type
if SAScene.machinima.Encode is not None:
    FastScreenshot.ScreenshotExtension = SAScene.machinima.Encode.ImageType

if SAScene.machinima.Render is not None:
    ClientAPI.LogInfo('Got render that is not none: %sx%s' % (SAScene.machinima.Render.Width, SAScene.machinima.Render.Height))
    FastScreenshot.SetTextureResolution(SAScene.machinima.Render.Width, SAScene.machinima.Render.Height)
    if SAScene.machinima.Render.Width > 0 and SAScene.machinima.Render.Height > 0:
        camera = ClientAPI.GetPlayerCamera()
        camera.AspectRatio = float(SAScene.machinima.Render.Width) / SAScene.machinima.Render.Height
        ClientAPI.LogInfo('Aspect ratio = %s' % camera.AspectRatio)
else:
    ClientAPI.LogInfo('Got render that is none')
    
if SAScene.machinima.Name is not None:
    worldFile = '%s.mvw' % SAScene.machinima.Name
    worldState = SAWorld.parseWorld(worldFile)

