import re
import itertools


CHORD_REGEX = re.compile(r'\([^)]+%[^)]+\)')

class ChordTokenizer:
    """Chord tokenizer transforms a score in text format to a list of tokens"""

    def __init__(self):
        pass

    def tokenize(self, text):
        """Tokenize a text (or score) to extract chord tokens

        Parameters
        ----------
        text :
            Score or str, if Score first convert it to its string representation

        Returns
        -------
        type
            List of tokens

        """
        chords = re.findall(CHORD_REGEX, str(text))
        # Deduplicate the chords, because we don't care about rythm here
        deduplicated_chords = [k for k, _g in itertools.groupby(chords)]
        return deduplicated_chords


    def tokenize_all(self, texts):
        """Tokenize all texts

        Parameters
        ----------
        texts :
            return: List of List of tokens

        Returns
        -------
        type
            List of List of tokens

        """
        data = []
        for text in texts:
            data.append(self.tokenize(text))

        return data

    def tokenize_file(self, file):
        """

        Parameters
        ----------
        file :
            

        Returns
        -------

        """
        with open(file, 'r') as f:
            return self.tokenize(f.read())

    def tokenize_directory(self, directory):
        """

        Parameters
        ----------
        directory :
            

        Returns
        -------

        """
        import os
        files = [os.path.join(dirpath, file)
                 for (dirpath, dirnames, filenames) in os.walk(directory)
         for file in filenames]

        data = []
        for file in files:
            data.append(self.tokenize_file(file))

        return data


class ChordDetokenizer:
    """Convert tokens from chord tokenizer to chords"""

    def detokenize(self, tokens):
        """

        Parameters
        ----------
        tokens :
            

        Returns
        -------

        """
        from musiclang.write.library import I, II, III, IV, V, VI, VII
        return sum(eval('+'.join(tokens)), None)