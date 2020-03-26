package multiverse.mars.events;

import multiverse.mars.objects.*;
import multiverse.server.engine.*;
import multiverse.server.network.*;

public class QuestAvailableEvent extends Event {
    public QuestAvailableEvent() {
	super();
    }

    public QuestAvailableEvent(MVByteBuffer buf, ClientConnection con) {
	super(buf, con);
    }

    public QuestAvailableEvent(MarsMob user,
                               MarsMob questGiver,
                               boolean isAvail,
                               boolean isConclude) {
	super(user);
	setQuestGiverOid(questGiver.getOid());
        isAvailable(isAvail);
        isConcludable(isConclude);
    }

    @Override
    public String getName() {
	return "QuestAvailableEvent";
    }

    public void setQuestGiverOid(Long oid) {
	this.questGiverOid = oid;
    }
    public Long getQuestGiverOid() {
	return questGiverOid;
    }

    public void isAvailable(boolean flag) {
        this.isAvailableFlag = flag;
    }
    public boolean isAvailable() {
        return isAvailableFlag;
    }

    public void isConcludable(boolean flag) {
        this.isConcludableFlag = flag;
    }
    public boolean isConcludable() {
        return isConcludableFlag;
    }

    @Override
    public MVByteBuffer toBytes() {
	int msgId = Engine.getEventServer().getEventID(this.getClass());

	MVByteBuffer buf = new MVByteBuffer(32);
	buf.putLong(getObjectOid());
	buf.putInt(msgId);
	
	buf.putLong(getQuestGiverOid());
	buf.putBoolean(isAvailable());
        buf.putBoolean(isConcludable());
	buf.flip();
	return buf;
    }

    @Override
    protected void parseBytes(MVByteBuffer buf) {
	buf.rewind();

	long userId = buf.getLong();
	setObjectOid(userId);
	/* int msgId = */ buf.getInt();

	Long questGiverOid = buf.getLong();
	setQuestGiverOid(questGiverOid);

        isAvailable(buf.getBoolean());
        isConcludable(buf.getBoolean());
    }

    private Long questGiverOid = null;
    private boolean isAvailableFlag = false;
    private boolean isConcludableFlag = false;
}