"""
Copyright (c) 2023, Florian GARDIN
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""

class Item(object):
    """ """
    def __init__(self, name, start, end, vel=0, pitch=0, track=0, channel=0, voice=0, value=''):
        self.name = name
        self.start = start  # start step
        self.end = end  # end step
        self.vel = vel
        self.pitch = pitch
        self.track = track
        self.channel = channel
        self.voice = voice
        self.value = value


    @classmethod
    def frommatrix(cls, matrix):
        """

        Parameters
        ----------
        matrix :
            

        Returns
        -------

        """
        return [Item('', start, end, vel, pitch, track, voice, channel) for start, end, vel, pitch, track, voice, channel in matrix]

    def __repr__(self):
        return f'Item(name={self.name:>10s}, start={self.start}, end={self.end}, ' \
               f'vel={self.vel}, pitch={self.pitch}, track={self.track}, channel={self.channel}, voice={self.voice},' \
               f'value={self.value})\n'

    def __eq__(self, other):
        return self.name == other.name and self.start == other.start and \
               self.pitch == other.pitch and self.track == other.track

    def array(self):
        """ """
        return [self.start, self.end, self.vel, self.pitch, self.track, self.channel, self.voice]



def quantize_notes_raw(notes, limit_denominator=8):
    """Quantize a sequence of notes limiting the denominator to "limit_denominator" parameter

    Parameters
    ----------
    notes :
        List[Item] : sequence of notes
    limit_denominator :
         (Default value = 8)

    Returns
    -------
    type
        new_notes : List[Item], quantized notes

    """
    from fractions import Fraction as frac
    new_notes = []
    for note in notes:
        note.start = note.start
        note.end = note.end
        note.start = frac(note.start).limit_denominator(limit_denominator)
        note.end = frac(note.end).limit_denominator(limit_denominator)
        new_notes.append(note)

    return new_notes


def convert_to_items(notes):
    """Convert an array of notes into an array of Item objects that represents notes
    and quantize them

    Parameters
    ----------
    notes :
        param bar_duration:
    offset :
        return:

    Returns
    -------

    """
    # Quantize
    items = []
    for note in notes:
        start = note[0]
        end = start + note[2]
        vel = int(note[3])
        pitch = int(note[1])
        track = int(note[4])
        channel = int(note[5])
        voice = int(note[6])
        items.append(Item("name", start, end, vel=vel, pitch=pitch, track=track, channel=channel, voice=voice))

    # Quantize notes in integer
    items = quantize_notes_raw(items)
    return items