package multiverse.mars.objects;

import java.util.*;
import java.io.*;
import multiverse.server.util.*;
import java.util.concurrent.locks.*;

public class MarsEquipSlot implements Serializable {
    public MarsEquipSlot() {
    }

    public MarsEquipSlot(String slotName) {
	this.name = slotName;
	mapLock.lock();
	try {
	    slotNameMapping.put(slotName, this);
	}
	finally {
	    mapLock.unlock();
	}
    }

    public void setName(String name) {
        this.name = name;
    }
    public String getName() {
	return name;
    }
    private String name = null;

    @Override
    public int hashCode() {
        return name.hashCode();
    }
    @Override
    public boolean equals(Object other) {
        if (other instanceof MarsEquipSlot) {
            MarsEquipSlot otherSlot = (MarsEquipSlot)other;
            return otherSlot.getName().equals(name);
        }
        return false;
    }

    @Override
    public String toString() {
	return "[MarsEquipSlot name=" + getName() + "]";
    }

    public static MarsEquipSlot getSlotByName(String slotName) {
	mapLock.lock();
	try {
	    return slotNameMapping.get(slotName);
	}
	finally {
	    mapLock.unlock();
	}
    }
    private static Map<String, MarsEquipSlot> slotNameMapping =
	new HashMap<String, MarsEquipSlot>();

    private static Lock mapLock = LockFactory.makeLock("MarsEquipSlot");

    public static MarsEquipSlot PRIMARYWEAPON = 
	new MarsEquipSlot("primaryWeapon");

    public static MarsEquipSlot CHEST = 
	new MarsEquipSlot("chest");

    public static MarsEquipSlot LEGS = 
	new MarsEquipSlot("legs");

    public static MarsEquipSlot HEAD = 
	new MarsEquipSlot("head");

    public static MarsEquipSlot FEET = 
	new MarsEquipSlot("feet");

    public static MarsEquipSlot HANDS = 
	new MarsEquipSlot("hands");

    private static final long serialVersionUID = 1L;
}