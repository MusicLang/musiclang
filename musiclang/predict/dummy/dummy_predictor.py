import musiclang
from ..base.predictor import BasePredictor


class DummyPredictor(BasePredictor):
    """
    Create a transformer model to predict chord progression model of a given score
    """
    def init_model(self, *args, **kwargs):
        from ..models.transformer_model import TransformerModelWrapper
        from .dummy_tokenizer import TOKENS

        return None


    def save_model(self, filepath):
        self.model.save_model(filepath)

    @classmethod
    def load_model(cls, filepath, *args, **kwargs):
        from ..models.transformer_model import TransformerModelWrapper
        predictor = cls(*args, **kwargs)
        predictor.model = TransformerModelWrapper.load_model(filepath)
        return predictor

    def predict_from_text(self, start_text, temperature=0, include_start=True, n_tokens=5, max_tokens=None):
        DEFAULT_START_TEXT = '(I%I.M)(V__0=r)'
        if max_tokens is None:
            max_tokens = 3 * n_tokens
        if n_tokens >= max_tokens:
            raise ValueError('"n_tokens" should be less than "max_tokens"')
        chars = ''
        last_valid_candidate = None
        last_chord_text = start_text
        prepend_text = '' if not include_start else start_text
        while True:
            from .dummy_tokenizer import get_candidates_idx, get_is_terminal
            is_terminal = get_is_terminal(last_chord_text)
            if is_terminal and (len(chars) - len(start_text)) >= n_tokens:
                return prepend_text + chars
            elif is_terminal:
                last_chord_text = DEFAULT_START_TEXT
                last_valid_candidate = chars
            elif len(chars) > max_tokens:
                print(start_text)
                if last_valid_candidate is None:
                    raise Exception('Not able to predict a sentence, try increase the "max_tokens" parameter')
                return prepend_text + last_valid_candidate

            import numpy as np
            from .dummy_tokenizer import TOKENIZER
            temperature_vec = temperature * np.random.randn(len(TOKENIZER))
            valid_candidates = get_candidates_idx(last_chord_text)
            serie = np.argmax((valid_candidates + temperature_vec)).tolist()
            text = self.untokenize([serie])
            chars += text
            start_text += text
            last_chord_text += text

        return chars

    def score_to_text(self, score: 'musiclang.Score') -> str:
        from .dummy_tokenizer import score_to_text
        return score_to_text(score)

    def tokenize(self, text):
        """
        Convert a text to a list of tokens (number)
        :param text:
        :return:
        """
        from .dummy_tokenizer import tokenize_string
        tokens = tokenize_string(text)
        return tokens

    def untokenize(self, tokens):
        """
        Convert a list of tokens to a text
        :param tokens:
        :return:
        """
        from .dummy_tokenizer import untokenize
        return untokenize(tokens)

    def text_to_score(self, text):
        """
        :param text:
        :return:
        """
        from musiclang.core.library import I, II, III, IV, V, VI, VII, s0, s1, s2, s3, s4, s5, s6, \
            h0, h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11, l, r

        # First make sure it compiles in musiclang code
        from .dummy_tokenizer import PARSER
        print(text)
        if not text.endswith(';'):
            text += ';'
        parsed = PARSER.parse(text)
        # Remove doubled voices names

        text = text.replace(';', '')
        score = eval(text)
        return score
