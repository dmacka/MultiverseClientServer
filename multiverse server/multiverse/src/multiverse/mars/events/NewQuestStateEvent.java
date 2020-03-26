package multiverse.mars.events;

import multiverse.mars.objects.*;
import multiverse.server.engine.*;
import multiverse.server.network.*;
import multiverse.server.util.*;
import java.io.*;

/**
 * the mobserver made a new quest state, probably a user accepted a quest.
 * so now we serialize and give the world server the quest state object
 * so it can attach it to the user object
 */
public class NewQuestStateEvent extends Event {
    public NewQuestStateEvent() {
	super();
    }

    public NewQuestStateEvent(MVByteBuffer buf, ClientConnection con) {
	super(buf, con);
    }

    public NewQuestStateEvent(MarsMob player, 
                              QuestState questState) {
	super(player);
        try {
            ByteArrayOutputStream ba = new ByteArrayOutputStream();
            ObjectOutputStream os = new ObjectOutputStream(ba);
            os.writeObject(questState);
            setData(ba.toByteArray());
        }
        catch(IOException e) {
            throw new RuntimeException("newqueststateevent" , e);
        }
    }

    @Override
    public String getName() {
	return "NewQuestStateEvent";
    }

    public byte[] getData() {
        return questStateData;
    }
    public void setData(byte[] questStateData) {
        this.questStateData = questStateData;
    }

    @Override
    public MVByteBuffer toBytes() {
	int msgId = Engine.getEventServer().getEventID(this.getClass());

	MVByteBuffer buf = new MVByteBuffer(20);
	buf.putLong(getObjectOid()); 
	buf.putInt(msgId);

	byte[] data = getData();
	if (data.length > 10000) {
	    throw new MVRuntimeException("NewQuestStateEvent.toBytes: overflow");
	}
	buf.putInt(data.length);
	buf.putBytes(data, 0, data.length);

	buf.flip();
	return buf;
    }

    @Override
    protected void parseBytes(MVByteBuffer buf) {
	buf.rewind();
	long playerId = buf.getLong();
	setObjectOid(playerId);
	/* int msgId = */ buf.getInt();

	// data length
	int dataLen = buf.getInt();
	byte[] data = new byte[dataLen];
	buf.getBytes(data, 0, dataLen);
	setData(data);
    }

    protected byte[] questStateData = null;
}
