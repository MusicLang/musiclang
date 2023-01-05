import gensim
import numpy as np
import re
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
# Create a simple parametrable chord prediction algorithm


class WindowedPredictor:
    """
    Simple next word predictor using a context window
    - using a Word2Vec embeding
    - A random forest regressor trained on a embedded chord window of size memory to predict the next chord embeding
    - The predicted chord will be the closest vector in the Word2Vec space
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
        self.wv = None
        self.config = config
        self.vector_size = vector_size
        self.memory = memory
        self.window = window
        self.encoder = LabelEncoder()


    def save(self, filepath):
        import joblib
        joblib.dump(self, filepath)

    @classmethod
    def load(cls, filepath):
        import joblib
        return joblib.load(filepath)

    def cross_val_score(self, data, **kwargs):
        """
        Return the cross val scores of this model using the data provided
        :param data:
        :param kwargs: arguments that will be passed to sklearn.model_selection.cross_val_score
        :return:
        """
        from sklearn.model_selection import cross_val_score
        from sklearn.metrics import make_scorer
        X, Y = self.transform(data, **kwargs)
        y = self.encoder.fit_transform(Y)
        scorer = 'accuracy'
        return cross_val_score(self.clf, X, y, scoring=scorer, **kwargs)

    def filter(self, data):
        """
        Filter some data by default before training, it can help to reduce the vocab size
        :param data:
        :return:
        """
        return data

    def train_embeding(self, data):
        # Pad with START TOKEN
        data = [['START'] * self.memory + self.filter(d) for d in data]  # Pad with a start token
        model = gensim.models.Word2Vec(data, min_count=1, vector_size=self.vector_size, window=self.window)
        self.wv = model.wv
        data_transformed = [[self.wv[chord] for chord in song] for song in data]
        return data_transformed, data

    def fit(self, data):
        X, Y = self.transform(data)
        y = self.encoder.fit_transform(Y)
        self.clf.fit(X, y)
        return self

    def transform(self, data):
        from sklearn.utils import shuffle
        data_transformed, filtered_data = self.train_embeding(data)
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

    def predict(self, sequence, topn=None):
        """

        Parameters
        ----------
        sequence : List[str]
                   Sequence of previous tokens on which to predict the next token
        topn :     int | None, optional
                   If topn is None, then returns the highest score prediction
                   Otherwise returns the list of top-n ranked predicted tokens (highest first)

        Returns
        -------
        token_result : str or List[str]
                       The predicted token if topn=None else the top-n ranked prediction (highest first)
        Examples
        --------

        >>> from musiclang.predict.predictors import WindowedPredictor
        >>> from musiclang.write.library import *
        >>> from musiclang.predict.tokenizers import ChordTokenizer
        >>> tokenizer = ChordTokenizer()
        >>> predictor = WindowedPredictor.load("ChordPredictor")
        >>> chord_progression = (I % I.M) + (VI['6'] % I.M) + (II['2'] % I.M)
        >>> chord_tokens = tokenizer.tokenize(chord_progression)
        >>> predictor.predict(chord_tokens)
        (V['65'] % I.M)

        """
        import numpy as np
        if len(sequence) < self.memory:
            to_fill = self.memory - len(sequence)
            sequence = ['START'] * to_fill + sequence

        data = np.asarray([self.wv[s] for s in sequence[-self.memory:]]).ravel()
        # Classification
        prediction = self.clf.predict_proba([data])[0]
        #temp_vec = temperature * np.random.randn(*prediction.shape)
        #prediction += temp_vec
        prediction = np.argmax(prediction)
        token_result = self.encoder.inverse_transform([prediction])[0]
        return token_result



class MelodyPredictor(WindowedPredictor):

    def filter(self, data):
        return [d for d in data if 'augment' not in d]