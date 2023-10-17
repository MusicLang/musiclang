

def best_voice_leading(fpd, pcd):
    pass


import numpy as np

class Rules:

    PARALLEL_OCTAVES = 'parallel_octaves'
    PARALLEL_FIFTHS = 'parallel_fifths'
    PARALLEL_DISSONNANCES = 'parallel_dissonnances'
    CROSSING = 'no_crossing'
    UNISSON = 'no_unisson'


ALL_RULES = [Rules.PARALLEL_OCTAVES, Rules.PARALLEL_FIFTHS,
             Rules.PARALLEL_DISSONNANCES, Rules.CROSSING,
             Rules.UNISSON]


class VoiceLeading:
    """
    This class is responsible of optimizing a voice leading on the first notes of a chord progression.

    - It first tries to minimize the movement of voices between each chords
    - It then finetune the solution using classic voice movement rules that are parametrizable (parallel octaves, fifths...)

    .. warning:: We strongly advise to first derive a good chord progression, then apply voice leading algorithm, then apply rythms
    and melodies because this class only deals with the first note of a chord.

    Examples
    --------
    >>> from musiclang.library import *
    >>> from musiclang.transform import VoiceLeading

    >>> score = (I % I.M)(cello=s0, violin=s1) * 2
    >>> vl = VoiceLeading(fixed_voices=['cello__0'], seed=5)
    >>> new_score = vl.optimize(score, method='voices_and_rules', max_iter=1000, max_iter_rules=100, max_norm=3)
    >>> print(new_score)
    (I % I.M)(cello=s0, violin=s1) + (I % I.M)(cello=s0, violin=s2)

    It has automatically solved the parallel dissonnance issue.
    """

    TYPES = ['b', 'c', 's', 'h']
    RULES = Rules

    def __init__(self, types=None, rules=None, exclude_rules=None, fixed_voices=None, change_octave_fixed=True, seed=34, method='voices_and_rules', **kwargs):
        """

        Parameters
        ----------
        types: None or list[str], default will be ['b', 'c', 's', 'h']
            List of types on which to apply the algorithm, if not present the notes will act as fixed voices
        rules: list of str in ALL_RULES
            Rules to apply if you use "voices_and_rules" or "rules" optimizer
            Existing rules are :
            - parallel_octaves
            - parallel_fifths
            - parallel_dissonnances
        fixed_voices: list[str]
            List of name of voice (with voice idx like piano__0) to not modify
        change_octave_fixed: list[str] or boolean or None
            Do we apply the octave change for the fixed voices (useful to set to true for bass)
        seed: int
            Seed used for random generation to get reproducible results
        """
        self.types = types if types is not None else self.TYPES
        self.fixed_voices = [] if (fixed_voices is None) else fixed_voices
        self.change_octave_fixed = change_octave_fixed
        if isinstance(self.change_octave_fixed, bool):
            self.change_octave_fixed = [self.change_octave_fixed for i in self.fixed_voices]

        self.rules = rules if rules is not None else ALL_RULES
        self.seed = seed
        self.rg = np.random.RandomState(seed)
        self.method = method
        self.kwargs = kwargs
        if exclude_rules is not None:
            self.rules = [r for r in self.rules if r not in exclude_rules]

    def optimize(self, score, skip=False, **kwargs):
        """
        Main entry point to optimize a score

        Parameters
        ----------
        score: Score
            Musiclang score on which to apply voice leading algorithm
        method: str
            Method, existing are : "voices", "voices_and_rules", "rules", "random"
            - voices : Try to create a parcimonious voice leading, starting with the proposed solution
            - rules : Try to erase voices movements errors (like parallel octaves or fifths)
            - voices_and_rules: Combo of both
            - random: Same metric as "voices" but the optimisation algorithm is completely random, use only if you know what you do

        kwargs: **kwargs
            Optimizer parameters
            - max_iter: Number of iteration of parcimonious voices optimizer
            - max_iter_rules: Number of iteration of harmonic rules enforcer
            - max_norm: Max movement allowed in term of relative value of note, set low if you want minimal changes
            - temperature: Set high for high degree of randomness
            - min_temperature: Temperature at the end of the voice optimisation (only for voice optimisation)

        Returns
        -------

        """
        self.init(score)
        self.rg = np.random.RandomState(self.seed)
        dvals = np.zeros(self.pitch.shape, dtype=np.int16)
        # DO OPTIMIZATION HERE
        #solution = self.random_optim(dvals, **kwargs)
        if self.method == 'voices_and_rules':
            solution = self.voices_and_rules(dvals, **self.kwargs)
        elif self.method == 'voices':
            solution = self.voices_optim(dvals, **self.kwargs)
        elif self.method == 'rules':
            solution = self.optimize_rules(dvals, **self.kwargs)
        elif self.method == 'random':
            solution = self.random_optim(dvals, **self.kwargs)
        else:
            raise Exception('Not existing method, existing are : "voices", "voices_and_rules", "rules", "random"')
        #######################

        return self.get_score(score, solution)

    def find_optimal_octaves(self, score):
        """
        Find optimal chord octaves, to get the most constant bass pitch
        Parameters
        ----------
        score

        Returns
        -------

        """
        def recursive_correct_octave(chord):
            bass_pitch = chord.bass_pitch
            if bass_pitch > 6:
                new_chord = chord.o(-1)
                for voice, change in zip(self.fixed_voices, self.change_octave_fixed):
                    if not change:
                        new_chord.score[voice] = new_chord.score[voice].o(1)
                return recursive_correct_octave(new_chord)
            elif bass_pitch <= -6:
                new_chord = chord.o(1)
                for voice, change in zip(self.fixed_voices, self.change_octave_fixed):
                    if not change:
                        new_chord.score[voice] = new_chord.score[voice].o(-1)
                return recursive_correct_octave(new_chord)
            else:
                return chord

        new_score = None
        for chord in score.chords:
            new_score += recursive_correct_octave(chord)
        return new_score

    def __call__(self, score, skip=False, **kwargs):
        # First Find best chords octaves
        score = self.find_optimal_octaves(score)
        if skip:
            return score
        new_score = self.optimize(score, **kwargs)
        return new_score

    def init(self, score):
        """
        Given existing chord progression find the best voice leading on given types, don't change other
        kinds of notes.
        Apply only for the first note of melodies chords

        Parameters
        ----------
        score: Score
            Score on which to apply the voice leading

        types: list[str]
            Types on which to apply a voice leading

        """
        import numpy as np

        score = score.to_score(copy=False).normalize_instruments()
        self.instruments = score.instruments

        pitches_chords = [chord.chord_pitches for chord in score.chords]
        pitches_extensions = [chord.chord_extension_pitches for chord in score.chords]
        pitches_scale = [chord.scale_pitches for chord in score.chords]
        pitches_chromatic = [chord.chromatic_scale_pitches for chord in score.chords]
        pitches_absolute = list(range(12))
        self.candidates_raw = [{
            'b': pitches_extensions[i],
            'c': pitches_chords[i],
            's': pitches_scale[i],
            'h': pitches_chromatic[i],
            'a': pitches_absolute,
            'r': [0],
            'l': [0],
            'bass': pitches_extensions[i][0]
        } for i in range(len(score.chords))]

        self.array = [[chord.score[ins].notes[0] for chord in score.chords]
                      for ins in self.instruments]
        self.type = np.asarray([[i.type for i in j] for j in self.array])
        self.val = np.asarray([[i.val for i in j] for j in self.array]).astype(np.int16)
        self.octave = np.asarray([[i.octave for i in j] for j in self.array]).astype(np.int16)
        self.pitch = np.asarray([[chord.to_pitch(chord.score[ins].notes[0]) or 0 for chord in score.chords]
                                 for ins in self.instruments]).astype(np.int16)

        idxs_instruments = [self.instruments.index(f) for f in self.fixed_voices]
        self.dvalsmask = np.ones(self.pitch.shape, dtype=np.int16)
        # Mask instruments
        for idx in idxs_instruments:
            self.dvalsmask[idx, :] = 0
        # Mask silences and continuations
        type_mask = np.zeros(self.dvalsmask.shape)
        for type in self.types:
            type_mask += 1 * (self.type == type)
        type_mask = 1 * (type_mask > 0)
        self.dvalsmask *= type_mask.astype(np.int16)
        self.candidates = [[self.candidates_raw[idxc][self.type[idxi, idxc]]
                            for idxc, chord in enumerate(score.chords)]
                           for idxi, instrument in enumerate(self.instruments)]

        return score

    def get_candidate_at(self, idx_ins, idx_chord):
        return self.candidates[idx_ins][idx_chord]

    def get_current_pitch_at(self, idx_ins, idx_chord):
        return self.pitch[idx_ins, idx_chord]

    def get_pitch_solution(self, dvals):
        new_vals = self.val + dvals
        octs = self.octave
        pitches = np.asarray([[self.candidates[idxi][idxc][new_val % len(self.candidates[idxi][idxc])]
                               + 12 * (new_val // len(self.candidates[idxi][idxc]))
                               for idxc, new_val in enumerate(row)]
                              for idxi, row in enumerate(new_vals)])
        pitches += 12 * octs

        return pitches


    def crossing_and_unisson_score(self, dvals):
        pitches = self.get_pitch_solution(dvals)
        crossings = np.std(pitches.argsort(axis=0), axis=1)
        crossing_score = np.sum(np.power(crossings, 2))
        return crossing_score

    def eval_solution(self, dvals):
        pitches = self.get_pitch_solution(dvals)
        # Minimize movement
        movement = self.get_movement(pitches)
        movement_score = np.mean(np.power(np.abs(movement), 1))
        # Check if crossings are present
        crossing_score = self.crossing_and_unisson_score(dvals)
        total_score = 10 * crossing_score + movement_score
        # space = np.diff(pitches, axis=0)
        # space_score =  np.mean(np.power(space, 2))
        return total_score

    def get_movement(self, pitches):
        movement = np.diff(pitches, axis=1)
        return movement



    def random_optim(self, dvals, max_iter=250, max_norm=3, **kwargs):
        solutions = [dvals + self.rg.randint(-max_norm, max_norm + 1, dvals.shape) for i in range(max_iter - 1)]
        solutions.append(dvals)
        scores = [self.eval_solution(sol) for sol in solutions]
        best = np.argmin(scores)

        return solutions[best]

    def voices_optim(self, dvals, max_iter=100, max_norm=3, temperature=8, min_temperature=1, **kwargs):
        min_score = self.eval_solution(dvals)
        start_temp = temperature
        end_temp = min_temperature
        for it in range(max_iter):
            pitches = self.get_pitch_solution(dvals)
            mov = self.get_movement(pitches).astype(np.float32)  # Find movements
            mov *= self.dvalsmask[:, :-1]
            sgn_mov = np.sign(mov)
            # Find probabilities of moving an index
            proba = np.exp(mov/temperature)/np.sum(np.exp(mov/temperature))
            assert np.max(proba) <= 1
            # Sample index given proba
            delta1 = sgn_mov * (self.rg.random(mov.shape) < proba)
            delta1 = (np.c_[delta1, np.zeros(len(delta1))])
            delta2 = - sgn_mov * (self.rg.random(mov.shape) < proba)
            delta2 = (np.c_[np.zeros(len(delta2)), delta2])
            mov = (delta1 + delta2).astype(int)
            proposed_sol = (dvals + mov).clip(-max_norm, max_norm)
            score = self.eval_solution(proposed_sol)
            if score < min_score:
                min_score = score
                dvals = proposed_sol
            coeff = (it / max_iter)
            temperature = coeff * end_temp + (1 - coeff) * start_temp

        self.eval_solution(dvals)

        return dvals
        # Move in direction of sgn


    def optimize_rules(self, dvals, max_iter_rules=100, max_norm_rules=3, temperature=1, **kwargs):

        def eval_solution(dvals):
            pitches = self.get_pitch_solution(dvals)
            problems = self.get_problems(pitches)
            return np.sum(problems)

        pitches = self.get_pitch_solution(dvals)
        problems = self.get_problems(pitches)
        min_score = eval_solution(dvals)
        crossing_and_unisson_score = self.crossing_and_unisson_score(dvals)
        tried = set()
        for i in range(max_iter_rules):
            pitches = self.get_pitch_solution(dvals)
            problems = self.get_problems(pitches)
            noise = 0.0
            proba = np.exp((problems + noise)/temperature)/np.sum(np.exp((problems + noise)/temperature))
            m, M = -1, 2
            delta = self.rg.randint(-max_norm_rules, max_norm_rules+1, proba.shape) * (self.rg.random(proba.shape) < proba)
            delta = delta.clip(-max_norm_rules, max_norm_rules)
            proposed_sol = (dvals + delta)
            proposed_sol *= self.dvalsmask
            proposed_set = tuple(proposed_sol.flatten().tolist())
            if proposed_set in tried:
                continue
            else:
                tried.add(proposed_set)

            score = eval_solution(proposed_sol)
            crossing_and_unisson_score_new = self.crossing_and_unisson_score(proposed_sol)
            if score < min_score and crossing_and_unisson_score_new <= crossing_and_unisson_score:
                min_score = score
                dvals = proposed_sol
                crossing_and_unisson_score = crossing_and_unisson_score_new
            if min_score == 0:
                break
        score = self.eval_solution(dvals)
        return dvals

    def get_val(self, pitches, v1, v2, idxc):
        if idxc >= pitches.shape[1]:
            return -1
        if self.type[v1, idxc] in ['r', 'l']:
            return -1
        if self.type[v2, idxc] in ['r', 'l']:
            return -1

        return abs(pitches[v1, idxc] - pitches[v2, idxc]) % 12

    def get_problems(self, pitches):
        # Parallel only counts if movement is not null
        movement = self.get_movement(pitches)
        moving = movement != 0
        dissonnances = {1, 2, 6, 11, 10}
        # Find intervals between all instruments
        intervals = np.zeros((pitches.shape[0], *pitches.shape))
        abs_intervals = np.zeros((pitches.shape[0], *pitches.shape))
        parallel_fifths = np.zeros(pitches.shape)
        parallel_octaves = np.zeros(pitches.shape)
        parallel_dissonnances = np.zeros(pitches.shape)
        unissons = np.zeros(pitches.shape)
        crossings = np.zeros(pitches.shape)
        for v1 in range(pitches.shape[0]):
            for v2 in range(pitches.shape[0]):
                if v2 >= v1:
                    break
                for idxc in range(pitches.shape[1]):
                    rel_val = pitches[v1, idxc] - pitches[v2, idxc]
                    abs_val = abs(rel_val)
                    val = abs_val % 12
                    intervals[v1, v2, idxc] = val
                    intervals[v2, v1, idxc] = val
                    abs_intervals[v1, v2, idxc] = abs_val
                    if Rules.PARALLEL_FIFTHS in self.rules:
                        if val == 7 and val == self.get_val(pitches, v1, v2, idxc + 1):
                            parallel_fifths[v1, idxc] += 1
                            parallel_fifths[v2, idxc] += 1
                            parallel_fifths[v1, idxc + 1] += 1
                            parallel_fifths[v2, idxc + 1] += 1

                    if Rules.PARALLEL_OCTAVES in self.rules:
                        if val == 0 and val == self.get_val(pitches, v1, v2, idxc + 1):
                            parallel_octaves[v1, idxc] += 1
                            parallel_octaves[v2, idxc] += 1
                            parallel_octaves[v1, idxc + 1] += 1
                            parallel_octaves[v2, idxc + 1] += 1
                    if Rules.PARALLEL_DISSONNANCES in self.rules:

                        if val in dissonnances and self.get_val(pitches, v1, v2, idxc + 1) in dissonnances:
                            parallel_dissonnances[v1, idxc] += 1
                            parallel_dissonnances[v2, idxc] += 1
                            parallel_dissonnances[v1, idxc + 1] += 1
                            parallel_dissonnances[v2, idxc + 1] += 1
                    if Rules.CROSSING in self.rules:
                        if rel_val < 0:
                            crossings[v1, idxc] += 3
                            crossings[v2, idxc] += 3
                    if Rules.UNISSON in self.rules:
                        if abs_val == 0:
                            unissons[v1, idxc] += 5
                            unissons[v2, idxc] += 5

        problems = parallel_fifths + parallel_octaves + parallel_dissonnances + unissons + crossings
        has_crossing_or_unisson = crossings + unissons
        problems *= self.dvalsmask
        return problems


    def voices_and_rules(self, dvals, **kwargs):
        dvals = self.voices_optim(dvals, **kwargs)
        # REMOVE CONSECUTIVE FIFTHS AND OCTAVES
        dvals = self.optimize_rules(dvals, **kwargs)

        return dvals




    def get_corrected_note(self, note, new_vals, idx_ins, idx_chord):
        nb = len(self.get_candidate_at(idx_ins, idx_chord))
        new_val = new_vals[idx_ins, idx_chord]
        note.val = int(new_val % nb)
        note.octave += int(new_val // nb)
        return note

    def get_score(self, score, dvals):
        new_score = score.copy()
        new_vals = self.val + dvals
        for idx_chord, chord in enumerate(new_score.chords):
            for idx_ins, ins in enumerate(self.instruments):
                if ins in chord.score.keys():
                    first_note = chord.score[ins].notes[0]
                    if not first_note.is_silence and not first_note.is_continuation:
                        chord.score[ins].notes[0] = self.get_corrected_note(first_note, new_vals, idx_ins, idx_chord)

        return new_score

