package multiverse.mars.core;

import multiverse.mars.objects.*;
import java.io.*;

/**
 * used with mars items - this gets called when a user activates this
 * item
 */
public interface ActivateHook extends Serializable {

    /**
     * returns whether the item was successfully activated
     * @param activator
     * @param item
     * @param target
     * @return 
     */
    public boolean activate(Long activator, MarsItem item, Long target);
}
