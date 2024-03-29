About MusicLang
===============

.. image:: ../images/MusicLang.png
  :width: 400
  :alt: MusicLang logo

The Python framework to write, analyze, transform and predict music.

What is MusicLang ?
--------------------

MusicLang which simply stands for "music language" is a Python framework
implementing a new language for tonal music.
This language allows composers to load, write, transform and predict symbolic music in a simple,
condensed and high level manner.
MusicLang internally uses  a `LLM (Large Language Model) <https://huggingface.co/floriangardin/musiclang`_  to predict what could happen next in a musical score.
This framework is well suited to :
- Generate musical ideas quickly.
- Predict what could happen next in an existing midi file
- Create an interpretable and information rich text representation of a midi file

.. note :: Writing music with this framework supposes that you have some basic knowledge on scales, tonalities and
    roman numeral notation of chords.

How to install
--------------

MusicLang is available on Pypi ::

    pip install musiclang



A first example
----------------

1. Here is a simple example to write a C-major chord in musiclang and save it to midi ::

    from musiclang.library import *

    # Write A C major chord
    score = (I % I.M)(s0, s2, s4)

    # Store it to midi
    score.to_midi('c_major.mid')


2. Create, transform and harmonize a theme quickly ::


    from musiclang.library import *

    # Create a cool melody (the beginning of happy birthday, independant of any harmonic context)
    melody = s4.ed + s4.s + s5 + s4 + s0.o(1) + s6.h

    # Create a simple accompaniment with a cello and a oboe
    acc_melody = r + s0.o(-1).q * 3 + s0.o(-1).h
    accomp = {'cello__0': acc_melody, 'oboe__0': acc_melody.o(1)}

    # Play it in F-major
    score = (I % IV.M)(violin__0=melody, **accomp)

    # Repeat the score a second time in F-minor and forte
    score += (score % I.m).f

    # Just to create an anachrusis at the first bar
    score = (I % I.M)(violin__0=r.h) + score

    # Transform a bit the accompaniment by applying counterpoint rules automatically
    from musiclang.transform.library import create_counterpoint_on_score
    score = create_counterpoint_on_score(score, fixed_parts=['violin__0'])

    # Save it to musicxml
    score.to_midi('happy_birthday.musicxml', signature=(3, 4), title='Happy birthday !')

    # Et voilà !

.. image:: ../images/happy_birthday.png
  :width: 400
  :alt: Happy birthday score

3. Predict a score using a deep learning model trained on musiclang language ::

    from musiclang.library import *
    from musiclang import Score

    # Some random bar of chopin op18 Waltz
    score = ((V % III.b.M)(
        piano__0=s0 + s2.e.mp + s3.e.mp,
        piano__4=s0.e.o(-2).p + r.e + s0.ed.o(-1).mp + r.s,
        piano__5=r + s4.ed.o(-1).mp + r.s,
        piano__6=r + s6.ed.o(-1).mp + r.s)+
    (V['7'] % III.b.M)(
        piano__0=s2.ed.mp + r.s,
        piano__2=s4.ed.mp + r.s,
        piano__4=s6.ed.o(-1).mp + r.s,
        piano__5=s0.ed.o(-1).mp + r.s,
        piano__6=s4.ed.o(-1).mp + r.s))

    # Predict the next two chords of the score using huggingface musiclang model
    predicted_score = score.predict_score(n_chords=2, temperature=0.5)
    # Save it to midi
    predicted_score.to_midi('test.mid')

Please note that this feature is still experimental, it will only work with
piano music for now and the model is not yet trained on a large corpus of music.
If you want to help us train a better model, please contact `us <mailto:fgardin.pro@gmail.com>`_


4. Mix everything together to create a new pieces of music !



Learn MusicLang
---------------

To learn MusicLang we strongly advise to read the :ref:`user-guide-index`.


Contributing to MusicLang
-------------------------

MusicLang is a very recent library and is moving fast. Now it's quite exciting times because the roadmap
is still opened to change. Don't hesitate to `contact me <fgardin.pro@gmail.com>`_.
We are very interested to get in touch with composers,
musicologists, programmers, data scientists and any other people who want to help us.
We will regularly update issues on our `github repository <https://github.com/MusicLang/musiclang/issues>`_.
Don't hesitate to submit your own pull request if it makes sense for you and reflect your usage of musiclang.
