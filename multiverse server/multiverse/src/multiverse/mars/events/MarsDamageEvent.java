package multiverse.mars.events;

import multiverse.server.engine.*;
import multiverse.server.objects.*;
import multiverse.server.network.*;

public class MarsDamageEvent extends Event {
    public MarsDamageEvent() {
	super();
    }

    public MarsDamageEvent(MVByteBuffer buf, ClientConnection con) {
	super(buf, con);
    }

    public MarsDamageEvent(MVObject src, MVObject target, int dmg) {
	super(target);
	setDmg(dmg);
	setDmgSrc(src);
    }

    @Override
    public String getName() {
	return "MarsDamageEvent";
    }

    @Override
    public MVByteBuffer toBytes() {
	int msgId = Engine.getEventServer().getEventID(this.getClass());

	MVByteBuffer buf = new MVByteBuffer(100);
	buf.putLong(getDmgSrc().getOid()); 
	buf.putInt(msgId);
	
	buf.putLong(getObjectOid());
	buf.putString("stun");
	buf.putInt(getDmg());
	buf.flip();
	return buf;
    }

    @Override
    protected void parseBytes(MVByteBuffer buf) {
	buf.rewind();

	setDmgSrc(MVObject.getObject(buf.getLong()));
	/* int msgId = */ buf.getInt();
	setObjectOid(buf.getLong());
	/* String dmgType = */ buf.getString();
	setDmg(buf.getInt());
    }

    public void setDmgSrc(MVObject dmgSrc) {
	this.dmgSrc = dmgSrc;
    }
    public MVObject getDmgSrc() {
	return dmgSrc;
    }

    public void setDmg(int dmg) {
	this.dmg = dmg;
    }
    public int getDmg() {
	return dmg;
    }

    private int dmg = 0;
    private MVObject dmgSrc = null;
}