import ClientAPI

def InstancePortalClickHandler(worldObj, args):
    ClientAPI.Log('got click')
    props = {}

    if worldObj.PropertyExists('instanceName'):
        props['instanceName'] = worldObj.GetProperty('instanceName')
    if worldObj.PropertyExists('locMarker'):
        props['locMarker'] = worldObj.GetProperty('locMarker')
    if worldObj.PropertyExists('instanceFlags'):
        props['flags'] = worldObj.GetProperty('instanceFlags')
    if worldObj.PropertyExists('restoreMarker'):
        props['restoreMarker'] = worldObj.GetProperty('restoreMarker')

    ClientAPI.Network.SendExtensionMessage(0, False, "proxy.INSTANCE_ENTRY", props)

def InstancePortalPropertyHandler(sender, args):
    ClientAPI.Log('got instancePortal property for obj=' + str(args.Oid))
    worldObj = ClientAPI.World.GetObjectByOID(args.Oid)
    instance = worldObj.GetProperty('instancePortal')
    if not instance is None:
        worldObj.SetProperty('click_handler', InstancePortalClickHandler)
        worldObj.SetProperty('context_cursor', "SPEAK_CURSOR")
        worldObj.SetProperty('tooltip', instance)
        worldObj.Targetable = True

ClientAPI.World.RegisterObjectPropertyChangeHandler("instancePortal", InstancePortalPropertyHandler)
