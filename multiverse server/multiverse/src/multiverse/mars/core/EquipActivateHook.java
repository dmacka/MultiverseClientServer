package multiverse.mars.core;

import multiverse.server.engine.*;
import multiverse.server.util.*;
import multiverse.server.plugins.*;
import multiverse.mars.plugins.*;
import multiverse.mars.objects.*;

/**
 * an activate hook attached to equippable items, eg: weapons, armor
 * hook will unequip the item in the current slot and equip the item
 * associated with the hook
 */
public class EquipActivateHook implements ActivateHook {
    public EquipActivateHook() {
        super();
    }

    /**
     * returns whether the item was successfully activated
     * @param activatorOid
     * @param targetOid
     */
    @Override
    public boolean activate(Long activatorOid, MarsItem item, Long targetOid) {
	// get the inventoryplugin
	MarsInventoryPlugin invPlugin = (MarsInventoryPlugin)Engine.getPlugin(InventoryPlugin.INVENTORY_PLUGIN_NAME);
	if (Log.loggingDebug)
	    Log.debug("EquipActivateHook: calling invPlugin, item=" + item +
	            ", activatorOid=" + activatorOid + ", targetOid=" + targetOid);
	
	// is this item already equipped
	MarsInventoryPlugin.EquipMap equipMap = 
	    invPlugin.getEquipMap(activatorOid);
	MarsEquipSlot slot;
	invPlugin.getLock().lock();
	try {
	    slot = equipMap.getSlot(item.getMasterOid());
	}
	finally {
	    invPlugin.getLock().unlock();
	}
	if (slot == null) {
	    // its not equipped
	    if (Log.loggingDebug)
	        Log.debug("EquipActivateHook: item not equipped: " + item);
	    return invPlugin.equipItem(item, activatorOid, true);
	}
	else {
	    // it is equipped, unequip it
	    if (Log.loggingDebug)
	        Log.debug("EquipActivateHook: item IS equipped: " + item);
	    return invPlugin.unequipItem(item, activatorOid);
	}
    }

    // use oids since cheaper to serialize
    protected long itemOid = -1;
    private static final long serialVersionUID = 1L;
}
