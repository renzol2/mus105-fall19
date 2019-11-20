########################################

# You can import from score, theory and any python module you want to use.

from .score import Pitch, Interval, Mode, import_score
from .theory import Analysis, Rule, timepoints
from copy import copy


# A template dictionary whose keys represent analytical checks performed on
# a melody. Your analysis will copy this dictionary into its self.results
# attribute and then run its rules to update the value of each check in the
# dictionary. When a rule is run and it determines a check is successful, the
# rule will set the dictionary value (e.g. self.analysis['MEl_START_NOTE'])
# to True and if its not successful it will set it to a list of zero or more
# values as described below.
melodic_checks = {
    
    # Pitch checks

    # Starting note must be tonic, mediant, or dominant. If the melody
    # starts correctly set this value to True, otherwise set it to an empty
    # list [].
    'MEL_START_NOTE': None,

    # Last two notes must be melodic cadence (2-1 or 7-1). If the
    # melody ends correctly set this value to True, otherwise set
    # it to an empty list [].
    'MEL_CADENCE': None,

    # At least 75% of notes must be within the tessitura (central Major
    # 6th of the melody's range). If the check is successful set this value
    # to true, otherwise set it to an empty list [].
    'MEL_TESSITURA': None,

    # All pitches must be diatonic. If the check is successful set
    # this value to True, otherwise set it to a list containing the
    # note positions of each note that fails. Note positions start
    # on 1 not 0.
    'MEL_DIATONIC': None,

    # Melodic interval checks

    # At least 51% of notes must be stepwise.  If the check is successful
    # set this value to True, otherwise set it to an empty list [].
    'INT_STEPWISE': None,

    # All intervals must be consonant (P4 is consonant). If the check
    # is successful set this value to True, otherwise set it to a list
    # containing the note positions of each note that fails. Note
    # positions start on 1 not 0. Since this check involves an interval
    # between two notes, use the position of the note to the left
    # of the offending interval.
    'INT_CONSONANT': None,

    # All intervals must be an octave or less. If the check is successful
    # set this value to True, otherwise set it to a list containing the
    # note positions of each note that fails. Note positions start on 1
    # not 0. Since this check involves an interval between two notes, use
    # the position of the note to the left of the offending interval.
    'INT_SIMPLE': None,

    # Max number of large leaps is 1. A large leap is defined as a perfect
    # fifth or more. If the check is successful set this value to True,
    # otherwise set it to a list containing the note positions of each
    # interval after the first one.
    'INT_NUM_LARGE': None,

    # Max number of unisons is 1. If the check is successful set this
    # value to True, otherwise set it to a list containing the note
    # positions of each unison after the first one.
    'INT_NUM_UNISON': None,

    # Max number of consecutive intervals moving in same direction is 3
    # (i.e four consecutive notes). If the check is successful set this
    # value to True, otherwise set it to a list containing the note
    # positions of each interval after the third one.
    'INT_NUM_SAMEDIR': None,

    # Leap checks

    # Leap of 4th must reverse direction, leap of 5th or more must reverse
    # by step. The leap can be the result of a single interval or by multiple
    # consecutive leaps in the same direction. For multiple leaps in the same
    # direction, the total size of the leap should be the sum of all the leaps
    # in the same direction. If the check is successful set this value to True,
    # otherwise set it to a list containing the note positions of each interval
    # that fails. To mark a leap spanning a 5th or greater that did not reverse
    # by step, set its note index to be negative.
    'LEAP_RECOVERY': None,  # @TODO

    # Max number of consecutive leaps in a row is 2 (three notes). If the
    # check is successful set this value to True, otherwise set it to a list
    # containing the note positions of each interval after the second leap.
    'LEAP_NUM_CONSEC': None,

    # Shape checks

    # Max number of climax notes is 1.  If the check is successful set
    # this value to True, otherwise set it to a list containing the note
    # positions of each climax after the first.
    'SHAPE_NUM_CLIMAX': None,

    # Climax note must be located within the center third of melody.  If
    # the check is successful set this value to True, otherwise set it to a
    # list containing the note positions of all climaxes outside it.
    'SHAPE_ARCHLIKE': None,

    # A set of intervals with at least one direct repetition cannot
    # occupy more than 50% of melody. If the check is successful set this
    # value to True, otherwise set it to a list containing the set of
    # interval motions (e.g [2, 2, -3].
    'SHAPE_UNIQUE': None  # @TODO
}


# Here is an example of a rule. You can define as many rules as you want.
# The purpose of running a rule is to perform some analytical check(s) and
# then update the self.analysis.results dictionary with its findings.
class MelodyStartNoteRule(Rule):

    # Rule initializer.
    def __init__(self, analysis):
        # Always set the rule's back pointer to its analysis!
        super().__init__(analysis, "True if: Starting note is in melodic triad")
        # Now initialize whatever attributes your rule defines.
        # ...
        # Need to grab the key from the first bar of the score...
        self.key = self.analysis.score.parts[0].staffs[0].bars[0].key
        self.tonic_triad = {self.key.scale()[0], self.key.scale()[2], self.key.scale()[4]}
        self.starting_note = self.analysis.pitches[0]
        self.success = False

    # This is where your rule does all its work. When the work is done you
    # should update the analysis results with whatever checks it is doing.
    def apply(self):
        # ... do some analysis...
        # ... update the analysis results, for example:
        # self.analysis.results['MEL_START_NOTE'] = True if success else []
        self.success = self.starting_note.pnum() in self.tonic_triad
        self.analysis.results['MEL_START_NOTE'] = True if self.success else []

    # Uncomment this code if you want your rule to print information to the
    # the terminal just after it runs...
    def display(self, index):
        print('-------------------------------------------------------------------')
        print(f"Rule {index+1}: {self.title}")
        print(self.success)


# ...ADD MORE RULES HERE!....

class MelodicCadenceRule(Rule):
    """
    Tests for a melodic cadence (Ending cadence uses scale degrees 7 - 1 or 2 - 1)
    """
    def __init__(self, analysis):
        super().__init__(analysis, "True if: Ending cadence is 7 - 1 or 2 - 1")
        self.key = self.analysis.score.parts[0].staffs[0].bars[0].key
        self.cadence = [p.pnum() for p in self.analysis.pitches[-2:]]
        self.cadence7_1 = [self.key.scale()[-1], self.key.tonic()]
        self.cadence2_1 = [self.key.scale()[1], self.key.tonic()]
        self.success = False

    def apply(self):
        self.success = self.cadence == self.cadence2_1 or self.cadence == self.cadence7_1
        self.analysis.results['MEL_CADENCE'] = True if self.success else []

    def display(self, index):
        print('-------------------------------------------------------------------')
        print(f"Rule {index+1}: {self.title}")
        print(self.success)


class MelodyWithinTessitura(Rule):
    """
    Tests whether the melody is 75% within the tessitura.
    """
    def __init__(self, analysis):
        super().__init__(analysis, "True if: Melody is 75% within the tessitura")
        max_pitch, min_pitch = max(self.analysis.pitches), min(self.analysis.pitches)
        avg_keynum = (max_pitch.keynum() + min_pitch.keynum()) // 2
        bottom_tess_keynum, top_tess_keynum = avg_keynum - 5, avg_keynum + 4
        self.bottom_tess_pitch = Pitch.from_keynum(bottom_tess_keynum)
        self.top_tess_pitch = Pitch.from_keynum(top_tess_keynum)\
            if Interval(self.bottom_tess_pitch, Pitch.from_keynum(top_tess_keynum)).is_sixth()\
            else Pitch.from_keynum(top_tess_keynum, '#')
        self.success = False

    def apply(self):
        pitches_within_tessitura = [p for p in self.analysis.pitches
                                    if self.bottom_tess_pitch <= p <= self.top_tess_pitch]
        self.success = len(pitches_within_tessitura) >= len(self.analysis.pitches) * 3 / 4
        self.analysis.results['MEL_TESSITURA'] = True if self.success else []

    def display(self, index):
        print('-------------------------------------------------------------------')
        print(f"Rule {index + 1}: {self.title}")
        print(self.success)


class MelodyDiatonic(Rule):
    """
    Tests whether the melody is diatonic.
    """
    def __init__(self, analysis):
        super().__init__(analysis, "True if: Melody is diatonic")
        self.key = self.analysis.score.parts[0].staffs[0].bars[0].key
        self.scale = self.key.scale()
        self.success = False

    def apply(self):
        scale = self.scale + [Interval('-m2').transpose(self.key.tonic())]\
            if self.key.mode == Mode.MINOR else self.scale  # adding sharp 7 for harmonic minor
        print(self.analysis.pitches)
        print(scale)
        pitch_is_diatonic = [p.pnum() in scale for p in self.analysis.pitches]
        self.success = not (False in pitch_is_diatonic)
        self.analysis.results['MEL_DIATONIC'] = True if self.success else\
            [i + 1 for i in range(len(pitch_is_diatonic)) if pitch_is_diatonic[i] is False]

    def display(self, index):
        print('-------------------------------------------------------------------')
        print(f"Rule {index + 1}: {self.title}")
        print(self.success)


class IntervalsStepwise(Rule):
    """
    Tests whether at least 51% of the intervals are stepwise.
    """
    def __init__(self, analysis):
        super().__init__(analysis, "True if: at least 51% of the intervals are stepwise")
        self.success = False

    def apply(self):
        stepwise_intervals = [span for span in self.analysis.spans if abs(span) == 2]
        self.success = len(stepwise_intervals) > len(self.analysis.spans) * 0.51
        self.analysis.results['INT_STEPWISE'] = True if self.success else []

    def display(self, index):
        print('-------------------------------------------------------------------')
        print(f"Rule {index + 1}: {self.title}")
        print(self.success)


class IntervalsConsonant(Rule):
    """
    Tests whether all the intervals are consonant.
    """
    def __init__(self, analysis):
        super().__init__(analysis, "True if: all the intervals are consonant")
        self.success = False

    def apply(self):
        is_consonant = [i.is_consonant() or i.lines_and_spaces() == 2 for i in self.analysis.intervals]
        self.success = not (False in is_consonant)
        self.analysis.results['INT_CONSONANT'] = True if self.success else \
            [i + 1 for i in range(len(is_consonant)) if is_consonant[i] is False]

    def display(self, index):
        print('-------------------------------------------------------------------')
        print(f"Rule {index + 1}: {self.title}")
        print(self.success)


class IntervalsSimple(Rule):
    """
    Tests whether all the intervals are simple.
    """
    def __init__(self, analysis):
        super().__init__(analysis, "True if: all the intervals are simple")
        self.success = False

    def apply(self):
        is_simple = [i.is_simple() for i in self.analysis.intervals]
        self.success = not (False in is_simple)
        self.analysis.results['INT_SIMPLE'] = True if self.success else \
            [i + 1 for i in range(len(is_simple)) if is_simple[i] is False]

    def display(self, index):
        print('-------------------------------------------------------------------')
        print(f"Rule {index + 1}: {self.title}")
        print(self.success)


class IntervalsNumLarge(Rule):
    """
    Tests that only one leap (fifth or higher) exists in the melody.
    """
    def __init__(self, analysis):
        super().__init__(analysis, "True if: only one leap exists in the melody")
        self.success = False

    def apply(self):
        is_leap = [i >= Interval('P5') for i in self.analysis.intervals]
        self.success = is_leap.count(True) <= 1
        self.analysis.results['INT_NUM_LARGE'] = True if self.success else \
            [i + 1 for i in range(len(is_leap)) if is_leap[i] is True][1:]

    def display(self, index):
        print('-------------------------------------------------------------------')
        print(f"Rule {index + 1}: {self.title}")
        print(self.success)


class IntervalsNumUnisons(Rule):
    """
    Tests that only one unison exists in the melody.
    """
    def __init__(self, analysis):
        super().__init__(analysis, "True if: only one unison exists in the melody")
        self.success = False

    def apply(self):
        is_unison = [i.lines_and_spaces() == 1 for i in self.analysis.intervals]
        self.success = is_unison.count(True) <= 1
        self.analysis.results['INT_NUM_UNISON'] = True if self.success else \
            [i + 1 for i in range(len(is_unison)) if is_unison[i] is True][1:]

    def display(self, index):
        print('-------------------------------------------------------------------')
        print(f"Rule {index + 1}: {self.title}")
        print(self.success)


class IntervalsSameDirection(Rule):
    """
    Tests that no more than 4 notes go in the same direction (no more than 3 consecutive similarly signed intervals).
    """
    def __init__(self, analysis):
        super().__init__(analysis, "True if: no more than 3 consecutive similarly signed intervals")
        self.success = False

    def apply(self):
        # iterate through every interval
        # if first interval or current interval has different sign from last, reset counter and assign testing sign
        # if current interval has same sign from last, add to counter
        #  if counter is 4 or more, add position to separate list
        consecutive_intervals = []
        current_sign = 0
        counter = 0
        for i in range(len(self.analysis.intervals)):
            if current_sign == 0 or self.analysis.intervals[i].sign != current_sign:
                counter = 1
                current_sign = self.analysis.intervals[i].sign
            elif self.analysis.intervals[i].sign == current_sign:
                counter += 1
                if counter > 3:
                    consecutive_intervals.append(i + 2)  # not really sure why it's +2, but that's what works!
        self.success = len(consecutive_intervals) == 0
        self.analysis.results['INT_NUM_SAMEDIR'] = True if self.success else consecutive_intervals

    def display(self, index):
        print('-------------------------------------------------------------------')
        print(f"Rule {index + 1}: {self.title}")
        print(self.success)


class LeapNumberConsecutive(Rule):
    """
    Tests that there are no more than 2 consecutive leaps in a row within the melody.
    """
    def __init__(self, analysis):
        super().__init__(analysis, "True if: no more than 2 consecutive leaps in a row are in the melody.")
        self.success = False

    def apply(self):
        # iterate through every span
        # if span is greater than 2, add to counter
        #   if counter > 2, add to list
        # if span is 2 or less, reset counter
        consecutive_leaps = []
        counter = 0
        for i in range(len(self.analysis.spans)):
            if abs(self.analysis.spans[i]) <= 2:
                counter = 0
            else:
                counter += 1
                if counter > 2:
                    consecutive_leaps.append(i + 1)
        self.success = len(consecutive_leaps) == 0
        self.analysis.results['LEAP_NUM_CONSEC'] = True if self.success else consecutive_leaps

    def display(self, index):
        print('-------------------------------------------------------------------')
        print(f"Rule {index + 1}: {self.title}")
        print(self.success)


class ShapeNumberClimax(Rule):
    """
    Tests that only one climax note exists.
    """
    def __init__(self, analysis):
        super().__init__(analysis, "True if: only one climax note exists")
        self.climax_note = max(self.analysis.pitches)
        self.success = False

    def apply(self):
        self.success = self.analysis.pitches.count(self.climax_note) == 1
        self.analysis.results['SHAPE_NUM_CLIMAX'] = True if self.success else\
            [i + 1 for i in range(len(self.analysis.pitches)) if self.analysis.pitches[i] == self.climax_note][1:]

    def display(self, index):
        print('-------------------------------------------------------------------')
        print(f"Rule {index + 1}: {self.title}")
        print(self.success)


class ShapeArchlike(Rule):
    """
    Tests that the climax appears in the middle third of the melody.
    """
    def __init__(self, analysis):
        super().__init__(analysis, "True if: the climax appears in the middle third of the melody")
        self.climax_note = max(self.analysis.pitches)
        self.success = False

    def apply(self):
        middle_third_range = (len(self.analysis.pitches) // 3, 2 * len(self.analysis.pitches) // 3)
        self.success = middle_third_range[0] <= self.analysis.pitches.index(self.climax_note) <= middle_third_range[1]
        self.analysis.results['SHAPE_ARCHLIKE'] = True if self.success else\
            [i + 1 for i in range(len(self.analysis.pitches))
             if self.analysis.pitches[i] == self.climax_note
             and (i < middle_third_range[0] or i > middle_third_range[1])]

    def display(self, index):
        print('-------------------------------------------------------------------')
        print(f"Rule {index + 1}: {self.title}")
        print(self.success)


# A class representing a melodic analysis of a voice in a score. The class
# has three attributes to being with, you will likely add more attributes.
# * self.score: The score passed into the analysis
# * self.rules: A list of rules that you define to implement the analysis
# * self.results: A dictionary containing the set of analytical checks your
# analysis performs. Your rules will update specific checks in this dictionary.
class MelodicAnalysis(Analysis):
    def __init__(self, score):
        # Call the superclass and give it the score. Don't change this line.
        super().__init__(score)
        # Copy the empty result checks template to this analysis. Don't
        # change this line
        self.results = copy(melodic_checks)

        # Adding instance variables for rules:
        self.timepoints = timepoints(score, measures=False)
        self.melody = [t.nmap['P1.1'] for t in self.timepoints]
        self.pitches = [n.pitch for n in self.melody]
        self.intervals = [Interval(n1, n2) for n1, n2 in zip(self.pitches, self.pitches[1:])]
        self.spans = [i.lines_and_spaces() * i.sign for i in self.intervals]

        # Create the list of rules this analysis runs. This example just
        # uses the demo Rule defined above.
        self.rules = [MelodyStartNoteRule(self),
                      MelodicCadenceRule(self),
                      MelodyWithinTessitura(self),
                      MelodyDiatonic(self),
                      IntervalsStepwise(self),
                      IntervalsConsonant(self),
                      IntervalsSimple(self),
                      IntervalsNumLarge(self),
                      IntervalsNumUnisons(self),
                      IntervalsSameDirection(self),
                      LeapNumberConsecutive(self),
                      ShapeNumberClimax(self),
                      ShapeArchlike(self)]

    # You can define a cleanup function if you want.
    def cleanup(self):
        self.melody, self.intervals = [], []

    # You MUST define a setup function! A first few steps are
    # done for you, you can add more steps as you wish.
    def setup(self, args, kwargs):
        assert len(args) == 1, "Call: analyze('pvid')"
        # melodic_id is the voice to analyze passed in by the caller.
        # you will want to use this when you access the timepoints
        melodic_id = args[0]
        tps = timepoints(self.score, span=True, measures=False)

    # This function is given to you, it returns your analysis results
    # for the autograder to check.  You can also use this function as
    # a top level call for testing. Just make sure that it always returns
    # self.results after the analysis has been performed!
    def submit_to_grading(self):
        # Call analyze() and pass it the pvid used in all the Laitz scores.
        self.analyze('P1.1')
        # Return the results to the caller.
        return self.results


"""
Console testing lines:

from hw8.score import import_score
from hw8.laitz82 import *
s = import_score('hw8/xmls/Laitz_p84F.musicxml')
m = MelodicAnalysis(s)
m.submit_to_grading()

"""
