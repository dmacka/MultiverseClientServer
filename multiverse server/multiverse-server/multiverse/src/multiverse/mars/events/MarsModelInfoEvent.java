package multiverse.mars.events;

import multiverse.server.objects.*;
import multiverse.server.network.*;
import multiverse.server.util.*;
import multiverse.server.events.*;
import multiverse.mars.objects.*;
import java.util.*;

/**
 * send out what meshes to draw for the given object
 * it is a full update, so if you unequip a rigged attachment,
 * a full update is sent out
 */
public class MarsModelInfoEvent extends ModelInfoEvent {
    public MarsModelInfoEvent() {
        super();
    }

    public MarsModelInfoEvent(MVByteBuffer buf, ClientConnection con) {
	super(buf, con);
    }

    public MarsModelInfoEvent(MVObject obj) {
	super(obj);
        if (obj instanceof MarsMob) {
            // add all the equipment also
            processMarsMob((MarsMob)obj);
        }
    }

    public MarsModelInfoEvent(Long oid) {
	super(oid);
    }

    @Override
    public String getName() {
        return "MarsModelInfoEvent";
    }

    // need to add all the equipment meshes also
    void processMarsMob(MarsMob mob) {
        Set<MarsItem> items = mob.getEquippedItems();

        if (Log.loggingDebug)
            log.debug("processMarsMob: mob=" + mob.getName() +
                      ", num items=" + items.size());
        for (MarsItem item : items) {
            if (Log.loggingDebug)
                log.debug("processMarsMob: mob=" + mob.getName() +
                          ", considering equipped item " + 
                          item.getName());
            DisplayContext itemDC = item.displayContext();
            String meshFile = itemDC.getMeshFile();
            if (meshFile == null) {
                // no meshfile
                continue;
            }

            // check if its an attachment (if it is, skip it)
            if (itemDC.getAttachableFlag()) {
                continue;
            }

            // add the submeshes to this event's display context
            Set<DisplayContext.Submesh> submeshes = itemDC.getSubmeshes();
            if (Log.loggingDebug)
                log.debug("processMarsMob: mob=" + mob.getName() +
                          ", adding submeshes for item " + 
                          item.getName() +
                          ", dc=" + this.dc);
            this.dc.addSubmeshes(submeshes);
            if (Log.loggingDebug)
                log.debug("processMarsMob: mob=" + mob.getName() +
                          ", done adding submeshes for item " + 
                          item.getName() +
                          ", dc=" + this.dc);
        }
    }

    static final Logger log = new Logger("MarsModelInfoEvent");
}
