Musiclang
=========

![MusicLang logo](https://github.com/MusicLang/musiclang/blob/main/documentation/images/MusicLang.png?raw=true "MusicLang")


[![Documentation Status](https://readthedocs.org/projects/musiclang/badge/?version=latest)](https://musiclang.readthedocs.io/en/latest/?badge=latest)

The Python framework to write, analyze, transform and predict music.


What is MusicLang ?
--------------------

MusicLang which simply stands for "music language" is a Python framework
that allows composers to write symbolic music in a condensed and high level manner.
The way one write music with this tool should be close to how one create music
in practice. This framework is not only another notation software but also
an assistant that is able to automate some tasks that would normally be tedious for a composer.
It is naturally good at analyzing and manipulating existing
pieces of music in musicxml or midi format.

[Read our documentation](https://musiclang.readthedocs.io/en/latest).


How to install
-------------

MusicLang is available on Pypi :

```
pip install musiclang
```

Or use this repo for the latest version :

```
pip install git+https://github.com/MusicLang/musiclang
```
    

Example
-------

Here is a simple example to write a C-major chord in musiclang and save it to midi :

```python
from musiclang.library import *

# Write A C major chord
score = (I % I.M)(piano__0=s0, piano__1=s2, piano__3=s4)

# Store it to midi
score.to_midi('c_major.mid')
```

