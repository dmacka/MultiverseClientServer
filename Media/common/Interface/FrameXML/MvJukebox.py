import ClientAPI
import FMOD

channelData = [
    { "name" : "DJ Steve",
      "type" : "stream",
      "url" : "http://ct5.fast-serv.com:8804/",
      "cost" : "FREE",
      "description" : ""
      },
    { "name" : "Groove Salad",
      "type" : "stream",
      "url" : "http://scfire-nyk0l-2.stream.aol.com:80/stream/1018",
      "cost" : "FREE",
      "description" : "Groove Salad: a nicely chilled plate of ambient beats and grooves. [Soma FM]"
      },
    { "name" : "The 80s Channel",
      "type" : "stream",
      "url" : "http://scfire-nyk0l-1.stream.aol.com:80/stream/1040",
      "cost" : "FREE",
      "description" : ".997 The 80s Channel"
      },
    { "name" : "Radio Paradise",
      "type" : "stream",
      "url" : "http://scfire-nyk0l-1.stream.aol.com:80/stream/1048",
      "cost" : "FREE",
      "description" : "Radio Paradise - DJ-mixed modern & classic rock, world, electronica & more - info: radioparadise.com"
      },
    { "name" : "The Hitz Channel",
      "type" : "stream",
      "url" : "http://scfire-nyk0l-1.stream.aol.com:80/stream/1074",
      "cost" : "FREE",
      "description" : ".997 The Hitz Channel"
      },
    { "name" : "SKY.FM",
      "type" : "stream",
      "url" : "http://scfire-nyk0l-1.stream.aol.com:80/stream/1010",
      "cost" : "FREE",
      "description" : "SKY.FM - Absolute Smooth Jazz - the world's smoothest jazz 24 hours a day"
      },
    { "name" : "Vocal Trance",
      "type" : "stream",
      "url" : "http://scfire-nyk0l-1.stream.aol.com:80/stream/1065",
      "cost" : "FREE",
      "description" : "DIGITALLY IMPORTED - Vocal Trance - a fusion of trance, dance, and chilling vocals"
      },
    { "name" : "-=[:: HOT 108 JAMZ ::]=-",
      "type" : "stream",
      "url" : "http://scfire-nyk0l-1.stream.aol.com:80/stream/1071",
      "cost" : "FREE",
      "description" : "-=[:: HOT 108 JAMZ ::]=- #1 FOR HIP HOP -128K HD) * CONNECT FROM OUR WEBSITE www.hot108.com"
      },
    { "name" : "Crazy",
      "type" : "audio",
      "url" : "http://sv1/mvsecret/Crazy.mp3",
      "cost" : "$0.25",
      "description" : ""
      },
    { "name" : "Ballad of Serenity",
      "type" : "audio",
      "url" : "http://sv1/mvsecret/Ballad_of_Serenity.mp3",
      "cost" : "$0.25",
      "description" : ""
      },
    ]

slots = 15
channelList = None
playingSound = None
jukeboxObj = None

attenuateRadius1 = 15000.0
attenuateRadius2 = 60000.0

attRad1Sq = attenuateRadius1 * attenuateRadius1
attRad2Sq = attenuateRadius2 * attenuateRadius2

def MvJukebox_OnLoad(frame):
    MvJukeboxFrameChannels.Properties["selected"] = None
    MvJukeboxFrameChannels.Properties["playing"] = None
    frame.RegisterEvent("PROPERTY_jukebox")
    ClientAPI.GetPlayerObject().RegisterEventHandler('PositionChange', MvJukebox_PositionChangeHandler)

def MvJukebox_RegisterChannelList(frame):
    global channelList
    channelList = frame

def MvJukebox_UpdateChannelList(frame):
    global slots
    global channelList
    for i in range(0, slots):
        channel = getglobal(channelList.GetName() + "Channel" + str(i+1))
        channelName = getglobal(channelList.GetName() + "Channel" + str(i+1) + "NameString")
        channelCost = getglobal(channelList.GetName() + "Channel" + str(i+1) + "CostString")
        if i < len(channelData):
            channelName.SetText(channelData[i]["name"])
            channelCost.SetText(channelData[i]["cost"])
            channel.Properties["url"] = channelData[i]["url"]
            channel.Properties["description"] = channelData[i]["description"]
            channel.Show()
        else:
            channelName.SetText("")
            channelCost.SetText("")
            channel.Properties["url"] = ""
            channel.Properties["description"] = ""
            channel.Hide()

def MvJukebox_SelectChannel(frame):
    selected = MvJukeboxFrameChannels.Properties["selected"]
    if selected is not None and selected is not frame:
        selected.SetButtonState("NORMAL", True)
    MvJukeboxFrameChannels.Properties["selected"] = frame
    frame.SetButtonState("PUSHED", True)
    MvJukeboxFrameControlsInfoDescription.SetText(frame.Properties["description"])

def MvJukebox_IsSelected(frame):
    selected = MvJukeboxFrameChannels.Properties["selected"]
    if selected is frame:
        return True
    else:
        return False

def MvJukebox_PlayChannel(frame):
    global playingSound
    play = getglobal(frame.GetName() + "Play")
    play.Show()
    MvJukeboxFrameChannels.Properties["playing"] = frame
    if playingSound is not None:
        playingSound.Stop()
        playingSound = None
    url = frame.Properties["url"]
    if url is not None:
        playingSound = ClientAPI.GetSoundSource(url, ClientAPI.Vector3.Zero, False, 1.0, True, False)
        if playingSound is not None:
            playingSound.Play()

def MvJukebox_StopChannel(frame):
    play = getglobal(frame.GetName() + "Play")
    play.Hide()
    MvJukeboxFrameChannels.Properties["playing"] = None

def MvJukebox_PlaySelected():
    selected = MvJukeboxFrameChannels.Properties["selected"]
    playing = MvJukeboxFrameChannels.Properties["playing"]
    if selected is playing:
        return
    if playing is not None:
        MvJukebox_StopChannel(playing)
    if selected is None:
        return
    MvJukebox_PlayChannel(selected)

def MvJukebox_Close():
    MvJukeboxFrame.Hide()

def MvJukebox_Open():
    MvJukeboxFrame.Show()

def MvJukebox_OnEvent(frame, event):
    global jukeboxObj
    if event.eventType == "PROPERTY_jukebox":
        if event.eventArgs[0] == "any":
            oid = long(event.eventArgs[1])
            jukeboxObj = ClientAPI.GetObjectByOID(oid)
            jukeboxObj.SetProperty("click_handler", MvJukebox_OnClick)
            jukeboxObj = ClientAPI.GetObjectByOID(oid)
            jukeboxObj.RegisterEventHandler('Disposed', MvJukebox_DisposedHandler)

def MvJukebox_OnClick(sender, args):
    MvJukebox_Open()

def MvJukebox_PositionChangeHandler(worldObj):
    global playingSound
    global jukeboxObj
    global attRad1Sq
    global attRad2Sq
    if playingSound is None or jukeboxObj is None:
        return
    pos1 = ClientAPI.GetPlayerObject().Position
    pos2 = jukeboxObj.Position
    distSq = (pos1-pos2).LengthSquared
    if distSq < attRad1Sq:
        playingSound.Gain = 1.0
    elif distSq > attRad2Sq:
        playingSound.Gain = 0.0
    else:
        gain = (attRad2Sq - distSq) / (attRad2Sq - attRad1Sq)
        playingSound.Gain = gain
    
def MvJukebox_DisposedHandler(worldObj):
    global playingSound
    global jukeboxObj
    if playingSound is not None:
        playingSound.Stop()
        playingSound = None
    if jukeboxObj is not None:
        jukeboxObj = None

