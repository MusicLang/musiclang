"""
Copyright (c) 2023, Florian GARDIN
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""


class Score:
    """Represents a score in musiclang


    """
    def __init__(self, chords=None, config=None, tags=None):
        self.chords = chords
        self.config = config
        if self.chords is None:
            self.chords = []
        if self.config is None:
            self.config = {'annotation': "", "tempo": 120}

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
        chord: Chord
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
        chord: Chord
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
        score: Score

        """
        cp = self.copy()
        cp.tags = cp.tags.union(set(tags))
        return cp

    def add_tag_children(self, tag):
        """
        Add a tag to each chord composing the score (A score itself don't have tags)
        Returns a copy of the object
        Parameters
        ----------
        tag: str

        Returns
        -------
        chord: Chord
        """
        return Score([c.add_tag(tag) for c in self.chords], tags=self.tags)


    def add_tags_children(self, tags):
        """
        Add several tags to each chord composing the score (A score itself don't have tags)
        Returns a copy of the object

        Parameters
        ----------
        tags: List[str]
        tags to add

        Returns
        -------
        score: Score

        """
        return Score([c.add_tags(tags) for c in self.chords], tags=self.tags)

    def remove_tags_children(self, tags):
        """
        Remove several tags to each chord composing the score (A score itself don't have tags)
        Returns a copy of the object

        Parameters
        ----------
        tags: List[str]
        tags to add

        Returns
        -------
        score: Score

        """
        return Score([c.remove_tags(tags) for c in self.chords], tags=self.tags)

    def remove_tag_children(self, tag):
        """
        Remove a tag to each chord composing the score (A score itself don't have tags)
        Returns a copy of the object

        Parameters
        ----------
        tags: List[str]
        tags to add

        Returns
        -------
        score: Score

        """
        return Score([c.remove_tag(tag) for c in self.chords], tags=self.tags)

    def clear_tags_children(self):
        """
        Clear all tags to each chord composing the score (A score itself don't have tags)
        Returns a copy of the object

        Parameters
        ----------
        tags: List[str]
        tags to add

        Returns
        -------
        score: Score

        """
        return Score([c.clear_tags() for c in self.chords], tags=self.tags)

    def remove_tags(self, tags):
        """
        Remove several tags from the object.
        Returns a copy of the object

        Parameters
        ----------
        tags: List[str]

        Returns
        -------
        score: Score


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
        chord: Chord
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
        chord: Chord
        """
        cp = self.copy()
        cp.tags = set()
        return cp

    def to_chords(self):
        """ """
        res = [chord.to_chord() for chord in self.chords]
        return res

    def copy(self):
        """
        Copy the score
        """
        return Score([c.copy() for c in self.chords], config=self.config.copy(), tags=set(self.tags))

    def o(self, val):
        """
        Apply octave to the score.

        Parameters
        ----------
        val : int
            Nb octave to transpose
            

        Returns
        -------
        score: Score
            Octaved score

        """
        return Score([c.o_melody(val) for c in self], config=self.config.copy(), tags=self.tags)

    def __add__(self, other):
        """
        Add another score, or a chord to the current score
        Returns A copy of the score

        Parameters
        ----------
        other: Store or Chord

        Returns
        -------
        score: Score

        """

        from .chord import Chord
        if other is None:
            return self.copy()
        if isinstance(other, Chord):
            return Score(self.copy().chords + [other], config=self.config.copy(), tags=self.tags)
        if isinstance(other, Score):
            return Score(self.copy().chords + other.copy().chords, config=self.config.copy(), tags=self.tags.union(other.tags))
        else:
            raise Exception('Cannot add to Score if not Chord or Score')

    def __iter__(self):
        return self.chords.__iter__()

    def __and__(self, other):
        if isinstance(other, int):
            return Score([c & other for c in self.chords], tags=self.tags)
        else:
            raise Exception(f'Not compatible type with & {other.__class__}')


    @property
    def instruments(self):
        """

        Parameters
        ----------

        Returns
        -------
        type
            :return:

        """
        result = []
        for chord in self:
            insts = list(chord.score.keys())
            result += insts
            result = list(set(result))

        return list(sorted(result, key=lambda x: (x.split('__')[0], int(x.split('__')[1]))))


    def to_voicings(self, instruments=None):
        """Convert score to a four voice voicing using the extensions provided in the chord.

        It will remove the existing scores of each chord and create the associated voicings

        Parameters
        ----------
        instruments : None or List[str] (Default value = ['piano__0', 'piano__1', 'piano__2', 'piano__3'])
                      The list of instruments used to create the voicings.

        Returns
        -------

        score: Score
               The score with voicings corresponding to chords

        """
        from .library import s0, s1, s2, s3, s4, s5, s6
        extension_dict = {
            '': [s0, s2, s4, s0.o(1)],
            '5': [s0, s2, s4, s0.o(1)],
            '6': [s2, s4, s0.o(1), s2],
            '64': [s4, s0.o(1), s2.o(1), s4.o(1)],
            '7': [s0, s2, s4, s6],
            '65': [s2, s4, s6, s0.o(1)],
            '43': [s4, s6, s0.o(1), s2.o(1)],
            '2': [s6, s0.o(1), s2.o(1), s4.o(1)]
        }
        if instruments is None:
            instruments = ['piano__0', 'piano__1', 'piano__2', 'piano__3']

        score = None
        for chord in self:
            notes = extension_dict[chord.extension]
            score += chord(**{ins: notes[i].copy() for i, ins in enumerate(instruments)})

        return score

    def show(self, *args, **kwargs):
        """Wrapper to the music21 show method
        :return:

        Parameters
        ----------
        *args :
            
        **kwargs :
            

        Returns
        -------

        """
        import music21
        import tempfile
        import os
        with tempfile.TemporaryDirectory() as di:
            m21_score = self.to_music21(**kwargs)
            return m21_score.show(*args)


    def __getitem__(self, item):
        """
        If str return a score with only this voice
        else returns item getter of the list of chords and convert it back to a score
        """
        from .note import Silence
        from .chord import Chord
        if isinstance(item, str):
            new_score = None
            for chord in self:
                if item in chord.score.keys():
                    new_score += chord(**{item: chord.score[item]})
                else:
                    new_score += chord(**{item: Silence(chord.duration)})
            return new_score
        elif isinstance(item, list):
            new_score = None
            for chord in self:
                chord_score = {}
                for it in item:
                    if it in chord.score.keys():
                        chord_score[it] = chord.score[it]
                    else:
                        chord_score[it] = Silence(chord.duration)
                new_score += chord(**chord_score)

            return new_score
        else:
            chords = self.chords.__getitem__(item)
            if isinstance(chords, Chord):
                return chords
            return sum(chords, None)

    def put_on_same_chord(self):
        """Take the first chord as reference,
        Put everything into the first chord preserving the note value (It will change the piece to a static harmony)

        Parameters
        ----------
        score : Score
                Input score


        Returns
        -------
        score: Score
               Score containing one chord with all the melodies

        Examples
        --------

        >>> from musiclang.library import *
        >>> score = (I % I.m)(piano__0=s0) + (V % I.m)(piano__0=s2)
        >>> score.put_on_same_chord()
        (I % I.m)(piano__0=s0 + s2)

        """
        from .time_utils import put_on_same_chord
        return put_on_same_chord(self)

    def project_on_score(self, score2, keep_score=False):
        """Project harmonically the current score onto the score2
        Algorithm : For each chord of score2 : get chords that belongs to score1 and reproject on chord of score2

        Parameters
        ----------
        score : Score
                Score to project on the chords of score2
        score2 : Score
            Score that contains the harmony
        keep_score : Score (Default value = False)
            Keep the voices of score2 ? (Default value = False)

        Returns
        -------
        new_score: Score
                  The score projected on score2 chord progression. It will fit the minimal duration of both scores

        Examples
        --------

        >>> from musiclang.library import *
        >>> score1 = (I % I.m)(piano__0=s0.e) + (V % I.m)(piano__0=s2.e)
        >>> score2 = (II % III.m)(piano__0=s0.e + s0.e)
        >>> score1.project_on_score(score2, keep_score=False)
        (II % III.m)(piano__0=s0.e + s2.e)

        """
        # Algo : For each chord of score2 : get chords that belongs to score1 and reproject on chord of score2
        from .time_utils import project_on_score
        return project_on_score(self.to_score(), score2.to_score(), keep_score=keep_score)


    def get_chord_between(self, chord, start, end):
        """

        Parameters
        ----------
        chord :
            
        start :
            
        end :
            

        Returns
        -------

        """
        from .time_utils import get_chord_between
        return get_chord_between(chord, start, end)


    def get_score_between(self, start=None, end=None):
        """
        Get the score between start and end time.

        Parameters
        ----------
        start :
             (Default value = None)
        end :
             (Default value = None)

        Returns
        -------

        """
        from .time_utils import get_score_between
        return get_score_between(self, start, end)

    def reduce(self, n_voices=4, start_low=False, instruments=None):
        """
        Reduce the score to n_voices

        Parameters
        ----------
        n_voices : int, (Default value = 4)
                   Number of voices in the reduction
        start_low : bool (Default value = False)
                    If true the first voice in the reduction will be the bass, else the soprano
        instruments : List[str] or None (Default value = None)
                      Name of the voices in the reduction
        Returns
        -------
        score : Score
                The reduced score

        Examples
        --------

        >>> from musiclang.library import *
        >>> score = (I % I.M)(piano=[s0, s2, s4]) + (V % I.M)(piano=[s0, s2, s4])
        >>> score.reduce(n_voices=2, start_low=False, instruments=['cello__0', 'violin__0'])
        (I % I.M)(
            cello__0=s0,
            violin__0=s4)+
        (V % I.M)(
            cello__0=s0,
            violin__0=s4)

        """
        from .arrange_utils import reduce
        return reduce(self, n_voices=n_voices, start_low=start_low, instruments=instruments)

    def to_pickle(self, filepath):
        """
        Save the score into a pickle file

        Parameters
        ----------
        filepath : str
                   Filepath on which to save the score

        """
        import pickle
        with open(filepath, 'wb') as f:
            pickle.dump(self, f)

    @classmethod
    def from_midi(cls, filename):
        """
        Load a midi score into musiclang

        .. warning:: This step can take some time depending on the length of the file

        Parameters
        ----------
        filename : str
                   Filepath of the file
            

        Returns
        -------
        score: Score
               The loaded score

        """
        from musiclang.analyze import parse_to_musiclang
        score, config = parse_to_musiclang(filename)
        score.config = config
        return score

    @classmethod
    def from_xml(cls, filename):
        """
        Load a musicxml score into musiclang

        .. warning:: This step can take some time depending on the length of the file


        Parameters
        ----------
        filename : str
                   Filepath of the file
            

        Returns
        -------

        score: Score
               The loaded score

        """
        from musiclang.analyze import parse_to_musiclang
        score, config = parse_to_musiclang(filename)
        score.config = config
        return score

    def decompose_duration(self):
        """
        Decompose the duration in a note + continuations. It recursively call
        :func:`~Note.decompose_duration()`
        """
        return Score([chord.decompose_duration() for chord in self.chords], tags=self.tags)

    def to_score(self):
        """ """
        return self.copy()

    @classmethod
    def from_sequence(cls, sequence, **kwargs):
        """

        Parameters
        ----------
        sequence :
            
        **kwargs :
            

        Returns
        -------

        """
        from .sequence.sequence import sequence_to_score
        return sequence_to_score(sequence, **kwargs)

    def to_sequence(self, **kwargs):
        """
        Convert
        Parameters
        ----------
        **kwargs :
            

        Returns
        -------

        """
        from .sequence.sequence import score_to_sequence
        return score_to_sequence(self, **kwargs)


    @classmethod
    def from_pickle(cls, filepath):
        """

        Parameters
        ----------
        filepath :
            

        Returns
        -------

        """
        import pickle
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
        return data

    def __eq__(self, other):
        from .chord import Chord
        if isinstance(other, Chord):
            return self == Score([other], config=self.config.copy())
        if not isinstance(other, Score):
            return False
        elif len(other.chords) != len(self.chords):
            return False
        else:
            return all([c1 == c2 for c1, c2 in zip(self.chords, other.chords)])

    def __getattr__(self, item):
        chords = self.copy()
        chords.chords = [getattr(s, item) for s in self.chords]
        return chords

    def __mod__(self, other):
        from .tonality import Tonality
        if isinstance(other, Tonality):
            return Score([c % other for c in self.chords], config=self.config.copy(), tags=self.tags)
        else:
            raise Exception('Following % should be a Tonality')

    def remove_accidents(self):
        return Score([chord.remove_accidents() for chord in self.chords], tags=set(self.tags))


    def __mul__(self, other):
        """
        If other is Integer, repeat the note other times
        """
        if isinstance(other, int):
            return sum([self.copy() for i in range(other)], None)
        else:
            raise Exception('Cannot multiply Score and ' + str(type(other)))

    def __radd__(self, other):
        if other is None:
            return self.copy()

    def __repr__(self):
        return '+ \n'.join([str(chord) for chord in self.chords])

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__ = d


    @property
    def duration(self):
        """ """
        return sum([c.duration for c in self.chords])

    def to_code(self, **kwargs):
        """Export the chord serie as a string representing valid python code that recreates the score
        :return:

        Parameters
        ----------
        **kwargs :
            

        Returns
        -------

        """
        from .out.to_code import chord_serie_to_code

        code = chord_serie_to_code(self, **kwargs)
        return code

    def to_code_file(self, filepath, **kwargs):
        """Export the chord serie as a file representing valid python code that recreates the score

        Parameters
        ----------
        filepath :
            return:
        **kwargs :
            

        Returns
        -------

        """
        code = self.to_code(**kwargs)
        with open(filepath, 'w') as f:
            f.write(code)

    def to_musicxml(self, filepath, signature=(4, 4), tonality=None, tempo=120, **kwargs):
        """
        Transform a musiclang score into a musicxml file, readable by all the main notation software (musescore, finale ...)

        Parameters
        ----------
        score: Score
                MusicLang score to transform
        filepath: str
                Filepath of the musicxml file
        signature: tuple (nom, den)
                Time signature of the piece
        tempo: int
                Tempo of the piece
        tonality: Tonality
                Tonality of the piece if applicable
        title: str
            Title of the piece

        """
        # Convert score to midi
        from .out.to_mxl import score_to_mxl

        return score_to_mxl(self, filepath, signature=signature, tonality=tonality, tempo=tempo, **kwargs)

    def to_music21(self, signature=(4, 4), tonality=None, tempo=120, **kwargs):
        """
        Transform a musiclang score into a Music21 score
        Parameters
        ----------
        score: Score
                MusicLang score to transform
        signature: tuple (nom, den)
                Time signature of the piece
        tempo: int
                Tempo of the piece
        tonality: Tonality
                Tonality of the piece if applicable
        title: str
            Title of the piece

        Returns
        -------
        m21_score: music21.Score
            Score transformed into a music21 object

        """
        from .out.to_mxl import score_to_music_21
        return score_to_music_21(self, signature=signature, tonality=tonality, tempo=tempo, **kwargs)

    def to_midi(self, filepath, **kwargs):
        """
        Save the score to midi

        Parameters
        ----------
        filepath :
            
        **kwargs :
            

        Returns
        -------

        """
        # Convert score to midi
        from .out.to_midi import score_to_midi

        return score_to_midi(self, filepath, **kwargs)

