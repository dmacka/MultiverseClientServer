import ClientAPI
import ObjCustomize
import math

def ObjCustom_SelectSubsurface(groupName, id):
    ObjCustom_InitColor()
    ObjCustom_InitParams()
    ObjCustom_InitPattern()
    
def ObjCustom_SelectColor(groupName, id):
    ObjCustom_InitColor()

RadioButton_RegisterGroup('subsurface', ObjCustom_SelectSubsurface)
RadioButton_RegisterGroup('color', ObjCustom_SelectColor)

currentPattern = 0
def ObjCustom_InitPattern():
    global patterns
    global currentPattern
    subsurfaceName = 'subsurface' + str(RadioButton_GetSelected('subsurface'))

    pattern = ObjCustomize.GetSubsurfaceProperty(subsurfaceName, 'tile')
    if pattern is None:
        pattern = 'solid'
    ObjCustomPatternSelectFramePatternTexture.SetTexture("Interface/FurniturePatterns/" + pattern)
    for i in range(0, len(patterns)):
        if patterns[i] == pattern:
            currentPattern = i
            break

def ObjCustom_NextPattern():
    global patterns
    global currentPattern
    subsurfaceName = 'subsurface' + str(RadioButton_GetSelected('subsurface'))

    currentPattern += 1
    if currentPattern == len(patterns):
        currentPattern = 0
    pattern = patterns[currentPattern]
    ObjCustomPatternSelectFramePatternTexture.SetTexture("Interface/FurniturePatterns/" + pattern)
    ObjCustomize.SetSubsurfaceProperty(subsurfaceName, 'tile', pattern)

def ObjCustom_PrevPattern():
    global patterns
    global currentPattern
    subsurfaceName = 'subsurface' + str(RadioButton_GetSelected('subsurface'))

    currentPattern -= 1
    if currentPattern < 0:
        currentPattern = len(patterns)-1
    pattern = patterns[currentPattern]
    ObjCustomPatternSelectFramePatternTexture.SetTexture("Interface/FurniturePatterns/" + pattern)
    ObjCustomize.SetSubsurfaceProperty(subsurfaceName, 'tile', pattern)

def ObjCustom_InitParams():
    subsurfaceName = 'subsurface' + str(RadioButton_GetSelected('subsurface'))

    scale = ObjCustomize.GetSubsurfaceProperty(subsurfaceName, 'scale')
    if scale is None:
        scale = 1.0
    logScale = (math.log10(scale) + 1)/3
    shiny = ObjCustomize.GetSubsurfaceProperty(subsurfaceName, 'shininess')
    if shiny is None:
        shiny = 1.0
    logShiny = (math.log10(shiny) + 1)/3

    ObjCustomParamFrameScale.SetValue(logScale)
    ObjCustomParamFrameScaleValue.SetText('%0.2f' % scale)
    ObjCustomParamFrameShiny.SetValue(logShiny)
    ObjCustomParamFrameShinyValue.SetText('%0.2f' % shiny)

def ObjCustom_InitColor():
    subsurfaceName = 'subsurface' + str(RadioButton_GetSelected('subsurface'))
    colorName = 'col' + str(RadioButton_GetSelected('color'))
    color = ObjCustomize.GetSubsurfaceProperty(subsurfaceName, colorName)
    if color is None:
        color = ClientAPI.ColorEx(1.0, 0.5, 0.5, 0.5)

    r = color.r
    g = color.g
    b = color.b
    a = color.a

    ObjCustomColorFrameRed.SetValue(r)
    ObjCustomColorFrameRedValue.SetText(str(r))
    ObjCustomColorFrameGreen.SetValue(g)
    ObjCustomColorFrameGreenValue.SetText(str(g))
    ObjCustomColorFrameBlue.SetValue(b)
    ObjCustomColorFrameBlueValue.SetText(str(b))
    ObjCustomColorFrameSpecular.SetValue(a)
    ObjCustomColorFrameSpecularValue.SetText(str(a))

    ObjCustomColorFrameSampleTexture.SetVertexColor(r, g, b)

def ObjCustom_UpdateColor():
    subsurfaceName = 'subsurface' + str(RadioButton_GetSelected('subsurface'))
    colorName = 'col' + str(RadioButton_GetSelected('color'))

    red = ObjCustomColorFrameRed.GetValue()
    green = ObjCustomColorFrameGreen.GetValue()
    blue = ObjCustomColorFrameBlue.GetValue()
    spec = ObjCustomColorFrameSpecular.GetValue()

    color = ClientAPI.ColorEx(spec, red, green, blue)

    ObjCustomize.SetSubsurfaceProperty(subsurfaceName, colorName, color)
    #colorDict = {}
    #colorDict['a'] = spec
    #colorDict['r'] = red
    #colorDict['g'] = green
    #colorDict['b'] = blue
    #ObjCustomize.SetSubsurfaceProperty(subsurfaceName, colorName, colorDict)

    ObjCustomColorFrameRedValue.SetText(str(color.r))
    ObjCustomColorFrameGreenValue.SetText(str(color.g))
    ObjCustomColorFrameBlueValue.SetText(str(color.b))
    ObjCustomColorFrameSpecularValue.SetText(str(color.a))

    ObjCustomColorFrameSampleTexture.SetVertexColor(red, green, blue)

def ObjCustom_UpdateParams():
    subsurfaceName = 'subsurface' + str(RadioButton_GetSelected('subsurface'))

    logScale = ObjCustomParamFrameScale.GetValue()
    scale = pow(10,logScale*3-1)
    logShiny = ObjCustomParamFrameShiny.GetValue()
    shiny = pow(10, logShiny*3-1)

    ObjCustomize.SetSubsurfaceProperty(subsurfaceName, 'scale', scale)
    ObjCustomize.SetSubsurfaceProperty(subsurfaceName, 'shininess', shiny)

    ObjCustomParamFrameScaleValue.SetText('%0.2f' % scale)
    ObjCustomParamFrameShinyValue.SetText('%0.2f' % shiny)

def ObjCustom_OnLoad(frame):
    frame.RegisterEvent("CUSTOMIZE_OBJECT")

    ObjCustomParamFrameScaleLabel.SetText('scale')
    ObjCustomParamFrameShinyLabel.SetText('shininess')
    ObjCustomColorFrameRedLabel.SetText('red')
    ObjCustomColorFrameGreenLabel.SetText('green')
    ObjCustomColorFrameBlueLabel.SetText('blue')
    ObjCustomColorFrameSpecularLabel.SetText('specular')
    getglobal(frame.GetName()+"Texture").SetVertexColor(0.20, 0.19, 0.17, 0.97)

import FurnitureTiles
patterns = FurnitureTiles.Tiles.keys()

