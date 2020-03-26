package multiverse.mars.core;

import multiverse.server.util.*;
import multiverse.mars.objects.*;

/**
 * an activate hook attached to skill scrolls.
 * when the scroll is activated, the mob gets the skill added to his list
 */
public class SkillActivateHook implements ActivateHook {
    public SkillActivateHook() {
    }

    /**
     * what is the skill you get for this
     * @param skill
     */
    public SkillActivateHook(MarsSkill skill) {
        setSkill(skill);
    }

    public void setSkill(MarsSkill skill) {
        this.skill = skill;
    }
    public MarsSkill getSkill() {
        return skill;
    }

    /**
     * returns whether the item was successfully activated
     * @param activatorOid
     * @param targetOid
     */
    @Override
    public boolean activate(Long activatorOid, MarsItem item, Long targetOid) {
        if (Log.loggingDebug)
            Log.debug("SkillActivateHook.activate: activator=" + activatorOid +
                      ", skill=" + getSkill().getName());
//         player.addSkill(getSkill());
//         player.sendServerInfo("You have learned the skill " + 
//                               getSkill().getName());

        // destroy the item
//         MarsItem item = player.findItem(item.getTemplate());
//         if (item == null) {
//             throw new MVRuntimeException("SkillActivateHook.activate: could not find the item with matching template");
//         }
//         if (! player.destroyItem(item)) {
//             throw new MVRuntimeException("SkillActivateHook.activate: destroyItem failed");
//         }
        return true;
    }

    protected MarsSkill skill = null;

    private static final long serialVersionUID = 1L;
}
