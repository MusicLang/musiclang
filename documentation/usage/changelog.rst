.. _changelog:


Changelog
=========

0.9.0
-----

First step toward integration of Deep learning model trained on musiclang language.

- Add Score.predict_score method to predict the continuation of the current score. It currently takes no arguments

0.8.0
-----

This version introduces many new features on how to write your score.
The main concept is that the chord extensions are now taken in account by the framework.
Moreover this chord naming is a lot more expressive, you can basically create any chord you want using
additions and replacements. There are now two kind of notes that uses this chord definition and helps you write cool chord progressions.
We also now supports drums with a specific instrument name "drum" and specific
notation in the language. Midi file loaded into musiclang parse these drum tracks.

These are still experimental and are not compatible troughout the whole API.

- Add Full chord extensions in Roman notation (ex : 64[sus2](+) for a sus2 with an augmented fifth in second inversion).
- Add Chord extension notes (b0, b1 ...). Chord extension notes are understood as the notes of the arpeggio of the current chord starting by the chord bass.
- Add Chord notes (c0, c1). Chord notes are the note of the arpeggio of the current chord starting by the chord root
- Add drum notes and drum instruments (eg: (I % I.M)(drums=bd + sd + bd + sd). Notes are automatically converted when instrument starts with drums.
- Add absolute notes that are never transposed in the library (eg : C5s for a C5#)
- Bug fixes and API and duplication of some methods for scores and chords
- Replacement of "to_voicings" method to "to_voicing" with new arguments

0.7.0
------

- Improve the documentation to show more concrete examples of musiclang
- Add `Score.to_musicxml` methods to export your score more easily into your favorite notation software
- Add `Score.to_music21` if you need the specific capabilities of music21 for your score
- Notes spelling follow the tonality correctly

