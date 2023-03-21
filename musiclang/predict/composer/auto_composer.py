from musiclang import Score
from .composer import Composer

from musiclang import Tonality, ScoreFormatter, Element
from musiclang.transform.library import VoiceLeading

def auto_compose(melody, harmony, orchestra, voicing, patternator,
                 tonality, solo_instrument, instruments, acc_amp='mf',
                 fixed_bass=True
                 ):

    real_tonality = Element(0) % Tonality.from_str(tonality)
    bass = 'v__0'
    temp_instruments = [f'v__{i}' for i in range(len(instruments))]
    score_theme = real_tonality(**{'m__0': melody}).to_absolute_note()
    chords = ScoreFormatter(harmony, instruments=temp_instruments, voicing=voicing).parse()
    score = score_theme.project_on_score(chords, keep_pitch=True, voice_leading=True, keep_score=True)
    fixed_voices = ['m__0']
    if fixed_bass:
        fixed_voices.append(bass)
    score = VoiceLeading(fixed_voices=fixed_voices)(score)
    score = patternator(orchestra().set_amp(acc_amp), score)
    score = score.replace_instruments(**{temp_instr: instr for temp_instr, instr in zip(temp_instruments, instruments)})
    score = score.replace_instruments(**{f'm__0': solo_instrument})
    return score


class AutoComposer:
    """
    Class for composing a piece automatically using an annotation generator model from musiclang_predict
    """

    def __init__(self, model, parts, tonalities, form, form_orchestra, orchestras, signature=(4, 4), **kwargs):
        self.model = model
        self.parts = parts
        self.tonalities = tonalities
        self.form = form
        self.form_orchestra = form_orchestra
        self.signature = signature
        self.orchestras = orchestras
        self.kwargs = kwargs

    def predict(self, signature, tonality, temperature=1.0, max_new_tokens=500, seed=None, **kwargs):
        start = f"Time Signature: {signature[0]}/{signature[1]}\nm0 {tonality}:"
        return self.model.predict(start=start,
                             temperature=temperature,
                             max_new_tokens=max_new_tokens,
                             seed=seed)

    def compose(self, **kwargs):
        """
        Main method to compose a song automatically with the provided material

        Parameters
        ----------
        kwargs

        Returns
        -------
        score: Score
        text: str
            Final annotation predicted by the auto composer

        """
        progressions = self.get_progressions(**kwargs)
        composer = Composer(progressions,
                            self.form,
                            self.form_orchestra,
                            self.orchestras,
                            signature=self.signature,
                            **self.kwargs)
        return composer.compose()

    def get_progressions(self, **kwargs):
        progressions = []
        for idx, (nb_bars, tonality) in enumerate(zip(self.parts, self.tonalities)):
            progression = self.predict(self.signature, tonality, **kwargs)
            progression = self.get_n_bars(nb_bars, progression)
            progressions.append(progression)
        return progressions

    def line_is_bar(self, line):
        return line.lstrip(' ').startswith('m')

    def get_n_bars(self, n, progression):
        lines = progression.split('\n')
        bars = [line for line in lines if self.line_is_bar(line)]
        new_lines = []
        nb_bars = 0
        for line in lines:
            if self.line_is_bar(line):
                new_lines.append(bars[nb_bars % len(bars)])
                nb_bars += 1
            else:
                new_lines.append(line)
            if nb_bars == n:
                break
        if nb_bars < n:
            for i in range(nb_bars, n):
                new_lines.append(bars[(nb_bars + i) % len(bars)])

        return '\n'.join(new_lines)
