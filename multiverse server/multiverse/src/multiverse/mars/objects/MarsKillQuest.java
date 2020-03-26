package multiverse.mars.objects;

import java.io.*;

public class MarsKillQuest extends MarsQuest {
    public MarsKillQuest() {
        super();
    }

    public void setKillGoal(String mobName, int count) {
        setKillGoal(new KillGoal(mobName, count));
    }

    public void setKillGoal(KillGoal goal) {
        this.goal = goal;
    }
    
    public KillGoal getKillGoal() {
        return goal;
    }

    @Override
    public QuestState generate(Long playerOid) {
	KillQuestState qs = new KillQuestState(this, playerOid);
	qs.setKillGoal(getKillGoal());
	return qs;
    }

    public static class KillGoal implements Serializable {
        public KillGoal() {
        }

        public KillGoal(String name, int count) {
            setName(name);
            setCount(count);
        }

        @Override
        public String toString() {
            return "[KillGoal: mobName=" + getName() +
                ", targetCount=" + getCount() + "]";
        }
        public void setName(String name) {
            this.name = name;
        }
        public String getName() {
            return name;
        }

        public void setCount(int count) {
            this.count = count;
        }
        public int getCount() {
            return count;
        }

        private String name = null;
        private int count = -1;
        private static final long serialVersionUID = 1L;
    }

    private KillGoal goal = null;

    private static final long serialVersionUID = 1L;
}
