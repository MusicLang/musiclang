"""
Copyright (c) 2023, Florian GARDIN
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""

import numpy as np

class SkylineSolution:
    """ """
    def get_skyline(self, notes):
        """

        Parameters
        ----------
        notes :
            

        Returns
        -------

        """
        if not notes:
            return []
        if len(notes) == 1:
            return [[notes[0][0], notes[0][2]] + notes[0][3:], [notes[0][1], 0] + notes[0][3:]]

        mid = len(notes) // 2
        left = self.get_skyline(notes[:mid])
        right = self.get_skyline(notes[mid:])
        return self.merge(left, right)

    def merge(self, left, right):
        """

        Parameters
        ----------
        left :
            
        right :
            

        Returns
        -------

        """
        h1, h2 = 0, 0
        i, j = 0, 0
        note1, note2 = [], []
        result = []

        while i < len(left) and j < len(right):
            if left[i][0] < right[j][0]:
                h1 = left[i][1]
                note1 = left[i][2:]
                corner = left[i][0]
                i += 1
            elif right[j][0] < left[i][0]:
                h2 = right[j][1]
                note2 = right[j][2:]
                corner = right[j][0]
                j += 1
            else:
                h1 = left[i][1]
                note1 = left[i][2:]
                h2 = right[j][1]
                note2 = right[j][2:]
                corner = right[j][0]
                i += 1
                j += 1
            if self.is_valid(result, max(h1, h2)):
                max_note = [note1, note2][np.argmax([h1, h2])]
                result.append([corner, max(h1, h2)] + max_note)
        result.extend(right[j:])
        result.extend(left[i:])
        return result

    def is_valid(self, result, new_height):
        """

        Parameters
        ----------
        result :
            
        new_height :
            

        Returns
        -------

        """
        return not result or result[-1][1] != new_height
