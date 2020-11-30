package multiverse.mars.core;

import java.io.*;

public class MarsCombatSkill extends MarsSkill implements Serializable {

    public static MarsCombatSkill Brawling = new MarsCombatSkill("Brawling");
    public static MarsCombatSkill Sword = new MarsCombatSkill("Sword");
    public static MarsCombatSkill Spear = new MarsCombatSkill("Spear");
    public static MarsCombatSkill Axe = new MarsCombatSkill("Axe");
    public static MarsCombatSkill Dagger = new MarsCombatSkill("Dagger");

    public MarsCombatSkill() {
    }

    public MarsCombatSkill(String name) {
        super(name);
    }

    @Override
    public String toString() {
        return "[MarsCombatSkill: " + getName() + "]";
    }

    private static final long serialVersionUID = 1L;
}
