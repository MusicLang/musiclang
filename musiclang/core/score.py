from .constants import *


class Score:
    def __init__(self, chords=None):
        self.chords = chords
        if self.chords is None:
            self.chords = []

    def to_chords(self):
        res = [chord.to_chord() for chord in self.chords]
        return res

    def copy(self):
        return Score([c.copy() for c in self.chords])

    def __add__(self, other):
        from .chord import Chord
        if isinstance(other, Chord):
            return Score(self.copy().chords + [other])
        if isinstance(other, Score):
            return Score(self.copy().chords + other.copy().chords)
        else:
            raise Exception('Cannot add to Score if not Chord or Score')

    def __iter__(self):
        return self.chords.__iter__()

    @property
    def instruments(self):
        """
        Return the list of all voices used in the score
        :return:
        """
        result = []
        for chord in self:
            insts = list(chord.score.keys())
            result += insts
            result = list(set(result))

        return list(sorted(result, key=lambda x: (x.split('__')[0], int(x.split('__')[1]))))


    def __getitem__(self, item):
        """
        If str return a score with only this voice
        Else returns item getter of the list of chords and convert it back to a score
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
        """
        Take the first chord as reference,
        Put everything into this chord (It will of course change the harmony)
        :return:
        """
        from musiclang import Silence
        first_chord = self[0]
        instruments = self.instruments
        score = {ins: None for ins in instruments}

        for chord in self.chords:
            duration = chord.duration
            for instrument in instruments:
                score[instrument] += chord.score.get(instrument, Silence(duration))

        return first_chord(**score)

    def project_on_score(self, score2, keep_score=False):
        """
        Project harmonically the score onto the score2
        :param score2: Score that contains the harmony
        :param keep_score: Keep the voice of score2 ?
        :return:
        """
        # Algo : For each chord of score2 : get chords that belongs to score1 and reproject on chord of score2

        start_time = 0
        new_score = None
        #
        instruments1 = [(ins.split('__')[0], int(ins.split('__')[1])) for ins in self.instruments]
        instruments2 = [(ins.split('__')[0], int(ins.split('__')[1])) for ins in score2.instruments]
        # Rename all instruments to avoid collisions
        offsets1 = {}
        for ins in instruments1:
            pass

        for idx, chord2 in enumerate(score2):
            # Get all segments of chord
            end_time = start_time + chord2.duration

            subscore1 = self.get_score_between(start_time, end_time)
            if subscore1 is None:
                break

            subscore = subscore1.put_on_same_chord()
            assert subscore.duration == chord2.duration, "Wrong duration when projecting"


            if keep_score:
                chord_score = chord2.score
                chord_score.update(subscore.score)
            else:
                chord_score = subscore.score
            new_score += chord2(**chord_score)

            start_time = end_time

        return new_score



    def get_chord_between(self, chord, start, end):
        new_parts = {ins: None for ins in chord.instruments}
        for part in chord.score.keys():
            time = 0
            voice = chord.score[part]
            new_voice = None
            to_break = False
            for note in voice:
                add_continuation = False
                note_duration = note.duration
                new_note = note.copy()
                if time >= end:
                    break
                if (time < start) and (time + note_duration <= start):
                    time += new_note.duration
                    continue
                if time + note_duration >= end:
                    new_note.duration = end - time
                    to_break = True
                if time < start:
                    new_note.duration = new_note.duration - (start - time)
                    time += start - time
                    add_continuation = True

                if add_continuation:
                    from .note import Continuation
                    new_voice += Continuation(new_note.duration)
                else:
                    new_voice += new_note


                if new_note.duration < 0:
                    raise Exception('Get a negative duration in get_chord_between')
                if new_voice.duration > end - start:
                    raise Exception('New voice duration should never be more than boundaries')

                time += new_note.duration

                if to_break:
                    break

            new_parts[part] = new_voice

        if len(new_parts.keys()) == 0:
            from .note import Silence
            return chord(**{'piano__0': Silence(end - start)})
            #if new_voice.duration != chord.duration:
            #    from pdb import set_trace; set_trace()
        return chord(**new_parts)

    def get_score_between(self, start=None, end=None):
        start = start if start is not None else 0
        end = end if end is not None else self.duration
        new_score = None
        time = 0
        for chord in self.chords:
            chord_start = time
            chord_end = time + chord.duration
            if chord_end <= start:
                time += chord.duration
                continue
            elif chord_start >= end:
                # We are already arrived at the end of time
                break
            elif chord_end < end and chord_start >= start:
                # Perfect case we just copy the full chord
                new_score += chord.copy()
            else:
                # In all other cases we have to cut the chord
                new_start = start - time
                new_end = end - time
                new_chord = self.get_chord_between(chord, new_start, new_end)
                new_score += new_chord

            time += chord.duration

        return new_score



    def to_pickle(self, filepath):
        import pickle
        with open(filepath, 'wb') as f:
            pickle.dump(self, f)

    @classmethod
    def read_pickle(cls, filepath):
        import pickle
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
        return data

    def __eq__(self, other):
        from .chord import Chord
        if isinstance(other, Chord):
            return self == Score([other])
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
            return Score([c % other for c in self.chords])
        else:
            raise Exception('Following % should be a Tonality')

    def __radd__(self, other):
        if other is None:
            return self.copy()

    def __repr__(self):
        return ' \n'.join([str(chord) for chord in self.chords])

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__ = d


    @property
    def duration(self):
        return sum([c.duration for c in self.chords])

    def to_code(self, **kwargs):
        """
        Export the chord serie as a string representing valid python code that recreates the score
        :return:
        """
        from .out.to_code import chord_serie_to_code

        code = chord_serie_to_code(self, **kwargs)
        return code

    def to_code_file(self, filepath, **kwargs):
        """
        Export the chord serie as a file representing valid python code that recreates the score
        :param filepath:
        :return:
        """
        code = self.to_code(**kwargs)
        with open(filepath, 'w') as f:
            f.write(code)


    def to_midi(self, filepath, **kwargs):
        # Convert score to midi
        from .out.to_midi import score_to_midi

        return score_to_midi(self, filepath, **kwargs)

