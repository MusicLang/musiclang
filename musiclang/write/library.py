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

r = Silence(1)
l = Continuation(1)

# Chord scale
c0 = Note('c', 0, 0, 1)
c1 = Note('c', 1, 0, 1)
c2 = Note('c', 2, 0, 1)
c3 = Note('c', 3, 0, 1)
c4 = Note('c', 4, 0, 1)
c5 = Note('c', 5, 0, 1)
c6 = Note('c', 6, 0, 1)
c7 = Note('c', 7, 0, 1)
c = lambda x: Note('c', x, 0, 1)

# Scale
s0 = Note('s', 0, 0, 1)
s1 = Note('s', 1, 0, 1)
s2 = Note('s', 2, 0, 1)
s3 = Note('s', 3, 0, 1)
s4 = Note('s', 4, 0, 1)
s5 = Note('s', 5, 0, 1)
s6 = Note('s', 6, 0, 1)
s = lambda x: Note('s', x, 0, 1)


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



a : List[Note] = [
     a0,
     a1,
     a2,
     a3,
     a4,
     a5,
     a6,
     a7,
     a8,
     a9,
     a10,
     a11,
     a12,
     a13,
     a14
     ]


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
h = lambda x: Note('h', x, 0, 1)

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
su = lambda x: Note('su', x, 0, 1)

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
sd = lambda x: Note('sd', x, 0, 1)

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
cu = lambda x: Note('cu', x, 0, 1)

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
cd = lambda x: Note('cd', x, 0, 1)

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
hu = lambda x: Note('hu', x, 0, 1)

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
hd = lambda x: Note('hd', x, 0, 1)

dw = Note('c', 0, 0, W)
dh = Note('c', 0, 0, H)
dq = Note('c', 0, 0, Q)
de = Note('c', 0, 0, E)
ds = Note('c', 0, 0, S)
dt = Note('c', 0, 0, T)

dw3 = Note('c', 0, 0, W3)
dh3 = Note('c', 0, 0, H3)
dq3 = Note('c', 0, 0, Q3)
de3 = Note('c', 0, 0, E3)
ds3 = Note('c', 0, 0, S3)
dt3 = Note('c', 0, 0, T3)

dw5 = Note('c', 0, 0, W5)
dh5 = Note('c', 0, 0, H5)
dq5 = Note('c', 0, 0, Q5)
de5 = Note('c', 0, 0, E5)
ds5 = Note('c', 0, 0, S5)
dt5 = Note('c', 0, 0, T5)

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



