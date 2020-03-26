package multiverse.mars.events;

import multiverse.server.events.*;
import multiverse.server.network.*;
import multiverse.server.util.*;
import multiverse.mars.objects.*;

public class MarsStateEvent extends StateEvent {
    public MarsStateEvent() {
	super();
    }

    public MarsStateEvent(MVByteBuffer buf, ClientConnection con) {
	super(buf,con);
    }

    public MarsStateEvent(MarsMob marsMob, boolean fullState) {
	super();
	setObject(marsMob);
	if (fullState) {
	    addState(MarsStates.Dead.toString(), (marsMob.isDead() ? 1 : 0));

            boolean combatState = (marsMob.getAutoAttackTarget() != null);
	    addState(MarsStates.Combat.toString(), (combatState ? 1 : 0));
            addState(MarsStates.Attackable.toString(),
		     (marsMob.attackable() ? 1 : 0));
            addState(MarsStates.Stunned.toString(),
		     (marsMob.isStunned() ? 1 : 0));

            if (Log.loggingDebug)
                Log.debug("MarsStateEvent: added state of mob " +
                          marsMob.getName() + 
                          ", deadstate=" + (marsMob.isDead() ? 1 : 0) +
                          ", combatState=" + combatState);
	}
    }

    @Override
    public String getName() {
	return "MarsStateEvent";
    }
}