import ClientAPI
import Voice
import MarsGroup

enableVoice = False
enableInput = False

inputDeviceCache = None
outputDeviceCache = None

pttState = False
pttLocked = True
pttLockState = True

import Multiverse.Base
_worldManager = Multiverse.Base.Client.Instance.WorldManager

configMap = {
    "connect_to_server" : False,
    "default_volume" : 1.0,
    "agc_level" : 10,
    "mic_device_number" : 0,
    "playback_device_number" : 0,
    "listen_to_yourself" : False,
    "player_oid" : None,
    "group_oid" : None
    }

connected = False
def _ConnectCallback(playerOid, success):
    global connected
    ClientAPI.Interface.DispatchEvent("VOICE_CONNECT", [])

def _MakeVoiceConfigStr(extraArgs = ""):
    global voiceConfigStr
    global configMap

    voiceConfigStr = extraArgs
    for param in configMap.keys():
        value = configMap[param]
        if value != None:
            voiceConfigStr += " " + param + " " + str(configMap[param]).lower()

def _ConnectToVoiceServer(extraArgs = ""):
    global voiceConfigStr
    _MakeVoiceConfigStr(extraArgs)
    Voice.StartVoiceManager(voiceConfigStr, _ConnectCallback)
    _UpdatePushToTalk()

def _UpdateVoiceConfig(extraArgs = ""):
    global enableVoice
    global voiceGroupOid
    global voiceConfigStr

    if ClientAPI.GetPlayerObject() == None:
        return

    if not enableVoice and Voice.VoiceManagerRunning():
        RemoveEventHandler("VoiceAllocation",HandleVoiceAllocation)
        RemoveEventHandler("VoiceDeallocation",HandleVoiceDeallocation)        
        _StopVoiceManager()
        return

    _MakeVoiceConfigStr(extraArgs)

    if enableVoice:
        if Voice.ConfigRequiresRestart(voiceConfigStr) or not Voice.VoiceManagerRunning():
            # configStr = configStr + " authentication_token " + authToken
            # send req for voice parms
            # Voice.StartVoiceManager(configStr, _ConnectCallback)
            ClientAPI.Log("MarsVoice: sending voice_parms request")
            ClientAPI.Network.SendExtensionMessage(ClientAPI.GetPlayerObject().OID, False, "voice_parms", {})
        else:
            # Reset event handlers if VM is already running
            RemoveEventHandler("VoiceAllocation",HandleVoiceAllocation)
            RemoveEventHandler("VoiceDeallocation",HandleVoiceDeallocation)              
            Voice.ConfigureVoiceManager(voiceConfigStr, _ConnectCallback)
            _UpdatePushToTalk()
        # Reset UI event handlers
        if Voice.VoiceManagerRunning():
            RegisterEventHandler("VoiceAllocation",HandleVoiceAllocation)
            RegisterEventHandler("VoiceDeallocation",HandleVoiceDeallocation)

def _StartTestRecording():
    args = "connect_to_server false default_volume " + str(configMap["default_volume"]) + " agc_level " + str(configMap["agc_level"]) + " mic_device_number " + str(configMap["mic_device_number"]) + " playback_device_number " + str(configMap["playback_device_number"]) + " mic_record_speex true"
    Voice.StartVoiceManager(args, None)

def _StopVoiceManager():
    Voice.StopVoiceManager()
    ClientAPI.Interface.DispatchEvent("VOICE_CONNECT", [])

def _PlaybackTestRecording():
    args = "connect_to_server false default_volume " + str(configMap["default_volume"]) + " playback_device_number " + str(configMap["playback_device_number"])
    Voice.StartTestPlayback(args)

# This function is an event handler that runs when the player has been initialized.
def _PlayerInitHandler(sender, args):
    # In the character selection world, I don't want voice.
    if not ClientAPI.World.IsWorldLocal and (ClientAPI.GetPlayerObject() is not None):
        ClientAPI.Log("MarsVoice: oid=" + str(ClientAPI.GetPlayerObject().OID))
        configMap["player_oid"] = ClientAPI.GetPlayerObject().OID
        LoadConfigSettings(ClientAPI.World.WorldName)
        ClientAPI.Network.SendExtensionMessage(ClientAPI.GetPlayerObject().OID, False, "voice_parms", {})
        ClientAPI.RemoveEventHandler("PlayerInitialized", _PlayerInitHandler)

def _HandleVoiceServerResponse(properties):
    global voiceServerArgs
    ClientAPI.Log("MarsVoice: voice server response = " + str(properties))
    host = ClientAPI.Voice.TranslateHostname(properties["host"])
    port = properties["port"]
    token = properties["auth_token"]
    extraArgs = "voice_server_host " + host + " voice_server_port " + str(port) + " authentication_token " + token;
    if Voice.VoiceManagerRunning():
        _StopVoiceManager()
    _ConnectToVoiceServer(extraArgs)

def LoadConfigSettings(worldName):
    global configMap
    global enableVoice
    global enableInput
    global inputDeviceCache
    global outputDeviceCache
    if (inputDeviceCache == None) or (outputDeviceCache == None):
        _InitDeviceCaches()
    voiceChatConfig = Voice.VoiceChatConfig(worldName)
    voiceChatConfig.LoadCategoryData()
    enableVoice = voiceChatConfig.Enabled
    enableInput = voiceChatConfig.InputEnabled
    configMap["connect_to_server"] = voiceChatConfig.Enabled
    configMap["mic_device_number"] = FindDeviceNumber(inputDeviceCache, voiceChatConfig.MicDevice)
    configMap["playback_device_number"] = FindDeviceNumber(outputDeviceCache, voiceChatConfig.PlaybackDevice)
    configMap["default_volume"] = voiceChatConfig.PlaybackLevel
    configMap["agc_level"] = voiceChatConfig.MicLevel
    if (voiceChatConfig.VADEnabled):
        LockPushToTalk(True)
    else:   
        UnlockPushToTalk()

def FindDeviceNumber(cache, deviceName):
    if deviceName == None:
        return 0
    elif deviceName in cache:
        return cache.IndexOf(cache, deviceName)
    else:
        return 0

def SaveConfigSettings():
    global configMap
    global enableVoice
    global enableInput
    global pttLocked
    global inputDeviceCache
    global outputDeviceCache
    if (inputDeviceCache == None) or (outputDeviceCache == None):
        _InitDeviceCaches()
    voiceChatConfig = Voice.VoiceChatConfig.Instance
    ClientAPI.Log("MarsVoice.SaveConfigSettings: voiceChatConfig is " + str(voiceChatConfig))
    voiceChatConfig.Enabled = enableVoice
    voiceChatConfig.InputEnabled = enableInput
    voiceChatConfig.MicDevice = inputDeviceCache[configMap["mic_device_number"]]
    voiceChatConfig.PlaybackDevice = outputDeviceCache[configMap["playback_device_number"]]
    voiceChatConfig.PlaybackLevel = configMap["default_volume"]
    voiceChatConfig.MicLevel = configMap["agc_level"]
    voiceChatConfig.VADEnabled = pttLocked
    voiceChatConfig.WriteCategoryData()

# Register an event handler that will run when the player has been initialized.
ClientAPI.RegisterEventHandler("PlayerInitialized", _PlayerInitHandler)
ClientAPI.Network.RegisterExtensionMessageHandler("voice_parms_response", _HandleVoiceServerResponse)

def GetOutputLevel():
    return configMap["default_volume"] / 2.0

def SetOutputLevel(level):
    configMap["default_volume"] = level * 2.0
    if Voice.VoiceManagerRunning():
        Voice.SetPlaybackVolumeForAllSpeakers(level)

def GetOutputDevice():
    return configMap["playback_device_number"]

def SetOutputDevice(index):
    configMap["playback_device_number"] = index
    _UpdateVoiceConfig()

def GetInputLevel():
    return (configMap["agc_level"] - 1) / 19.0

def SetInputLevel(level):
    level = int(level * 19 + 1)
    configMap["agc_level"] = level
    if Voice.VoiceManagerRunning():
        Voice.SetMicLevel(GetInputDevice(), level)

def GetInputDevice():
    return configMap["mic_device_number"]

def SetInputDevice(index):
    configMap["mic_device_number"] = index
    _UpdateVoiceConfig()

def GetVoiceEnabled():
    return enableVoice

def SetVoiceEnabled(enable):
    global enableVoice
    enableVoice = enable
    configMap["connect_to_server"] = enable
    _UpdateVoiceConfig()
    _UpdatePushToTalk()

def GetInputEnabled():
    return enableInput

def SetInputEnabled(enable):
    global enableInput
    enableInput = enable
    _UpdatePushToTalk()
    
def GetTestMode():
    return configMap["listen_to_yourself"]

def SetTestMode(enable):
    configMap["listen_to_yourself"] = enable
    _UpdateVoiceConfig()

def _InitDeviceCaches():
    global inputDeviceCache
    global outputDeviceCache

    vmgrRunning = Voice.VoiceManagerRunning()
    if not vmgrRunning:
        Voice.StartVoiceManager("connect_to_server false", None)
    inputDeviceCache = Voice.GetAllMicrophoneDevices()
    outputDeviceCache = Voice.GetAllPlaybackDevices()
    if not vmgrRunning:
        Voice.StopVoiceManager()

def GetOutputDeviceName():
    global outputDeviceCache
    if outputDeviceCache == None:
        _InitDeviceCaches()
    return outputDeviceCache[configMap["playback_device_number"]]

def GetInputDeviceName():
    global inputDeviceCache
    if inputDeviceCache == None:
        _InitDeviceCaches()
    return inputDeviceCache[configMap["mic_device_number"]]

def GetAllOutputDevices():
    global outputDeviceCache

    if Voice.VoiceManagerRunning():
        outputDeviceCache = Voice.GetAllPlaybackDevices()
    elif outputDeviceCache == None:
        _InitDeviceCaches()
    return outputDeviceCache

    if Voice.VoiceManagerRunning():
        return Voice.GetAllPlaybackDevices()
    else:
        return [ "Not Available" ]

def GetAllInputDevices():
    global inputDeviceCache

    if Voice.VoiceManagerRunning():
        inputDeviceCache = Voice.GetAllMicrophoneDevices()
    elif inputDeviceCache == None:
        _InitDeviceCaches()
    return inputDeviceCache

def PushToTalk(nowTalking):
    global pttState
    pttState = nowTalking
    _UpdatePushToTalk()

def LockPushToTalk(nowTalking):
    global pttLocked
    global pttLockState
    pttLocked = True
    pttLockState = nowTalking
    _UpdatePushToTalk()

def UnlockPushToTalk():
    global pttLocked
    pttLocked = False
    _UpdatePushToTalk()

def GetPushToTalkState():
    return pttState, pttLocked, pttLockState

def _UpdatePushToTalk():
    if not Voice.VoiceManagerRunning():
        return
    elif not enableInput:
        Voice.PushToTalk(False)
    elif pttLocked:
        Voice.PushToTalk(pttLockState)
    else:
        Voice.PushToTalk(pttState)

def SetParameters(parms):
    for parm in parms.keys():
        configMap[parm] = parms[parm]
    _UpdateVoiceConfig()

def SetVoiceGroupOid(value):
    global configMap
    configMap["group_oid"] = value

def GetVoiceGroupOid():
    global configMap
    return configMap["group_oid"]

def JoinVoiceGroup(groupOid):
    SetVoiceGroupOid(groupOid)
    _UpdateVoiceConfig()
    
def RegisterEventHandler(eventName, eventHandler):
    global _worldManager
    if eventName == "VoiceAllocation":
        _worldManager.VoiceMgr.onVoiceAllocation += eventHandler
    elif eventName == "VoiceDeallocation":
        _worldManager.VoiceMgr.onVoiceDeallocation += eventHandler
    else:
        ClientAPI.LogError("Invalid event name '%s' passed to MarsVoice.RegisterEventHandler" % str(eventName))

def RemoveEventHandler(eventName, eventHandler):
    global _worldManager
    if eventName == "VoiceAllocation":
        _worldManager.VoiceMgr.onVoiceAllocation -= eventHandler
    elif eventName == "VoiceDeallocation":
        _worldManager.VoiceMgr.onVoiceDeallocation -= eventHandler
    else:
        ClientAPI.LogError("Invalid event name '%s' passed to MarsVoice.RegisterEventHandler" % str(eventName))

def HandleVoiceAllocation(playerOid, voiceNumber, positional):    
    ClientAPI.Interface.DispatchEvent("VOICE_ALLOCATION",[str(playerOid)])

def HandleVoiceDeallocation(playerOid):
    ClientAPI.Interface.DispatchEvent("VOICE_DEALLOCATION",[str(playerOid)])
