from music21 import note, stream, metadata, meter, tie, dynamics
import music21
from musiclang import Chord


MUSESCORE_REPLACE_DICT = {
    'French horn': 'Horns in F'
}


SCALES_MAJOR = {
    0: ['C', 'D', 'E', 'F', 'G', 'A', 'B'],
    1: ['Db', 'Eb', 'F', 'Gb', 'Ab', 'Bb', 'C'],
    2: ['D', 'E', 'F#', 'G', 'A', 'B', 'C#'],
    3: ['Eb', 'F', 'G', 'Ab', 'Bb', 'C', 'D'],
    4: ['E', 'F#', 'G#', 'A', 'B', 'C#', 'D#'],
    5: ['F', 'G', 'A', 'Bb', 'C', 'D', 'E'],
    6: ['Gb', 'Ab', 'Bb', 'Cb', 'Db', 'Eb', 'F'],
    7: ['G', 'A', 'B', 'C', 'D', 'E', 'F#'],
    8: ['Ab', 'Bb', 'C', 'Db', 'Eb', 'F', 'G'],
    9: ['A', 'B', 'C#', 'D', 'E', 'F#', 'G#'],
    10: ['Bb', 'C', 'D', 'Eb', 'F', 'G', 'A'],
    11: ['B', 'C#', 'D#', 'E', 'F#', 'G#', 'A#']
}


SCALES_MINOR = {
    0: ['C', 'D', 'Eb', 'F', 'G', 'Ab', 'B'],
    1: ['C#', 'D#', 'E', 'F#', 'G#', 'A', 'B#'],
    2: ['D', 'E', 'F', 'G', 'A', 'Bb', 'C#'],
    3: ['Eb', 'F', 'Gb', 'Ab', 'Bb', 'Cb', 'D'],
    4: ['E', 'F#', 'G', 'A', 'B', 'C', 'D#'],
    5: ['F', 'G', 'Ab', 'Bb', 'C', 'Db', 'E'],
    6: ['F#', 'G#', 'A', 'B', 'C#', 'D', 'E#'],
    7: ['G', 'A', 'Bb', 'C', 'D', 'Eb', 'F#'],
    8: ['G#', 'A#', 'B', 'C#', 'D#', 'E', 'F##'],
    9: ['A', 'B', 'C', 'D', 'E', 'F', 'G#'],
    10: ['Bb', 'C', 'Db', 'Eb', 'F', 'Gb', 'A'],
    11: ['B', 'C#', 'D', 'E', 'F#', 'G', 'A#']
}

SCALES_MELODIC_MINOR = {
    0: ['C', 'D', 'Eb', 'F', 'G', 'A', 'B'],
    1: ['C#', 'D#', 'E', 'F#', 'G#', 'A#', 'B#'],
    2: ['D', 'E', 'F', 'G', 'A', 'B', 'C#'],
    3: ['Eb', 'F', 'Gb', 'Ab', 'Bb', 'C', 'D'],
    4: ['E', 'F#', 'G', 'A', 'B', 'C#', 'D#'],
    5: ['F', 'G', 'Ab', 'Bb', 'C', 'D', 'E'],
    6: ['F#', 'G#', 'A', 'B', 'C#', 'D#', 'E#'],
    7: ['G', 'A', 'Bb', 'C', 'D', 'E', 'F#'],
    8: ['G#', 'A#', 'B', 'C#', 'D#', 'E#', 'F##'],
    9: ['A', 'B', 'C', 'D', 'E', 'F#', 'G#'],
    10: ['Bb', 'C', 'Db', 'Eb', 'F', 'G', 'A'],
    11: ['B', 'C#', 'D', 'E', 'F#', 'G#', 'A#']
}

SCALES = {
    'm': SCALES_MINOR,
    'mm': SCALES_MELODIC_MINOR,
    'M': SCALES_MAJOR
}


def get_note_spelling(note, chord, last_pitch=None):
    from .to_midi import note_to_pitch_result
    degree = chord.degree
    tonality_degree = chord.tonality.degree
    mode = chord.tonality.mode
    pitch = note_to_pitch_result(note, chord, last_pitch=last_pitch)
    tonality_scale_pitches = [p % 12 for p in chord.tonality.scale_pitches]
    if (pitch % 12) in tonality_scale_pitches:
        idx = tonality_scale_pitches.index(pitch % 12)
        note_spelling = SCALES[mode][tonality_degree][idx]
        # Correct octave
        octave = (pitch + 48) // 12
        if note_spelling in ['B#']:
            octave -= 1
        elif note_spelling in ['Cb']:
            octave += 1
        note_spelling = note_spelling + str(octave)
        new_note = music21.note.Note(note_spelling)
        new_note.duration = music21.duration.Duration(note.duration)
    else:
        new_note = music21.note.Note(pitch % 12)
        new_note.octave = (pitch + 48) // 12
        new_note.duration = music21.duration.Duration(note.duration)

    return new_note, pitch


def tonality_to_music21_key(tonality):
    tonality_mode = tonality.mode
    tonality_degree = tonality.degree
    tonalities_major = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
    tonalities_minor = ['c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'bb', 'b']
    tonalities = tonalities_major if tonality_mode in ['M', 'lydian', 'mixolydian'] else tonalities_minor
    key = music21.key.Key(tonalities[tonality_degree])
    return key


def find_tonality(score):
    from musiclang.transform.features import ExtractMainTonality
    tonality = ExtractMainTonality()(score)
    return tonality_to_music21_key(tonality)


def get_musescore_name(ins):
    """
    Get the name of the part as printed on the score
    Parameters
    ----------
    ins: str
        Raw instrument name

    Returns
    -------
    result: str
        Name
    """
    res = ins.capitalize().replace('_', ' ')

    return MUSESCORE_REPLACE_DICT.get(res, res)


def find_instruments(score):
    """
    Given a score return the list of instruments as printed on the score
    Parameters
    ----------
    score

    Returns
    -------
    parts_dict_names: dict
        Dict of music21 part for each instrument, keyed by part name in musiclang
    parts_dic: dict
        Dict of music21 part for each instrument keyed by instrument name

    """
    from music21 import instrument, stream
    from musiclang.write.out.constants import INSTRUMENTS_DICT
    from musiclang.write.constants import ALL_INST
    instruments = [(ins.split('__')[0], ins) for ins in score.instruments]

    parts_dict = {}
    parts_dict_names = {}
    # Regroup same instruments on same part
    for ins, part_name in instruments:
        if ins not in parts_dict:
            parts_dict[ins] = stream.Part()
            instr = instrument.Instrument(get_musescore_name(ins))
            instr.midiProgram = INSTRUMENTS_DICT.get(ins, 0)
            part = parts_dict[ins]
            part.append(instr)

        part = parts_dict[ins]
        parts_dict_names[part_name] = part

    return parts_dict_names, parts_dict

def score_instrument_to_notes(score, part_name, voice, voice_idx, no_repeat=False):
    """
    Given a score and a part name, returns the music21 voice with all the notes

    Parameters
    ----------
    score: Score
    part_name: str
    voice: music21.Voice
    voice_idx: int

    Returns
    -------
    voice: music21.Voice

    """
    last_spelling = None
    last_pitch = None
    last_is_silence = True
    curr_dynamic = 'mf'
    for chord in score.chords:
        voice, last_spelling, curr_dynamic, last_pitch, last_is_silence = chord_instrument_to_notes(chord, voice, part_name,
                                                                       voice_idx,
                                                                       last_spelling=last_spelling,
                                                                       curr_dynamic=curr_dynamic,
                                                                       no_repeat=no_repeat,
                                                                       last_pitch=last_pitch,
                                                                       last_is_silence=last_is_silence
                                                                       )
    return voice


def chord_to_musescore_lyric(chord: Chord):
    """
    Create the chord scale symbol on the score

    Parameters
    ----------
    chord

    Returns
    -------
    result: str
        Chord scale symbol
    """
    return "{} /{}".format(chord.element_to_str(), chord.tonality_to_str()).replace('%', '')


def chord_instrument_to_notes(chord, voice, part_name, ins_idx, last_spelling=None, curr_dynamic='mf', no_repeat=False,
                              last_pitch=None, last_is_silence=True):
    """
    Given a chord, get spellings

    Returns
    -------
    """

    # Enharmonic
    old_last_is_silence = last_is_silence
    last_is_silence = False
    FIGURES = ['n', 'ppp', 'pp', 'p', 'mp', 'mf', 'f', 'ff', 'fff']
    if part_name in chord.score.keys():
        part = chord.score[part_name]
        for idx_note, n in enumerate(part.notes):
            if n.is_note:
                old_last_pitch = last_pitch
                new_note, last_pitch = get_note_spelling(n, chord, last_pitch=last_pitch)
                last_spelling = new_note.nameWithOctave
                if idx_note == 0 and ins_idx == 0:
                    new_note.addLyric(chord_to_musescore_lyric(chord))
                if n.amp_figure != curr_dynamic:
                    dyn = dynamics.Dynamic(n.amp_figure)
                    voice.append(dyn)
                    curr_dynamic = n.amp_figure
                if (last_pitch != old_last_pitch) or (not no_repeat):
                    voice.append(new_note)
                else:
                    try:
                        if last_spelling is not None and not last_is_silence:
                            new_note = note.Note(last_spelling)
                            new_note.duration = music21.duration.Duration(n.duration)
                            voice[-1].tie = tie.Tie('start')
                            new_note.tie = tie.Tie('stop')
                            voice.append(new_note)
                        else:
                            voice.append(note.Rest(n.duration))
                            last_is_silence = True
                    except:
                        voice.append(note.Rest(n.duration))
                        last_is_silence = True
            elif n.is_silence:
                voice.append(note.Rest(n.duration))
                last_is_silence = True
            elif n.is_continuation:
                if old_last_is_silence:
                    last_is_silence = True
                try:
                    if last_spelling is not None and not last_is_silence:
                        new_note = note.Note(last_spelling)
                        new_note.duration = music21.duration.Duration(n.duration)
                        voice[-1].tie = tie.Tie('start')
                        new_note.tie = tie.Tie('stop')
                        voice.append(new_note)
                    else:
                        voice.append(note.Rest(n.duration))
                        last_is_silence = True
                except:
                    voice.append(note.Rest(n.duration))
                    last_is_silence = True

    else:
        voice.append(note.Rest(chord.duration))

    return voice, last_spelling, curr_dynamic, last_pitch, last_is_silence


def score_to_music_21(score, signature=(4, 4), tempo=50, tonality=None, title='MusicLang score', composer='MusicLang', no_repeat=False, **kwargs):
    """
    Transform a musiclang score into a Music21 score
    Parameters
    ----------
    score: Score
            MusicLang score to transform
    signature: tuple (nom, den)
            Time signature of the piece
    tempo: int
            Tempo of the piece
    tonality: Tonality
            Tonality of the piece if applicable
    title: str
        Title of the piece

    Returns
    -------
    m21_score: music21.Score
        Score transformed into a music21 object

    """
    # Find tonality
    if tonality is None:
        tonality = find_tonality(score)
    else:
        tonality = tonality_to_music21_key(tonality)

    # Find instruments
    parts, instruments = find_instruments(score)

    idx = 0
    # Add time signatures and tonalities ...
    for part_name, part in instruments.items():
        if idx == 0:
            part.append(music21.tempo.MetronomeMark('', tempo, note.Note(type='quarter')))
        part.append(tonality)
        part.append(meter.TimeSignature(f'{signature[0]}/{signature[1]}'))
        idx += 1

    # Create voices
    idx = 0
    for part_name, part in parts.items():
        # Add notes for each chord if first add lyrics ...
        voice = stream.Voice(number=idx + 1)
        voice = score_instrument_to_notes(score, part_name, voice, idx, no_repeat=no_repeat)

        part.insert(0, voice)
        idx += 1

    m21_score = stream.Score()
    meta = metadata.Metadata(title=title, composer=composer)
    m21_score.insert(0, meta)
    for part_name, part in instruments.items():
        m21_score.insert(0, part)
    # Iterate over chord for each instrument
    return m21_score


def score_to_mxl(score, filepath, signature=(4, 4), tempo=50, tonality=None, no_repeat=False, **kwargs):
    """
    Transform a musiclang score into a musicxml file, readable by all the main notation software (musescore, finale ...)

    Parameters
    ----------
    score: Score
            MusicLang score to transform
    filepath: str
            Filepath of the musicxml file
    signature: tuple (nom, den)
            Time signature of the piece
    tempo: int
            Tempo of the piece
    tonality: Tonality
            Tonality of the piece if applicable
    title: str
        Title of the piece

    """
    # Find tonality
    m21_score = score_to_music_21(score, signature=signature, tempo=tempo, tonality=tonality, no_repeat=no_repeat, **kwargs)
    m21_score.write('mxl', filepath)

