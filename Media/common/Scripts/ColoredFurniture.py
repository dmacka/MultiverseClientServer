import ClientAPI
import ColoredFurnitureMaterial

# these need to be initialized with the tile map and texture
# name for the current world
AtlasTexture = None
TileMap = None

# clean up
def disposeHandler(worldObj):
    coloredObj = worldObj.GetProperty('__coloredObj')
    coloredObj.Dispose()

def _update(worldObj, coloredObj, ssNum):
    propName = 'subsurface%d' % ssNum
    if worldObj.PropertyExists(propName):
        # get the property map for this subsurface
        ssProp = worldObj.GetProperty(propName)
            
        # get the subsurface object
        subsurface = coloredObj.Subsurfaces[ssNum]
            
        # set the properties on the subsurface object
        subsurface.TileName = ssProp['tile']
        subsurface.Shininess = ssProp['shininess']
        subsurface.Scale = ssProp['scale']
        if ssProp['col0'] is not None:
            subsurface.SetColorAndSpecular(0, ssProp['col0'], False)
        if ssProp['col1'] is not None:
            subsurface.SetColorAndSpecular(1, ssProp['col1'], False)
        if ssProp['col2'] is not None:
            subsurface.SetColorAndSpecular(2, ssProp['col2'], False)
        if ssProp['col3'] is not None:
            subsurface.SetColorAndSpecular(3, ssProp['col3'], False)

def Update(worldObj, ssNum):
    coloredObj = worldObj.GetProperty('__coloredObj')
    
    _update(worldObj, coloredObj, ssNum)
    
    # now that the colors are set, update the colormap texture
    ColoredFurnitureMaterial.SharedColormap.LoadTexture()

def UpdateAll(worldObj):
    coloredObj = worldObj.GetProperty('__coloredObj')
    
    for i in range(0, 8):
        _update(worldObj, coloredObj, i)

    # now that the colors are set, update the colormap texture
    ColoredFurnitureMaterial.SharedColormap.LoadTexture()

def propertyChangeHandler(worldObj, propName):
    if propName.startswith('subsurface'):
        # grab the last digit of the property name and convert it to int
        #  which is the subsurface number
        Update(worldObj, int(propName[-1]))
    elif propName == 'brighten':
        coloredObj = worldObj.GetProperty('__coloredObj')
        value = worldObj.GetProperty(propName)
        coloredObj.Brighten(float(value))

appearanceOverrideList = []

def appearanceOverrideHandler(sender, args):
    propName = args.PropName
    worldObj = ClientAPI.World.GetObjectByOID(args.Oid)
    overrideProp = worldObj.GetProperty("AppearanceOverride")
    global appearanceOverrideList
    if (overrideProp == "coloredfurniture") and not (worldObj in appearanceOverrideList):
        appearanceOverrideList.append(worldObj)

        # get the ambient occlusion map name
        if ( worldObj.PropertyExists('AOMap') ):
            aoMap = worldObj.GetProperty('AOMap')
        else:
            aoMap = 'White.dds'
        if aoMap == '':
            aoMap = 'White.dds'
        # create the colored object material state
        coloredObj = ColoredFurnitureMaterial.ColoredObject(worldObj, AtlasTexture, TileMap, aoMap)
        
        # save the colored object as a property on the worldObj
        worldObj.SetProperty('__coloredObj', coloredObj)
        
        # hook event handlers
        worldObj.RegisterEventHandler("Disposed", disposeHandler)
        worldObj.RegisterEventHandler("PropertyChange", propertyChangeHandler)
        
        # update the object with the data from its properties
        UpdateAll(worldObj)
        
ClientAPI.World.RegisterObjectPropertyChangeHandler("AppearanceOverride", appearanceOverrideHandler)


