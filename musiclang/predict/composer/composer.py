from musiclang import Score
from musiclang.transform.melody.continuation import ContinuationWhenSameNote


class Composer:
    """
    Class for composing a piece automatically using an annotation generator model from musiclang_predict
    """

    def __init__(self, progressions, form, form_orchestra, orchestras, signature=(4, 4), continuation=True, **kwargs):
        self.form = form
        self.form_orchestra = form_orchestra
        self.signature = signature
        self.orchestras = orchestras
        self.progressions = progressions
        self.continuation = continuation

    def compose(self, **kwargs):
        """
        Main method to compose

        Parameters
        ----------
        kwargs

        Returns
        -------
        score: Score
        text: str
            Final annotation predicted by the auto composer

        """
        text = self.assemble_progressions(self.progressions)
        score = Score.from_annotation(text)
        # Use standard pipeline
        if self.continuation:
            score = ContinuationWhenSameNote()(score)
        return score, text

    def assemble_progressions(self, progressions):
        full_text = []
        for i, idx_form in enumerate(self.form):
            new_text = progressions[idx_form]
            full_text.append(self.orchestras[self.form_orchestra[i]])
            full_text.append(new_text)
        full_text = '\n'.join(full_text)
        full_text = self.clean(full_text)
        return full_text

    def line_is_bar(self, line):
        return line.lstrip(' ').startswith('m')

    def clean(self, progression):
        # Rename bar number to fit a progression
        # Basic replacements
        already_has_time_signature = False
        progression = progression.replace('iV', 'IV').replace('vI', 'VI').replace('iI', 'II')
        progression = progression.replace('Vi', 'VI')
        progression = progression.replace(':||', '').replace('||:', '')
        progression = progression.replace('||', '')
        new_lines = []
        for line in progression.split('\n'):
            line = line.lstrip('\t').lstrip(' ')
            if line.startswith('m') and '=' not in line:
                try:
                    elements = line.split(' ')
                    elements[0] = f'mx'
                    new_lines.append(' '.join(elements))
                except:
                    # FIXME : Repetitions are removed for the time being
                    pass

            elif line.capitalize().startswith('Time'):
                if not already_has_time_signature:
                    new_lines.append(line)
                    already_has_time_signature = True
            elif line.startswith('!'):
                new_lines.append(line)

        return '\n'.join(new_lines)