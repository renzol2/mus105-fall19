###############################################################################

from enum import Enum

# Line-Space unit constants.
TOP_LINE = 8
SPACE_BELOW_TOP_LINE = 7
LINE_ABOVE_MIDDLE_LINE = 6
SPACE_ABOVE_MIDDLE_LINE = 5
MIDDLE_LINE = 4
SPACE_BELOW_MIDDLE_LINE = 3
LINE_BELOW_MIDDLE_LINE = 2
SPACE_ABOVE_BOTTOM_LINE = 1
BOTTOM_LINE = 0

_NON_TRANSPOSING = 0
_8VA_UP = 8
_8VA_DOWN = -8
_15MA_UP = 15
_15MA_DOWN = -15


# An enumeration of music clefs using 3-tuples. The first value in the enum's
# tuple is a unique number of the clef 0-15. The second value is the
# attachment position of the clef in 'line-space' units (see above), where 0
# is bottom line, 1 is the space above , 3 is space below middle line,
# and so on. The third value is a clef transposition value. This is usually 0,
# but for a transposing clef it will be either 8, -8, 15, or -15 depending on
# the clef. The clefs to enumerate are: TREBLE, SOPRANO, MEZZO_SOPRANO, ALTO,
# TENOR, BARITONE, BASS, TREBLE_8VA, BASS_8VA, TREBLE_15MA, BASS_15MA,
# TENOR_TREBLE, BARITONE_F, SUB_BASS, FRENCH_VIOLIN, PERCUSSION
#
# For information about clefs see: https://en.wikipedia.org/wiki/Clef
class Clef (Enum):
    TREBLE = (0, LINE_BELOW_MIDDLE_LINE, _NON_TRANSPOSING)
    SOPRANO = (1, BOTTOM_LINE, _NON_TRANSPOSING)
    MEZZO_SOPRANO = (2, LINE_BELOW_MIDDLE_LINE, _NON_TRANSPOSING)
    ALTO = (3, MIDDLE_LINE, _NON_TRANSPOSING)
    TENOR = (4, LINE_ABOVE_MIDDLE_LINE, _NON_TRANSPOSING)
    BARITONE = (5, TOP_LINE, _NON_TRANSPOSING)
    BASS = (6, LINE_ABOVE_MIDDLE_LINE, _NON_TRANSPOSING)
    TREBLE_8VA = (7, LINE_BELOW_MIDDLE_LINE, _8VA_UP)
    BASS_8VA = (8, LINE_ABOVE_MIDDLE_LINE, _8VA_DOWN)
    TREBLE_15MA = (9, LINE_BELOW_MIDDLE_LINE, _15MA_UP)
    BASS_15MA = (10, LINE_ABOVE_MIDDLE_LINE, _15MA_DOWN)
    TENOR_TREBLE = (11, LINE_BELOW_MIDDLE_LINE, _8VA_DOWN)
    BARITONE_F = (12, MIDDLE_LINE, _NON_TRANSPOSING)
    SUB_BASS = (13, TOP_LINE, _NON_TRANSPOSING)
    FRENCH_VIOLIN = (14, BOTTOM_LINE, _NON_TRANSPOSING)
    PERCUSSION = (15, MIDDLE_LINE, _NON_TRANSPOSING)  # not sure about this one...

    # Returns the linespace attachment value of the clef.
    def linespace(self):
        return self.value[1]

    # Returns the transposition level of the clef.
    def transposition(self):
        return self.value[2]


