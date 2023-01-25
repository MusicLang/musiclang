from musiclang import Note, Silence, Continuation



def test_notes():
    note = Note("s", 0, 0, 1)
    assert note.notes == (None + note).notes


def test_scale_pitch():
    note = Note("s", 1, 1, 1)

    assert note.scale_pitch == 8

def test_scale_pitch_negative():
    note = Note("s", -1, 1, 1)

    assert note.scale_pitch == 6

def test_delta_value():
    note = Note("su", 1, 0, 1)
    # FIXME : Should delta value takes in account octaves ?
    assert note.delta_value == 1


def test_is_note():
    assert not Silence(1).is_note
    assert not Continuation(1).is_note
    assert Note("s", 1, 0, 1).is_note

def test_is_silence():
    note = Silence(1)
    assert note.is_silence
    assert not Note("s", 1, 0, 1).is_silence


def test_is_continuation():
    note = Continuation(1)
    assert note.is_continuation
    assert not Note("s", 1, 0, 1).is_continuation