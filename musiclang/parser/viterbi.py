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