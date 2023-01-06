About MusicLang
===============


MusicLang is a Python framework to write, analyze, transform and predict music.


How to install
==============

MusicLang is available on Pypi ::

    pip install musiclang


Or use this repo for the latest version ::

    pip install git+https://github.com/musiclang/<url>


Hello World example
===================

Here is a simple example to write a C-major chord in musiclang and save it to midi ::

    from musiclang.write.library import *

    # Write A C major chord
    score = (I % I.M)(piano__0=s0, piano__1=s2, piano__3=s4)

    # Load it in a midi player
    score.to_midi('c_major.mid')

