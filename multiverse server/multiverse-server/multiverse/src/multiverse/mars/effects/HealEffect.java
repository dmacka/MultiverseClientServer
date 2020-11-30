package multiverse.mars.effects;

import multiverse.mars.objects.*;
import multiverse.mars.core.*;
import java.util.*;

public class HealEffect extends MarsEffect {
    static Random random = new Random();

    public HealEffect(String name) {
        super(name);
    }

    // add the effect to the object
    @Override
    public void apply(EffectState state) {
	super.apply(state);
        int heal = minHeal;

        if (maxHeal > minHeal) {
            heal += random.nextInt(maxHeal - minHeal);
        }

        CombatInfo obj = state.getObject();
	if (heal == 0) {
	    return;
	}
        obj.statModifyBaseValue(getHealProperty(), heal);
        obj.sendStatusUpdate();
    }

    // perform the next periodic pulse for this effect on the object
    @Override
    public void pulse(EffectState state) {
	super.pulse(state);
        int heal = minPulseHeal;

        if (maxPulseHeal > minPulseHeal) {
            heal += random.nextInt(maxPulseHeal - minPulseHeal);
        }

	if (heal == 0) {
	    return;
	}
        CombatInfo obj = state.getObject();
        obj.statModifyBaseValue(getHealProperty(), heal);
        obj.sendStatusUpdate();
    }

    public int getMinInstantHeal() { return minHeal; }
    public void setMinInstantHeal(int hps) { minHeal = hps; }
    protected int minHeal = 0;

    public int getMaxInstantHeal() { return maxHeal; }
    public void setMaxInstantHeal(int hps) { maxHeal = hps; }
    protected int maxHeal = 0;

    public int getMinPulseHeal() { return minPulseHeal; }
    public void setMinPulseHeal(int hps) { minPulseHeal = hps; }
    protected int minPulseHeal = 0;

    public int getMaxPulseHeal() { return maxPulseHeal; }
    public void setMaxPulseHeal(int hps) { maxPulseHeal = hps; }
    protected int maxPulseHeal = 0;

    public String getHealProperty() { return healProperty; }
    public void setHealProperty(String property) { healProperty = property; }
    protected String healProperty = CombatInfo.COMBAT_PROP_HEALTH;
}
