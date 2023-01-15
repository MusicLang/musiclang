from hashlib import sha256
from struct import unpack
import numpy as np

def bytes_to_float(b):
    return float(unpack('L', sha256(b).digest()[:8])[0]) / 2**64


def random_permutation(chars, array, seed="", root=""):
    """
    Generate a permutation of size n following a bytes encoding
    if chars,seed,root,proba is the same it always generates the same output
    Algorithm : Fisher Yates shuffle  : https://en.wikipedia.org/wiki/Random_permutation#:~:text=A%20simple%20algorithm%20to%20generate,has%20index%200%2C%20and%20the
    :param array: array to shuffle
    :param seed:
    :param root:
    :return:
    """
    n = len(array)
    for i in range(n - 1):
        j = i + random_int(chars + str(i), low=0, high=n - i, seed=seed, root=root)
        z = array[i]
        array[i] = array[j]
        array[j] = z

    return array


def random_boolean(chars, seed="", root="", proba=0.2):
    """
    Generate a random boolean following a bytes encoding
    if chars,seed,root,proba is the same it always generates the same output
    :param seed:
    :param root:
    :param chars:
    :param proba:
    :return:
    """
    text = f'{chars}{seed}{root}'
    text = bytes(text, encoding='utf-8')
    return bytes_to_float(text) < proba


def random_int(chars, low, high, seed="", root=""):
    """
    Generate an integer between low and high following a bytes encoding
    if chars,seed,root,proba is the same it always generates the same output
    :param chars:
    :param low:
    :param high:
    :param seed:
    :param root:
    :return:
    """
    return int(random_float(chars, low, high, seed=seed, root=root))


def random_float(chars, low, high, seed="", root=""):
    """
    Generate a float between low and high following a bytes encoding
    if chars,seed,root,proba is the same it always generates the same output
    :param chars:
    :param low:
    :param high:
    :param seed:
    :param root:
    :return:
    """
    text = f'{chars}{seed}{root}'
    text = bytes(text, encoding='utf-8')
    return (high - low) * bytes_to_float(text) + low

def init_seed(seed):
    if seed is None:
        return np.random.randint(0, 2 ** 31)
    else:
        return seed


def random_choice(array, chars, seed="", root=""):
    return array[random_int(chars, 0, len(array), seed=seed, root=root)]