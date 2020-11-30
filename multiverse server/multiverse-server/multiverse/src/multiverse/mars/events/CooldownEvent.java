package multiverse.mars.events;

import multiverse.server.engine.*;
import multiverse.server.network.*;
import multiverse.server.util.*;
import multiverse.mars.objects.*;
import multiverse.mars.core.*;
import java.util.*;
import java.util.concurrent.locks.*;

// Update the state of listed cooldowns for the object

public class CooldownEvent extends Event {
    public CooldownEvent() {
        super();
    }

    public CooldownEvent(MVByteBuffer buf, ClientConnection con) {
        super(buf, con);
    }

    public CooldownEvent(MarsObject obj) {
        super();
        setObjOid(obj.getOid());
    }

    public CooldownEvent(Cooldown.State state) {
        super();
        setObjOid(state.getObject().getOid());
        addCooldown(state);
    }

    @Override
    public String getName() {
        return "CooldownEvent";
    }

    @Override
    public MVByteBuffer toBytes() {
        int msgId = Engine.getEventServer().getEventID(this.getClass());
        MVByteBuffer buf = new MVByteBuffer(400);

        lock.lock();
        try {
            buf.putLong(objOid);
            buf.putInt(msgId);
            for (CooldownEvent.Entry entry : cooldowns) {
                buf.putString(entry.getCooldownID());
                buf.putLong(entry.getDuration());
                buf.putLong(entry.getEndTime());
            }
        } finally {
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
            /* int msgId = */buf.getInt();
            int size = buf.getInt();
            while (size-- > 0) {
                String cooldownID = buf.getString();
                long duration = buf.getLong();
                long endTime = buf.getLong();
                addCooldown(cooldownID, duration, endTime);
            }
        } finally {
            lock.unlock();
        }
    }

    public long getObjOid() { return objOid; }
    public void setObjOid(long oid) { objOid = oid; }
    protected long objOid;

    public void addCooldown(String id, long duration, long endTime) {
        lock.lock();
        try {
            CooldownEvent.Entry entry = new CooldownEvent.Entry(id, duration,
                    endTime);
            cooldowns.add(entry);
        } finally {
            lock.unlock();
        }
    }

    public void addCooldown(Cooldown.State state) {
        addCooldown(state.getID(), state.getDuration(), state.getEndTime());
    }

    public void setCooldowns(Set<CooldownEvent.Entry> cooldowns) {
        lock.lock();
        try {
            this.cooldowns = new HashSet<>(cooldowns);
        } finally {
            lock.unlock();
        }
    }

    public Set<CooldownEvent.Entry> getCooldowns() {
        lock.lock();
        try {
            return new HashSet<>(cooldowns);
        } finally {
            lock.unlock();
        }
    }

    protected Set<CooldownEvent.Entry> cooldowns = new HashSet<>();

    public class Entry {
        public Entry() {
        }

        public Entry(String id, long duration, long endTime) {
            setCooldownID(id);
            setDuration(duration);
            setEndTime(endTime);
        }

	public String getCooldownID() { return cooldownID; }
	public void setCooldownID(String cd) { cooldownID = cd; }
	protected String cooldownID;

	public long getDuration() { return duration; }
	public void setDuration(long duration) { this.duration = duration; }
	protected long duration;

	public long getEndTime() { return endTime; }
	public void setEndTime(long endTime) { this.endTime = endTime; }
	protected long endTime;
    }

    transient Lock lock = LockFactory.makeLock("AbilityInfoEvent");
}
