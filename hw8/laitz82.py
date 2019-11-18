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
    'LEAP_RECOVERY': None,

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
    'SHAPE_UNIQUE': None
}


# Here is an example of a rule. You can define as many rules as you want.
# The purpose of running a rule is to perform some analytical check(s) and
# then update the self.analysis.results dictionary with its findings.
class MelodyStartNoteRule(Rule):

    # Rule initializer.
    def __init__(self, analysis):
        # Always set the rule's back pointer to its analysis!
        super().__init__(analysis, "Starting note is in melodic triad")
        # Now initialize whatever attributes your rule defines.
        # ...
        # Need to grab the key from the first bar of the score...
        self.key = self.analysis.score.parts[0].staffs[0].bars[0].key
        self.tonic_triad = {self.key.scale()[0], self.key.scale()[2], self.key.scale()[4]}
        # print(vars(self.analysis))
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
        """
        Constructor for the rule.
        :param analysis: Backpointer to the (Melodic) analysis of the rule.
        """
        super().__init__(analysis, "Ending cadence is 7 - 1 or 2 - 1")

        # grabbing information...
        self.key = self.analysis.score.parts[0].staffs[0].bars[0].key
        self.cadence = [p.pnum() for p in self.analysis.pitches[-2:]]
        self.cadence7_1 = [self.key.scale()[-1], self.key.tonic()]
        self.cadence2_1 = [self.key.scale()[1], self.key.tonic()]
        self.success = False

    def apply(self):
        """
        Determines whether the rule is met or not.
        """
        self.success = self.cadence == self.cadence2_1 or self.cadence == self.cadence7_1
        self.analysis.results['MEL_CADENCE'] = True if self.success else []

    # Uncomment this code if you want your rule to print information to the
    # the terminal just after it runs...
    def display(self, index):
        print('-------------------------------------------------------------------')
        print(f"Rule {index+1}: {self.title}")
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

        # Create the list of rules this analysis runs. This example just
        # uses the demo Rule defined above.
        self.rules = [MelodyStartNoteRule(self), MelodicCadenceRule(self)]

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

