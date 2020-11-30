import ClientAPI
import MarsCommand

#
# This class manages the data associated with a subsurface, and affects the changes
#  in the material and colormap texture.
# 
class SubSurface(object):
    def __init__(self, material, subSurfaceNum, colormap, colorUOffset, colorVCoord, tileMap):
        self._material = material
        self._subSurfaceNum = subSurfaceNum
        self._colormap = colormap
        self._colorUOffset = colorUOffset
        self._colorVCoord = colorVCoord
        self._pass = material.GetBestTechnique().GetPass('Single')
        self._tileMap = tileMap
        
        # initialize to default tile
        self.TileName = 'solid_01'
        
        self._scale = 1.0
        self._shininess = 1.0
        self._set_ShininessAndScale()
        
        # initialize all colors to black
        self.SetColor(0, ClientAPI.ColorEx.Gray, False)
        self.SetColor(1, ClientAPI.ColorEx.Gray, False)
        self.SetColor(2, ClientAPI.ColorEx.Gray, False)
        self.SetColor(3, ClientAPI.ColorEx.Gray, False)
        
        # initialize all specular multipliers
        self.SetSpecularMult(0, 0.0, False)
        self.SetSpecularMult(1, 0.0, False)
        self.SetSpecularMult(2, 0.0, False)
        self.SetSpecularMult(3, 0.0, False)
        
    def _get_TileName(self):
        return self._tileName
        
    def _set_TileName(self, name):
        # use the solid tile if we can't find the one asked for
        if name in self._tileMap:
            self._tileName = name
        else:
            self._tileName = 'solid_01'
        # fetch the tile parameters
        (self._tileU, self._tileV, self._tileW, self._tileH) = self._tileMap[self._tileName]
        
        # compute vector of values for gpu param
        v = ClientAPI.Vector4(self._tileU, self._tileV, self._tileW, self._tileH)
        
        # compute gpu param name
        paramName = 'tileOffsetAndSize[%d]' % self._subSurfaceNum
        
        # set the gpu parameter
        self._pass.SetGPUParam(ClientAPI.GPUProgramType.Vertex, paramName, v)

        
    TileName = property(_get_TileName, _set_TileName, None, None)
    
    # internal method for setting the scale and shininess gpu param
    def _set_ShininessAndScale(self):
        v = ClientAPI.Vector4(self._shininess, self._scale, 0, 0)

        # compute gpu param name
        paramName = 'shininessAndScale[%d]' % self._subSurfaceNum        

        # set the gpu parameter
        self._pass.SetGPUParam(ClientAPI.GPUProgramType.Vertex, paramName, v)
                
    def _get_Scale(self):
        return self._scale
        
    def _set_Scale(self, scale):
        self._scale = scale
        self._set_ShininessAndScale()
        
    Scale = property(_get_Scale, _set_Scale, None, None)
    
    def _get_Shininess(self):
        return self._shininess
        
    def _set_Shininess(self, shininess):
        self._shininess = shininess
        self._set_ShininessAndScale()
        
    Shininess = property(_get_Shininess, _set_Shininess, None, None)
    
    # Set one of this subsurface's color values in the colormap.
    # Note that this only sets RGB, and preserves Alpha, which is used
    #  to hold the specular multiplier.
    def SetColor(self, colorNum, color, loadTexture):
        x = self._colorUOffset + colorNum
        saveColor = self._colormap.GetPixel(x, self._colorVCoord)
        newColor = ClientAPI.ColorEx(saveColor.a, color.r, color.g, color.b)
        self._colormap.SetPixel(x, self._colorVCoord, newColor)
        if loadTexture:
            self._colormap.LoadTexture()
    
    # Set one of this subsurface's color specular multipliers in the colormap.
    # Note that this only sets the Alpha channel, which is used to hold the
    #  specular multiplier, and that the RGB channels are preserved.
    def SetSpecularMult(self, colorNum, specular, loadTexture):
        x = self._colorUOffset + colorNum
        saveColor = self._colormap.GetPixel(x, self._colorVCoord)
        newColor = ClientAPI.ColorEx(specular, saveColor.r, saveColor.g, saveColor.b)
        self._colormap.SetPixel(x, self._colorVCoord, newColor)
        if loadTexture:
            self._colormap.LoadTexture()
            
    # Set one of this subsurface's colors and specular multiplier in the colormap.
    # Note that the alpha channel of the color contains the specular multiplier
    def SetColorAndSpecular(self, colorNum, color, loadTexture):
        x = self._colorUOffset + colorNum
        self._colormap.SetPixel(x, self._colorVCoord, color)
        if loadTexture:
            self._colormap.LoadTexture()

colormapSize = 256
SharedColormap = None
colormapSlots = None
colormapName = 'colored_furniture_colormap'
colorsPerSubsurface = 4
subsurfacesPerObject = 8
colorsPerObject = colorsPerSubsurface * subsurfacesPerObject

#
# Initialize the shared colormap
#
def InitColormap():
    global SharedColormap
    global colormapSlots
    global colormapSize
    
    # initialize list of colormap slots
    colormapSlots = []
    for i in range(0, colormapSize):
        colormapSlots.append(None)

    # initialize the colormap with no mipmaps and fill it with black    
    SharedColormap = ClientAPI.EditableImage.EditableImage(colormapName, colorsPerObject, colormapSize, ClientAPI.PixelFormat.A8R8G8B8, ClientAPI.ColorEx.Black, 0)
    SharedColormap.LoadTexture()
    
#
# Find the first slot that is not in use in the colormap
#
def FindColormapSlot(obj):
    for i in range(0, len(colormapSlots)):
        if colormapSlots[i] is None:
            colormapSlots[i] = obj
            return i
    return -1
    
#
# Mark the colormap slot as being free for future use
#
def FreeColormapSlot(slot):
    colormapSlots[slot] = None

class ColoredObject:
    def __init__(self, worldObj, atlasName, tileMap, ambientOcclusionMap):
        global SharedColormap
        self._worldObj = worldObj
        
        # find out slot in the colormap
        self._colormapSlot = FindColormapSlot(self)
        
        # create the material
        self.SetupMaterial(atlasName, ambientOcclusionMap)
        
        # set the material on all submeshes of the object
        for submeshName in worldObj.Model.SubMeshNames:
            worldObj.Model.SetSubMeshMaterial(submeshName, self._material.Name)

        # set up the subsurfaces
        self.Subsurfaces = []
        cmOffset = 0
        for i in range(0, subsurfacesPerObject):
            self.Subsurfaces.append(SubSurface(self._material, i, SharedColormap, cmOffset, self._colormapSlot, tileMap))
            cmOffset = cmOffset + colorsPerSubsurface
            
        # after all the subsurfaces are initialized, load the texture
        SharedColormap.LoadTexture()
        
    def SetupMaterial(self, atlasName, ambientOcclusionMap):
        baseMaterial = ClientAPI.GetMaterial('ColoredFurniture')
        
        # create a unique material for this object instance
        material = ClientAPI.GetMaterial('ColoredFurniture-%s' % str(self._worldObj.OID))
        if material is None:
            material = baseMaterial.Clone('ColoredFurniture-%s' % str(self._worldObj.OID))
        self._material = material
        material.Load()
        
        # apply the colormap to the material
        material.ApplyTextureAlias("ColormapTex", colormapName)
        material.ApplyTextureAlias("AtlasTex", atlasName)
        material.ApplyTextureAlias("AmbientOcclusionTex", ambientOcclusionMap)
        
        # compute vertical offset in the colormap.  Include half pixel offset.
        vPixelSize = 1.0 / colormapSize
        vCoord = ( self._colormapSlot + 0.5 ) * vPixelSize
        
        # set object specific gpu params
        matpass = material.GetBestTechnique().GetPass('Single')
        matpass.SetGPUParam(ClientAPI.GPUProgramType.Vertex, 'colormapVCoord', float(vCoord))
        
    def Brighten(self, value):
        matpass = self._material.GetBestTechnique().GetPass('Single')
        matpass.SetGPUParam(ClientAPI.GPUProgramType.Vertex, 'brighten', value)
    
    def Dispose(self):
        FreeColormapSlot(self._colormapSlot)
        
#
# Stuff to do at startup
#
InitColormap()
