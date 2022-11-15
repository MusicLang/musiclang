import numpy as np

"""
The algorithm is based on this paper :
HMM-Based Voice Separation of MIDI
Performance
Andrew McLeod
University of Edinburgh
Mark Steedman
University of Edinburgh
https://homepages.inf.ed.ac.uk/steedman/papers/music/VoiceSeparation.pdf

Tunable parameters : 
- sigp
- gmin
- sigg
- snew
"""
from .item import Item
import time
import pickle

def separate_voices(notes):
    """
    Input a sequence of notes
    :param notes:
    :return: List of voices for each notes
    """
    # Split notes in each offsets
    splitted_notes = split_notes(notes)

    voices = voice_separation_algorithm(splitted_notes)
    new_notes = []
    for idx, voice in enumerate(voices):
        for n in voice:
            n[5] = idx
            new_notes.append(n)

    return Item.frommatrix(new_notes)


def voice_separation_algorithm(splitted_notes, beam_size=1, max_states=1):

    S = [([], 1)]
    for idx, incoming_notes in enumerate(splitted_notes):
        print(f'=== Voice separation : Iteration {idx}/{len(splitted_notes)}')
        for n in incoming_notes:
            S = sum([evaluate_new_states(s, logprob, n, beam_size) for s, logprob in S], [])

            if len(S) > max_states:
                S = list(sorted(S, key=lambda x: -x[-1]))[:max_states]
    # Find max
    final_path, logprob = list(sorted(S, key=lambda x: -x[-1]))[0]
    return final_path

def recurse_voice_separation_algorithm():
    pass

def evaluate_new_states(S, logprob, n, beam_size):
    probas = generate_probas_for_one(S, n)
    assert len(probas) > 0
    # Save best 2
    probas = list(sorted(probas, key=lambda x: -x[1]))[:beam_size]
    # Save new_S, proba
    new_states = [(get_new_state(S, n, w), logprob + proba) for w, proba in probas]
    return new_states

def split_notes(notes):
    notes = sorted(notes, key=lambda x: x[0])
    splitted_notes = []
    time = notes[0][0]
    current_split = []
    for note in notes:
        if note[0] != time:
            splitted_notes.append(sorted(current_split, key=lambda x: x[3]))
            current_split = []
            time = note[0]
        current_split.append(note)

    splitted_notes.append(sorted(current_split, key=lambda x: x[3]))
    return splitted_notes

def get_new_state(S, n, w):
    import copy
    import time
    new_S = pickle.loads(pickle.dumps(S, -1))
    if w > 0:
        new_S[w-1].append(n)
    elif w < 0:
        new_S.insert(-w-1, [n])
    else:
        raise Exception('w must not be 0')
    return new_S


def generate_probas_for_one(S, n):
    nb_voices = len(S)
    new_voices = np.arange(-1, -nb_voices-2, -1).tolist()
    existing_voices = np.arange(1, nb_voices+1).tolist()
    # Filter new_voices and existing voices
    W = new_voices + existing_voices
    orders = [order(S, n, w) for w in W]
    max_order = max(orders)
    # Filter only max orders
    W = [w for w, ord in zip(W, orders) if ord == max_order]
    W = [w for w in W if w < 0 or can_be_same_voice(S[w-1][-1], n)]
    probas = [logP_Ti(S, n, w) for w in W]

    return list(zip(W, probas))

def on(n):
    return n[0]

def off(n):
    return n[1]

def duration(n):
    return off(n) - on(n)

def num(n):
    return n[3]

def can_be_same_voice(n1, n2):
    cond1 = off(n1) - on(n2) <= duration(n1)/2
    cond2 = off(n1) < off(n2)
    return cond1 and cond2

def gauss(mu, sig):
    return np.exp(-((mu) / sig)**2)


def g(S, n, w, sig_g=127000):
    last_V_w = S[w-1][-1]
    return np.log(1-(on(n) - off(last_V_w))/sig_g) + 1

def gap(S, n, w, gmin=9e-5):
    return max(g(S, n, w), gmin)


def pitch(S, n, w, sigp=4):
    return gauss(num(n) - average_pitch(S[w-1]), sigp)


def logP_Ti(S, ni, wi):
    return np.log(P(S, ni, wi)) + np.log(order(S, ni, wi))

def P_T(S, n, w):
    return np.product([P(S, ni, wi) * order(S, ni, wi) for ni, wi in zip(n, w)])

def order(S, n, w):
    case1 = (abs(w) > 1) and (average_pitch(S[abs(w) - 2]) > num(n))
    case2 = (0 < w < len(S)) and (average_pitch(S[w]) < num(n))
    case3 = (-len(S) <= w < 0) and (average_pitch(S[abs(w)-1]) < num(n))
    return 2 ** -(case1 + case2 + case3)

def P(S, n, w, s_new=2e-11):
    if w > 0:
        return pitch(S, n, w) * gap(S, n, w)
    else:
        return s_new

def average_pitch(V, l=5):
    """
    Calculate the weighted average pitch of the voice over a window of size l
    :param V:
    :param l:
    :return:
    """
    min_l_V = min(l, len(V))
    len_V = len(V)
    numerator = sum([(2**i) * num(V[len_V - i - 1]) for i in range(min_l_V)])
    denominator = sum([(2**i) for i in range(min_l_V)])
    return numerator / denominator
