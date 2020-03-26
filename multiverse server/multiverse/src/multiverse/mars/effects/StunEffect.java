package multiverse.mars.effects;

import multiverse.mars.core.*;

public class StunEffect extends MarsEffect {
    public StunEffect(String name) {
	super(name);
	isPeriodic(false);
	isPersistent(true);
    }

    // add the effect to the object
    @Override
    public void apply(EffectState state) {
	super.apply(state);
    }

    // remove the effect from the object
    @Override
    public void remove(EffectState state) {
	super.remove(state);
    }

    // perform the next periodic pulse for this effect on the object
    @Override
    public void pulse(EffectState state) {
	super.pulse(state);
    }
}