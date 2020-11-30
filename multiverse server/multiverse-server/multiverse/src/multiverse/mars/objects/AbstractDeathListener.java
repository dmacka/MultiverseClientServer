package multiverse.mars.objects;

import multiverse.server.engine.*;
import multiverse.server.objects.*;
import multiverse.server.util.*;
import multiverse.mars.events.*;

import java.rmi.*;

public abstract class AbstractDeathListener extends AbstractEventListener {

    private static final long serialVersionUID = 1L;

    public AbstractDeathListener() throws RemoteException {
	super();
    }

    public AbstractDeathListener(String name) throws RemoteException {
	super();
	this.name = name;
    }

    protected String name = "";

    @Override
    public String getName() {
	return name;
    }

    protected boolean isDead = false;

    // handleDeath is called when the mob the listener is attached to dies
    protected abstract void handleDeath(Event event, MVObject target);
   
    // handleEvent will be called by multiple threads, so you must
    // make it thread-safe
    @Override
    public void handleEvent(Event event, MVObject target) {
	MarsStateEvent stateEvent = (MarsStateEvent)event;
	Long eventObjOid = stateEvent.getObjectOid();
        if (Log.loggingDebug)
            Log.debug("AbstractDeathListener: handleEvent target=" + target + " eventobj=" + eventObjOid);
	if (eventObjOid.equals(target.getOid())) {
	    Integer dead = stateEvent.getStateMap().get(MarsStates.Dead);
	    if (dead != null) {
		if ((dead == 1) && !isDead) {
		    isDead = true;
		    Log.debug("AbstractDeathListener: handleEvent object is dead");
		    handleDeath(event, target);
		}
	    }
	}
    }
}