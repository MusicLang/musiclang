import numpy as np
import pandas as pd
from musiclang.write.elements import ChordElement
import glob
import os
import joblib


class ArrangerTrainer:

    def __init__(self, files_regex, output_directory):
        """

        Parameters
        ----------
        files_regex: str
            File regex that will be used for training
        output_directory: str
            Where the arrangement model will be saved
        """
        self.directory = files_regex
        self.output_directory = output_directory


    def train(self, nb_candidates=None):
        """
        Train the arranger model
        Parameters
        ----------
        nb_candidates: int
            Number of chords to keep per mode, will reduce the size of the transition matrix

        Returns
        -------

        """
        files = glob.glob(self.directory)
        self.texts = []
        for file in files:
            with open(file, 'r') as f:
                self.texts.append(f.read())
        states, priors, transitions, emissions = self.find_chords(self.texts)

        # Save
        os.makedirs(self.output_directory, exist_ok=True)
        filepath_states = os.path.join(self.output_directory, 'states.pickle')
        filepath_priors = os.path.join(self.output_directory, 'priors.pickle')
        filepath_transitions = os.path.join(self.output_directory, 'transitions.pickle')
        filepath_emissions = os.path.join(self.output_directory, 'emissions.pickle')

        if nb_candidates is not None:
            # Find the most probable candidates
            keep_index = {mode: priors[mode].sort_values(ascending=False).index[:nb_candidates]
                          for mode in priors.keys()}
            priors = {mode: priors[mode].loc[keep_index[mode]]
                              for mode in priors.keys()}

            transitions = {mode: transitions[mode].loc[keep_index[mode], keep_index[mode]]
                                for mode in transitions.keys()}
            emissions = {mode: emissions[mode].loc[keep_index[mode]]
                              for mode in emissions.keys()}

            states = {mode: [s for s in states[mode] if s in keep_index[mode]] for mode in states.keys()}

        joblib.dump(states, filepath_states)
        joblib.dump(self._convert_to_dict(priors), filepath_priors)
        joblib.dump(self._convert_to_dict(transitions), filepath_transitions)
        joblib.dump(self._convert_to_dict(emissions), filepath_emissions)


    def _convert_to_dict(self, x):
        return {key: val.to_dict() for key, val in x.items()}


    def find_chords(self, texts):
        tonality = None
        mode = None
        sequences = {'M': [], 'm': []}
        indexes = {'m': set(), 'M': set()}

        # First construct the sequences
        for text in texts:
            lines = text.split('\n')
            lines = [l for l in lines if l != '' and l[0] == 'm']
            for line in lines:
                for el in line.split(' '):
                    if el == '' or el[0] == 'm':
                        pass
                    elif el.startswith('b') and el[1].isdigit():
                        pass
                    elif ':' in el and not ('|' in el):
                        new_tonality = el.replace(':', '')
                        if new_tonality != tonality:
                            tonality = new_tonality
                            mode = 'M' if new_tonality[0].upper() == el[0] else 'm'
                            sequences[mode].append([])
                    else:
                        sequences[mode][-1].append(el)
                        indexes[mode].add(el)

        # Create the proper indexes
        indexes_list = {mode: list(value) for mode, value in indexes.items()}
        indexes = {mode: {val: i for i, val in enumerate(value)} for mode, value in indexes_list.items()}
        reversed_indexes = {mode: {val: key2 for key2, val in value.items()} for mode, value in indexes.items()}

        # Construct the pitches candidates
        pitches_candidates = {'m': {}, 'M': {}}
        for mode, tone in [('m', 'c'), ('M', 'C')]:
            for pitch in range(12):
                pitches_candidates[mode][pitch] = set()
                for chord in indexes_list[mode]:
                    try:
                        if ChordElement(chord).has_pitch(pitch, tone):
                            pitches_candidates[mode][pitch].add(chord)
                    except:
                        pass

        # Construct Prior proba of chords and transition probabilities
        priors = {mode: np.zeros(len(index), dtype=np.float32) for mode, index in indexes.items()}
        transitions = {mode: np.zeros((len(index), len(index)), dtype=np.float32) for mode, index in indexes.items()}
        for mode in ['m', 'M']:
            for sequence in sequences[mode]:
                transitions_seq = list(zip(sequence, sequence[1:]))
                for chord in sequence:
                    priors[mode][indexes[mode][chord]] += 1
                for chord1, chord2 in transitions_seq:
                    transitions[mode][indexes[mode][chord1], indexes[mode][chord2]] += 1

        # Normalize probabilities
        transitions = {mode: np.nan_to_num(val / val.sum(axis=1)[:, np.newaxis]) for mode, val in transitions.items()}
        priors = {mode: val / val.sum() for mode, val in priors.items()}
        transitions = {mode: pd.DataFrame(transitions[mode],
                                          index=indexes_list[mode],
                                          columns=indexes_list[mode]) for mode in ['m', 'M']}
        priors = {mode: pd.Series(priors[mode],
                                  index=indexes_list[mode]) for mode in ['m', 'M']}

        # Create emission matrix
        emissions = {mode: pd.DataFrame(np.zeros((len(index), 12), dtype=np.float32),
                                        index=indexes_list[mode],
                                        columns=list(range(12)))
                     for mode, index in indexes.items()}
        for mode in ['m', 'M']:
            for i in range(12):
                emission = emissions[mode]
                emission.loc[list(pitches_candidates[mode][i]), i] = 1

        states = indexes_list
        return states, priors, transitions, emissions



