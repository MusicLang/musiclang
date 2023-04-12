from .counterpoint import create_counterpoint, create_counterpoint_on_chord, create_counterpoint_on_score
from .project import project_on_one_chord, project_on_rhythm, project_on_score_keep_notes, project_on_several_chord
from .voice_leading import VoiceLeading, Rules
from .patternator import Patternator
import musiclang.transform.composing.pattern as pattern
from .layer import MelodicLayer, OrchestralLayer, PartComposer, GlobalLayer