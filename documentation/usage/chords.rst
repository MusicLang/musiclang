.. _chords:

Chords
=======

Chords are the building block to represent local harmony in musiclang.
In reality a chord is a chord scale, it means that it encapsulates information about the tonality.

In musiclang the melodies are expressed relatively to the chord, that is one bias that allows for expressiveness
and transformative power. Let's dive in to see how to write these chords.


Chord notation
----------------

As we saw in the general guide a chord is a degree, a tonality and an extension.

Here are some examples ::

    from musiclang.library import *

    C_major_chord = (I % I.M)  # I in key of C major
    C_minor_chord = (I % I.m)  # I In key of C minor
    F_sharp_diminished7 = (VII % V.m) # VII in key of G minor
    D_major_sus2_second_inversion = (I % II.M)['64[sus2]'] # I in key of D major



.. note:: Contrarily to usual notation we only have upper cased roman numerals "I", there is no "i". So the mode of the chord will depend only of the tonality

.. note:: The VII in minor (``m``) mode is the diminished chord (eg: F# diminished in G minor), not the VIIb by default.

.. note:: You can use the ``Chord.to_voicing`` method to get the notes of a given chord extension at any time


Chord extensions
-----------------

Chord extensions is a way to add information about a chord. Mainly its inversion and if it has some other notes than the base triad.

Formalism
````````````

You can write your chords using the following syntax :

``extension_code[replacement1]...[replacementN](addition1)...(additionN)...{omission1}...{omissionN}``

The extension is implemented on the ``__getitem__`` method of the chord (or []), calling this will return a new chord
with the proper extension.

Extension code :
****************

The extension follows the roman numeral notation standard :

- '' or '5' for root position of triad
- '6' for first inversion of triad
- '64' for second inversion of triad
- '7' for 4-note chord in root position
- '65' for 4-note chord first inversion
- '43' for 4-note chord second inversion
- '2' for 4-note chord third inversion
- '9' for 5-note chord root position
- '11' for 6-note chord root position
- '13' for 7-note chord root position


.. note:: There are not inversions for 9, 11 and 13 chords because these chord can usually be renamed by a fourth chord with additions.


Replacement :
****************

This is the replacement dict, the key is the name you can use between [] eg: [sus2]
The first value is the note replaced in the chord, the second value in the note added in the chord ::


    DICT_REPLACEMENT = {
        "sus2": (s2, s1),
        "sus4": (s2, s3),
        "+": (s4, h8),
        "b5": (s4, h6),
        "m3": (s2, h3),
        "M3": (s2, h4),
        "m6": (s5, h8),
        "M6": (s5, h9),
        "m7": (s6, h10),
        "M7": (s6, h11),
        "m9": (s1, h1.o(1)),
        "M9": (s1, h2.o(1)),
        "#11": (s3, h6.o(1)),
        "m13": (s5, h8.o(1)),
        "M13": (s5, h9.o(1))
    }


Additions :
****************



Here is the addition dict, the key is the name you can use between () eg: (+) for augmented chord
The first value is the note that will give the octave of the addition in the existing chord, the second value in the note added in the chord ::

    DICT_ADDITION = {
        "add2": (s0, s1),
        "add4": (s2, s3),
        "add6": (s4, s5),
        "add9": (s0, s1.o(1)),
        "add11": (s2, s3.o(1)),
        "add13": (s4, s5.o(1)),
        "+": (s4, h8),
        "m2": (s0, h1),
        "M2": (s0, h2),
        "m3": (s2, h3),
        "M3": (s2, h4),
        "m6": (s4, h8),
        "M6": (s4, h9),
        "m7": (s4, h10),
        "M7": (s4, h11),
        "m9": (s0, h1.o(1)),
        "M9": (s0, h3.o(1)),
        "m10": (s2, h3.o(1)),
        "M10": (s2, h4.o(1)),
        "#11": (s4, h6.o(1)),
        "m13": (s4, s5.o(1)),
        "M13": (s4, s5.o(1))
    }


Omissions :
****************

Here is the omission dict, the key is the name you can use between {} eg: {-1}
The value is the note removed in the chord ::

    DICT_REMOVAL = {
        "-1": s0,
        "-3": s2,
        "-5": s4,
        "-7": s6,
        "-9": s1,
        "-11": s3
    }

Create chord and arpeggios
```````````````````````````

Now that you can express fully extended chords, let's talk about chord notes and bass notes.
These two kind of notes allows you to write melodies


Chord extension notes
**********************

Chord extension notes (b0, b1 ...). Chord extension notes are understood as the notes of the
arpeggio of the current chord starting by the chord bass::

    score = (I % I.M)['6[sus2]'](b0 + b1 + b2 + b3)

Will give the notes : ``D, G, C.o(1), E.o(1)``

Another example slightly more complex ::


    score = (I % I.M)['6[m3](+){-1}'](b0 + b1 + b2 + b3)

Will give the notes : ``Eb, G#, Eb.o(1), G#.o(1)``


Chord notes
************

Chord notes (c0, c1 ...). Chord extension notes are understood as the notes of the
arpeggio of the current chord starting by the chord root. For example ::

    score = (I % I.M)['6[sus2]'](c0 + c1 + c2 + c3)

Will give the notes : ``C, D, G, C.o(1)``








