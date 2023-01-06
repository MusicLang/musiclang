import musiclang
from ..base.predictor import BasePredictor


class ScoreTransformerPredictor(BasePredictor):
    """Create a transformer model to predict chord progression model of a given score"""
    def init_model(self, *args, lr=2, sc=0.95, **kwargs):
        """

        Parameters
        ----------
        *args :
            
        lr :
             (Default value = 2)
        sc :
             (Default value = 0.95)
        **kwargs :
            

        Returns
        -------

        """
        from ..models.transformer_model import TransformerModelWrapper
        from .score_tokenizer import TOKENS
        n_tokens = len(TOKENS)  # size of vocabulary
        d_model = 100 # embedding dimension
        d_hid = 500  # dimension of the feedforward network model in nn.TransformerEncoder
        n_layers = 3  # number of nn.TransformerEncoderLayer in nn.TransformerEncoder
        n_head = 10  # number of heads in nn.MultiheadAttention
        dropout = 0.2  # dropout probability
        batch_size = 128
        bptt = 100
        lr = lr
        sc = sc
        return TransformerModelWrapper(n_tokens, d_model, n_head,  d_hid, n_layers, bptt, batch_size, lr, sc, dropout=dropout)


    def save_model(self, filepath):
        """

        Parameters
        ----------
        filepath :
            

        Returns
        -------

        """
        self.model.save_model(filepath)

    @classmethod
    def load_model(cls, filepath, *args, **kwargs):
        """

        Parameters
        ----------
        filepath :
            
        *args :
            
        **kwargs :
            

        Returns
        -------

        """
        from ..models.transformer_model import TransformerModelWrapper
        predictor = cls(*args, **kwargs)
        predictor.model = TransformerModelWrapper.load_model(filepath)
        return predictor

    def predict_from_text(self, start_text, authorized_tokens=None, temperature=0, include_start=True, n_tokens=5, max_tokens=None, **kwargs):
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
        DEFAULT_START_TEXT = '(I%I.M)(V__0=r)'
        if max_tokens is None:
            max_tokens = 3 * n_tokens
        if n_tokens >= max_tokens:
            raise ValueError('"n_tokens" should be less than "max_tokens"')
        chars = ''
        last_valid_candidate = None
        last_chord_text = start_text
        tokens = self.tokenize(start_text)
        prepend_text = '' if not include_start else start_text
        while True:
            from .score_tokenizer import get_candidates_idx, get_is_terminal
            is_terminal = get_is_terminal(last_chord_text)
            if is_terminal and (len(chars) - len(start_text)) >= n_tokens:
                return prepend_text + chars
            elif is_terminal:
                last_chord_text = DEFAULT_START_TEXT
                last_valid_candidate = chars
            elif len(chars) > max_tokens:
                if last_valid_candidate is None:
                    raise Exception('Not able to predict a sentence, try increase the "max_tokens" parameter')
                return prepend_text + last_valid_candidate

            import numpy as np
            from .score_tokenizer import TOKENIZER
            temperature_vec = temperature * np.random.randn(len(TOKENIZER))
            output = self.predict_proba(tokens)
            valid_candidates = get_candidates_idx(last_chord_text)
            if np.max(valid_candidates) < 0:
                raise Exception('Cannot create a score with these constraints, try ading new authorized tokens')
            serie = (output.cpu() + valid_candidates + temperature_vec).argmax().tolist()
            text = self.untokenize([serie])
            chars += text
            start_text += text
            last_chord_text += text
            tokens = self.tokenize(start_text)

    def score_to_text(self, score: 'musiclang.Score') -> str:
        """

        Parameters
        ----------
        score: 'musiclang.Score' :
            

        Returns
        -------

        """
        from .score_tokenizer import score_to_text
        return score_to_text(score)

    def tokenize(self, text):
        """Convert a text to a list of tokens (number)

        Parameters
        ----------
        text :
            return:

        Returns
        -------

        """
        from .score_tokenizer import tokenize_string
        tokens = tokenize_string(text)
        return tokens

    def untokenize(self, tokens):
        """Convert a list of tokens to a text

        Parameters
        ----------
        tokens :
            return:

        Returns
        -------

        """
        from .score_tokenizer import untokenize
        return untokenize(tokens)

    def text_to_score(self, text):
        """

        Parameters
        ----------
        text :
            return:

        Returns
        -------

        """
        from musiclang.write.library import I, II, III, IV, V, VI, VII, s0, s1, s2, s3, s4, s5, s6, \
            h0, h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11, l, r

        # First make sure it compiles in musiclang code
        from .score_tokenizer import PARSER
        if not text.endswith(';'):
            text += ';'
        parsed = PARSER.parse(text)
        # Remove doubled voices names

        text = text.replace(';', '').replace('\n', '')
        score = eval(text)
        return score