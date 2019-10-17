###############################################################################

from .pitch import Pitch

## A class that implements musical intervals.
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

    ## Creates an Interval from a string, list, or two Pitches.
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
        pass

    ## A private method that checks four integer values (span, qual, xoct, sign) to make sure
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
        pass

    ## A private method that accepts an interval string and parses it into four
    # integer values: span, qual, xoct, sign. If all four values can be parsed
    # from the string they should be passed to the _init_from_list() method to
    # check the values and assign them to the instance's attributes. A ValueError
    # should be raised for any value that cannot be parsed from the string. See:
    # _init_from_list().
    def _init_from_string(self, string):
        # ... parse the string into a span, qual, xoct and sign values
        span, qual, xoct, sign = (-1,-1,-1,-1)
        # ... pass on to check an assign instance attributes.
        self._init_from_list(span,qual,xoct,sign)

    ## A private method that determines approprite span, qual, xoct, sign
    # from two pitches. If pitch2 is lower than pitch1 then a descending
    # interval should be formed. The values should be passed to the
    # _init_from_list() method to initalize the interval's attributes.
    # See: _init_from_list().
    #
    # Do NOT implement this method yet.
    def _init_from_pitches(self, pitch1, pitch2):
        # ... parse the string into a span, qual, xoct and sign values
        span, qual, xoct, sign = (-1,-1,-1,-1)
        # ... pass on to check and assign instance attributes.
        self._init_from_list(span,qual,xoct,sign)
        
    ## Returns a string displaying information about the
    #  Interval within angle brackets. Information includes the
    #  the class name, the interval text, the span, qual, xoct and sign
    #  values, and the id of the object. Example:
    #  <Interval: oooo8 [7, 1, 0, 1] 0x1075bf6d0>
    #  See also: string().
    def __str__(self):
        return ''

    ## The string the console prints shows the external form.
    # Example: Interval("oooo8")
    def __repr__(self):
        return ''

    ## Implements Interval < Interval.
    # @param other The interval to compare with this interval.
    # @returns True if this interval is less than the other.
    #
    # A TypeError should be raised if other is not an Interval.
    # This method should call self.pos() and other.pos() to get the
    # values to compare. See: pos().
    def __lt__(self, other):
        pass

    ## Implements Interval <= Interval.
    # @param other The interval to compare with this interval.
    # @returns True if this interval is less than or equal to the other.
    #
    # A TypeError should be raised if other is not an Interval.
    # This method should call self.pos() and other.pos() to get the
    # values to compare. See: pos().
    def __le__(self, other):
        pass

    ## Implements Interval == Interval.
    # @param other The interval to compare with this interval.
    # @returns True if this interval is equal to the other.
    #
    # A TypeError should be raised if other is not an Interval.
    # This method should call self.pos() and other.pos() to get the
    # values to compare. See: pos().
    def __eq__(self, other):
        pass

    ## Implements Interval != Interval.
    # @param other The interval to compare with this interval.
    # @returns True if this interval is not equal to the other.
    #
    # A TypeError should be raised if other is not an Interval.
    # This method should call self.pos() and other.pos() to get the
    # values to compare. See: pos().
    def __ne__(self, other):
        pass

    ## Implements Interval >= Interval.
    # @param other The interval to compare with this interval.
    # @returns True if this interval is greater than or equal to the other.
    #
    # A TypeError should be raised if other is not an Interval.
    # This method should call self.pos() and other.pos() to get the
    # values to compare. See: pos().
    def __ge__(self, other):
        pass

    ## Implements Interval > Interval.
    # @param other The interval to compare with this interval.
    # @returns True if this interval is greater than the other.
    #
    # A TypeError should be raised if other is not an Interval.
    # This method should call self.pos() and other.pos() to get the
    # values to compare. See: pos().
    def __gt__(self, other):
        pass

    ## Returns a numerical value for comparing the size of this interval to
    # another. The comparison depends on the span, extra octaves, and quality
    # of the intervals but not their signs. For two intervals, if the span of
    # the first (including extra octaves) is larger than the second then the
    # first interval is larger than the second regardless of the quality of
    # either interval. If the interval spans are the same then the first is
    # larger than the second if its quality is larger. This value can be
    # encoded as a 16 bit integer: (((span + (xoct * 7)) + 1) << 8) + qual  
    def pos(self):
        pass

    ## Returns a string containing the interval name.
    #  For example, Interval('-P5').string() would return '-P5'.
    def string(self):
        pass

    ## Returns the full interval name, e.g. 'doubly-augmented third'
    #  or 'descending augmented sixth'
    # @param sign If true then "descending" will appear in the
    # name if it is a descending interval.
    def full_name(self, *, sign=True):
        pass

    ## Returns the full name of the interval's span, e.g. a
    # unison would return "unison" and so on.
    def span_name(self):
        pass

    ## Returns the full name of the interval's quality, e.g. a
    # perfect unison would return "perfect" and so on.
    def quality_name(self):
        pass

    ## Returns true if this interval and the other interval have the
    # same span, quality and sign. The extra octaves are ignored.
    def matches(self, other):
        pass

    ## Returns the interval's number of lines and spaces, e.g.
    # a unison will return 1.
    def lines_and_spaces(self):
        pass

    ## Private method that returns a zero based interval quality from its 
    #  external name. Raises an assertion if the name is invalid. See:
    # is_unison() and similar.
    def _to_iq(self, name):
        pass

    ## Returns the interval values as a list: [span, qual, xoct, sign]
    def to_list(self):
        return [self.span, self.qual, self.xoct, self.sign]

    ## Returns true if the interval is a unison otherwise false.
    # @param qual If specified the predicate tests for that specific
    # quality of unison, which can be any valid quality symbol, e.g.
    # 'P', 'M' 'm' 'd' 'A' 'o' '+' and so on. See: _to_iq().
    def is_unison(self, qual=None):
        pass

    ## Returns true if the interval is a second otherwise false.
    # @param qual If specified the predicate tests for that specific
    # quality of second, which can be any quality symbol, e.g.
    # 'P', 'M' 'm' 'd' 'A' 'o' '+' and so on. See: _to_iq().
    def is_second(self, qual=None):
        pass

    ## Returns true if the interval is a third otherwise false.
    # @param qual If specified the predicate tests for that specific
    # quality of third, which can be any quality symbol, e.g.
    # 'P', 'M' 'm' 'd' 'A' 'o' '+' and so on. See: _to_iq().
    def is_third(self, qual=None):
        pass

    ## Returns true if the interval is a fourth otherwise false.
    # @param qual If specified the predicate tests for that specific
    # quality of fourth, which can be any quality symbol, e.g.
    # 'P', 'M' 'm' 'd' 'A' 'o' '+' and so on. See: _to_iq().
    def is_fourth(self, qual=None):
        pass

    ## Returns true if the interval is a fifth otherwise false.
    # @param qual If specified the predicate tests for that specific
    # quality of fifth, which can be any quality symbol, e.g.
    # 'P', 'M' 'm' 'd' 'A' 'o' '+' and so on. See: _to_iq().
    def is_fifth(self, qual=None):
        pass

    ## Returns true if the interval is a sixth otherwise false.
    # @param qual If specified the predicate tests for that specific
    # quality of sixth, which can be any quality symbol, e.g.
    # 'P', 'M' 'm' 'd' 'A' 'o' '+' and so on. See: _to_iq().
    def is_sixth(self, qual=None):
        pass

    ## Returns true if the interval is a seventh otherwise false.
    # @param qual If specified the predicate tests for that specific
    # quality of seventh, which can be any quality symbol, e.g.
    # 'P', 'M' 'm' 'd' 'A' 'o' '+' and so on. See: _to_iq().
    def is_seventh(self, qual=None):
        pass

    ## Returns true if the interval is an octave otherwise false.
    # @param qual If specified the predicate tests for that specific
    # quality of octave, which can be any quality symbol, e.g.
    # 'P', 'M' 'm' 'd' 'A' 'o' '+' and so on. See: _to_iq().
    def is_octave(self, qual=None):
        pass

    ## Returns a 'diminution count' 1-5 if the interval is diminished else False.
    # For example, if the interval is doubly-diminished then 2 is returned.
    # If the interval not diminished at all (e.g. is perfect, augmented, minor or
    # major) then False is returned.
    def is_diminished(self):
        pass

    ## Returns true if the interval is minor, otherwise false.
    def is_minor(self):
        pass

    ## Returns true if the interval is perfect, otherwise false.
    def is_perfect(self):
        pass

    ## Returns true if the interval is major, otherwise false.
    def is_major(self):
        pass

    ## Returns a 'augmentation count' 1-5 if the interval is augmented else False.
    # For example, if the interval is doubly-augmented then 2 is returned.
    # If the interval not augmented at all (e.g. is perfect, diminished, minor or
    # major) then False is returned.
    def is_augmented(self):
        pass

    ## Returns true if the interval belongs to the 'perfect interval'
    #  family, i.e. it is a Unison, 4th, 5th, or Octave.
    def is_perfect_type(self):
        pass

    ## Returns true if this interval belongs to the 'imperfect interval'
    #  family, i.e. it is a 2nd, 3rd, 6th, or 7th.
    def is_imperfect_type(self):
        pass

    ## Returns true if this is a simple interval, i.e. its span is
    #  less-than-or-equal to an octave.
    def is_simple(self):
        pass

    ## Returns true if this is a compound interval, i.e. its span is
    #  more than an octave (an octave is a simple interval).
    def is_compound(self):
        pass

    ## Returns true if this interval's sign is 1.
    def is_ascending(self):
        pass

    ## Returns true if this interval's sign is -1.
    def is_descending(self):
        pass

    ## Returns true if the interval is a consonant interval. In this
    # context the perfect fourth should be considered consonant.
    def is_consonant(self):
        pass

    ## Returns true if the interval is not a consonant interval.
    def is_dissonant(self):
        pass

    ##  Returns a complemented copy of the interval. To complement an interval
    # you invert its span and quality. To invert the span, subtract it from
    # the maximum span index (the octave index). To invert the  quality subtract
    # it from the maximum quality index (quintuply augmented).
    def complemented(self):
        pass

    ## Returns the number of semitones in the interval. It is possible
    # to determine the number of semitones by looking at the span and
    # quality indexes. For example, if the span is a perfect fifth
    # (span index 4) and the quality is perfect (quality index 6)
    # then the semitones will be 5 and augmented or diminished fifths
    # will add or subtract semitones accordingly.
    #
    # This value will be negative for descending intervals otherwise positive.
    def semitones(self):
        pass

    ## Adds a specified interval to this interval.
    #  @return  a new interval expressing the total span of both intervals.
    #  @param other the interval to add to this one.
    #
    # A TypeError should be raised if other is not an interval. A
    # NotImplementedError if either intervals are descending.
    def add(self, other):
        # Do NOT implement this method yet.
        pass

    # Transposes a Pitch or Pnum by the interval. Pnum transposition
    #  has no direction so if the interval is negative its complement
    #  should be used.
    #  @param pref  The Pitch or Pnum to transpose.
    #  @return The transposed Pitch or Pnum.
    def transpose(self, pref):
        # Do NOT implement this method yet.
        pass
