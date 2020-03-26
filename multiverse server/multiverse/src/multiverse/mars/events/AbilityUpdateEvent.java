package multiverse.mars.events;

import multiverse.server.engine.*;
import multiverse.server.network.*;
import multiverse.server.util.*;
import multiverse.mars.objects.*;
import multiverse.mars.core.*;
import java.util.*;
import java.util.concurrent.locks.*;

// Update the list of abilities that this object knows

public class AbilityUpdateEvent extends Event {
    public AbilityUpdateEvent() {
	super();
    }

    public AbilityUpdateEvent(MVByteBuffer buf, ClientConnection con) {
	super(buf,con);
    }

    public AbilityUpdateEvent(MarsObject obj) {
	super(obj);
	setObjOid(obj.getOid());
	for(MarsAbility.Entry entry : obj.getAbilityMap().values()) {
	    addAbilityEntry(entry);
	}
    }

    @Override
    public String getName() {
	return "AbilityUpdateEvent";
    }

    @Override
    public MVByteBuffer toBytes() {
	int msgId = Engine.getEventServer().getEventID(this.getClass());
	MVByteBuffer buf = new MVByteBuffer(500);

        lock.lock();
        try {
	    buf.putLong(objOid);
	    buf.putInt(msgId);
	
	    int size = abilityEntrySet.size();
	    buf.putInt(size);
	    for(MarsAbility.Entry entry : abilityEntrySet) {
		buf.putString(entry.getAbilityName());
		buf.putString(entry.getIcon());
		buf.putString(entry.getCategory());
	    }
        }
        finally {
            lock.unlock();
        }

	buf.flip();
	return buf;
    }

    @Override
    protected void parseBytes(MVByteBuffer buf) {
        lock.lock();
        try {
	    buf.rewind();

	    setObjOid(buf.getLong());
	    /* int msgId = */ buf.getInt();

            int size = buf.getInt();
	    abilityEntrySet = new HashSet<>(size);
	    while (size-- > 0) {
		String name = buf.getString();
		String icon = buf.getString();
		String category = buf.getString();
		addAbilityEntry(new MarsAbility.Entry(name, icon, category));
	    }
        }
        finally {
            lock.unlock();
        }
    }

    public long getObjOid() { return objOid; }
    public void setObjOid(long oid) { objOid = oid; }
    protected long objOid;

    public void addAbilityEntry(MarsAbility.Entry entry) {
	lock.lock();
	try {
	    abilityEntrySet.add(entry);
	}
	finally {
	    lock.unlock();
	}
    }
    public Set<MarsAbility.Entry> getAbilityEntrySet() {
	lock.lock();
	try {
	    return new HashSet<>(abilityEntrySet);
	}
	finally {
	    lock.unlock();
	}
    }
    public void setAbilityEntrySet(Set<MarsAbility.Entry> set) {
	lock.lock();
	try {
	    abilityEntrySet = new HashSet<>(set);
	}
	finally {
	    lock.unlock();
	}
    }
    protected Set<MarsAbility.Entry> abilityEntrySet = null;

    transient Lock lock = LockFactory.makeLock("AbilityInfoEvent");
}
