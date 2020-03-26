package multiverse.mars.events;

import multiverse.mars.objects.*;
import multiverse.server.engine.*;
import multiverse.server.objects.*;
import multiverse.server.network.*;
import multiverse.server.util.*;

/**
 * the client is turning in a quest
 */
public class ConcludeQuest extends Event {
    public ConcludeQuest() {
	super();
    }

    public ConcludeQuest(MVByteBuffer buf, ClientConnection con) {
	super(buf, con);
    }

    public ConcludeQuest(MarsMob player, 
                         MarsMob questNpc) {
	super(player);
	setQuestNpcOid(questNpc.getOid());
    }

    @Override
    public String getName() {
	return "ConcludeQuest";
    }

    public MarsMob getQuestNpc() {
	try {
	    return MarsMob.convert(MVObject.getObject(questNpcOid));
	}
	catch(MVRuntimeException e) {
	    throw new RuntimeException("concludequest", e);
	}
    }
    public Long getQuestNpcOid() {
	return this.questNpcOid;
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
	buf.putLong(getQuestNpc().getOid());
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
