from musiclang.library import *
from musiclang import Tonality
import time
import numpy as np


def generate_harmony(nb_bars, tonality, arranger, time_signature=(4, 4), temperature=0.02):
    bar_duration = 4 * frac(time_signature[0], time_signature[1])

    def random_melody_note(proba_scale=0.8):
        scale = np.random.random() < proba_scale
        if scale:
            val = np.random.randint(0, 7)
            note = s0.set_duration(bar_duration)
        else:
            val = np.random.randint(0, 12)
            note = h0.set_duration(bar_duration)
        note.val = val
        return note

    random_melody = sum([random_melody_note() for i in range(nb_bars)], None)
    harmony = melody_to_harmony(random_melody, tonality, arranger, time_signature=time_signature, temperature=temperature)

    return harmony


def harmony_to_melody(harmony, tonality):
    """
    Given a harmony text and a tonality returns a one note per chord melody relative to the tonality
    """
    from musiclang import ScoreFormatter, VoiceLeading
    chords = ScoreFormatter(harmony).parse()

    rules = VoiceLeading.RULES
    score = VoiceLeading(
        # fixed_voices=['piano__0'],
        voicing=[b0.o(-1), b2.o(-1), b0, b1],
        # exclude_rules=[rules.CROSSING, rules.UNISSON]
    )(chords)
    instr = 'piano__3'
    base_chord = (I % Tonality.from_str(tonality))
    melody = sum([chord.score[instr].to_absolute_note(chord).to_standard_note(base_chord) for chord in score], None)
    return melody


ORNEMENTATIONS = ['suspension_prev', 'suspension_prev_repeat', 'interpolate'
                  ]
INTERPOLATE = ['interpolate']


def auto_enrich_melody(melody, proba_enrich=1.0):
    new_melody = None
    for note in melody.notes:
        random_number = np.random.random()
        if random_number < proba_enrich:
            second_random_number = np.random.random()
            if second_random_number < 0.2:
                new_note = note.add_tag(np.random.choice(ORNEMENTATIONS))
            elif note.duration >= 0.5:
                new_note = note.add_tag(np.random.choice(INTERPOLATE))
            else:
                new_note = note.copy()
        else:
            new_note = note.copy()

        new_melody += new_note

    return new_melody


def melody_to_harmony(melody, tonality, arranger, time_signature=(4, 4), temperature=0.02):
    """
    Given a one note per chord melody, tonality and time signature, returns a harmony
    """

    def get_real_value(time_signature, beat, duration):
        CONVENTION_DICT = {(6, 8): 2, (2, 2): 2}
        nb_beats = CONVENTION_DICT.get(time_signature, duration)
        ratio = frac(nb_beats, 1) / duration

        return float((beat) * ratio) + 1

    from fractions import Fraction as frac
    melody_arranger = [[(note, 1)] for note in melody.notes]
    chord_progression = arranger.arrange(melody_arranger, tonality, temperature=temperature)
    # Convert to harmony grid
    bar_duration = 4 * frac(time_signature[0], time_signature[1])
    text = [f"Time Signature : {time_signature[0]}/{time_signature[1]}",
            f"Tonality : {tonality}"]
    current_bar_idx = 0
    current_beat = 0
    time = 0
    current_text = f"m{current_bar_idx}"
    for note, chord in zip(melody.notes, chord_progression):
        bar_idx = time // bar_duration
        if bar_idx != current_bar_idx:
            text.append(current_text)
            current_text = f"m{bar_idx}"
            current_bar_idx = bar_idx

        beat = time % bar_duration
        if beat != 0:
            real_beat = get_real_value(time_signature, beat, bar_duration)
            current_text += " b{:1.2f}".format(real_beat)

        current_text += f" {chord}"
        time += note.duration

    text.append(current_text)

    return "\n".join(text)



def compose_melody_and_harmony(tonality, nb_bars, arranger,
                               time_signature=(4, 4), temperature=0.02,
                               enrich_melody=False,
                               proba_enrich_melody=0.5
                               ):

    harmony = generate_harmony(nb_bars, tonality, arranger, time_signature=time_signature, temperature=temperature)
    new_melody = harmony_to_melody(harmony, tonality)
    new_harmony = melody_to_harmony(new_melody, tonality, arranger, time_signature=time_signature, temperature=temperature)
    if enrich_melody:
        new_melody = auto_enrich_melody(new_melody, proba_enrich=proba_enrich_melody)

    return new_melody, new_harmony