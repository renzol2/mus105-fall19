########################################

from .pitch import Pitch
from .mode import Mode
from .interval import Interval

"""
Major Scales:
-7: Cb major 0
-6: Gb major 1
-5: Db major 2
-4: Ab major 3
-3: Eb major 4
-2: Bb major 5
-1: F major 6
0: C major 7
1: G major 8
2: D major 9
3: A major 10
4: E major 11
5: B major 12
6: F# major 13
7: C# major 14
"""
tonics_by_major = [Pitch.pnums.Cf, Pitch.pnums.Gf, Pitch.pnums.Df, Pitch.pnums.Af, Pitch.pnums.Ef, Pitch.pnums.Bf,
                   Pitch.pnums.F, Pitch.pnums.C, Pitch.pnums.G, Pitch.pnums.D, Pitch.pnums.A, Pitch.pnums.E,
                   Pitch.pnums.B, Pitch.pnums.Fs, Pitch.pnums.Cs]

major_scale_intervals = [Interval('P1'), Interval('M2'), Interval('M3'), Interval('P4'),
                         Interval('P5'), Interval('M6'), Interval('M7')]


# A class that implements musical keys.
#
# The Key class represents the complete chromatic set of keys in western music.
# A key consists of an integer 'signum' representing the number of sharps or
# flats in the key's signature, and a mode (Enum). Keys can return Pnums
# representing their tonic note and diatonic scale degrees.
# See: https://en.wikipedia.org/wiki/Key_(music)
class Key:
    # Creates a Key from an integer key signature identifier and mode.
    #  @param signum  A value -7 to 7 representing the number of flats
    #  (negative) or sharps (positive).
    #  @param mode  A Mode enum, or its case-insensitive string name.
    #
    #  The constructor should raise a TypeError if signum is not an integer
    #  or if mode is not a Mode or string. The constructor should raise a
    #  ValueError if the signum integer or the mode string is invalid.
    def __init__(self, signum, mode):
        if isinstance(signum, int) and (isinstance(mode, Mode) or isinstance(mode, str)):
            if -7 <= signum <= 7 and (mode in [m.name.lower().capitalize() for m in Mode] or mode in Mode):
                self.signum = signum
                if isinstance(mode, Mode):
                    self.mode = mode.name.lower().capitalize()
                else:
                    self.mode = mode
            else:
                raise ValueError("signum is not a valid integer (-7 to 7) and/or mode is not a valid mode.")
        else:
            raise TypeError("signum must be an integer from -7 to 7 and mode must be a Mode Enum object.")

    # Returns the print representation of the key. The string should
    # include the class name, tonic, mode, number of sharps or flats,
    # and the instance id.
    #
    # Examples:
    # <Key: C-Major (0 sharps or flats) 0x10c03c050>
    # <Key: G-Major (1 sharp) 0x10eec5250>
    # <Key: A-Mixolydian (2 sharps) 0x10c03c490>
    # <Key: Af-Minor (7 flats) 0x10c03c390>
    def __str__(self):
        signum = self.signum
        if self.signum > 0:
            accidental_name = 'sharps'
        elif self.signum < 0:
            accidental_name = 'flats'
            # removing the negative from the number
            signum = str(self.signum)[1:]
        else:
            accidental_name = 'sharps or flats'
        if abs(self.signum) == 1:
            # changing from plural to singular
            accidental_name = accidental_name[:len(accidental_name) - 1]
        return f'<Key: {self.string()} ({signum} {accidental_name}) {hex(id(self))}>'

    # Returns the external representation of the Key including the
    # constructor name, signum, and the capitalized version of the
    # mode's name.
    #
    # Examples:
    # 'Key(4, "Dorian")'
    # 'Key(-1, "Major")'
    def __repr__(self):
        return f'Key({self.signum}, "{self.mode}")'

    # Returns a string containing the name of the tonic Pnum, a
    # hyphen, and the capitalized version of the mode's name.
    #
    # Examples: Fs-Dorian, Bf-Phrygian, B-Major
    def string(self):
        return f'{self.tonic().name}-{self.mode}'

    # Returns a Pnum representing the key's tonic. The tonic can
    # be calculated by transposing the Major tonic (Pnum) by the
    # interval distance of the mode above the major. The
    # transposition can be performed using that interval's transpose()
    # method. The interval distances of Major up to Locrian are:
    # P1, M2, M3, P4, P5, M6, M7.
    #
    # Examples:
    # Key(0, "lydian").tonic() is Pnum F.
    # Key(2, "dorian").tonic() is Pnum E.
    # Key(-6, "phrygian").tonic() is Pnum Bf.
    def tonic(self):
        return self.scale()[0]

    # Returns a list of Pnums representing the unique pitches of the key's
    # diatonic scale. The octave completion should NOT be included in the list.
    def scale(self):
        major_tonic_pnum = tonics_by_major[self.signum + 7]
        major_scale = [interval.transpose(major_tonic_pnum) for interval in major_scale_intervals]
        return major_scale[Mode[self.mode.upper()]:] + major_scale[:Mode[self.mode.upper()]]
