from miditok import REMI
from miditok.classes import TokenizerConfig
from miditoolkit import MidiFile




def test_exotic_time_signature():
    config = TokenizerConfig(
        beat_res={(0, 8): 16, (8, 16): 16},
        use_tempos=True,
        use_time_signatures=True,
        time_signature_range={8: [3, 12, 6, 9, 10, 11],
                              4: [5, 6, 7, 3, 2, 1, 4],
                              16: [3, 6, 7, 9, 12, 14, 15, 17],
                              2: [1, 2, 3, 4],
                              1: [1, 2, 3, 4]
                              },
        one_token_stream_for_programs=True,
        use_programs=True)

    tokenizer = REMI(
        tokenizer_config=config,
    )
    tokenizer.one_token_stream = True
    tokens = ['Bar_None', 'TimeSig_9/8', 'Position_0', 'Program_24', 'Pitch_52', 'Velocity_127',
              'Duration_0.8.16', 'Program_24', 'Pitch_64', 'Velocity_127', 'Duration_0.8.16',
              'Position_8', 'Program_24', 'Pitch_50', 'Velocity_127', 'Duration_0.8.16',
              'Program_24', 'Pitch_62', 'Velocity_127', 'Duration_0.8.16', 'Position_16',
              'Program_24', 'Pitch_49', 'Velocity_127', 'Duration_0.8.16', 'Program_24',
              'Pitch_61', 'Velocity_127', 'Duration_0.8.16', 'Position_24', 'Program_24',
              'Pitch_50', 'Velocity_127', 'Duration_0.8.16', 'Program_24', 'Pitch_62',
              'Velocity_127', 'Duration_0.8.16', 'Position_32', 'Program_24',
              'Pitch_40', 'Velocity_127', 'Duration_1.0.16', 'Program_24', 'Pitch_52',
              'Velocity_127', 'Duration_1.0.16', 'Program_24', 'Pitch_64', 'Velocity_127', 'Duration_1.0.16',

              'Bar_None', 'TimeSig_9/8', 'Position_0', 'Program_24', 'Pitch_52', 'Velocity_127',
              'Duration_0.8.16', 'Program_24', 'Pitch_64', 'Velocity_127', 'Duration_0.8.16',
              'Position_8', 'Program_24', 'Pitch_50', 'Velocity_127', 'Duration_0.8.16',
              'Program_24', 'Pitch_62', 'Velocity_127', 'Duration_0.8.16', 'Position_16',
              'Program_24', 'Pitch_49', 'Velocity_127', 'Duration_0.8.16', 'Program_24',
              'Pitch_61', 'Velocity_127', 'Duration_0.8.16', 'Position_24', 'Program_24',
              'Pitch_50', 'Velocity_127', 'Duration_0.8.16', 'Program_24', 'Pitch_62',
              'Velocity_127', 'Duration_0.8.16', 'Position_32', 'Program_24',
              'Pitch_40', 'Velocity_127', 'Duration_1.0.16', 'Program_24', 'Pitch_52',
              'Velocity_127', 'Duration_1.0.16', 'Program_24', 'Pitch_64', 'Velocity_127', 'Duration_1.0.16',

              ]

    idxs = [tokenizer[t] for t in tokens]
    midi = tokenizer.tokens_to_midi(idxs)
    import tempfile

    from fractions import Fraction
    # Save midi to a tempfile
    with tempfile.NamedTemporaryFile(suffix='.mid') as f:
        output_path = f.name
        midi.dump(output_path)
        # Reload with musiclang
        from musiclang import Score
        score = Score.from_midi(output_path, tokenize_before=True)
        assert [c.duration for c in score] == [Fraction(9, 2),
                                               Fraction(9, 2),
                                               ]



def test_time_signature_change():
    """
    Test musiclang parser capability to parse a midi file with various time signature changes

    Returns
    -------

    """
    config = TokenizerConfig(
        beat_res={(0, 8): 16, (8, 16): 16},
        use_tempos=True,
        use_time_signatures=True,
        time_signature_range={8: [3, 12, 6, 9, 10, 11],
                              4: [5, 6, 7, 3, 2, 1, 4],
                              16: [3, 6, 7, 9, 12, 14, 15, 17],
                              2: [1, 2, 3, 4],
                              1: [1, 2, 3, 4]
                              },
        one_token_stream_for_programs=True,
        use_programs=True)

    tokenizer = REMI(
        tokenizer_config=config,
    )
    tokenizer.one_token_stream = True
    tokens = ['Bar_None', 'TimeSig_4/4', 'Position_0', 'Program_24', 'Pitch_52', 'Velocity_127',
              'Duration_0.8.16', 'Program_24', 'Pitch_64', 'Velocity_127', 'Duration_0.8.16',
              'Position_8', 'Program_24', 'Pitch_50', 'Velocity_127', 'Duration_0.8.16',
              'Program_24', 'Pitch_62', 'Velocity_127', 'Duration_0.8.16', 'Position_16',
              'Program_24', 'Pitch_49', 'Velocity_127', 'Duration_0.8.16', 'Program_24',
              'Pitch_61', 'Velocity_127', 'Duration_0.8.16', 'Position_24', 'Program_24',
              'Pitch_50', 'Velocity_127', 'Duration_0.8.16', 'Program_24', 'Pitch_62',
              'Velocity_127', 'Duration_0.8.16', 'Position_32', 'Program_24',
              'Pitch_40', 'Velocity_127', 'Duration_1.0.16', 'Program_24', 'Pitch_52',
              'Velocity_127', 'Duration_1.0.16', 'Program_24', 'Pitch_64', 'Velocity_127', 'Duration_1.0.16',

              'Bar_None', 'TimeSig_6/8', 'Position_0', 'Program_24', 'Pitch_52', 'Velocity_127',
              'Duration_0.8.16', 'Program_24', 'Pitch_64', 'Velocity_127', 'Duration_0.8.16',
              'Position_8', 'Program_24', 'Pitch_50', 'Velocity_127', 'Duration_0.8.16',
              'Program_24', 'Pitch_62', 'Velocity_127', 'Duration_0.8.16', 'Position_16',
              'Program_24', 'Pitch_49', 'Velocity_127', 'Duration_0.8.16', 'Program_24',
              'Pitch_61', 'Velocity_127', 'Duration_0.8.16', 'Position_24', 'Program_24',
              'Pitch_50', 'Velocity_127', 'Duration_0.8.16', 'Program_24', 'Pitch_62',
              'Velocity_127', 'Duration_0.8.16', 'Position_32', 'Program_24',
              'Pitch_40', 'Velocity_127', 'Duration_1.0.16', 'Program_24', 'Pitch_52',
              'Velocity_127', 'Duration_1.0.16', 'Program_24', 'Pitch_64', 'Velocity_127', 'Duration_1.0.16',

              'Bar_None', 'TimeSig_4/4', 'Position_0', 'Program_24', 'Pitch_52', 'Velocity_127',
              'Duration_0.8.16', 'Program_24', 'Pitch_64', 'Velocity_127', 'Duration_0.8.16',
              'Position_8', 'Program_24', 'Pitch_50', 'Velocity_127', 'Duration_0.8.16',
              'Program_24', 'Pitch_62', 'Velocity_127', 'Duration_0.8.16', 'Position_16',
              'Program_24', 'Pitch_49', 'Velocity_127', 'Duration_0.8.16', 'Program_24',
              'Pitch_61', 'Velocity_127', 'Duration_0.8.16', 'Position_24', 'Program_24',
              'Pitch_50', 'Velocity_127', 'Duration_0.8.16', 'Program_24', 'Pitch_62',
              'Velocity_127', 'Duration_0.8.16', 'Position_32', 'Program_24',
              'Pitch_40', 'Velocity_127', 'Duration_1.0.16', 'Program_24', 'Pitch_52',
              'Velocity_127', 'Duration_1.0.16', 'Program_24', 'Pitch_64', 'Velocity_127', 'Duration_1.0.16',

              'Bar_None', 'TimeSig_6/8', 'Position_0', 'Program_24', 'Pitch_52', 'Velocity_127',
              'Duration_0.8.16', 'Program_24', 'Pitch_64', 'Velocity_127', 'Duration_0.8.16',
              'Position_8', 'Program_24', 'Pitch_50', 'Velocity_127', 'Duration_0.8.16',
              'Program_24', 'Pitch_62', 'Velocity_127', 'Duration_0.8.16', 'Position_16',
              'Program_24', 'Pitch_49', 'Velocity_127', 'Duration_0.8.16', 'Program_24',
              'Pitch_61', 'Velocity_127', 'Duration_0.8.16', 'Position_24', 'Program_24',
              'Pitch_50', 'Velocity_127', 'Duration_0.8.16', 'Program_24', 'Pitch_62',
              'Velocity_127', 'Duration_0.8.16', 'Position_32', 'Program_24',
              'Pitch_40', 'Velocity_127', 'Duration_1.0.16', 'Program_24', 'Pitch_52',
              'Velocity_127', 'Duration_1.0.16', 'Program_24', 'Pitch_64', 'Velocity_127', 'Duration_1.0.16',

              'Bar_None', 'TimeSig_6/8', 'Position_0', 'Program_24', 'Pitch_52', 'Velocity_127',
              'Duration_0.8.16', 'Program_24', 'Pitch_64', 'Velocity_127', 'Duration_0.8.16',
              'Position_8', 'Program_24', 'Pitch_50', 'Velocity_127', 'Duration_0.8.16',
              'Program_24', 'Pitch_62', 'Velocity_127', 'Duration_0.8.16', 'Position_16',
              'Program_24', 'Pitch_49', 'Velocity_127', 'Duration_0.8.16', 'Program_24',
              'Pitch_61', 'Velocity_127', 'Duration_0.8.16', 'Position_24', 'Program_24',
              'Pitch_50', 'Velocity_127', 'Duration_0.8.16', 'Program_24', 'Pitch_62',
              'Velocity_127', 'Duration_0.8.16', 'Position_32', 'Program_24',
              'Pitch_40', 'Velocity_127', 'Duration_1.0.16', 'Program_24', 'Pitch_52',
              'Velocity_127', 'Duration_1.0.16', 'Program_24', 'Pitch_64', 'Velocity_127', 'Duration_1.0.16',

              'Bar_None', 'TimeSig_4/4', 'Position_0', 'Program_24', 'Pitch_52', 'Velocity_127',
              'Duration_0.8.16', 'Program_24', 'Pitch_64', 'Velocity_127', 'Duration_0.8.16',
              'Position_8', 'Program_24', 'Pitch_50', 'Velocity_127', 'Duration_0.8.16',
              'Program_24', 'Pitch_62', 'Velocity_127', 'Duration_0.8.16', 'Position_16',
              'Program_24', 'Pitch_49', 'Velocity_127', 'Duration_0.8.16', 'Program_24',
              'Pitch_61', 'Velocity_127', 'Duration_0.8.16', 'Position_24', 'Program_24',
              'Pitch_50', 'Velocity_127', 'Duration_0.8.16', 'Program_24', 'Pitch_62',
              'Velocity_127', 'Duration_0.8.16', 'Position_32', 'Program_24',
              'Pitch_40', 'Velocity_127', 'Duration_1.0.16', 'Program_24', 'Pitch_52',
              'Velocity_127', 'Duration_1.0.16', 'Program_24', 'Pitch_64', 'Velocity_127', 'Duration_1.0.16',

              'Bar_None', 'TimeSig_4/4', 'Position_0', 'Program_24', 'Pitch_52', 'Velocity_127',
              'Duration_0.8.16', 'Program_24', 'Pitch_64', 'Velocity_127', 'Duration_0.8.16',
              'Position_8', 'Program_24', 'Pitch_50', 'Velocity_127', 'Duration_0.8.16',
              'Program_24', 'Pitch_62', 'Velocity_127', 'Duration_0.8.16', 'Position_16',
              'Program_24', 'Pitch_49', 'Velocity_127', 'Duration_0.8.16', 'Program_24',
              'Pitch_61', 'Velocity_127', 'Duration_0.8.16', 'Position_24', 'Program_24',
              'Pitch_50', 'Velocity_127', 'Duration_0.8.16', 'Program_24', 'Pitch_62',
              'Velocity_127', 'Duration_0.8.16', 'Position_32', 'Program_24',
              'Pitch_40', 'Velocity_127', 'Duration_1.0.16', 'Program_24', 'Pitch_52',
              'Velocity_127', 'Duration_1.0.16', 'Program_24', 'Pitch_64', 'Velocity_127', 'Duration_1.0.16',

              ]


    idxs = [tokenizer[t] for t in tokens]
    midi = tokenizer.tokens_to_midi(idxs)
    import tempfile

    from fractions import Fraction
    # Save midi to a tempfile
    with tempfile.NamedTemporaryFile(suffix='.mid') as f:
        output_path = f.name
        midi.dump(output_path)
        # Reload with musiclang
        from musiclang import Score
        score = Score.from_midi(output_path, tokenize_before=True)
        assert [c.duration for c in score] == [Fraction(4, 1),
             Fraction(3, 1),
             Fraction(4, 1),
             Fraction(3, 1),
             Fraction(3, 1),
             Fraction(4, 1),
             Fraction(4, 1)]

