package multiverse.mars.core;

import multiverse.mars.objects.LevelingMap;
import multiverse.server.util.*;
import java.io.*;

public class MarsSkill implements Serializable {

    public static MarsSkill NullSkill = 
        new MarsSkill("NullSkill");

    public MarsSkill() {
    }

    public MarsSkill(String name) {
        setName(name);
    }

    @Override
    public String toString() {
        return "[MarsSkill: " + getName() + "]";
    }

    @Override
    public boolean equals(Object other) {
        MarsSkill otherSkill = (MarsSkill) other;
        boolean val = getName().equals(otherSkill.getName());
        return val;
    }

    @Override
    public int hashCode() {
        return getName().hashCode();
    }

    public void setName(String name) {
        this.name = name;
    }
    public String getName() {
        return name;
    }
    String name = null;

    public void setSkillCostMultiplier(int c) {
        skillCost = c;
    }
    public int getSkillCostMultiplier() {
        return skillCost;
    }
    int skillCost = 1;

    /**
     * each level costs 1000 xp
     * @param c
     */
    public void setLevelCostMultiplier(int c) {
        levelCost = c;
    }
    public int getLevelCostMultiplier() {
        return levelCost;
    }
    int levelCost = 1000;

    /**
     * returns the amount of total xp required to be at level 'skillLevel'
     * for this skill
     * @param level
     * @return 
     */
    public int xpRequired(int level) {
        return (level * (level + 1)) / 2 * levelCost * skillCost;
    }

    /**
     * returns the level you have in this skill if you have the xp passed in
     * @param xp
     * @return 
     */
    public int getLevel(int xp) {
        // do real math here sometime
        int i=0;
        while (xpRequired(i+1) < xp) {
            i++;
        }
        if (Log.loggingDebug)
            Log.debug("MarsSkill.getLevel: skill=" + getName() + 
                      ", level=" + i);
        return i;
    }

    String defaultAbility = null;
    int exp_per_use = 0;
    LevelingMap lm = new LevelingMap();
    int exp_max = 100;
    int rank_max = 3;

    public void setDefaultAbility(String ability) {
        defaultAbility = ability;
    }

    public String getDefaultAbility() {
        return defaultAbility;
    }
    
     /**
     * -Experience system component-
     * 
     * Returns the amount of experience to be gained after a successful use of
     * this skill.
     * @return 
     */
    public int getExperiencePerUse() {
        return exp_per_use;
    }

    /**
     * -Experience system component-
     * 
     * Sets the amount of experience that should be gained after a successful
     * use of this skill.
     * <p>
     * NOTE: Skill increases are meant to be minimal since there will generally
     * be many abilities increasing the skill level.
     * @param xp
     */
    public void setExperiencePerUse(int xp) {
        exp_per_use = xp;
    }

    public void setLevelingMap(LevelingMap lm) {
        this.lm = lm;
    }

    public LevelingMap getLevelingMap() {
        return this.lm;
    }

    /**
     * -Experience system component-
     * 
     * Returns the default max experience required before increasing this skills
     * level.
     * @return 
     */
    public int getBaseExpThreshold() {
        return exp_max;
    }

    /**
     * -Experience system component-
     * 
     * Sets the default max experience required to increase the skills level.
     * @param max
     */
    public void setBaseExpThreshold(int max) {
        exp_max = max;
    }

    /**
     * -Experience system component-
     * 
     * Returns the max possible rank for this skill.
     * @return 
     */
    public int getMaxRank() {
        return rank_max;
    }

    /**
     * -Experience system component-
     * 
     * Sets the max possible rank for this skill.
     * @param rank
     */
    public void setMaxRank(int rank) {
        rank_max = rank;
    }


    private static final long serialVersionUID = 1L;
}
