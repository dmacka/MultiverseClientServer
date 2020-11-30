package multiverse.mars.plugins;

import java.io.*;
import java.io.ObjectInputStream;
import java.util.Set;
import java.util.Map;
import java.util.HashMap;
import java.util.concurrent.locks.Lock;

import multiverse.msgsys.*;
import multiverse.server.engine.Engine;
import multiverse.server.network.MVByteBuffer;
import multiverse.server.util.*;
import multiverse.mars.objects.CoordinatedEffect;

public class AnimationClient {

    public static void playSingleAnimation(Long oid, String animName) {
        if (Log.loggingDebug)
            Log.debug("AnimationClient.playSingleAnimation: playing anim " + animName);
        CoordinatedEffect effect = new CoordinatedEffect("PlayAnimation");
        effect.sendSourceOid(true);
        effect.putArgument("animName", animName);
        effect.invoke(oid, null);
    }

    /**
     * InvokeEffectMessage
     *
     * Tells the client to invoke a coordinated effect. The message oid is used by the server to
     * determine who can perceive the effect, but is not sent to the client. The client only sees
     * the oid for the effect instance.
     */
    public static class InvokeEffectMessage extends SubjectMessage {
	public InvokeEffectMessage() {
	    super();
	    setMsgType(MSG_TYPE_INVOKE_EFFECT);
            setupTransient();
	}

	public InvokeEffectMessage(Long oid, String effectName) {
	    super(MSG_TYPE_INVOKE_EFFECT, oid);
            setupTransient();
	    setEffectName(effectName);
	    setEffectOid(Engine.getOIDManager().getNextOid());
	}

        @Override
        public String toString() {
            String s = "[InvokeEffectMessage super=" + super.toString();
	    s += " effectName=" + effectName + " effectOid=" + effectOid;
            for (Map.Entry<String, Serializable> entry : propertyMap.entrySet()) {
                String key = entry.getKey();
                Serializable val = entry.getValue();
                s += " key=" + key + ",value=" + val.toString();
            }
            return s + "]";
        }

	public void setEffectName(String effectName) { this.effectName = effectName; }
	public String getEffectName() { return effectName; }
	protected String effectName;

	public void setEffectOid(Long oid) { effectOid = oid; }
	public Long getEffectOid() { return effectOid; }
	protected Long effectOid;

        /**
         * Associate the value with the key.
         * @param key
         * @param val
         * @Deprecated Use {@link #setProperty(String key, Serializable val)} instead
         */
        public void put(String key, Serializable val) {
            setProperty(key, val);
        }

        /**
         * Associate the value with the key.
         * @param key A String key.
         * @param val A Serializable value.
         */
        public void setProperty(String key, Serializable val) {
            lock.lock();
            try {
                propertyMap.put(key, val);
            } finally {
                lock.unlock();
            }
        }

        /**
         * Get the value associated with a key.
         * @param key
         * @return 
         * @Deprecated Use {@link #getProperty(String key)} instead
         */
        public Serializable get(String key) {
            return getProperty(key);
        }

        /**
         * Return the value associated with a key.
         * @param key A String key.
         * @return The Serializable value associated with the key, or null if none exists.
         */
        public Serializable getProperty(String key) {
            lock.lock();
            try {
                return propertyMap.get(key);
            } finally {
                lock.unlock();
            }
        }

        public Set<String> keySet() {
            lock.lock();
            try {
                return propertyMap.keySet();
            } finally {
                lock.unlock();
            }
        }

        public MVByteBuffer toBuffer(String version) {
            lock.lock();
            try {
                MVByteBuffer buf = new MVByteBuffer(400);
                buf.putLong(getEffectOid());
                buf.putInt(71);
		buf.putString(effectName);

                if (Log.loggingDebug)
                    Log.debug("InvokeEventMessage: oid=" + getSubject());
                buf.putPropertyMap(propertyMap);
                buf.flip();
                return buf;
            } finally {
                lock.unlock();
            }
        }

        void setupTransient() {
            lock = LockFactory.makeLock("InvokeEffectMessageLock");
        }

        private void readObject(ObjectInputStream in) throws IOException,
                ClassNotFoundException {
            in.defaultReadObject();
            setupTransient();
        }

        transient protected Lock lock = null;

        protected Map<String, Serializable> propertyMap = new HashMap<>();

        private static final long serialVersionUID = 1L;
    }

    /**
     * the animation key for the animation template
     */
    public static final String TEMPL_ANIM = ":tmpl.anim";
    
    public static final MessageType MSG_TYPE_INVOKE_EFFECT = MessageType.intern("mv.INVOKE_EFFECT");

}
