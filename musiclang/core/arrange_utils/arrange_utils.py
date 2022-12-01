import numpy as np
import pandas as pd


class Solution:
    def get_skyline(self, notes):
        """
        :type notes: List[List[int]]
        :rtype: List[List[int]]
        """
        if not notes:
            return []
        if len(notes) == 1:
            return [[notes[0][0], notes[0][2]] + notes[0][3:], [notes[0][1], 0] + notes[0][3:]]

        mid = len(notes) // 2
        left = self.get_skyline(notes[:mid])
        right = self.get_skyline(notes[mid:])
        return self.merge(left, right)

    def merge(self, left, right):
        h1, h2 = 0, 0
        i, j = 0, 0
        note1, note2 = [], []
        result = []

        while i < len(left) and j < len(right):
            if left[i][0] < right[j][0]:
                h1 = left[i][1]
                note1 = left[i][2:]
                corner = left[i][0]
                i += 1
            elif right[j][0] < left[i][0]:
                h2 = right[j][1]
                note2 = right[j][2:]
                corner = right[j][0]
                j += 1
            else:
                h1 = left[i][1]
                note1 = left[i][2:]
                h2 = right[j][1]
                note2 = right[j][2:]
                corner = right[j][0]
                i += 1
                j += 1
            if self.is_valid(result, max(h1, h2)):
                max_note = [note1, note2][np.argmax([h1, h2])]
                result.append([corner, max(h1, h2)] + max_note)
        result.extend(right[j:])
        result.extend(left[i:])
        return result

    def is_valid(self, result, new_height):
        return not result or result[-1][1] != new_height



def reduce_one(sequence, high=True):
    sequence = sequence.copy()
    SILENCE_ABS_VAL = 2000
    silence_value = -SILENCE_ABS_VAL if high else SILENCE_ABS_VAL
    # Use skyline algorithm to find height map
    notes = sequence[['start', 'end', 'pitch', 'note', 'chord', 'chord_idx', 'instrument', 'note_idx']].fillna(
        silence_value)

    if not high:
        notes['pitch'] = - notes['pitch']
    notes['pitch'] += SILENCE_ABS_VAL

    # Add little randomness to store equals pitches
    random_noise = np.random.random(len(notes)) / 3
    notes['pitch'] += random_noise
    notes = notes.values.tolist()
    solution = pd.DataFrame(Solution().get_skyline(notes),
                            columns=['start', 'pitch', 'note', 'chord', 'chord_idx', 'instrument', 'note_idx'])
    solution['end'] = solution['start'] + solution['start'].diff(1).shift(-1)
    solution['pitch'] -= SILENCE_ABS_VAL
    if not high:
        solution['pitch'] = - solution['pitch']
    solution.loc[solution['pitch'] == silence_value, 'pitch'] = np.nan
    solution = solution.iloc[:-1]
    return solution

def reduce(score, n_voices=4, start_low=False, instruments=None):
    """
    Arrange a score to sum it up of 4 voices
    :param score:
    :param n_voices:
    :return:
    """

    from ..note import Silence
    sequence = score.to_sequence()

    # Use skyline algorithm to find enveloppes
    if instruments is None:
        instruments = [f'piano__{idx}' for idx in range(n_voices)]
    if not start_low:
        instruments = instruments[::-1]
    idxs = [0, -1, 1, -2, 2, -3, 3, -4, 4, -5, 5, -6, 6][:n_voices]
    solutions = []
    for i, idx in enumerate(idxs):
        solution = reduce_one(sequence, high=(i % 2) == 1 * start_low)
        solution['instrument'] = instruments[idx]
        solutions.append(solution)
        # Replace all solution notes in sequence with silences
        replace_silence = set(solution['note_idx'].unique())
        indexer = sequence['note_idx'].isin(replace_silence)
        len_indexer = indexer.sum()
        sequence.loc[indexer, 'note'] = [Silence(1) for i in range(len_indexer)]
        sequence.loc[indexer, 'pitch'] = np.nan

    solution = pd.concat(solutions, axis=0).sort_values('start')

    # For each voice reassign to most probable pitch average
    # Recalculate pitch
    solution['pitch'] = solution.apply(lambda x: x['chord'].to_pitch(x['note']), axis=1)
    # Recalculate is_silence
    solution['is_silence'] = solution['note'].apply(lambda x: x.is_silence)
    solution['is_continuation'] = solution['note'].apply(lambda x: x.is_continuation)
    solution['is_note'] = solution['note'].apply(lambda x: x.is_note)
    # For each chord remove voices with only silences
    # For each chord each voice calculate average pitch
    # Then starting with first chord reassign each voice with closenessness of average pitch

    # Remove silences

    # Parse solution to new sequence
    from ..score import Score
    score_result = Score.from_sequence(solution)
    return score_result


def optimize_voices(score):
    """
    Reduce the number of voices if possible, maximize number of notes in already big voices
    :param score:
    :param n_voices:
    :param start_low:
    :param instruments:
    :return:
    """
    from ..note import Silence
    sequence = score.to_sequence()

    # Find path
    nb_parts = [len(chord.parts) for chord in score]




    from pdb import set_trace; set_trace()


