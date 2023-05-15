from .composer.auto_composer import AutoComposer
from .arranger import Arranger, ArrangerTrainer
from.composer.harmony import compose_melody_and_harmony, generate_harmony, harmony_to_melody, melody_to_harmony, auto_enrich_melody
from .predictors.hugging import deduplicate_chord_instruments, generate_n_chords, generate_one_chord

__all__ = ['AutoComposer', 'Arranger', 'ArrangerTrainer',
           'compose_melody_and_harmony', 'generate_harmony', 'harmony_to_melody', 'melody_to_harmony', 'auto_enrich_melody'
           ]