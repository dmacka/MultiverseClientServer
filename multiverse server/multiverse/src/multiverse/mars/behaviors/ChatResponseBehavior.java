package multiverse.mars.behaviors;

import java.util.*;

import multiverse.msgsys.*;
import multiverse.server.plugins.WorldManagerClient;
import multiverse.server.engine.Behavior;
import multiverse.server.engine.Engine;

public class ChatResponseBehavior extends Behavior implements MessageCallback {
    @Override
    public void initialize() {
	MessageTypeFilter filter = new MessageTypeFilter();
	filter.addType(WorldManagerClient.MSG_TYPE_COM);
	eventSub = Engine.getAgent().createSubscription(filter, this);
    }
    
    @Override
    public void activate() {
    }

    @Override
    public void deactivate() {
	if (eventSub != null) {
	    Engine.getAgent().removeSubscription(eventSub);
	    eventSub = null;
	}
        //return true;
    }

    @Override
    public void handleMessage(Message msg, int flags) {
        String response = null;
        if (msg instanceof WorldManagerClient.ComMessage) {
            WorldManagerClient.ComMessage comMsg = (WorldManagerClient.ComMessage)msg;
            response = responses.get(comMsg.getString());

        }
        else if (msg instanceof WorldManagerClient.TargetedComMessage) {
            WorldManagerClient.TargetedComMessage comMsg = (WorldManagerClient.TargetedComMessage)msg;
            response = responses.get(comMsg.getString());
        }
        if (response != null) {
            WorldManagerClient.sendChatMsg(obj.getOid(), 1, response);
        }
    }
        
    public void addChatResponse(String trigger, String response) {
	responses.put(trigger, response);
    }

    Map<String, String> responses = new HashMap<>();
    Long eventSub = null;

    private static final long serialVersionUID = 1L;
}