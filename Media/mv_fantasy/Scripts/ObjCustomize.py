import ClientAPI
import MarsCommand
import MarsTarget
import ColoredFurnitureMaterial

subsurface0 = {
    'tile' : 'solid_01',
    'shininess' : 10.0,
    'scale' : 1,
    'col0' : ClientAPI.ColorEx(1.0, 1.0, 0.0, 0.0),
    'col1' : ClientAPI.ColorEx(0.0, 0.0, 1.0, 0.0),
    'col2' : ClientAPI.ColorEx(0.0, 0.0, 0.0, 0.0),
    'col3' : ClientAPI.ColorEx(0.0, 0.0, 0.0, 0.0),
    }

currentObj = None

def SetSubsurfaceProperty(subsurfaceName, propName, propValue):
    global currentObj
    if currentObj == None:
        return
    if not currentObj.PropertyExists(subsurfaceName):
        return
    if currentObj.PropertyExists(subsurfaceName):
        subsurface = currentObj.GetProperty(subsurfaceName)
        subsurface[propName] = propValue
        currentObj.SetProperty(subsurfaceName, subsurface)
        prop = {}
        prop['oid'] = currentObj.OID
        prop['subsurface'] = subsurfaceName
        prop['value'] = subsurface
        # ClientAPI.Network.SendExtensionMessage(0, False, "mv.SET_PROPERTY", prop)

def SetSubsurfaceN(objName, ssNum, textureColorSet):
    worldObj = ClientAPI.World.GetObjectByName(objName)
    subsurfaceName = "subsurface%d" % ssNum
    if worldObj.PropertyExists(subsurfaceName):
        subsurface = worldObj.GetProperty(subsurfaceName)
    else:
        subsurface = {}
        subsurface['tile'] = 'solid_01'
        subsurface['shininess'] = 1.0
        subsurface['scale'] = 1.0
        subsurface['color'] = 0
        subsurface['col0'] = 0.0
        subsurface['col1'] = 0.0
        subsurface['col2'] = 0.0
        subsurface['col3'] = 0.0
    (t, c, (c0, c1, c2, c3)) = textureColorSet
    subsurface['tile'] = t
    subsurface['color'] = c
    subsurface['col0'] = c0
    subsurface['col1'] = c1
    subsurface['col2'] = c2
    subsurface['col3'] = c3
    prop = {}
    prop['oid'] = worldObj.OID
    prop['subsurface'] = subsurfaceName
    prop['value'] = subsurface
    ClientAPI.Network.SendExtensionMessage(0, False, "mv.SET_PROPERTY", prop)
    ColoredFurnitureMaterial.SharedColormap.LoadTexture()

def SetSubsurfaceNProperty(objName, ssNum, propName, propValue):
    worldObj = ClientAPI.World.GetObjectByName(objName)
    subsurfaceName = "subsurface%d" % ssNum
    if worldObj.PropertyExists(subsurfaceName):
        subsurface = worldObj.GetProperty(subsurfaceName)
    else:
        subsurface = {}
        subsurface['tile'] = 'solid_01'
        subsurface['shininess'] = 1.0
        subsurface['scale'] = 1.0
        subsurface['color'] = 0
        subsurface['col0'] = 1.0
        subsurface['col1'] = 1.0
        subsurface['col2'] = 1.0
        subsurface['col3'] = 1.0
    subsurface[propName] = propValue
    prop = {}
    prop['oid'] = worldObj.OID
    prop['subsurface'] = subsurfaceName
    prop['value'] = subsurface
    ClientAPI.Network.SendExtensionMessage(0, False, "mv.SET_PROPERTY", prop)
    ColoredFurnitureMaterial.SharedColormap.LoadTexture()

def SetSubsurfaceNColorN(objName, ssNum, colNum, r, g, b):
    worldObj = ClientAPI.World.GetObjectByName(objName)
    subsurfaceName = "subsurface%d" % ssNum
    if worldObj.PropertyExists(subsurfaceName):
        subsurface = worldObj.GetProperty(subsurfaceName)
    else:
        subsurface = {}
        subsurface['tile'] = 'solid_01'
        subsurface['shininess'] = 1.0
        subsurface['scale'] = 1.0
        subsurface['color'] = 0
        subsurface['col0'] = 0.0
        subsurface['col1'] = 0.0
        subsurface['col2'] = 0.0
        subsurface['col3'] = 0.0
    color = ClientAPI.ColorEx(1.0, r, g, b)
    colName = "col%d" % colNum
    subsurface[colName] = color
    prop = {}
    prop['oid'] = worldObj.OID
    prop['subsurface'] = subsurfaceName
    prop['value'] = subsurface
    ClientAPI.Network.SendExtensionMessage(0, False, "mv.SET_PROPERTY", prop)
    ColoredFurnitureMaterial.SharedColormap.LoadTexture()

def GetSubsurfaceProperty(subsurfaceName, propName):
    global currentObj
    if currentObj == None:
        return None
    if not currentObj.PropertyExists(subsurfaceName):
        return None
    subsurface = currentObj.GetProperty(subsurfaceName)
    return subsurface[propName]

def CustomizeTarget(args):
    global currentObj
    currentObj = MarsTarget.GetCurrentTarget()
    if currentObj != None:
        ClientAPI.Interface.DispatchEvent("CUSTOMIZE_OBJECT",[])

MarsCommand.RegisterCommandHandler("customize", CustomizeTarget)
