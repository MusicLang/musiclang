import musiclang
# Base predictor
from .model import ModelWrapper

class BasePredictor:
    """ """

    def __init__(self, *args, **kwargs):
        self.model: 'ModelWrapper' = self.init_model(*args, **kwargs)


    ## BASE METHODS

    def train(self, train_scores, eval_scores, epochs=10, tokenize=True, **kwargs):
        """

        Parameters
        ----------
        train_scores :
            
        eval_scores :
            
        epochs :
             (Default value = 10)
        tokenize :
             (Default value = True)
        **kwargs :
            

        Returns
        -------

        """
        # Convert scores
        # If already scores
        if tokenize:
            train_data = self.scores_to_tokens(train_scores)
            eval_data = self.scores_to_tokens(eval_scores)
        else:
            train_data = train_scores
            eval_data = eval_scores
        self.model.train(train_data, eval_data, epochs=epochs, **kwargs)

    def predict_proba(self, tokens):
        """

        Parameters
        ----------
        tokens :
            

        Returns
        -------

        """
        return self.model.predict(tokens).squeeze(1)[-1]

    def predict(self, text, output='score', temperature=0, include_start=True, n_tokens=5, max_tokens=None, **kwargs):
        """

        Parameters
        ----------
        text :
            Input on which to predict (If it is a score it will be converted to a text first)
        output :
            str, Either text or score (Default value = 'score')
        include_start :
            boolean (Default value = True)
        n_tokens :
            int, Number of additional tokens to predict, it can be more if the predicted score cannot be compiled (Default value = 5)
        max_tokens :
            int, If nb tokens generated > max_tokens, then returns the last valid generated text (Default value = None)
        kwargs :
            return:
        temperature :
             (Default value = 0)
        **kwargs :
            

        Returns
        -------

        """
        if not isinstance(text, str):
            text = self.score_to_text(text).replace(';', '')

        result_text = self.predict_from_text(text, temperature=temperature, include_start=include_start, n_tokens=n_tokens,
                                        max_tokens=max_tokens, **kwargs)

        if output == 'score':
            return self.text_to_score(result_text)
        elif output == 'text':
            return result_text
        else:
            raise ValueError('Wrong output value :  {}. It should be "score" or "text" '.format(output))


    def save_model(self, filepath):
        """

        Parameters
        ----------
        filepath :
            

        Returns
        -------

        """
        raise NotImplemented

    @classmethod
    def load_model(self, filepath):
        """

        Parameters
        ----------
        filepath :
            

        Returns
        -------

        """
        raise NotImplemented

    def predict_to_score(self, text, **kwargs):
        """

        Parameters
        ----------
        text :
            
        **kwargs :
            

        Returns
        -------

        """
        return self.text_to_score(text + self.predict(text, **kwargs))

    def predict_score(self, score, **kwargs):
        """

        Parameters
        ----------
        score :
            
        **kwargs :
            

        Returns
        -------

        """
        text = self.score_to_text(score)
        return self.predict(text, **kwargs)

    def scores_to_tokens(self, scores):
        """

        Parameters
        ----------
        scores :
            

        Returns
        -------

        """
        return sum([self.score_to_tokens(score) for score in scores], [])

    def score_to_tokens(self, score):
        """

        Parameters
        ----------
        score :
            

        Returns
        -------

        """
        # If already text do nothing else convert to text and tokenize
        if isinstance(score, str):
            return self.tokenize(score)
        return self.tokenize(self.score_to_text(score))

    def tokens_to_score(self, tokens):
        """

        Parameters
        ----------
        tokens :
            

        Returns
        -------

        """
        return self.text_to_score(self.untokenize(tokens))

    ## METHODS TO OVERRIDE
    def predict_next_token(self):
        """ """
        raise NotImplemented

    def predict_from_text(self, start_text, authorized_tokens=None,
                          temperature=0, include_start=True, n_tokens=5, max_tokens=None, **kwargs):
        """

        Parameters
        ----------
        start_text :
            
        authorized_tokens :
             (Default value = None)
        temperature :
             (Default value = 0)
        include_start :
             (Default value = True)
        n_tokens :
             (Default value = 5)
        max_tokens :
             (Default value = None)
        **kwargs :
            

        Returns
        -------

        """
        raise NotImplemented

    def init_model(self, *args, **kwargs):
        """

        Parameters
        ----------
        *args :
            
        **kwargs :
            

        Returns
        -------

        """
        raise NotImplemented

    def score_to_text(self, score: 'musiclang.Score') -> str:
        """

        Parameters
        ----------
        score: 'musiclang.Score' :
            

        Returns
        -------

        """
        raise NotImplemented

    def tokenize(self, text):
        """

        Parameters
        ----------
        text :
            

        Returns
        -------

        """
        raise NotImplemented

    def untokenize(self, tokens):
        """

        Parameters
        ----------
        tokens :
            

        Returns
        -------

        """
        raise NotImplemented

    def text_to_score(self, text):
        """

        Parameters
        ----------
        text :
            

        Returns
        -------

        """
        raise NotImplemented