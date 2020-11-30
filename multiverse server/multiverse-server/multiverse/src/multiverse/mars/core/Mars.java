package multiverse.mars.core;

import multiverse.server.engine.*;

public class Mars {
    public static Manager<MarsAbility> AbilityManager =
	new Manager<MarsAbility>("AbilityManager");

    public static Manager<MarsEffect> EffectManager =
	new Manager<MarsEffect>("EffectManager");

    public static Manager<MarsSkill> SkillManager = new Manager<MarsSkill>("SkillManager");
    
    public static int getDefaultCorpseTimeout() {
	return defaultCorpseTimeout;
    }
    public static void setDefaultCorpseTimeout(int timeout) {
	defaultCorpseTimeout = timeout;
    }
    private static int defaultCorpseTimeout = 60000;
}