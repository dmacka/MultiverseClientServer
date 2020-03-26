package multiverse.mars.events;

import multiverse.mars.objects.*;
import multiverse.server.engine.*;
import multiverse.server.objects.*;
import multiverse.server.network.*;
import multiverse.server.util.*;

/**
 * the client is responding to a quest, saying it will accept or decline
 */
public class QuestResponse extends Event {
    public QuestResponse() {
	super();
    }

    public QuestResponse(MVByteBuffer buf, ClientConnection con) {
	super(buf, con);
    }

    public QuestResponse(MarsMob player, 
                         MarsMob questNpc,
                         long questId,
                         boolean response) {
	super(player);
        setQuestId(questId);
        setResponse(response);
        setQuestNpcOid(questNpc.getOid());
    }

    @Override
    public String getName() {
	return "QuestResponse";
    }

    public void setQuestId(long id) {
        this.questId = id;
    }
    public long getQuestId() {
        return questId;
    }
    long questId = -1;

    public void setResponse(boolean response) {
        this.response = response;
    }
    public boolean getResponse() {
        return response;
    }
    boolean response;

    public MarsMob getQuestNpc() {
	try {
	    return MarsMob.convert(MVObject.getObject(questNpcOid));
	}
	catch(MVRuntimeException e) {
	    throw new RuntimeException("QuestResponse", e);
	}
    }
    public Long getQuestNpcOid() {
	return questNpcOid;
    }
    public void setQuestNpcOid(Long questNpcOid) {
	this.questNpcOid = questNpcOid;
    }

    Long questNpcOid = null;
    

    @Override
    public MVByteBuffer toBytes() {
	int msgId = Engine.getEventServer().getEventID(this.getClass());

	MVByteBuffer buf = new MVByteBuffer(32);
	buf.putLong(getObjectOid()); 
	buf.putInt(msgId);
        buf.putLong(getQuestNpc().getOid());
	buf.putLong(getQuestId());
        buf.putInt(getResponse() ? 1 : 0);
	buf.flip();
	return buf;
    }

    @Override
    protected void parseBytes(MVByteBuffer buf) {
	buf.rewind();
	long playerId = buf.getLong();
	setObjectOid(playerId);
	/* int msgId = */ buf.getInt();
        setQuestNpcOid(buf.getLong());
        setQuestId(buf.getLong());
        setResponse(buf.getInt() == 1);
    }
}
