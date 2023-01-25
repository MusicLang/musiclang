from musiclang.transform import FeatureExtractor
from collections import Counter


class ExtractMainTonality(FeatureExtractor):
    """
    Return the tonality of a given score in terms of chord frequence of apparition
    """

    def action(self, score, **kwargs):
        tonalities = [chord.tonality for chord in score]
        tonality = Counter(tonalities).most_common(1)[0][0]
        return tonality


class MostCommonTonalities(FeatureExtractor):
    """
    Return the most common n tonalities of a given score in terms of chord frequence of apparition
    """

    def __init__(self, n):
        self.n = n

    def action(self, score, **kwargs):
        tonalities = [chord.tonality for chord in score]
        tonalities = [t[0] for t in Counter(tonalities).most_common(self.n)[:self.n]]
        return tonalities

