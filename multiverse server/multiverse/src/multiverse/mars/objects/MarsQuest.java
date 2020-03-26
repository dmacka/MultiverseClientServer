package multiverse.mars.objects;

import multiverse.server.objects.*;
import multiverse.server.engine.*;
import java.util.*;

abstract public class MarsQuest extends Entity {

    private static final long serialVersionUID = 1L;
    public MarsQuest() {
        super();
        // For now, put establish the quest oid in this constructor.
        // When quests are persisted, however, the quest oid will come
        // from the one-arg constructor
        setOid(Engine.getOIDManager().getNextOid());
        setNamespace(Namespace.QUEST);
    }

    public void setDesc(String desc) {
        this.desc = desc;
    }
    public String getDesc() {
        return desc;
    }
    String desc = null;

    public void setObjective(String s) {
	this.objective = s;
    }
    public String getObjective() {
	return objective;
    }
    String objective = null;

    public void setCashReward(int reward) {
	cashReward = reward;
    }
    public int getCashReward() {
	return cashReward;
    }
    int cashReward = 0;

    /**
     * returns a list item template names
     * @return 
     */
    public List<String> getRewards() {
        return itemRewards;
    }
    public void setRewards(List<String> rewards) {
        itemRewards = rewards;
    }
    public void addReward(String reward) {
        lock.lock();
        try {
            itemRewards.add(reward);
        }
        finally {
            lock.unlock();
        }
    }
    List<String> itemRewards = new LinkedList<>();

    public List<String> getQuestPrereqs() {
	return questPrereqs;
    }
    public void setQuestPrereqs(List<String> prereqs) {
	questPrereqs = prereqs;
    }
    public void addQuestPrereq(String questRef) {
	questPrereqs.add(questRef);
    }
    List<String> questPrereqs = new LinkedList<>();

    // quest that is immediately offered when this quest is concluded
    public MarsQuest getChainQuest() {
        return chainQuest;
    }
    public void setChainQuest(MarsQuest chainQuest) {
        this.chainQuest = chainQuest;
    }
    MarsQuest chainQuest = null;

    public abstract QuestState generate(Long playerOid);
}
