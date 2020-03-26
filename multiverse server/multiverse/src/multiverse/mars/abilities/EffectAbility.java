package multiverse.mars.abilities;

import multiverse.mars.core.MarsAbility;
import multiverse.mars.core.MarsEffect;

public class EffectAbility extends MarsAbility {
    protected MarsEffect activationEffect;
    protected MarsEffect channelEffect;
    protected MarsEffect activeEffect;

    public EffectAbility(String name) {
        super(name);
        this.activeEffect = null;
        this.channelEffect = null;
        this.activationEffect = null;
    }

    public MarsEffect getActivationEffect() { return activationEffect; }
    public void setActivationEffect(MarsEffect effect) { this.activationEffect = effect; }

    public MarsEffect getChannelEffect() { return channelEffect; }
    public void setChannelEffect(MarsEffect effect) { this.channelEffect = effect; }

    public MarsEffect getActiveEffect() { return activeEffect; }
    public void setActiveEffect(MarsEffect effect) { this.activeEffect = effect; }

    @Override
    public void completeActivation(State state) {
        super.completeActivation(state);
        MarsEffect.applyEffect(activationEffect, state.getObject(), state.getTarget());
    }

    @Override
    public void pulseChannelling(State state) {
        super.pulseChannelling(state);
        MarsEffect.applyEffect(channelEffect, state.getObject(), state.getTarget());
    }

    @Override
    public void pulseActivated(State state) {
        super.pulseActivated(state);
        MarsEffect.applyEffect(activeEffect, state.getObject(), state.getTarget());
    }
}