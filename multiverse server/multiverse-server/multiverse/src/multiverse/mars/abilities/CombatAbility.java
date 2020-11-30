package multiverse.mars.abilities;

import java.util.HashMap;
import java.util.Map;
import multiverse.mars.core.MarsAbility;
import multiverse.mars.core.MarsEffect;
import multiverse.mars.plugins.CombatPlugin;
import multiverse.server.util.Log;

public class CombatAbility extends MarsAbility {
    protected MarsEffect activationEffect;
    public CombatAbility(String name) {
        super(name);
        this.activationEffect = null;
    }

    public Map<?,?> resolveHit(State state) {
	return new HashMap<>(1);
    }

    public MarsEffect getActivationEffect() { return activationEffect; }
    public void setActivationEffect(MarsEffect effect) { this.activationEffect = effect; }

    /**
     *
     * @param state
     */
    @Override
    public void completeActivation(State state) {
        super.completeActivation(state);

        //Add attacker to target's list of attackers
        CombatPlugin.addAttacker(state.getTarget().getOid(), state.getObject().getOid());
        state.getObject().setCombatState(true);        
        
	Map<?,?> params = resolveHit(state);
	Log.debug("CombatAbility.completeActivation: params=" + params);
        MarsEffect.applyEffect(activationEffect, state.getObject(), state.getTarget(), params);
    }
}