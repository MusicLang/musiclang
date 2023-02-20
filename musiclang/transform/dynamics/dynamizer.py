import numpy as np


class PitchDynamizer:
    """
    Create the dynamics with the average pitch of each chord
    If ascending is true : A higher average pitch means an higher dynamic for this dynamizer
    if ascending is false, the contrary
    """

    def __init__(self, minimum=30, maximum=110, ascending=True):
        self.minimum = minimum
        self.maximum = maximum
        self.ascending = ascending

    def __call__(self, score, **kwargs):

        # Calculate mean pitch per chords

        pitches = []
        for chord in score.chords:
            pitches_ = [chord.to_pitch(n) for part in chord.parts for n in chord.score[part].notes if n.is_note]
            pitches.append(np.mean(pitches_))

        # min max
        minimum = self.minimum
        maximum = self.maximum

        pitches = [(p - np.min(pitches)) / (np.max(pitches) - np.min(pitches)) for p in pitches]
        if not self.ascending:
            amps = [(p * minimum) + (1 - p) * maximum for p in pitches]
        else:
            amps = [(p * maximum) + (1 - p) * minimum for p in pitches]

        for i in range(5):
            amps = [(a + b)/2 for a, b in zip(amps, [amps[0]] + amps[:-1])]

        new_score = None
        for chord, amp in zip(score.chords, amps):
            new_score += chord.set_amp(amp)

        return new_score