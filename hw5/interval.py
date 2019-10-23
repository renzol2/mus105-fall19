########################################

from .pitch import Pitch

# A class that implements musical intervals.
#
#  An Interval measures the distance between two Pitches. Interval distance
#  can be measured in different ways, for example using lines-and-spaces,
#  semitones, ratios, or cents. In western music theory an interval distance is
#  measured using 'span' (number of lines and spaces) and 'quality' (a chromatic
#  adjustment to the size). The Interval class supports the standard interval
#  names and classification system, including the notion of descending or
#  ascending intervals and simple or compound intervals.
#  Intervals can be numerically compared for their size (span+quality) and
#  can be used to transpose Pitches.
#
#  An Interval contains four integer attributes:
#  * span  The number of lines and spaces the interval moves (0-7).
#  * qual  The quality of the interval (0-12).
#  * xoct  The 'extra octaves' spanned by compound intervals (0-10).
#  * sign  1 for ascending intervals, -1 for descending.
#
#  See also: https://en.wikipedia.org/wiki/Interval_(music)


class Interval:
    # qualities
    _5dim_qual, _4dim_qual, _3dim_qual, _2dim_qual, _dim_qual, _minor_qual, _perfect_qual, _major_qual, \
        _aug_qual, _2aug_qual, _3aug_qual, _4aug_qual, _5aug_qual = range(13)

    # spans
    _unison_span, _second_span, _third_span, _fourth_span, \
        _fifth_span, _sixth_span, _seventh_span, _octave_span = range(8)

    # letters
    _C, _D, _E, _F, _G, _A, _B = range(7)

    # perfect spans
    perfect = {_unison_span, _fourth_span, _fifth_span, _octave_span}

    # imperfect qualities
    imperfect_quals = {_minor_qual, _major_qual}

    quals = {'ooooo': _5dim_qual, 'oooo': _4dim_qual, 'ooo': _3dim_qual, 'oo': _2dim_qual, 'o': _dim_qual,
             'm': _minor_qual, 'P': _perfect_qual, 'M': _major_qual,
             '+': _aug_qual, '++': _2aug_qual, '+++': _3aug_qual, '++++': _4aug_qual, '+++++': _5aug_qual}

    quals_to_string = {}
    for k, v in quals.items():
        quals_to_string[v] = k

    quals_to_names = {_5dim_qual: "quintuply-diminished", _4dim_qual: "quadruply-diminished",
                      _3dim_qual: "triply-diminished", _2dim_qual: "doubly-diminished",
                      _dim_qual: "diminished", _minor_qual: "minor", _perfect_qual: "perfect",
                      _major_qual: "major", _aug_qual: "augmented", _2aug_qual: "doubly-augmented",
                      _3aug_qual: "triply-augmented", _4aug_qual: "quadruply-augmented",
                      _5aug_qual: "quintuply-augmented"}

    spans_to_names = {_unison_span: "unison", _second_span: "second", _third_span: "third", _fourth_span: "fourth",
                      _fifth_span: "fifth", _sixth_span: "sixth", _seventh_span: "seventh", _octave_span: "octave"}


    # Creates an Interval from a string, list, or two Pitches.
    #  * Interval(string) - creates an Interval from a pitch string.
    #  * Interval([s, q, x, s]) - creates a Pitch from a list of four
    #  integers: a span, quality, extra octaves and sign. (see below).
    #  * Interval(pitch1, pitch2) - creates an Interval from two Pitches.
    #
    #  @param arg If only arg is specified it should be either an
    #  interval string or a list of four interval indexes.  If both
    #  arg and other are provided, both should be a Pitch.
    #  @param other A Pitch if arg is a Pitch, otherwise None.
    #
    # The format of a Interval string is:
    #  @code
    #  interval  = ["-"] , <quality> , <span>
    #  <quality> = <diminished> | <minor> | <perfect> | <major> | <augmented>
    #  <diminished> = <5d> , <4d> , <3d> , <2d> , <1d> ;
    #  <5d> = "ooooo" | "ddddd"
    #  <4d> = "oooo" | "dddd"
    #  <3d> = "ooo" | "ddd"
    #  <2d> = "oo" | "dd"
    #  <1d> = "o" | "d"
    #  <minor> = "m"
    #  <perfect> = "P"
    #  <major> = "M"
    #  <augmented> = <5a>, <4a>, <3a>, <2a>, <1a>
    #  <5d> = "+++++" | "aaaaa"
    #  <4d> = "++++" | "aaaa"
    #  <3d> = "+++" | "aaa"
    #  <2d> = "++" | "aa"
    #  <1d> = "+" | "a"
    #  <span> = "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ...
    # @endcode
    #
    # The __init__function should check to make sure the arguments are either a string, a
    # list of four integers, or two pitches.  If the input is a string then __init__ should
    # pass the string to the the private _init_from_string() method (see below).  If the
    # input is a list of four ints, __init__ will pass them to the private _init_from_list()
    # method (see below). If the input is two pitches they will be passed to the private
    # _init_from_pitches() method (see below).  Otherwise (if the input is not
    # a string, list of four integers, or two pitches) the method will raise a TypeError
    # for the offending value.
    def __init__(self, arg, other=None):
        # Initialize instance variables
        self.span = None
        self.qual = None
        self.xoct = None
        self.sign = None
        self.interval_string = None
        # CASE 1: Argument is an INTERVAL STRING that must be parsed into components and stored appropriately.
        if isinstance(arg, str) and other is None:
            self._init_from_string(arg)

        # CASE 2: Argument is an INTERVAL LIST with 4 params that must be stored appropriately.
        elif isinstance(arg, list) and other is None:
            if len(arg) == 4 and isinstance(arg[0], int) and isinstance(arg[1], int)\
                        and isinstance(arg[2], int) and isinstance(arg[3], int):
                self._init_from_list(*arg)
            else:
                raise ValueError(f"The parameter is not a valid integer list."
                                 f"\nThe pitch list must have 4 integer values "
                                 f"for a span, quality, octave index, and sign.")

        # CASE 3: Arguments are TWO PITCH OBJECTS and the interval must be found between them.
        elif isinstance(arg, Pitch) and isinstance(other, Pitch):
            self._init_from_pitches(arg, other)

        else:
            raise TypeError("Invalid parameter for Interval. Intervals can be made using"
                            "interval strings, lists with four parameters, or with two"
                            "Pitch objects.")

    # A private method that checks four integer values (span, qual, xoct, sign) to make sure
    # they are valid index values for the span, qual, xoct and sign attributes. Legal values
    # are: span 0-7, qual 0-12, xoct 0-10, sign -1 or 1. If any value is out of range the
    # method will raise a ValueError for that value. If all values are legal the method will
    # make the following 'edge case' tests:
    # * span and quality values cannot produce negative semitones, i.e. an interval
    #   whose 'top' would be lower that its 'bottom'. Here are the smallest VALID 
    #   interval for each span that could cause this: perfect unison, diminished-second,
    #   triply-diminished third.
    # * Only the span of a fifth can be quintuply diminished.
    # * Only the span of a fourth can be quintuply augmented.
    # * No interval can surpass 127 semitones, LOL. The last legal intervals are: 'P75'
    #  (a 10 octave perfect 5th), and a 'o76' (a 10 octave diminished 6th) 
    # * If a user specifies an octave as a unison span with 1 extra octave, e.g. [0,*,1,*],
    # it should be converted to an octave span with 0 extra octaves, e.g. [7,*,0,*]
    #
    # Only if all the edge case checks pass then _init_from_list() should assign
    # the four values to the attributes, e.g. self.span=span, self.qual=qual, and
    # so on. Otherwise if any edge case fails the method should raise a ValueError.
    def _init_from_list(self, span, qual, xoct, sign):
        if 0 <= span <= 7 and 0 <= qual <= 12 and 0 <= xoct <= 10 and abs(sign) == 1:
            # Set the sign from the fourth value and the quality from the third value.
            self.sign = sign
            self.qual = qual

            # Compare span to qual to make sure they're compatible.
            # If the span is a perfect interval, then the quality cannot be major or minor.
            if span in Interval.perfect and self.qual not in Interval.imperfect_quals:
                self.span = span

            # If the span is an imperfect interval, then the quality cannot be perfect.
            elif span not in Interval.perfect and self.qual != Interval._perfect_qual:
                self.span = span
            else:
                raise ValueError("Invalid interval list. Perfect intervals must use perfect qualities and"
                                 " imperfect intervals must use imperfect qualities.")

            # Set octave
            self.xoct = xoct

            # Check edge cases
            # A* span and quality values cannot produce negative semitones, i.e. an interval
            #   whose 'top' would be lower that its 'bottom'. Here are the smallest VALID
            #   interval for each span that could cause this: perfect unison, diminished-second,
            #   triply-diminished third.
            # B* Only the span of a fifth can be quintuply diminished.
            # C* Only the span of a fourth can be quintuply augmented.
            # D* No interval can surpass 127 semitones, LOL. The last legal intervals are: 'P75'
            #  (a 10 octave perfect 5th), and a 'o76' (a 10 octave diminished 6th)
            # E* If a user specifies an octave as a unison span with 1 extra octave, e.g. [0,*,1,*],
            #  it should be converted to an octave span with 0 extra octaves, e.g. [7,*,0,*]

            # edge case A
            # only applies if the interval is in the same octave
            if self.xoct == 0:
                if self.span == Interval._unison_span and self.qual < Interval._perfect_qual:
                    raise ValueError("Invalid interval. Unison intervals can only"
                                     " have a quality of perfect and higher.")
                elif self.span == Interval._second_span and self.qual < Interval._dim_qual:
                    raise ValueError("Invalid interval. Second intervals can only"
                                     " have a quality of diminished and higher.")
                elif self.span == Interval._third_span and self.qual < Interval._3dim_qual:
                    raise ValueError("Invalid interval. Third intervals can only"
                                     " have a quality of triply diminished and higher.")

            # edge case B + C
            if self.qual == Interval._5dim_qual and self.span != Interval._fifth_span:
                raise ValueError("Invalid interval. Only the span of a fifth can be quintuply diminished.")
            if self.qual == Interval._5aug_qual and self.span != Interval._fourth_span:
                raise ValueError("Invalid interval. Only the span of a fourth can be quintuply augmented.")

            # edge case D
            if self.xoct > 10:
                raise ValueError("Invalid interval. Interval is too big (10+ octaves)")
            elif self.xoct == 10:
                if self.span > Interval._sixth_span:
                    raise ValueError("Invalid interval. Interval is too big (Greater than sixth at 10 octaves)")
                else:
                    if self.span == Interval._sixth_span:
                        if self.qual > Interval._dim_qual:
                            raise ValueError("Invalid interval. Interval is too big "
                                             "(Greater than diminished sixth at 10 octaves)")
                    elif self.span == Interval._fifth_span:
                        if self.qual > Interval._perfect_qual:
                            raise ValueError("Invalid interval. Interval is too big "
                                             "(Greater than perfect fifth at 10 octaves)")

            # edge case E
            if self.span == Interval._unison_span and self.xoct == 1:
                self.span = Interval._octave_span
                self.xoct = 0

            # Concatenate string using four values... but only if it wasn't made by init_to_string already
            if self.interval_string is None:
                if self.sign == -1:
                    sign_string = '-'
                else:
                    sign_string = ''
                qual_string = Interval.quals_to_string[self.qual]
                span_string = str(self.span + 1 + Interval._octave_span * self.xoct)
                self.interval_string = sign_string + qual_string + span_string

        else:
            raise ValueError("All values in an interval list must be integers."
                             "\nThe first value is for span, which includes indices 0-7."
                             "\nThe second value is for quality, which includes indices 0-12."
                             "\nThe third value is for octaves, which includes indices 0-10."
                             "\nThe fourth value is for sign, which must be -1 or 1.")

    # A private method that accepts an interval string and parses it into four
    # integer values: span, qual, xoct, sign. If all four values can be parsed
    # from the string they should be passed to the _init_from_list() method to
    # check the values and assign them to the instance's attributes. A ValueError
    # should be raised for any value that cannot be parsed from the string. See:
    # _init_from_list().
    def _init_from_string(self, string):
        # ... parse the string into a span, qual, xoct and sign values
        if len(string) != 0:
            # Use a temporary string (if temp_arg passes the parsing,
            # then arg will be used as the final Interval string.)
            # Method is to continuously delete components as they are parsed
            # to ensure that the string is valid/in the right order, which necessitates
            # the need for a temporary string.
            temp_arg = string

            # Replace safe with symbolics
            temp_arg = temp_arg.replace('d', 'o')
            temp_arg = temp_arg.replace('a', '+')
            temp_arg = temp_arg.replace('D', 'o')
            temp_arg = temp_arg.replace('A', '+')

            # First check for descending intervals
            if temp_arg.find('-') != -1:
                if temp_arg[0] == '-':
                    sign = -1
                    temp_arg = temp_arg.replace('-', '')
                else:
                    raise ValueError("Invalid interval string. To denote descending intervals, "
                                     "place a '-' at the beginning of the interval string.")
            else:
                sign = 1

            # Next, check for the quality
            if Interval.quals.get(temp_arg[0]) is not None:
                if temp_arg[0] == 'o' or temp_arg[0] == '+':
                    count = temp_arg.count(temp_arg[0])
                    temp_qual = ''
                    for i in range(count):
                        temp_qual += temp_arg[0]
                    qual = Interval.quals[temp_qual]
                    temp_arg = temp_arg.replace(temp_qual, '')
                else:
                    qual = Interval.quals[temp_arg[0]]
                    temp_arg = temp_arg.replace(temp_arg[0], '')
            else:
                raise ValueError("Invalid interval string. The quality of the interval must be valid.")

            # Finally, check for the span
            # Must check if span is COMPATIBLE with qual, i.e. perfects must be with spans 0, 3, 4, 7
            if temp_arg.isnumeric():
                if int(temp_arg) > 0:
                    temp_span = (int(temp_arg) - 1) % 7
                    if temp_span in Interval.perfect and qual not in Interval.imperfect_quals:
                        span = temp_span
                    elif temp_span not in Interval.perfect and qual != Interval._perfect_qual:  # qual is not perfect
                        span = temp_span
                    else:
                        raise ValueError("Invalid interval string. Perfect intervals must use perfect qualities and"
                                         " imperfect intervals must use imperfect qualities.")
                    xoct = (int(temp_arg) - 1) // 7
                else:
                    raise ValueError("Invalid interval string. The span of the interval must be greater than 0.")
            else:
                raise ValueError("Invalid interval string. The span of the "
                                 "interval must be an integer greater than 0.")

            # If the string parsing succeeds, the original string is valid.
            # Set it to a variable for str and repr to use... but change safes to symbolics after.
            self.interval_string = string
            self.interval_string = self.interval_string.replace('d', 'o')
            self.interval_string = self.interval_string.replace('D', 'o')
            self.interval_string = self.interval_string.replace('A', '+')
            self.interval_string = self.interval_string.replace('a', '+')
        else:
            raise ValueError("Invalid interval string. Interval strings must include a quality and span.")

        # ... pass on to check an assign instance attributes.
        self._init_from_list(span, qual, xoct, sign)

    # A private method that determines appropriate span, qual, xoct, sign
    # from two pitches. If pitch2 is lower than pitch1 then a descending
    # interval should be formed. The values should be passed to the
    # _init_from_list() method to initialize the interval's attributes.
    # See: _init_from_list().
    #
    # Do NOT implement this method yet.
    def _init_from_pitches(self, pitch1, pitch2):
        # First, find span and sign
        pitch1_letter = pitch1.letter
        pitch2_letter = pitch2.letter
        if pitch1 <= pitch2:
            sign = 1
        else:
            sign = -1
        span = ((pitch2_letter - pitch1_letter) * sign) % Interval._octave_span

        # differentiate between octave and unison
        semi = int((pitch2.keynum() - pitch1.keynum()) * sign)
        if span == Interval._unison_span and semi > 4:
            span = Interval._octave_span

        # manually check if there are invalid small intervals:
        if sign == 1 and semi < 0:
            raise ValueError("Invalid interval. Smaller pitch has larger keynum than larger pitch. Likely due to "
                             "an excess of sharps on smaller pitch or flats on larger pitch.")

        # Finding the smaller pitch for use in xoct and qual
        if sign > 0:
            smaller_pitch = pitch1
            larger_pitch = pitch2
        else:
            smaller_pitch = pitch2
            larger_pitch = pitch1

        # Finding the octave
        xoct = abs((pitch2.keynum() - pitch1.keynum())) // 12
        # if a simple interval passes an octave in midi keyvals through accidentals, it will accidentally
        # create an extra octave, so we want to get rid of it
        # - if it's a sixth and
        if span == Interval._octave_span or (Interval._sixth_span <= span < Interval._octave_span and xoct > 0
            and (smaller_pitch.accidental < 2 or larger_pitch.accidental > 2)):
            xoct -= 1

        # Finding qual:
        # handle perfect and imperfect intervals differently
        # if the span is perfect (0, 3, 4, 7):
        #  find the semitonal difference of the PERFECT version (in midi)
        #  compare that to the actual difference of the midi vals

        # Key(span): Object(semitonal difference in midi)

        # ex. Perfect fifth (4): 7 semitones apart (7)
        perfect_differences = {Interval._unison_span: 0, Interval._fourth_span: 5,
                               Interval._fifth_span: 7, Interval._octave_span: 12}

        # ex. Minor third (2): 3 semitones apart (3)
        imperfect_minor_differences = {Interval._second_span: 1, Interval._third_span: 3,
                                       Interval._sixth_span: 8, Interval._seventh_span: 10}

        # ex. Major third (2): 4 semitones apart (4)
        imperfect_major_differences = {Interval._second_span: 2, Interval._third_span: 4,
                                       Interval._sixth_span: 9, Interval._seventh_span: 11}

        # the actual difference of midi values
        midi_difference = int(abs(pitch2.keynum() - pitch1.keynum()))

        if span in perfect_differences:  # if span is a key in perfect differences
            perfect_difference = perfect_differences[span]

            # if midi_offset is negative, qual is diminished
            # if midi_offset is positive, qual is augmented
            # if midi_offset is 0, qual is perfect
            if midi_difference > 12 and xoct > 0:
                midi_difference %= 12
            midi_offset = (midi_difference - perfect_difference)
            if midi_offset > 0:
                midi_offset %= 12

            # self.qual = perfect quality + any diminished/augmented discrepancy
            qual = Interval._perfect_qual + midi_offset
            # adjust for the presence of minor/major quals
            if qual > Interval._perfect_qual:
                qual += 1
            elif qual < Interval._perfect_qual:
                qual -= 1
        # Basing imperfect intervals off major:
        elif span in imperfect_major_differences:
            imperfect_difference = imperfect_major_differences[span]

            # minors
            # 2nd: E -> F, B -> C
            minor_second_letters = {Interval._E, Interval._B}
            # 3rd: D -> F, E -> G, A -> C, B -> D
            minor_third_letters = {Interval._D, Interval._E, Interval._A, Interval._B}
            # 6th: E -> C, A -> F, B -> G
            minor_sixth_letters = {Interval._E, Interval._A, Interval._B}
            # 7th: D -> C, E -> D, G -> F, A -> G, B -> A
            minor_seventh_letters = {Interval._D, Interval._E, Interval._G, Interval._A, Interval._B}

            # figure out if the interval is major or minor:
            # if the interval is actually minor, further subtract 2 from the eventual quality
            # (since major - minor = 2)
            diatonically_minor = False
            if (span == Interval._second_span and smaller_pitch.letter in minor_second_letters) or \
                    (span == Interval._third_span and smaller_pitch.letter in minor_third_letters) or \
                    (span == Interval._sixth_span and smaller_pitch.letter in minor_sixth_letters) or \
                    (span == Interval._seventh_span and smaller_pitch.letter in minor_seventh_letters):
                # this is used for decreasing major qualities to diminished
                imperfect_difference -= 1
                diatonically_minor = True

            # if midi_offset is negative, qual is diminished
            # if midi_offset is positive, qual is augmented
            # if midi_offset is 0, qual is major/minor
            if midi_difference > 12 and xoct > 0:
                midi_difference %= 12
            midi_offset = (midi_difference - imperfect_difference)

            # self.qual = perfect quality + any diminished/augmented discrepancy
            qual = Interval._perfect_qual + midi_offset
            if diatonically_minor and (qual == Interval._perfect_qual or midi_difference == 0):
                qual -= 1
            elif (not diatonically_minor and qual >= Interval._major_qual) or (qual == Interval._perfect_qual):
                qual += 1

        # ... parse the string into a span, qual, xoct and sign values
        # ... pass on to check and assign instance attributes.
        self._init_from_list(span, qual, xoct, sign)
        
    # Returns a string displaying information about the
    #  Interval within angle brackets. Information includes the
    #  the class name, the interval text, the span, qual, xoct and sign
    #  values, and the id of the object. Example:
    #  <Interval: oooo8 [7, 1, 0, 1] 0x1075bf6d0>
    #  See also: string().
    def __str__(self):
        return f'<Interval: {self.interval_string} [{self.span}, {self.qual}, ' \
               f'{self.xoct}, {self.sign}] {hex(id(self))}>'

    # The string the console prints shows the external form.
    # Example: Interval("oooo8")
    def __repr__(self):
        return f'Interval("{self.interval_string}")'

    # Implements Interval < Interval.
    # @param other The interval to compare with this interval.
    # @returns True if this interval is less than the other.
    #
    # A TypeError should be raised if other is not an Interval.
    # This method should call self.pos() and other.pos() to get the
    # values to compare. See: pos().
    def __lt__(self, other):
        if isinstance(other, Interval):
            if self.pos() < other.pos():
                return True
            else:
                return False
        else:
            raise TypeError("Interval comparisons can only be performed between two Intervals.")

    # Implements Interval <= Interval.
    # @param other The interval to compare with this interval.
    # @returns True if this interval is less than or equal to the other.
    #
    # A TypeError should be raised if other is not an Interval.
    # This method should call self.pos() and other.pos() to get the
    # values to compare. See: pos().
    def __le__(self, other):
        if isinstance(other, Interval):
            if self.pos() <= other.pos():
                return True
            else:
                return False
        else:
            raise TypeError("Interval comparisons can only be performed between two Intervals.")

    # Implements Interval == Interval.
    # @param other The interval to compare with this interval.
    # @returns True if this interval is equal to the other.
    #
    # A TypeError should be raised if other is not an Interval.
    # This method should call self.pos() and other.pos() to get the
    # values to compare. See: pos().
    def __eq__(self, other):
        if isinstance(other, Interval):
            if self.pos() == other.pos():
                return True
            else:
                return False
        else:
            raise TypeError("Interval comparisons can only be performed between two Intervals.")

    # Implements Interval != Interval.
    # @param other The interval to compare with this interval.
    # @returns True if this interval is not equal to the other.
    #
    # A TypeError should be raised if other is not an Interval.
    # This method should call self.pos() and other.pos() to get the
    # values to compare. See: pos().
    def __ne__(self, other):
        if isinstance(other, Interval):
            if self.pos() != other.pos():
                return True
            else:
                return False
        else:
            raise TypeError("Interval comparisons can only be performed between two Intervals.")

    # Implements Interval >= Interval.
    # @param other The interval to compare with this interval.
    # @returns True if this interval is greater than or equal to the other.
    #
    # A TypeError should be raised if other is not an Interval.
    # This method should call self.pos() and other.pos() to get the
    # values to compare. See: pos().
    def __ge__(self, other):
        if isinstance(other, Interval):
            if self.pos() >= other.pos():
                return True
            else:
                return False
        else:
            raise TypeError("Interval comparisons can only be performed between two Intervals.")

    # Implements Interval > Interval.
    # @param other The interval to compare with this interval.
    # @returns True if this interval is greater than the other.
    #
    # A TypeError should be raised if other is not an Interval.
    # This method should call self.pos() and other.pos() to get the
    # values to compare. See: pos().
    def __gt__(self, other):
        if isinstance(other, Interval):
            if self.pos() > other.pos():
                return True
            else:
                return False
        else:
            raise TypeError("Interval comparisons can only be performed between two Intervals.")

    # Returns a numerical value for comparing the size of this interval to
    # another. The comparison depends on the span, extra octaves, and quality
    # of the intervals but not their signs. For two intervals, if the span of
    # the first (including extra octaves) is larger than the second then the
    # first interval is larger than the second regardless of the quality of
    # either interval. If the interval spans are the same then the first is
    # larger than the second if its quality is larger. This value can be
    # encoded as a 16 bit integer: (((span + (xoct * 7)) + 1) << 8) + qual  
    def pos(self):
        return (((self.span + (self.xoct * 7)) + 1) << 8) + self.qual

    # Returns a string containing the interval name.
    #  For example, Interval('-P5').string() would return '-P5'.
    def string(self):
        return self.interval_string

    # Returns the full interval name, e.g. 'doubly-augmented third'
    #  or 'descending augmented sixth'
    # @param sign If true then "descending" will appear in the
    # name if it is a descending interval.
    def full_name(self, *, sign=True):
        name = f'{self.quality_name()} {self.span_name()}'
        if sign and self.sign == -1:
            name = f'descending {name}'
        return name

    # Returns the full name of the interval's span, e.g. a
    # unison would return "unison" and so on.
    def span_name(self):
        if self.span == Interval._unison_span and self.xoct > 0:
            span = Interval._octave_span
        else:
            span = self.span
        return Interval.spans_to_names[span]

    # Returns the full name of the interval's quality, e.g. a
    # perfect unison would return "perfect" and so on.
    def quality_name(self):
        return Interval.quals_to_names[self.qual]

    # Returns true if this interval and the other interval have the
    # same span, quality and sign. The extra octaves are ignored.
    def matches(self, other):
        if isinstance(other, Interval):
            if self.span == other.span and self.qual == other.qual and self.sign == other.sign:
                return True
            else:
                return False
        else:
            raise TypeError("matches() can only be performed between two Intervals.")

    # Returns the interval's number of lines and spaces, e.g.
    # a unison will return 1.
    def lines_and_spaces(self):
        return self.span + 1

    # Private method that returns a zero based interval quality from its 
    #  external name. Raises an assertion if the name is invalid. See:
    # is_unison() and similar.
    # def _to_iq(self, name):

    # Returns the interval values as a list: [span, qual, xoct, sign]
    def to_list(self):
        return [self.span, self.qual, self.xoct, self.sign]

    # Sets up skeleton for the is_span functions
    # @param qual If specified the predicate tests for that specific
    # quality of unison, which can be any valid quality symbol, e.g.
    # 'P', 'M' 'm' 'd' 'A' 'o' '+' and so on.
    def is_span(self, span, qual):
        if isinstance(qual, str):
            qual = qual.replace('a', '+')
            qual = qual.replace('A', '+')
            qual = qual.replace('d', 'o')
            qual = qual.replace('D', 'o')
        if qual is None:
            if self.span == span:
                return True
            else:
                return False
        elif Interval.quals.get(qual, -1) != -1:
            if self.span == span and Interval.quals[qual] == self.qual:
                return True
            else:
                return False
        else:
            raise TypeError("Invalid quality. Please enter a valid quality string (P, M, m, d, A, o, +, etc.)")

    # Returns true if the interval is a unison otherwise false.
    # @param qual If specified the predicate tests for that specific
    # quality of unison, which can be any valid quality symbol, e.g.
    # 'P', 'M' 'm' 'd' 'A' 'o' '+' and so on. See: _to_iq().
    def is_unison(self, qual=None):
        return self.is_span(Interval._unison_span, qual)

    # Returns true if the interval is a second otherwise false.
    # @param qual If specified the predicate tests for that specific
    # quality of second, which can be any quality symbol, e.g.
    # 'P', 'M' 'm' 'd' 'A' 'o' '+' and so on. See: _to_iq().
    def is_second(self, qual=None):
        return self.is_span(Interval._second_span, qual)

    # Returns true if the interval is a third otherwise false.
    # @param qual If specified the predicate tests for that specific
    # quality of third, which can be any quality symbol, e.g.
    # 'P', 'M' 'm' 'd' 'A' 'o' '+' and so on. See: _to_iq().
    def is_third(self, qual=None):
        return self.is_span(Interval._third_span, qual)

    # Returns true if the interval is a fourth otherwise false.
    # @param qual If specified the predicate tests for that specific
    # quality of fourth, which can be any quality symbol, e.g.
    # 'P', 'M' 'm' 'd' 'A' 'o' '+' and so on. See: _to_iq().
    def is_fourth(self, qual=None):
        return self.is_span(Interval._fourth_span, qual)

    # Returns true if the interval is a fifth otherwise false.
    # @param qual If specified the predicate tests for that specific
    # quality of fifth, which can be any quality symbol, e.g.
    # 'P', 'M' 'm' 'd' 'A' 'o' '+' and so on. See: _to_iq().
    def is_fifth(self, qual=None):
        return self.is_span(Interval._fifth_span, qual)

    # Returns true if the interval is a sixth otherwise false.
    # @param qual If specified the predicate tests for that specific
    # quality of sixth, which can be any quality symbol, e.g.
    # 'P', 'M' 'm' 'd' 'A' 'o' '+' and so on. See: _to_iq().
    def is_sixth(self, qual=None):
        return self.is_span(Interval._sixth_span, qual)

    # Returns true if the interval is a seventh otherwise false.
    # @param qual If specified the predicate tests for that specific
    # quality of seventh, which can be any quality symbol, e.g.
    # 'P', 'M' 'm' 'd' 'A' 'o' '+' and so on. See: _to_iq().
    def is_seventh(self, qual=None):
        return self.is_span(Interval._seventh_span, qual)

    # Returns true if the interval is an octave otherwise false.
    # @param qual If specified the predicate tests for that specific
    # quality of octave, which can be any quality symbol, e.g.
    # 'P', 'M' 'm' 'd' 'A' 'o' '+' and so on. See: _to_iq().
    def is_octave(self, qual=None):
        return self.is_span(Interval._octave_span, qual)

    # Returns a 'diminution count' 1-5 if the interval is diminished else False.
    # For example, if the interval is doubly-diminished then 2 is returned.
    # If the interval not diminished at all (e.g. is perfect, augmented, minor or
    # major) then False is returned.
    def is_diminished(self):
        if self.qual <= Interval._dim_qual:
            return 5 - self.qual
        else:
            return False

    # Returns true if the interval is minor, otherwise false.
    def is_minor(self):
        return self.qual == Interval._minor_qual

    # Returns true if the interval is perfect, otherwise false.
    def is_perfect(self):
        return self.qual == Interval._perfect_qual

    # Returns true if the interval is major, otherwise false.
    def is_major(self):
        return self.qual == Interval._major_qual

    # Returns a 'augmentation count' 1-5 if the interval is augmented else False.
    # For example, if the interval is doubly-augmented then 2 is returned.
    # If the interval not augmented at all (e.g. is perfect, diminished, minor or
    # major) then False is returned.
    def is_augmented(self):
        if self.qual >= Interval._aug_qual:
            return self.qual - Interval._aug_qual + 1
        else:
            return False

    # Returns true if the interval belongs to the 'perfect interval'
    #  family, i.e. it is a Unison, 4th, 5th, or Octave.
    def is_perfect_type(self):
        return self.span == Interval._unison_span or self.span == Interval._fourth_span or \
               self.span == Interval._fifth_span or self.span == Interval._octave_span

    # Returns true if this interval belongs to the 'imperfect interval'
    #  family, i.e. it is a 2nd, 3rd, 6th, or 7th.
    def is_imperfect_type(self):
        return not self.is_perfect_type()

    # Returns true if this is a simple interval, i.e. its span is
    #  less-than-or-equal to an octave.
    def is_simple(self):
        return self.xoct == 0

    # Returns true if this is a compound interval, i.e. its span is
    #  more than an octave (an octave is a simple interval).
    def is_compound(self):
        return self.xoct > 0

    # Returns true if this interval's sign is 1.
    def is_ascending(self):
        return self.sign == 1

    # Returns true if this interval's sign is -1.
    def is_descending(self):
        return self.sign == -1

    # Returns true if the interval is a consonant interval. In this
    # context the perfect fourth should be considered consonant.
    def is_consonant(self):
        return Interval._minor_qual <= self.qual <= Interval._major_qual \
               and self.span != Interval._second_span \
               and self.span != Interval._seventh_span

    # Returns true if the interval is not a consonant interval.
    def is_dissonant(self):
        return not self.is_consonant()

    #  Returns a complemented copy of the interval. To complement an interval
    # you invert its span and quality. To invert the span, subtract it from
    # the maximum span index (the octave index). To invert the  quality subtract
    # it from the maximum quality index (quintuply augmented).
    def complemented(self):
        return Interval([Interval._octave_span - self.span, Interval._5aug_qual - self.qual, self.xoct, self.sign])

    # Returns the number of semitones in the interval. It is possible
    # to determine the number of semitones by looking at the span and
    # quality indexes. For example, if the span is a perfect fifth
    # (span index 4) and the quality is perfect (quality index 6)
    # then the semitones will be 7 and augmented or diminished fifths
    # will add or subtract semitones accordingly.
    #
    # This value will be negative for descending intervals otherwise positive.
    def semitones(self):
        quals_to_semitones = {Interval._5dim_qual: -5, Interval._4dim_qual: -4, Interval._3dim_qual: -3,
                              Interval._2dim_qual: -2, Interval._dim_qual: -1,
                              # since we're basing imperfect intervals on MAJOR intervals, major will be 0 and
                              # minor will be -1. When we're accounting for diminished qualities with imperfect
                              # intervals, we will have to subtract 1 from the final semitonal count
                              Interval._minor_qual: -1, Interval._perfect_qual: 0, Interval._major_qual: 0,
                              Interval._aug_qual: 1, Interval._2aug_qual: 2, Interval._3aug_qual: 3,
                              Interval._4aug_qual: 4, Interval._5aug_qual: 5}
        if self.is_perfect_type():
            spans_to_semitones = {Interval._unison_span: 0, Interval._fourth_span: 5,
                                  Interval._fifth_span: 7, Interval._octave_span: 12}
            return self.sign * spans_to_semitones[self.span] + quals_to_semitones[self.qual] + self.xoct * 12
        else:
            # lets try basing it off of major
            spans_to_semitones = {Interval._second_span: 2, Interval._third_span: 4,
                                  Interval._sixth_span: 9, Interval._seventh_span: 11}
            semitones = self.sign * spans_to_semitones[self.span] + quals_to_semitones[self.qual]
            if self.qual < Interval._minor_qual:
                semitones -= 1
            return semitones + self.xoct * 12

    # Adds a specified interval to this interval.
    #  @return  a new interval expressing the total span of both intervals.
    #  @param other the interval to add to this one.
    #
    # A TypeError should be raised if other is not an interval. A
    # NotImplementedError if either intervals are descending.
    def add(self, other):
        # Do NOT implement this method yet.
        if isinstance(other, Interval):
            if self.sign != -1 and other.sign != -1:
                pass
            else:
                raise NotImplementedError("Adding any descending intervals has not been implemented yet.")
        else:
            raise TypeError("Only intervals can be added to other intervals.")

    # Transposes a Pitch or Pnum by the interval. Pnum transposition
    #  has no direction so if the interval is negative its complement
    #  should be used.
    #  @param pref  The Pitch or Pnum to transpose.
    #  @return The transposed Pitch or Pnum.
    def transpose(self, pref):
        # Do NOT implement this method yet.
        pass
