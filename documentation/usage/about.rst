About MusicLang
===============

.. image:: ../images/MusicLang.png
  :width: 400
  :alt: MusicLang logo

The Python framework to write, analyze, transform and predict music.

What is MusicLang ?
--------------------

MusicLang which simply stands for "music language" is a Python framework
that allows composers to write symbolic music in a simple, condensed and high level manner.
This framework is not only another notation software but also
an assistant that is able to automate some tasks that would normally be tedious for a composer.
It is well suited to write new music or to manipulate existing music.

Being a simple text language it aims to integrates
naturally with Large language models.

.. note :: This framework supposes that you have some basic knowledge on scales, tonalities and
    roman numeral notation of chords.

How to install
--------------

MusicLang is available on Pypi ::

    pip install musiclang


Or use this repo for the latest version ::

    pip install git+https://github.com/MusicLang/musiclang


A first example
----------------

Here is a simple example to write a C-major chord in musiclang and save it to midi ::

    from musiclang.library import *

    # Write A C major chord
    score = (I % I.M)(s0, s2, s4)

    # Store it to midi
    score.to_midi('c_major.mid')



Learn MusicLang
---------------

To learn MusicLang we strongly advise to read the :ref:`user-guide-index`.


Contributing to MusicLang
-------------------------

MusicLang is a very recent library and is moving fast. Now it's quite exciting times because the roadmap
is still opened to change. Don't hesitate to `contact me <fgardin.pro@gmail.com>`.
We are very interested to get in touch with composers,
musicologists, programmers, data scientists and any other people who want to help us.
We will regularly update issues on our `github repository <https://github.com/MusicLang/musiclang/issues>`.
Don't hesitate to submit your own pull request if it makes sense for you and reflect your usage of musiclang.
