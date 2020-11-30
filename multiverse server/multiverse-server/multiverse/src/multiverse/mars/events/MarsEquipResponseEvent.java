package multiverse.mars.events;

import multiverse.server.engine.*;
import multiverse.server.objects.*;
import multiverse.server.network.*;
import multiverse.server.util.*;
import multiverse.mars.objects.*;

public class MarsEquipResponseEvent extends Event {

    public MarsEquipResponseEvent() {
	super();
    }

    public MarsEquipResponseEvent(MVByteBuffer buf, ClientConnection con) {
	super(buf,con);
    }

    public MarsEquipResponseEvent(MarsMob equipper, 
				  MarsItem obj, 
				  String slotName,
				  boolean success) {
	super(equipper);
	setObjToEquip(obj);
	setSlotName(slotName);
	setSuccess(success);
    }

    @Override
    public String getName() {
	return "MarsEquipResponseEvent";
    }

    @Override
    public MVByteBuffer toBytes() {
	int msgId = Engine.getEventServer().getEventID(this.getClass());

	MVByteBuffer buf = new MVByteBuffer(200);
	buf.putLong(getObjectOid());
	buf.putInt(msgId);

	buf.putLong(getObjToEquip().getOid());
	buf.putString(getSlotName());
	buf.putInt(getSuccess()?1:0);
	
	buf.flip();
	return buf;
    }

    @Override
    protected void parseBytes(MVByteBuffer buf) {
	buf.rewind();
	MVObject obj = MVObject.getObject(buf.getLong());
	if (! (obj.isMob())) {
	    throw new MVRuntimeException("EquipResponseEvent.parseBytes: not a mob");
	}
	setEquipper(MarsMob.convert(obj));

	/* int msgId = */ buf.getInt();
	
	setObjToEquip(MarsItem.convert(MVObject.getObject(buf.getLong())));
	setSlotName(buf.getString());
	setSuccess(buf.getInt() == 1);
    }

    public void setEquipper(MarsMob mob) {
	setObject(mob);
    }

    public void setObjToEquip(MarsItem item) {
	objToEquip = item;
    }
    public MVObject getObjToEquip() {
	return objToEquip;
    }

    public void setSuccess(boolean success) {
	this.success = success;
    }
    public boolean getSuccess() {
	return success;
    }
    public void setSlotName(String slotName) {
	this.slotName = slotName;
    }
    public String getSlotName() {
	return slotName;
    }

    private MarsItem objToEquip = null;
    private boolean success = false;
    private String slotName = null;
}