"""
Copyright (c) 2023, Florian GARDIN
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""

from .constants import *

class Melody:
    """
    Main class to write a melody in MusicLang. A melody is a serie of notes

    Examples
    --------

    For example here is an example of a melody that plays the seven note of a scale :

    >>> from musiclang.write.library import *
    >>> melody =  s0 + s1 + s2 + s3 + s4 + s5 + s6
    >>> melody
    s0 + s1 + s2 + s3 + s4 + s5 + s6

    You can also create it using the melody class :

    >>> from musiclang import Melody
    >>> melody = Melody([s0, s1, s2, s3, s4, s5, s6])
    >>> melody
    s0 + s1 + s2 + s3 + s4 + s5 + s6

    """
    def __init__(self, notes, nb_bars=1, tags=None):
        from .note import Note
        if isinstance(notes, Note):
            notes = []
        self.notes = notes
        self.tags = set(tags) if tags is not None else set()
        self.nb_bars = nb_bars

    def has_tag(self, tag):
        """
        Check if the tag exists for this object
        Returns a copy of the object
        Parameters
        ----------
        tag: str

        Returns
        -------
        melody: Melody
        """
        return tag in self.tags


    def add_tag(self, tag):
        """
        Add a tag to this object
        Returns a copy of the object
        Parameters
        ----------
        tag: str

        Returns
        -------
        melody: Melody
        """
        cp = self.copy()
        cp.tags.add(tag)
        return cp

    def add_tags(self, tags):
        """
        Add several tags to the object.
        Returns a copy of the object

        Parameters
        ----------
        tags: List[str]
        tags to add

        Returns
        -------
        melody: Melody

        """
        cp = self.copy()
        cp.tags = cp.tags.union(set(tags))
        return cp

    def repeated_notes_to_legato(self):
        from musiclang import Continuation
        new_melody = []
        last_note = None
        for note in self.notes:
            if last_note is None:
                new_melody.append(note)

            if 'u' in note.type and note.val == 0 and note.octave == 0:
                new_melody.append(Continuation(note.duration))
            elif note.val == last_note.val and note.type == last_note.type and note.octave == last_note.octave:
                new_melody.append(Continuation(note.duration))
            last_note = note
        return Melody(new_melody)

    def remove_tags(self, tags):
        """
        Remove several tags from the object.
        Returns a copy of the object

        Parameters
        ----------
        tags: List[str]

        Returns
        -------
        melody: Melody


        """
        cp = self.copy()
        cp.tags = cp.tags - set(tags)
        return cp

    def remove_tag(self, tag):
        """
        Remove a tag from this object
        Returns a copy of the object
        Parameters
        ----------
        tag: str

        Returns
        -------
        melody: Melody
        """
        cp = self.copy()
        cp.tags.remove(tag)
        return cp

    def clear_tags(self):
        """
        Clear all tags from this object
        Returns a copy of the object
        Parameters
        ----------
        tag: str

        Returns
        -------
        melody: Melody
        """
        cp = self.copy()
        cp.tags = set()

        return cp

    def set_amp(self, amp):
        return Melody([n.set_amp(amp) for n in self.notes], nb_bars=self.nb_bars, tags=set(self.tags))


    def set_duration(self, duration):
        return self.augment(duration / self.duration)

    def to_drum(self):
        return Melody([n.to_drum() for n in self.notes], nb_bars=self.nb_bars, tags=set(self.tags))

    def to_melody(self):
        return self.copy()

    def remove_accidents(self):
        return Melody([n.remove_accidents() for n in self.notes], nb_bars=self.nb_bars, tags=set(self.tags))

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__.update(d)

    def __add__(self, other):
        from .note import Note
        if other is None:
            return self.copy()
        if isinstance(other, Note):
            return Melody(self.notes + [other], nb_bars=self.nb_bars, tags=set(self.tags))
        if isinstance(other, Melody):
            return Melody(self.notes + other.notes, nb_bars=self.nb_bars, tags=set(self.tags).union(other.tags))

    def __or__(self, other):
        from .note import Note
        if other is None:
            return self.copy()
        if isinstance(other, Note):
            assert other.duration == self.duration / self.nb_bars, f"Invalid duration of bar {other}: {other.duration}q, expected : {self.duration / self.nb_bars}q/bar"
            return Melody(self.notes + [other], nb_bars=self.nb_bars + 1, tags=set(self.tags))
        if isinstance(other, Melody):
            assert other.duration / other.nb_bars == self.duration / self.nb_bars, \
                f"Invalid duration of bar {other} : {other.duration}q with {other.nb_bars} bars, expected : {self.duration / self.nb_bars}q/bar"
            return Melody(self.notes + other.notes, nb_bars=self.nb_bars + other.nb_bars, tags=set(self.tags).union(other.tags))
        else:
            raise Exception(f'Invalid type when adding melody, {other.__class__}')

    def __hash__(self):
        return hash(self.__repr__())

    def __eq__(self, other):
        from .note import Note
        if isinstance(other, Note):
            return self.__eq__(Melody([other]))
        return isinstance(other, Melody) and str(other) == str(self)

    def to_absolute_note(self, chord, last_pitch=None):
        notes = []
        for note in self.notes:
            note = note.to_absolute_note(chord, last_pitch=last_pitch)
            last_pitch_temp = chord.to_pitch(note, last_pitch=last_pitch)
            if last_pitch_temp is not None:
                last_pitch = last_pitch_temp
            notes.append(note)

        return Melody(notes, nb_bars=self.nb_bars, tags=set(self.tags))


    def get_between(self, start, end):
        """
        Get the notes between start and end time
        Parameters
        ----------
        start: int
        end: int

        Returns
        -------
        melody: Melody
        """
        from musiclang.write.time_utils import get_melody_between
        return get_melody_between(self, start, end)
    def get_pitches(self, chord, track_idx, time, last_note_array=None):
        """

        Parameters
        ----------
        chord :
            
        track_idx :
            
        time :
            
        last_note_array :
             (Default value = None)

        Returns
        -------

        """
        pitches = []
        for note in self.notes:
            result = note.pitch(chord, track_idx, time, last_note_array)
            if not last_note_array[SILENCE] and not last_note_array[CONTINUATION]:
                last_note_array = result

            pitches.append(result)
        return pitches

    def apply_pattern(self, *voicing):
        """
        Replace pattern notes by voicing

        Examples
        ---------

        >>> melody = x0.h + x1.h
        >>> melody.apply_pattern(s1, s0)
        s1.h + s0.h

        Parameters
        ----------
        voicing: List[Note] : Voicing used to replace in the template

        Returns
        -------
        melody: Patternized melody
        """
        new_melody =[]
        for note in self.notes:
            if note.type == "x":
                try:
                    new_melody.append(voicing[note.val].set_duration(note.duration).o(note.octave).set_amp(note.amp))
                except:
                    raise ValueError(f'Unexisting voicing index : {note.val}')
            else:
                new_melody.append(note)

        return Melody(new_melody)


    def to_scale_notes(self, chord):
        return Melody([n.to_scale_note(chord) for n in self.notes], nb_bars=self.nb_bars, tags=set(self.tags))

    def decompose_duration(self):
        """ """
        return Melody(sum([note.decompose_duration() for note in self.notes], None).notes, nb_bars=self.nb_bars, tags=set(self.tags))

    def replace_pitch(self, to_replace, new_note):
        """

        Parameters
        ----------
        to_replace :
            
        new_note :
            

        Returns
        -------

        """

        new_melody = []
        for note in self.notes:
            to_add = note.copy()
            if note.val == to_replace.val and note.type == to_replace.type:
                to_add.type = new_note.type
                to_add.val = new_note.val
            new_melody.append(to_add)
        return sum(new_melody, None)

    def replace(self, to_replace, new_note, **kwargs):
        """

        Parameters
        ----------
        to_replace :

        new_note :


        Returns
        -------

        """

        return Melody([n.replace(to_replace, new_note, **kwargs) for n in self.notes],
                      nb_bars=self.nb_bars, tags=set(self.tags))

    def set_tempo(self, tempo):
        new_melody = self.copy()
        new_melody.notes[0] = new_melody.notes[0].set_tempo(tempo)
        return new_melody


    def project_on_rhythm(self, rhythm, chord=None, **kwargs):
        from musiclang.transform.composing import project_on_rhythm
        return project_on_rhythm(rhythm, self, chord=chord)

    def accelerando(self, start, end):
        """
        Accelerate or decelerate melody from start tempo to end tempo
        Parameters
        ----------
        start: int
            Starting tempo
        end: int
            Ending tempo

        """
        new_melody = self.copy()
        L = len(new_melody)
        for i in range(len(new_melody)):
            local_tempo = int(end * (i / L) + start * ((L - i)/L))
            new_melody.notes[i] = new_melody.notes[i].set_tempo(local_tempo)
        return new_melody

    def realize_tags(self, last_note=None, final_note=None):
        new_melody = None
        for idx, note in enumerate(self.notes):
            last_note = self.notes[idx - 1] if idx - 1 >= 0 else last_note
            next_note = self.notes[idx + 1] if idx + 1 < len(self.notes) else None
            if idx == len(self.notes) - 1:
                next_note = final_note
            new_melody += note.realize_tags(last_note=last_note, next_note=next_note)

        new_melody.nb_bars = self.nb_bars
        new_melody.tags = self.tags
        return new_melody

    @property
    def pedal_on(self):
        new_melody = self.copy()
        new_melody.notes[0] = new_melody.notes[0].pedal_on
        return new_melody

    @property
    def pedal(self):
        """
        Apply pedal on first note and release on last
        """
        new_melody = self.copy()
        new_melody.notes[0] = new_melody.notes[0].pedal_on
        new_melody.notes[-1] = new_melody.notes[-1].pedal_off
        return new_melody

    @property
    def pedal_off(self):
        new_melody = self.copy()
        new_melody.notes[0] = new_melody.notes[0].pedal_off
        return new_melody


    def remove_effects(self):
        """
        Remove pedals and tempo change
        Returns
        -------
        """
        return Melody([n.remove_effects() for n in self.notes], nb_bars=self.nb_bars, tags=set(self.tags))

    def remove_tempo(self):
        """
        Remove pedals and tempo change
        Returns
        -------
        """
        return Melody([n.remove_tempo() for n in self.notes], nb_bars=self.nb_bars, tags=set(self.tags))

    def remove_pedal(self):
        """
        Remove pedals and tempo change
        Returns
        -------
        """
        return Melody([n.remove_pedal() for n in self.notes], nb_bars=self.nb_bars, tags=set(self.tags))


    def to_sequence(self, chord, inst):
        """Transform in a list of [(start_time, end_time, pitch, self)]
        :return:

        Parameters
        ----------
        chord :
            
        inst :
            

        Returns
        -------

        """
        time = 0
        sequence = []
        for note in self.notes:
            pitch = chord.to_pitch(note)
            start = time
            end = time + note.duration
            sequence.append([start, end, pitch, chord.to_chord(), inst, note])
            time += note.duration
        return sequence


    def to_standard_note(self, chord):
        return Melody([n.to_standard_note(chord) for n in self.notes], nb_bars=self.nb_bars, tags=set(self.tags))

    def clear_note_tags(self):
        return sum([n.clear_note_tags() for n in self.notes], None)

    def to_extension_note(self, chord):
        return Melody([n.to_extension_note(chord) for n in self.notes], nb_bars=self.nb_bars, tags=set(self.tags))

    def to_chord_note(self, chord):
        return Melody([n.to_chord_note(chord) for n in self.notes], nb_bars=self.nb_bars, tags=set(self.tags))


    def get_note_times(self):
        t = 0
        times = []
        for n in self.notes:
            if n.is_note or n.type in ["x", "d"]:
                times.append(t)
            t += n.duration
        return times

    def get_onset_times(self):
        t = 0
        times = []
        for n in self.notes:
            times.append(t)
            t += n.duration
        return times

    def get_offset_times(self):
        t = 0
        times = []
        for n in self.notes:
            t += n.duration
            times.append(t)
        return times


    def get_playing_style(self):
        """
        Get if legato, marcato or staccato by  only looking at the note durations
        Returns
        -------

        """

    def get_rhythm_notes(self, rhythm, tatum, chord=None):

        time = 0
        notes = []
        for r in rhythm:
            sub_melody = self.get_between(time, time + tatum)
            note = sub_melody.notes[0]
            note = note.set_duration(1)
            if chord is not None:
                note = chord.to_pitch(note)
            notes.append(note)
            time += tatum

        return notes

    def quantize_melody(self, max_frac=4, chord=None, include_grid=False, notes=None):
        import math

        def lcm(a, b):
            return (a * b) // math.gcd(a, b)

        def duration_to_ts(duration):
            if float(duration) % 1 == 0:
                return int(duration), 4
            elif float(duration) % 0.5 == 0:
                return int(duration * 2), 8
            elif float(duration) % 0.25 == 0:
                return int(duration * 4), 16
            else:
                return int(duration * 8), 32

        times = self.get_note_times()  # Fractions
        # Find common denominator between times
        common_denominator = 1
        for t in times:
            common_denominator = lcm(common_denominator, t.denominator)

        common_denominator = min(max_frac, common_denominator)
        step = frac(1, common_denominator)

        nb_steps = self.duration / step

        # Projects each note time (times) on the grid
        new_times = [round(t / step) * step for t in times]

        # Get index on the grid
        new_times = [int(t / step) for t in new_times]

        # As binary vector
        if notes is None:
            rhythm = [1 if i in new_times else 0 for i in range(int(nb_steps))]
        else:
            rhythm = [[1 if i in new_times else 0 for i in range(int(nb_steps))]]
        tatum = step
        data = {'rhythm': rhythm,
                'tatum': (step.numerator, step.denominator),
                'time_signature': duration_to_ts(self.duration),
                "notes": notes
                }
        if include_grid:
            notes = self.get_rhythm_notes(rhythm, tatum, chord=chord)
            data['grid'] = notes
        return data




    def to_code(self):
        """ """
        return " + ".join([n.to_code() for n in self.notes])

    def convert_to_drum_note(self, chord):
        return Melody([n.convert_to_drum_note(chord) for n in self.notes], nb_bars=self.nb_bars, tags=set(self.tags))

    @property
    def is_continuation(self):
        """ """
        return all([n.is_continuation for n in self.notes])

    @property
    def starts_with_absolute_note(self):
        """ """
        if len(self.notes) > 0:
            return self.notes[0].starts_with_absolute_note
        else:
            return False

    @property
    def had_absolute_note(self):
        """ """
        return any([n.starts_with_absolute_note for n in self.notes])

    @property
    def starts_with_absolute_or_silence(self):
        """ """
        if len(self.notes) > 0:
            return self.notes[0].starts_with_absolute_or_silence
        else:
            return False

    @property
    def starts_with_note(self):
        """ """
        if len(self.notes) > 0:
            return self.notes[0].starts_with_note
        else:
            return False

    def augment(self, value):
        """

        Parameters
        ----------
        value :
            

        Returns
        -------

        """
        return Melody([n.augment(value) for n in self.notes], nb_bars=self.nb_bars, tags=set(self.tags))

    @property
    def duration(self):
        """ """
        return sum([n.duration for n in self.notes])

    def __iter__(self):
        return self.notes.__iter__()

    def __getitem__(self, item):
        return Melody(self.notes[item])

    def __radd__(self, other):
        if other is None:
            return self.copy()

    def __and__(self, other):
        return Melody([n & other for n in self.notes], nb_bars=self.nb_bars, tags=set(self.tags))

    def __matmul__(self, other):
        # Apply a function to each note
        return Melody([n @ other for n in self.notes], nb_bars=self.nb_bars, tags=set(self.tags))

    def __mul__(self, other):
        from .note import Note
        if isinstance(other, int):
            melody_copy = self.copy()
            return Melody(melody_copy.notes * other, nb_bars=self.nb_bars, tags=set(self.tags))
        if isinstance(other, Note):
            return self * Melody([other.copy()], nb_bars=self.nb_bars, tags=set(self.tags))
        else:
            raise Exception('Cannot multiply Melody and ' + str(type(other)))

    def __len__(self):
        return len(self.notes)

    def o(self, octave):
        """

        Parameters
        ----------
        octave :
            

        Returns
        -------

        """
        return Melody([n.o(octave) for n in self.notes], nb_bars=self.nb_bars, tags=set(self.tags))

    def __hasattr__(self, item):
        try:
            self.__getattr__(item)
        except:
            return False
        return True

    def __getattr__(self, item):
        try:
            res = Melody([getattr(n, item) for n in self.notes], nb_bars=self.nb_bars, tags=set(self.tags))
            return res
        except:
            raise AttributeError(f"Not existing property : {item}")

    def copy(self):
        """ """
        return Melody([s.copy() for s in self.notes], tags=set(self.tags), nb_bars=self.nb_bars)

    def __repr__(self):
        return self.to_code()

    def to_grid(self, pitches, octave=0, max_frac=4):
        import numpy as np
        # IN melody.py
        import math
        from musiclang.library import NC, r

        def lcm(a, b):
            return (a * b) // math.gcd(a, b)

        def duration_to_ts(duration):
            if float(duration) % 1 == 0:
                return int(duration), 4
            elif float(duration) % 0.5 == 0:
                return int(duration * 2), 8
            elif float(duration) % 0.25 == 0:
                return int(duration * 4), 16
            else:
                return int(duration * 8), 32

        times = self.get_note_times()  # Fractions
        # Find common denominator between times
        common_denominator = 1
        for t in times:
            common_denominator = lcm(common_denominator, t.denominator)

        common_denominator = min(max_frac, common_denominator)
        step = frac(1, common_denominator)

        nb_steps = self.duration / step

        # Projects each note time (times) on the grid
        new_times = [round(t / step) * step for t in times]

        # Get index on the grid
        new_times = [int(t / step) for t in new_times]

        # Get rhythm notes
        rhythm = [1 if i in new_times else 0 for i in range(int(nb_steps))]
        tatum = step
        notes = self.get_rhythm_notes(rhythm, tatum)

        mean_amp = np.mean([n.amp for n in notes if n.is_note])
        if mean_amp is None or mean_amp != mean_amp:
            mean_amp = 60
        mean_amp_figure = r.set_amp(mean_amp).amp_figure
        notes_pitches = [NC.to_pitch(n) for n in notes]
        mean_articulation = 'legato' if self.silence_fraction() < 0.5 else 'staccato'
        notes_pitches_index = [pitches.index(n - 12 * octave) if (n is not None and (n - 12 * octave) in pitches) else None for n in notes_pitches]
        rhythm = np.zeros((len(pitches), int(nb_steps)), dtype=int)
        for idx, note_index in enumerate(notes_pitches_index):
            if note_index is not None:
                rhythm[note_index ][idx] = 1


        rhythm = rhythm.tolist()

        return {'rhythm': rhythm,
                'tatum': (step.numerator, step.denominator),
                'time_signature': duration_to_ts(self.duration),
                'notes': pitches,
                'octave': octave,
                'amp': mean_amp_figure,
                'mode': mean_articulation
                }


    def silence_fraction(self):

        silence_duration = sum([n.duration for n in self.notes if n.is_silence])
        return silence_duration / self.duration

    @classmethod
    def from_grid(cls, data, time_signature):
        # rhythm, notes, tatum, time_signature, chord
        import numpy as np
        from musiclang import Silence, Continuation, Note
        grid = np.asarray(data['rhythm']).T

        assert grid.shape[1] == len(data['notes']), "Grid and notes must have the same length"
        tatum = frac(*data['tatum'])
        notes = data['notes']
        mode = data['mode']
        amp = data['amp']
        octave = data['octave']
        ts = time_signature
        bar_duration = 4 * ts[0] / ts[1]
        melody = []

        time = 0
        for timestep in grid:
            for idx, cell in enumerate(timestep):
                if cell:
                    note = notes[idx]
                    note = Note("a", note % 12, note //12, tatum)
                    note = note.set_amp(amp).oabs(octave)
                    melody.append(note)
                    break
            else:
                if mode == 'legato' and not time % bar_duration == 0: # Not a beginning of a bar
                    melody.append(Continuation(tatum))
                else:
                    melody.append(Silence(tatum))

            time += tatum


        return Melody(melody)



