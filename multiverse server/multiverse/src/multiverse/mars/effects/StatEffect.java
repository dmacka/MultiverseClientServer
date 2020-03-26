package multiverse.mars.effects;

import multiverse.mars.objects.*;
import multiverse.mars.core.*;
import java.util.*;

public class StatEffect extends MarsEffect {
    public StatEffect(String name) {
	super(name);
	isPeriodic(false);
	isPersistent(true);
    }

    public void setStat(String stat, int adj) {
	statMap.put(stat, adj);
    }
    public Integer getStat(String stat) {
	return statMap.get(stat);
    }
    protected Map<String, Integer> statMap = new HashMap<>();

    // add the effect to the object
    @Override
    public void apply(EffectState state) {
	super.apply(state);
	CombatInfo obj = state.getObject();
	for (Map.Entry<String, Integer> entry : statMap.entrySet()) {
	    obj.statAddModifier(entry.getKey(), state, entry.getValue());
	}
    }

    // remove the effect from the object
    @Override
    public void remove(EffectState state) {
	CombatInfo obj = state.getObject();
	for (Map.Entry<String, Integer> entry : statMap.entrySet()) {
	    obj.statRemoveModifier(entry.getKey(), state);
	}
	super.remove(state);
    }

    // perform the next periodic pulse for this effect on the object
    @Override
    public void pulse(EffectState state) {
	super.pulse(state);
    }
}