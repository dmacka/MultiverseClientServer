import ClientAPI
import System

# Size of the displayed map in pixels.  This includes the buffer on each side.
XMinimapSize = 200
YMinimapSize = 200

# Size of the border in pixels
FrameEdgeBuffer = 8

# avatar base color RGB values: [0.0, 1.0]
RAvatar = 0.5
GAvatar = 0.5
BAvatar = 1.0

# zoom values
MinZoom = 0.5     # MinZoom must be > 0.0
ZoomInc = 0.5
ZoomLevels = 8

MaxZoom = MinZoom + ((ZoomLevels - 1) * ZoomInc)
# MinimapScale = 2
MinimapScale = MinZoom + (((ZoomLevels - 1)/2) * ZoomInc)

# Specify the size of minimap image in pixels
XImageSize = 1024
YImageSize =  512

# Specify the coordinates of the corners of the minimap image
# Upper Left coordinates in mm
ULx = -674785.7
ULz = -511844.4
# Lower Right coordinates in mm
LRx =  238214.3
LRz =   94686.2

# meters
FalseEasting  = ULx / 1000.0
FalseNorthing = ULz / 1000.0

# meters per pixel
Xmpp = ((LRx - ULx)/1000.0) / XImageSize
Ympp = ((LRz - ULz)/1000.0) / YImageSize

# ms
MinimapRefresh = 100


def _setCoords(t, A, B, C, D, E, F):
    det  = A*E - B*D
    bfce = B*F - C*E
    cdaf = C*D - A*F

    # ULx = ( (B*F) + -(C*E)) / det # ULx = ((B*F) - (C*E)) / det
    # ULy = (-(A*F) +  (C*D)) / det # ULy = ((C*D) - (A*F)) / det
    ULx = bfce / det
    ULy = cdaf / det

    # LLx = (-B +  (B*F) + -(C*E)) / det # LLx = ((B*F) - (C*E) - B) / det
    # LLy = ( A + -(A*F) +  (C*D)) / det # LLy = ((C*D) - (A*F) + A) / det
    LLx = (bfce - B) / det
    LLy = (cdaf + A) / det

    # URx = ( E +  (B*F) + -(C*E)) / det # URx = ((B*F) - (C*E) + E) / det
    # URy = (-D + -(A*F) +  (C*D)) / det # URy = ((C*D) - (A*F) - D) / det
    URx = (bfce + E) / det
    URy = (cdaf - D) / det

    # LRx = ( E + -B +  (B*F) + -(C*E)) / det # LRx = ((B*F) - (C*E) + E - B) / det
    # LRy = (-D +  A + -(A*F) +  (C*D)) / det # LRy = ((C*D) - (A*F) + A - D) / det
    LRx = (bfce + E - B) / det
    LRy = (cdaf + A - D) / det

    t.SetTexCoord(ULx, ULy, LLx, LLy, URx, URy, LRx, LRy)

def _rotate(t, rad):
   rad = rad - System.Math.PI
   c = System.Math.Cos(rad)
   s = System.Math.Sin(rad)
   factor = 1.4142136
   _setCoords(t, c * factor, s * factor, 0.5 + (-0.5 * c - 0.5 * s) * factor, -s * factor, c * factor, 0.5 + (-0.5 * c + 0.5 * s) * factor)

def _extent(t, x_mm, y_mm, width_pixels, height_pixels, scale):
    # x is EW
    # y is NS
    x_m = x_mm / 1000.0
    y_m = y_mm / 1000.0

    half_width_m  = (width_pixels  * MinimapScale / 2.0) * Xmpp
    half_height_m = (height_pixels * MinimapScale / 2.0) * Ympp

    left_m   = x_m - half_width_m
    right_m  = x_m + half_width_m

    top_m    = y_m - half_height_m
    bottom_m = y_m + half_height_m

    left_ratio  = (left_m  - FalseEasting) / (XImageSize * Xmpp)
    right_ratio = (right_m - FalseEasting) / (XImageSize * Xmpp)

    top_ratio    = (top_m    - FalseNorthing) / (YImageSize * Ympp)
    bottom_ratio = (bottom_m - FalseNorthing) / (YImageSize * Ympp)

    t.SetTexCoord(left_ratio, right_ratio, top_ratio, bottom_ratio)
    # t.SetTexCoord(ULx, ULy, LLx, LLy, URx, URy, LRx, LRy)

def MvMinimap_OrientationUpdate():
    player = ClientAPI.GetPlayerObject()
    if player is None:
        return
    AvatarTexture = getglobal("MvMinimapMapOverlayFrameFrameAvatarIconLayerTextureAvatarIcon")
    _rotate(AvatarTexture, player.Orientation.Yaw)

def MvMinimap_RegionUpdate():
    player = ClientAPI.GetPlayerObject()
    if player is None:
        return
    MapTexture = getglobal("MvMinimapMapOverlayFrameLayerTextureMap")
    # Position.x is EW
    # Position.y is altitude
    # Position.z is NS
    _extent(MapTexture, player.Position.x, player.Position.z, (XMinimapSize - (2 * FrameEdgeBuffer)), (YMinimapSize - (2 * FrameEdgeBuffer)), MinimapScale)

def MvMinimap_TickHandler(arg1, arg2):
    global lastTimeTick
    if (ClientAPI.GetCurrentTime() - lastTimeTick < MinimapRefresh):
        return
    lastTimeTick = ClientAPI.GetCurrentTime()
    MvMinimap_OrientationUpdate()
    MvMinimap_RegionUpdate()

def MvMinimap_OnLoad():
    global lastTimeTick
    lastTimeTick = ClientAPI.GetCurrentTime()
    ClientAPI.RegisterEventHandler("FrameStarted", MvMinimap_TickHandler)

def MvMinimap_ZoomIn():
    global MinimapScale
    MinimapScale = MinimapScale - ZoomInc
    if (MinimapScale > MaxZoom):
        MinimapScale = MaxZoom
    if (MinimapScale < MinZoom):
        MinimapScale = MinZoom
    MvMinimap_RegionUpdate()

def MvMinimap_ZoomOut():
    global MinimapScale
    MinimapScale = MinimapScale + ZoomInc
    if (MinimapScale > MaxZoom):
        MinimapScale = MaxZoom
    if (MinimapScale < MinZoom):
        MinimapScale = MinZoom
    MvMinimap_RegionUpdate()

def ToggleMinimap():
    if MvMinimapFrame.IsVisible():
        MvMinimapFrame.Hide()
    else:
        MvMinimapFrame.Show()

# ClientAPI.Write("MvMinimap")

AvatarTexture = getglobal("MvMinimapMapOverlayFrameFrameAvatarIconLayerTextureAvatarIcon")
AvatarTexture.SetVertexColor(RAvatar, GAvatar, BAvatar)

MvMinimap_OrientationUpdate()
MvMinimap_RegionUpdate()

MvMinimapFrame.SetWidth(XMinimapSize)
MvMinimapFrame.SetHeight(YMinimapSize)
MvMinimapFrame.Show()

# ClientAPI.Write("MvMinimap loaded")
