#
# WARNING - this script is auto-generated from a world file.  Edit at your own risk
#
import ClientAPI

TerrainString = "<Terrain><algorithm>HybridMultifractalWithFloor</algorithm><xOffset>0</xOffset><yOffset>0</yOffset><zOffset>0</zOffset><h>0.25</h><lacunarity>2</lacunarity><octaves>8</octaves><metersPerPerlinUnit>500</metersPerPerlinUnit><heightScale>0</heightScale><heightOffset>0</heightOffset><fractalOffset>0.7</fractalOffset><heightFloor>20</heightFloor></Terrain><TerrainDisplay RockToSnowHeight=\"450000\" SandToGrassHeight=\"50000\" RockTextureName=\"splatting_rock.dds\" GrassTextureName=\"splatting_grass.dds\" TextureTileSize=\"5\" SandTextureName=\"splatting_sand.dds\" ShadeMaskTextureName=\"\" GrassToRockHeight=\"250000\" SnowTextureName=\"splatting_snow.dds\" UseParams=\"True\" Type=\"AutoSplat\" UseGeneratedShadeMask=\"True\" />"

StaticObjects = {}

Markers = {}

Regions = {}

#
# Markers
#
Markers["spawnPt"] = (ClientAPI.Vector3(101840,20010,-372265), ClientAPI.Quaternion(0.9437235,0,0.3307356,0), {  })
Markers["stuck"] = (ClientAPI.Vector3(101840,20010,-372265), ClientAPI.Quaternion(0.9437235,0,0.3307356,0), {  })
Markers["MobPt0"] = (ClientAPI.Vector3(137512.8,20100,-375226.4), ClientAPI.Quaternion(1,0,0,0), {  })
Markers["MobPt1"] = (ClientAPI.Vector3(104798.2,20000,-374829.5), ClientAPI.Quaternion(1,0,0,0), {  })
Markers["MobPt2"] = (ClientAPI.Vector3(100518.7,20100,-357829.5), ClientAPI.Quaternion(1,0,0,0), {  })
Markers["MobPt3"] = (ClientAPI.Vector3(123120.3,20100,-357300.2), ClientAPI.Quaternion(1,0,0,0), {  })
Markers["MobPt4"] = (ClientAPI.Vector3(139200.5,20100,-357453.3), ClientAPI.Quaternion(1,0,0,0), {  })
Markers["MobPt5"] = (ClientAPI.Vector3(150650,20132.35,-295426.3), ClientAPI.Quaternion(1,0,0,0), {  })
Markers["MobPt6"] = (ClientAPI.Vector3(132157.4,20100,-295770.2), ClientAPI.Quaternion(1,0,0,0), {  })
Markers["MobPt7"] = (ClientAPI.Vector3(120740.9,20100,-295019.7), ClientAPI.Quaternion(1,0,0,0), {  })
Markers["MobPt8"] = (ClientAPI.Vector3(102575.3,20100,-295452.4), ClientAPI.Quaternion(1,0,0,0), {  })
Markers["steam_45Broadway_01"] = (ClientAPI.Vector3(97991.54,19500,-444561.2), ClientAPI.Quaternion(1,0,0,0), {  })
Markers["steam_45Broadway_02"] = (ClientAPI.Vector3(128780.9,19500,-447079.8), ClientAPI.Quaternion(1,0,0,0), {  })
Markers["steam_TS_01"] = (ClientAPI.Vector3(124508.6,19500,-391044.6), ClientAPI.Quaternion(1,0,0,0), {  })
Markers["steam_TS_02"] = (ClientAPI.Vector3(108187,19500,-373505.1), ClientAPI.Quaternion(1,0,0,0), {  })
Markers["steam_44TS_03"] = (ClientAPI.Vector3(139611.2,19500,-367009.3), ClientAPI.Quaternion(1,0,0,0), {  })
Markers["steam_Broadway_03"] = (ClientAPI.Vector3(107259,19500,-353918), ClientAPI.Quaternion(1,0,0,0), {  })
Markers["steam_TS_03"] = (ClientAPI.Vector3(139425.3,19500,-306997.6), ClientAPI.Quaternion(1,0,0,0), {  })
Markers["steam_TS_04"] = (ClientAPI.Vector3(137441.1,19500,-305997.6), ClientAPI.Quaternion(1,0,0,0), {  })
Markers["steam_Broadway_04"] = (ClientAPI.Vector3(107551.7,19500,-302309.7), ClientAPI.Quaternion(1,0,0,0), {  })
Markers["steam_Broadway_05"] = (ClientAPI.Vector3(114322.7,19500,-300009.7), ClientAPI.Quaternion(1,0,0,0), {  })
Markers["steam_Broadway_06"] = (ClientAPI.Vector3(114008.2,19500,-274309.7), ClientAPI.Quaternion(1,0,0,0), {  })
Markers["steam_43TS_04"] = (ClientAPI.Vector3(156000,19500,-285612.3), ClientAPI.Quaternion(1,0,0,0), {  })
Markers["steam_army_01"] = (ClientAPI.Vector3(124140.4,19000,-326159.6), ClientAPI.Quaternion(1,0,0,0), {  })
Markers["steam_army_02"] = (ClientAPI.Vector3(124686.4,19000,-324136.6), ClientAPI.Quaternion(0.7071068,0,0.7071068,0), {  })
Markers["steam_army_03"] = (ClientAPI.Vector3(124669.1,19000,-321089.9), ClientAPI.Quaternion(1,0,0,0), {  })
Markers["steam_popo_01"] = (ClientAPI.Vector3(125648,19000,-278909.5), ClientAPI.Quaternion(1,0,0,0), {  })
Markers["steam_sweetSpot_01"] = (ClientAPI.Vector3(121652.1,19000,-376033), ClientAPI.Quaternion(1,0,0,0), {  })
Markers["steam_sweetSpot_02"] = (ClientAPI.Vector3(121667.9,19000,-378376.6), ClientAPI.Quaternion(1,0,0,0), {  })
Markers["steam_43TS_05"] = (ClientAPI.Vector3(144922.9,19500,-251988.7), ClientAPI.Quaternion(1,0,0,0), {  })
Markers["steam_42Broadway_07"] = (ClientAPI.Vector3(116908,19500,-216208.6), ClientAPI.Quaternion(1,0,0,0), {  })
Markers["steam_ParaDog_01"] = (ClientAPI.Vector3(102035.5,20900,-349858), ClientAPI.Quaternion(1,0,0,0), {  })
Markers["camerapath0"] = (ClientAPI.Vector3(110513.5,29817.18,-470823), ClientAPI.Quaternion(0.05229665,-0.002025033,-0.9978818,-0.03863947), { "Path" : "camerapath","PathTime" : "0","PathOffset" : "0", })
Markers["camerapath1"] = (ClientAPI.Vector3(112847.1,41731.2,-437450.5), ClientAPI.Quaternion(0.02599713,-0.003062026,-0.9927948,-0.1169335), { "Path" : "camerapath","PathTime" : "2","PathOffset" : "1", })
Markers["camerapath2"] = (ClientAPI.Vector3(115586.8,50576.53,-398270.5), ClientAPI.Quaternion(0.06912452,-0.009367488,-0.9885285,-0.1339612), { "Path" : "camerapath","PathTime" : "4","PathOffset" : "2", })
Markers["camerapath3"] = (ClientAPI.Vector3(121860.5,67304.34,-340883.8), ClientAPI.Quaternion(0.03806974,-0.02129171,-0.8719426,-0.4876612), { "Path" : "camerapath","PathTime" : "6","PathOffset" : "3", })
Markers["camerapath4"] = (ClientAPI.Vector3(124899.6,69677.13,-316086.9), ClientAPI.Quaternion(0.02664913,-0.02253422,-0.763134,-0.6452974), { "Path" : "camerapath","PathTime" : "8","PathOffset" : "4", })
Markers["camerapath5"] = (ClientAPI.Vector3(125996.5,38205.07,-301262.3), ClientAPI.Quaternion(-0.03465986,0.004082317,0.9925301,0.1169024), { "Path" : "camerapath","PathTime" : "10","PathOffset" : "5", })
Markers["camerapath6"] = (ClientAPI.Vector3(125996.5,38205.07,-301262.3), ClientAPI.Quaternion(-0.7219838,0.2875674,0.5846512,0.2328676), { "Path" : "camerapath","PathTime" : "12","PathOffset" : "6", })
Markers["camerapath7"] = (ClientAPI.Vector3(125996.5,38205.07,-301262.3), ClientAPI.Quaternion(-0.975319,0.2201103,-0.01702399,-0.003842028), { "Path" : "camerapath","PathTime" : "14","PathOffset" : "7", })
Markers["mobpath1-0"] = (ClientAPI.Vector3(75177.55,20116.71,-439857.1), ClientAPI.Quaternion(1,0,0,0), { "Path" : "mobpath1","PathOffset" : "0", })
Markers["mobpath1-1"] = (ClientAPI.Vector3(93119.31,20116.71,-439821.6), ClientAPI.Quaternion(1,0,0,0), { "Path" : "mobpath1","PathOffset" : "1", })
Markers["mobpath1-2"] = (ClientAPI.Vector3(100463.8,20116.71,-432000.8), ClientAPI.Quaternion(1,0,0,0), { "Path" : "mobpath1","PathOffset" : "2", })
Markers["mobpath1-3"] = (ClientAPI.Vector3(99657.05,20116.71,-423016.5), ClientAPI.Quaternion(1,0,0,0), { "Path" : "mobpath1","PathOffset" : "3", })
Markers["mobpath1-4"] = (ClientAPI.Vector3(101633.2,20216.86,-372983.1), ClientAPI.Quaternion(1,0,0,0), { "Path" : "mobpath1","PathOffset" : "4", })
Markers["mobpath1-5"] = (ClientAPI.Vector3(122184.3,20114.39,-372562.1), ClientAPI.Quaternion(1,0,0,0), { "Path" : "mobpath1","PathOffset" : "5", })
Markers["mobpath1-6"] = (ClientAPI.Vector3(137622.5,20119.35,-371508.5), ClientAPI.Quaternion(1,0,0,0), { "Path" : "mobpath1","PathOffset" : "6", })
Markers["mobpath1-7"] = (ClientAPI.Vector3(139916.2,20189.46,-358866.4), ClientAPI.Quaternion(1,0,0,0), { "Path" : "mobpath1","PathOffset" : "7", })
Markers["mobpath1-8"] = (ClientAPI.Vector3(151761.1,20234.12,-296023.8), ClientAPI.Quaternion(1,0,0,0), { "Path" : "mobpath1","PathOffset" : "8", })
Markers["mobpath1-9"] = (ClientAPI.Vector3(158317.1,20117.04,-292443.4), ClientAPI.Quaternion(1,0,0,0), { "Path" : "mobpath1","PathOffset" : "9", })
Markers["mobpath1-10"] = (ClientAPI.Vector3(186735.6,20000,-293483.5), ClientAPI.Quaternion(1,0,0,0), { "Path" : "mobpath1","PathOffset" : "10", })
Markers["panoramacam"] = (ClientAPI.Vector3(101521.4,30351.68,-365207.2), ClientAPI.Quaternion(0.7545935,0.01320904,-0.6559591,0.01148259), {  })
Markers["panoramacam2"] = (ClientAPI.Vector3(108719,30841.93,-365727.7), ClientAPI.Quaternion(0.7309089,-0.02548748,-0.6815848,-0.02376737), {  })
Markers["crowdSceneSpawn"] = (ClientAPI.Vector3(116585.1,20000,-315030.4), ClientAPI.Quaternion(-4.371139E-08,0,1,0), {  })

#
# Marker attached particle systems
#
markerParticles = [
 ("steam_45Broadway_01", "nyts_smoke", 2, 1),
 ("steam_45Broadway_02", "nyts_smoke", 2, 1),
 ("steam_TS_01", "nyts_smoke", 1, 1),
 ("steam_TS_02", "nyts_smoke", 1, 1),
 ("steam_44TS_03", "nyts_smoke", 2, 1),
 ("steam_Broadway_03", "nyts_smoke", 1, 1),
 ("steam_TS_03", "nyts_smoke", 1, 1),
 ("steam_TS_04", "nyts_smoke", 2, 1),
 ("steam_Broadway_04", "nyts_smoke", 1, 1),
 ("steam_Broadway_05", "nyts_smoke", 2, 1),
 ("steam_Broadway_06", "nyts_smoke", 1, 1),
 ("steam_43TS_04", "nyts_smoke", 2, 1),
 ("steam_army_01", "nyts_smoke", 1, 1.5),
 ("steam_army_02", "nyts_smoke", 3, 1.5),
 ("steam_army_03", "nyts_smoke", 2, 3),
 ("steam_popo_01", "nyts_smoke", 2, 2.5),
 ("steam_sweetSpot_01", "nyts_smoke", 2, 2.5),
 ("steam_sweetSpot_02", "nyts_smoke", 2, 1.5),
 ("steam_43TS_05", "nyts_smoke", 2, 1),
 ("steam_42Broadway_07", "nyts_smoke", 3, 1),
 ("steam_ParaDog_01", "nyts_smoke", 1, 1),
 ]

#
# Regions
#
Regions["dancespawn"] = [ClientAPI.Vector3(144332.8,20000,-315752.9), ClientAPI.Vector3(101613.3,20000,-314752.9), ClientAPI.Vector3(100952.4,20000,-353219.3), ClientAPI.Vector3(141179.4,20000,-354752.9), ]

#
# Object attached particle systems
#
objectParticles = [
 ("streetProps", "nyts_street_light", 1, 1, "streetLight_01"),
 ("streetProps", "nyts_street_light", 1, 1, "streetLight_02"),
 ("streetProps", "nyts_street_light", 1, 1, "streetLight_03"),
 ("streetProps", "nyts_street_light", 1, 1, "streetLight_04"),
 ("streetProps", "nyts_street_light", 1, 1, "streetLight_05"),
 ("streetProps", "nyts_street_light", 1, 1, "streetLight_06"),
 ("streetProps", "nyts_street_light", 1, 1, "streetLight_07"),
 ("streetProps", "nyts_street_light", 1, 1, "streetLight_08"),
 ("streetProps", "nyts_street_light", 1, 1, "streetLight_09"),
 ("streetProps", "nyts_street_light", 1, 1, "streetLight_10"),
 ("streetProps", "nyts_street_light", 1, 1, "streetLight_11"),
 ("streetProps", "nyts_street_light", 1, 1, "streetLight_12"),
 ("streetProps", "nyts_street_light", 1, 1, "streetLight_13"),
 ("streetProps", "nyts_street_light", 1, 1, "streetLight_14"),
 ("streetProps", "nyts_street_light", 1, 1, "streetLight_15"),
 ("streetProps", "nyts_street_light", 1, 1, "streetLight_16"),
 ("streetProps", "nyts_street_light", 1, 1, "streetLight_17"),
 ("streetProps", "nyts_street_light", 1, 1, "streetLight_18"),
 ("streetProps", "nyts_street_light", 1, 1, "streetLight_19"),
 ("streetProps", "nyts_street_light", 1, 1, "streetLight_20"),
 ("streetProps", "nyts_street_light", 1, 1, "streetLight_21"),
 ("streetProps", "nyts_street_light", 1, 1, "streetLight_22"),
 ("streetProps", "nyts_street_light", 1, 1, "streetLight_23"),
 ("streetProps", "nyts_street_light", 1, 1, "streetLight_24"),
 ("streetProps", "nyts_street_light", 1, 1, "streetLight_25"),
 ("streetProps", "nyts_street_light", 1, 1, "streetLight_26"),
 ("streetProps", "nyts_street_light", 1, 1, "streetLight_27"),
 ("streetProps", "nyts_street_light", 1, 1, "streetLight_28"),
 ("streetProps", "nyts_street_light", 1, 1, "streetLight_29"),
 ("streetProps", "nyts_street_light", 1, 1, "streetLight_30"),
 ("streetProps", "nyts_street_light", 1, 1, "streetLight_31"),
 ("streetProps", "nyts_street_light", 1, 1, "streetLight_32"),
 ]

def SetupWorld():
    #
    # Skybox
    #
    ClientAPI.SetSkyBox("eve_skybox")
    #
    # Global Fog
    #
    ClientAPI.FogConfig.FogColor = ClientAPI.ColorEx(0.0627451,0.05882353,0.08235294)
    ClientAPI.FogConfig.FogNear = 50000
    ClientAPI.FogConfig.FogFar = 200000
    #
    # Global Ambient Light
    #
    ClientAPI.AmbientLight.Color = ClientAPI.ColorEx(0.1333333,0.145098,0.1921569)
    #
    # Global Directional Light
    #
    globalDirLight = ClientAPI.Light.Light("globalDirLight")
    globalDirLight.Type = ClientAPI.Light.LightType.Directional
    globalDirLight.Direction = ClientAPI.Vector3(-0.01074477, -0.7880108, -0.6155677)
    globalDirLight.Diffuse = ClientAPI.ColorEx(0.254902, 0.2117647, 0.3607843)
    globalDirLight.Specular = ClientAPI.ColorEx(0.7372549, 0.7843137, 0.854902)

def SetupCamera():
    #
    # Camera
    #
    camera = ClientAPI.GetPlayerCamera()
    camera.Position = ClientAPI.Vector3(114777.2, 22755.02, -310446.4)
    camera.Orientation = ClientAPI.Quaternion(0.9860201, -0.1297622, -0.1036356, -0.0136386)

def SetupObjects():
    #
    # Static Objects
    #
    obj = ClientAPI.WorldObject.WorldObject(ClientAPI.GetLocalOID(), "times square streets", "nyts_streets.mesh", ClientAPI.Vector3(127105.6,20000,-319948.4), False, ClientAPI.Quaternion(1,0,0,0), ClientAPI.Vector3(1,1,1))
    StaticObjects["times square streets"] = obj
    obj = ClientAPI.WorldObject.WorldObject(ClientAPI.GetLocalOID(), "oneTimesSquare", "nyts_oneTimesSquare.mesh", ClientAPI.Vector3(133605.5,20000,-234915.4), False, ClientAPI.Quaternion(1,0,0,0), ClientAPI.Vector3(1,1,1))
    StaticObjects["oneTimesSquare"] = obj
    obj = ClientAPI.WorldObject.WorldObject(ClientAPI.GetLocalOID(), "condeNast", "nyts_condeNast.mesh", ClientAPI.Vector3(193788.6,20100,-245018.5), False, ClientAPI.Quaternion(1,0,0,0), ClientAPI.Vector3(1,1,1))
    StaticObjects["condeNast"] = obj
    obj = ClientAPI.WorldObject.WorldObject(ClientAPI.GetLocalOID(), "reuters", "nyts_reuters.mesh", ClientAPI.Vector3(71123.63,19900,-250289), False, ClientAPI.Quaternion(1,0,0,0), ClientAPI.Vector3(1,1,1))
    StaticObjects["reuters"] = obj
    obj = ClientAPI.WorldObject.WorldObject(ClientAPI.GetLocalOID(), "paramount", "nyts_paramount.mesh", ClientAPI.Vector3(73259.94,20092,-325948), False, ClientAPI.Quaternion(1,0,0,0), ClientAPI.Vector3(1.01,1.01,1.01))
    StaticObjects["paramount"] = obj
    obj = ClientAPI.WorldObject.WorldObject(ClientAPI.GetLocalOID(), "viacom", "nyts_viacom.mesh", ClientAPI.Vector3(46859.25,20000,-405389.6), False, ClientAPI.Quaternion(1,0,0,0), ClientAPI.Vector3(1,1,1))
    StaticObjects["viacom"] = obj
    obj = ClientAPI.WorldObject.WorldObject(ClientAPI.GetLocalOID(), "edelmann", "nyts_edelmann.mesh", ClientAPI.Vector3(173786.1,20091,-325880.3), False, ClientAPI.Quaternion(1,0,0,0), ClientAPI.Vector3(1,1,1))
    StaticObjects["edelmann"] = obj
    obj = ClientAPI.WorldObject.WorldObject(ClientAPI.GetLocalOID(), "milleniumBroadway", "nyts_milleniumBroadway.mesh", ClientAPI.Vector3(187747.8,20000,-405411.6), False, ClientAPI.Quaternion(1,0,0,0), ClientAPI.Vector3(1.03,1.03,1.03))
    StaticObjects["milleniumBroadway"] = obj
    obj = ClientAPI.WorldObject.WorldObject(ClientAPI.GetLocalOID(), "knickerbocker", "nyts_knickerbocker.mesh", ClientAPI.Vector3(197714,20000,-161173.8), False, ClientAPI.Quaternion(1,0,0,0), ClientAPI.Vector3(1,1,1))
    StaticObjects["knickerbocker"] = obj
    obj = ClientAPI.WorldObject.WorldObject(ClientAPI.GetLocalOID(), "timesSquareTower", "nyts_timesSquareTower.mesh", ClientAPI.Vector3(148463.6,20000,-158562.4), False, ClientAPI.Quaternion(1,0,0,0), ClientAPI.Vector3(1,1,1))
    StaticObjects["timesSquareTower"] = obj
    obj = ClientAPI.WorldObject.WorldObject(ClientAPI.GetLocalOID(), "ernstYoung", "nyts_ernstYoung.mesh", ClientAPI.Vector3(79774.96,20000,-155785.8), False, ClientAPI.Quaternion(1,0,0,0), ClientAPI.Vector3(1,1,1))
    StaticObjects["ernstYoung"] = obj
    obj = ClientAPI.WorldObject.WorldObject(ClientAPI.GetLocalOID(), "bertlesmann", "nyts_bertlesmann.mesh", ClientAPI.Vector3(168400.8,20000,-486060.3), False, ClientAPI.Quaternion(1,0,0,0), ClientAPI.Vector3(1,1,1))
    StaticObjects["bertlesmann"] = obj
    obj = ClientAPI.WorldObject.WorldObject(ClientAPI.GetLocalOID(), "marriot", "nyts_marriot.mesh", ClientAPI.Vector3(32721.38,20000,-486471.8), False, ClientAPI.Quaternion(1,0,0,0), ClientAPI.Vector3(1,1,1))
    StaticObjects["marriot"] = obj
    obj = ClientAPI.WorldObject.WorldObject(ClientAPI.GetLocalOID(), "times square streets2", "nyts_streets.mesh", ClientAPI.Vector3(99754.5,20000,-571698), False, ClientAPI.Quaternion(-4.371139E-08,0,-1,0), ClientAPI.Vector3(1,1,1))
    StaticObjects["times square streets2"] = obj
    obj = ClientAPI.WorldObject.WorldObject(ClientAPI.GetLocalOID(), "streets_2Lane_01", "nyts_streets_2Lane.mesh", ClientAPI.Vector3(207368.8,20080,-445824.1), False, ClientAPI.Quaternion(1,0,0,0), ClientAPI.Vector3(1,1,1))
    StaticObjects["streets_2Lane_01"] = obj
    obj = ClientAPI.WorldObject.WorldObject(ClientAPI.GetLocalOID(), "streets_2Lane_02", "nyts_streets_2Lane.mesh", ClientAPI.Vector3(19492.97,20080,-445826.3), False, ClientAPI.Quaternion(-4.371139E-08,0,1,0), ClientAPI.Vector3(1,1,1))
    StaticObjects["streets_2Lane_02"] = obj
    obj = ClientAPI.WorldObject.WorldObject(ClientAPI.GetLocalOID(), "streets_2Lane_03", "nyts_streets_2Lane.mesh", ClientAPI.Vector3(-565.83,20080,-365486.5), False, ClientAPI.Quaternion(-4.371139E-08,0,1,0), ClientAPI.Vector3(1,1,1))
    StaticObjects["streets_2Lane_03"] = obj
    obj = ClientAPI.WorldObject.WorldObject(ClientAPI.GetLocalOID(), "streets_2Lane_04", "nyts_streets_2Lane.mesh", ClientAPI.Vector3(240997.2,20080,-365483.2), False, ClientAPI.Quaternion(1,0,0,0), ClientAPI.Vector3(1,1,1))
    StaticObjects["streets_2Lane_04"] = obj
    obj = ClientAPI.WorldObject.WorldObject(ClientAPI.GetLocalOID(), "streets_2Lane_05", "nyts_streets_2Lane.mesh", ClientAPI.Vector3(254863.8,20080,-285976.7), False, ClientAPI.Quaternion(1,0,0,0), ClientAPI.Vector3(1,1,1))
    StaticObjects["streets_2Lane_05"] = obj
    obj = ClientAPI.WorldObject.WorldObject(ClientAPI.GetLocalOID(), "streets_2Lane_06", "nyts_streets_2Lane.mesh", ClientAPI.Vector3(-607.05,20080,-286301), False, ClientAPI.Quaternion(-4.371139E-08,0,1,0), ClientAPI.Vector3(1,1,1))
    StaticObjects["streets_2Lane_06"] = obj
    obj = ClientAPI.WorldObject.WorldObject(ClientAPI.GetLocalOID(), "streets_4Lane_01", "nyts_streets_4Lane.mesh", ClientAPI.Vector3(112404.7,20080,-154670), False, ClientAPI.Quaternion(0.7071068,0,-0.7071068,0), ClientAPI.Vector3(1,1,1))
    StaticObjects["streets_4Lane_01"] = obj
    obj = ClientAPI.WorldObject.WorldObject(ClientAPI.GetLocalOID(), "streets_4Lane_02", "nyts_streets_4Lane.mesh", ClientAPI.Vector3(63390.92,20080,-200153.2), False, ClientAPI.Quaternion(-4.371139E-08,0,1,0), ClientAPI.Vector3(1,1,1))
    StaticObjects["streets_4Lane_02"] = obj
    obj = ClientAPI.WorldObject.WorldObject(ClientAPI.GetLocalOID(), "streets_4Lane_03", "nyts_streets_4Lane.mesh", ClientAPI.Vector3(214604.1,20080,-199547.1), False, ClientAPI.Quaternion(1,0,0,0), ClientAPI.Vector3(1,1,1))
    StaticObjects["streets_4Lane_03"] = obj
    obj = ClientAPI.WorldObject.WorldObject(ClientAPI.GetLocalOID(), "streets_4Lane_04", "nyts_streets_4Lane.mesh", ClientAPI.Vector3(176688.6,20060,-153078.1), False, ClientAPI.Quaternion(0.7660444,0,-0.6427876,0), ClientAPI.Vector3(1,1,1))
    StaticObjects["streets_4Lane_04"] = obj
    obj = ClientAPI.WorldObject.WorldObject(ClientAPI.GetLocalOID(), "police", "nyts_police.mesh", ClientAPI.Vector3(128560.5,20170,-265015.4), False, ClientAPI.Quaternion(-4.371139E-08,0,1,0), ClientAPI.Vector3(1,1,1))
    StaticObjects["police"] = obj
    obj = ClientAPI.WorldObject.WorldObject(ClientAPI.GetLocalOID(), "army", "nyts_army.mesh", ClientAPI.Vector3(124738.3,20420,-304349.5), False, ClientAPI.Quaternion(1,0,0,0), ClientAPI.Vector3(1,1,1))
    StaticObjects["army"] = obj
    obj = ClientAPI.WorldObject.WorldObject(ClientAPI.GetLocalOID(), "skylineNear_01", "nyts_skylineNear.mesh", ClientAPI.Vector3(225365.1,20000,-325484.8), False, ClientAPI.Quaternion(0.7071068,0,0.7071068,0), ClientAPI.Vector3(0.9,0.9,0.9))
    StaticObjects["skylineNear_01"] = obj
    obj = ClientAPI.WorldObject.WorldObject(ClientAPI.GetLocalOID(), "skylineNear_02", "nyts_skylineNear.mesh", ClientAPI.Vector3(280839.6,20000,-245563.1), False, ClientAPI.Quaternion(0.7071068,0,-0.7071068,0), ClientAPI.Vector3(0.9,0.9,0.9))
    StaticObjects["skylineNear_02"] = obj
    obj = ClientAPI.WorldObject.WorldObject(ClientAPI.GetLocalOID(), "skylineNear_03", "nyts_skylineNear.mesh", ClientAPI.Vector3(-23069.2,20000,-249501.6), False, ClientAPI.Quaternion(0.7071068,0,0.7071068,0), ClientAPI.Vector3(0.8,0.8,0.8))
    StaticObjects["skylineNear_03"] = obj
    obj = ClientAPI.WorldObject.WorldObject(ClientAPI.GetLocalOID(), "skylineNear_04", "nyts_skylineNear.mesh", ClientAPI.Vector3(-47072.68,20000,-406329.8), False, ClientAPI.Quaternion(1,0,0,0), ClientAPI.Vector3(0.8,0.8,0.8))
    StaticObjects["skylineNear_04"] = obj
    obj = ClientAPI.WorldObject.WorldObject(ClientAPI.GetLocalOID(), "skylineFar_01", "nyts_skylineFar.mesh", ClientAPI.Vector3(-180273.1,20000,-316887), False, ClientAPI.Quaternion(1,0,0,0), ClientAPI.Vector3(1,1,1))
    StaticObjects["skylineFar_01"] = obj
    obj = ClientAPI.WorldObject.WorldObject(ClientAPI.GetLocalOID(), "skylineFar_02", "nyts_skylineFar.mesh", ClientAPI.Vector3(407511.5,20000,-309208.5), False, ClientAPI.Quaternion(-4.371139E-08,0,1,0), ClientAPI.Vector3(1,1,1))
    StaticObjects["skylineFar_02"] = obj
    obj = ClientAPI.WorldObject.WorldObject(ClientAPI.GetLocalOID(), "skylineFar_04", "nyts_skylineFar.mesh", ClientAPI.Vector3(167636.5,20000,14906.69), False, ClientAPI.Quaternion(0.7071068,0,0.7071068,0), ClientAPI.Vector3(1,1,1))
    StaticObjects["skylineFar_04"] = obj
    obj = ClientAPI.WorldObject.WorldObject(ClientAPI.GetLocalOID(), "skylineFar_05", "nyts_skylineFar.mesh", ClientAPI.Vector3(78276.93,20000,-778467.9), False, ClientAPI.Quaternion(-4.371139E-08,0,-1,0), ClientAPI.Vector3(1,1,1))
    StaticObjects["skylineFar_05"] = obj
    obj = ClientAPI.WorldObject.WorldObject(ClientAPI.GetLocalOID(), "skylineNear_05", "nyts_skylineNear.mesh", ClientAPI.Vector3(-24616.15,20000,-325521.6), False, ClientAPI.Quaternion(0.7071068,0,-0.7071068,0), ClientAPI.Vector3(0.85,0.85,0.85))
    StaticObjects["skylineNear_05"] = obj
    obj = ClientAPI.WorldObject.WorldObject(ClientAPI.GetLocalOID(), "skylineNear_06", "nyts_skylineNear.mesh", ClientAPI.Vector3(248549.1,19700,-487785.1), False, ClientAPI.Quaternion(1,0,0,0), ClientAPI.Vector3(0.85,0.85,0.85))
    StaticObjects["skylineNear_06"] = obj
    obj = ClientAPI.WorldObject.WorldObject(ClientAPI.GetLocalOID(), "streetProps", "nyts_props.mesh", ClientAPI.Vector3(127070.5,20005,-320026), False, ClientAPI.Quaternion(1,0,0,0), ClientAPI.Vector3(1,1,1))
    StaticObjects["streetProps"] = obj
