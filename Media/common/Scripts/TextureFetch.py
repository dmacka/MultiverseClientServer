import ClientAPI
import MarsCommand
 
unique = 0

texObjMap = {}

def getUnique():
    global unique
    unique = unique+1
    return unique
   
def fetchHandler(textureName, loaded):
    ClientAPI.DebugWrite("texture handler : " + textureName)
    if loaded:
        ClientAPI.DebugWrite("texture loaded")
        
        # fetch the object
        cubeObj = texObjMap[textureName]
        
        # get the name of the submesh
        submesh = cubeObj.Model.SubMeshNames[0]
        
        # get material to copy
        baseMaterial = ClientAPI.GetMaterial("MVSimpleLighting")
        
        # make our own copy of the material
        cubeMaterial = baseMaterial.Clone('clonematerial%d' % getUnique())
        
        # apply the texture to the material
        cubeMaterial.ApplyTextureAlias("DiffuseTex", textureName)
        
        # set the new material on the model
        cubeObj.Model.SetSubMeshMaterial(submesh, cubeMaterial.Name)
        
def SpawnCube(url):
    
    # get a unique ID and use it to generate unique texture and object names
    id = getUnique()
    objName = 'cube%d' % id
    texName = 'cubeTex%d' % id

    playerPos = ClientAPI.GetPlayerObject().Position
    cubePos = ClientAPI.Vector3(playerPos.x, playerPos.y + 2000, playerPos.z + 2000)
    cubeObj = ClientAPI.WorldObject.WorldObject(ClientAPI.GetLocalOID(), objName, 'unit_box.mesh', cubePos, False, ClientAPI.GetPlayerObject().Orientation)
    
    # save object for later lookup by texture name
    texObjMap[texName] = cubeObj
    
    # call the fetcher
    ClientAPI.FetchRemoteTexture(url, texName, fetchHandler, 256, 256, True, ClientAPI.ColorEx.Blue)
    
MarsCommand.RegisterCommandHandler("spawncube", SpawnCube)
