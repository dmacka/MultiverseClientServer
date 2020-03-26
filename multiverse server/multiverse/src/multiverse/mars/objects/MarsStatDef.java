package multiverse.mars.objects;

import java.util.*;

import multiverse.server.objects.Entity;
import multiverse.server.util.*;

public class MarsStatDef {
    public MarsStatDef(String name) {
	this.name = name;
    }

    public String getName() { return name; }
    protected String name;

    public void addDependent(MarsStatDef stat) {
	dependents.add(stat);
    }
    protected Set<MarsStatDef> dependents = new HashSet<>();

    public void update(MarsStat stat, Entity info) {
	if ((stat.min != null) && (stat.base <= stat.min)) {
	    stat.base = stat.min;
	}
	if ((stat.max != null) && (stat.base >= stat.max)) {
	    stat.base = stat.max;
	}
	stat.applyMods();
	if ((stat.min != null) && (stat.current <= stat.min)) {
	    stat.current = stat.min;
	}
	if ((stat.max != null) && (stat.current >= stat.max)) {
	    stat.current = stat.max;
	}

	int oldFlags = stat.flags;
	stat.flags = stat.computeFlags();

	for (MarsStatDef statDef : dependents) {
	    MarsStat depStat = (MarsStat)info.getProperty(statDef.name);
	    if (depStat != null) {
		Log.debug("MarsStatDef.update: stat=" + name + " updating dependent stat="
			  + statDef.getName());
		statDef.update(depStat, info);
	    }
	}

	notifyFlags(stat, info, oldFlags, stat.flags);

    }
    public void notifyFlags(MarsStat stat, Entity info, int oldFlags, int newFlags) {
    }

    public final static int MARS_STAT_FLAG_MIN = 1;
    public final static int MARS_STAT_FLAG_MAX = 2;
}
