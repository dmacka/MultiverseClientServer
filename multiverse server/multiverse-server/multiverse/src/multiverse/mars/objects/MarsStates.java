package multiverse.mars.objects;

/**
 * used in marsobjects . setState
 */
public enum MarsStates {
    Dead("deadState"),
    PVP("pvpstate"),
    Combat("combatstate"),
    QuestAvailable("questavailable"),
    QuestConcludable("questconcludable"),
    Attackable("attackable"),
    Lootable("lootable"),
    Stunned("stunned"),
    Movement("movement");
    
    /**
     * pass in the string which gets sent over to the client.
     * we dont use toString() since the client and server may have different
     * names
     */
    MarsStates(String encodeStr) {
	this.str = encodeStr;
    }

    @Override
    public String toString() {
	return str;
    }
    
    String str = null;
}