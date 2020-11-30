import ClientAPI
import SAUtil
import Region
import MarsCommand

NumMobs = 100

Models = [ 'casual03_m_mediumpoly.mesh',
    'casual04_m_mediumpoly.mesh',
    'casual07_m_mediumpoly.mesh',
    'casual10_m_mediumpoly.mesh',
    'casual16_m_mediumpoly.mesh',
    'casual21_m_mediumpoly.mesh',
    'business03_m_mediumpoly.mesh',
    'business05_m_mediumpoly.mesh',
    'sportive01_m_mediumpoly.mesh',
    'sportive09_m_mediumpoly.mesh',
    'casual06_f_mediumpoly.mesh',
    'casual07_f_mediumpoly.mesh',
    'casual13_f_mediumpoly.mesh',
    'casual15_f_mediumpoly.mesh',
    'casual19_f_mediumpoly.mesh', 
    'casual21_f_mediumpoly.mesh', 
    'business04_f_mediumpoly.mesh',
    'sportive01_f_mediumpoly.mesh',
    'sportive02_f_mediumpoly.mesh',
    'sportive05_f_mediumpoly.mesh',
    'sportive07_f_mediumpoly.mesh', 
    ]
    
def RandomMob(region):
    pt = region.RandomPoint()
    pos = ClientAPI.Vector3(pt.x, 20100.0, pt.z)
    quat = ClientAPI.Quaternion.FromEulerAnglesInDegrees(0.0, ClientAPI.RandomFloat(360.0), 0.0)
    #ClientAPI.Write('Spawning random mob at %s' % pos.ToString())
    model = Models[ClientAPI.Random(len(Models))]
    mob = ClientAPI.WorldObject.WorldObject(ClientAPI.GetLocalOID(), SAUtil.GetUniqueName('mob'), model, pos, True, quat, ClientAPI.Vector3.UnitScale, ClientAPI.WorldObject.WorldObjectType.Npc)
    ClientAPI.InvokeEffect("DelayAnimEffect", ClientAPI.GetLocalOID(), {'target': mob, 'delay': ClientAPI.Random(5000), 'anim' : 'dance'})
        
def BuildCrowd(count):
    region = SAUtil.Regions['dancespawn']
    for i in range(count):
        RandomMob(region)
        
# test function that invokes the effect
def TestCrowd(argstr=""):
    BuildCrowd(NumMobs)

# register slash command to test the effect
MarsCommand.RegisterCommandHandler("testcrowd", TestCrowd)