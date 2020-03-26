import ClientAPI

def _dispatchXPEvent(props):
    ClientAPI.Interface.DispatchEvent("CLASSABILITY_REPORT", [str(props["stat"])])

ClientAPI.Network.RegisterExtensionMessageHandler("mv.STAT_XP_UPDATE", _dispatchXPEvent)