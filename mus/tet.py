###############################################################################
## @file
#  Twelve-tone Equal Temperament (TET).
#
#  The standard scale in western music divides the octave into twelve equal
#  divisions tuned to the frequency of A440 (440 Hertz). This module defines
#  an API that allows users to map between four common representations of
#  TET information:
#  1. Hertz frequency (cycles per second). A440 is 440.0 Hz and middle C
#     is 261.625 Hz.
#  2. MIDI key numbers (integers). MIDI key numbers range from 0 to 127.
#     A440 is the MIDI key number 69 and middle C is key number 60.
#  3. Pitch names (strings). A pitch name consists of a letter, an optional
#     accidental, and an octave number. The middle C octave is 4, so A440
#     is the pitch string 'A4' and middle C is 'C4'. The pitch strings 'B#3'
#     and 'Dbb4' are enharmonic spellings of 'C4', etc.
#  4. Pitch classes (integers). PCs range from 0 to 11 and represent the
#     ordinal positions of the chromatic scale without respect to octaves
#     or pitch spelling.  For example, the PC 0 represents any key number
#     or pitch that sounds like some octave multiple of 'C': e.g. 60,
#     72, 'C3', 'C5', 'B#4', 'Dbb8',  and so on.

import math


## Returns the midi key number for a given hertz frequency.
#  The formula for mapping frequency to midi key numbers is
#  69 + log2(hertz/440.0) * 12 rounded to the nearest integer.
#  @param hertz  The hertz frequency to convert.
#  @returns  An integer midi key number 0 - 127.
#
#  The function should raise a ValueError if the input
#  is not a positive number or does not produce a valid
#  midi key number.
def hertz_to_midi(hertz):
    if hertz < 0:
        raise ValueError("The value {} failed because it is negative. Choose a positive value.".format(hertz))
    elif hertz < midi_to_hertz(0):
        raise ValueError("The value {} failed because it is too low. "
                         "The frequency of the lowest possible MIDI note is ~8.18 Hz".format(hertz))
    elif hertz > midi_to_hertz(127):
        raise ValueError("The value {} failed because it is too high. "
                         "The frequency of the highest possible MIDI note is ~12,543.85 Hz".format(hertz))
    else:
        return round(69 + math.log2(hertz/440.0) * 12)


## Returns the hertz value for a given midi key number.
#  The formula for mapping midi key numbers into hertz is
#  440.0 * 2 ** ((midi-69)/12).
#  @param midi  The midi key number to convert.
#  @returns the hertz frequency of the midi key number.
#
#  The function should raise a ValueError if the input
#  is not a valid midi key number.
def midi_to_hertz(midi):
    if midi < 0 or midi > 127:
        raise ValueError("{} is not a valid MIDI value. MIDI values include integer values from 0 to 127.".format(midi))
    else:
        return 440.0 * 2 ** ((midi-69)/12)


## Returns the pitch class integer for a given midi key number.
#  The formula for converting a midi key number into a pitch class
#  is: midi % 12.
#  @param midi  The midi key number to convert.
#  @returns An integer pitch class 0 - 11.
#
#  The function should raise a ValueError if the input is not valid
#  midi key number.
def midi_to_pc(midi):
    if midi < 0 or midi > 127:
        raise ValueError("{} is not a valid MIDI value. MIDI values include integer values from 0 to 127.".format(midi))
    else:
        return midi % 12


## Converts a pitch name into a midi key number. The BNF grammar of a
#  pitch string is:
# @code
#  <pitch> :=  <letter>, [<accidental>], <octave>
#  <letter> := 'C' | 'D' | 'E' | 'F' | 'G' | 'A' | 'B'
#  <accidental> := <2flat> | <flat> | <natural> | <sharp> | <2sharp>
#  <2flat> := 'bb' | 'ff'
#  <flat> := 'b' | 'f'
#  <natural> := ''
#  <sharp> := '#' | 's'
#  <2sharp> := '##' | 'ss'
#  <octave> := '00' | '0' | '1'  | '2'  | '3'  | '4'  | '5'  | '6'
#              '7'  | '8'  | '9'
# @endcode
#  The lowest possible pitch is 'C00' (key number 0) and then highest is
#  'Abb9' (key number 127 spelled with a double flat ). The pitch 'C4' is
#  midi key number 60 and 'A4' is midi key number 69. Examples of pitch
#  names: 'C4', 'F##2', 'Gs8', 'Bb3', 'Df00'.
#  @param pitch  The pitch name (string) to convert.
#  @returns An integer midi key number 0-127.
#
#  The function should signal a ValueError if the input is not a valid
#  pitch name or produces an invalid midi key number.
def pitch_to_midi(pitch):
    # check if pitch starts with letter name
    if pitch[0].capitalize().isalpha():
        pitch_classes = {
            "C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11
        }
        # check if pitch has sharps or flats
        if pitch.find("#") == pitch.find("s") == pitch.find("b") == pitch.find("f") == -1:
            has_accidental = False
            accidental_modifier = 0
        else:
            has_accidental = True
            if pitch[1:3] == "##" or pitch[1:3] == "ss":
                accidental_modifier = 2
            elif pitch[1:3] == "bb" or pitch[1:3] == "ff":
                accidental_modifier = -2
            elif pitch[1] == "#" or pitch[1] == "s":
                accidental_modifier = 1
            elif pitch[1] == "b" or pitch[1] == "f":
                accidental_modifier = -1
            else:
                raise ValueError("{} is not a valid pitch name."
                                 "\nFor sharps, use # or s after letter name (C#4, Ds5, E##2, Fss0)"
                                 "\nFor flats, use b or f after letter name (Db2, Gf5, Ebb7, Aff2)".format(pitch))

        if has_accidental or pitch[1].isnumeric():
            # check if octave is 00 or otherwise
            if pitch.find("00") == -1:
                # this case is for 0-9
                octave = int(pitch[len(pitch) - 1]) + 1
            else:
                octave = 0
            pitch_class = pitch_classes[pitch[0]]
        else:
            raise ValueError("{} is not a valid pitch name."
                             "\nFor sharps, use # or s after letter name (C#4, Ds5, E##2, Fss0)"
                             "\nFor flats, use b or f after letter name (Db2, Gf5, Ebb7, Aff2)"
                             "\nFor naturals, use an octave in range 00, 1, 2, ... 8, 9 immediately"                                 
                             " after letter name".format(pitch))

        # compute & return the midi int once all information is gathered from pitch str
        midi_val = octave * 12 + pitch_class + accidental_modifier
        if 0 <= midi_val <= 127 and 1 <= len(pitch) <= 4:
            return midi_val
        else:
            raise ValueError("{} is not a valid pitch name. \nThe lowest possible pitch is 'C00' (key number 0) "
                             "\nand the highest is 'Abb9' (key number 127 spelled with a double flat)")
    else:
        raise ValueError("{} is not a valid pitch name. A pitch name starts with a pitch letter A-G".format(pitch))


## Returns a pitch name for the given key number.
#  If no accidental is proved in the call, white key numbers produce
#  pitch names with no accidentals and black key numbers return C# Eb F# Ab Bb.
#  If an accidental is provided the pitch returned must use that accidental.
#  @param midi  the integer midi key number to convert.
#  @param accidental an optional argument that forces the returned pitch
#  to use the accidental provided
#  @returns A midi pitch name.
#
#  The function should raise a ValueError if the midi key number
#  is invalid or if the pitch requested does not support the specified
#  accidental.
def midi_to_pitch(midi, accidental=None):
    pitch_class = midi_to_pc(midi)
    octave_int = midi // 12
    accidental_val = 0
    octave_names = ['00', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    pitch_classes = {
        0: "C", 2: "D", 4: "E", 5: "F", 7: "G", 9: "A", 11: "B"
    }
    pitch = pitch_classes[pitch_class] + octave_names[octave_int]
    return pitch

    # get pitch class
    # get octave

## Returns a pitch name for the given hertz value.
#  Hint: first convert the hertz value to midi.
#  @param hertz  The integer midi key number to convert.
#  @returns A floating point hertz value.
def hertz_to_pitch(hertz):
    pass


## Returns a hertz value for the given pitch.
#  Hint: first convert the pitch to midi.
#  @param pitch  The pitch name to convert.
#  @returns A floating point hertz value.
def pitch_to_hertz(pitch):
    midi_val = pitch_to_midi(pitch)
    return midi_to_hertz(midi_val)


###############################################################################
# There are two methods you can use to test out code as you develop it.
#
# 1. Interactive testing: Start your Python interpreter, import the module 
#    (python file) that you are working on and then call your code:
#
#    >>> import tet
#    >>> pitch_to_hertz('A4')
#        440.0
#    >>> midi_to_pitch(72)
#        'C5'
#
# 2. Script testing: Start python in 'script' mode by giving it the file
#    you are working on. When Python loads the file it will evaluate all
#    definitions including a special 'if' block that you can put at the
#    end of the file. If this block exists then the code you put inside
#    the if statement (e.g. your testing code) will also be executed. To
#    define the block add this statement to the end of your file but with
#    the work 'pass' replaced by your testing code:
#
#    if __name__ == 'main':
#        pass
#
#    To run the file as python script use your IDE's 'Run' command. If
#    you are using the terminal, provide the file directly to the Python
#    command like this:
#
#    $ python3 /path/to/myfile.py 
#
#    See https://www.cs.bu.edu/courses/cs108/guides/runpython.html for more info.

if __name__ == '__main__':
    print("Testing...")
    print(midi_to_pitch(2))
    print("Done!")

