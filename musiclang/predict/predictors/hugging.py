

_TOKENIZER = None
_MODEL = None

def _load_models():
    global _TOKENIZER, _MODEL
    from transformers import GPT2LMHeadModel, GPT2TokenizerFast
    if _TOKENIZER is not None:
        return _TOKENIZER, _MODEL
    hub_model_path = "floriangardin/musiclang"
    TOKENIZER = GPT2TokenizerFast.from_pretrained(hub_model_path)
    MODEL = GPT2LMHeadModel.from_pretrained(hub_model_path)
    _TOKENIZER = TOKENIZER
    _MODEL = MODEL

    return TOKENIZER, MODEL



def preprocess(prompt, tokenizer):
    """
    Preprocess the prompt stripping spaces, line return and tabulations
    Parameters
    ----------
    prompt

    Returns
    -------

    """
    prompt = prompt.replace(' ', '').replace('\t', '').replace('\r', '').replace('\n', '')
    prompt = tokenizer.eos_token + prompt
    return prompt

import torch



def generate_one_chord(input_text, model, tokenizer,
                                 max_length=100, temperature=0.7,
                                 top_k=20,
                                 target_sequence=')+('):
    # Tokenize the input text
    input_ids = tokenizer.encode(tokenizer.eos_token + input_text, return_tensors='pt')
    target_ids = tokenizer.encode(target_sequence)
    target_length = len(target_ids)
    start_length = len(input_ids[0])
    output = input_ids
    while True:
        # Generate text with the model
        output = model.generate(
            output,
            max_new_tokens=max_length,
            num_return_sequences=1,
            do_sample=True,
            temperature=temperature,
            top_k=top_k,
            pad_token_id=tokenizer.eos_token_id,
        )

        # Decode the generated text
        output_text = tokenizer.decode(output[0], skip_special_tokens=True)
        if target_sequence in output_text[start_length+target_length:]:
            output_text = target_sequence.join(output_text.split(target_sequence)[:-1]) + ')'
            return output_text




def generate_n_chords(text, model, tokenizer, n, **kwargs):
    """
    Generate n chords from a text prompt
    Parameters
    ----------
    text: str
    model: GPT2LMHeadModel

    tokenizer: GPT2TokenizerFast
    n: int
        The number of chords to generate


    Returns
    -------
    text: str
        The generated text
    """
    for i in range(n):
        text = generate_one_chord(text, model, tokenizer, **kwargs)
    return text

def predict_score_from_huggingface(prompt, n_chords=1, temperature=0.75, top_k=20):
    """
    Given a text prompt, generate a score using the huggingface model

    Parameters
    ----------
    prompt: str
        The text prompt
    n_chords: int
        The number of chords to generate
    temperature: float
        The temperature of the generation, the higher the more random, usually don't go over 1.0 to avoid syntax errors
    top_k: int
        The number of top k tokens to consider when generating the next token


    Returns
    -------
    result: str
        The generated text score
    """


    TOKENIZER, MODEL = _load_models()

    prompt = preprocess(prompt, TOKENIZER)


    return generate_n_chords(prompt, MODEL, TOKENIZER, n_chords, temperature=temperature, top_k=top_k)
