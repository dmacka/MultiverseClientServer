package multiverse.mars.events;

import multiverse.server.engine.*;
import multiverse.server.objects.*;
import multiverse.server.network.*;
import multiverse.mars.objects.*;

/**
 * mob is equiping obj
 */
public class EquipEvent extends Event {
    public EquipEvent() {
	super();
    }

    public EquipEvent(MVByteBuffer buf, ClientConnection con) {
	super(buf,con);
    }

    public EquipEvent(MarsMob equipper, MarsItem equipObj, String slotName) {
	super(equipper);
	setObjToEquipId(equipObj.getOid());
	setSlotName(slotName);
    }

    @Override
    public String getName() {
	return "EquipEvent";
    }

    @Override
    public MVByteBuffer toBytes() {
	int msgId = Engine.getEventServer().getEventID(this.getClass());

	MVByteBuffer buf = new MVByteBuffer(200);
	buf.putLong(getObjectOid()); 
	buf.putInt(msgId);
	buf.putLong(getObjToEquip().getOid());
	buf.putString(getSlotName());
	buf.flip();
	return buf;
    }

    @Override
    protected void parseBytes(MVByteBuffer buf) {
	buf.rewind();
	setObjectOid(buf.getLong());
	/* int msgId = */ buf.getInt();
	setObjToEquipId(buf.getLong());
	setSlotName(buf.getString());
    }

    public void setObjToEquipId(MarsItem obj) {
	this.objToEquipId = obj.getOid();
    }
    public void setObjToEquipId(Long id) {
	this.objToEquipId = id;
    }
    public Long getObjToEquipId() {
	return objToEquipId;
    }
    public MarsItem getObjToEquip() {
	return MarsItem.convert(MVObject.getObject(objToEquipId));
    }

    public void setSlotName(String slotName) {
	this.slotName = slotName;
    }
    public String getSlotName() {
	return slotName;
    }

    private Long objToEquipId = null;
    private String slotName = null;
}
