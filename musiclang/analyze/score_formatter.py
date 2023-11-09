
from musiclang.library import *
from .score_formatter_elements import BarLine, BarChord, Beat, MultiBar, Event, TimeSignature, TonalityLine
import re
"""
The roman numeral parsed language is an extension of this paper : 
https://archives.ismir.net/ismir2019/paper/000012.pdf

By Dmitri Tymoczko Mark Gotham Michael Scott Cuthbert and Christopher Ariza

"""
DEFAULT_INSTRUMENTS = ['piano__0', 'piano__1', 'piano__2', 'piano__3']
DEFAULT_VOICING = (b0, b1, b2, b3)
class ScoreFormatter:

    def __init__(self, text, instruments=None, voicing=None):
        self.text = text
        self.time_signature = (4, 4)
        self.prev_time_signature = (4, 4)
        self.elements = []
        self.first_change_time_signature = True
        self.bar_elements = {}
        self.allow_multi_signature = True
        ## PARAMETERS
        self.rhythm = {}
        self.counterpoint = []
        self.voice_leading = []
        self.chord_idx_voice_leading = 0
        self.chord_idx_counterpoint = 0
        self.key = 0
        self.init_offset_bar = 0
        self.mode = 'M'
        self.instruments = DEFAULT_INSTRUMENTS if instruments is None else instruments
        self.init_bar_number = -1
        self.current_score = DEFAULT_VOICING if voicing is None else voicing
        self.bar_number = 0
        self.chord_number = 0
        self.current_beat = 0
        self.pickup = 0
        self.chord_started_time = (0, 0)  # Bar idx, beat idx
        ## Init elements
        self.init()

    @classmethod
    def convert_harmony_with_relative_tones(cls, text):
        """
        Convert roman numeral harmony to roman numeral with only one tonality at the beginning
        Parameters
        ----------
        text

        Returns
        -------

        """



    def add_chord(self, chord, score):
        if score is not None:
            # Deduce how much last chord should lasts
            bar_start, beat_start = self.chord_started_time
            duration = self.prev_duration * (self.bar_number - bar_start) + (self.current_beat - beat_start)
            if duration == 0:
                score.chords = score.chords[:-1]
            else:
                score.chords[-1] = score.chords[-1].set_duration(duration)
                assert score.chords[-1].duration == duration
        # Create new chord started time
        self.chord_started_time = (self.bar_number, self.current_beat)
        if score is None and self.current_beat > 0:
            self.pickup = self.current_beat
        score += chord
        return score

    def set_voice_leading(self, voice_leading):
        if len(self.voice_leading) > 0:
            self.voice_leading[-1][1] = self.chord_number
        self.voice_leading = self.voice_leading + [[self.chord_number, None, voice_leading]]

    def set_counterpoint(self, fixed_voices):
        if len(self.counterpoint) > 0:
            self.counterpoint[-1][1] = self.chord_number
        self.counterpoint = self.counterpoint + [[self.chord_number, None, fixed_voices]]

    def set_rhythm(self, instrument, nb_bars, rhythm):
        from musiclang import Metric
        metric = (rhythm, nb_bars)
        if instrument in self.rhythm.keys():
            self.rhythm[instrument][-1][1] = self.chord_number
        self.rhythm[instrument] = self.rhythm.get(instrument, []) + [[self.chord_number, None, metric]]

    def set_time_signature(self, time_signature):
        if self.time_signature is not None:
            if not self.allow_multi_signature:
                raise Exception('Cannot handle multi signature scores with "allow_multi_signature" flag to false')
            self.prev_time_signature = tuple(self.time_signature)
        else:
            self.prev_time_signature = time_signature

        if self.first_change_time_signature:
            self.first_change_time_signature = False
            self.prev_time_signature = time_signature

        self.time_signature = time_signature

    def set_bar_number(self, idx):
        assert (idx > self.bar_number) or (self.bar_number == 0)

        self.bar_number = idx
        self.current_beat = 0

    def set_current_beat(self, beat):
        if beat <= self.current_beat:
            pass
        else:
            self.current_beat = beat

    def __iter__(self):
        for element in self.elements:
            yield element

    @property
    def duration(self):
        if self.time_signature is None:
            return 4
        return 4 * self.time_signature[0] / self.time_signature[1]

    @property
    def prev_duration(self):
        if self.prev_time_signature is None:
            return frac(4 * self.time_signature[0] / self.time_signature[1]).limit_denominator(8)
        return frac(4 * self.prev_time_signature[0] / self.prev_time_signature[1]).limit_denominator(8)


    @property
    def base(self):
        return 4 / self.time_signature[1]

    def is_time_signature(self, line):
        return line.startswith('Time') or line.startswith('time')

    def is_tonality(self, line):
        return line.lower().startswith('tonality') or line.lower().startswith('key')
    def is_event(self, line):
        return line.startswith('!')

    def is_bar(self, line):
        return line.startswith('m')

    def is_multibar(self, line):
        first_word = line.split(' ')[0]
        return line.startswith('m') and (('-' in first_word) or ('=' in line))

    def apply_voice_leading(self, score):
        # Normalize score
        for start, end, voice_leading in self.voice_leading:
            score[start: end] = voice_leading(score[start: end].normalize_instruments())
        return score

    def apply_counterpoint(self, score):
        from musiclang import Melody
        # Normalize score
        score = score.normalize_instruments()
        for start, end, fixed_voices in self.counterpoint:
            # Find first notes of each ...
            # Apply counterpoint
            from musiclang.transform.library import create_counterpoint_on_score
            counterpoint_score = score[start:end].copy()
            if len(fixed_voices) == 0:
                # Add a fake bass
                for chord in counterpoint_score.chords:
                    chord.score['temp_bass__0'] = b0.o(-2).augment(chord.duration)
                fixed_voices = ['temp_bass__0']
            counterpoint_score = counterpoint_score.to_standard_note()
            counterpoint_score = create_counterpoint_on_score(counterpoint_score, fixed_parts=fixed_voices)
            # Remove fake bass
            # Reapply first notes of each chord to keep harmonic content ok
            for idx, chord in enumerate(counterpoint_score):
                for ins, melody in chord.score.items():
                    if ins in score[start + idx].score.keys():
                        score[start + idx].score[ins] = score[start + idx].score[ins].notes[0] + Melody([n for n in melody.notes[1:]])

        return score

    def apply_rhythm(self, score):
        from musiclang import ScoreRhythm
        from musiclang import Metric
        for key, rhythm_array in self.rhythm.items():
            for start_idx, end_idx, metric_data in rhythm_array:
                rhythm, nb_bars = metric_data
                metric = Metric.FromArray(rhythm, signature=self.time_signature, nb_bars=nb_bars)
                score[start_idx:end_idx] = ScoreRhythm(rhythm_dict={key: metric})(score[start_idx: end_idx])
        return score

    def parse(self, allow_multi_signature=True, tonality=None):
        """
        Parse the chord progression into music lang using voice leading
        """

        if tonality is not None:
            for idx, el in enumerate(self.elements):
                if isinstance(el, TonalityLine):
                    self.elements[idx] = TonalityLine("Tonality :" + tonality)

        self.allow_multi_signature = allow_multi_signature
        interpreter = ScoreInterpreter(self)
        score = interpreter.parse()
        if self.voice_leading is not None:
            score = self.apply_voice_leading(score)
        if self.rhythm:
            # Apply proper rhythm to each section
            score = self.apply_rhythm(score)
        if self.counterpoint is not None:
            # Apply counterpoint to notes starting from second if voice leading
            score = self.apply_counterpoint(score)
        score.config['pickup'] = self.pickup
        score.config['time_signature'] = self.time_signature
        score.config['annotation'] = self.text
        return score

    @classmethod
    def init_object(cls, elements):
        return cls(''.join([e.to_text() for e in elements]))

    @classmethod
    def get_score(cls, elements):
        return cls.init_object(elements).parse()

    def init(self):
        lines = self.text.split('\n')
        for line in lines:
            line = line.lstrip('\t').lstrip(' ')
            if self.is_time_signature(line):
                self.elements.append(TimeSignature(line))
            elif self.is_tonality(line):
                self.elements.append(TonalityLine(line))
            elif self.is_event(line):
                self.elements.append(Event(line, self))
            elif self.is_multibar(line):
                multibar = MultiBar(line)
                new_range = multibar.receiver_range
                old_range = multibar.emitter_range
                # Copy proper elements
                for idx, old_idx in zip(range(*new_range), range(*old_range)):
                    self.elements.append(BarLine(f"m{idx}", self))
                    self.elements += self.bar_elements[old_idx]
                    self.bar_elements[idx] = self.bar_elements[old_idx]
                    self.chord_number += len([e for e in self.bar_elements[idx] if isinstance(e, BarChord)])
            elif self.is_bar(line):
                bar = BarLine(line, self)
                elements = bar.get_elements()
                if self.init_bar_number > bar.idx:
                    continue
                    #raise Exception('Invalid bar number, should be higher than current')
                elif self.init_bar_number != bar.idx:  # Get only first variation of a bar
                    self.elements.append(bar)
                    self.elements += elements
                    self.init_bar_number = bar.idx
                    self.bar_elements[bar.idx] = elements
                    self.chord_number += len([e for e in elements if isinstance(e, BarChord)])

    def __repr__(self):
        return f"ScoreFormatter({self.elements})"

class ScoreInterpreter:

    def __init__(self, sf):
        self.sf = sf

    def parse(self):
        score = None
        for event in self.sf:
            score = event.parse(score, self.sf)

        return score
