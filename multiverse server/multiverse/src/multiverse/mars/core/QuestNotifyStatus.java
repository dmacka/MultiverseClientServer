package multiverse.mars.core;

import java.io.*;

/**
 * see QuestNotifyManager
 * this class describes whether the quest is available by the player
 * to 'take' or complete, with respect to an npc
 */
public class QuestNotifyStatus implements Serializable {

    public QuestNotifyStatus() {
    }
    
    public QuestNotifyStatus(boolean isAvail,
                             boolean isConcludable) {
        this.available = isAvail;
        this.concludable = isConcludable;
    }
    
    @Override
    public String toString() {
        return "[QuestNotifyStatus avail=" + available +
            ", concludable=" + concludable +
            "]";
    }

    public boolean available = false;
    public boolean concludable = false;
    private static final long serialVersionUID = 1L;
}
