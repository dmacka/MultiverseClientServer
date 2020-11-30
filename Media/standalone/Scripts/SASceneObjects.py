import xml
import xml.dom

import ClientAPI

def getText(nodeList):
    rc = ""
    for node in nodeList:
        if node.nodeType == xml.dom.Node.TEXT_NODE:
            rc += node.data
    return rc

def parseScene(sceneFile):
    dom = xml.dom.minidom.parse(sceneFile)
    ClientAPI.LogInfo("dom = %s" % dom)
    return Machinima(dom.documentElement)

class Machinima:
    def __init__(self):
        self.Name = None
        self.World = None
        self.Interactive = False
        self.Scenes = []
        self.Render = None
        self.Encode = None

    def __init__(self, node):
        self.Name = None
        self.World = None
        self.Interactive = False
        self.Scenes = []
        self.Render = None
        self.Encode = None
        if node.hasAttribute('Name'):
            self.Name = node.getAttribute('Name')
        if node.hasAttribute('World'):
            self.World = node.getAttribute('World')
        if node.hasAttribute('Interactive'):
            if node.getAttribute('Interactive') == 'true':
                self.Interactive = True
        for childNode in node.childNodes:
            if childNode.nodeType == xml.dom.Node.ELEMENT_NODE:
                if childNode.tagName == 'Scene':
                    self.Scenes.append(Scene(childNode))
                elif childNode.tagName == 'Encode':
                    self.Encode = Encode(childNode)
                elif childNode.tagName == 'Render':
                    self.Render = Render(childNode)
        
    def _get_Scene(self):
        if len(self.Scenes) > 0:
            return self.Scenes[0]
        return None

    def __getattr__(self, attrname):
        if attrname in self._getters:
            return self._getters[attrname](self)
        else:
            raise AttributeError, attrname

    _getters = { 'Scene': _get_Scene }


class Scene:
    def __init__(self):
        self.length = 0.0
        self.CameraMarkers = []
        self.MobileObjects = []

    def __init__(self, node):
        self.length = 0.0
        self.CameraMarkers = []
        self.MobileObjects = []
        if node.hasAttribute('length'):
            self.length = float(node.getAttribute('length'))
        for childNode in node.childNodes:
            if childNode.nodeType == xml.dom.Node.ELEMENT_NODE:
                if childNode.tagName == 'CameraMarker':
                    self.CameraMarkers.append(getText(childNode.childNodes).strip())
                elif childNode.tagName == 'MobileObject':
                    self.MobileObjects.append(MobileObject(childNode))

    def _get_CameraMarker(self):
        if len(self.CameraMarkers) > 0:
            return self.CameraMarkers[0]
        return None

    def __getattr__(self, attrname):
        if attrname in self._getters:
            return self._getters[attrname](self)
        else:
            raise AttributeError, attrname

    _getters = { 'CameraMarker': _get_CameraMarker }


class MobileObject:
    def __init__(self):
        self.id = None
        self.Name = None
        self.Mesh = None
        self.SpawnPoint = None
        self.Animations = []
        self.Properties = {}

    def __init__(self, node):
        self.id = None
        self.Name = None
        self.Mesh = None
        self.SpawnPoint = None
        self.Animations = []
        self.Properties = {}
        if node.hasAttribute('id'):
            self.id = node.getAttribute('id')
        for childNode in node.childNodes:
            if childNode.nodeType == xml.dom.Node.ELEMENT_NODE:
                if childNode.tagName == 'Name':
                    self.Name = getText(childNode.childNodes).strip()
                elif childNode.tagName == 'Mesh':
                    self.Mesh = getText(childNode.childNodes).strip()
                elif childNode.tagName == 'SpawnPoint':
                    self.SpawnPoint = getText(childNode.childNodes).strip()
                elif childNode.tagName == 'Animation':
                    self.Animations.append(Animation(childNode))
                elif childNode.tagName == 'Property':
                    if childNode.hasAttribute('name') and childNode.hasAttribute('value'):
                        self.Properties[childNode.getAttribute('name')] = childNode.getAttribute('value')

class Animation:
    def __init__(self):
        self.name = None
        self.delay = 0.0
        self.loop = False
        
    def __init__(self, node):
        self.name = None
        self.delay = 0.0
        self.loop = False
        if node.hasAttribute('name'):
            self.name = node.getAttribute('name')
        if node.hasAttribute('delay'):
            self.delay = float(node.getAttribute('delay'))
        if node.hasAttribute('loop'):
            self.loop = bool(node.getAttribute('loop'))

class Render:
    def __init__(self):
        self.Width = 0
        self.Height = 0
        self.FPS = 15

    def __init__(self, node):
        self.Width = 0
        self.Height = 0
        self.FPS = 15
        if node.hasAttribute('Width'):
            self.Width = int(node.getAttribute('Width'))
        if node.hasAttribute('Height'):
            self.Height = int(node.getAttribute('Height'))
        if node.hasAttribute('FPS'):
            self.FPS = int(node.getAttribute('FPS'))
    
class Encode:
    def __init__(self):
        self.BitRate = 1500
        self.IndexFrame = 0
        self.Soundtrack = None
        self.ImageType = 'jpg'

    def __init__(self, node):
        self.BitRate = 1500
        self.IndexFrame = 0
        self.Soundtrack = None
        self.ImageType = 'jpg'
        if node.hasAttribute('BitRate'):
            self.BitRate = int(node.getAttribute('BitRate'))
        if node.hasAttribute('IndexFrame'):
            self.IndexFrame = int(node.getAttribute('IndexFrame'))
        if node.hasAttribute('Soundtrack'):
            self.SoundTrack = node.getAttribute('Soundtrack')
        if node.hasAttribute('ImageType'):
            self.ImageType = node.getAttribute('ImageType')
