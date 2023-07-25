"""
Copyright (c) 2023, Florian GARDIN
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""

from .constants import *
from .element import Element
from .note import Note, Silence, Continuation
from typing import List

I = i = Element(0)
II = ii = Element(1)
III = iii = Element(2)
IV = iv = Element(3)
V = v = Element(4)
VI = vi = Element(5)
VII = vii = Element(6)
Atonal = (I % I.M)
NC = (I % I.M)
r = Silence(1)
l = Continuation(1)

# Chord scale
c0 = Note('c', 0, 0, 1)  # c0 represents the first note in the chord.chord_notes
c1 = Note('c', 1, 0, 1)
c2 = Note('c', 2, 0, 1)
c3 = Note('c', 3, 0, 1)
c4 = Note('c', 4, 0, 1)
c5 = Note('c', 5, 0, 1)
c6 = Note('c', 6, 0, 1)
c7 = Note('c', 7, 0, 1)
c8 = Note('c', 8, 0, 1)
c9 = Note('c', 9, 0, 1)
c10 = Note('c', 10, 0, 1)
c11 = Note('c', 11, 0, 1)

cu0 = Note('cu', 0, 0, 1)
cu1 = Note('cu', 1, 0, 1)
cu2 = Note('cu', 2, 0, 1)
cu3 = Note('cu', 3, 0, 1)
cu4 = Note('cu', 4, 0, 1)
cu5 = Note('cu', 5, 0, 1)
cu6 = Note('cu', 6, 0, 1)
cu7 = Note('cu', 7, 0, 1)
cu8 = Note('cu', 8, 0, 1)
cu9 = Note('cu', 9, 0, 1)
cu10 = Note('cu', 10, 0, 1)
cu11 = Note('cu', 11, 0, 1)

cd0 = Note('cd', 0, 0, 1)
cd1 = Note('cd', 1, 0, 1)
cd2 = Note('cd', 2, 0, 1)
cd3 = Note('cd', 3, 0, 1)
cd4 = Note('cd', 4, 0, 1)
cd5 = Note('cd', 5, 0, 1)
cd6 = Note('cd', 6, 0, 1)
cd7 = Note('cd', 7, 0, 1)
cd8 = Note('cd', 8, 0, 1)
cd9 = Note('cd', 9, 0, 1)
cd10 = Note('cd', 10, 0, 1)
cd11 = Note('cd', 11, 0, 1)


# Scale
s0 = Note('s', 0, 0, 1)
s1 = Note('s', 1, 0, 1)
s2 = Note('s', 2, 0, 1)
s3 = Note('s', 3, 0, 1)
s4 = Note('s', 4, 0, 1)
s5 = Note('s', 5, 0, 1)
s6 = Note('s', 6, 0, 1)

# chord from basses
b0 = Note('b', 0, 0, 1)  # b0 represents the first note in the chord.extension_notes
b1 = Note('b', 1, 0, 1)  # b1 represents the second note in the chord.extension_notes
b2 = Note('b', 2, 0, 1)
b3 = Note('b', 3, 0, 1)
b4 = Note('b', 4, 0, 1)
b5 = Note('b', 5, 0, 1)
b6 = Note('b', 6, 0, 1)
b7 = Note('b', 7, 0, 1)
b8 = Note('b', 8, 0, 1)
b9 = Note('b', 9, 0, 1)
b10 = Note('b', 10, 0, 1)
b11 = Note('b', 11, 0, 1)

bu0 = Note('bu', 0, 0, 1)  # b0 represents the first note in the chord.extension_notes
bu1 = Note('bu', 1, 0, 1)  # b1 represents the second note in the chord.extension_notes
bu2 = Note('bu', 2, 0, 1)
bu3 = Note('bu', 3, 0, 1)
bu4 = Note('bu', 4, 0, 1)
bu5 = Note('bu', 5, 0, 1)
bu6 = Note('bu', 6, 0, 1)
bu7 = Note('bu', 7, 0, 1)
bu8 = Note('bu', 8, 0, 1)
bu9 = Note('bu', 9, 0, 1)
bu10 = Note('bu', 10, 0, 1)
bu11 = Note('bu', 11, 0, 1)

bd0 = Note('bd', 0, 0, 1)  # b0 represents the first note in the chord.extension_notes
bd1 = Note('bd', 1, 0, 1)  # b1 represents the second note in the chord.extension_notes
bd2 = Note('bd', 2, 0, 1)
bd3 = Note('bd', 3, 0, 1)
bd4 = Note('bd', 4, 0, 1)
bd5 = Note('bd', 5, 0, 1)
bd6 = Note('bd', 6, 0, 1)
bd7 = Note('bd', 7, 0, 1)
bd8 = Note('bd', 8, 0, 1)
bd9 = Note('bd', 9, 0, 1)
bd10 = Note('bd', 10, 0, 1)
bd11 = Note('bd', 11, 0, 1)



# Absolute notes
a0 = Note('a', 0, 0, 1)
a1 = Note('a', 1, 0, 1)
a2 = Note('a', 2, 0, 1)
a3 = Note('a', 3, 0, 1)
a4 = Note('a', 4, 0, 1)
a5 = Note('a', 5, 0, 1)
a6 = Note('a', 6, 0, 1)
a7 = Note('a', 7, 0, 1)
a8 = Note('a', 8, 0, 1)
a9 = Note('a', 9, 0, 1)
a10 = Note('a', 10, 0, 1)
a11 = Note('a', 11, 0, 1)
a12 = Note('a', 12, 0, 1)
a13 = Note('a', 13, 0, 1)
a14 = Note('a', 14, 0, 1)

# Pattern notes
x0 = Note('x', 0, 0, 1)
x1 = Note('x', 1, 0, 1)
x2 = Note('x', 2, 0, 1)
x3 = Note('x', 3, 0, 1)
x4 = Note('x', 4, 0, 1)
x5 = Note('x', 5, 0, 1)
x6 = Note('x', 6, 0, 1)
x7 = Note('x', 7, 0, 1)
x8 = Note('x', 8, 0, 1)
x9 = Note('x', 9, 0, 1)
x10 = Note('x', 10, 0, 1)
x11 = Note('x', 11, 0, 1)
x12 = Note('x', 12, 0, 1)
x13 = Note('x', 13, 0, 1)
x14 = Note('x', 14, 0, 1)
x15 = Note('x', 15, 0, 1)
x16 = Note('x', 16, 0, 1)
x17 = Note('x', 17, 0, 1)
x18 = Note('x', 18, 0, 1)
x19 = Note('x', 19, 0, 1)
x20 = Note('x', 20, 0, 1)
x21 = Note('x', 21, 0, 1)
x22 = Note('x', 22, 0, 1)



bdd = Note('d', 11, -3, 1)  # bassdrum
bd = Note('d', 0, -2, 1)  # bassdrum
rs = Note('d', 1, -2, 1)     # rimshot
sn = Note('d', 2, -2, 1)  # Snare drum 1
cp = Note('d', 3, -2, 1)   # Clap
sn2 = Note('d', 4, -2, 1)   # Snare drum 2
bt = Note('d', 5, -2, 1)   # Bass tom
hh = Note('d', 6, -2, 1)  # Bass tom
lt = Note('d', 7, -2, 1)  # Low tom
ch = Note('d', 8, -2, 1)  # Closed hat
mt = Note('d', 9, -2, 1)  # Medium tom
oh = Note('d', 10, -2, 1)  # Open hat
ht = Note('d', 11, -2, 1)  # High tom

d0 = Note('d', 0, 0, 1)
d1 = Note('d', 1, 0, 1)
d2 = Note('d', 2, 0, 1)
d3 = Note('d', 3, 0, 1)
d4 = Note('d', 4, 0, 1)
d5 = Note('d', 5, 0, 1)
d6 = Note('d', 6, 0, 1)
d7 = Note('d', 7, 0, 1)
d8 = Note('d', 8, 0, 1)
d9 = Note('d', 9, 0, 1)
d10 = Note('d', 10, 0, 1)
d11 = Note('d', 11, 0, 1)

hht = Note('d', 0, -1, 1)
crash = Note('d', 1, -1, 1)
other_hht = Note('d', 2, -1, 1)
ride = Note('d', 3, -1, 1)
ride_hard = Note('d', 4, -1, 1)
dr050 = Note('d', 5, -1, 1)
dr060 = Note('d', 6, -1, 1)
dr070 = Note('d', 7, -1, 1)
dr080 = Note('d', 8, -1, 1)
dr090 = Note('d', 9, -1, 1)
dr100 = Note('d', 10, -1, 1)
dr110 = Note('d', 11, -1, 1)

dr001 = Note('d', 0, 0, 1)
dr011 = Note('d', 1, 0, 1)
dr021 = Note('d', 2, 0, 1)
dr031 = Note('d', 3, 0, 1)
dr041 = Note('d', 4, 0, 1)
dr051 = Note('d', 5, 0, 1)
dr061 = Note('d', 6, 0, 1)
dr071 = Note('d', 7, 0, 1)
dr081 = Note('d', 8, 0, 1)
dr091 = Note('d', 9, 0, 1)
dr101 = Note('d', 10, 0, 1)
dr111 = Note('d', 11, 0, 1)

dr002 = Note('d', 0, 1, 1)
dr012 = Note('d', 1, 1, 1)
dr022 = Note('d', 2, 1, 1)
dr032 = Note('d', 3, 1, 1)
dr042 = Note('d', 4, 1, 1)
dr052 = Note('d', 5, 1, 1)
dr062 = Note('d', 6, 1, 1)
dr072 = Note('d', 7, 1, 1)
dr082 = Note('d', 8, 1, 1)
dr092 = Note('d', 9, 1, 1)
dr102 = Note('d', 10, 1, 1)
dr112 = Note('d', 11, 1, 1)

dr003 = Note('d', 0, 2, 1)
dr013 = Note('d', 1, 2, 1)
dr023 = Note('d', 2, 2, 1)
dr033 = Note('d', 3, 2, 1)
dr043 = Note('d', 4, 2, 1)
dr053 = Note('d', 5, 2, 1)
dr063 = Note('d', 6, 2, 1)
dr073 = Note('d', 7, 2, 1)
dr083 = Note('d', 8, 2, 1)
dr093 = Note('d', 9, 2, 1)
dr103 = Note('d', 10, 2, 1)
dr113 = Note('d', 11, 2, 1)


C1 = Note('a', 0, -4, 1)
Cs1 = Note('a', 1, -4, 1)
Db1 = Note('a', 1, -4, 1)
D1 = Note('a', 2, -4, 1)
Ds1 = Note('a', 3, -4, 1)
Eb1 = Note('a', 3, -4, 1)
E1 = Note('a', 4, -4, 1)
F1 = Note('a', 5, -4, 1)
Fs1 = Note('a', 6, -4, 1)
Gb1 = Note('a', 6, -4, 1)
G1 = Note('a', 7, -4, 1)
Gs1 = Note('a', 8, -4, 1)
Ab1 = Note('a', 8, -4, 1)
A1 = Note('a', 9, -4, 1)
As1 = Note('a', 10, -4, 1)
Bb1 = Note('a', 10, -4, 1)
B1 = Note('a', 11, -4, 1)

C2 = Note('a', 0, -3, 1)
Cs2 = Note('a', 1, -3, 1)
Db2 = Note('a', 1, -3, 1)
D2 = Note('a', 2, -3, 1)
Ds2 = Note('a', 3, -3, 1)
Eb2 = Note('a', 3, -3, 1)
E2 = Note('a', 4, -3, 1)
F2 = Note('a', 5, -3, 1)
Fs2 = Note('a', 6, -3, 1)
Gb2 = Note('a', 6, -3, 1)
G2 = Note('a', 7, -3, 1)
Gs2 = Note('a', 8, -3, 1)
Ab2 = Note('a', 8, -3, 1)
A2 = Note('a', 9, -3, 1)
As2 = Note('a', 10, -3, 1)
Bb2 = Note('a', 10, -3, 1)
B2 = Note('a', 11, -3, 1)


C3 = Note('a', 0, -2, 1)
Cs3 = Note('a', 1, -2, 1)
Db3 = Note('a', 1, -2, 1)
D3 = Note('a', 2, -2, 1)
Ds3 = Note('a', 3, -2, 1)
Eb3 = Note('a', 3, -2, 1)
E3 = Note('a', 4, -2, 1)
F3 = Note('a', 5, -2, 1)
Fs3 = Note('a', 6, -2, 1)
Gb3 = Note('a', 6, -2, 1)
G3 = Note('a', 7, -2, 1)
Gs3 = Note('a', 8, -2, 1)
Ab3 = Note('a', 8, -2, 1)
A3 = Note('a', 9, -2, 1)
As3 = Note('a', 10, -2, 1)
Bb3 = Note('a', 10, -2, 1)
B3 = Note('a', 11, -2, 1)

C4 = Note('a', 0, -1, 1)
Cs4 = Note('a', 1, -1, 1)
Db4 = Note('a', 1, -1, 1)
D4 = Note('a', 2, -1, 1)
Ds4 = Note('a', 3, -1, 1)
Eb4 = Note('a', 3, -1, 1)
E4 = Note('a', 4, -1, 1)
F4 = Note('a', 5, -1, 1)
Fs4 = Note('a', 6, -1, 1)
Gb4 = Note('a', 6, -1, 1)
G4 = Note('a', 7, -1, 1)
Gs4 = Note('a', 8, -1, 1)
Ab4 = Note('a', 8, -1, 1)
A4 = Note('a', 9, -1, 1)
As4 = Note('a', 10, -1, 1)
Bb4 = Note('a', 10, -1, 1)
B4 = Note('a', 11, -1, 1)


C5 = Note('a', 0, 0, 1)
Cs5 = Note('a', 1, 0, 1)
Db5 = Note('a', 1, 0, 1)
D5 = Note('a', 2, 0, 1)
Ds5 = Note('a', 3, 0, 1)
Eb5 = Note('a', 3, 0, 1)
E5 = Note('a', 4, 0, 1)
F5 = Note('a', 5, 0, 1)
Fs5 = Note('a', 6, 0, 1)
Gb5 = Note('a', 6, 0, 1)
G5 = Note('a', 7, 0, 1)
Gs5 = Note('a', 8, 0, 1)
Ab5 = Note('a', 8, 0, 1)
A5 = Note('a', 9, 0, 1)
As5 = Note('a', 10, 0, 1)
Bb5 = Note('a', 10, 0, 1)
B5 = Note('a', 11, 0, 1)

C6 = Note('a', 0, 1, 1)
Cs6 = Note('a', 1, 1, 1)
Db6 = Note('a', 1, 1, 1)
D6 = Note('a', 2, 1, 1)
Ds6 = Note('a', 3, 1, 1)
Eb6 = Note('a', 3, 1, 1)
E6 = Note('a', 4, 1, 1)
F6 = Note('a', 5, 1, 1)
Fs6 = Note('a', 6, 1, 1)
Gb6 = Note('a', 6, 1, 1)
G6 = Note('a', 7, 1, 1)
Gs6 = Note('a', 8, 1, 1)
Ab6 = Note('a', 8, 1, 1)
A6 = Note('a', 9, 1, 1)
As6 = Note('a', 10, 1, 1)
Bb6 = Note('a', 10, 1, 1)
B6 = Note('a', 11, 1, 1)


C7 = Note('a', 0, 2, 1)
Cs7 = Note('a', 1, 2, 1)
Db7 = Note('a', 1, 2, 1)
D7 = Note('a', 2, 2, 1)
Ds7 = Note('a', 3, 2, 1)
Eb7 = Note('a', 3, 2, 1)
E7 = Note('a', 4, 2, 1)
F7 = Note('a', 5, 2, 1)
Fs7 = Note('a', 6, 2, 1)
Gb7 = Note('a', 6, 2, 1)
G7 = Note('a', 7, 2, 1)
Gs7 = Note('a', 8, 2, 1)
Ab7 = Note('a', 8, 2, 1)
A7 = Note('a', 9, 2, 1)
As7 = Note('a', 10, 2, 1)
Bb7 = Note('a', 10, 2, 1)
B7 = Note('a', 11, 2, 1)


C8 = Note('a', 0, 2, 1)
Cs8 = Note('a', 1, 2, 1)
Db8 = Note('a', 1, 2, 1)
D8 = Note('a', 2, 2, 1)
Ds8 = Note('a', 3, 2, 1)
Eb8 = Note('a', 3, 2, 1)
E8 = Note('a', 4, 2, 1)
F8 = Note('a', 5, 2, 1)
Fs8 = Note('a', 6, 2, 1)
Gb8 = Note('a', 6, 2, 1)
G8 = Note('a', 7, 2, 1)
Gs8 = Note('a', 8, 2, 1)
Ab8 = Note('a', 8, 2, 1)
A8 = Note('a', 9, 2, 1)
As8 = Note('a', 10, 2, 1)
Bb8 = Note('a', 10, 2, 1)
B8 = Note('a', 11, 2, 1)



# Chromatic
h0 = Note('h', 0, 0, 1)
h1 = Note('h', 1, 0, 1)
h2 = Note('h', 2, 0, 1)
h3 = Note('h', 3, 0, 1)
h4 = Note('h', 4, 0, 1)
h5 = Note('h', 5, 0, 1)
h6 = Note('h', 6, 0, 1)
h7 = Note('h', 7, 0, 1)
h8 = Note('h', 8, 0, 1)
h9 = Note('h', 9, 0, 1)
h10 = Note('h', 10, 0, 1)
h11 = Note('h', 11, 0, 1)

# Scale sup
su0 = Note('su', 0, 0, 1)
su1 = Note('su', 1, 0, 1)
su2 = Note('su', 2, 0, 1)
su3 = Note('su', 3, 0, 1)
su4 = Note('su', 4, 0, 1)
su5 = Note('su', 5, 0, 1)
su6 = Note('su', 6, 0, 1)
su7 = Note('su', 7, 0, 1)
su8 = Note('su', 8, 0, 1)
su9 = Note('su', 9, 0, 1)
su10 = Note('su', 10, 0, 1)
su11 = Note('su', 11, 0, 1)

# Scale sdown
sd0 = Note('sd', 0, 0, 1)
sd1 = Note('sd', 1, 0, 1)
sd2 = Note('sd', 2, 0, 1)
sd3 = Note('sd', 3, 0, 1)
sd4 = Note('sd', 4, 0, 1)
sd5 = Note('sd', 5, 0, 1)
sd6 = Note('sd', 6, 0, 1)
sd7 = Note('sd', 7, 0, 1)
sd8 = Note('sd', 8, 0, 1)
sd9 = Note('sd', 9, 0, 1)
sd10 = Note('sd', 10, 0, 1)
sd11 = Note('sd', 11, 0, 1)

# Chord up
cu0 = Note('cu', 0, 0, 1)
cu1 = Note('cu', 1, 0, 1)
cu2 = Note('cu', 2, 0, 1)
cu3 = Note('cu', 3, 0, 1)
cu4 = Note('cu', 4, 0, 1)
cu5 = Note('cu', 5, 0, 1)
cu6 = Note('cu', 6, 0, 1)
cu7 = Note('cu', 7, 0, 1)
cu8 = Note('cu', 8, 0, 1)
cu9 = Note('cu', 9, 0, 1)
cu10 = Note('cu', 10, 0, 1)
cu11 = Note('cu', 11, 0, 1)

# Chord down
cd0 = Note('cd', 0, 0, 1)
cd1 = Note('cd', 1, 0, 1)
cd2 = Note('cd', 2, 0, 1)
cd3 = Note('cd', 3, 0, 1)
cd4 = Note('cd', 4, 0, 1)
cd5 = Note('cd', 5, 0, 1)
cd6 = Note('cd', 6, 0, 1)
cd7 = Note('cd', 7, 0, 1)
cd8 = Note('cd', 8, 0, 1)
cd9 = Note('cd', 9, 0, 1)
cd10 = Note('cd', 10, 0, 1)
cd11 = Note('cd', 11, 0, 1)

# Chromatic up
# Chord up
hu0 = Note('hu', 0, 0, 1)
hu1 = Note('hu', 1, 0, 1)
hu2 = Note('hu', 2, 0, 1)
hu3 = Note('hu', 3, 0, 1)
hu4 = Note('hu', 4, 0, 1)
hu5 = Note('hu', 5, 0, 1)
hu6 = Note('hu', 6, 0, 1)
hu7 = Note('hu', 7, 0, 1)
hu8 = Note('hu', 8, 0, 1)
hu9 = Note('hu', 9, 0, 1)
hu10 = Note('hu', 10, 0, 1)
hu11 = Note('hu', 11, 0, 1)

# Chord down
hd0 = Note('hd', 0, 0, 1)
hd1 = Note('hd', 1, 0, 1)
hd2 = Note('hd', 2, 0, 1)
hd3 = Note('hd', 3, 0, 1)
hd4 = Note('hd', 4, 0, 1)
hd5 = Note('hd', 5, 0, 1)
hd6 = Note('hd', 6, 0, 1)
hd7 = Note('hd', 7, 0, 1)
hd8 = Note('hd', 8, 0, 1)
hd9 = Note('hd', 9, 0, 1)
hd10 = Note('hd', 10, 0, 1)
hd11 = Note('hd', 11, 0, 1)


# Base tonality

TONALITY_C = I.M
TONALITY_Cs = I.s.M
TONALITY_Db = II.b.M
TONALITY_D = II.M
TONALITY_Ds = II.s.M
TONALITY_Eb = III.b.M
TONALITY_E = III.M
TONALITY_F = IV.M
TONALITY_Fs = IV.s.M
TONALITY_Gb = V.b.M
TONALITY_G = V.M
TONALITY_Gs = VI.b.M
TONALITY_Ab = VI.b.M
TONALITY_A = VI.M
TONALITY_As = VII.b.M
TONALITY_Bb = VII.b.M
TONALITY_B = VII.M
TONALITY_Bs = I.M


# Others

STRONG_BEAT = a0
WEAK_BEAT = a1
CHORD_NOTE = a2
SCALE_NOTE = a3
TONIC = a4
TONIC_OR_FIFTH = a5
TRIAD_NOTE = a6
SCALE_DISSONNANCE = a7


CONTINUATION = l
SILENCE = r

BASE_EXTENSION_DICT = {
    '': [s0, s2, s4],
    '5': [s0, s2, s4],
    '6': [s2, s4, s0.o(1)],
    '64': [s4, s0.o(1), s2.o(1)],
    '7': [s0, s2, s4, s6],
    '65': [s2, s4, s6, s0.o(1)],
    '43': [s4, s6, s0.o(1), s2.o(1)],
    '2': [s6.o(-1), s0, s2, s4],
    '9': [s0, s2, s4, s6, s1.o(1)],
    '11': [s0, s2, s4, s6, s1.o(1), s3.o(1)],
    '13': [s0, s2, s4, s6, s1.o(1), s3.o(1), s5.o(1)],
}
ALL_EXTENSIONS = {'5', '6', '64', '7', '65', '43', '2', '9', '11', '13'}
ALL_REPLACEMENTS = {"sus2", "sus4", "+", "b5", "m3", "M3", "m6", "M6", "m7", "M7", "b9", "#9", "m11", "M11", "m13", "M13", "#4"}
ALL_ADDITIONS = {"add2", "add4", "add6", "add9", "add11", "add13", "+",
                 "b2", "#2", "M3", "m3", "m6", "M6", "m7", "M7", "b9", "#9", "m10", "M10", "#11", "m13", "M13"}

DICT_REPLACEMENT = {
    "sus2": (s2, s1),
    "sus4": (s2, s3),
    "+": (s4, h8),
    "b5": (s4, h6),
    "m3": (s2, h3),
    "M3": (s2, h4),
    "m6": (s5, h8),
    "M2": (s2, h2),
    "M6": (s5, h9),
    "m7": (s6, h10),
    "M7": (s6, h11),
    "m9": (s1, h1),
    "M9": (s1, h2),
    "#11": (s3, h6),
    "m13": (s5, h8),
    "M13": (s5, h9)
}

DICT_REMOVAL = {
    "-1": s0,
    "-3": s2,
    "-5": s4,
    "-7": s6,
    "-9": s1,
    "-11": s3
}

DICT_ADDITION = {
    "add2": (s0, s1),
    "add4": (s2, s3),
    "add6": (s4, s5),
    "add7": (s4, s6),
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
    "#4": (s4, h6),
    "m13": (s4, s5.o(1)),
    "M13": (s4, s5.o(1))
}