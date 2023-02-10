.. _drums:

Drum notes
===========

Drum track
-----------

You can specifically use a drum track in your song by using the "drums" instrument. Eg::

    from musiclang.library import *

    drum_score = (I % I.m)(drums=[bd + r + bd + r, hh * 4, r + sn + r + sn])





Drum note library
------------------

This is the list of drum figures that you can use in MusicLang :

- ``bd``: Bass drum
- ``rs``: Rimshot of snare drum
- ``sn``: Snare drum (lower)
- ``cp``: Clap
- ``sn2``: Snare drum (higher)
- ``bt``: Bass Tom
- ``hh``: Hihat
- ``lt``: Low tom
- ``ch``: Closing Hihat (with foot pedal)
- ``mt``: Medium Tom
- ``oh``: Open Hihat shot
- ``ht``: High Tom


