import pandas as pd
import numpy as np
from madmom.io.midi import MIDIFile
from mido import tempo2bpm

from .chords import convert_notes
from .to_musiclang import infer_chords, infer_chords_direct_method, infer_voices_per_instruments, infer_score
from .constants import *



class MidiToMusicLang:
    """
    Class to load midi into a musiclang score
    """
    def __init__(self, filename, **kwargs):
        self.score = MidiNotes.from_midi(filename, **kwargs)
        self.notes = np.asarray(self.score.notes_in_beats()[[START_TIME, NOTE, DURATION, VEL, TRACK, CHANNEL, VOICE]])
        self.metric_infos = {}
        self.kwargs = kwargs

    def get_score(self):
        """
        Return musiclang score
        :return: musiclang.Score
        """
        sequence, bar_duration_in_ticks, offset_in_ticks, max_chords, tick_value = \
            convert_notes(self.notes, **self.kwargs)
        chords = infer_chords(sequence, bar_duration_in_ticks, max_chords, **self.kwargs)
        sequence = infer_voices_per_instruments(sequence)
        score = infer_score(sequence, chords, self.score.instruments, bar_duration_in_ticks, offset_in_ticks, tick_value)

        self.metric_infos = {'bar_duration_in_ticks': bar_duration_in_ticks,
                        'offset_in_ticks': offset_in_ticks ,'max_chords': max_chords,
                        'tick_value': tick_value}


        return score, self.score.tempo


class MusicLangIgnoreException(Exception):
    pass

class MidiNotes:
    """
    Class to store midi notes and information about a midi file
    """
    def __init__(self, notes, ticks_per_beats=480, instruments=None,
                 tempo=120, beat_value=1, bar_duration=None,
                 tempos=None,
                 **kwargs):
        self.events = pd.DataFrame(notes, columns=[TYPE, TIME, NOTE, VEL, CHANNEL, TRACK])
        self.ticks_per_beats = ticks_per_beats
        self.notes = self.get_duration_dataframe()
        self.instruments = instruments
        self.tempo = tempo
        self.beat_value = beat_value
        self.kwargs = kwargs
        self.bar_duration = bar_duration
        self.tempos = tempos

    @classmethod
    def from_midi(cls, filename, ignore_file_with_bar_change=False, **kwargs):
        """
        Factory function to create a MidiNotes object from a midi file
        :param filename:
        :return:
        """
        parser = MidiParser(filename)
        notes, config = parser.parse()
        if len(config['bar_durations']) > 1 and ignore_file_with_bar_change:
            raise MusicLangIgnoreException('Bar duration change events in midifile, MusicLang cannot parse that')
        elif len(config['bar_durations']) == 1:
            config['bar_duration'] = config['bar_durations'][0]
        else:
            config['bar_duration'] = None
        return cls(notes, **config)

    def notes_in_beats(self):
        """
        By default notes are stored in ticks from midi file, convert it to beats
        :return:
        """
        df = self.notes.copy()
        df[START_TIME] /= self.ticks_per_beats
        df[END_TIME] /= self.ticks_per_beats
        df[DURATION] /= self.ticks_per_beats
        return df

    @property
    def config(self):
        return {'ticks_per_beats': self.ticks_per_beats, 'instruments': self.instruments,
                'tempo': self.tempo, 'beat_value': self.beat_value,
                'bar_duration': self.bar_duration, 'tempos': self.tempos
                }

    def get_duration_dataframe(self):
        """
        Convert note_on, note_off events to a note dataframe
        :return:
        """
        from itertools import product
        times = {(track, note): 0 for track, note in product(self.events[TRACK].unique(), range(120))}
        vels = {(track, note): 0 for track, note in product(self.events[TRACK].unique(), range(120))}
        ons = {(track, note): False for track, note in product(self.events[TRACK].unique(), range(120))}
        notes = []
        for idx, row in self.events.iterrows():
            if (row[TYPE] == ON) and row[VEL] > 0 and not ons[row[TRACK], row[NOTE]]:
                times[row[TRACK], row[NOTE]] = row[TIME]
                vels[row[TRACK], row[NOTE]] = row[VEL]
                ons[row[TRACK], row[NOTE]] = True
            else: # Note OFF
                start_time = times[row[TRACK], row[NOTE]]
                ons[row[TRACK], row[NOTE]] = False
                vel = vels[row[TRACK], row[NOTE]]
                end_time = row[TIME]
                duration = end_time - start_time
                notes.append([start_time, end_time, duration, row[NOTE], vel, row[CHANNEL], row[TRACK], 0])

        self.notes = pd.DataFrame(notes, columns=[START_TIME, END_TIME, DURATION, NOTE, VEL, CHANNEL, TRACK, VOICE]).sort_values(START_TIME)
        return self.notes



class MidiParser:

    def __init__(self, filename):
        self.filename = filename
        self.bar_durations = []
        self.tempos = []

    def parse(self, **kwargs):
        mf = MIDIFile(self.filename, unit="beats")
        notes, instruments = self._parse_midi(mf)
        tempo = int(tempo2bpm(mf.tempi[0][1]))
        beat_value = self._get_beat_value(mf)
        config ={'ticks_per_beats': mf.ticks_per_beat,
                 'instruments': instruments,
                 'tempo': tempo, 'tempos': self.tempos, 'beat_value': beat_value, 'bar_durations': self.bar_durations}
        return notes, config


    def _get_beat_value(self, mf):
        beat_value = 4 / mf.time_signatures[0][2]
        return beat_value

    def _infer_instruments(self, mf):
        from musiclang.core.out.constants import REVERSE_INSTRUMENT_DICT
        channel_inst = {}
        for track in mf.tracks:
            for note in track:
                if note.type == 'program_change':
                    channel_inst[note.channel] = REVERSE_INSTRUMENT_DICT[note.program]
        return channel_inst

    def _parse_midi(self, mf):
        from fractions import Fraction as frac
        instruments = self._infer_instruments(mf)
        notes = []
        for track_idx, track in enumerate(mf.tracks):
            time = 0
            for note in track:
                if note.type == 'note_on':
                    notes.append([1, time + note.time, note.note, note.velocity, note.channel, track_idx])
                elif note.type == 'note_off':
                    notes.append([0, time + note.time, note.note, note.velocity, note.channel, track_idx])
                elif note.type == 'time_signature':
                    self.bar_durations.append(note.numerator * frac(4, note.denominator))
                elif note.type == 'set_tempo':
                    self.tempos.append((time, note.tempo))
                time = time + note.time
        notes = np.asarray(notes)

        return notes, instruments
