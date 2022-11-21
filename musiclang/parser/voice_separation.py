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
    :return: Sequence of note items with voice correctly
    set with the following algorithm : (https://homepages.inf.ed.ac.uk/steedman/papers/music/VoiceSeparation.pdf)
    """

    # Split notes in groups that are playing simultaneously
    splitted_notes = split_notes(notes)

    voices = voice_separation_algorithm(splitted_notes)
    print('NB VOICES FOR TRACK : ', len(voices))
    new_notes = []
    for idx, voice in enumerate(voices):
        for n in voice:
            n[6] = idx
            new_notes.append(n)

    return Item.frommatrix(new_notes)


def voice_separation_algorithm(splitted_notes, beam_size=1, max_states=1):
    """
    Implementation of the voice separation algorithm
    :param splitted_notes:
    :param beam_size: Number of best states to keep for each iteration
    :param max_states: Number of state to keep for each iteration
    :return:
    """
    S = [([], 1)] # State, logprob of state
    for idx, incoming_notes in enumerate(splitted_notes):
        print(f'=== Voice separation : Iteration {idx}/{len(splitted_notes)}', end='\r')
        for n in incoming_notes:
            S = sum([evaluate_new_states(s, logprob, n, beam_size) for s, logprob in S], [])
            if len(S) > max_states:
                S = list(sorted(S, key=lambda x: -x[-1]))[:max_states]
    # Find max
    final_path, logprob = list(sorted(S, key=lambda x: -x[-1]))[0]
    print()
    return final_path

def evaluate_new_states(S, logprob, n, beam_size):
    """
    Evaluate all candidate states for new note n in state S
    :param S:
    :param logprob:
    :param n:
    :param beam_size:
    :return:
    """
    probas = generate_probas_for_one(S, n)
    assert len(probas) > 0
    # Save best 2
    probas = list(sorted(probas, key=lambda x: -x[1]))[:beam_size]
    # Save new_S, proba
    new_states = [(get_new_state(S, n, w), logprob + proba) for w, proba in probas]
    return new_states

def split_notes(notes):
    """
    Split notes in a group of notes that are playing simultaneously
    :param notes:
    :return: list[list[note]]
    """
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
    #W = [w for w, ord in zip(W, orders) if ord == max_order]
    W = [w for w in W if w < 0 or can_be_same_voice(S[w-1][-1], n)]
    # if all([w < 0 for w in W]):
    #     print('Must create a new voice')
    #     from pdb import set_trace; set_trace()

    probas = [logP_Ti(S, n, w) for w in W]

    return list(zip(W, probas))

def on(n):
    """
    On time of note
    :param n: note
    :return:
    """
    return n[0]

def off(n):
    """
    Off time of note
    :param n: note
    :return:
    """
    return n[1]

def duration(n):
    """
    Duration of note
    :param n:
    :return:
    """
    return off(n) - on(n)

def num(n):
    """
    Pitch of note
    :param n:
    :return:
    """
    return n[3]

def can_be_same_voice(n1, n2):
    """
    Can n1 and n2 be on the same voice
    There is a condition on the overlapping of the two notes
    :param n1:
    :param n2:
    :return:
    """
    cond1 = off(n1) - on(n2) <= duration(n1)/2
    cond2 = off(n1) < off(n2)
    return cond1 and cond2

def gauss(mu, sig):
    """
    Gaussian density
    """
    return np.exp(-((mu) / sig)**2)


def g(S, n, w, sig_g=127000):
    """
    Estimate a penalty about the time gap between new note added in the specific voice of S
    :param S: State
    :param n: note
    :param w: voice index of note
    :param sig_g: std of g, tunable parameter
    :return:
    """
    last_V_w = S[w-1][-1]
    return np.log(1-(on(n) - off(last_V_w))/sig_g) + 1

def gap(S, n, w, gmin=9e-5):
    """
    Bound g gap function with a gmin
    :param S:
    :param n:
    :param w:
    :param gmin:
    :return:
    """
    return max(g(S, n, w), gmin)


def pitch(S, n, w, sigp=4):
    """
    Return the deviation of note pitch with average pitch of the state voice with gaussian density
    :param S: State
    :param n: note
    :param w: index in state where to add the note
    :param sigp: standard deviation of the density
    :return:
    """
    return gauss(num(n) - average_pitch(S[w-1]), sigp)


def logP_Ti(S, ni, wi):
    """
    Log-probability of a state transition of ni in voice wi - 1 of S
    :param S: State
    :param ni: note
    :param wi: index in state where to add the note
    :return:
    """
    return np.log(P(S, ni, wi)) + np.log(order(S, ni, wi))

def P_T(S, n, w):
    """
    Log-probability of a state transition of notes n in voices w of S
    :param S: State
    :param ni: list[note]
    :param wi: list[index in state where to add the note]
    :return:
    """
    return np.product([P(S, ni, wi) * order(S, ni, wi) for ni, wi in zip(n, w)])

def order(S, n, w):
    """
    Penalty to avoid note crossing, see : https://homepages.inf.ed.ac.uk/steedman/papers/music/VoiceSeparation.pdf
    :param S:
    :param n:
    :param w: index in state where to add the note
    :return:
    """
    case1 = (abs(w) > 1) and (average_pitch(S[abs(w) - 2]) > num(n)) # Crossing
    case2 = (0 < w < len(S)) and (average_pitch(S[w]) < num(n))
    case3 = (-len(S) <= w < 0) and (average_pitch(S[abs(w)-1]) < num(n))
    return 2 ** -(case1 + case2 + case3)

def P(S, n, w, s_new=2e-11):
    """
    Probability
    :param S: State
    :param n: note
    :param w: index in state where to add the note
    :param s_new: Proba of creating a new voice
    :return:
    """
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
