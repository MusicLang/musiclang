from musiclang import Note
from musiclang import Silence

class Patternator:

    def __init__(self, restart_each_chord=False):
        self.restart_each_chord = restart_each_chord

    def __call__(self, pattern, score):
        if not self.restart_each_chord:
            projected = pattern.project_on_score(score,
                                                 keep_score=True,
                                                 allow_override=True,
                                                 repeat_to_duration=True)

        else:
            projected = None
            for chord in score.chords:
                projected_chord = pattern.project_on_score(chord, keep_score=True,
                                                           allow_override=True,
                                                           repeat_to_duration=True)
                projected += projected_chord
        for c1, c2 in zip(projected.chords, score.chords):
            parts = pattern.parts
            parts = [p for p in parts if p in c2.score.keys()]
            voicing = []
            for idx, part in enumerate(parts):
                voicing.append(c2.score[part].notes[0])

            voicing = list(sorted(voicing, key=lambda note: c1.to_pitch(note)))
            for idx, part in enumerate(parts):
                for id_note, note in enumerate(c1.score[part].notes):
                    if note.type == 'x':
                        current_note = c1.score[part].notes[id_note]
                        replaced = current_note.replace(note, voicing[note.val], octave=False)
                        c1.score[part].notes[id_note] = replaced

        return projected