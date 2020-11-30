package multiverse.mars.objects;

import java.io.Serializable;
import java.util.HashMap;
import java.util.Map;

import multiverse.mars.plugins.GroupPlugin;
import multiverse.server.plugins.WorldManagerClient;
import multiverse.server.util.Log;
import multiverse.server.util.Logger;
import multiverse.server.objects.Entity;

public class MarsGroupMember extends Entity {
    // properties
    private static final long serialVersionUID = 1L;
    private long _groupMemberOid;
    private long _groupOid;
    private String _groupMemberName;
    private Boolean _voiceEnabled = Boolean.FALSE;
    private Boolean _allowedSpeaker = Boolean.TRUE; // everyone can speak by default   
    private Map<String, Serializable> _entryStats = new HashMap<>();
    private static final Logger _log = new Logger("GroupMember");

    // constructor
    public MarsGroupMember(CombatInfo combatInfo, long groupOid) {
        super("");
        this._groupMemberOid = combatInfo.getOwnerOid();
        this._groupMemberName = WorldManagerClient.getObjectInfo(combatInfo
                .getOwnerOid()).name;
        this._groupOid = groupOid;
        SetGroupMemberStats(combatInfo);
    }

    // methods
    public long GetGroupMemberOid() {
        return this._groupMemberOid;
    }

    public String GetGroupMemberName() {
        return this._groupMemberName;
    }

    public long GetGroupOid(){
        return this._groupOid;
    }

    protected void SetGroupMemberStats(CombatInfo combatInfo) {
        for (String stat : GroupPlugin.GetRegisteredStats()) {
            _entryStats.put(stat, combatInfo.statGetCurrentValue(stat));
        }
    }

    public Serializable GetGroupMemberStat(String stat) {
        if (Log.loggingDebug) {
            _log.debug("MarsGroup.GetGroupMemberStat : " + stat + " = "
                    + _entryStats.get(stat));
        }
        return _entryStats.get(stat);
    }
    
    public void SetVoiceEnabled(Boolean value){        
        this._voiceEnabled = value;
    }
    
    public Boolean GetVoiceEnabled(){
        return this._voiceEnabled;
    }
    
    public void SetAllowedSpeaker(Boolean value){
        this._allowedSpeaker = value;
    }
    
    public Boolean GetAllowedSpeaker(){
        return this._allowedSpeaker;
    }
}
