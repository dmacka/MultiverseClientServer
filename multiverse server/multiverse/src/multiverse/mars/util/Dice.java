package multiverse.mars.util;

import java.util.*;

public class Dice {
    public Dice(int sides) {
	this.sides = sides;
    }

    public synchronized int roll(int numTimes) {
	int total = 0;
	while (numTimes > 0) {
	    total = total + random.nextInt(sides) + 1;
	    --numTimes;
	}
	return total;
    }

    private int sides = 0;
    private Random random = new Random();

    // standard six sided dice
    public static Dice StdDice = new Dice(6);
}
