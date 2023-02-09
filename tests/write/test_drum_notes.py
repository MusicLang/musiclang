from musiclang.library import *
import pytest


def test_drum_note_dont_octave():
    assert sn.o(1) == sn


def test_drum_note_dont_transpose():
    assert (sn & 2) == sn


def test_drums_auto_converted():

    chord = (I % I.M)(drums=s0.o(-2))
    assert chord == (I % I.M)(drums=bd)

def test_unexisting_drum_lead_to_error():

    chord = (I % I.M)(drums=s0.o(-2) + s0)
    assert chord == (I % I.M)(drums=s0.o(-2) + r)