########################################
from enum import IntEnum
from math import pow


# A class that implements musical pitches.
#
# The Pitch class represent equal tempered pitches and returns information
# in hertz, keynum, pitch class, Pnum  and pitch name formats.  Pitches
# can be compared using standard math relations and maintain proper spelling
# when complemented or transposed by an Interval.


class Pitch:
    # A class variable that holds an IntEnum of all possible letter-and-accidental
    #  combinations Cff up to Bss. Each pnum encodes its letter and accidental index
    #  as a one byte value 'llllaaaa', where 'llll' is its letter index 0-6, and
    #  'aaaa' is its accidental index 0-4.  You should set the pnums variable like this:
    #  pnum = IntEnum('Pnum', [tuple...]) where Pnum is the name of the enum class,
    #  [tuple...'] is a list of tuples, and each tuple is (enum_name, enum_val).
    #  The enum names are all possible combinations of pitch letters and accidentals
    #  e.g. 'Cff' upto  'Bss'.  Since the accidental character # is illegal as a
    #  python enum name be sure to use only the 'safe versions' of the accidental
    #  names: 'ff' upto 'ss'. The enum values are the one byte integers containing
    #  the letter and accidental indexes: (letter << 4) + accidental.
    pnums = IntEnum('Pnum', [])

    # CONSTRUCTOR
    # Creates a Pitch from a string or list, if neither is provided
    #  an empty Pitch is returned.
    #  * Pitch(string) - creates a Pitch from a pitch name string.
    #  * Pitch([l, a, o]) - creates a Pitch from a three element
    #  pitch list containing a letter, accidental and octave index
    #  (see below).
    #  * Pitch() - creates an empty Pitch.
    #
    #  @param ref A pitch name string, a list of three pitch indexes, or None.
    #
    # The format of a Pitch name string is:
    # @code
    #  <pitch> :=  <letter>, [<accidental>], <octave>
    #  <letter> := 'C' | 'D' | 'E' | 'F' | 'G' | 'A' | 'B'
    #  <accidental> := <2flat> | <flat> | <natural> | <sharp> | <2sharp>
    #  <2flat> := 'bb' | 'ff'
    #  <flat> := 'b' | 'f'
    #  <natural> := ''
    #  <sharp> := '#' | 's'
    #  <2sharp> := '#' | 'ss'
    #  <octave> := '00' | '0' | '1'  | '2'  | '3'  | '4'  | '5'  | '6'  | '7'  | '8'  | '9'
    # @endcode
    #
    # The format of a three-element pitch list is:
    # * A letter index 0-6 corresponding to the pitch letter names ['C', 'D', 'E', 'F', 'G', 'A', 'B'].
    # * An accidental index 0-4 corresponding to symbolic accidental names ['bb', 'b', '', '#', '#']
    #   or 'safe' accidental names ['ff', 'f', '', 's', 'ss'].
    # * An octave index 0-10 corresponding to the pitch octave names ['00', '0', '1', '2', '3',
    #   '4', '5', '6', '7', '8', '9'].
    #
    # If the argument is not a pitch string, a pitch list, or None the method
    # should raise a TypeError.  If the string or list contains invalid information the
    # method should raise a ValueError.
    #
    # Examples: Pitch('C4'), Pitch('F#2'), Pitch('Gs8'), Pitch('Bb3'), Pitch("Df00"),
    # Pitch([0,3,6]), Pitch()

    def __init__(self, ref=None):
        # FIRST CASE: an empty pitch initializes everything as None
        if ref is None:
            self.letter = None
            self.accidental = None
            self.octave = None
            self.midi_val = None
            self.pitch_class = None
            self.pitch_string = None

        # SECOND CASE: a pitch string will be parsed and converted into all instance values
        elif type(ref) == str:
            # check if pitch starts with letter name
            if ref[0].isalpha():
                pitch_classes = {
                    "C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11
                }
                # check if pitch has sharps or flats
                if ref.find("#") == ref.find("s") == ref.find("b") == ref.find("f") == -1:
                    has_accidental = False
                    accidental_modifier = 0
                    self.accidental = 2
                    if len(ref) > 3:
                        raise ValueError(f"{ref} is not a valid pitch string."
                                         "\nValid octave numbers range from 00, 0, 1, 2, ..., 8, 9")
                else:
                    has_accidental = True
                    if (ref[1:3] == "#" or ref[1:3] == "ss") and ref.find("b") == ref[1:3].find("f") == -1:
                        accidental_modifier = 2
                        self.accidental = 4
                    elif (ref[1:3] == "bb" or ref[1:3] == "ff") and ref.find("#") == ref.find("s") == -1:
                        accidental_modifier = -2
                        self.accidental = 0
                    elif (ref[1] == "#" or ref[1] == "s") and ref.find("b") == ref[1:3].find("f") == -1:
                        accidental_modifier = 1
                        self.accidental = 3
                    elif (ref[1] == "b" or ref[1] == "f") and ref.find("#") == ref.find("s") == -1:
                        accidental_modifier = -1
                        self.accidental = 1
                    else:
                        raise ValueError("{} is not a valid pitch string."
                                         "\nFor sharps, use # or s after letter name (C#4, Ds5, E#2, Fss0)"
                                         "\nFor flats, use b or f after letter name (Db2, Gf5, Ebb7, Aff2)"
                                         .format(ref))

                if has_accidental or ref[1].isnumeric():
                    # check if octave is 00 or otherwise
                    if ref.find("00") == -1:
                        # this case is for 0-9
                        if ref[len(ref) - 2].isnumeric() or len(ref) > 4:
                            raise ValueError(f"{ref} is not a valid pitch string."
                                             "\nAccidentals can only go up to double sharps (# or ss) or flats (bb or ff)"
                                             "\nValid octave numbers range from 00, 0, 1, 2, ..., 8, 9")
                        else:
                            octave = int(ref[len(ref) - 1]) + 1
                            self.octave = int(ref[len(ref) - 1]) + 1
                    else:
                        octave = 0
                        self.octave = 0
                    pitch_class = pitch_classes[ref[0].capitalize()]
                    letter_classes = {
                        "C": 0, "D": 1, "E": 2, "F": 3, "G": 4, "A": 5, "B": 6
                    }
                    self.letter = letter_classes[ref[0].capitalize()]
                else:
                    raise ValueError("{} is not a valid pitch string."
                                     "\nFor sharps, use # or s after letter name (C#4, Ds5, E#2, Fss0)"
                                     "\nFor flats, use b or f after letter name (Db2, Gf5, Ebb7, Aff2)"
                                     "\nUse an octave in range 00, 0, 1, 2, ... 8, 9 immediately"
                                     " after letter name".format(ref))

                # compute & return the midi int once all information is gathered from pitch str
                midi_val = octave * 12 + pitch_class + accidental_modifier
                if 0 <= midi_val <= 127 and 1 <= len(ref) <= 5:
                    self.midi_val = midi_val
                    self.pitch_class = self.midi_val % 12
                    # assign and clean up pitch string
                    temp_pitch_string = ref
                    temp_pitch_string = temp_pitch_string.capitalize()
                    temp_pitch_string = temp_pitch_string.replace('s', '#')
                    temp_pitch_string = temp_pitch_string.replace('f', 'b')
                    self.pitch_string = temp_pitch_string
                else:
                    raise ValueError(
                        "{} is not a valid pitch string. \nThe lowest possible pitch is 'C00' (key number 0) "
                        "\nand the highest is 'Abb9' (key number 127 spelled with a double flat)".format(ref))
            else:
                raise ValueError(
                    "{} is not a valid pitch string. A pitch name starts with a pitch letter A-G".format(ref))

        # THIRD CASE: a list of three ints representing letter, acci, and octave will be converted to midi and then
        # parsed into all the other remaining instance variables
        elif type(ref) == list:
            if len(ref) == 3:
                if isinstance(ref[0], int) and isinstance(ref[1], int) and isinstance(ref[2], int):
                    if 0 <= ref[0] <= 6 and 0 <= ref[1] <= 4 and 0 <= ref[2] <= 10:
                        self.letter = ref[0]
                        self.accidental = ref[1]
                        self.octave = ref[2]
                        # this changes the parameter (with A-G corresponding to 0-6) to be measured in a
                        # pitch class that is easier to use when calculating a MIDI value
                        letter_class_to_pitch_class = {
                            0: 0, 1: 2, 2: 4, 3: 5, 4: 7, 5: 9, 6: 11
                        }
                        self.midi_val = self.octave * 12 + letter_class_to_pitch_class[self.letter] + (
                                    self.accidental - 2)
                        if self.midi_val < 0 or self.midi_val > 127:
                            raise ValueError(
                                "The integer values made a MIDI value that is out of range."
                                "\nThe lowest possible pitch is 'C00' (key number 0) "
                                "\nand the highest is 'Abb9' (key number 127 spelled with a double flat)")
                        self.pitch_class = self.midi_val % 12
                        self.pitch_string = Pitch.from_keynum(self.midi_val, self.accidental)
                    else:
                        raise ValueError("All values in a pitch list must be integers."
                                         "\nThe first value is for letters, which includes indices 0-6."
                                         "\nThe second value is for accidentals, which includes indices 0-4."
                                         "\nThe third value is for octaves, which includes indices 0-10.")
                else:
                    raise ValueError("All values in a pitch list must be integers."
                                     "\nThe first value is for letters, which includes indices 0-6."
                                     "\nThe second value is for accidentals, which includes indices 0-4."
                                     "\nThe third value is for octaves, which includes indices 0-10.")
            else:
                raise ValueError(f"The parameter is not a valid pitch list."
                                 f"\nThe pitch list must have 3 integer values "
                                 f"for a letter, accidental, and octave index.")
        else:
            raise TypeError(f"{ref} is not a valid parameter. Create a Pitch object with a pitch string, pitch list,"
                            f"\nor without any value (creates an empty Pitch).")

    # Returns a string displaying information about the
    #  pitch within angle brackets. Information includes the
    #  the class name, the pitch text, and the id of the object,
    #  for example '<Pitch: C#7 0x10f263e10>'. If the pitch is
    #  empty the string will show '<Pitch: empty 0x10f263b50>'.
    #  See also: string().
    def __str__(self):
        return f'<Pitch: {self.pitch_string} {hex(id(self))}>'

    # Prints the external form of the Pitch that, if evaluated
    #  would create a Pitch with the same content as this pitch.
    #  Examples: 'Pitch("C#7")' and Pitch().  See also string().
    def __repr__(self):
        return f'Pitch("{self.pitch_string}")'

    # Implements Pitch < Pitch.
    # @param other The pitch to compare with this pitch.
    # @returns True if this Pitch is less than the other.
    #
    # This method should call self.pos() and other.pos() to get the
    # two values to compare. See: pos().
    def __lt__(self, other):
        if isinstance(other, Pitch):
            if self.pos() < other.pos():
                return True
            else:
                return False
        else:
            raise TypeError("Pitch comparisons can only be performed between two Pitches.")

    # Implements Pitch <= Pitch.
    # @param other The pitch to compare with this pitch.
    # @returns True if this Pitch is less than or equal to the other.
    #
    # A TypeError should be raised if other is not a Pitch.
    # This method should call self.pos() and other.pos() to get the
    # values to compare. See: pos().
    def __le__(self, other):
        if isinstance(other, Pitch):
            if self.pos() <= other.pos():
                return True
            else:
                return False
        else:
            raise TypeError("Pitch comparisons can only be performed between two Pitches.")

    # Implements Pitch == Pitch.
    # @param other The pitch to compare with this pitch.
    # @returns True if this Pitch is equal to the other.
    #
    # A TypeError should be raised if other is not a Pitch.
    # This method should call self.pos() and other.pos() to get the
    # values to compare. See: pos().
    def __eq__(self, other):
        if isinstance(other, Pitch):
            if self.pos() == other.pos():
                return True
            else:
                return False
        else:
            raise TypeError("Pitch comparisons can only be performed between two Pitches.")

    # Implements Pitch != Pitch.
    # @param other The pitch to compare with this pitch.
    # @returns True if this Pitch is not equal to the other.
    #
    # A TypeError should be raised if other is not a Pitch.
    # This method should call self.pos() and other.pos() to get the
    # values to compare. See: pos().
    def __ne__(self, other):
        if isinstance(other, Pitch):
            if self.pos() != other.pos():
                return True
            else:
                return False
        else:
            raise TypeError("Pitch comparisons can only be performed between two Pitches.")

    # Implements Pitch >= Pitch.
    # @param other The pitch to compare with this pitch.
    # @returns True if this Pitch is greater or equal to the other.
    #
    # A TypeError should be raised if other is not a Pitch.
    # This method should call self.pos() and other.pos() to get the
    # values to compare. See: pos().
    def __ge__(self, other):
        if isinstance(other, Pitch):
            if self.pos() >= other.pos():
                return True
            else:
                return False
        else:
            raise TypeError("Pitch comparisons can only be performed between two Pitches.")

    # Implements Pitch > Pitch.
    # @param other The pitch to compare with this pitch.
    # @returns True if this Pitch is greater than the other.
    #
    # A TypeError should be raised if other is not a Pitch.
    # This method should call self.pos() and other.pos() to get the
    # values to compare. See: pos().
    def __gt__(self, other):
        if isinstance(other, Pitch):
            if self.pos() > other.pos():
                return True
            else:
                return False
        else:
            raise TypeError("Pitch comparisons can only be performed between two Pitches.")

    # Returns a unique integer representing this pitch's position in
    #  the octave-letter-accidental space. The expression to calculate
    #  this value is (octave<<8) + (letter<<4) + accidental.
    def pos(self):
        return (self.octave << 8) + (self.letter << 4) + self.accidental

    # Returns true if the Pitch is empty. A pitch is empty if its
    # letter, accidental and octave attributes are None. Only one of
    # these attributes needs to be checked because __init__ will only
    # create a Pitch if all three are legal values or all three are None.
    def is_empty(self):
        if self.letter is None:
            return True
        else:
            return False

    # Returns a string containing the pitch name including the
    #  letter, accidental, and octave.  For example,
    #  Pitch("C#7").string() would return 'C#7'.
    def string(self):
        return self.pitch_string

    # Returns the midi key number of the Pitch.
    def keynum(self):
        return self.midi_val

    # Returns the pnum (pitch class enum) of the Pitch. Pnums enumerate
    #  and order the letter and accidental of a Pitch so they can be compared,
    #  e.g.: C < C# < Dbb. See also: pnums.
    def pnum(self):  # @TODO
        pass

    # Returns the pitch class (0-11) of the Pitch.
    def pc(self):
        return self.pitch_class

    # Returns the hertz value of the Pitch.
    def hertz(self):
        return 440.0 * 2 ** ((self.midi_val - 69) / 12)

    # A @classmethod that creates a Pitch for the specified
    #  midi key number.
    #  @param keynum A valid keynum 0-127.
    #  @param acci  The accidental to use. If no accidental is provided
    #  a default is chosen from C C# D Eb F F# G Ab A Bb B
    #  @returns a new Pitch with an appropriate spelling.
    #
    #  The function should raise a ValueError if the midi key number
    #  is invalid or if the pitch requested does not support the specified
    #  accidental.
    @classmethod
    def from_keynum(cls, keynum, acci=None):  # @TODO
        if isinstance(keynum, int) and 0 <= keynum <= 127:
            octave_names = ['00', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            pitch_classes = {
                0: "C", 1: "C#", 2: "D", 3: "Eb", 4: "E", 5: "F",
                6: "F#", 7: "G", 8: "Ab", 9: "A", 10: "Bb", 11: "B"
            }
            pitch_class = keynum % 12
            octave_int = keynum // 12
            if acci is not None:
                if acci == "#" or acci == 's' or acci == 3:
                    pitch_classes = {
                        0: "B#", 1: "C#", 3: "D#", 5: "E#", 6: "F#", 8: "G#", 10: "A#"
                    }
                    if pitch_class == 0:
                        octave_int -= 1
                elif acci == "##" or acci == 'ss' or acci == 4:
                    pitch_classes = {
                        1: "B##", 2: "C##", 4: "D##", 6: "E##", 7: "F##", 9: "G##", 11: "A##"
                    }
                    if pitch_class == 0:
                        octave_int -= 1
                elif acci == "b" or acci == 'f' or acci == 1:
                    pitch_classes = {
                        1: "Db", 3: "Eb", 4: "Fb", 6: "Gb", 8: "Ab", 10: "Bb", 11: "Cb"
                    }
                    if pitch_class == 11:
                        octave_int += 1
                elif acci == "bb" or acci == 'ff' or acci == 0:
                    pitch_classes = {
                        0: "Dbb", 2: "Ebb", 3: "Fbb", 5: "Gbb", 7: "Abb", 9: "Bbb", 10: "Cbb"
                    }
                    if pitch_class == 10:
                        octave_int += 1
                else:
                    raise ValueError(f"{acci} is not a valid accidental value."
                                     f"\nPlease use #, ##, b, or bb for accidentals")

            if pitch_classes.get(pitch_class, -1) == -1:
                raise ValueError(f"{acci} is not a valid accidental for the midi value {keynum}")

            pitch = pitch_classes[pitch_class] + octave_names[octave_int]
            return Pitch(pitch)
        else:
            raise TypeError("The MIDI key number must be an integer in range 0-127.")

