import joblib
import os
import pandas as pd
import numpy as np
from musiclang.write.elements import ChordElement

class Arranger:

    def __init__(self, directory, nb_candidates=None):
        self.directory = directory
        filepath_states = os.path.join(self.directory, 'states.pickle')
        filepath_priors = os.path.join(self.directory, 'priors.pickle')
        filepath_transitions = os.path.join(self.directory, 'transitions.pickle')
        filepath_emissions = os.path.join(self.directory, 'emissions.pickle')
        print('Loading infos ...')
        self.states = joblib.load(filepath_states)
        self.priors = self._to_series(joblib.load(filepath_priors))
        self.transitions = self._to_dataframe(joblib.load(filepath_transitions))
        self.emissions = self._to_dataframe(joblib.load(filepath_emissions))
        print('Finished loading')
        if nb_candidates is not None:
            # Find the most probable candidates
            keep_index = {mode: self.priors[mode].sort_values(ascending=False).index[:nb_candidates]
                          for mode in self.priors.keys()}
            self.transitions = {mode: self.transitions[mode].loc[keep_index[mode], keep_index[mode]]
                                for mode in self.transitions.keys()}
            self.emissions = {mode: self.emissions[mode].loc[keep_index[mode]]
                                for mode in self.transitions.keys()}
            self.priors = {mode: self.priors[mode].loc[keep_index[mode]]
                                for mode in self.priors.keys()}

            self.states = {mode: [s for s in self.states[mode] if s in keep_index[mode]] for mode in self.states.keys()}

    @staticmethod
    def _to_dataframe(x):
        return {key: pd.DataFrame(val) for key, val in x.items()}

    @staticmethod
    def _to_series(x):
        return {key: pd.Series(val) for key, val in x.items()}

    def arrange(self, melody, tonality, candidates=None, instrument='piano',
                temperature=0.0, eps=1e-5, zero_diag=True, weak_beat_importance=0.5,
                return_score=False
                ):

        import random
        # melody= [[(s0, 1), (s1, 0)], [], []]
        tone, mode = ChordElement.get_key_mode(tonality)
        # Get pitches from melody
        base_chord = ChordElement.get_tonic_chord(tonality)
        pitches = []
        arrange_with_next = False
        for chord_change in melody:
            curr_pitch = None
            temp_pitches = []
            for note, is_in_chord in chord_change:
                if is_in_chord and not note.is_silence:
                    curr_pitch = (base_chord.to_pitch(note, last_pitch=curr_pitch) - tone) % 12
                    temp_pitches.append((curr_pitch, 1.0))
                elif not is_in_chord and note.is_continuation:
                    curr_pitch = random.choice(range(12))
                    temp_pitches.append((curr_pitch, weak_beat_importance))
                elif not is_in_chord and not note.is_silence:
                    curr_pitch = (base_chord.to_pitch(note, last_pitch=curr_pitch) - tone) % 12
                    temp_pitches.append((curr_pitch, weak_beat_importance))

            if arrange_with_next and len(temp_pitches) > 0:
                pitches = [list(temp_pitches)] * len(pitches)
                arrange_with_next = False

            if len(temp_pitches) == 0 and len(pitches) > 0:
                pitches.append(pitches[-1])

            elif len(temp_pitches) == 0 or arrange_with_next:
                pitches.append([])
                arrange_with_next = True

            if len(temp_pitches) > 0:
                pitches.append(temp_pitches)

        if candidates is None:
            candidates = [None] * len(pitches)

        chords, proba = self.get_chord_progression(pitches, candidates, tonality,
                                              self.states,
                                              self.priors,
                                              self.transitions,
                                              self.emissions,
                                              temperature=temperature,
                                              eps=eps,
                                              zero_diag=zero_diag)

        if not return_score:
            return chords
        # Re-arrange the melody inside the chords
        score = None
        for literal_chord, chord_change in zip(chords, melody):
            chord_melody = None
            chord = ChordElement(literal_chord).parse_with_tonality(tonality)
            for note, is_in_chord in chord_change:
                if note.is_note:
                    curr_pitch = base_chord.to_pitch(note, last_pitch=curr_pitch)
                    new_note = chord.parse(curr_pitch).set_duration(note.duration)
                else:
                    new_note = note.copy()
                chord_melody += new_note

            score += chord(**{instrument: chord_melody})


        return score



    def viterbi(self, obs, candidates, states, start_p, trans_p, emit_p, eps=1e-5):

        def get_emit(st, t):
            if isinstance(obs[t], int):
                # If observable is a single pitch
                emit = emit_p[st][obs[t]]
            else:
                # If multi pitches
                emit = 1.0
                for ob, strength in obs[t]:
                    emit *= emit_p[st][ob] * strength
            if candidates[t] is not None:
                if isinstance(candidates[t], str):
                    emit = 1.0 * (st == candidates[t]) + eps
                else:
                    emit = 1.0 * (st in candidates[t]) / len(candidates[t]) + eps

            return emit

        V = [{}]
        for st in states:
            V[0][st] = {"prob": start_p[st] * get_emit(st, 0), "prev": None}
        # Run Viterbi when t > 0
        for t in range(1, len(obs)):
            V.append({})
            for st in states:
                max_tr_prob = V[t - 1][states[0]]["prob"] * trans_p[states[0]][st] * get_emit(st, t)
                prev_st_selected = states[0]
                for prev_st in states[1:]:
                    tr_prob = V[t - 1][prev_st]["prob"] * trans_p[prev_st][st] * get_emit(st, t)
                    if tr_prob > max_tr_prob:
                        max_tr_prob = tr_prob
                        prev_st_selected = prev_st

                max_prob = max_tr_prob
                V[t][st] = {"prob": max_prob, "prev": prev_st_selected}

        opt = []
        max_prob = - np.inf
        best_st = None
        # Get most probable state and its backtrack
        for st, data in V[-1].items():
            if data["prob"] > max_prob:
                max_prob = data["prob"]
                best_st = st
        opt.append(best_st)
        previous = best_st

        # Follow the backtrack till the first observation
        for t in range(len(V) - 2, -1, -1):
            opt.insert(0, V[t + 1][previous]["prev"])
            previous = V[t + 1][previous]["prev"]
        return opt, max_prob

    def dptable(self, V):
        # Print a table of steps from dictionary
        yield " " * 5 + "     ".join(("%3d" % i) for i in range(len(V)))
        for state in V[0]:
            yield "%.7s: " % state + " ".join("%.7s" % ("%lf" % v[state]["prob"]) for v in V)

    def get_chord_progression(self, pitches, candidates, tonality, states, priors, transitions,
                              emissions, temperature=0.0, eps=1e-5, zero_diag=True):
        # Get pitch relative to tonality
        tone, mode = ChordElement.get_key_mode(tonality)
        #obs = [((p[0] - tone) % 12, p[1]) if isinstance(p[0], tuple) else [((pi[0] - tone), pi[1]) % 12 for pi in p] for p in pitches]
        obs = pitches
        # If temperature add random noise to each matrix
        if temperature > 0:
            priors = {m: prior + (temperature * np.random.randn(*prior.shape)) for m, prior in priors.items()}
            transitions = {m: transition + (temperature * np.random.randn(*transition.shape)) for m, transition in transitions.items()}
            emissions = {m: emission + (temperature * np.random.randn(*emission.shape)) for m, emission in emissions.items()}

        if zero_diag:
            for mode_ in transitions.keys():
                transitions[mode_] = transitions[mode_] * (1 - np.eye(*transitions[mode_].shape))
        chords, prob = self.viterbi(obs,
                               candidates,
                               states[mode],
                               (priors[mode]).to_dict(),
                               (transitions[mode].T + eps).to_dict(),
                               (emissions[mode].T + eps).to_dict(),
                               eps=eps)
        return chords, prob

