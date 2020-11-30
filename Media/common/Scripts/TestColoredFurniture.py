import ClientAPI
import MarsCommand
import HTMLColors
import MarsTarget

solidProps = {
    'subsurface0' : {
        'tile' : 'solid_01',
        'shininess' : 10.0,
        'scale' : 1,
        'col0' : ClientAPI.ColorEx(1.0, 1.0, 0.0, 0.0),
        'col1' : ClientAPI.ColorEx(1.0, 0.0, 0.0, 0.0),
        'col2' : ClientAPI.ColorEx(1.0, 0.0, 0.0, 0.0),
        'col3' : ClientAPI.ColorEx(1.0, 0.0, 0.0, 0.0),
    },
    'subsurface1' : {
        'tile' : 'solid_01',
        'shininess' : 10.0,
        'scale' : 1,
        'col0' : ClientAPI.ColorEx(1.0, 0.0, 1.0, 0.0),
        'col1' : ClientAPI.ColorEx(1.0, 0.0, 0.0, 0.0),
        'col2' : ClientAPI.ColorEx(1.0, 0.0, 0.0, 0.0),
        'col3' : ClientAPI.ColorEx(1.0, 0.0, 0.0, 0.0),
    },
    'subsurface2' : {
        'tile' : 'solid_01',
        'shininess' : 10.0,
        'scale' : 1,
        'col0' : ClientAPI.ColorEx(1.0, 0.0, 0.0, 1.0),
        'col1' : ClientAPI.ColorEx(1.0, 0.0, 0.0, 0.0),
        'col2' : ClientAPI.ColorEx(1.0, 0.0, 0.0, 0.0),
        'col3' : ClientAPI.ColorEx(1.0, 0.0, 0.0, 0.0),
    },
    'subsurface3' : {
        'tile' : 'solid_01',
        'shininess' : 10.0,
        'scale' : 1,
        'col0' : ClientAPI.ColorEx(1.0, 1.0, 1.0, 0.0),
        'col1' : ClientAPI.ColorEx(1.0, 0.0, 0.0, 0.0),
        'col2' : ClientAPI.ColorEx(1.0, 0.0, 0.0, 0.0),
        'col3' : ClientAPI.ColorEx(1.0, 0.0, 0.0, 0.0),
    },    
    'subsurface4' : {
        'tile' : 'solid_01',
        'shininess' : 10.0,
        'scale' : 1,
        'col0' : ClientAPI.ColorEx(1.0, 1.0, 0.0, 1.0),
        'col1' : ClientAPI.ColorEx(1.0, 0.0, 0.0, 0.0),
        'col2' : ClientAPI.ColorEx(1.0, 0.0, 0.0, 0.0),
        'col3' : ClientAPI.ColorEx(1.0, 0.0, 0.0, 0.0),
    },
    'subsurface5' : {
        'tile' : 'solid_01',
        'shininess' : 10.0,
        'scale' : 1,
        'col0' : ClientAPI.ColorEx(1.0, 0.0, 1.0, 1.0),
        'col1' : ClientAPI.ColorEx(1.0, 0.0, 0.0, 0.0),
        'col2' : ClientAPI.ColorEx(1.0, 0.0, 0.0, 0.0),
        'col3' : ClientAPI.ColorEx(1.0, 0.0, 0.0, 0.0),
    },
    'subsurface6' : {
        'tile' : 'solid_01',
        'shininess' : 10.0,
        'scale' : 1,
        'col0' : ClientAPI.ColorEx(1.0, 1.0, 1.0, 1.0),
        'col1' : ClientAPI.ColorEx(1.0, 0.0, 0.0, 0.0),
        'col2' : ClientAPI.ColorEx(1.0, 0.0, 0.0, 0.0),
        'col3' : ClientAPI.ColorEx(1.0, 0.0, 0.0, 0.0),
    },
    'subsurface7' : {
        'tile' : 'solid_01',
        'shininess' : 10.0,
        'scale' : 1,
        'col0' : ClientAPI.ColorEx(1.0, 0.0, 0.0, 0.0),
        'col1' : ClientAPI.ColorEx(1.0, 1.0, 1.0, 1.0),
        'col2' : ClientAPI.ColorEx(1.0, 0.0, 0.0, 0.0),
        'col3' : ClientAPI.ColorEx(1.0, 0.0, 0.0, 0.0),
    },
}

cuteProps = {
    'subsurface0' : {
        'tile' : 'medium-vstripes',
        'shininess' : 10.0,
        'scale' : 1.5,
        'col0' : ClientAPI.ColorEx(1.0, 137/255.0, 62/255.0, 93/255.0),
        'col1' : ClientAPI.ColorEx(1.0, 153/255.0, 65/255.0, 99/255.0),
        'col2' : ClientAPI.ColorEx(0.0, 0.0, 0.0, 0.0),
        'col3' : ClientAPI.ColorEx(0.0, 0.0, 0.0, 0.0),
    },
    'subsurface1' : {
        'tile' : 'small-dots',
        'shininess' : 10.0,
        'scale' : 1,
        'col0' : ClientAPI.ColorEx(1.0, 244/255.0, 218/255.0, 231/255.0),
        'col1' : ClientAPI.ColorEx(1.0, 222/255.0, 154/255.0, 189/255.0),
        'col2' : ClientAPI.ColorEx(0.0, 0.0, 0.0, 0.0),
        'col3' : ClientAPI.ColorEx(0.0, 0.0, 0.0, 0.0),
    },
    'subsurface2' : {
        'tile' : 'large-dots',
        'shininess' : 10.0,
        'scale' : 2.5,
        'col0' : ClientAPI.ColorEx(1.0, 99/255.0, 47/255.0, 90/255.0),
        'col1' : ClientAPI.ColorEx(1.0, 120/255.0, 66/255.0, 112/255.0),
        'col2' : ClientAPI.ColorEx(0.0, 0.0, 0.0, 0.0),
        'col3' : ClientAPI.ColorEx(0.0, 0.0, 0.0, 0.0),
    },
    'subsurface3' : {
        'tile' : 'solid_01',
        'shininess' : 10.0,
        'scale' : 1,
        'col0' : ClientAPI.ColorEx(1.0, 1.0, 1.0, 0.0),
        'col1' : ClientAPI.ColorEx(1.0, 1.0, 1.0, 0.0),
        'col2' : ClientAPI.ColorEx(0.0, 0.0, 0.0, 0.0),
        'col3' : ClientAPI.ColorEx(0.0, 0.0, 0.0, 0.0),
    },    
    'subsurface4' : {
        'tile' : 'solid_01',
        'shininess' : 10.0,
        'scale' : 1,
        'col0' : ClientAPI.ColorEx(1.0, 1.0, 0.0, 1.0),
        'col1' : ClientAPI.ColorEx(0.0, 0.0, 0.0, 0.0),
        'col2' : ClientAPI.ColorEx(0.0, 0.0, 0.0, 0.0),
        'col3' : ClientAPI.ColorEx(0.0, 0.0, 0.0, 0.0),
    },
    'subsurface5' : {
        'tile' : 'small-dots',
        'shininess' : 10.0,
        'scale' : 1,
        'col0' : ClientAPI.ColorEx(1.0, 244/255.0, 218/255.0, 231/255.0),
        'col1' : ClientAPI.ColorEx(1.0, 222/255.0, 154/255.0, 189/255.0),
        'col2' : ClientAPI.ColorEx(0.0, 0.0, 0.0, 0.0),
        'col3' : ClientAPI.ColorEx(0.0, 0.0, 0.0, 0.0),
    },
    'subsurface6' : {
        'tile' : 'small-dots',
        'shininess' : 10.0,
        'scale' : 1,
        'col0' : ClientAPI.ColorEx(1.0, 244/255.0, 218/255.0, 231/255.0),
        'col1' : ClientAPI.ColorEx(1.0, 222/255.0, 154/255.0, 189/255.0),
        'col2' : ClientAPI.ColorEx(0.0, 0.0, 0.0, 0.0),
        'col3' : ClientAPI.ColorEx(0.0, 0.0, 0.0, 0.0),
    },
    'subsurface7' : {
        'tile' : 'medium-vstripes',
        'shininess' : 10.0,
        'scale' : 1.5,
        'col0' : ClientAPI.ColorEx(1.0, 137/255.0, 62/255.0, 93/255.0),
        'col1' : ClientAPI.ColorEx(1.0, 153/255.0, 65/255.0, 99/255.0),
        'col2' : ClientAPI.ColorEx(0.0, 0.0, 0.0, 0.0),
        'col3' : ClientAPI.ColorEx(0.0, 0.0, 0.0, 0.0),
    },
}

def CopyProp(propDict):
    destDict = {}
    destDict['tile'] = propDict['tile']
    destDict['shininess'] = propDict['shininess']
    destDict['scale'] = propDict['scale']
    color = propDict['col0']
    destDict['col0'] = ClientAPI.ColorEx(color.a, color.r, color.g, color.b)
    color = propDict['col1']
    destDict['col1'] = ClientAPI.ColorEx(color.a, color.r, color.g, color.b)
    color = propDict['col2']
    destDict['col2'] = ClientAPI.ColorEx(color.a, color.r, color.g, color.b)
    color = propDict['col3']
    destDict['col3'] = ClientAPI.ColorEx(color.a, color.r, color.g, color.b)
    return destDict

def DumpSubsurface(worldObj, ssNum, indent):
    propName = 'subsurface%d' % ssNum
    if worldObj.PropertyExists(propName):
        ssProp = worldObj.GetProperty(propName)
        subin = '  ' + indent
        c0 = ssProp['col0']
        c1 = ssProp['col1']
        c2 = ssProp['col2']
        c3 = ssProp['col3']
        ret = '%s\"%s\" : {\n' % (indent, propName) + \
            '%s\"tile\" : \"%s\",\n' % (subin, ssProp['tile']) + \
            '%s\"shininess\" : %f,\n' % (subin, ssProp['shininess']) +\
            '%s\"scale\" : %f,\n' % (subin, ssProp['scale']) + \
            '%s\"col0\" : ClientAPI.ColorEx(%f, %f, %f, %f),\n' % (subin, c0.a, c0.r, c0.g, c0.b) + \
            '%s\"col1\" : ClientAPI.ColorEx(%f, %f, %f, %f),\n' % (subin, c1.a, c1.r, c1.g, c1.b) + \
            '%s\"col2\" : ClientAPI.ColorEx(%f, %f, %f, %f),\n' % (subin, c2.a, c2.r, c2.g, c2.b) + \
            '%s\"col3\" : ClientAPI.ColorEx(%f, %f, %f, %f),\n' % (subin, c3.a, c3.r, c3.g, c3.b) + \
            '%s},\n' % (indent)
    else:
        ret = ""
    return ret

def DumpColorizeProps(worldObj, schemeName):
    logstr = '\n### BEGIN FURNITURE SCHEME ###\n'
    logstr = logstr + '%s = {\n' % schemeName
    for i in range(0, 8):
        logstr = logstr + DumpSubsurface(worldObj, i, '  ')
    logstr = logstr + '}\n'
    logstr = logstr + '### END FURNITURE SCHEME ###\n'
    ClientAPI.Log(logstr)
    
def TestSolid(args):
    playerPos = ClientAPI.GetPlayerObject().Position
    furnPos = ClientAPI.Vector3(playerPos.x, playerPos.y, playerPos.z + 2000)
    testObj = ClientAPI.WorldObject.WorldObject(ClientAPI.GetLocalOID(), 'furn1', 'FRW_furn_cute_bed.mesh', furnPos, False, ClientAPI.GetPlayerObject().Orientation)
    testObj.Targetable = True
    
    for propName in solidProps.keys():
        testObj.SetProperty(propName, CopyProp(solidProps[propName]))
        
    testObj.SetProperty('AppearanceOverride', 'coloredfurniture')

furnitureAliases = {
    'cute_bed' : 'FRW_furn_cute_bed.mesh',
}

#
# spawn the named model in the scene, and load it up with the solid color
#  properties.
#
def SpawnFurn(arg):
    # create a unique name for the object
    objName = 'furn-' + str(ClientAPI.GetLocalOID())
    
    if arg in furnitureAliases:
        meshName = furnitureAliases[arg]
    else:
        meshName = arg
    playerPos = ClientAPI.GetPlayerObject().Position
    furnPos = ClientAPI.Vector3(playerPos.x, playerPos.y, playerPos.z + 2000)
    testObj = ClientAPI.WorldObject.WorldObject(ClientAPI.GetLocalOID(), objName, meshName, furnPos, False, ClientAPI.GetPlayerObject().Orientation)
    testObj.Targetable = True
    
    for propName in solidProps.keys():
        testObj.SetProperty(propName, CopyProp(solidProps[propName]))
        
    testObj.SetProperty('AppearanceOverride', 'coloredfurniture')
    ClientAPI.DebugWrite("SpawnFurn: %s" % objName)
    
def TestCute(args):
    playerPos = ClientAPI.GetPlayerObject().Position
    furnPos = ClientAPI.Vector3(playerPos.x, playerPos.y, playerPos.z + 2000)
    testObj = ClientAPI.WorldObject.WorldObject(ClientAPI.GetLocalOID(), 'furn2', 'FRW_furn_cute_bed.mesh', furnPos, False, ClientAPI.GetPlayerObject().Orientation)
    testObj.Targetable = True
    
    for propName in cuteProps.keys():
        testObj.SetProperty(propName, CopyProp(cuteProps[propName]))
        
    testObj.SetProperty('AppearanceOverride', 'coloredfurniture')
    
def TestOrig(args):
    global testObj
    playerPos = ClientAPI.GetPlayerObject().Position
    furnPos = ClientAPI.Vector3(playerPos.x, playerPos.y, playerPos.z + 2000)
    testObj = ClientAPI.WorldObject.WorldObject(ClientAPI.GetLocalOID(), 'furn3', 'FRW_furn_cute_bed_orig.mesh', furnPos, False, ClientAPI.GetPlayerObject().Orientation)
    
   
def SetPattern(args):
    testObj = MarsTarget.GetCurrentTarget()
    argList = args.split()
    propName = 'subsurface' + argList[0]
    tileName = argList[1]
    prop = testObj.GetProperty(propName)
    prop['tile'] = tileName
    testObj.SetProperty(propName, prop)

def SetShin(args):
    testObj = MarsTarget.GetCurrentTarget()
    argList = args.split()
    propName = 'subsurface' + argList[0]
    val = float(argList[1])
    prop = testObj.GetProperty(propName)
    prop['shininess'] = val
    testObj.SetProperty(propName, prop)
    
def SetScale(args):
    testObj = MarsTarget.GetCurrentTarget()
    argList = args.split()
    propName = 'subsurface' + argList[0]
    val = float(argList[1])
    prop = testObj.GetProperty(propName)
    prop['scale'] = val
    testObj.SetProperty(propName, prop)

def SetColor(args):
    testObj = MarsTarget.GetCurrentTarget()
    argList = args.split()
    propName = 'subsurface' + argList[0]
    colorNum = 'col' + argList[1]
    
    if len(argList) == 5:
        val = ClientAPI.ColorEx(float(argList[2])/255.0, float(argList[3])/255.0, float(argList[4])/255.0)
    else:
        colorName = argList[2].lower()
        if colorName in HTMLColors.NamedColors:
            val = HTMLColors.NamedColors[colorName]
        else:
            val = ClientAPI.ColorEx.White
    
    prop = testObj.GetProperty(propName)
    prop[colorNum] = val
    testObj.SetProperty(propName, prop)

def DumpScheme(args):
    testObj = MarsTarget.GetCurrentTarget()
    DumpColorizeProps(testObj, args)    

MarsCommand.RegisterCommandHandler("dumpscheme", DumpScheme)
MarsCommand.RegisterCommandHandler("spawnfurn", SpawnFurn)
MarsCommand.RegisterCommandHandler("solidbed", TestSolid)
MarsCommand.RegisterCommandHandler("cutebed", TestCute)
MarsCommand.RegisterCommandHandler("origbed", TestOrig)
MarsCommand.RegisterCommandHandler("sspat", SetPattern)
MarsCommand.RegisterCommandHandler("ssshin", SetShin)
MarsCommand.RegisterCommandHandler("ssscale", SetScale)
MarsCommand.RegisterCommandHandler("sscolor", SetColor)
