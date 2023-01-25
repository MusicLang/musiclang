from musiclang.transform import TransformGraph


from musiclang.transform.features import ExtractMainTonality
from musiclang.transform.score_merger import ConcatWithPattern, ConcatScores
from musiclang.transform.chord import Modulate


class SonataGraph(TransformGraph):
    """
    Create a simple sonata from two themes (A, B) in their own tonalities
    - Returns the pattern : A, B, A, B in A tonality
    """
    NODES = [
        ('A_TONALITY', ['A'], ExtractMainTonality()),
        ('B_TONALITY', ['B'], ExtractMainTonality()),
        ('B_TO_A', ['A_TONALITY', 'B_TONALITY'], lambda x, y: x - y),
        ('B_IN_A_TONALITY', ['B', 'B_TO_A'], lambda score, a_tone: Modulate(a_tone)(score)),
        ('Sonata', ['A', 'B', 'B_IN_A_TONALITY'], ConcatWithPattern([0, 1, 0, 2]))
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(['A', 'B'], 'Sonata', nodes=self.NODES)


class RondoGraph(TransformGraph):

    """
    Create a Rondo form from a A-theme and other themes (how many you want). Finish by the A-theme
    """

    def __init__(self, a_theme, *other_themes, **kwargs):
        inputs = [a_theme] + list(other_themes)
        themes = [a_theme]
        for theme in other_themes:
            themes.append(theme)
            themes.append(a_theme)

        nodes = [('Rondo', themes, ConcatScores())]
        super().__init__(inputs, 'Rondo', nodes=nodes)