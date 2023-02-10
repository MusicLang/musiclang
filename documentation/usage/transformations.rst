.. _transforms:

Transformations library
========================

Transformations of scores are at the core of MusicLang. One the goal of musiclang is to be able
to easily manipulate music.

The transformers class
-----------------------

There are 4 different kinds of transformers :

- ``ScoreTransformer`` : You can input a score, will output a score
- ``ChordTransformer`` : You can input a score or a chord, will output the same class as the input
- ``MelodyTransformer`` : You can input a score, a chord or a melody, will output the same class as the input
- ``NoteTransformer`` : You can input a score, a chord, a melody or a note, will output the same class as the input

These transformers are mappings that acts on one specific object

Example ::

    from musiclang.transform.library import ReverseMelody
    from musiclang.library import *

    reverser = ReverseMelody()
    score = (I % I.M)(s0 + s1 + s2)

    print(reverser(score))

It will display : ``(I % I.M)(s2 + s1 + s0)``


Create your own transformer
----------------------------


For example here is the code of the ReverseMelody transformer ::

    from musiclang.transform import MelodyTransformer

    class ReverseMelody(MelodyTransformer):
        def action(self, melody, **kwargs):
            return Melody(melody.notes[::-1], tags=melody.tags)


You just have to override the action method and you are done !
If you pass for example a chord to this object, all the melodies will be mapped by the ``action`` method.

.. note:: There are specific arguments you can use for each kind of transformer if you need to pass some parameters from the parent to the child. For example the MelodyTransformer has a ``chord`` argument and an ``instrument`` argument