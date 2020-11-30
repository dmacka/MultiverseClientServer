import ClientAPI

compositor = None

# app can set a different screenshot path
ScreenshotPath = None
ScreenshotNum = 0
# this defaults to png, but will be changed to jpg when we have an 'Encode' tag
ScreenshotExtension = 'png'
# ScreenshotExtension = 'jpg'
PixelFormat = ClientAPI.PixelFormat.BYTE_RGB
CompositorName = 'FastScreenshot'
# If Width and Height are None, we will use the viewport dimensions
Width = 0
Height = 0

nextScreenshotName = None
shotCount = 0

def CreateCompositor():
    global compositor
    global CompositorName
    global Width
    global Height
    # If the compositor already exists, we can skip this
    if compositor is not None:
        return
    # Create the new compositor
    compositor = ClientAPI.Compositor.Compositor(CompositorName)
    # Set the various properties on the compositor
    compositor.SetTextureResolution('rt0', Width, Height)
    compositor.Enabled = True

def DisposeCompositor():
    global compositor
    global CompositorName
    if compositor is not None:
        compositor.Dispose()
        compositor = None

def SetTextureResolution(width, height):
    global Width
    global Height
    Width = width
    Height = height
    
def SetCompositor(compositorName):
    global compositor
    global CompositorName
    CompositorName = compositorName
    DisposeCompositor()
    CreateCompositor()
        
def CompositorOn():
    global compositor
    global CompositorName
    CreateCompositor()
    
def CompositorOff():
    global compositor
    DisposeCompositor()

def ToggleCompositor():
    global compositor
    if compositor is not None:
        CompositorOff()
    else:
        CompositorOn()
        
def Capture(ssname):
    global ScreenshotPath
    global ScreenshotNum
    global ScreenshotExtension
    global PixelFormat
    
    # Get screenshot number and path from the client unless they have been
    #  overridden by a script.
    if ScreenshotPath is None:
        ssPath = ClientAPI.ScreenshotPath
    else:
        ssPath = ScreenshotPath

    if ssname is None:
        if ScreenshotNum is None:
            ssNum = ClientAPI.NumExistingScreenshots() + 1
        else:
            ssNum = ScreenshotNum
            ScreenshotNum = ScreenshotNum + 1
        ssname = 'screenshot%05d.%s' % (ssNum, ScreenshotExtension)
    
    # make sure path ends with a separator
    if not ssPath.endswith('\\'):
        ssPath = ssPath + '\\'
    filename = ssPath + ssname
    
    if compositor is not None:
        compositor.SaveRenderTarget('rt0', filename, PixelFormat)
        # ClientAPI.Write('Wrote screenshot %s' % filename)

def Screenshot():
    Screenshot(None)

def Screenshot(ssname):
    global nextScreenshotName
    global shotCount
    nextScreenshotName = ssname
    Screenshots(1)
    
def ScreenshotsDone():
    return shotCount <= 0

def doScreenshots(sender, args):
    global nextScreenshotName
    global shotCount
    Capture(nextScreenshotName)
    
    shotCount = shotCount - 1
    if shotCount <= 0:
        ClientAPI.RemoveEventHandler('FrameEnded', doScreenshots)
        CompositorOff()
    
def Screenshots(numShots):
    global shotCount
    if int(numShots) < 1:
        numShots = 1
    shotCount = numShots
    CompositorOn()
    ClientAPI.RegisterEventHandler('FrameEnded', doScreenshots)

def ScreenshotsCommand(argstr=""):
    count = int(argstr)
    ClientAPI.Write('Starting capture of %d screenshots' % count)
    Screenshots(count)

def ScreenshotCommand(argstr=""):
    Screenshot(argstr)

import MarsCommand

# register slash command to test the effect
MarsCommand.RegisterCommandHandler("screenshots", ScreenshotsCommand)
MarsCommand.RegisterCommandHandler("screenshot", ScreenshotCommand)
