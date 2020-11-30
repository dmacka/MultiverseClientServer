package multiverse.mars.objects;

import multiverse.server.util.*;
import java.util.*;
import java.util.concurrent.locks.*;
import java.io.*;

/**
 * stores information about how to handle equipping.
 * says what equipslots are valid.
 * says what socket the equipslot maps to.
 * marsmobs all refer to an object like this
 */
public class MarsEquipInfo implements Cloneable, Serializable {
    public MarsEquipInfo() {
	setupTransient();
    }

    public MarsEquipInfo(String name) {
	setupTransient();
        setName(name);
    }

    @Override
    public String toString() {
        localLock.lock();
        try {
            String s = "[MarsEquipInfo: name=" + name;
            for (MarsEquipSlot slot : equipSlots) {
                s += ", slot=" + slot;
            }
            return s + "]";
        }
        finally {
            localLock.unlock();
        }
    }

    public String getName() {
	return name;
    }
    public void setName(String name) {
	staticMapLock.lock();
	try {
            this.name = name;
	    equipInfoMap.put(name, this);
	}
	finally {
	    staticMapLock.unlock();
	}
    }
    private String name;


    public void addEquipSlot(MarsEquipSlot slot) {
	localLock.lock();
	try {
	    equipSlots.add(slot);
	}
	finally {
	    localLock.unlock();
	}
    }
    public List<MarsEquipSlot> getEquippableSlots() {
	localLock.lock();
	try {
	    return new ArrayList<>(equipSlots);
	}
	finally {
	    localLock.unlock();
	}
    }
    public void setEquippableSlots(List<MarsEquipSlot> slots) {
        localLock.lock();
        try {
            equipSlots = new ArrayList<>(slots);
        }
        finally {
            localLock.unlock();
        }
    }
    List<MarsEquipSlot> equipSlots = new ArrayList<>();
    
    public static MarsEquipInfo getEquipInfo(String name) {
	staticMapLock.lock();
	try {
	    return equipInfoMap.get(name);
	}
	finally {
	    staticMapLock.unlock();
	}
    }

    private static Map<String, MarsEquipInfo> equipInfoMap =
	new HashMap<String, MarsEquipInfo>();


    private static Lock staticMapLock = LockFactory.makeLock("StaticMarsEquipInfo");
    transient private Lock localLock = null;

    void setupTransient() {
	localLock = LockFactory.makeLock("MarsEquipInfo");
    }
    private void readObject(ObjectInputStream in) 
	throws IOException, ClassNotFoundException {
	in.defaultReadObject();
	setupTransient();
    }

    // define the standard mob equippable slots
    public static MarsEquipInfo DefaultEquipInfo =
	new MarsEquipInfo("MarsDefaultEquipInfo");
    static {
	DefaultEquipInfo.addEquipSlot(MarsEquipSlot.PRIMARYWEAPON);
	DefaultEquipInfo.addEquipSlot(MarsEquipSlot.CHEST);
	DefaultEquipInfo.addEquipSlot(MarsEquipSlot.LEGS);
	DefaultEquipInfo.addEquipSlot(MarsEquipSlot.HEAD);
	DefaultEquipInfo.addEquipSlot(MarsEquipSlot.FEET);
	DefaultEquipInfo.addEquipSlot(MarsEquipSlot.HANDS);
    }

    private static final long serialVersionUID = 1L;
}