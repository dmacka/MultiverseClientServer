#
# This is a fake standin version of SAScene.py which is used for testing.  The real one
#  should be generated from the queued rendering request
#

import ClientAPI
import SASceneObjects

machinima = SASceneObjects.parseScene(ClientAPI.GetAssetPath('SAScene.xml'))
ScreenshotPath = None
Properties = {}
