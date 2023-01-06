"""Templates for texturizing annotation files and turn them into scores."""

import random


class TextureTemplate(object):
    """The base class for texturization templates."""

    supported_durations = [4.0, 3.0, 2.0, 1.5, 1.0]
    supported_number_of_notes = [3, 4]

    def __init__(self, duration, notes, intervals):
        self.numberOfNotes = len(notes)
        if duration not in self.supported_durations:
            raise ValueError("Wrong duration value for this template.")
        if self.numberOfNotes not in self.supported_number_of_notes:
            raise ValueError(
                "This template doesn't support that number of notes."
            )
        self.duration = duration
        self.notes = notes
        self.intervals = intervals
        self.header = (
            "s_offset,s_duration,s_measure,s_notes,s_intervals,s_isOnset\n"
        )
        if self.numberOfNotes == 3:
            self.template = self.templateTriad
        elif self.numberOfNotes == 4:
            self.template = self.templateSeventh

    def templateTriad(self):
        """ """
        if self.duration == 3.0:
            return self.templateTriadDottedHalf()
        elif self.duration == 1.5:
            return self.templateTriadDottedQuarter()
        else:
            return self.templateTriadBinary()

    def templateTriadDottedHalf(self):
        """ """
        raise NotImplementedError()

    def templateTriadDottedQuarter(self):
        """ """
        raise NotImplementedError()

    def templateTriadBinary(self):
        """ """
        raise NotImplementedError()

    def templateSeventh(self):
        """ """
        if self.duration == 3.0:
            return self.templateSeventhDottedHalf()
        elif self.duration == 1.5:
            return self.templateSeventhDottedQuarter()
        else:
            return self.templateSeventhBinary()

    def templateSeventhDottedHalf(self):
        """ """
        raise NotImplementedError()

    def templateSeventhDottedQuarter(self):
        """ """
        raise NotImplementedError()

    def templateSeventhBinary(self):
        """ """
        raise NotImplementedError()

    def __str__(self):
        return self.header + self.template()

    def __repr__(self):
        return str(self)


class BassSplit(TextureTemplate):
    """Dividing the bass and remaining notes.
    
    The original chord duration is divided by half, playing
    the bass note in isolation during the first half,
    followed by the remaining upper notes.

    Parameters
    ----------

    Returns
    -------

    """

    def templateTriadBinary(self):
        """ """
        dur = self.duration / 2
        return f"""\
0.0,{dur},,['{self.notes[0]}'],[],[True]
{dur},{dur},,"['{self.notes[1]}', '{self.notes[2]}']",['{self.intervals[2]}'],"[True, True]"
"""

    def templateTriadDottedHalf(self):
        """ """
        dur = 0.5
        return f"""\
0.0,{dur},,['{self.notes[0]}'],[],[True]
{dur},{dur},,"['{self.notes[1]}', '{self.notes[2]}']",['{self.intervals[2]}'],"[True, True]"
{dur*2},{dur},,"['{self.notes[1]}', '{self.notes[2]}']",['{self.intervals[2]}'],"[True, True]"
{dur*3},{dur},,"['{self.notes[1]}', '{self.notes[2]}']",['{self.intervals[2]}'],"[True, True]"
{dur*4},{dur},,"['{self.notes[1]}', '{self.notes[2]}']",['{self.intervals[2]}'],"[True, True]"
{dur*5},{dur},,"['{self.notes[1]}', '{self.notes[2]}']",['{self.intervals[2]}'],"[True, True]"
"""

    def templateTriadDottedQuarter(self):
        """ """
        dur = 0.5
        return f"""\
0.0,{dur},,['{self.notes[0]}'],[],[True]
{dur},{dur},,"['{self.notes[1]}', '{self.notes[2]}']",['{self.intervals[2]}'],"[True, True]"
{dur*2},{dur},,"['{self.notes[1]}', '{self.notes[2]}']",['{self.intervals[2]}'],"[True, True]"
"""

    def templateSeventhBinary(self):
        """ """
        dur = self.duration / 2
        return f"""\
0.0,{dur},,['{self.notes[0]}'],[],[True]
{dur},{dur},,"['{self.notes[1]}', '{self.notes[2]}', '{self.notes[3]}']","['{self.intervals[3]}', '{self.intervals[4]}']","[True, True, True]"
"""

    def templateSeventhDottedHalf(self):
        """ """
        dur = 0.5
        return f"""\
0.0,{dur},,['{self.notes[0]}'],[],[True]
{dur},{dur},,"['{self.notes[1]}', '{self.notes[2]}', '{self.notes[3]}']","['{self.intervals[3]}', '{self.intervals[4]}']","[True, True, True]"
{dur*2},{dur},,"['{self.notes[1]}', '{self.notes[2]}', '{self.notes[3]}']","['{self.intervals[3]}', '{self.intervals[4]}']","[True, True, True]"
{dur*3},{dur},,"['{self.notes[1]}', '{self.notes[2]}', '{self.notes[3]}']","['{self.intervals[3]}', '{self.intervals[4]}']","[True, True, True]"
{dur*4},{dur},,"['{self.notes[1]}', '{self.notes[2]}', '{self.notes[3]}']","['{self.intervals[3]}', '{self.intervals[4]}']","[True, True, True]"
{dur*5},{dur},,"['{self.notes[1]}', '{self.notes[2]}', '{self.notes[3]}']","['{self.intervals[3]}', '{self.intervals[4]}']","[True, True, True]"
"""

    def templateSeventhDottedQuarter(self):
        """ """
        dur = 0.5
        return f"""\
0.0,{dur},,['{self.notes[0]}'],[],[True]
{dur},{dur},,"['{self.notes[1]}', '{self.notes[2]}', '{self.notes[3]}']","['{self.intervals[3]}', '{self.intervals[4]}']","[True, True, True]"
{dur*2},{dur},,"['{self.notes[1]}', '{self.notes[2]}', '{self.notes[3]}']","['{self.intervals[3]}', '{self.intervals[4]}']","[True, True, True]"
"""


class Alberti(TextureTemplate):
    """An Alberti-bass-like texturization of a chord.
    
    A  4-note  melodic  pattern with the contour
    lowest, highest, middle, highest.

    Parameters
    ----------

    Returns
    -------

    """

    def templateTriadBinary(self):
        """ """
        dur = self.duration / 4
        return f"""\
0.0,{dur},,['{self.notes[0]}'],[],[True]
{dur},{dur},,['{self.notes[2]}'],[],[True]
{dur*2},{dur},,['{self.notes[1]}'],[],[True]
{dur*3},{dur},,['{self.notes[2]}'],[],[True]
"""

    def templateTriadDottedHalf(self):
        """ """
        dur = 0.5
        return f"""\
0.0,{dur},,['{self.notes[0]}'],[],[True]
{dur},{dur},,['{self.notes[2]}'],[],[True]
{dur*2},{dur},,['{self.notes[1]}'],[],[True]
{dur*3},{dur},,['{self.notes[2]}'],[],[True]
{dur*4},{dur},,['{self.notes[1]}'],[],[True]
{dur*5},{dur},,['{self.notes[2]}'],[],[True]
"""

    def templateTriadDottedQuarter(self):
        """ """
        dur = 0.5
        return f"""\
0.0,{dur},,['{self.notes[0]}'],[],[True]
{dur},{dur},,['{self.notes[2]}'],[],[True]
{dur*2},{dur},,['{self.notes[1]}'],[],[True]
"""

    def templateSeventhBinary(self):
        """ """
        dur = self.duration / 4
        return f"""\
0.0,{dur},,['{self.notes[0]}'],[],[True]
{dur},{dur},,['{self.notes[3]}'],[],[True]
{dur*2},{dur},,['{self.notes[1]}'],[],[True]
{dur*3},{dur},,['{self.notes[2]}'],[],[True]
"""

    def templateSeventhDottedHalf(self):
        """ """
        dur = 0.5
        return f"""\
0.0,{dur},,['{self.notes[0]}'],[],[True]
{dur},{dur},,['{self.notes[3]}'],[],[True]
{dur*2},{dur},,['{self.notes[1]}'],[],[True]
{dur*3},{dur},,['{self.notes[2]}'],[],[True]
{dur*4},{dur},,['{self.notes[1]}'],[],[True]
{dur*5},{dur},,['{self.notes[2]}'],[],[True]
"""

    def templateSeventhDottedQuarter(self):
        """ """
        dur = 0.5
        return f"""\
0.0,{dur},,"['{self.notes[0]}', '{self.notes[3]}']",['{self.intervals[2]}'],[True]
{dur},{dur},,['{self.notes[1]}'],[],[True]
{dur*2},{dur},,['{self.notes[2]}'],[],[True]
"""


class Syncopation(TextureTemplate):
    """A syncopated pattern to separate the upper voice from the rest.
    
    The highest note is played in isolation,
    followed by the remaining lower notes,
    played in syncopation.

    Parameters
    ----------

    Returns
    -------

    """

    supported_durations = [4.0, 2.0]

    def templateTriad(self):
        """ """
        dur = self.duration / 4
        return f"""\
0.0,{dur},,['{self.notes[2]}'],[],[True]
{dur},{dur*2},,['{self.notes[0]}'],[],[True]
{dur*3},{dur},,['{self.notes[1]}'],[],[True]
"""

    def templateSeventh(self):
        """ """
        dur = self.duration / 4
        return f"""\
0.0,{dur},,['{self.notes[3]}'],[],[True]
{dur},{dur*2},,"['{self.notes[0]}', '{self.notes[1]}', '{self.notes[2]}']","['{self.intervals[0]}', '{self.intervals[1]}']","[True, True, True]"
{dur*3},{dur},,"['{self.notes[0]}', '{self.notes[1]}', '{self.notes[2]}']","['{self.intervals[0]}', '{self.intervals[1]}']","[True, True, True]"
"""


class BlockChord(TextureTemplate):
    """A block-chord texture. The default texture in music21-generated scores."""

    def templateTriad(self):
        """ """
        dur = self.duration
        return f"""\
0.0,{dur},,"['{self.notes[0]}', '{self.notes[1]}', '{self.notes[2]}']","['{self.intervals[0]}', '{self.intervals[1]}']","[True, True, True]"
"""

    def templateSeventh(self):
        """ """
        dur = self.duration
        return f"""\
0.0,{dur},,"['{self.notes[0]}', '{self.notes[1]}', '{self.notes[2]}', '{self.notes[3]}']","['{self.intervals[0]}', '{self.intervals[1]}', '{self.intervals[2]}']","[True, True, True, True]"
"""


available_templates = {
    "BassSplit": BassSplit,
    "Alberti": Alberti,
    "Syncopation": Syncopation,
    "BlockChord": BlockChord,
}

available_durations = list(
    reversed(
        sorted(
            set(
                [
                    d
                    for t in available_templates.values()
                    for d in t.supported_durations
                ]
            )
        )
    )
)

available_number_of_notes = list(
    reversed(
        sorted(
            set(
                [
                    n
                    for t in available_templates.values()
                    for n in t.supported_number_of_notes
                ]
            )
        )
    )
)


def _getRelevantTemplates(duration, numberOfNotes):
    """

    Parameters
    ----------
    duration :
        
    numberOfNotes :
        

    Returns
    -------

    """
    ret = []
    for template in available_templates.values():
        if (
            duration in template.supported_durations
            and numberOfNotes in template.supported_number_of_notes
        ):
            ret.append(template)
    return ret


def applyTextureTemplate(duration, notes, intervals, templateName=None):
    """Apply a random texture to a chord with the given duration and notes.

    Parameters
    ----------
    duration :
        
    notes :
        
    intervals :
        
    templateName :
         (Default value = None)

    Returns
    -------

    """

    numberOfNotes = len(notes)
    if templateName:
        if templateName not in available_templates:
            raise KeyError()
        else:
            template = available_templates[templateName]
            return str(template(duration, notes, intervals))
    if (
        duration not in available_durations
        or numberOfNotes not in available_number_of_notes
    ):
        raise KeyError()
    relevantTemplates = _getRelevantTemplates(duration, numberOfNotes)
    return str(random.choice(relevantTemplates)(duration, notes, intervals))
