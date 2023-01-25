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
    def __init__(self, notes, tags=None):
        from .note import Note
        if isinstance(notes, Note):
            notes = []
        self.notes = notes
        self.tags = set(tags) if tags is not None else set()

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

    def to_melody(self):
        return self.copy()

    def remove_accidents(self):
        return Melody([n.remove_accidents() for n in self.notes], tags=set(self.tags))

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__.update(d)

    def __add__(self, other):
        from .note import Note
        if other is None:
            return self.copy()
        if isinstance(other, Note):
            return Melody(self.notes + [other], tags=set(self.tags))
        if isinstance(other, Melody):
            return Melody(self.notes + other.notes, tags=set(self.tags).union(other.tags))

    def __hash__(self):
        return hash(self.__repr__())

    def __eq__(self, other):
        from .note import Note
        if isinstance(other, Note):
            return self.__eq__(Melody([other]))
        return isinstance(other, Melody) and str(other) == str(self)

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

    def decompose_duration(self):
        """ """
        return Melody([note.decompose_duration() for note in self.notes], tags=set(self.tags))

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


    def to_code(self):
        """ """
        return " + ".join([n.to_code() for n in self.notes])

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
        return Melody([n.augment(value) for n in self.notes], tags=set(self.tags))

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
        return Melody([n & other for n in self.notes], tags=set(self.tags))

    def __matmul__(self, other):
        # Apply a function to each note
        return Melody([n @ other for n in self.notes], tags=set(self.tags))

    def __mul__(self, other):
        from .note import Note
        if isinstance(other, int):
            melody_copy = self.copy()
            return Melody(melody_copy.notes * other, tags=set(self.tags))
        if isinstance(other, Note):
            return self * Melody([other.copy()], tags=set(self.tags))
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
        return Melody([n.o(octave) for n in self.notes], tags=set(self.tags))

    def __hasattr__(self, item):
        try:
            self.__getattr__(item)
        except:
            return False
        return True

    def __getattr__(self, item):
        try:
            res = Melody([getattr(n, item) for n in self.notes], tags=set(self.tags))
            return res
        except:
            raise AttributeError(f"Not existing property : {item}")

    def copy(self):
        """ """
        return Melody([s.copy() for s in self.notes], tags=set(self.tags))

    def __repr__(self):
        return self.to_code()