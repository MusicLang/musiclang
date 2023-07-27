
from .composer import Composer

from musiclang import Tonality, ScoreFormatter, Element, Chord, Note, Score
from musiclang.transform.library import VoiceLeading
from musiclang.transform.composing.pattern import Pattern
from musiclang.library import NC

import numpy as np

def apply_pattern(pattern, chords, instruments=None, voicing=None, restart_each_chord=False,
                  fixed_bass=True, voice_leading=True, amp='mf'):
    """
    Apply a pattern to a chord progression
    Parameters
    ----------
    pattern: Score or Chord
        Pattern to use
    chords: Score or list
        Chord progression to use
    instruments: list[str] or None
        Instruments to use, by default use only piano
    voicing: list[Note] or None
        Voicing to use in the pattern. By default, spread the voicing between root -2 octave and fifth +1 octave
    restart_each_chord: bool
        If True, the pattern will be restarted at each chord
    fixed_bass: bool
        If True, the bass will be fixed in the voice leading
    voice_leading: bool
        If True, the voice leading optimizer will be applied
    amp: str
        Amplitude of the pattern (in ppp, pp, p, mp, mf, f, ff, fff)

    Returns
    -------
    Score

    """

    orchestra = {'bar_duration': pattern.duration, 'nb_instruments': len(pattern.instruments), 'pattern': pattern}

    if isinstance(chords, (list, tuple)):
        chords = sum(chords, None)
    if isinstance(chords, Chord):
        chords = Score(chords)
    if instruments is None:
        instruments = [f'piano' for i in range(orchestra['nb_instruments'])]

    # Clean instruments
    real_instruments = _clean_instrument_names(instruments)

    if voicing is None:
        values = np.linspace(-6, 5, orchestra['nb_instruments']).astype(int)
        voicing = [Note('b', value % 3, value // 3, 1) for value in values]

    patternator = {'restart_each_chord': restart_each_chord}
    return auto_compose([], chords, orchestra, voicing, patternator,
                 "C", [], real_instruments, acc_amp=amp,
                 fixed_bass=fixed_bass, voice_leading=voice_leading
                 )

def _clean_instrument_names(instruments):
    """
    Given a list of raw instrument, spread the voice indexes accordingly
    eg : ['piano', 'piano'] -> ['piano__0', 'piano__1']
    Returns
    -------
    list[str]
    """
    real_instruments = []
    instrument_dict = {}
    for instrument in instruments:
        clean_instrument = ''.join(instrument.split('__')[:-1])
        instrument_dict[clean_instrument] = instrument_dict.get(clean_instrument, -1) + 1
        index = instrument_dict[clean_instrument]
        real_instruments.append(instrument + f'__{index}')

    return real_instruments

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
    if isinstance(harmony, str):
        chords = ScoreFormatter(harmony, instruments=flat_temp_instruments, voicing=flat_voicings).parse()
    else:
        chords = sum([chord(**{ins: voicing.set_duration(chord.duration)
                               for ins, voicing in zip(flat_temp_instruments, flat_voicings)}) for chord in harmony.to_score().chords], None)

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

    score = VoiceLeading(fixed_voices=fixed_voices)(score, max_norm=2, max_norm_rules=2)

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
