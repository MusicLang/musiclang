"""
Copyright (c) 2023, Florian GARDIN
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""

class NotePitch:
    """ """

    def __init__(self, pitch, offset=0, duration=1, velocity=120, track=0, silence=0, continuation=0,
                 tempo=None, pedal=None
                 ):
        self.pitch = pitch
        self.offset = offset
        self.duration = duration
        self.velocity = velocity
        self.track = track
        self.silence = silence
        self.continuation = continuation
        self.tempo = tempo
        self.pedal = pedal


    def is_note(self):
        """ """
        return not (self.silence or self.continuation)

    def to_midi_note(self):
        """ """
        return [self.pitch, self.offset, self.duration, self.velocity, self.track, self.silence, self.continuation,
                self.tempo, self.pedal
                ]


