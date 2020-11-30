package multiverse.mars.events;

import multiverse.server.engine.*;
import multiverse.server.network.*;
import multiverse.server.util.*;
import multiverse.mars.objects.*;
import multiverse.mars.core.*;
import java.util.concurrent.locks.*;

// Activate an ability

public class AbilityActivateEvent extends Event {
    public AbilityActivateEvent() {
	super();
    }

    public AbilityActivateEvent(MVByteBuffer buf, ClientConnection con) {
	super(buf,con);
    }

    public AbilityActivateEvent(MarsMob obj, MarsAbility ability, MarsObject target, MarsItem item) {
	super();
	setObjOid(obj.getOid());
	setAbilityName(ability.getName());
	if (target != null) {
	    setTargetOid(target.getOid());
	}
	if (item != null) {
	    setItemOid(item.getOid());
	}
    }

    @Override
    public String getName() {
	return "AbilityActivateEvent";
    }

    @Override
    public MVByteBuffer toBytes() {
	int msgId = Engine.getEventServer().getEventID(this.getClass());
	MVByteBuffer buf = new MVByteBuffer(200);

        lock.lock();
        try {
	    buf.putLong(objOid);
	    buf.putInt(msgId);
	    buf.putString(abilityName);
	    buf.putLong(targetOid);
	    buf.putLong(itemOid);
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
	    setAbilityName(buf.getString());
	    setTargetOid(buf.getLong());
	    setItemOid(buf.getLong());
        }
        finally {
            lock.unlock();
        }
    }

    public long getObjOid() { return objOid; }
    public void setObjOid(long oid) { objOid = oid; }
    protected long objOid;

    public long getTargetOid() { return targetOid; }
    public void setTargetOid(long oid) { targetOid = oid; }
    protected long targetOid = -1;

    public String getAbilityName() { return abilityName; }
    public void setAbilityName(String name) { abilityName = name; }
    protected String abilityName;

    public long getItemOid() { return itemOid; }
    public void setItemOid(long oid) { itemOid = oid; }
    protected long itemOid = -1;

    transient Lock lock = LockFactory.makeLock("AbilityInfoEvent");
}
