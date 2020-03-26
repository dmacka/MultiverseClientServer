package multiverse.mars.events;

import multiverse.server.engine.*;
import multiverse.server.network.*;
import multiverse.mars.objects.*;

public class RemoveQuestResponse extends Event {
    public RemoveQuestResponse() {
	super();
    }

    public RemoveQuestResponse(MVByteBuffer buf, ClientConnection con) {
	super(buf,con);
    }

    public RemoveQuestResponse(QuestState questState) {
	super();
        setPlayerOid(questState.getPlayerOid());
        //FIXME:
        //setQuestId(questState.getQuestId());
    }

    @Override
    public String getName() {
	return "RemoveQuestResponse";
    }

    void setPlayerOid(Long id) {
        this.playerId = id;
    }
    void setQuestId(Long id) {
        this.questId = id;
    }

    @Override
    public MVByteBuffer toBytes() {
	int msgId = Engine.getEventServer().getEventID(this.getClass());

	MVByteBuffer buf = new MVByteBuffer(20);
	buf.putLong(playerId); 
	buf.putInt(msgId);
	buf.putLong(questId);
	buf.flip();
	return buf;
    }

    @Override
    protected void parseBytes(MVByteBuffer buf) {
	buf.rewind();
	setPlayerOid(buf.getLong());
	/* int msgId = */ buf.getInt();
        setQuestId(buf.getLong());
    }

    Long playerId = null;
    Long questId = null;
}
