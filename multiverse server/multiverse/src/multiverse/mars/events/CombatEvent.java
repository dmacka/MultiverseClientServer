package multiverse.mars.events;

import multiverse.mars.objects.*;
import multiverse.server.engine.*;
import multiverse.server.network.*;
import multiverse.server.util.*;

public class CombatEvent extends Event {
    public CombatEvent() {
	super();
    }

    public CombatEvent(MVByteBuffer buf, ClientConnection con) {
	super(buf, con);
    }

    public CombatEvent(MarsMob attacker, 
		       MarsObject target, 
		       String attackType) {
	super(target);
	setAttackType(attackType);
	setAttacker(attacker);
    }

    @Override
    public String getName() {
	return "CombatEvent";
    }

    @Override
    public MVByteBuffer toBytes() {
	throw new MVRuntimeException("not implemented");
    }

    @Override
    protected void parseBytes(MVByteBuffer buf) {
	throw new MVRuntimeException("not implemented");
    }

    public void setAttacker(MarsMob attacker) {
	this.attacker = attacker;
    }
    public MarsMob getAttacker() {
	return attacker;
    }

    public void setAttackType(String attackType) {
	this.attackType = attackType;
    }
    public String getAttackType() {
	return attackType;
    }

    private String attackType = null;
    private MarsMob attacker = null;
}