from Converter.helpers import *
import wave

def parse(resource):
    for resid in resource.keys():
        snd_dict = resource[resid]
        snd_name = snd_dict['name']
        raw_data = snd_dict['data']
        filename = snd_name + ".wav"
        print("Writing HSND %s as %s" % (snd_name, filename))
        with wave.open(filename, 'wb') as wavfile:
            wavfile.setparams((2, 2, 22050, 0, 'NONE', 'NONE'))
            wavfile.writeframes(raw_data)