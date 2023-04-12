from musiclang.library import *
from musiclang.transform.library import *
from musiclang.transform.composing.pattern import Nocturne, StandardPlucked, EpicMusicTernary
from musiclang.transform.composing import PartComposer
from musiclang.predict import compose_melody_and_harmony

def get_epic_orchestration(melody, harmony, tonality, bar_duration=6):
    composer = PartComposer(**{
        'orchestral_layers': [{
            "instruments": ['contrabasses', 'string_ensemble_1', 'french_horn'],
            "voicing": [b0.o(-2), b1.o(-1), b2.o(-1)],
            "orchestra": EpicMusicTernary(drums=0),
            "fixed_bass": True,
            "voice_leading": True
        },
            {

                "instruments": ['choir_aahs', 'choir_aahs', 'choir_aahs'],
                "voicing":  [b2, b0.o(1), b1.o(1)],
                "orchestra": StandardPlucked(bar_duration=bar_duration).to_json(),
                "fixed_bass": False,
                "voice_leading": True
            }
        ],
        'melodic_layers': [{
            "instrument": "string_ensemble_1",
            "melody": melody
        }],
        'global_layer': {
            "tonality": tonality,
            "harmony": harmony,
            "acc_amp": 'f',
            "patternator": {"restart_each_chord": False}
        }
    })
    return composer.to_json()
