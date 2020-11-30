# import clr
# clr.AddReference("System")
# clr.AddReference("Multiverse.Network")

from System.Math import PI
from System.Collections.Generic import *
from Axiom.Core import ColorEx
from Axiom.MathLib import *
from Multiverse.Network import *
from Multiverse.Base import Client
from Multiverse.MathLib import MathUtil

def InitStandaloneWorld():
    # First, the login response
    loginResponse = AuthorizedLoginResponseMessage()
    loginResponse.Oid = 1
    loginResponse.Success = True
    loginResponse.Message = "standalone"
    loginResponse.Version = "standalone"
    MessageDispatcher.Instance.QueueMessage(loginResponse)
    
    # Next, set up the world
    InitializeWorld()
    # Initialize vegetation
    InitializeVegetation()
    # Setup the directional lights
    InitializeLights()
    # Set up the sound
    InitializeSound()
    # Now, set up the player model
    InitializePlayer()
    # Add Lucy
    InitializeLucy()
    # Add the Orc
    InitializeOrc()
    # Add Saul
    InitializeSaul()
    # Add the static world objects
    AddWorldObjects()
    # Send a test comm message
    SendTestComm()
    # Send a test extension message
    SendTestExtension()
    # Tell the client we're initialized
    SendLoadingStateMessage()

def InitializeWorld():
    forestInitString = "<boundaries><boundary><name>boundary1</name><points><point x=\"441000\" y=\"4269000\" /><point x=\"105000\" y=\"4278000\" /><point x=\"66000\" y=\"4162000\" /><point x=\"-132000\" y=\"4102000\" /><point x=\"-540000\" y=\"3658000\" /><point x=\"-639000\" y=\"3570000\" /><point x=\"182000\" y=\"3510000\" /><point x=\"236000\" y=\"3845000\" /><point x=\"382000\" y=\"3966000\" /></points> <boundarySemantic type=\"SpeedTreeForest\"><seed>1234</seed><name>Forest1</name><windFilename>demoWind.ini</windFilename><windStrength>1</windStrength><windDirection x=\"1\" y=\"0\" z=\"0\" /><treeType filename=\"WeepingWillow_RT_Fall.spt\" size=\"4500\" sizeVariance=\"0\" numInstances=\"30\" /><treeType filename=\"AmericanBoxwood_RT.spt\" size=\"6000\" sizeVariance=\"0\" numInstances=\"30\" /><treeType filename=\"RDApple_RT_Apples.spt\" size=\"5000\" sizeVariance=\"0\" numInstances=\"30\" /></boundarySemantic> </boundary><boundary><name>boundary2</name><points><point x=\"285000\" y=\"3462000\" /><point x=\"-679000\" y=\"3560000\" /><point x=\"-647000\" y=\"3381000\" /><point x=\"-512000\" y=\"3230000\" /><point x=\"402000\" y=\"3116000\" /><point x=\"402000\" y=\"3339000\" /><point x=\"305000\" y=\"3363000\" /></points> <boundarySemantic type=\"SpeedTreeForest\"><seed>1234</seed><name>Forest2</name><windFilename>demoWind.ini</windFilename><windStrength>1</windStrength><windDirection x=\"1\" y=\"0\" z=\"0\" /><treeType filename=\"EnglishOak_RT.spt\" size=\"9000\" sizeVariance=\"0\" numInstances=\"150\" /><treeType filename=\"AmericanHolly_RT.spt\" size=\"3000\" sizeVariance=\"0\" numInstances=\"150\" /><treeType filename=\"WeepingWillow_RT_Fall.spt\" size=\"3000\" sizeVariance=\"0\" numInstances=\"150\" /></boundarySemantic> </boundary></boundaries>"
    terrainInitString = "<Terrain><algorithm>HybridMultifractalWithSeedMap</algorithm><xOffset>-0.4</xOffset><yOffset>-0.3</yOffset><zOffset>0</zOffset><h>0.25</h><lacunarity>2</lacunarity><octaves>8</octaves><metersPerPerlinUnit>800</metersPerPerlinUnit><heightScale>300</heightScale><heightOffset>-0.15</heightOffset><fractalOffset>0.1</fractalOffset><heightFloor>0</heightFloor><seedMapOriginX>-3200</seedMapOriginX><seedMapOriginY>0</seedMapOriginY><seedMapOriginZ>-5120</seedMapOriginZ><seedMapMetersPerSample>128</seedMapMetersPerSample><outsideSeedMapHeight>0</outsideSeedMapHeight><seedMap width=\"50\" height=\"80\" mapFormat=\"digitString\">0000000000000000011111111000000000000000000000000000000000000000011111111111000000000000000000000000000000000000001112212221211000000000000000000000000000000000000112222222222211000000000000000000000000000000000001122222222222211000000000000000000000000000000000112223333222222211000000000000000000000000000000011222333333332222110000000000000000000000000000001122554344443332222110000000000000000000000000000112257655555544333222211000000000000000000000000011225776555555544433221110000000000000000000000000112557766655555444443322110000000000000000000000001125577755665665444443221110000000000000000000000011257987766666664444433322110000000000000000000000112579878866666644444333322110000000000000000000011125798777666666544444333322110000000000000000001121257988766666666665444433321100000000000000000011212579887766666666654444333221100000000000000000112224579877666666666544444333211000000000000000001123445798666666666665544443332110000000000000000011234457986666666666665444433321100000000000000001122444557986666666666654333332211000000000000000112234445579866666666666543332221100000000000000000112334445798666666666665543321110000000000000000001123444555798666666666665433211000000000000000000011233444557986666666666654332211000000000000000000112234444579866666666666544332110000000000000000000112344455787666666666665443322110000000000000000001122344555666666666666665443322110000000000000000001122444557876666666666655533322110000000000000000001124444579866666666666665333322110000000000000000011234445798666666666666653333322110000000000000001122344555798666666666666653333322110111000000000011223445557986666666666666533333321101210000000000011224445579866666666666665533333221111100000000000011234445798666666666666665333333221100000000000000112234457986666666666666653333333211000000000000000112244557986666666666666533333332110000000000000000112345579866666666666665333333321100000000000000011223445579866666666666444433333211000000000000000112444557688666666666644443333332110000000000000001122445576877666666664444333333322110000000000000001124445678776666666644444433333211000000000000000011234456798766644444444433333222110000000000000000112344579997764444444444333332121100000000000000001123455799976444444444444433321110000200000000000011244568999764444444444444333221100000000000000000112445677786555554444466444333211100000000000000011224444556655555544446666443332221100000000000000112334444445555655555666664443322110000000000000001123344444445555655576666644332211000000000000000111233344444455555555577776553221100000000000000111222333444444445555555577766532110000000000000011122333334444444575555555577665221100000000000001122223333344444445755555555576652110000000000000011222333333444444557555555555566421100000000000000112223333344444445766555555555642211000000000000001122233334444444457655555554455421100000000000000011222333334444445586443334444542211000000000000000011222333334444575754333344442211100000000000000001122222333344445755433333442221110000000000000000001122223333334557544333333221110000000000000000000001122223333345675433333222111000000000000000000000001111222333557533333332111000000000000000000000000001111122222553333333222110000000000000000000000000000011111122533333332121100000000000000000000000000000001111122333333321110000000000000000000000000000000000001123333332211100000000000000000000000000000000000011233333321100000000000000000000000000000000000000112233333211000000000000000000000000000000000000000112233332110000000000000000000000000000000000000000112233321100000000000000000000000000000000000000000112233221100000000000000000000000000000000000000000112223211000000000000000000000000000000000000000000111232110000000000000000000000000000000000000000000112221100000000000000000000000000000000000000000000111221100000000000000000000000000000000000000000000111110000000000000000000000000000000000000000000000011000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000</seedMap></Terrain>"
    
    # Initialization messages
    terrainConfigMessage = TerrainConfigMessage()
    terrainConfigMessage.ConfigString = terrainInitString
    MessageDispatcher.Instance.QueueMessage(terrainConfigMessage)

    newObjMessage = NewObjectMessage()
    newObjMessage.Oid = 1
    newObjMessage.ObjectId = 1
    newObjMessage.Name = "Fengal"
    # by the beach
    # newObjMessage.Location = Vector3(546000, 0, 3643000)
    # in town
    newObjMessage.Location = Vector3(123000, 0, 3643000)
    # by the trees
    # newObjMessage.Location = Vector3(0, 0, 4000000)
    newObjMessage.Orientation = Quaternion.FromAngleAxis(PI, Vector3.UnitY)
    newObjMessage.ScaleFactor = Vector3.UnitScale
    newObjMessage.ObjectType = ObjectNodeType.User
    newObjMessage.FollowTerrain = True
    MessageDispatcher.Instance.QueueMessage(newObjMessage)

    uiThemeMessage = UiThemeMessage()
    uiThemeMessage.UiModules = List[str]()
    # uiThemeMessage.UiModules.Add("basic.toc")
    uiThemeMessage.UiModules.Add("mars.toc")
    MessageDispatcher.Instance.QueueMessage(uiThemeMessage)

    skyboxMaterialMessage = SkyboxMaterialMessage()
    skyboxMaterialMessage.Material = "Multiverse/SceneSkyBoxSunset"
    MessageDispatcher.Instance.QueueMessage(skyboxMaterialMessage)

    ambientLightMessage = AmbientLightMessage()
    ambientLightMessage.Color = ColorEx.Gray
    MessageDispatcher.Instance.QueueMessage(ambientLightMessage)
    
    fogMessage = FogMessage()
    fogMessage.FogColor = ColorEx(.77, .89, 1.0)
    fogMessage.FogStart = 10 * Client.OneMeter
    fogMessage.FogEnd = 20 * Client.OneMeter
    # fogMessage.FogStart = 100 * Client.OneMeter
    # fogMessage.FogEnd = Client.HorizonDistance
    # MessageDispatcher.Instance.QueueMessage(fogMessage)

    # regionConfigMessage = RegionConfigMessage()
    # regionConfigMessage.ConfigString = forestInitString
    # MessageDispatcher.Instance.QueueMessage(regionConfigMessage)
    
    roadInfoMessage = RoadInfoMessage()
    roadInfoMessage.Name = "Via Appia"
    roadInfoMessage.Points.Add(Vector3(97000, 0, 4156000))
    roadInfoMessage.Points.Add(Vector3(205000, 0, 4031000))
    roadInfoMessage.Points.Add(Vector3(254000, 0, 3954000))
    roadInfoMessage.Points.Add(Vector3(234000, 0, 3500000))
    roadInfoMessage.Points.Add(Vector3(256000, 0, 3337000))
    roadInfoMessage.Points.Add(Vector3(98000, 0, 3242000))
    MessageDispatcher.Instance.QueueMessage(roadInfoMessage)
    # End of initialization messages


def InitializeLights():
    newLightMessage = NewLightMessage()
    newLightMessage.Oid = 1
    newLightMessage.ObjectId = 100
    newLightMessage.Name = "dirlight"
    newLightMessage.LightType = LightNodeType.Directional
    newLightMessage.Orientation = Quaternion.FromAngleAxis(1, Vector3(1, 0, 0))
    # newLightMessage.Orientation = Quaternion()
    # newLightMessage.LightType = LightNodeType.Point
    newLightMessage.Location = Vector3(100, 100, 100)
    newLightMessage.Diffuse = ColorEx.Gray
    newLightMessage.Specular = ColorEx.Gray
    newLightMessage.AttenuationRange = 1000 * Client.OneMeter
    newLightMessage.AttenuationConstant = 1.0
    newLightMessage.AttenuationLinear = 0.0
    newLightMessage.AttenuationQuadratic = 0.0
    MessageDispatcher.Instance.QueueMessage(newLightMessage)

    newLightMessage = NewLightMessage()
    newLightMessage.Oid = 1
    newLightMessage.ObjectId = 101
    newLightMessage.Name = "pointlight"
    newLightMessage.LightType = LightNodeType.Point
    newLightMessage.Orientation = Quaternion()
    newLightMessage.Location = Vector3(123000, 90000, 3643000)
    newLightMessage.Diffuse = ColorEx.Red
    newLightMessage.Specular = ColorEx.Red
    newLightMessage.AttenuationRange = 20 * Client.OneMeter
    newLightMessage.AttenuationConstant = 0.001
    newLightMessage.AttenuationLinear = 0.0
    newLightMessage.AttenuationQuadratic = 0.0000001
    MessageDispatcher.Instance.QueueMessage(newLightMessage)

def InitializeQuestData():
    infoMessage = QuestInfoResponseMessage()
    infoMessage.Oid = 1
    infoMessage.ObjectId = 2
    infoMessage.QuestId = 1
    infoMessage.Title = "Shrubbery Quest"
    infoMessage.Description = "Kabeker needs a shrubbery to decorate his home.  But wait, there's more.  Act now and get three matching knives for just 9 platinum."
    infoMessage.Objective = "Get a shrubbery"
    item = ItemEntry()
    item.name = "Sword of Killin Stuff"
    item.icon = "Interface\Icons\INV_weapon_sword"
    item.count = 0
    infoMessage.RewardItems.Add(item)
    # MessageDispatcher.Instance.QueueMessage(infoMessage)

    questLogMessage = QuestLogInfoMessage()
    questLogMessage.Oid = 1
    questLogMessage.QuestId = 1
    questLogMessage.Title = "Shrubbery Quest"
    questLogMessage.Description = "Hail mighty adventurer, I am filling your quest log with lots of junk that you will have to read.  If you are lucky, I will scroll really slowly.  Kabeker needs a shrubbery to decorate his home.  I want to put even more text here just to test random stuff.  What will happen if we have too much? Can you have too much of something.  I guess not, I still needed more text.  Hail mighty adventurer, I am filling your quest log with lots of junk that you will have to read.  If you are lucky, I will scroll really slowly.  Kabeker needs a shrubbery to decorate his home.  I want to put even more text here just to test random stuff.  What will happen if we have too much? Can you have too much of something.  I guess not, I still needed more text."
    questLogMessage.Objective = "Get a shrubbery"
    MessageDispatcher.Instance.QueueMessage(questLogMessage)
    
    questLogMessage = QuestLogInfoMessage()
    questLogMessage.Oid = 1
    questLogMessage.QuestId = 2
    questLogMessage.Title = "Tree Quest"
    questLogMessage.Description = "Kabeker needs a tree."
    questLogMessage.Objective = "Get a tree"
    questLogMessage.RewardItems = List[ItemEntry]()
    entry = ItemEntry()
    entry.name = "Leather Armor"
    entry.icon = "Interface\Icons\INV_clothes_armor"
    entry.count = 3
    questLogMessage.RewardItems.Add(entry)
    entry = ItemEntry()
    entry.name = "Some Boots"
    entry.icon = "Interface\Icons\INV_clothes_boots"
    entry.count = 0
    questLogMessage.RewardItems.Add(entry)
    MessageDispatcher.Instance.QueueMessage(questLogMessage)
    
    questStateMessage = QuestStateInfoMessage()
    questStateMessage.Oid = 1
    questStateMessage.QuestId = 1
    questStateMessage.Objectives.Add("Tree: 0/1")
    MessageDispatcher.Instance.QueueMessage(questStateMessage)


def InitializeGroup():
    groupMessage = GroupInfoMessage()
    groupMessage.Oid = 1
    groupMessage.LeaderId = 1
    groupMessage.GroupId = 1
    groupEntry = GroupInfoEntry()
    groupEntry.memberId = 1
    groupEntry.memberName = "Peter"
    groupMessage.GroupInfoEntries.Add(groupEntry)
    groupEntry = GroupInfoEntry()
    groupEntry.memberId = 2
    groupEntry.memberName = "Paul"
    groupMessage.GroupInfoEntries.Add(groupEntry)
    groupEntry = GroupInfoEntry()
    groupEntry.memberId = 3
    groupEntry.memberName = "Mary"
    groupMessage.GroupInfoEntries.Add(groupEntry)
    groupEntry = GroupInfoEntry()
    groupEntry.memberId = 4
    groupEntry.memberName = "Mary2"
    groupMessage.GroupInfoEntries.Add(groupEntry)
    MessageDispatcher.Instance.QueueMessage(groupMessage)
                        

def InitializeInventory():
    invMessage = InventoryUpdateMessage()

    invEntry = InventoryUpdateEntry()
    invEntry.itemId = 100
    invEntry.containerId = 0
    invEntry.slotId = 0
    invEntry.name = "Long Sword"
    invEntry.icon = "Interface\Icons\INV_weapon_sword"
    invMessage.Inventory.Add(invEntry)
    
    invEntry = InventoryUpdateEntry()
    invEntry.itemId = 101
    invEntry.containerId = 0
    invEntry.slotId = 1
    invEntry.name = "Orc Sword"
    invEntry.icon = "Interface\Icons\INV_weapon_sword"
    invMessage.Inventory.Add(invEntry)
    
    invEntry = InventoryUpdateEntry()
    invEntry.itemId = 102
    invEntry.containerId = 0
    invEntry.slotId = 2
    invEntry.name = "Plate Armor"
    invEntry.icon = "Interface\Icons\INV_clothes_armor"
    invMessage.Inventory.Add(invEntry)
    
    invEntry = InventoryUpdateEntry()
    invEntry.itemId = 103
    invEntry.containerId = 0
    invEntry.slotId = 4
    invEntry.name = "Chain Armor"
    invEntry.icon = "Interface\Icons\INV_clothes_armor"
    invMessage.Inventory.Add(invEntry)
    
    invEntry = InventoryUpdateEntry()
    invEntry.itemId = 104
    invEntry.containerId = 0
    invEntry.slotId = 7
    invEntry.name = "Leather Armor"
    invEntry.icon = "Interface\Icons\INV_clothes_armor"
    invMessage.Inventory.Add(invEntry)

    MessageDispatcher.Instance.QueueMessage(invMessage)
    

def InitializePlayer():
    modelInfoMessage = OldModelInfoMessage()
    modelInfoMessage.Oid = 1
    human_model = False
    meshInfo = MeshInfo()
    if human_model:
        meshInfo.MeshFile = "human_male.mesh"
        meshInfo.SubmeshList = List[SubmeshInfo]()
        # body
        submeshInfo = SubmeshInfo()
        submeshInfo.SubmeshName = "bodyShape-lib.0"
        submeshInfo.MaterialName = "human_male.skin_material"
        meshInfo.SubmeshList.Add(submeshInfo)
        # head
        submeshInfo = SubmeshInfo()
        submeshInfo.SubmeshName = "head_aShape-lib.0"
        submeshInfo.MaterialName = "human_male.head_a_material"
        meshInfo.SubmeshList.Add(submeshInfo)
        # chest
        submeshInfo = SubmeshInfo()
        submeshInfo.SubmeshName = "cloth_a_shirtShape-lib.0"
        submeshInfo.MaterialName = "human_male.cloth_a_material"
        meshInfo.SubmeshList.Add(submeshInfo)
        # pants
        submeshInfo = SubmeshInfo()
        submeshInfo.SubmeshName = "cloth_a_pantsShape-lib.0"
        submeshInfo.MaterialName = "human_male.cloth_a_material"
        meshInfo.SubmeshList.Add(submeshInfo)
        # belt
        #meshInfo.SubmeshNames.Add("cloth_a_beltShape-lib.0")
        #meshInfo.MaterialNames.Add("human_male.cloth_a_material")
        # boots
        submeshInfo = SubmeshInfo()
        submeshInfo.SubmeshName = "cloth_a_bootsShape-lib.0"
        submeshInfo.MaterialName = "human_male.cloth_a_material"
        meshInfo.SubmeshList.Add(submeshInfo)
        # hair
        #meshInfo.SubmeshNames.Add("hair_aShape-lib.0")
        #meshInfo.MaterialNames.Add("human_male.hair_a_material")
        # apron
        #meshInfo.SubmeshNames.Add("cloth_a_apronShape-lib.0")
        #meshInfo.MaterialNames.Add("human_male.apron_a_material")
        # mustache
        #meshInfo.SubmeshNames.Add("facial_hair_aShape-lib.0")
        #meshInfo.MaterialNames.Add("human_male.facial_hair_a_material")
    else:
        meshInfo.MeshFile = "human_male.mesh"
        # meshInfo.MeshFile = "test8_14.mesh"
        # meshInfo.SubmeshList = List[SubmeshInfo]()
        # submeshInfo = SubmeshInfo()
        # submeshInfo.SubmeshName = "casual29_m_mediumpoly-obj.0";
        # meshInfo.MaterialNames.Add("Default");
        # submeshInfo.MaterialName = "test8_14.body"
        # meshInfo.SubmeshList.Add(submeshInfo);
    modelInfoMessage.ModelInfo.Add(meshInfo)
    MessageDispatcher.Instance.QueueMessage(modelInfoMessage)

    propMessage = ObjectPropertyMessage()
    propMessage.Oid = 1
    propMessage.Properties["health-max"] = 40
    propMessage.Properties["health"] = 30
    propMessage.Properties["mana-max"] = 50
    propMessage.Properties["mana"] = 30
    propMessage.Properties["str"] = 30
    propMessage.Properties["int"] = 30
    propMessage.Properties["dex"] = 30
    propMessage.Properties["combatstate"] = 1
    MessageDispatcher.Instance.QueueMessage(propMessage)
    
    attachMessage = AttachMessage()
    attachMessage.Oid = 1
    attachMessage.ObjectId = 10
    attachMessage.SlotName = "primaryWeapon"
    attachMessage.MeshFile = "axe.mesh"
    MessageDispatcher.Instance.QueueMessage(attachMessage)
    
    attachMessage = AttachMessage()
    attachMessage.Oid = 1
    attachMessage.ObjectId = 11
    attachMessage.SlotName = "shield"
    attachMessage.MeshFile = "shield.mesh"
    MessageDispatcher.Instance.QueueMessage(attachMessage)

    animEntry = AnimationEntry()
    animEntry.animationName = "idle"
    animEntry.animationSpeed = 1.0
    animEntry.loop = True
    animMessage = AnimationMessage()
    animMessage.Animations.Add(animEntry)
    animMessage.Oid = 1
    MessageDispatcher.Instance.QueueMessage(animMessage)

    InitializeInventory()
    InitializeGroup()
    InitializeQuestData()
    

def InitializeLucy():
    newObjMessage = NewObjectMessage()
    newObjMessage.Oid = 1
    newObjMessage.ObjectId = 66
    newObjMessage.Name = "Lucy"
    newObjMessage.Location = Vector3(129000, 0, 3643000)
    newObjMessage.Orientation = Quaternion.FromAngleAxis(PI * -0.75, Vector3.UnitY)
    newObjMessage.ScaleFactor = Vector3.UnitScale
    newObjMessage.ObjectType = ObjectNodeType.Npc
    newObjMessage.FollowTerrain = True
    MessageDispatcher.Instance.QueueMessage(newObjMessage)
    
    modelInfoMessage = ModelInfoMessage()
    modelInfoMessage.Oid = 66
    meshInfo = MeshInfo()
    meshInfo.MeshFile = "human_female.mesh"
    meshInfo.SubmeshList = List[SubmeshInfo]()
    # body
    submeshInfo = SubmeshInfo()
    submeshInfo.SubmeshName = "bodyShape-lib.0"
    submeshInfo.MaterialName = "human_female.skin_material"
    meshInfo.SubmeshList.Add(submeshInfo)
    # head
    submeshInfo = SubmeshInfo()
    submeshInfo.SubmeshName = "head_aShape-lib.0"
    submeshInfo.MaterialName = "human_female.head_a_material"
    meshInfo.SubmeshList.Add(submeshInfo)
    # hair
    #submeshInfo = SubmeshInfo()
    #submeshInfo.SubmeshName = "hair_bShape-lib.0"
    #submeshInfo.MaterialName = "human_female.hair_b_material"
    #meshInfo.SubmeshList.Add(submeshInfo)
    # helmet
    submeshInfo = SubmeshInfo()
    submeshInfo.SubmeshName = "plate_b_helmetShape-lib.0"
    submeshInfo.MaterialName = "human_female.plate_b_material"
    meshInfo.SubmeshList.Add(submeshInfo)
    # tunic
    submeshInfo = SubmeshInfo()
    #submeshInfo.SubmeshName = "leather_a_tunicShape-lib.0"
    #submeshInfo.MaterialName = "human_female.leather_a_material"
    submeshInfo.SubmeshName = "plate_b_tunicShape-lib.0"
    submeshInfo.MaterialName = "human_female.plate_b_material"
    meshInfo.SubmeshList.Add(submeshInfo)
    # pants
    submeshInfo = SubmeshInfo()
    submeshInfo.SubmeshName = "plate_b_pantsShape-lib.0"
    submeshInfo.MaterialName = "human_female.plate_b_material"
    meshInfo.SubmeshList.Add(submeshInfo)
    # belt
    #submeshInfo = SubmeshInfo()
    #submeshInfo.SubmeshName = "leather_a_beltShape-lib.0"
    #submeshInfo.MaterialName = "human_female.leather_a_material"
    #meshInfo.SubmeshList.Add(submeshInfo)
    # boots
    submeshInfo = SubmeshInfo()
    #submeshInfo.SubmeshName = "leather_a_bootsShape-lib.0"
    #submeshInfo.MaterialName = "human_female.leather_a_material"
    submeshInfo.SubmeshName = "plate_b_bootsShape-lib.0"
    submeshInfo.MaterialName = "human_female.plate_b_material"
    meshInfo.SubmeshList.Add(submeshInfo)
    # bracers
    submeshInfo = SubmeshInfo()
    #submeshInfo.SubmeshName = "leather_a_bracersShape-lib.0"
    #submeshInfo.MaterialName = "human_female.leather_a_material"
    submeshInfo.SubmeshName = "plate_b_glovesShape-lib.0"
    submeshInfo.MaterialName = "human_female.plate_b_material"
    meshInfo.SubmeshList.Add(submeshInfo)

    modelInfoMessage.ModelInfo.Add(meshInfo)
    MessageDispatcher.Instance.QueueMessage(modelInfoMessage)
    
    propMessage = ObjectPropertyMessage()
    propMessage.Oid = 66
    propMessage.Properties["health-max"] = 40
    propMessage.Properties["health"] = 30
    propMessage.Properties["mana-max"] = 50
    propMessage.Properties["mana"] = 30
    propMessage.Properties["questavailable"] = 1
    MessageDispatcher.Instance.QueueMessage(propMessage)

    attachMessage = AttachMessage()
    attachMessage.Oid = 66
    attachMessage.ObjectId = 12
    attachMessage.SlotName = "primaryWeapon"
    attachMessage.MeshFile = "pick.mesh"
    MessageDispatcher.Instance.QueueMessage(attachMessage)

    animEntry = AnimationEntry()
    animEntry.animationName = "idle"
    animEntry.animationSpeed = 1.0
    animEntry.loop = True
    animMessage = AnimationMessage()
    animMessage.Animations.Add(animEntry)
    animMessage.Oid = 66
    MessageDispatcher.Instance.QueueMessage(animMessage)


def InitializeAthene():
    newObjMessage = NewObjectMessage()
    newObjMessage.Oid = 1
    newObjMessage.ObjectId = 8
    newObjMessage.Name = "Orgrimmar Grunt"
    newObjMessage.Location = Vector3(120000, 95000, 3646000)
    newObjMessage.Orientation = Quaternion.FromAngleAxis(PI * 0.75, Vector3.UnitY)
    newObjMessage.ScaleFactor = Vector3(10, 10, 10)
    newObjMessage.ObjectType = ObjectNodeType.Npc
    newObjMessage.FollowTerrain = True
    MessageDispatcher.Instance.QueueMessage(newObjMessage)

    modelInfoMessage = ModelInfoMessage()
    modelInfoMessage.Oid = 8
    meshInfo = MeshInfo()
    meshInfo.MeshFile = "athene.mesh"
    meshInfo.SubmeshList = List[SubmeshInfo]()
    submeshInfo = SubmeshInfo()
    submeshInfo.SubmeshName = "athene.mesh_SubMesh0"
    # meshInfo.MaterialNames.Add("Examples/Athene/NormalMappedSpecular")
    submeshInfo.MaterialName = "Examples/Athene/Basic"
    meshInfo.SubmeshList.Add(submeshInfo)
    modelInfoMessage.ModelInfo.Add(meshInfo)
    MessageDispatcher.Instance.QueueMessage(modelInfoMessage)

    propMessage = ObjectPropertyMessage()
    propMessage.Oid = 8
    propMessage.Properties["health-max"] = 20
    propMessage.Properties["health"] = 20
    propMessage.Properties["mana-max"] = 30
    propMessage.Properties["mana"] = 30
    propMessage.Properties["lootable"] = 1
    propMessage.Properties["questavailable"] = 0
    MessageDispatcher.Instance.QueueMessage(propMessage)


def InitializeOrc():
    newObjMessage = NewObjectMessage()
    newObjMessage.Oid = 1
    newObjMessage.ObjectId = 2
    newObjMessage.Name = "Orgrimmar Grunt"
    newObjMessage.Location = Vector3(128000, 0, 3649000)
    newObjMessage.Orientation = Quaternion.FromAngleAxis(PI * 0.75, Vector3.UnitY)
    newObjMessage.ScaleFactor = Vector3.UnitScale
    newObjMessage.ObjectType = ObjectNodeType.Npc
    newObjMessage.FollowTerrain = True
    MessageDispatcher.Instance.QueueMessage(newObjMessage)

    modelInfoMessage = ModelInfoMessage()
    modelInfoMessage.Oid = 2
    meshInfo = MeshInfo()
    meshInfo.MeshFile = "orc.mesh"
    modelInfoMessage.ModelInfo.Add(meshInfo)
    MessageDispatcher.Instance.QueueMessage(modelInfoMessage)

    propMessage = ObjectPropertyMessage()
    propMessage.Oid = 2
    propMessage.Properties["health-max"] = 20
    propMessage.Properties["health"] = 20
    propMessage.Properties["mana-max"] = 30
    propMessage.Properties["mana"] = 30
    propMessage.Properties["lootable"] = 1
    propMessage.Properties["questavailable"] = 0
    MessageDispatcher.Instance.QueueMessage(propMessage)

    attachMessage = AttachMessage()
    attachMessage.Oid = 2
    attachMessage.ObjectId = 13
    attachMessage.SlotName = "primaryWeapon"
    attachMessage.MeshFile = "spear.mesh"
    MessageDispatcher.Instance.QueueMessage(attachMessage)

    animEntry = AnimationEntry()
    animEntry.animationName = "idle"
    animEntry.animationSpeed = 1.0
    animEntry.loop = True
    animMessage = AnimationMessage()
    animMessage.Animations.Add(animEntry)
    animMessage.Oid = 2
    MessageDispatcher.Instance.QueueMessage(animMessage)
        

def InitializeSaul():
    newObjMessage = NewObjectMessage()
    newObjMessage.Oid = 1
    newObjMessage.ObjectId = 3
    newObjMessage.Name = "Saul"
    newObjMessage.Location = Vector3(139000, 0, 3643000)
    newObjMessage.Orientation = Quaternion.FromAngleAxis(PI * -0.75, Vector3.UnitY)
    newObjMessage.ScaleFactor = Vector3.UnitScale
    newObjMessage.ObjectType = ObjectNodeType.Npc
    newObjMessage.FollowTerrain = True
    MessageDispatcher.Instance.QueueMessage(newObjMessage)
    
    modelInfoMessage = ModelInfoMessage()
    modelInfoMessage.Oid = 3
    meshInfo = MeshInfo()
    meshInfo.MeshFile = "human_male.mesh"
    meshInfo.SubmeshList = List[SubmeshInfo]()
    # body
    submeshInfo = SubmeshInfo()
    submeshInfo.SubmeshName = "bodyShape-lib.0"
    submeshInfo.MaterialName = "human_male.skin_material"
    meshInfo.SubmeshList.Add(submeshInfo)
    # head
    submeshInfo = SubmeshInfo()
    submeshInfo.SubmeshName = "head_dShape-lib.0"
    submeshInfo.MaterialName = "human_male.head_a_material"
    meshInfo.SubmeshList.Add(submeshInfo)
    # pants
    submeshInfo = SubmeshInfo()
    submeshInfo.SubmeshName = "plate_a_pantsShape-lib.0"
    submeshInfo.MaterialName = "human_male.plate_a_matte_material"
    meshInfo.SubmeshList.Add(submeshInfo)
    # chest
    submeshInfo = SubmeshInfo()
    submeshInfo.SubmeshName = "plate_a_armorShape-lib.0"
    submeshInfo.MaterialName = "human_male.plate_a_material"
    meshInfo.SubmeshList.Add(submeshInfo)
    # boots
    submeshInfo = SubmeshInfo()
    submeshInfo.SubmeshName = "plate_a_bootsShape-lib.0"
    submeshInfo.MaterialName = "human_male.plate_a_material"
    meshInfo.SubmeshList.Add(submeshInfo)
    # gloves
    submeshInfo = SubmeshInfo()
    submeshInfo.SubmeshName = "plate_a_glovesShape-lib.0"
    submeshInfo.MaterialName = "human_male.plate_a_material"
    meshInfo.SubmeshList.Add(submeshInfo)
    modelInfoMessage.ModelInfo.Add(meshInfo)
    MessageDispatcher.Instance.QueueMessage(modelInfoMessage)

    propMessage = ObjectPropertyMessage()
    propMessage.Oid = 3
    propMessage.Properties["health-max"] = 40
    propMessage.Properties["health"] = 30
    propMessage.Properties["mana-max"] = 50
    propMessage.Properties["mana"] = 30
    MessageDispatcher.Instance.QueueMessage(propMessage)

    attachMessage = AttachMessage()
    attachMessage.Oid = 3
    attachMessage.ObjectId = 14
    attachMessage.SlotName = "primaryWeapon"
    attachMessage.MeshFile = "sword.mesh"
    MessageDispatcher.Instance.QueueMessage(attachMessage)
    
    attachMessage = AttachMessage()
    attachMessage.Oid = 3
    attachMessage.ObjectId = 15
    attachMessage.SlotName = "secondaryWeapon"
    attachMessage.MeshFile = "dagger.mesh"
    MessageDispatcher.Instance.QueueMessage(attachMessage)

    animEntry = AnimationEntry()
    animEntry.animationName = "idle"
    animEntry.animationSpeed = 1.0
    animEntry.loop = True
    animMessage = AnimationMessage()
    animMessage.Animations.Add(animEntry)
    animMessage.Oid = 3
    MessageDispatcher.Instance.QueueMessage(animMessage)


def AddWorldObjects():
    newObjMessage = NewObjectMessage()
    newObjMessage.Oid = 1
    newObjMessage.ObjectId = 6
    newObjMessage.Name = "tower"
    newObjMessage.Location = Vector3(123000, 84000, 3654000)
    newObjMessage.Orientation = MathUtil.FromEulerAngles(102, 0, 0)
    newObjMessage.ScaleFactor = Vector3.UnitScale
    newObjMessage.ObjectType = ObjectNodeType.Prop
    newObjMessage.FollowTerrain = False
    MessageDispatcher.Instance.QueueMessage(newObjMessage)
    
    modelInfoMessage = ModelInfoMessage()
    modelInfoMessage.Oid = 6
    meshInfo = MeshInfo()
    meshInfo.MeshFile = "tower.mesh"
    modelInfoMessage.ModelInfo.Add(meshInfo)
    MessageDispatcher.Instance.QueueMessage(modelInfoMessage)
    
    newObjMessage = NewObjectMessage()
    newObjMessage.Oid = 1
    newObjMessage.ObjectId = 7
    newObjMessage.Name = "orc_house"
    newObjMessage.Location = Vector3(123000, 84000, 3649000)
    newObjMessage.Orientation = Quaternion.Identity
    newObjMessage.ScaleFactor = Vector3.UnitScale
    newObjMessage.ObjectType = ObjectNodeType.Prop
    newObjMessage.FollowTerrain = False
    MessageDispatcher.Instance.QueueMessage(newObjMessage)
    
    modelInfoMessage = ModelInfoMessage()
    modelInfoMessage.Oid = 7
    meshInfo = MeshInfo()
    meshInfo.MeshFile = "human_shack_tall.mesh"
    modelInfoMessage.ModelInfo.Add(meshInfo)
    MessageDispatcher.Instance.QueueMessage(modelInfoMessage)

    addParticleMessage = AddParticleEffectMessage()
    addParticleMessage.Oid = 7
    addParticleMessage.ObjectId = 100
    addParticleMessage.SlotName = "chimney"
    addParticleMessage.EffectName = "smoke"
    addParticleMessage.VelocityMultiplier = 10
    addParticleMessage.ParticleSizeMultiplier = 10
    MessageDispatcher.Instance.QueueMessage(addParticleMessage)

    soundEntry = PropertyMap()
    soundEntry.Properties["Gain"] = "0.5"
    soundEntry.Properties["Loop"] = "true"
    soundMessage = SoundControlMessage()
    soundMessage.Oid = 0
    soundMessage.NewSoundEntries["ambient.wav"] = soundEntry
    MessageDispatcher.Instance.QueueMessage(soundMessage)

    soundEntry = PropertyMap()
    soundEntry.Properties["Gain"] = "0.15"
    soundEntry.Properties["Loop"] = "false"
    soundMessage = SoundControlMessage()
    soundMessage.Oid = 1
    soundMessage.NewSoundEntries["ugh.wav"] = soundEntry
    MessageDispatcher.Instance.QueueMessage(soundMessage)


def SendTestComm():
    commMessage = CommMessage()
    commMessage.Oid = 1
    commMessage.ChannelId = 1
    commMessage.Message = "Hello World"
    MessageDispatcher.Instance.QueueMessage(commMessage)
    
    commMessage = CommMessage()
    commMessage.Oid = 2
    commMessage.ChannelId = 1
    commMessage.Message = "Howdy folks! This is a test of the system to see how it handles large text"
    MessageDispatcher.Instance.QueueMessage(commMessage)

    
def SendTestExtension():
    extMessage = ExtensionMessage()
    extMessage.Oid = 1
    extMessage.Properties["sample_extension"] = "sample message"
    extMessage.Properties["sample_extension_channel"] = 5
    MessageDispatcher.Instance.QueueMessage(extMessage)

def SendLoadingStateMessage():
    loadingStateMessage = LoadingStateMessage()
    loadingStateMessage.LoadingState = False
    MessageDispatcher.Instance.QueueMessage(loadingStateMessage)
    
def InitializeSound():
    ambientSoundMessage = AmbientSoundMessage()
    ambientSoundMessage.Oid = 0
    ambientSoundMessage.Sound = "ambient_hills_day.ogg"
    ambientSoundMessage.Active = True
    # MessageDispatcher.Instance.QueueMessage(ambientSoundMessage)

def InitializeVegetation():
    grassInitString = "<boundaries><boundary><name>boundary8</name><points><point x=\"285000\" y=\"3462000\" /><point x=\"-679000\" y=\"3560000\" /><point x=\"-647000\" y=\"3381000\" /><point x=\"-512000\" y=\"3230000\" /><point x=\"402000\" y=\"3116000\" /><point x=\"402000\" y=\"3339000\" /><point x=\"305000\" y=\"3363000\" /></points><boundarySemantic type=\"Vegetation\"><name>Grass7</name><PlantType numInstances=\"500\" imageName=\"rose\" scaleWidthLow=\"1600\" scaleWidthHi=\"2400\" scaleHeightLow=\"800\" scaleHeightHi=\"1200\" colorMultLow=\".8\" colorMultHi=\"1\" windMagnitude=\"50\"><color r=\"0.418\" g=\"0.535\" b=\"0.277\"/></PlantType><PlantType numInstances=\"500\" imageName=\"cattail\" scaleWidthLow=\"800\" scaleWidthHi=\"1200\" scaleHeightLow=\"1400\" scaleHeightHi=\"1700\" colorMultLow=\".8\" colorMultHi=\"1\" windMagnitude=\"100\"><color r=\"0.96\" g=\"0.87\" b=\"0.5\"/></PlantType></boundarySemantic></boundary></boundaries>"
    regionConfigMessage = RegionConfigMessage()
    regionConfigMessage.ConfigString = grassInitString
    MessageDispatcher.Instance.QueueMessage(regionConfigMessage)
    
InitStandaloneWorld()
tmp = "print \"this is a test\"\nprint \"this is another test\""
