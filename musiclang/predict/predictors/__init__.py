from .windowed import WindowedPredictor, MelodyPredictor
from .hugging import predict_score_from_huggingface
from .transformer import predict, predict_melody, predict_with_fixed_instruments, \
    predict_with_fixed_instruments_no_prompt, predict_with_template