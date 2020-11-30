package multiverse.mars.behaviors;

import multiverse.msgsys.*;
import multiverse.server.engine.*;
import multiverse.server.objects.*;
import multiverse.server.math.*;
import multiverse.server.plugins.*;
import multiverse.server.plugins.WorldManagerClient.TargetedExtensionMessage;

public class TeleporterBehavior extends Behavior implements MessageCallback {
    public TeleporterBehavior() {
	super();
    }

    @Override
    public void initialize() {
        SubjectFilter filter = new SubjectFilter(obj.getOid());
	filter.addType(ObjectTracker.MSG_TYPE_NOTIFY_REACTION_RADIUS);
        eventSub = Engine.getAgent().createSubscription(filter, this);
    }

    @Override
    public void activate() {
	activated = true;
	MobManagerPlugin.getTracker(obj.getInstanceOid()).addReactionRadius(obj.getOid(), radius);
    }

    @Override
    public void deactivate() {
	lock.lock();
	try {
	    activated = false;
	    if (eventSub != null) {
                Engine.getAgent().removeSubscription(eventSub);
		eventSub = null;
	    }
	}
	finally {
	    lock.unlock();
	}
    }

    @Override
    public void handleMessage(Message msg, int flags) {
	if (activated == false) {
	    return;
	}
	if (msg.getMsgType() == ObjectTracker.MSG_TYPE_NOTIFY_REACTION_RADIUS) {
	    ObjectTracker.NotifyReactionRadiusMessage nMsg = (ObjectTracker.NotifyReactionRadiusMessage)msg;
// 	    Log.debug("TeleporterBehavior: myOid=" + obj.getOid() + " objOid=" + nMsg.getObjOid()
// 		      + " inRadius=" + nMsg.getInRadius() + " wasInRadius=" + nMsg.getWasInRadius());
	    if (nMsg.getInRadius()) {
		reaction(nMsg);
	    }
	}
    }

    public void reaction(ObjectTracker.NotifyReactionRadiusMessage nMsg) {
	BasicWorldNode wnode = new BasicWorldNode();
	wnode.setLoc(destination);
        // tell the worldmanager we've moved
        // this should update everyone near me
        TargetedExtensionMessage teleportBegin =
            new TargetedExtensionMessage(nMsg.getSubject(), nMsg.getSubject());
        teleportBegin.setExtensionType("mv.SCENE_BEGIN");
        teleportBegin.setProperty("action","teleport");
        TargetedExtensionMessage teleportEnd =
            new TargetedExtensionMessage(nMsg.getSubject(), nMsg.getSubject());
        teleportEnd.setExtensionType("mv.SCENE_END");
        teleportEnd.setProperty("action","teleport");
        WorldManagerClient.updateWorldNode(nMsg.getSubject(), wnode, true,
            teleportBegin, teleportEnd);
    }

    public void setRadius(int radius) {
	this.radius = radius;
    }
    public int getRadius() {
	return radius;
    }

    public void setDestination(Point loc) {
	destination = loc;
    }
    public Point getDestination() {
	return destination;
    }

    protected int radius = 0;
    protected Point destination;
    protected boolean activated = false;
    Long eventSub = null;
    private static final long serialVersionUID = 1L;
}
