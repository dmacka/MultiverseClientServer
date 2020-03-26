import ClientAPI
import MarsCommand

NamedColors = {}

NamedColorsOrig = {
    'AliceBlue': ClientAPI.ColorEx.AliceBlue,
    'AntiqueWhite': ClientAPI.ColorEx.AntiqueWhite,
    'Aqua': ClientAPI.ColorEx.Aqua,
    'Aquamarine': ClientAPI.ColorEx.Aquamarine,
    'Azure': ClientAPI.ColorEx.Azure,
    'Beige': ClientAPI.ColorEx.Beige,
    'Bisque': ClientAPI.ColorEx.Bisque,
    'Black': ClientAPI.ColorEx.Black,
    'BlanchedAlmond': ClientAPI.ColorEx.BlanchedAlmond,
    'Blue': ClientAPI.ColorEx.Blue,
    'BlueViolet': ClientAPI.ColorEx.BlueViolet,
    'Brown': ClientAPI.ColorEx.Brown,
    'BurlyWood': ClientAPI.ColorEx.BurlyWood,
    'CadetBlue': ClientAPI.ColorEx.CadetBlue,
    'Chartreuse': ClientAPI.ColorEx.Chartreuse,
    'Chocolate': ClientAPI.ColorEx.Chocolate,
    'Coral': ClientAPI.ColorEx.Coral,
    'CornflowerBlue': ClientAPI.ColorEx.CornflowerBlue,
    'Cornsilk': ClientAPI.ColorEx.Cornsilk,
    'Crimson': ClientAPI.ColorEx.Crimson,
    'Cyan': ClientAPI.ColorEx.Cyan,
    'DarkBlue': ClientAPI.ColorEx.DarkBlue,
    'DarkCyan': ClientAPI.ColorEx.DarkCyan,
    'DarkGoldenrod': ClientAPI.ColorEx.DarkGoldenrod,
    'DarkGray': ClientAPI.ColorEx.DarkGray,
    'DarkGreen': ClientAPI.ColorEx.DarkGreen,    
    'DarkKhaki': ClientAPI.ColorEx.DarkKhaki,
    'DarkMagenta': ClientAPI.ColorEx.DarkMagenta,
    'DarkOliveGreen': ClientAPI.ColorEx.DarkOliveGreen,
    'DarkOrange': ClientAPI.ColorEx.DarkOrange,
    'DarkOrchid': ClientAPI.ColorEx.DarkOrchid,
    'DarkRed': ClientAPI.ColorEx.DarkRed,
    'DarkSalmon': ClientAPI.ColorEx.DarkSalmon,
    'DarkSeaGreen': ClientAPI.ColorEx.DarkSeaGreen,
    'DarkSlateBlue': ClientAPI.ColorEx.DarkSlateBlue,
    'DarkSlateGray': ClientAPI.ColorEx.DarkSlateGray,
    'DarkTurquoise': ClientAPI.ColorEx.DarkTurquoise,
    'DarkViolet': ClientAPI.ColorEx.DarkViolet,
    'DeepPink': ClientAPI.ColorEx.DeepPink,    
    'DeepSkyBlue': ClientAPI.ColorEx.DeepSkyBlue,
    'DimGray': ClientAPI.ColorEx.DimGray,
    'DodgerBlue': ClientAPI.ColorEx.DodgerBlue,
    'Firebrick': ClientAPI.ColorEx.Firebrick,
    'FloralWhite': ClientAPI.ColorEx.FloralWhite,
    'ForestGreen': ClientAPI.ColorEx.ForestGreen,
    'Fuchsia': ClientAPI.ColorEx.Fuchsia,
    'Gainsboro': ClientAPI.ColorEx.Gainsboro,
    'GhostWhite': ClientAPI.ColorEx.GhostWhite,
    'Gold': ClientAPI.ColorEx.Gold,
    'Goldenrod': ClientAPI.ColorEx.Goldenrod,
    'Gray': ClientAPI.ColorEx.Gray,
    'Green': ClientAPI.ColorEx.Green,
    'GreenYellow': ClientAPI.ColorEx.GreenYellow,
    'Honeydew': ClientAPI.ColorEx.Honeydew,  
    'HotPink': ClientAPI.ColorEx.HotPink,
    'IndianRed': ClientAPI.ColorEx.IndianRed,
    'Indigo': ClientAPI.ColorEx.Indigo,
    'Ivory': ClientAPI.ColorEx.Ivory,
    'Khaki': ClientAPI.ColorEx.Khaki,
    'Lavender': ClientAPI.ColorEx.Lavender,
    'LavenderBlush': ClientAPI.ColorEx.LavenderBlush,
    'LawnGreen': ClientAPI.ColorEx.LawnGreen,
    'LemonChiffon': ClientAPI.ColorEx.LemonChiffon,
    'LightBlue': ClientAPI.ColorEx.LightBlue,
    'LightCoral': ClientAPI.ColorEx.LightCoral,
    'LightCyan': ClientAPI.ColorEx.LightCyan,
    'LightGoldenrodYellow': ClientAPI.ColorEx.LightGoldenrodYellow,
    'LightGreen': ClientAPI.ColorEx.LightGreen,
    'LightGray': ClientAPI.ColorEx.LightGray,
    'LightPink': ClientAPI.ColorEx.LightPink,
    'LightSalmon': ClientAPI.ColorEx.LightSalmon,
    'LightSeaGreen': ClientAPI.ColorEx.LightSeaGreen,
    'LightSkyBlue': ClientAPI.ColorEx.LightSkyBlue,
    'LightSlateGray': ClientAPI.ColorEx.LightSlateGray,
    'LightSteelBlue': ClientAPI.ColorEx.LightSteelBlue,
    'LightYellow': ClientAPI.ColorEx.LightYellow,
    'Lime': ClientAPI.ColorEx.Lime,
    'LimeGreen': ClientAPI.ColorEx.LimeGreen,
    'Linen': ClientAPI.ColorEx.Linen,
    'Magenta': ClientAPI.ColorEx.Magenta,
    'Maroon': ClientAPI.ColorEx.Maroon,
    'MediumAquamarine': ClientAPI.ColorEx.MediumAquamarine,
    'MediumBlue': ClientAPI.ColorEx.MediumBlue,
    'MediumOrchid': ClientAPI.ColorEx.MediumOrchid,
    'MediumPurple': ClientAPI.ColorEx.MediumPurple,
    'MediumSeaGreen': ClientAPI.ColorEx.MediumSeaGreen,
    'MediumSlateBlue': ClientAPI.ColorEx.MediumSlateBlue,
    'MediumSpringGreen': ClientAPI.ColorEx.MediumSpringGreen,
    'MediumTurquoise': ClientAPI.ColorEx.MediumTurquoise,
    'MediumVioletRed': ClientAPI.ColorEx.MediumVioletRed,
    'MidnightBlue': ClientAPI.ColorEx.MidnightBlue,
    'MistyRose': ClientAPI.ColorEx.MistyRose,
    'Moccasin': ClientAPI.ColorEx.Moccasin,
    'NavajoWhite': ClientAPI.ColorEx.NavajoWhite,
    'Navy': ClientAPI.ColorEx.Navy,
    'OldLace': ClientAPI.ColorEx.OldLace,
    'Olive': ClientAPI.ColorEx.Olive,
    'OliveDrab': ClientAPI.ColorEx.OliveDrab,
    'Orange': ClientAPI.ColorEx.Orange,
    'OrangeRed': ClientAPI.ColorEx.OrangeRed,
    'Orchid': ClientAPI.ColorEx.Orchid,
    'PaleGoldenrod': ClientAPI.ColorEx.PaleGoldenrod,
    'PaleGreen': ClientAPI.ColorEx.PaleGreen,
    'PaleTurquoise': ClientAPI.ColorEx.PaleTurquoise,
    'PaleVioletRed': ClientAPI.ColorEx.PaleVioletRed,
    'PapayaWhip': ClientAPI.ColorEx.PapayaWhip,
    'PeachPuff': ClientAPI.ColorEx.PeachPuff,
    'Peru': ClientAPI.ColorEx.Peru,
    'Pink': ClientAPI.ColorEx.Pink,
    'Plum': ClientAPI.ColorEx.Plum,
    'PowderBlue': ClientAPI.ColorEx.PowderBlue,
    'Purple': ClientAPI.ColorEx.Purple,
    'Red': ClientAPI.ColorEx.Red,
    'RosyBrown': ClientAPI.ColorEx.RosyBrown,
    'RoyalBlue': ClientAPI.ColorEx.RoyalBlue,
    'SaddleBrown': ClientAPI.ColorEx.SaddleBrown,
    'Salmon': ClientAPI.ColorEx.Salmon,
    'SandyBrown': ClientAPI.ColorEx.SandyBrown,
    'SeaGreen': ClientAPI.ColorEx.SeaGreen,
    'SeaShell': ClientAPI.ColorEx.SeaShell,
    'Sienna': ClientAPI.ColorEx.Sienna,
    'Silver': ClientAPI.ColorEx.Silver,
    'SkyBlue': ClientAPI.ColorEx.SkyBlue,
    'SlateBlue': ClientAPI.ColorEx.SlateBlue,
    'SlateGray': ClientAPI.ColorEx.SlateGray,
    'Snow': ClientAPI.ColorEx.Snow,
    'SpringGreen': ClientAPI.ColorEx.SpringGreen,
    'SteelBlue': ClientAPI.ColorEx.SteelBlue,
    'Tan': ClientAPI.ColorEx.Tan,
    'Teal': ClientAPI.ColorEx.Teal,
    'Thistle': ClientAPI.ColorEx.Thistle,
    'Tomato': ClientAPI.ColorEx.Tomato,
    'Turquoise': ClientAPI.ColorEx.Turquoise,
    'Violet': ClientAPI.ColorEx.Violet,
    'Wheat': ClientAPI.ColorEx.Wheat,
    'White': ClientAPI.ColorEx.White,
    'WhiteSmoke': ClientAPI.ColorEx.WhiteSmoke,
    'Yellow': ClientAPI.ColorEx.Yellow,
    'YellowGreen': ClientAPI.ColorEx.YellowGreen,
}

def DumpColorNames(args=""):
    colorStr = ""
    for colorName in NamedColors.keys():
        colorStr = colorStr + '%s, ' % colorName
    ClientAPI.Write(colorStr)
    
def ColorValue(args):
    ClientAPI.Write(NamedColors[args.lower()].ToString())
 
couchObj = None
   
def SpawnCouch(args):
    global couchObj
    playerPos = ClientAPI.GetPlayerObject().Position
    couchPos = ClientAPI.Vector3(playerPos.x, playerPos.y, playerPos.z + 2000)
    couchObj = ClientAPI.WorldObject.WorldObject(ClientAPI.GetLocalOID(), 'couch', 'FRW_furn_hiphop_loveseat.mesh', couchPos, False, ClientAPI.GetPlayerObject().Orientation)
    
def CouchColor(args):
    global couchObj
    
    # spawn the couch if it doesnt exist
    if couchObj is None:
        SpawnCouch('')
    
    if args.lower() in NamedColors:
        # extract color from the arg string
        color = NamedColors[args.lower()]
    else:
        argList = args.split()
        if len(argList) == 3:
            r = int(argList[0])
            g = int(argList[1])
            b = int(argList[2])
            color = ClientAPI.ColorEx(r/255.0, g/255.0, b/255.0)
            ClientAPI.Write('Setting color to: ' + color.ToString())
        else:
            ClientAPI.Write('Color not found')
            return
    
    # get the material from the couch object
    materialName = couchObj.Model.GetSubMeshMaterial(couchObj.Model.SubMeshNames[0])
    material = ClientAPI.GetMaterial(materialName)
    tech = material.GetTechnique('Fixed')
    if tech.IsSupported:
        matpass = tech.GetPass('Single')
        tu = matpass.GetTextureUnit('Color')
        tu.SetColorOperationEx(ClientAPI.LayerBlendOperationEx.Modulate, ClientAPI.LayerBlendSource.Diffuse, ClientAPI.LayerBlendSource.Manual, color, color)
        
# make copies of the colors in the dictionary with all lower case names
for colorName in NamedColorsOrig.keys():
    NamedColors[colorName.lower()] = NamedColorsOrig[colorName]
    
MarsCommand.RegisterCommandHandler("colornames", DumpColorNames)
MarsCommand.RegisterCommandHandler("colorvalue", ColorValue)
MarsCommand.RegisterCommandHandler("spawncouch", SpawnCouch)
MarsCommand.RegisterCommandHandler("couchcolor", CouchColor)