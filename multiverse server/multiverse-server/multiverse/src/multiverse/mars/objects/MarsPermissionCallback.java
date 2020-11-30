package multiverse.mars.objects;

import multiverse.server.objects.*;

public class MarsPermissionCallback extends PermissionCallback {

    public MarsPermissionCallback(MVObject obj) {
	super(obj);
    }

    /**
     * returns true if allowed to pick up this object.
     * CURRENTLY - objects can only be picked up if they are on the ground
     * @param acquirer
     * @return 
     */
    @Override
    public boolean acquire(MVObject acquirer) {
	if (! thisObj.isItem()) {
	    return false;
	}

// 	MVObject container = thisObj.getContainedIn();
// 	if (container != null) {
// 	    log.debug("acquire: failed because target obj is in a container");
// 	    return false;
// 	}
	return true;
    }
    
    /**
     * returns true if allowed to drop this object.
     * CURRENTLY - all objects can be dropped
     * @param dropInto
     * @return 
     */
    @Override
    public boolean drop(MVObject dropInto) {
	return true;
    }

    /**
     * returns if the user is allowed to use this object
     * CURRENTLY - you can use if you have it in inventory
     * @param user
     * @return 
     */
    public boolean use(MVObject user) {
// 	MVObject container = thisObj.getContainedIn();
// 	if (container == null) {
// 	    // you cant use what you dont have
// 	    log.debug("use: failed because obj is not in user's inventory");
// 	    return false;
// 	}

	// see if the container is the same object as the user
	// (doesnt work if the object to be used is in a nested container)
// 	if (! MVObject.equals(container, user)) {
// 	    log.debug("use: failed because container is not the same as the obj trying to use");
// 	    return false;
// 	}
	return true;
    }

    /**
     * returns true if allowed to destory this object.
     * CURRENTLY - you must have the object in your "inventory" to destroy it
     * @param destroyer
     * @return 
     */
    @Override
    public boolean destroy(MVObject destroyer) {
// 	MVObject container = thisObj.getContainedIn();
// 	if (container == null) {
//             Log.debug("MarsPermissionCallback.destroy: cannot destroy because obj has no container");

// 	    // you cant destory what you dont have
// 	    return false;
// 	}

// 	// see if the container is the same object as the destroyer
// 	// (doesnt work if destroyObject is in a nested container)
// 	boolean rv = MVObject.equals(container, destroyer);
//         if (! rv) {
//             Log.debug("MarsPermissionCallback.destroy: container and destroyer are not the same, cannot destroy");
//         }
//         else {
//             Log.debug("MarsPermissionCallback.destroy: can destroy");
//         }
//         return rv;
	return true;
    }

    private static final long serialVersionUID = 1L;
}
