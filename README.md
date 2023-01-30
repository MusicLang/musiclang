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
--------------

MusicLang is available on Pypi :

```
pip install musiclang
```

Or use this repo for the latest version :

```
pip install git+https://github.com/MusicLang/musiclang
```
    

Examples
---------

1. A hello world example to create a C-major chord in musiclang and save it to midi :

```python
from musiclang.library import *

# Write A C major chord
score = (I % I.M)(piano=[s0, s2, s4])

# Store it to midi
score.to_midi('c_major.mid')
```

2. Create, transform and harmonize a theme quickly : 

```python
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
from musiclang.transform.composing import create_counterpoint_on_score
score = create_counterpoint_on_score(score, fixed_parts=['violin__0'])

# Save it to musicxml
score.to_musicxml('happy_birthday.musicxml', signature=(3, 4), title='Happy birthday !')

# Et voilà !
```

![Happy birthday score](https://github.com/MusicLang/musiclang/blob/main/documentation/images/happy_birthday.png?raw=true "Happy Birthday")
