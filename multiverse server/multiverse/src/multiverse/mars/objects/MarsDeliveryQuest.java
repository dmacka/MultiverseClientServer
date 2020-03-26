package multiverse.mars.objects;

public class MarsDeliveryQuest extends MarsQuest {
    public MarsDeliveryQuest() {
        super();
    }

    public void setDeliveryTarget(MarsMob mob) {
        deliveryTarget = mob;
    }
    public MarsMob getDeliveryTarget() {
        return deliveryTarget;
    }
    MarsMob deliveryTarget = null;

    @Override
    public DeliveryQuestState generate(Long playerOid) {
	throw new RuntimeException("not implemented");
    }

    private static final long serialVersionUID = 1L;
}
