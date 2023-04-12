from musiclang import Score

from .composer import Composer

from musiclang import Tonality, ScoreFormatter, Element
from musiclang.transform.library import VoiceLeading
from musiclang.library import NC
from musiclang.transform.composing.pattern import Pattern
def auto_compose(melody, harmony, orchestra, voicing, patternator,
                 tonality, solo_instrument, instruments, acc_amp='mf',
                 fixed_bass=True, voice_leading=True
                 ):
    from musiclang.transform import Patternator


    if isinstance(melody, list):
        melodies = melody
    else:
        melodies = [melody]

    if isinstance(voice_leading, list):
        voice_leadings = voice_leading
    else:
        voice_leadings = [voice_leading]

    if isinstance(orchestra, list):
        orchestras = orchestra
    else:
        orchestras = [orchestra]

    if isinstance(voicing, list) and not isinstance(voicing[0], list):
        voicings = [voicing]
    else:
        voicings = voicing

    if isinstance(solo_instrument, list):
        solo_instruments = solo_instrument
    else:
        solo_instruments = [solo_instrument]

    if isinstance(instruments, list) and not isinstance(instruments[0], list):
        instrumentss = [instruments]
    else:
        instrumentss = instruments

    if isinstance(fixed_bass, list):
        fixed_basses = fixed_bass
    else:
        fixed_basses = [fixed_bass for i in range(len(instrumentss))]

    real_tonality = Element(0) % Tonality.from_str(tonality)
    basses = [f'v_{j}__0' for j in range(len(instrumentss))]
    temp_instrumentss = [[f'v_{j}__{i}' for i in range(len(instr))] for j, instr in enumerate(instrumentss)]

    if len(melodies) > 0:
        score_theme = real_tonality(**{f'm__{idx}': melody for idx, melody in enumerate(melodies)}).to_absolute_note()
    else:
        score_theme = None

    flat_temp_instruments = sum(temp_instrumentss, [])
    flat_voicings = sum(voicings, [])
    chords = ScoreFormatter(harmony, instruments=flat_temp_instruments, voicing=flat_voicings).parse()

    if score_theme is not None:
        score = score_theme.project_on_score(chords, keep_pitch=True, voice_leading=True, keep_score=True)
        assert score.duration == score_theme.duration, f"Durations don't match between theme ({score_theme.duration}) and chords"
    else:
        score = chords


    fixed_voices = [f'm__{i}' for i in range(len(melodies))]
    if fixed_bass:
        fixed_voices = fixed_voices + [bass for bass, fixed_bass in zip(basses, fixed_basses) if fixed_bass]
    for instruments, voice_leading in zip(temp_instrumentss, voice_leadings):
        if not voice_leading:
            fixed_voices = fixed_voices + instruments[1:]

    score = VoiceLeading(fixed_voices=fixed_voices)(score, max_norm=3, max_norm_rules=1)

    patternator = Patternator(**patternator)
    for orchestra, temp_instruments in zip(orchestras, temp_instrumentss):
        realized_orchestra = NC(**Pattern.from_json(orchestra, instruments=temp_instruments))
        score = patternator(realized_orchestra.set_amp(acc_amp), score)

    score = score.replace_instruments(**{temp_instr: instr for temp_instruments, instruments in zip(temp_instrumentss, instrumentss)
                                         for temp_instr, instr in zip(temp_instruments, instruments)})
    score = score.replace_instruments(**{f'm__{i}': solo_instrument for i, solo_instrument in enumerate(solo_instruments)})
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
