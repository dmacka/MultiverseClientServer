package multiverse.mars.objects;

public class HumanoidHitLocationTable extends HitLocationTable {
	public static HitLocation getHitLocation(int loc) {
		HitLocation rv = new HitLocation();
		if (loc <=5) {
			rv.name = "head";
			rv.stunMultiplier = 5;
			rv.nStunMultiplier = 2;
			rv.bodyMultiplier = 2;
		} else if (loc <=6) {
			rv.name = "hand";
			rv.stunMultiplier = 1;
			rv.nStunMultiplier = 0.5f;
			rv.bodyMultiplier = 0.5f;
		} else if (loc <= 8) {
			rv.name = "arm";
			rv.stunMultiplier = 2;
			rv.nStunMultiplier = 0.5f;
			rv.bodyMultiplier = 0.5f;
		} else if (loc <= 9) {
			rv.name = "shoulder";
			rv.stunMultiplier = 3;
			rv.nStunMultiplier = 1;
			rv.bodyMultiplier = 1;
		} else if (loc <= 11) {
			rv.name = "chest";
			rv.stunMultiplier = 3;
			rv.nStunMultiplier = 1;
			rv.bodyMultiplier = 1;
		} else if (loc <= 12) {
			rv.name = "stomach";
			rv.stunMultiplier = 4;
			rv.nStunMultiplier = 1.5f;
			rv.bodyMultiplier = 1;
		} else if (loc <= 13) {
			rv.name = "vitals";
			rv.stunMultiplier = 4;
			rv.nStunMultiplier = 1.5f;
			rv.bodyMultiplier = 2;
		} else if (loc <= 14) {
			rv.name = "thigh";
			rv.stunMultiplier = 2;
			rv.nStunMultiplier = 1;
			rv.bodyMultiplier = 1;
		} else if (loc <= 16) {
			rv.name = "leg";
			rv.stunMultiplier = 2;
			rv.nStunMultiplier = 0.5f;
			rv.bodyMultiplier = 0.5f;
		} else if (loc <= 18) {
			rv.name = "foot";
			rv.stunMultiplier = 1;
			rv.nStunMultiplier = 0.5f;
			rv.bodyMultiplier = 0.5f;
		}
		return rv;
	} 
}
