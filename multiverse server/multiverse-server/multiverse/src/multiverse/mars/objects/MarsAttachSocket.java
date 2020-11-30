package multiverse.mars.objects;

import multiverse.server.util.*;
import java.util.*;
import java.io.*;
import java.util.concurrent.locks.*;

public class MarsAttachSocket implements Serializable {
    public MarsAttachSocket() {
    }

    public MarsAttachSocket(String socketName) {
	this.name = socketName;
	mapLock.lock();
	try {
	    socketNameMapping.put(socketName, this);
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
    private String name;

    @Override
    public String toString() {
	return "[MarsAttachSocket name=" + getName() + "]";
    }

    public static MarsAttachSocket getSocketByName(String socketName) {
	mapLock.lock();
	try {
	    return socketNameMapping.get(socketName);
	}
	finally {
	    mapLock.unlock();
	}
    }

    private static Map<String, MarsAttachSocket> socketNameMapping =
	new HashMap<String, MarsAttachSocket>();


    private static Lock mapLock = LockFactory.makeLock("MarsAttachSocketLock");

    public static MarsAttachSocket PRIMARYWEAPON = 
	new MarsAttachSocket("primaryWeapon");

    private static final long serialVersionUID = 1L;
}