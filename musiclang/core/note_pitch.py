
class NotePitch:

    def __init__(self, pitch, offset=0, duration=1, velocity=120, track=0, silence=0, continuation=0):
        self.pitch = pitch
        self.offset = offset
        self.duration = duration
        self.velocity = velocity
        self.track = track
        self.silence = silence
        self.continuation = continuation


    def is_note(self):
        return not (self.silence or self.continuation)

    def to_midi_note(self):
        return [self.pitch, self.offset, self.duration, self.velocity, self.track, self.silence, self.continuation]


