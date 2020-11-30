import ClientAPI
import MarsCommand

exterior = 'http://72.13.81.178:8010/'
sound = ClientAPI.GetSoundSource(exterior, ClientAPI.Vector3.Zero, False, 0.0, True, False)

#exterior = 'Urban_Illusion.ogg'
#sound = ClientAPI.GetSoundSource(exterior, ClientAPI.Vector3.Zero, True, 0.0, True, True)

gain = 0.2

if not sound == None:
    sound.Gain = gain
    sound.Play()
