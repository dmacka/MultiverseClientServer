package multiverse.mars.objects;

import java.util.HashMap;
import java.util.Map;

import multiverse.server.engine.Namespace;
import multiverse.server.objects.Entity;

/**
 * a subobject for a player that keeps track of the players quest states
 * @author cedeno
 *
 */
public class PlayerQuestStates extends Entity {

    public PlayerQuestStates() {
        super();
        setNamespace(Namespace.PLAYERQUESTSTATES);
        // TODO Auto-generated constructor stub
    }

    public PlayerQuestStates(String name) {
        super(name);
        setNamespace(Namespace.PLAYERQUESTSTATES);
        // TODO Auto-generated constructor stub
    }

    public PlayerQuestStates(Long oid) {
        super(oid);
        setNamespace(Namespace.PLAYERQUESTSTATES);
        // TODO Auto-generated constructor stub
    }

    public void addQuestState(QuestState qs) {
        lock.lock();
        try {
            questStateMap.put(qs.getQuestRef(), qs);
        }
        finally {
            lock.unlock();
        }
    }
    
    public QuestState getQuestState(String name) {
        lock.lock();
        try {
            return questStateMap.get(name);
        }
        finally {
            lock.unlock();
        }
    }
    
    public void setQuestStateMap(Map<String, QuestState> map) {
        lock.lock();
        try {
            this.questStateMap = new HashMap<>(map);
        }
        finally {
            lock.unlock();
        }
    }
    
    public Map<String, QuestState> getQuestStateMap() {
        lock.lock();
        try {
            return new HashMap<>(questStateMap);
        }
        finally {
            lock.unlock();
        }
    }
    
    private Map<String,QuestState> questStateMap = new HashMap<>();

    private static final long serialVersionUID = 1L;
}
