package multiverse.mars.events;

import multiverse.server.engine.*;
import multiverse.server.objects.*;
import multiverse.server.network.*;
import multiverse.mars.objects.*;

// mob is unequiping obj
public class MarsUnequipEvent extends Event {
    public MarsUnequipEvent() {
	super();
    }

    public MarsUnequipEvent(MVByteBuffer buf, ClientConnection con) {
	super(buf,con);
    }

    public MarsUnequipEvent(MarsMob unequipper, 
			    MarsItem objToUnequip, 
			    String slotName) {
	super(unequipper);
	setObjToUnequip(objToUnequip);
	setSlotName(slotName);
    }

    @Override
    public String getName() {
	return "UnequipEvent";
    }

    @Override
    public MVByteBuffer toBytes() {
	int msgId = Engine.getEventServer().getEventID(this.getClass());

	MVByteBuffer buf = new MVByteBuffer(200);
	buf.putLong(getObjectOid()); 
	buf.putInt(msgId);
	buf.putLong(getObjToUnequip().getOid());
	buf.putString(getSlotName());
	buf.flip();
	return buf;
    }

    @Override
    protected void parseBytes(MVByteBuffer buf) {
	buf.rewind();
	setUnequipper(MarsMob.convert(MVObject.getObject(buf.getLong())));
	/* int msgId = */ buf.getInt();
	setObjToUnequip(MarsItem.convert(MVObject.getObject(buf.getLong())));
	setSlotName(buf.getString());
    }

    public void setUnequipper(MarsMob mob) {
	setObject(mob);
    }

    public void setObjToUnequip(MarsItem obj) {
	objToUnequip = obj;
    }
    public MarsItem getObjToUnequip() {
	return objToUnequip;
    }

    public void setSlotName(String slotName) {
	this.slotName = slotName;
    }
    public String getSlotName() {
	return slotName;
    }

    private MarsItem objToUnequip = null;
    private String slotName = null;
}