/********************************************************************

The Multiverse Platform is made available under the MIT License.

Copyright (c) 2012 The Multiverse Foundation

Permission is hereby granted, free of charge, to any person 
obtaining a copy of this software and associated documentation 
files (the "Software"), to deal in the Software without restriction, 
including without limitation the rights to use, copy, modify, 
merge, publish, distribute, sublicense, and/or sell copies 
of the Software, and to permit persons to whom the Software 
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be 
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES 
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE 
OR OTHER DEALINGS IN THE SOFTWARE.

*********************************************************************/


package multiverse.example;

import java.util.ArrayList;
import multiverse.msgsys.FilterUpdate;
import multiverse.msgsys.Message;
import multiverse.msgsys.MessageCallback;
import multiverse.msgsys.MessageType;
import static multiverse.server.engine.Engine.getAgent;
import multiverse.server.messages.PerceptionFilter;
import static multiverse.server.messages.PerceptionFilter.FIELD_TARGETS;
import multiverse.server.messages.PerceptionMessage;
import multiverse.server.messages.PerceptionTrigger;
import multiverse.server.plugins.WorldManagerClient;
import static multiverse.server.plugins.WorldManagerClient.MSG_TYPE_PERCEPTION;
import static multiverse.server.plugins.WorldManagerClient.MSG_TYPE_UPDATEWNODE;

/** Simple perception messaging example.  Monitor the location of
objects perceived by some set of objects.  Contains methods to
dynamically change the set of perceiving objects.
*/
public class PerceptionExample implements MessageCallback
{
    PerceptionFilter perceptionFilter;
    PerceptionTrigger perceptionTrigger;
    long perceptionSubId;
    public PerceptionExample()
    {
        perceptionFilter = new PerceptionFilter();
        perceptionFilter.addType(MSG_TYPE_PERCEPTION);
        perceptionFilter.addType(MSG_TYPE_UPDATEWNODE);
        perceptionFilter.setMatchAllSubjects(true);
        PerceptionTrigger perceptionTrigger;
        perceptionTrigger = new PerceptionTrigger();
        ArrayList<MessageType> triggerTypes;
        triggerTypes = new ArrayList<>(1);
        triggerTypes.add(MSG_TYPE_PERCEPTION);
        perceptionTrigger.setTriggeringTypes(triggerTypes);
        perceptionSubId = getAgent().createSubscription(perceptionFilter, this, NO_FLAGS, perceptionTrigger);
    }

    public synchronized void addObjectMonitoring(long oid) {
        if (perceptionFilter.addTarget(oid)) {
            FilterUpdate filterUpdate;
            filterUpdate = new FilterUpdate(1);
            filterUpdate.addFieldValue(FIELD_TARGETS, oid);
            getAgent().applyFilterUpdate(perceptionSubId, filterUpdate);
        }
    }

    public synchronized void removeObjectMonitoring(long oid) {
        if (perceptionFilter.removeTarget(oid)) {
            FilterUpdate filterUpdate;
            filterUpdate = new FilterUpdate(1);
            filterUpdate.removeFieldValue(FIELD_TARGETS, oid);
            getAgent().applyFilterUpdate(perceptionSubId, filterUpdate);
        }
    }

    @Override
    public void handleMessage(Message msg, int flags) {
        if (msg.getMsgType() == MSG_TYPE_PERCEPTION) {
            handlePerception((PerceptionMessage)msg);
        }
        else if (msg.getMsgType() == MSG_TYPE_UPDATEWNODE) {
            handleUpdateWorldNode((WorldManagerClient.UpdateWorldNodeMessage)msg);
        }
    }
  
    void handlePerception(PerceptionMessage message)
    {
    }
    
    void handleUpdateWorldNode(
        WorldManagerClient.UpdateWorldNodeMessage message)
    {
    }
    
}

