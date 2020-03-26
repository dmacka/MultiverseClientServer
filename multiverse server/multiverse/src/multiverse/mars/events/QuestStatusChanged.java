package multiverse.mars.events;

// import multiverse.mars.objects.*;
// import multiverse.server.engine.*;
// import multiverse.server.objects.*;
// import multiverse.server.network.*;
// import multiverse.server.network.rdp.*;
// import multiverse.server.util.*;

/**
 * the user's quest state has changed.  they may have dropped a quest
 * or completed a quest.
 * the server needs to modify what the mobs around the user
 */
// public class ConcludeQuest extends Event {
//     public ConcludeQuest() {
// 	super();
//     }

//     public ConcludeQuest(MVByteBuffer buf, RDPConnection con) {
// 	super(buf, con);
//     }

//     public ConcludeQuest(MarsMob player, 
//                          MarsMob questNpc) {
// 	super(player);
// 	setQuestNpc(questNpc);
//     }

//     public String getName() {
// 	return "ConcludeQuest";
//     }

//     public MarsMob getQuestNpc() {
// 	return questNpc;
//     }
//     public void setQuestNpc(MarsMob questNpc) {
// 	this.questNpc = questNpc;
//     }

//     public MVByteBuffer toBytes() {
// 	int msgId = Engine.getEventServer().getEventID(this.getClass());

// 	MVByteBuffer buf = new MVByteBuffer(5000);
// 	buf.putLong(getObject().getOid()); 
// 	buf.putInt(msgId);
// 	buf.putLong(getQuestNpc().getOid());
// 	buf.flip();
// 	return buf;
//     }

//     protected void parseBytes(MVByteBuffer buf) {
// 	buf.rewind();
// 	long playerId = buf.getLong();
// 	setObject(MVObject.getObject(playerId));
// 	int msgId = buf.getInt();
// 	long questNpcId = buf.getLong();
// 	setQuestNpc(MarsMob.convert(MVObject.getObject(questNpcId)));
//     }

//     protected MarsMob questNpc = null;
// }
