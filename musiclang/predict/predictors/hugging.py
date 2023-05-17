

_TOKENIZER = None
_MODEL = None
_GPU = False
_DEVICE = None
def _load_models():
    global _TOKENIZER, _MODEL, _GPU, _DEVICE
    from transformers import GPT2LMHeadModel, GPT2TokenizerFast
    import torch
    if _TOKENIZER is not None:
        return _TOKENIZER, _MODEL
    hub_model_path = "floriangardin/musiclang"
    TOKENIZER = GPT2TokenizerFast.from_pretrained(hub_model_path, padding_side='left')
    MODEL = GPT2LMHeadModel.from_pretrained(hub_model_path)
    _GPU = torch.cuda.is_available()
    _DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    if _GPU:
        MODEL = MODEL.to('cuda')
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




def generate_one_chord(input_text, model, tokenizer,
                                 max_length=100, temperature=0.7,
                                 top_k=20,
                                 target_sequence=')+('):
    # Tokenize the input text
    import torch
    block_size = 1024
    input_ids = tokenizer.encode(input_text, return_tensors='pt').to(_DEVICE)
    target_ids = tokenizer.encode(target_sequence)

    target_length = len(target_ids)
    start_length = len(input_ids[0])

    # split between block size and predicted sequence
    # Divide start_length between block_size - max_length
    end_ids = input_ids[:, -(block_size-max_length):]
    start_ids = input_ids[:, :-(block_size-max_length)]
    assert len(end_ids[0]) + len(start_ids[0]) == start_length
    idx = 0
    while True:
        # Generate text with the model
        idx += 1
        end_ids = model.generate(
            end_ids,
            max_new_tokens=max_length,
            num_return_sequences=1,
            do_sample=True,
            temperature=temperature,
            top_k=top_k,
            bad_words_ids=[[tokenizer.eos_token_id]],
            pad_token_id=tokenizer.eos_token_id,
        )

        output = torch.cat((start_ids, end_ids), 1)
        end_ids = output[:, -(block_size - max_length):]
        start_ids = output[:, :-(block_size - max_length)]
        # Decode the generated text
        output_text = tokenizer.decode(output[0], skip_special_tokens=False)
        output_text = output_text.replace(tokenizer.eos_token, '+')
        if output_text.startswith('+'):
            output_text = output_text[1:]
        if target_sequence in output_text[start_length+target_length:]:
            output_text = target_sequence.join(output_text.split(target_sequence)[:-1]) + ')'
            return output_text


import re


def deduplicate_chord_instruments(text):
    # Split the text into parts
    parts = re.split('([a-zA-Z0-9_]+=)', text)

    # Create a new list to hold the modified parts
    modified_parts = []

    # Keep track of the keys we've seen
    seen_keys = {}

    # Process each part
    for part in parts:
        if part.endswith('='):
            # This part is a key, check if we've seen it before
            key = part[:-1]  # remove the '='
            ins, idx = key.split('__')
            idx = int(idx)
            modified_key = None
            if (ins, idx) in seen_keys:
                # We've seen this key before, append a unique identifier
                while (ins, idx) in seen_keys:
                    ind, idx = ins, idx + 1
                    modified_key = ins + '__' + str(idx)

                seen_keys[(ins, idx)] = True
            else:
                # This is a new key, add it to the dictionary
                modified_key = key
                seen_keys[(ins, idx)] = True

            # Add the modified key to the list
            modified_parts.append(modified_key + '=')
        else:
            # This part is not a key, just add it to the list
            modified_parts.append(part)

    # Join the parts back together and return
    return ''.join(modified_parts)


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
        chords = text.split(')+(')
        chords[-1] = deduplicate_chord_instruments(chords[-1])
        text = ')+('.join(chords)
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
