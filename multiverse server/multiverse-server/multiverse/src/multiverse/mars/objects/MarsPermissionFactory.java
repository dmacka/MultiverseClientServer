package multiverse.mars.objects;

import multiverse.server.objects.*;

public class MarsPermissionFactory implements PermissionFactory {
    /**
     * from PermissionFactory interface - pass in the object this permission
     * is for.
     * @param obj
     * @return 
     */
    @Override
    public PermissionCallback createPermission(MVObject obj) {
	return new MarsPermissionCallback(obj);
    }
}
