package multiverse.mars.events;

import multiverse.mars.objects.*;
import multiverse.server.engine.*;
import multiverse.server.network.*;

/**
 * the client is asking for what quests this questnpc has for the user
 * see serverrequestinfo for what the world server sends to the
 * mobserver to find out
 */
public class RequestQuestInfo extends Event {
    public RequestQuestInfo() {
	super();
    }

    public RequestQuestInfo(MVByteBuffer buf, ClientConnection con) {
	super(buf, con);
    }

    public RequestQuestInfo(MarsMob player, 
			    MarsMob questNpc) {
	super(player);
	setQuestNpcOid(questNpc.getOid());
    }

    @Override
    public String getName() {
	return "RequestQuestInfo";
    }

    public Long getQuestNpcOid() {
	return questNpcOid;
    }
    public void setQuestNpcOid(Long questNpcOid) {
	this.questNpcOid = questNpcOid;
    }

    @Override
    public MVByteBuffer toBytes() {
	int msgId = Engine.getEventServer().getEventID(this.getClass());

	MVByteBuffer buf = new MVByteBuffer(20);
	buf.putLong(getObjectOid()); 
	buf.putInt(msgId);
	buf.putLong(getQuestNpcOid());
	buf.flip();
	return buf;
    }

    @Override
    protected void parseBytes(MVByteBuffer buf) {
	buf.rewind();
	long playerId = buf.getLong();
	setObjectOid(playerId);

	/* int msgId = */ buf.getInt();

	long questNpcId = buf.getLong();
	setQuestNpcOid(questNpcId);
    }

    protected Long questNpcOid = null;
}
