from musiclang import Melody, Score
from musiclang.transform import ScoreTransformer
from musiclang import Continuation

class ContinuationWhenSameNote(ScoreTransformer):
    """
    When a note is repeated create a continuation instead of repeating the note
    """

    def __init__(self, only_inside_chord=False, instruments=None, keep_instruments=None):
        self.only_inside_chord = only_inside_chord
        self.keep_instruments = keep_instruments if keep_instruments is not None else []
        self.instruments = instruments

    def action(self, score: Score, **kwargs):
        new_score = score.copy()
        instruments = new_score.instruments
        for inst in instruments:
            current_pitch = None
            for chord in new_score.chords:
                if self.only_inside_chord:
                    current_pitch = None
                if inst in chord.score and inst not in self.keep_instruments:
                    if self.instruments is None or inst in self.instruments:
                        mel = chord.score[inst]
                        for idx, note in enumerate(mel.notes):
                            if note.is_note:
                                pitch = chord.to_pitch(note)
                                if current_pitch == pitch:
                                    mel.notes[idx] = Continuation(note.duration)
                                current_pitch = pitch
                            elif note.is_continuation:
                                pass
                            else:
                                current_pitch = None

        return new_score

