import musiclang
# Base predictor
from .model import ModelWrapper

class BasePredictor:

    def __init__(self, *args, **kwargs):
        self.model: 'ModelWrapper' = self.init_model(*args, **kwargs)


    ## BASE METHODS

    def train(self, train_scores, eval_scores, epochs=10, **kwargs):
        # Convert scores
        train_data = self.scores_to_tokens(train_scores)
        eval_data = self.scores_to_tokens(eval_scores)
        self.model.train(train_data, eval_data, epochs=epochs, **kwargs)

    def predict_proba(self, tokens):
        return self.model.predict(tokens).squeeze(1)[-1]

    def predict(self, text, output='score', include_start=True, n_tokens=5, max_tokens=None, **kwargs):
        """

        :param text: Input on which to predict (If it is a score it will be converted to a text first)
        :param output: str, Either text or score
        :param include_start: boolean
        :param n_tokens: int, Number of additional tokens to predict, it can be more if the predicted score cannot be compiled
        :param max_tokens: int, If nb tokens generated > max_tokens, then returns the last valid generated text
        :param kwargs:
        :return:
        """
        if not isinstance(text, str):
            text = self.score_to_text(text).replace(';', '')

        result_text = self.predict_from_text(text, include_start=include_start, n_tokens=n_tokens,
                                        max_tokens=max_tokens, **kwargs)

        if output == 'score':
            return self.text_to_score(result_text)
        elif output == 'text':
            return result_text
        else:
            raise ValueError('Wrong output value :  {}. It should be "score" or "text" '.format(output))


    def save_model(self, filepath):
        raise NotImplemented

    @classmethod
    def load_model(self, filepath):
        raise NotImplemented

    def predict_to_score(self, text, **kwargs):
        return self.text_to_score(text + self.predict(text, **kwargs))

    def predict_score(self, score, **kwargs):
        text = self.score_to_text(score)
        return self.predict(text, **kwargs)

    def scores_to_tokens(self, scores):
        return sum([self.score_to_tokens(score) for score in scores], [])

    def score_to_tokens(self, score):
        return self.tokenize(self.score_to_text(score))

    def tokens_to_score(self, tokens):
        return self.text_to_score(self.untokenize(tokens))

    ## METHODS TO OVERRIDE
    def predict_next_token(self):
        raise NotImplemented

    def predict_from_text(self, start_text, include_start=True, n_tokens=5, max_tokens=None):
        raise NotImplemented

    def init_model(self, *args, **kwargs):
        raise NotImplemented

    def score_to_text(self, score: 'musiclang.Score') -> str:
        raise NotImplemented

    def tokenize(self, text):
        raise NotImplemented

    def untokenize(self, tokens):
        raise NotImplemented

    def text_to_score(self, text):
        raise NotImplemented