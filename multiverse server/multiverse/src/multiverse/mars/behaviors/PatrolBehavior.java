package multiverse.mars.behaviors;

import java.util.*;
import java.util.concurrent.*;

import multiverse.msgsys.*;
import multiverse.server.objects.*;
import multiverse.server.math.*;
import multiverse.server.util.*;
import multiverse.server.engine.*;
import multiverse.server.plugins.InstanceClient;

public class PatrolBehavior extends Behavior implements MessageCallback, Runnable {
    public PatrolBehavior() {
	super();
    }

    public PatrolBehavior(SpawnData data) {
	super();
	String markerNames = (String)data.getProperty("PatrolPoints");
	if (markerNames != null) {
	    for (String markerName : markerNames.split(",")) {
                markerName = markerName.trim();
                if (markerName.length() == 0)
                    continue;
                Point point = InstanceClient.getMarkerPoint(
                    data.getInstanceOid(), markerName);
		if (point == null) {
		    Log.error("PatrolBehavior: unknown marker=" + markerName +
                        " instanceOid=" + data.getInstanceOid());
		}
		else {
		    point.setY(0);
		    addWaypoint(point);
		}
	    }
	}
    }

    @Override
    public void initialize() {
        SubjectFilter filter = new SubjectFilter(obj.getOid());
        filter.addType(Behavior.MSG_TYPE_EVENT);
        eventSub = Engine.getAgent().createSubscription(filter, this);
    }
    @Override
    public void activate() {
        startPatrol();
    }
    @Override
    public void deactivate() {
        if (eventSub != null) {
	    Engine.getAgent().removeSubscription(eventSub);
            eventSub = null;
        }
    }

    @Override
    public void handleMessage(Message msg, int flags) {
        if (msg.getMsgType() == Behavior.MSG_TYPE_EVENT) {
	    String event = ((Behavior.EventMessage)msg).getEvent();
	    if (event.equals(BaseBehavior.MSG_EVENT_TYPE_ARRIVED)) {
		Engine.getExecutor().schedule(this, getLingerTime(), TimeUnit.MILLISECONDS);
	    }
        }
        //return true;
    }

    public void addWaypoint(Point wp) {
        waypoints.add(wp);
    }
    protected List<Point> waypoints = new ArrayList<>();

    public void setLingerTime(long time) {
        lingerTime = time;
    }
    public long getLingerTime() {
        return lingerTime;
    }
    protected long lingerTime = 2000;

    public void setMovementSpeed(int speed) {
        this.speed = speed;
    }
    public int getMovementSpeed() {
        return speed;
    }
    protected Integer speed = 3000;

    protected void startPatrol() {
        nextWaypoint = 0;
        nextPatrol();
    }

    protected void sendMessage(Point waypoint, int speed) {
        Engine.getAgent().sendBroadcast(new BaseBehavior.GotoCommandMessage(obj, waypoint, speed));
    }

    protected void nextPatrol() {
	sendMessage(waypoints.get(nextWaypoint), getMovementSpeed());
        nextWaypoint++;
        if (nextWaypoint == waypoints.size()) {
            nextWaypoint = 0;
        }
    }

    @Override
    public void run() {
        nextPatrol();
    }

    int nextWaypoint = 0;
    Long eventSub = null;
    private static final long serialVersionUID = 1L;

}
