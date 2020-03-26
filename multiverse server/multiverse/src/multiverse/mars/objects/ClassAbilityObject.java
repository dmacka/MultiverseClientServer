package multiverse.mars.objects;

import multiverse.mars.plugins.ClassAbilityClient;
import multiverse.mars.plugins.ClassAbilityPlugin;
import multiverse.server.engine.Engine;
import multiverse.server.engine.Namespace;
import multiverse.server.messages.PropertyMessage;
import multiverse.server.objects.Entity;
import multiverse.server.objects.ObjectType;
import multiverse.server.plugins.WorldManagerClient.TargetedPropertyMessage;

/**
 * 
 * This class is meant to be the generated object for the Player that holds the stats for skills/abilities that a 
 * player has.
 * 
 * @author Judd
 *
 */
public class ClassAbilityObject extends Entity {
	
	String playerclass;
	
	/**
	 *
	 */
	private static final long serialVersionUID = 1L;
	
	public ClassAbilityObject() {
        super();
        setNamespace(Namespace.CLASSABILITY);
    }

    public ClassAbilityObject(Long objOid) {
        super(objOid);
        setNamespace(Namespace.CLASSABILITY);
    }

        @Override
    public String toString() {
        return "[Entity: " + getName() + ":" + getOid() + "]";
    }
	
        @Override
    public ObjectType getType() {
        return ObjectType.intern((short)11, "ClassAbilityObject");
    }
    
    public String getPlayerClass(){
    	return playerclass;
    }
    
    public void setPlayerClass(String playerclassname){
    	playerclass = playerclassname;
    }
    
     
    public void updateBaseStat(String name, int modifier){
    	MarsStat stat = (MarsStat)getProperty(name + "_exp");
    	MarsStat rank = (MarsStat)getProperty(name + "_rank");
    	if(stat == null || rank == null){
    	    log.warn("ClassAbilityObject.updateBaseStat - player does nt have the skill/ability " + name);
    	    return;
    	}
    	if (rank.base < rank.max){
	    	stat.modifyBaseValue(modifier);
	    	ClassAbilityClient.sendXPUpdate(this.getOid(), stat.getName(), stat.getCurrentValue());
	    	ClassAbilityPlugin.lookupStatDef(name + "_rank").update(stat, this);
	    	statSendUpdate(false);
    	}
    }
    
    public void statSendUpdate(boolean sendAll) {
        statSendUpdate(sendAll, null);
    }

    public void statSendUpdate(boolean sendAll, Long targetOid) {
		lock.lock();
		try {
	            PropertyMessage propMsg = null;
	            TargetedPropertyMessage targetPropMsg = null;
	            if (targetOid == null)
	                propMsg = new PropertyMessage(getOid());
	            else
	                targetPropMsg =
	                    new TargetedPropertyMessage(targetOid,getOid());
	            int count = 0;
		    for (Object value : getPropertyMap().values()) {
			if (value instanceof MarsStat) {
			    MarsStat stat = (MarsStat) value;
			    if (sendAll || stat.isDirty()) {
	                        if (propMsg != null)
	                            propMsg.setProperty(stat.getName(), stat.getCurrentValue());
	                        else{
	                            targetPropMsg.setProperty(stat.getName(), stat.getCurrentValue());
	                        }
	                        if (! sendAll)
	                            stat.setDirty(false);
	                        count++;
			    }
			}
		    }
		    if (count > 0) {
			Engine.getPersistenceManager().setDirty(this);
	                if (propMsg != null)
	                    Engine.getAgent().sendBroadcast(propMsg);
	                else
	                    Engine.getAgent().sendBroadcast(targetPropMsg);
		    }
		}
		finally {
		    lock.unlock();
		}
    }

}
