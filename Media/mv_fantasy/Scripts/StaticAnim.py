import ClientAPI

# Static animations and particles for objects based on properties

def StaticAnimHandler(sender, args):
    propName = args.PropName
    worldObj = ClientAPI.World.GetObjectByOID(args.Oid)
    anim = worldObj.GetProperty('StaticAnim')
    worldObj.QueueAnimation(anim, looping=True)

#
# When the object is destroyed, free up any static particle system instances
#  that have been attached to it.
# 
def particleDisposed(worldObj):
    particles = worldObj.GetProperty('_attachedParticles')
    for particle in particles:
        worldObj.DetachObject(particle)
        particle.Dispose()

def StaticParticleHandler(sender, args):
    propName = args.PropName
    worldObj = ClientAPI.World.GetObjectByOID(args.Oid)
    particles = worldObj.GetProperty('StaticParticles')
    attachedParticles = []
    for particleValues in particles:
        particleName, attachName, velocityMult, sizeMult = particleValues
        particle = ClientAPI.ParticleSystem.ParticleSystem(particleName + "_"
                                                           + str(ClientAPI.GetLocalOID()), particleName)
        particle.ScaleVelocity(velocityMult)
        particle.DefaultWidth = particle.DefaultWidth * sizeMult
        particle.DefaultHeight = particle.DefaultHeight * sizeMult
        worldObj.AttachObject(attachName, particle)
        
        # remember which particle systems have been attached to this object
        attachedParticles.append(particle)
        
    # Save the attached particle systems as a property on the object, and
    #  register a dispose handler to clean them up when the object is
    #  removed.
    worldObj.SetProperty('_attachedParticles', attachedParticles)
    worldObj.RegisterEventHandler('Disposed', particleDisposed)

ClientAPI.World.RegisterObjectPropertyChangeHandler('StaticAnim', StaticAnimHandler)
ClientAPI.World.RegisterObjectPropertyChangeHandler('StaticParticles', StaticParticleHandler)

