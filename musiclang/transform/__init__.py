from .pipeline import TransformPipeline, ConcatPipeline
from .mask import Mask
from .transformer import Transformer, ChordTransformer, ScoreTransformer, MelodyTransformer, NoteTransformer
from .transformer import ChordFilter, ChordFilterTransform, MelodyFilterTransform, MelodyFilter
from .transformer import NoteFilter, NoteFilterTransform, FeatureExtractor
from .transformer import MaskFilter, NoteMaskFilter, ChordMaskFilter, MelodyMaskFilter
from .merger import ScoreMerger
from .graph import TransformGraph
from .composing import VoiceLeading, PartComposer, create_counterpoint_on_score
from .dynamics import PitchDynamizer
from .melody import ContinuationWhenSameNote
from .composing import Patternator, OrchestralLayer, MelodicLayer, GlobalLayer
from .orchestrations import get_epic_orchestration, get_nocturne_orchestration

__all__ = ['TransformPipeline', 'ConcatPipeline', 'Mask',
           'Transformer', 'ChordTransformer', 'ScoreTransformer', 'MelodyTransformer',
           'NoteTransformer',
           'ChordFilter', 'ChordFilterTransform', 'MelodyFilterTransform', 'MelodyFilter',
           'NoteFilter', 'NoteFilterTransform', 'FeatureExtractor', 'MaskFilter', 'NoteMaskFilter',
           'ChordMaskFilter', 'MelodyMaskFilter', 'ScoreMerger', 'TransformGraph',
           'VoiceLeading', 'PitchDynamizer', 'ContinuationWhenSameNote', 'Patternator',
           'get_epic_orchestration', 'get_nocturne_orchestration', 'PartComposer','OrchestralLayer',
              'MelodicLayer', 'GlobalLayer', 'create_counterpoint_on_score'
           ]