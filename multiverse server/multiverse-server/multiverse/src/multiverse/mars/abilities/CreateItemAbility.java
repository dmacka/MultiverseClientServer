package multiverse.mars.abilities;

import multiverse.mars.core.MarsAbility;
import multiverse.mars.core.MarsAbility.State;
import multiverse.server.engine.Namespace;
import multiverse.server.objects.Template;
import multiverse.server.plugins.InventoryClient;
import multiverse.server.plugins.ObjectManagerClient;

public class CreateItemAbility extends MarsAbility {
    protected String template;
    public CreateItemAbility(String name) {
        super(name);
        this.template = null;
    }

    public String getItem() { return template; }
    public void setItem(String template) { this.template = template; }

    @Override
    public void completeActivation(State state) {
        super.completeActivation(state);
        Long playerOid;
        playerOid = state.getObject().getOwnerOid();
        Long bagOid = playerOid;

        // Normally the persistence flag is inherited from the enclosing
        // object, but all we have are OIDs.  Assume this is only used
        // for players and players are always persistent.
        Template overrideTemplate = new Template();
        overrideTemplate.put(Namespace.OBJECT_MANAGER,
                ObjectManagerClient.TEMPL_PERSISTENT, true);

        Long itemOid = ObjectManagerClient.generateObject(template, overrideTemplate);
        InventoryClient.addItem(bagOid, playerOid, bagOid, itemOid);
    }
}
