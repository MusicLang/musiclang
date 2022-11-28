
import numpy as np
from fractions import Fraction as frac

class BarDurationEstimator:

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def estimate(self, notes):
        feel = self._get_binary_or_ternary(notes)
        offset = self._get_offset(notes, feel)
        bar_duration, offset = self._get_chord_change_period(notes, feel, offset)
        return bar_duration, offset

    def _get_binary_or_ternary(self, notes):
        """
        Returns 2 if the notes are in a ternary feeling (Bar duration in 4/4, 2/4)
        Otherwise returns 3
        """
        As = notes[:, 0]
        Ts = np.asarray([1.5, 2, 3, 4, 4.5])
        fs = 1 / Ts
        dots = np.dot(fs[:, np.newaxis], As[np.newaxis, :])
        exps = np.exp(- 2.j * np.pi * dots)
        cnotes = np.abs(np.sum(exps, axis=1))
        cnotes /= np.max(cnotes)
        binary = np.dot([0, 1, 0, 1, 0], cnotes) / 2
        ternary = np.dot([1, 0, 1, 0, 1], cnotes) / 3
        if binary >= ternary:
            return 2
        else:
            return 3


    def _get_offset(self, notes, feel):
        if feel == 2:
            candidates = np.arange(-4, 4, 0.125)
        else:
            candidates = np.arange(-6, 6, 0.125)
        candidates = [(feel, c) for c in candidates]
        ranks_mean_pitches = self._rank_with_method(candidates, notes, self._get_mean_pitches_every_beat)
        ranks_cuts = self._rank_with_method(candidates, notes, self._get_mean_negative_cuts_every_beat)
        average_rank = (ranks_cuts * ranks_mean_pitches ** 0.2)
        best_candidates = [candidates[idx] for idx, r in enumerate(average_rank) if r == np.min(average_rank)]
        best_candidate = min(best_candidates, key=lambda x: abs(x[1]))
        return best_candidate[1]

    def _get_chord_change_period(self, notes, duration, offset):
        if duration == 2:
            candidates = [(2, offset), (4, offset)]
        elif duration == 3:
            candidates = [(frac(3, 2), offset), (3, offset), (frac(9, 2), offset), (6, offset)]
        else:
            raise Exception('Wrong candidate duration, either 2 or 3')

        means = []
        for candidate in candidates:
            means.append(self._get_mean_number_different_notes_over_threshold(notes, *candidate))
        # Get max candidate that is true
        new_candidates = [c for c, m in zip(candidates, means) if m > 0.8]
        # Else returns first
        if len(new_candidates) > 0:
            best_candidate = new_candidates[-1]
        else:
            best_candidate = candidates[0]
        return best_candidate[0], offset % best_candidate[0]

    def _find_min_max_beat(self, notes):
        """
        Return the beat of the first and last note
        """
        min_beat, max_beat = int(np.min(notes[:, 0])), int(np.max(notes[:, 0]))
        return min_beat, max_beat


    def _get_mean_number_different_notes_over_threshold(self, notes, duration, offset, threshold=5, **kwargs):
        def get_pitches(notes, beat, duration):
            starts = notes[:, 0]
            return notes[(starts >= beat) & (starts < beat + duration)][:, 1].tolist()

        min_beat, max_beat = self._find_min_max_beat(notes)
        beats = np.arange(offset, max_beat + offset + 1, duration)
        beats = beats[beats >= min_beat]
        different_pitches_per_beats = [get_pitches(notes, beat, duration)
                                       for beat in beats]

        different_pitches_per_beats = [n for n in different_pitches_per_beats if len(n) > 0]
        nb_different_pitches_per_beats = np.asarray(
            [1.0 * (len(set([p % 12 for p in n])) <= threshold) for n in different_pitches_per_beats])
        # Remove 0s
        if len(nb_different_pitches_per_beats) == 0:
            return 0
        else:
            return np.mean(nb_different_pitches_per_beats)

    def _get_mean_pitches_every_beat(self, notes, duration, offset, tol=1e-1, weights=True, **kwargs):
        """
        Return the mean number of pitches that are played ON specified beat period and offset with a tolerance
        """

        min_beat, max_beat = self._find_min_max_beat(notes)
        beats = np.arange(offset, max_beat + offset + 1, duration)
        beats = beats[beats >= min_beat]
        pitches_per_beats = [notes[abs(notes[:, 0] - beat) <= tol][:, 1].tolist()
                             for beat in beats]
        nb_pitches_per_beats = np.asarray([len(n) for n in pitches_per_beats])

        if len(nb_pitches_per_beats) == 0:
            return 0
        else:
            return np.mean(nb_pitches_per_beats)

    def _get_negative_mean_different_pitches_every_beat(self, notes, duration, offset, **kwargs):
        """
        Find average number of different pitches per bar
        :param notes:
        :param duration:
        :param offset:
        :param kwargs:
        :return:
        """

        def get_pitches(notes, beat, duration):
            starts = notes[:, 0]
            return notes[(starts >= beat) & (starts < beat + duration)][:, 1].tolist()

        min_beat, max_beat = self._find_min_max_beat(notes)
        beats = np.arange(offset, max_beat + offset + 1, duration)
        beats = beats[beats >= min_beat]
        different_pitches_per_beats = [get_pitches(notes, beat, duration)
                                       for beat in beats]

        different_pitches_per_beats = [n for n in different_pitches_per_beats if len(n) > 0]
        weighted_duration = [duration ** 0.3 for n in different_pitches_per_beats]
        nb_different_pitches_per_beats = np.asarray(
            [len(set([p % 12 for p in n])) / w for n, w in zip(different_pitches_per_beats, weighted_duration)])
        # Remove 0s
        if len(nb_different_pitches_per_beats) == 0:
            return 0
        else:
            return - np.mean(nb_different_pitches_per_beats)

    def _get_mean_negative_cuts_every_beat(self, notes, duration, offset, tol=1e-1, **kwargs):
        """
        Return the negative average of beats that are playing for each beats separated by duration and starting by offset
        It allows to measure how many notes are playing during a bar change in average (with a minus sign)
        """
        min_beat, max_beat = self._find_min_max_beat(notes)
        beats = np.arange(offset, max_beat + offset + 1, duration)
        beats = beats[beats >= min_beat]
        ends = notes[:, 0] + notes[:, 2]
        starts = notes[:, 0]
        cuts_per_beats = [notes[(starts < beat - tol) & (ends > beat + tol)][:, 1].tolist()
                          for beat in beats]
        nb_cuts_per_beatss = np.asarray([len(n) for n in cuts_per_beats])
        if len(nb_cuts_per_beatss) == 0:
            return 0
        else:
            return - np.mean(nb_cuts_per_beatss)



    def _rank_with_method(self, candidates, notes, f, **kwargs):
        from scipy.stats import rankdata
        f_results = [-f(notes, *c, **kwargs) for c in candidates]
        # Rank result with egality
        ranked_result = rankdata(f_results)
        return ranked_result



