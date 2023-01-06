import numpy as np
import re
import itertools
from sklearn.linear_model import LinearRegression
from sklearn.metrics import make_scorer
from sklearn.preprocessing import LabelEncoder
# Create a simple parametrable chord prediction algorithm


REGEX_CHORD = re.compile(r"(I|II|III|IV|V|VI|VII)(\[('7'|'6'|'64'|'65'|'43'|'2')\]|) % ((I|II|III|IV|V|VI|VII)(.[s|b|])?.[m|mm|M])")

DEGREES = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']
ACCIDENTS = ['', '.b', '.s']
MODES = ['m', 'mm', 'M']
EXTENSIONS = ["['6']", "['64']", "['65']", "['43']", "['2']", "['7']"]
TONALITIES = [f"{degree}{accident}.{mode}" for degree, accident, mode in itertools.product(DEGREES, ACCIDENTS, MODES)]

from sklearn_hierarchical_classification.classifier import HierarchicalClassifier
from sklearn_hierarchical_classification.constants import ROOT

LEVEL_2 = {tone: [f"{degree} {tone}" for degree in DEGREES] for tone in TONALITIES}
ALL_LEVEL_2 = np.ravel([val for key, val in LEVEL_2.items()]).tolist()
LEVEL_3 = {val: [f"({val.split(' ')[0]}{extension} % {val.split(' ')[1]})" for extension in EXTENSIONS] for val in ALL_LEVEL_2}

class_hierarchy = {
        ROOT: TONALITIES,
        **LEVEL_2,
        **LEVEL_3
    }


def reconstruct_chord(degree, extension, tonality):
    """

    Parameters
    ----------
    degree :
        
    extension :
        
    tonality :
        

    Returns
    -------

    """
    return f"({degree}{extension} % {tonality})"


def get_chord_characs(chord):
    """

    Parameters
    ----------
    chord :
        

    Returns
    -------

    """
    result = re.findall(REGEX_CHORD, chord)
    if len(result) == 0:
        return '', '', ''
    degree, extension, _, tonality, _, _ = result[0]
    return degree, extension, tonality

def scorer_func(y_true, y_pred):
    """

    Parameters
    ----------
    y_true :
        
    y_pred :
        

    Returns
    -------

    """
    return np.mean(np.min((y_pred == y_true), axis=1))

class HierarchicalChordPredictor:
    """Hierarchical classifier for next chord prediction
    - using a Word2Vec embeding
    - A random forest regressor trained on a embedded chord window of size memory to predict the next chord embeding
    - The predicted chord will be the closest vector in the Word2Vec space

    Parameters
    ----------

    Returns
    -------

    """
    _vector_size = 10
    _window = 3
    _memory = 4

    def __init__(self, clf, vector_size=_vector_size, window=_window, memory=_memory, **config):
        """

        :param clf:
        :param vector_size: int, Size of Word2Vec embedding (default=3)
        :param window: int, Window size used for Word2Vec, (default=3)
        :param memory: int, How much tokens are used to predict the next one (default)
        :param config: Other parameters
        """
        self.clf = clf
        self.config = config
        self.vector_size = vector_size
        self.memory = memory
        self.window = window
        self.encoder = LabelEncoder()
        self.encoder_degree = LabelEncoder()
        self.encoder_extension = LabelEncoder()
        self.encoder_tonality = LabelEncoder()

    def cross_val_score(self, data, **kwargs):
        """Return the cross val scores of this model using the data provided

        Parameters
        ----------
        data :
            param kwargs: arguments that will be passed to sklearn.model_selection.cross_val_score
        **kwargs :
            

        Returns
        -------

        """
        from sklearn.model_selection import cross_val_score
        X, Y = self.transform(data, **kwargs)
        y = self.encoder.fit_transform(Y)
        scorer = make_scorer(scorer_func)
        #y = [self.get_feature_vector(chord) for chord in Y]
        return cross_val_score(self.clf, X, y, scoring='accuracy', **kwargs)


    def filter(self, data):
        """Filter some data by default before training, it can help to reduce the vocab size

        Parameters
        ----------
        data :
            return:

        Returns
        -------

        """
        return data


    def get_feature_vector(self, chord):
        """

        Parameters
        ----------
        chord :
            

        Returns
        -------

        """
        degree, extension, tonality = get_chord_characs(chord)

        return [self.encoder_degree.transform([degree])[0],
                self.encoder_extension.transform([extension])[0],
                self.encoder_tonality.transform([tonality])[0]]

    def preprocess(self, data):
        """

        Parameters
        ----------
        data :
            

        Returns
        -------

        """
        self.encoder_degree.fit(DEGREES + [''])
        self.encoder_extension.fit(EXTENSIONS + [''])
        self.encoder_tonality.fit(TONALITIES + [''])
        # Pad with START TOKEN
        data = [['START'] * self.memory + self.filter(d) for d in data]  # Pad with a start token
        data_transformed = [[self.get_feature_vector(chord) for chord in song] for song in data]
        return data_transformed, data


    def fit(self, data):
        """

        Parameters
        ----------
        data :
            

        Returns
        -------

        """
        X, Y = self.transform(data)
        y = self.encoder.fit_transform(Y)
        #y = [self.get_feature_vector(chord) for chord in Y]
        self.clf.fit(X, y)
        return self

    def transform(self, data):
        """

        Parameters
        ----------
        data :
            

        Returns
        -------

        """
        from sklearn.utils import shuffle
        data_transformed, filtered_data = self.preprocess(data)
        # Create X, Y dataset
        X = [np.asarray(song[chord_idx:chord_idx + self.memory]).ravel() for song in data_transformed
             for chord_idx, chord in enumerate(song[self.memory:])
             ]

        Y = [song[chord_idx + self.memory] for song in filtered_data for chord_idx, chord in
             enumerate(song[self.memory:])]
        X = np.asarray(X)
        Y = np.asarray(Y)
        X, Y = shuffle(X, Y)
        return X, Y

    def predict(self, sequence, temperature=0):
        """

        Parameters
        ----------
        sequence :
            
        temperature :
             (Default value = 0)

        Returns
        -------

        """
        import numpy as np
        if len(sequence) < self.memory:
            to_fill = self.memory - len(sequence)
            sequence = ['START'] * to_fill + sequence

        data = np.asarray([self.get_feature_vector(s) for s in sequence[-self.memory:]]).ravel()

        prediction = self.clf.predict([data])[0]
        #temp_vec = temperature * np.random.randn(*prediction.shape)
        #prediction += temp_vec
        #prediction = np.argmax(prediction)
        res = self.encoder.inverse_transform([prediction])[0]
        return res

