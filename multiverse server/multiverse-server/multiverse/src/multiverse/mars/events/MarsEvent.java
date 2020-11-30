package multiverse.mars.events;

import multiverse.server.engine.*;
import multiverse.mars.objects.*;
import multiverse.server.network.*;

public abstract class MarsEvent extends Event {
    public MarsEvent() {
	super();
    }

    public MarsEvent(MarsObject obj) {
	super();
	setObject(obj);
    }

    public MarsEvent(MVByteBuffer buf, ClientConnection con) {
	super(buf,con);
    }

}
