from musiclang.predict.composer import auto_compose
from musiclang import Score
from musiclang.transform.composing.pattern import Pattern
class OrchestralLayer:

    def __init__(self,
                 orchestra,
                 voicing,
                 instruments,
                 metadata=None,
                 fixed_bass=True,
                 voice_leading=True):

        self.orchestra = orchestra
        self.voicing = voicing
        self.fixed_bass = fixed_bass
        self.voice_leading = voice_leading
        self.instruments = instruments
        self.metadata = metadata if metadata is not None else {}

    @classmethod
    def from_json(cls, data):
        return OrchestralLayer(
            orchestra=data['orchestra'],
            voicing=[Score.from_str(note) for note in data['voicing']],
            instruments=data['instruments'],
            fixed_bass=data['fixed_bass'],
            metadata=data.get('metadata', {}),
            voice_leading=data['voice_leading']
        )

    def to_json(self):
        dictionary = {key: item for key, item in self.__dict__.items()}
        dictionary['voicing'] = [str(note) for note in self.voicing]
        if hasattr(dictionary['orchestra'], 'to_json'):
            dictionary['orchestra'] = dictionary['orchestra'].to_json()
        return dictionary


class MelodicLayer:

    def __init__(self, melody, instrument):
        self.melody = melody
        self.instrument = instrument

    def to_json(self):
        return {
                "melody": [str(note) for note in self.melody],
                "instrument": self.instrument
                }

    @classmethod
    def from_json(self, data):
        return MelodicLayer(melody=sum([Score.from_str(note) for note in data['melody']], None), instrument=data['instrument'])

class GlobalLayer:

    def __init__(self, tonality, harmony, patternator, acc_amp='mf'):
        self.tonality = tonality
        self.harmony = harmony
        self.patternator = patternator
        self.acc_amp = acc_amp

    def to_json(self):
        return self.__dict__

    @classmethod
    def from_json(self, data):
        return GlobalLayer(
            tonality=data['tonality'],
            harmony=data['harmony'],
            patternator=data['patternator'],
            acc_amp=data['acc_amp']
        )


class PartComposer:
    """
    Class that is responsible of merging the layer together to pass it to the auto_composer
    """

    def __init__(self, orchestral_layers, melodic_layers, global_layer):
        self.orchestral_layers = self.init_orchestral_layers(orchestral_layers)
        self.melodic_layers = self.init_melodic_layers(melodic_layers)
        self.global_layer = self.init_global_layers(global_layer)

    @classmethod
    def from_json(cls, data):
        return PartComposer(
            orchestral_layers=[OrchestralLayer.from_json(layer) for layer in data['orchestral_layers']],
            melodic_layers=[MelodicLayer.from_json(layer) for layer in data['melodic_layers']],
            global_layer=GlobalLayer.from_json(data['global_layer'])
        )

    def to_json(self):
        return {"global_layer": self.global_layer.to_json(),
                "melodic_layers": [layer.to_json() for layer in self.melodic_layers],
                "orchestral_layers": [layer.to_json() for layer in self.orchestral_layers]
                }

    def init_orchestral_layers(self, orchestral_layers):
        return [OrchestralLayer(**layer) if isinstance(layer, dict) else layer for layer in orchestral_layers]

    def init_melodic_layers(self, melodic_layers):
        return [MelodicLayer(**layer) if isinstance(layer, dict) else layer for layer in melodic_layers]

    def init_global_layers(self, global_layer):
        return GlobalLayer(**global_layer) if isinstance(global_layer, dict) else global_layer

    @classmethod
    def compose(cls, data):
        return cls.from_json(data)()
    def __call__(self):

        melodies = []
        orchestras = []
        voicings = []
        fixed_basses = []
        voice_leadings = []
        instrumentss = []
        all_instrumentss = []
        solo_instruments = []
        tonality = self.global_layer.tonality
        patternator = self.global_layer.patternator
        harmony = self.global_layer.harmony
        acc_amp = self.global_layer.acc_amp
        harmony = harmony.replace('m0', f'm0 {tonality}:')

        instrument_dict = {}
        for layer in self.orchestral_layers:
            orchestras.append(layer.orchestra)
            voicings.append(layer.voicing)
            fixed_basses.append(layer.fixed_bass)
            real_instruments = []
            voice_leadings.append(layer.voice_leading)

            for instrument in layer.instruments:
                clean_instrument = ''.join(instrument.split('__')[:-1])
                instrument_dict[clean_instrument] = instrument_dict.get(clean_instrument, -1) + 1
                index = instrument_dict[clean_instrument]
                real_instruments.append(instrument + f'__{index}')
            instrumentss.append(real_instruments)
            all_instrumentss = all_instrumentss + real_instruments

        for layer in self.melodic_layers:
            melodies.append(layer.melody)
            instrument = layer.instrument
            clean_instrument = ''.join(instrument.split('__')[:-1])
            instrument_dict[clean_instrument] = instrument_dict.get(clean_instrument, -1) + 1
            index = instrument_dict[clean_instrument]
            real_instrument = instrument + f'__{index}'
            solo_instruments.append(real_instrument)
        return auto_compose(melodies, harmony, orchestras, voicings, patternator,
                 tonality, solo_instruments, instrumentss, acc_amp=acc_amp,
                 fixed_bass=fixed_basses, voice_leading=voice_leadings
                 )



# def auto_compose(melody, harmony, orchestra, voicing, patternator,
#                  tonality, solo_instrument, instruments, acc_amp='mf',
#                  fixed_bass=True, voice_leading=True
#                  ):