from .composing import create_counterpoint, create_counterpoint_after_chords
from .melody import CircularPermutationMelody, SelectRangeMelody, ReverseMelody, \
    InvertMelody, ReverseMelodyWithoutRhythm
from .note import LimitRegister, ApplySilence, TransposeDiatonic, TransposeChromatic, ApplyContinuation
from .score import RepeatScore
from .features import ExtractMainTonality, MostCommonTonalities
from .chord import RepeatChord, Modulate, ModulateKeepOriginMode

__all__ = ['create_counterpoint', 'create_counterpoint_after_chords',
           'CircularPermutationMelody', 'SelectRangeMelody', 'ReverseMelody', 'InvertMelody',
           'RepeatScore', 'ReverseMelodyWithoutRhythm',
            'LimitRegister', 'ApplySilence', 'TransposeDiatonic', 'TransposeChromatic', 'ApplyContinuation',
            'ExtractMainTonality', 'MostCommonTonalities',
            'RepeatChord', 'Modulate', 'ModulateKeepOriginMode'
           ]
