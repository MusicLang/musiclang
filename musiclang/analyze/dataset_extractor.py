
import glob

import os
import multiprocessing as mp
import random

from musiclang import Score

import concurrent.futures
import time
import signal

def signal_handler(signum, frame):
    raise Exception("Timed out!")

signal.signal(signal.SIGALRM, signal_handler)


def extract_one(self, filename):
    try:
        score = self.extract_musiclang(filename)
        if self.remove_drums:
            score = Score([self.remove_drums_in_score(chord) for chord in score.chords])
            score = Score([chord for chord in score.chords if chord.duration > 0])
        if score is not None:
            text_filename = ''.join(os.path.basename(filename).split('.')[:-1]) + '.txt'
            pickle_filename = ''.join(os.path.basename(filename).split('.')[:-1]) + '.pkl'
            text_output_filename = os.path.join(self.text_output_directory, text_filename)
            pickle_output_filename = os.path.join(self.pickle_output_directory, pickle_filename)
            score.to_text_file(text_output_filename)
            score.to_pickle(pickle_output_filename)
            print('SUCCESS !')
    except Exception as e:
        print('Error while processing file %s' % filename)
        print(e)
        # Add the file to the error file
        with open(self.error_file, 'a') as f:
            f.write(os.path.basename(filename) + '\n')

        return None
def extract_one_with_time_limit(self, filename):
    import time
    print('Processing file %s' % filename)
    start = time.time()
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(self.time_budget_per_file)
    try:
        extract_one(self, filename)
    except Exception as msg:
        print("Timed out!", msg)
        with open(self.error_file, 'a') as f:
            f.write(os.path.basename(filename) + '\n')
    # Try to extract the file (self.extract_one) within a given time budget (self.time_budget_per_file)
    # If it fails, add the file to the error file
    print('TOOK', time.time() - start)

class DatasetExtractor:

    """
    Main class to extract musiclang notation from a glob pattern of midi files
    """

    def __init__(self, input_pattern, output_directory,
                 remove_drums=False, fast_chord_inference=True,
                 time_budget_per_file=120
                 ):

        self.remove_drums = remove_drums
        self.time_budget_per_file = time_budget_per_file
        self.fast_chord_inference = fast_chord_inference

        # List all the files to process
        self.files = glob.glob(input_pattern)
        random.shuffle(self.files)

        # Create output directory if it does not exist
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        # Create text output directory
        self.text_output_directory = os.path.join(output_directory, 'text')
        if not os.path.exists(self.text_output_directory):
            os.makedirs(self.text_output_directory)

        # Create pickle output directory
        self.pickle_output_directory = os.path.join(output_directory, 'pickle')
        if not os.path.exists(self.pickle_output_directory):
            os.makedirs(self.pickle_output_directory)

        # Create error file
        self.error_file = os.path.join(output_directory, 'errors.txt')

        # Filter files that have already been processed
        print('Original length :', len(self.files))
        self.filter_files()


    def filter_files(self):
        # Read error files and remove them from the list of files to process
        if os.path.exists(self.error_file):
            with open(self.error_file, 'r') as f:
                errors = f.read().split('\n')
            self.files = [file for file in self.files if not os.path.basename(file) in errors]
        print('Filtered error length :', len(self.files))
        self.files = [file for file in self.files
                      if not
                      os.path.exists(os.path.join(self.text_output_directory,
                                                  ''.join(os.path.basename(file).split('.')[:-1]) + '.txt'))]
        print('Filtered length :', len(self.files))

    def remove_drums_in_score(self, chord):
        return chord(**{ins: val for ins, val in chord.items() if not ins.startswith('drums')})

    def extract_musiclang(self, filename):
        """
        Extract musiclang notation from a midi file
        """
        return Score.from_midi(filename, fast_chord_inference=self.fast_chord_inference)



    def extract_all_files(self, n_jobs=1):
        """
        Multiprocess the extract one method to parallelize the extraction, it call extract_one with a mapping
        """
        import functools
        if n_jobs > 1:
            print('Using multiprocessing')
            pool = mp.Pool(n_jobs, maxtasksperchild=1)
            pool.map(functools.partial(extract_one_with_time_limit, self), self.files)
            pool.close()
            pool.join()
        else:
            print('Not using multiprocessing')
            import time

            for filename in self.files:
                print('Processing file %s' % filename)

                start = time.time()
                signal.signal(signal.SIGALRM, signal_handler)
                signal.alarm(self.time_budget_per_file)
                try:
                    extract_one(self, filename)
                except Exception as msg:
                    print("Timed out!", msg)
                    with open(self.error_file, 'a') as f:
                        f.write(os.path.basename(filename) + '\n')
                # Try to extract the file (self.extract_one) within a given time budget (self.time_budget_per_file)
                # If it fails, add the file to the error file
                print('TOOK', time.time() - start)

