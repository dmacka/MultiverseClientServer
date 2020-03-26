package multiverse.mars.effects;

import multiverse.mars.objects.*;
import multiverse.mars.core.*;
import multiverse.mars.plugins.CombatPlugin;

public class TeachAbilityEffect extends MarsEffect {
    public TeachAbilityEffect(String name) {
	super(name);
	isPeriodic(false);
	isPersistent(false);
    }

    public TeachAbilityEffect(String name, String abilityName) {
	super(name);
	isPeriodic(false);
	isPersistent(false);
	setAbilityName(abilityName);
    }

    public String getAbilityName() { return abilityName; }
    public void setAbilityName(String name) { abilityName = name; }
    protected String abilityName = null;

    public String getCategory() { return category; }
    public void setCategory(String name) { category = name; }
    protected String category = null;

    // add the effect to the object
    @Override
    public void apply(EffectState state) {
	super.apply(state);
	CombatInfo mob = state.getObject();
	MarsAbility ability = Mars.AbilityManager.get(abilityName);
	mob.addAbility(ability.getName());
	CombatPlugin.sendAbilityUpdate(mob);
    }
}
