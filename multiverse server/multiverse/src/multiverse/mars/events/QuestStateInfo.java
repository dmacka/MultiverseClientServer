package multiverse.mars.events;

import multiverse.server.engine.*;
import multiverse.server.network.*;
import multiverse.mars.objects.*;
import java.util.*;

public class QuestStateInfo extends Event {
    public QuestStateInfo() {
	super();
    }

    public QuestStateInfo(MVByteBuffer buf, ClientConnection con) {
	super(buf,con);
    }

    public QuestStateInfo(MarsMob marsMob, QuestState questState) {
	super();
        setPlayerOid(marsMob.getOid());
        // FIXME:
        //setQuestId(questState.getQuestId());
        setObjectiveStatus(questState.getObjectiveStatus());
    }

    @Override
    public String getName() {
	return "QuestStateInfo";
    }

    // i use a long here so i dont have to lock around it
    void setPlayerOid(Long id) {
        this.playerId = id;
    }
    void setQuestId(Long id) {
        this.questId = id;
    }
    void setObjectiveStatus(List<String> objStatus) {
        this.objStatus = objStatus;
    }

    @Override
    public MVByteBuffer toBytes() {
	int msgId = Engine.getEventServer().getEventID(this.getClass());

	MVByteBuffer buf = new MVByteBuffer(500);
	buf.putLong(playerId); 
	buf.putInt(msgId);
	
	buf.putLong(questId);
        buf.putInt(objStatus.size());
        Iterator<String> iter = objStatus.iterator();
        while (iter.hasNext()) {
            buf.putString(iter.next());
        }
	buf.flip();
	return buf;
    }

    @Override
    protected void parseBytes(MVByteBuffer buf) {
	buf.rewind();
	setPlayerOid(buf.getLong());
	/* int msgId = */ buf.getInt();
        setQuestId(buf.getLong());

        // read in the obj status list
        List<String> l = new LinkedList<>();
        int len = buf.getInt();
        while (len>0) {
            l.add(buf.getString());
            len--;
        }
        setObjectiveStatus(l);
    }

    Long playerId = null;
    Long questId = null;
    List<String> objStatus = null;
}
