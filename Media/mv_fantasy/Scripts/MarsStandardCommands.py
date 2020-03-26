"""This module contains miscellaneous command handlers that are generally
   useful to a virtual world developer."""

import ClientAPI
import Interface

import MarsCommand
import MarsTarget
import MarsGroup
import MarsVoice

def HandleHelp(args_str):
    msg = "Commands:"
    for command in ClientAPI._commandHandlers.keys():
        msg = msg + " " + command
    ClientAPI.Write(msg)
   
def HandleSay(args_str):
    ClientAPI.Network.SendCommMessage(args_str)
    
def HandleQuit(args_str):
    ClientAPI.Exit()

def HandleLogout(args_str):
    ClientAPI.Network.SendLogoutMessage()

def HandleScript(args_str):
    ClientAPI.Interface.RunScript(args_str)

def HandleReloadUI(args_str):
    ClientAPI.Interface.ReloadUI()

def HandleLoc(args_str):
    player = ClientAPI.GetPlayerObject()
    ClientAPI.Write("Player Position: " + str(player.Position))

def HandleInfo(args_str):
    target = MarsTarget.GetCurrentTarget()
    if target is None:
        target = ClientAPI.GetPlayerObject()
    ClientAPI.DebugWrite("Target Id: " + str(target.OID))
    ClientAPI.DebugWrite("Target Position: " + str(target.Position))
    ClientAPI.DebugWrite("Target Orientation: " + str(target.Orientation))
    camera = ClientAPI.GetPlayerCamera()
    ClientAPI.DebugWrite("Camera Position: " + str(camera.Position))
    ClientAPI.DebugWrite("Camera Orientation: " + str(camera.Orientation))

def HandleProperties(args_str):
    target = MarsTarget.GetCurrentTarget()
    if target is None:
        target = ClientAPI.GetPlayerObject()
    ClientAPI.DebugWrite("Properties for %s:" % target.Name)
    for prop in target.PropertyNames:
        ClientAPI.DebugWrite(" %s: %s" % (prop, target.FormatProperty(prop)))

def HandleTarget(args_str):
    args = args_str.split()
    if len(args) < 1:
        ClientAPI.Write("Insufficient args to target command")
        return
    MarsTarget.TargetByName(args[0])
    
def HandleAcquire(args_str):
    target = MarsTarget.GetCurrentTarget()
    if target is None:
        ClientAPI.Write("No target selected")
        return
    ClientAPI.Network.SendAcquireMessage(target.OID)

def HandlePickup(args_str):
    target = MarsTarget.GetCurrentTarget()
    if target is None:
        ClientAPI.Write("No target selected")
        return
    ClientAPI.Network.SendAcquireMessage(target.OID)
    ClientAPI.Network.SendEquipMessage(target.OID, "primaryWeapon")

def HandleAttack(args_str):
    MarsTarget.AttackTarget()

def HandleServer(args_str):
    ClientAPI.Network.SendCommMessage("/" + args_str)

def HandleInstance(args_str):
    args = args_str.split()
    if len(args) < 1:
        ClientAPI.Write("Insufficient args to instance command")
        return

    flags = None
    marker = None
    name = None
    oid = None
    restoreMarker = None

    ii = 0
    while ii < len(args):
        arg = args[ii]
        if arg == "-push":
            flags = "push"
        elif arg == "-pop":
            flags = "pop"
        elif arg == "-m" or arg == "-waypoint":
            ii = ii + 1
            marker = args[ii]
        elif arg == "-n" or arg == "-name":
            ii = ii + 1
            name = args[ii]
        elif arg == "-oid":
            ii = ii + 1
            oid = args[ii]
        elif arg == "-r":
            ii = ii + 1
            restoreMarker = args[ii]
        ii = ii + 1

    props = {}
    if name != None:
        props["instanceName"] = name
    if marker != None:
        props["locMarker"] = marker
    if flags != None:
        props["flags"] = flags
    if oid != None:
        props["instanceOid"] = long(oid)
    if restoreMarker != None:
        props["restoreMarker"] = restoreMarker

    ClientAPI.Network.SendExtensionMessage(0, False, "proxy.INSTANCE_ENTRY", props)


def HandleGenerate(args_str):
    args = args_str.split()
    if len(args) < 1:
        ClientAPI.Write("Insufficient args to generate command")
        return

    props = {}
    ii = 0
    while ii < len(args):
        arg = args[ii]
        if arg == "-P":
            props["persistent"] = 1
        elif arg == "-m":
            ii = ii + 1
            props["marker"] = args[ii]
        elif len(arg) > 0 and arg[0] != "-":
	    break
	else:
	    print "unknown option " + arg
	ii = ii + 1

    if ii >= len(args):
        ClientAPI.DebugWrite("Missing template name")
	return

    props["template"] = " ".join(args[ii:])

    ClientAPI.Network.SendExtensionMessage(0, False, "proxy.GENERATE_OBJECT", props)


#
# Voice command: The format is /voice cmd parm1 val1 parm2 val2 ... parmN valN
# keywords and optional values.  The parameter parsing is done entirely in the 
# voice substrate, and the keywords may be any legal VoiceParm, as defined
# in Lib/Voice/VoiceParm.cs
#
def HandleVoice(args_str):
    ClientAPI.Log("/voice " + args_str)
    args = args_str.split()
    if len(args) < 1:
        ClientAPI.Write("/voice cmd must have at least 1 arg")
        DisplayVoiceHelp(True)
        return
    cmd = args[0]
    del args[0]

    parms = {}
    while len(args) >= 2:
        parms[args[0]] = args[1]
        del args[0]
        del args[0]

    if cmd == "help":
        DisplayVoiceHelp(True)
    elif cmd == "detailedhelp":
        DisplayVoiceHelp(False)
    elif cmd == "start":
        # We stash the args, and send the proxy a message to get 
        # the server host and port.
        ClientAPI.Log("HandleVoice start: args " + str(parms))
        MarsVoice.SetParameters(parms)
        MarsVoice.SetVoiceEnabled(True)
        MarsVoice.SetInputEnabled(True)
    elif cmd == "stop":
        MarsVoice.SetVoiceEnabled(False)
        MarsVoice.SetInputEnabled(False)
    elif cmd == "config":
        MarsVoice.SetParameters(parms)
        ClientAPI.Log("HandleVoice config: args " + (parms))
    else:
        DisplayVoiceHelp(True)

def DisplayVoiceHelp(common):
    ClientAPI.Write("Usage: /voice cmd parms  Where cmd is start, stop, config, help or detailedhelp; and parms are name-value pairs")
    if common:
        ClientAPI.Write("Commonly-used command parms:")
        ClientAPI.Write(ClientAPI.Voice.MakeHelpString(True))
    else:
        ClientAPI.Write("All legal command parms:")
        ClientAPI.Write(ClientAPI.Voice.MakeHelpString(False))


def HandleGroup(args_str):
    MarsGroup.SendGroupChatMessage(args_str)

def HandleInvite(args_str):
    targetOid = ClientAPI.World.GetObjectByName(args_str).OID
    MarsGroup.SendInviteRequestMessage(targetOid)

MarsCommand.RegisterCommandHandler("help", HandleHelp)
MarsCommand.RegisterCommandHandler("say", HandleSay)
MarsCommand.RegisterCommandHandler("quit", HandleQuit)
MarsCommand.RegisterCommandHandler("logout", HandleLogout)
MarsCommand.RegisterCommandHandler("script", HandleScript)
MarsCommand.RegisterCommandHandler("reloadui", HandleReloadUI)

MarsCommand.RegisterCommandHandler("loc", HandleLoc)
MarsCommand.RegisterCommandHandler("info", HandleInfo)
MarsCommand.RegisterCommandHandler("props", HandleProperties)
MarsCommand.RegisterCommandHandler("properties", HandleProperties)
MarsCommand.RegisterCommandHandler("target", HandleTarget)

MarsCommand.RegisterCommandHandler("acquire", HandleAcquire)
MarsCommand.RegisterCommandHandler("pickup", HandlePickup)
MarsCommand.RegisterCommandHandler("attack", HandleAttack)
MarsCommand.RegisterCommandHandler("server", HandleServer)

MarsCommand.RegisterCommandHandler("voice", HandleVoice)
MarsCommand.RegisterCommandHandler("instance", HandleInstance)

MarsCommand.RegisterCommandHandler("generate", HandleGenerate)
MarsCommand.RegisterCommandHandler("group", HandleGroup)
MarsCommand.RegisterCommandHandler("invite", HandleInvite)
