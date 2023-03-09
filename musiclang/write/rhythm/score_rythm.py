from typing import Dict
from .metric import Metric

class ScoreRhythm:
    """
    Helper class to apply rhythms
    """

    def __init__(self, rhythm_dict):
        self.rhythm_dict: Dict[Metric] = rhythm_dict

    def signature(self, part):
        return self.rhythm_dict[part].signature

    def tatum(self, part):
        return self.rhythm_dict[part].tatum

    def array(self, part):
        return self.rhythm_dict[part].array

    def nb_bars(self, part):
        return self.rhythm_dict[part].nb_bars

    def duration(self, part):
        return self.rhythm_dict[part].duration

    def __call__(self, score, **kwargs):
        """
        Apply the rythm dict to the score, keeping durations

        Parameters
        ----------
        score
        kwargs

        Returns
        -------
        """

        new_score = None
        time = 0
        for chord in score.chords:
            duration = chord.duration
            new_part = {}
            for part in chord.parts:
                if part in self.rhythm_dict:
                    bar_time_start = time
                    bar_time_end = (time + chord.duration)
                    if bar_time_end == 0:
                        bar_time_end = self.duration(part)
                    assert bar_time_end - bar_time_start > 0, str((bar_time_end, bar_time_start, self.duration(part)))
                    try:
                        temps_melody = self.rhythm_dict[part].apply_to_melody(chord.score[part], start=bar_time_start, end=bar_time_end)
                        melody = temps_melody
                    except IndexError:
                        melody = chord.score[part].augment(chord.duration/chord.score[part].duration).to_melody()

                    assert melody.duration == chord.duration


                else:
                    melody = chord.score[part]
                new_part[part] = melody

            new_score += chord(**new_part)
            time += duration

        return new_score

