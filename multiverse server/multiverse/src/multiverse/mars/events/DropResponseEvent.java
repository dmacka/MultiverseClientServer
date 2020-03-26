package multiverse.mars.events;

import multiverse.server.engine.*;
import multiverse.server.objects.*;
import multiverse.server.network.*;

/**
 * object is dropping the a diff obj from its inventory
 */
public class DropResponseEvent extends Event {
    public DropResponseEvent() {
	super();
    }

    public DropResponseEvent(MVByteBuffer buf, ClientConnection con) {
	super(buf, con);
    }

    public DropResponseEvent(MVObject dropper, 
			     MVObject obj, 
			     String slot, 
			     boolean status) {
	super(obj);
	setDropper(dropper);
	setSlotName(slot);
	setStatus(status);
    }

    @Override
    public String getName() {
	return "DropEvent";
    }

    @Override
    public MVByteBuffer toBytes() {
	int msgId = Engine.getEventServer().getEventID(this.getClass());

	MVByteBuffer buf = new MVByteBuffer(200);
	buf.putLong(getDropper().getOid()); 
	buf.putInt(msgId);
	
	buf.putLong(getObjectOid());
	buf.putString(getSlotName());
	buf.putInt(getStatus()?1:0);
	buf.flip();
	return buf;
    }

    @Override
    protected void parseBytes(MVByteBuffer buf) {
	buf.rewind();

	long playerId = buf.getLong();
	setDropper(MVObject.getObject(playerId));

	/* int msgId = */ buf.getInt();

	long objId = buf.getLong();
	setObjectOid(objId);

	setSlotName(buf.getString());
	setStatus(buf.getInt() == 1);
    }

    public void setDropper(MVObject dropper) {
	this.dropper = dropper;
    }
    public MVObject getDropper() {
	return dropper;
    }

    public void setSlotName(String slotName) {
	this.slotName = slotName;
    }
    public String getSlotName() {
	return slotName;
    }

    public void setStatus(boolean status) {
	this.status = status;
    }
    public boolean getStatus() {
	return status;
    }

    private MVObject dropper = null;
    private String slotName = null;
    private boolean status;
}
