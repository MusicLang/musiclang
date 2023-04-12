import json
from musiclang import Score
from .pattern_analyzer import PatternExtractor

class PicklePatternSampler:
    """
    Sample a chord pattern from a nested directory of musiclang text files
    """
    def __init__(self, directory, metadata_file=None,
                 bar_duration=4, min_nb_instruments=2,
                 **kwargs
                 ):
        self.directory = directory
        self.metadata_file = metadata_file
        self.bar_duration = bar_duration
        self.files = self.load_files()
        self.metadata = self.load_metadata()
        self.min_nb_instruments = min_nb_instruments
        self.kwargs = kwargs

    def load_metadata(self):
        if self.metadata_file is None:
            return {}
        else:
            with open(self.metadata_file, 'r') as f:
                metadata = json.load(f)
            return metadata

    def load_files(self):
        import glob
        files = glob.glob(self.directory + '/**/*.pkl', recursive=True)
        return files

    def sample(self):
        # Sample a file
        import random
        max_iter = 100
        idx = 0
        while idx < max_iter:
            file = random.choice(self.files)
            # Load the score from the file
            score = Score.from_pickle(file)

            # if score.config['time_signature'] != (4, 4):
            #     print('No good time signature', score.config['time_signature'])
            #     continue
            # Look for a chord with proper bar duration
            available_chords = [chord for chord in score.chords if (chord.duration == self.bar_duration)
                                and len(chord.instruments) >= self.min_nb_instruments]
            if len(available_chords) == 0:
                idx += 1
                continue

            chord_idx = random.choice(range(len(available_chords)))
            chord = available_chords[chord_idx]
            # Sort instruments from lower to higher pitch
            return PatternExtractor(**self.kwargs).extract(chord)

        raise Exception('No chord respecting criterias were found')



class TextPatternSampler(PicklePatternSampler):


    def load_files(self):
        import glob
        files = glob.glob(self.directory + '/**/*.txt', recursive=True)
        return files
