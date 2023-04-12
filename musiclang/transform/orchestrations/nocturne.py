from musiclang.library import *
from musiclang.transform.library import *
from musiclang.transform.composing.pattern import Nocturne, StandardPlucked, EpicMusicTernary
from musiclang.transform.composing import PartComposer
from musiclang.predict import compose_melody_and_harmony


def get_nocturne_orchestration(melody, harmony, tonality, bar_duration=4):
    composer = PartComposer(**{
        'orchestral_layers': [{
            "instruments": ['piano', 'piano', 'piano', 'piano'],
            "voicing": [b0.o(-1), b2.o(-1), b0, b1],
            "orchestra": Nocturne().to_json(),
            "fixed_bass": True,
            "voice_leading": True
        },

        ],
        'melodic_layers': [{
            "instrument": "piano",
            "melody": melody
        }],
        'global_layer': {
            "tonality": tonality,
            "harmony": harmony,
            "acc_amp": 'p',
            "patternator": {"restart_each_chord": False}

        }
    })
    return composer.to_json()