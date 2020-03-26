package multiverse.mars.events;

import multiverse.server.engine.*;
import multiverse.server.network.*;
import multiverse.server.util.*;
import multiverse.mars.core.*;
import java.util.concurrent.locks.*;

// Update progress for the activation of an ability

public class AbilityProgressEvent extends Event {
    public AbilityProgressEvent() {
	super();
    }

    public AbilityProgressEvent(MVByteBuffer buf, ClientConnection con) {
	super(buf,con);
    }

    public AbilityProgressEvent(MarsAbility.State state) {
	super();
	setObjOid(state.getObject().getOid());
	setAbilityName(state.getAbility().getName());
	setState(state.getState().toString());
	setDuration(state.getDuration());
	setEndTime(calculateEndTime(state));
    }

    protected long calculateEndTime(MarsAbility.State state) {
	MarsAbility ability = state.getAbility();

	switch (state.getState()) {
	case ACTIVATING:
	    return state.getNextWakeupTime();
	case CHANNELLING:
	    int pulsesRemaining = ability.getChannelPulses() - state.getNextPulse() - 1;
	    long endTime = state.getNextWakeupTime() + (pulsesRemaining * ability.getChannelPulseTime());
	    return endTime;
	default:
	    return 0;
	}
    }

    @Override
    public String getName() {
	return "AbilityProgressEvent";
    }

    @Override
    public MVByteBuffer toBytes() {
	int msgId = Engine.getEventServer().getEventID(this.getClass());
	MVByteBuffer buf = new MVByteBuffer(400);

        lock.lock();
        try {
	    buf.putLong(objOid);
	    buf.putInt(msgId);
	    buf.putString(abilityName);
	    buf.putString(state);
	    buf.putLong(duration);
	    buf.putLong(endTime);
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
	    setState(buf.getString());
	    setDuration(buf.getLong());
	    setEndTime(buf.getLong());
        }
        finally {
            lock.unlock();
        }
    }

    public long getObjOid() { return objOid; }
    public void setObjOid(long oid) { objOid = oid; }
    protected long objOid;

    public String getAbilityName() { return abilityName; }
    public void setAbilityName(String name) { abilityName = name; }
    protected String abilityName;

    public String getState() { return state; }
    public void setState(String state) { this.state = state; }
    protected String state;

    public long getDuration() { return duration; }
    public void setDuration(long duration) { this.duration = duration; }
    protected long duration;

    public long getEndTime() { return endTime; }
    public void setEndTime(long time) { endTime = time; }
    protected long endTime;

    transient Lock lock = LockFactory.makeLock("AbilityInfoEvent");
}
