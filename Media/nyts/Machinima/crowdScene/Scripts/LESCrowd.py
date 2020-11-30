import ClientAPI
import SAUtil
import Region
import MarsCommand

NumMobs = 100

Tattoos = [
    'tattoo_butterfly_01_chest',
    'tattoo_butterfly_01_arm',
    'tattoo_butterfly_01_back',
    'tattoo_butterfly_02_chest',
    'tattoo_butterfly_02_arm',
    'tattoo_butterfly_02_back',
    'tattoo_butterfly_03_chest',
    'tattoo_butterfly_03_arm',
    'tattoo_butterfly_03_back',
    'tattoo_butterfly_04_chest',
    'tattoo_butterfly_04_arm',
    'tattoo_butterfly_04_back',
    'tattoo_butterfly_05_chest',
    'tattoo_butterfly_05_arm',
    'tattoo_butterfly_05_back',
    'tattoo_roses_01_chest',
    'tattoo_roses_01_arm',
    'tattoo_roses_01_back',
    'tattoo_roses_02_chest',
    'tattoo_roses_02_arm',
    'tattoo_roses_02_back',
    'tattoo_roses_03_chest',
    'tattoo_roses_03_arm',
    'tattoo_roses_03_back',
    'tattoo_roses_04_chest',
    'tattoo_roses_04_arm',
    'tattoo_roses_04_back',
    'tattoo_roses_05_chest',
    'tattoo_roses_05_arm',
    'tattoo_roses_05_back',
    'tattoo_roses_06_chest',
    'tattoo_roses_06_arm',
    'tattoo_roses_06_back',
    'tattoo_sunburst_01_chest',
    'tattoo_sunburst_01_arm',
    'tattoo_sunburst_01_back',
    'tattoo_sunburst_02_chest',
    'tattoo_sunburst_02_arm',
    'tattoo_sunburst_02_back',
    'tattoo_sunburst_03_chest',
    'tattoo_sunburst_03_arm',
    'tattoo_sunburst_03_back',
    'tattoo_sunburst_04_chest',
    'tattoo_sunburst_04_arm',
    'tattoo_sunburst_04_back',
    'tattoo_sunburst_05_chest',
    'tattoo_sunburst_05_arm',
    'tattoo_sunburst_05_back'
]
   
PossibleProps = [
    ('SkinColor', ['caucasian', 'asian', 'african_american']),
    ('HeadShape', ['caucasian_01', 'asian_01', 'african_american_01']),
    ('HeadDetail', ['']),
    ('HairStyle', ['bob', 'pony', 'layers', 'bob2']),
    ('HairColor', ['red', 'blonde', 'brown', 'black']),
    ('ClothesTorso', ['sleeveless_white', 'sleeveless_purple', 'sleeveless_blue', 'strapless_brown', 'strapless_purple', 'strapless_red', 'leotard_blue', 'leotard_red', 'leotard_skull'] ),
    ('ClothesLegs', ['capris_black', 'capris_brown', 'capris_blue', 'short_skirt_leopard', 'short_skirt_red']),
    ('Tattoo', Tattoos),
    ('AppearanceOverride', ['avatar'])
]

Dances = ['dance1', 'dance2', 'dance3', 'dance4', 'dance5', 'dance6']

# generate random appearance props
def RandomProps():
    props = []
    for name, values in PossibleProps:
        offset = ClientAPI.Random(len(values))
        #ClientAPI.Write('Prop: %s, Len: %d, Off: %d' % (name, len(values), offset))
        props.append((name, values[offset]))
    return props
    
def RandomMob(region):
    pt = region.RandomPoint()
    pos = ClientAPI.Vector3(pt.x, 20100.0, pt.z)
    quat = ClientAPI.Quaternion.FromEulerAnglesInDegrees(0.0, ClientAPI.RandomFloat(360.0), 0.0)
    #ClientAPI.Write('Spawning random mob at %s' % pos.ToString())
    mob = ClientAPI.WorldObject.WorldObject(ClientAPI.GetLocalOID(), SAUtil.GetUniqueName('mob'), 'LES_avatar.mesh', pos, True, quat, ClientAPI.Vector3.UnitScale, ClientAPI.WorldObject.WorldObjectType.Npc)
    for prop, value in RandomProps():
        mob.SetProperty(prop, value)
    dance = Dances[ClientAPI.Random(len(Dances))]
    ClientAPI.InvokeEffect("DelayAnimEffect", ClientAPI.GetLocalOID(), {'target': mob, 'delay': ClientAPI.Random(5000), 'anim' : dance})
        
def BuildCrowd():
    region = SAUtil.Regions['dancespawn']
    for i in range(NumMobs):
        RandomMob(region)
        
# test function that invokes the effect
def TestCrowd(argstr=""):
    BuildCrowd()

# register slash command to test the effect
MarsCommand.RegisterCommandHandler("testcrowd", TestCrowd)