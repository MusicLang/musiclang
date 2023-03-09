import joblib
import os
import pandas as pd
from musiclang.write.elements import ChordElement

class Arranger:

    def __init__(self, directory):
        self.directory = directory
        filepath_states = os.path.join(self.directory, 'states.pickle')
        filepath_priors = os.path.join(self.directory, 'priors.pickle')
        filepath_transitions = os.path.join(self.directory, 'transitions.pickle')
        filepath_emissions = os.path.join(self.directory, 'emissions.pickle')
        self.states = joblib.load(filepath_states)
        self.priors = self._to_series(joblib.load(filepath_priors))
        self.transitions = self._to_dataframe(joblib.load(filepath_transitions))
        self.emissions = self._to_dataframe(joblib.load(filepath_emissions))

    @staticmethod
    def _to_dataframe(x):
        return {key: pd.DataFrame(val) for key, val in x.items()}

    @staticmethod
    def _to_series(x):
        return {key: pd.Series(val) for key, val in x.items()}

    def arrange(self, melody, tonality, candidates=None, instrument='piano', eps=1e-5):

        # melody= [[(s0, 1), (s1, 0)], [], []]

        # Get pitches from melody
        base_chord = ChordElement.get_tonic_chord(tonality)
        pitches = []
        curr_pitch = None
        for chord_change in melody:
            temp_pitches = []
            for note, is_in_chord in chord_change:
                if is_in_chord and not note.is_silence:
                    curr_pitch = base_chord.to_pitch(note, last_pitch=curr_pitch)
                    temp_pitches.append(curr_pitch)

            pitches.append(temp_pitches)
        if candidates is None:
            candidates = [None] * len(pitches)

        chords, proba = self.get_chord_progression(pitches, candidates, tonality,
                                              self.states,
                                              self.priors,
                                              self.transitions,
                                              self.emissions,
                                              eps=eps)
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
                emit = emit_p[st][obs[t]]
            else:
                emit = 1.0
                for ob in obs[t]:
                    emit *= emit_p[st][ob]
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
        max_prob = 0.0
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

    def get_chord_progression(self, pitches, candidates, tonality, states, priors, transitions, emissions, eps=1e-5):
        # Get pitch relative to tonality
        tone, mode = ChordElement.get_key_mode(tonality)
        obs = [(p - tone) % 12 if isinstance(p, int) else [(pi - tone) % 12 for pi in p] for p in pitches]
        chords, prob = self.viterbi(obs,
                               candidates,
                               states[mode],
                               (priors[mode] + eps).to_dict(),
                               (transitions[mode].T + eps).to_dict(),
                               (emissions[mode].T + eps).to_dict(),
                               eps=eps)

        return chords, prob

