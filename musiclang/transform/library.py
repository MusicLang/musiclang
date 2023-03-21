from .composing import create_counterpoint, create_counterpoint_on_score
from .melody import CircularPermutationMelody, SelectRangeMelody, ReverseMelody, \
    InvertMelody, ReverseMelodyWithoutRhythm
from .note import LimitRegister, ApplySilence, TransposeDiatonic, TransposeChromatic, ApplyContinuation
from .score import RepeatScore
from .features import ExtractMainTonality, MostCommonTonalities
from .chord import RepeatChord, Modulate, ModulateKeepOriginMode
from .score_merger import ConcatScores, ConcatWithPattern, TakeSlice, TakeFirst, TakeLast, TakeIdx
from .composing import VoiceLeading, Patternator
from .dynamics import PitchDynamizer
from .melody import ContinuationWhenSameNote

__all__ = ['create_counterpoint', 'create_counterpoint_on_score',
           'CircularPermutationMelody', 'SelectRangeMelody', 'ReverseMelody', 'InvertMelody',
           'RepeatScore', 'ReverseMelodyWithoutRhythm',
            'LimitRegister', 'ApplySilence', 'TransposeDiatonic', 'TransposeChromatic', 'ApplyContinuation',
            'ExtractMainTonality', 'MostCommonTonalities',
            'RepeatChord', 'Modulate', 'ModulateKeepOriginMode',
           'ConcatScores', 'ConcatWithPattern', 'TakeSlice', 'TakeFirst', 'TakeLast', 'TakeIdx',
           'VoiceLeading', 'PitchDynamizer', 'ContinuationWhenSameNote', 'Patternator'
           ]
