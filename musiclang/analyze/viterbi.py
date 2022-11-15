import numpy as np

def logviterbi(emission,
                       prior,
                       transitions,
                       index
               ):
    """Use the Viterbi algorithm to infer a sequence of key-chord pairs."""
    num_frames, num_chords = emission.shape
    num_transitions = len(transitions)

    loglik_matrix = np.zeros([num_frames, num_transitions])
    path_matrix = np.zeros([num_frames, num_transitions], dtype=np.int32)

    # Initialize with a uniform distribution over keys.
    loglik_matrix[0, :] = 1 / loglik_matrix.shape[1]
    loglik_matrix[0, :] = np.log(loglik_matrix[0, :])


    for frame in range(1, num_frames):
        # At each frame, store the log-likelihood of the best sequence ending in
        # each key-chord pair, along with the index of the parent key-chord pair
        # from the previous frame.
        mat = (np.tile(loglik_matrix[frame - 1][:, np.newaxis],
                       [1, num_transitions]) +
               transitions)

        path_matrix[frame, :] = mat.argmax(axis=0)
        loglik_matrix[frame, :] = (
            mat[path_matrix[frame, :], range(num_transitions)] +
            np.tile(emission[frame], 1))


    # Reconstruct the most likely sequence of key-chord pairs.
    path = [np.argmax(loglik_matrix[-1])]
    for frame in range(num_frames, 1, -1):
        path.append(path_matrix[frame - 1, path[-1]])

    return [index[i % num_chords]
            for i in path[::-1]]


def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]
    for st in states:
        V[0] [st] = {"prob": start_p[st] * emit_p[st] [obs[0]], "prev": None}
    # Run Viterbi when t > 0
    for t in range(1, len(obs)):
        V.append({})
        for st in states:
            max_tr_prob = V[t - 1] [states[0]] ["prob"] * trans_p[states[0]] [st]
            prev_st_selected = states[0]
            for prev_st in states[1:]:
                tr_prob = V[t - 1] [prev_st] ["prob"] * trans_p[prev_st] [st]
                if tr_prob > max_tr_prob:
                    max_tr_prob = tr_prob
                    prev_st_selected = prev_st

            max_prob = max_tr_prob * emit_p[st] [obs[t]]
            V[t] [st] = {"prob": max_prob, "prev": prev_st_selected}

    for line in dptable(V):
        print(line)

    opt = []
    max_prob = 0.0
    best_st = None
    # Get most probable state and its backtrack
    for st, data in V[-1].items():
        if data["prob"] > max_prob:
            max_prob = data["prob"]
            best_st = st
    opt.append(best_st)
    previous = best_st

    # Follow the backtrack till the first observation
    for t in range(len(V) - 2, -1, -1):
        opt.insert(0, V[t + 1] [previous] ["prev"])
        previous = V[t + 1] [previous] ["prev"]

    print ("The steps of states are " + " ".join(opt) + " with highest probability of %s" % max_prob)

def dptable(V):
    # Print a table of steps from dictionary
    yield " " * 5 + "     ".join(("%3d" % i) for i in range(len(V)))
    for state in V[0]:
        yield "%.7s: " % state + " ".join("%.7s" % ("%lf" % v[state] ["prob"]) for v in V)