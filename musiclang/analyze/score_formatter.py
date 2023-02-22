from musiclang.analyze.roman_parser import analyze_one_chord
from musiclang.library import *

import re
"""
The roman numeral parsed language is an extension of this paper : 
https://archives.ismir.net/ismir2019/paper/000012.pdf

By Dmitri Tymoczko Mark Gotham Michael Scott Cuthbert and Christopher Ariza

"""
class ScoreFormatter:

    def __init__(self, text):
        self.text = text
        self.time_signature = (4, 4)
        self.prev_time_signature = (4, 4)
        self.elements = []

        self.bar_elements = {}

        ## PARAMETERS
        self.rhythm = {}
        self.counterpoint = None
        self.voice_leading = None
        self.key = 0
        self.mode = 'M'
        self.instruments = ['piano__0', 'piano__1', 'piano__2', 'piano__3']
        self.init_bar_idx = -1
        self.current_score = (b0, b1, b2, b3)
        self.bar_number = 0
        self.chord_number = 0
        self.current_beat = 0
        self.chord_started_time = (0, 0)  # Bar idx, beat idx
        ## Init elements
        self.init()

    def add_chord(self, chord, score):
        if score is not None:
            # Deduce how much last chord should lasts
            bar_start, beat_start = self.chord_started_time
            duration = self.prev_duration * (self.bar_number - bar_start) + (self.current_beat - beat_start)
            score.chords[-1] = score.chords[-1].set_duration(duration)
        # Create new chord started time
        self.chord_started_time = (self.bar_number, self.current_beat)
        score += chord
        return score

    def set_rhythm(self, instrument, nb_bars, rhythm):
        from musiclang import Metric
        metric = Metric.FromArray(rhythm, signature=self.time_signature, nb_bars=nb_bars)
        if instrument in self.rhythm.keys():
            self.rhythm[instrument][-1][1] = self.chord_number
        self.rhythm[instrument] = self.rhythm.get(instrument, []) + [[self.chord_number, None, metric]]

    def set_time_signature(self, time_signature):
        self.prev_time_signature = tuple(self.time_signature)
        self.time_signature = time_signature

    def set_bar_number(self, idx):
        assert (idx > self.bar_number) or (self.bar_number == 0)
        self.bar_number = idx
        self.current_beat = 0

    def set_current_beat(self, beat):
        self.current_beat = beat

    def __iter__(self):
        for element in self.elements:
            yield element

    @property
    def duration(self):
        return 4 * self.time_signature[0] / self.time_signature[1]

    @property
    def prev_duration(self):
        return 4 * self.prev_time_signature[0] / self.prev_time_signature[1]


    @property
    def base(self):
        return 4 / self.time_signature[1]

    def is_time_signature(self, line):
        return line.startswith('Time') or line.startswith('time')

    def is_event(self, line):
        return line.startswith('!')

    def is_bar(self, line):
        return line.startswith('m')

    def is_multibar(self, line):
        first_word = line.split(' ')[0]
        return line.startswith('m') and (('-' in first_word) or ('=' in line))

    def apply_counterpoint(self, score):
        from musiclang import Melody
        # Normalize score
        score = score.normalize_instruments()
        # Find first notes of each ...
        # Apply counterpoint
        from musiclang.transform.library import create_counterpoint_on_score
        counterpoint_score = create_counterpoint_on_score(score.to_standard_note())

        # Reapply first notes of each chord to keep harmonic content ok
        for idx, chord in enumerate(counterpoint_score):
            for ins, melody in chord.score.items():
                score[idx].score[ins] = score[idx].score[ins].notes[0] + Melody([n for n in melody.notes[1:]])

        return score

    def apply_rhythm(self, score):
        from musiclang import ScoreRhythm
        for key, rhythm_array in self.rhythm.items():
            for start_idx, end_idx, metric in rhythm_array:
                print(start_idx, end_idx, score[start_idx: end_idx])
                score[start_idx:end_idx] = ScoreRhythm(rhythm_dict={key: metric})(score[start_idx: end_idx])
        return score

    def parse(self):
        """
        Parse the chord progression into music lang using voice leading
        """
        interpreter = ScoreInterpreter(self)
        score = interpreter.parse()
        if self.voice_leading is not None:
            score = self.voice_leading(score)
        if self.rhythm:
            # Apply proper rhythm to each section
            score = self.apply_rhythm(score)
        if self.counterpoint:
            # Apply counterpoint to notes starting from second if voice leading
            score = self.apply_counterpoint(score)

        return score

    def init(self):
        lines = self.text.split('\n')
        for line in lines:
            print(line, self.chord_number, self.rhythm)
            line = line.lstrip('\t').lstrip(' ')
            if self.is_time_signature(line):
                self.elements.append(TimeSignature(line))
            elif self.is_event(line):
                self.elements.append(Event(line, self))
            elif self.is_multibar(line):
                multibar = MultiBar(line)
                new_range = multibar.receiver_range
                old_range = multibar.emitter_range
                # Copy proper elements
                for idx, old_idx in zip(range(*new_range), range(*old_range)):
                    self.elements.append(Bar(f"m{idx}"))
                    self.elements += self.bar_elements[old_idx]
                    self.bar_elements[idx] = self.bar_elements[old_idx]
                    self.chord_number += len([e for e in self.bar_elements[idx] if isinstance(e, BarChord)])

            elif self.is_bar(line):
                bar = Bar(line)
                elements = bar.get_elements()
                if self.init_bar_idx != bar.idx:  # Get only first variation of a bar
                    self.elements.append(bar)
                    self.elements += elements
                    self.init_bar_idx = bar.idx
                    self.bar_elements[bar.idx] = elements
                    self.chord_number += len([e for e in elements if isinstance(e, BarChord)])
                elif self.init_bar_idx > bar.idx:
                    raise Exception('Invalid bar number, should be higher than current')

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


class Bar:
    def __init__(self, text):
        self.text = text
        self.idx = 0
        self.init()

    def is_chord(self, element):
        return not self.is_beat(element)

    def is_beat(self, element):
        return element.startswith('b') and element[1].isdigit()

    def is_tonality(self, element):
        return ':' in element

    def init(self):
        # Get bar idx, ignoring var
        bar_number = self.text.split(' ')[0].split('var')[0]
        self.idx = int(bar_number[1:])

    def get_elements(self):
        array = self.text.split(' ')
        elements = []
        for element in array[1:]:
            if self.is_beat(element):
                elements.append(Beat(element))
            elif self.is_tonality(element):
                elements.append(CurrentTonality(element))
            elif self.is_chord(element):
                elements.append(BarChord(element))
        return elements

    def parse(self, score, parent):
        parent.set_bar_number(self.idx)
        return score

    def __repr__(self):
        return f"Bar({self.idx})"


class CurrentTonality:

    def __init__(self, text):
        self.text = text
        self.key = 0
        self.mode = 'M'
        self.init()

    def init(self):
        tab = 'CDEFGAB'
        notes = [0, 2, 4, 5, 7, 9, 11]
        note = self.text.replace(':', '').replace('#', '').replace('b', '').replace('-', '')
        tone = notes[tab.index(note.upper())]
        mode = 'major' if note.upper() == note else 'minor'

        tone += self.text.count('#')
        tone -= self.text.count('b')
        tone -= self.text.count('-')

        self.key = tone
        self.mode = mode

    def parse(self, score, parent):
        parent.key = self.key
        parent.mode = self.mode
        return score

    def __repr__(self):
        return f"CurrentTonality({self.key}, {self.mode})"


class MultiBar:
    def __init__(self, text):
        self.text = text
        self.receiver_range = None
        self.emitter_range = None
        self.init()

    def is_chord(self, element):
        pass

    def is_beat(self, element):
        pass

    def init(self):
        new, old = self.text.replace(' ', '').split('=')
        res = new[1:].split('-')
        if len(res) == 1:
            a = res[0]
            b = a
        else:
            a, b = res

        a, b = int(a), int(b) + 1
        self.receiver_range = a, b

        res = old[1:].split('-')
        if len(res) == 1:
            c = res[0]
            d = c
        else:
            c, d = res
        c, d = int(c), int(d) + 1
        self.emitter_range = c, d
        if d - c != b - a:
            raise Exception(f'Range of bars must be equals for: {self.text}')

    def parse(self, score, parent):
        return score

    def __repr__(self):
        return f"MultiBar({self.text})"


class Event:

    def __new__(cls, text, parent):
        return cls.init(text, parent)

    @classmethod
    def is_generate(cls, text):
        return text.replace(' ', '').startswith('!generate')

    @classmethod
    def is_voicing(cls, text):
        return text.replace(' ', '').startswith('!voicing')

    @classmethod
    def is_voice_leading(cls, text):
        return text.replace(' ', '').startswith('!voice_leading')

    @classmethod
    def is_rhythm(cls, text):
        return text.replace(' ', '').startswith('!rhythm')

    @classmethod
    def is_instruments(cls, text):
        return text.replace(' ', '').startswith('!instruments')

    @classmethod
    def is_counterpoint(cls, text):
        return text.replace(' ', '').startswith('!counterpoint')

    @classmethod
    def init(cls, text, parent):
        if cls.is_generate(text):
            return Generate(text)
        elif cls.is_voicing(text):
            return Voicing(text)
        elif cls.is_instruments(text):
            return Instruments(text)
        elif cls.is_rhythm(text):
            return Rhythm(text, parent)
        elif cls.is_voice_leading(text):
            return VoiceLeading(text)
        elif cls.is_counterpoint(text):
            return Counterpoint(text)
        else:
            raise Exception(f'Not existing event {text}')




class Counterpoint:
    def __init__(self, text):
        self.text = text
        self.init()

    def init(self):
        from musiclang.transform import VoiceLeading
        self.text = re.sub(' +', ' ', self.text)
        insts = ','.join([f"'{ins}'" for ins in self.text.replace('!voice_leading', '').lstrip(' ').split(' ')])
        insts = eval(insts)
        tracks = {}
        # Assign tracks
        fixed_voices = []
        for ins in insts:
            if '__' in ins:
                fixed_voices.append(ins)
                tracks[ins] = int(ins.split('__')[1]) + 1
            fixed_voices.append(f'{ins}__{tracks.get(ins, 0)}')
            tracks[ins] = tracks.get(ins, 0) + 1

        self.fixed_voices = fixed_voices

    def parse(self, score, parent):
        parent.counterpoint = True
        return score

    def __repr__(self):
        return f"Counterpoint({self.text})"

class VoiceLeading:
    def __init__(self, text):
        self.text = text
        self.init()

    def init(self):
        from musiclang.transform import VoiceLeading
        self.text = re.sub(' +', ' ', self.text)
        insts = ','.join([f"'{ins}'" for ins in self.text.replace('!voice_leading', '').lstrip(' ').split(' ')])
        insts = eval(insts)
        tracks = {}
        # Assign tracks
        fixed_voices = []
        for ins in insts:
            if '__' in ins:
                fixed_voices.append(ins)
                tracks[ins] = int(ins.split('__')[1]) + 1
            fixed_voices.append(f'{ins}__{tracks.get(ins, 0)}')
            tracks[ins] = tracks.get(ins, 0) + 1

        self.voice_leading = VoiceLeading(fixed_voices=fixed_voices)

    def parse(self, score, parent):
        parent.voice_leading = self.voice_leading
        return score

    def __repr__(self):
        return f"VoiceLeading({self.text})"

class Rhythm:
    """
    Apply a rhythm to a specific part
    """
    def __init__(self, text, parent):
        self.text = text
        self.init(parent)

    def init(self, parent):
        self.text = re.sub(' +', ' ', self.text)
        self.text = self.text.lstrip(' ')
        args = self.text.split(' ')
        self.instrument = f"{args[1]}"
        self.rhythm = f"{args[2]}"
        self.nb_bars = len(self.rhythm.split('|'))
        self.rhythm = [r if r in ['x', '.'] else '' for r in self.rhythm.replace('|', '')]
        self.rhythm = [1 if r == 'x' else 0 for r in self.rhythm]
        if '__' not in self.instrument:
            self.instrument = f"{self.instrument}__0"
        parent.set_rhythm(self.instrument, self.nb_bars, self.rhythm)

    def parse(self, score, parent):
        return score

    def __repr__(self):
        return f"Rhythm({self.text})"


class Instruments:
    def __init__(self, text):
        self.text = text
        self.init()

    def init(self):
        self.text = re.sub(' +', ' ', self.text)
        insts = ','.join([f"'{ins}'" for ins in self.text.replace('!instruments', '').lstrip(' ').split(' ')])
        insts = eval(insts)
        tracks = {}
        # Assign tracks
        self.instruments = []
        for ins in insts:
            self.instruments.append(f'{ins}__{tracks.get(ins, 0)}')
            tracks[ins] = tracks.get(ins, 0) + 1

    def parse(self, score, parent):
        parent.instruments = self.instruments
        return score

    def __repr__(self):
        return f"Instruments({self.text})"

class Voicing:
    def __init__(self, text):
        self.text = text
        self.init()

    def init(self):
        import re
        self.text = re.sub(' +', ' ', self.text)
        self.score = ','.join([f"{ins}" for ins in self.text.replace('!voicing', '').lstrip(' ').split(' ')])
        self.score = eval(self.score)

    def parse(self, score, parent):
        parent.current_score = self.score
        return score

    def __repr__(self):
        return f"Voicing({self.text})"

class Generate:
    def __init__(self, text):
        self.text = text

    def parse(self, score, parent):
        return score

    def __repr__(self):
        return f"Generate({self.text})"


class TimeSignature:

    def __init__(self, text):
        self.text = text
        self.num = 4
        self.den = 4

    def parse(self, score, parent):
        num, den = self.text.split(':')[1].replace(' ', '').split('/')
        parent.set_time_signature((int(num), int(den)))
        return score

    def __repr__(self):
        return f'TimeSignature({self.num}, {self.den})'


class Beat:
    def __init__(self, text):
        self.text = text
        self.value = None
        self.init()

    def init(self):
        from fractions import Fraction as frac
        self.value = self.text.replace('b', '')

    def get_real_value(self, parent):
        CONVENTION_DICT = {(6, 8): 2, (2, 2): 2}
        nb_beats = CONVENTION_DICT.get(parent.time_signature, parent.duration)
        ratio = frac(nb_beats / parent.duration).limit_denominator(8)
        real_value = frac(float(self.value)).limit_denominator(8) - 1
        real_value /= ratio
        return real_value

    def parse(self, score, parent):
        parent.set_current_beat(self.get_real_value(parent))
        return score

    def __repr__(self):
        return f'Beat({self.value})'


class BarChord:

    def __init__(self, text):
        self.text = text

    def parse(self, score, parent):
        from musiclang import Chord, Tonality
        key, mode = parent.key, parent.mode
        final_degree, extension, final_key, final_mode = analyze_one_chord(self.text, key, mode)
        chord = Chord(final_degree,
                      tonality=Tonality(final_key, final_mode))[extension]
        new_dur = parent.duration - parent.current_beat
        applied_score = {key: item for key, item in zip(parent.instruments, parent.current_score)}
        chord = chord(**applied_score).set_duration(new_dur)
        score = parent.add_chord(chord, score)
        return score

    def __repr__(self):
        return f"Chord({self.text})"


