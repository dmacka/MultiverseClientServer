package multiverse.mars.events;

import multiverse.server.engine.*;
import multiverse.server.network.*;
import multiverse.server.util.*;
import java.util.*;
import java.util.concurrent.locks.*;

public class QuestLogInfo extends Event {
    public QuestLogInfo() {
	super();
    }

    public QuestLogInfo(MVByteBuffer buf, ClientConnection con) {
	super(buf,con);
    }

//    public QuestLogInfo(MarsMob marsMob, MarsQuest quest) {
//	super();
//        setPlayerOid(marsMob.getOid());
//        setQuestId(quest.getOid());
//        setTitle(quest.getName());
//        setDesc(quest.getDesc());
//        setObjective(quest.getObjective());
//
//        List<QuestInfo.Reward> rewards = new LinkedList<QuestInfo.Reward>();
//        List<ItemTemplate> rewardTempls = quest.getRewards();
//        for (ItemTemplate itemTempl : rewardTempls) {
//            QuestInfo.Reward reward = 
//                new QuestInfo.Reward(itemTempl.getName(),
//                                     itemTempl.getIcon(),
//                                     1);
//            rewards.add(reward);
//        }
//        setRewards(rewards);
//    }

    @Override
    public String getName() {
	return "QuestLogInfo";
    }

    // i use a long here so i dont have to lock around it
    void setPlayerOid(Long id) {
        this.playerId = id;
    }
    void setQuestId(Long id) {
        this.questId = id;
    }
    void setTitle(String title) {
        this.title = title;
    }
    void setDesc(String desc) {
        this.desc = desc;
    }
    void setObjective(String obj) {
        this.obj = obj;
    }

    public void setRewards(List<QuestInfo.Reward> rewards) {
        lock.lock();
        try {
            this.rewards = new LinkedList<>(rewards);
        }
        finally {
            lock.unlock();
        }
    }
    public List<QuestInfo.Reward> getRewards() {
        lock.lock();
        try {
            return new LinkedList<>(rewards);
        }
        finally {
            lock.unlock();
        }
    }

    @Override
    public MVByteBuffer toBytes() {
	int msgId = Engine.getEventServer().getEventID(this.getClass());

	MVByteBuffer buf = new MVByteBuffer(500);
	buf.putLong(playerId); 
	buf.putInt(msgId);
	
	buf.putLong(questId);
	buf.putString(title);
	buf.putString(desc);
	buf.putString(obj);

        lock.lock();
        try {
            int size = rewards.size();
            buf.putInt(size);
            Iterator<QuestInfo.Reward> iter = rewards.iterator();
            while(iter.hasNext()) {
                QuestInfo.Reward reward = iter.next();
                buf.putString(reward.name);
                buf.putString(reward.icon);
                buf.putInt(reward.count);
            }
        }
        finally {
            lock.unlock();
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
        setTitle(buf.getString());
        setDesc(buf.getString());
        setObjective(buf.getString());

        lock.lock();
        try {
            this.rewards = new LinkedList<>();
            int size = buf.getInt(); // num rewards
            while (size > 0) {
                String name = buf.getString();
                String icon = buf.getString();
                int count = buf.getInt();
                QuestInfo.Reward reward = 
                    new QuestInfo.Reward(name, icon, count);
                rewards.add(reward);
                size--;
            }
        }
        finally {
            lock.unlock();
        }
    }

    Long playerId;
    Long questId;
    String title;
    String desc;
    String obj;
    List<QuestInfo.Reward> rewards = null;
    transient Lock lock = LockFactory.makeLock("QuestLogInfo");
}
