########################################

# You can import from score, theory, and any python system modules you want.

from .score import Note, Pitch, Rest, Interval, Ratio, Mode, import_score
from .theory import Analysis, Rule, timepoints
from copy import copy
from math import inf

# Settings for a species 1 analysis. Pass this to SpeciesAnalysis() if you
# are analyzing a species 1 score. See also: SpeciesAnalysis.
s1_settings = {
    # Maximum number of melodic unisons allowed.
    'MAX_UNI': 1,
    # Maximum number of melodic 4ths allowed.
    'MAX_4TH': 2,
    # Maximum number of melodic 5ths allowed.
    'MAX_5TH': 1,
    # Maximum number of melodic 6ths allowed.
    'MAX_6TH': 0,
    # Maximum number of melodic 7ths allowed.
    'MAX_7TH': 0,
    # Maximum number of melodic 8vas allowed.
    'MAX_8VA': 0,
    # Maximum number of leaps larger than a 3rd.
    'MAX_LRG': 2,
    # Maximum number of consecutive melodic intervals moving in same direction.
    'MAX_SAMEDIR': 3,
    # Maximum number of parallel consecutive harmonic 3rds/6ths.
    'MAX_PARALLEL': 3,
    # Maximum number of consecutive leaps of any type.
    'MAX_CONSEC_LEAP': 2,
    # Smallest leap demanding recovery step in opposite direction.
    'STEP_THRESHOLD': 5,
    # List of allowed starting scale degrees of a CP that is above the CF.
    'START_ABOVE': [1, 5],
    # List of allowed starting scale degrees of a CP that is below the CF.
    'START_BELOW': [1],
    # List of allowed melodic cadence patterns for the CP.
    'CADENCE_PATTERNS': [[2, 1], [7, 1]]
}

# Settings for species 2 analysis. Pass this to SpeciesAnalysis() if you
# are analyzing a second species score. See also: SpeciesAnalysis.
s2_settings = copy(s1_settings)
s2_settings['START_ABOVE'] = [1, 3, 5]
s2_settings['MAX_4TH'] = inf  # no limit on melodic fourths
s2_settings['MAX_5TH'] = inf  # no limit on melodic fifths
s2_settings['MAX_UNI'] = 0    # no melodic unisons allowed

# A list of all the possible result strings your analysis can generate.
# The {} marker in each string will always receive the 1-based integer index
# of the left-side time point that contains the offending issue. For example,
# if the first timepoint (e.g. self.timepoints[0]) contained an illegal
# starting pitch the message would be: 'At 1: forbidden starting pitch'
# Note: the variable result_strings does not need to be used by your code,
# it simply contains the list of all the result strings ;)
result_strings = [
    # VERTICAL RESULTS
    'At #{}: consecutive unisons',
    'At #{}: consecutive fifths',
    'At #{}: consecutive octaves',
    'At #{}: direct unisons',
    'At #{}: direct fifths',
    'At #{}: direct octaves',
    'At #{}: consecutive unisons in cantus firmus notes',  # if species 2
    'At #{}: consecutive fifths in cantus firmus notes',   # if species 2
    'At #{}: consecutive octaves in cantus firmus notes',  # if species 2
    'At #{}: voice overlap',
    'At #{}: voice crossing',
    'At #{}: forbidden weak beat dissonance',   # vertical dissonance
    'At #{}: forbidden strong beat dissonance',  # vertical dissonance
    'At #{}: too many consecutive parallel intervals',  # parallel vertical intervals

    # MELODIC RESULTS
    'At #{}: forbidden starting pitch',  # 14
    'At #{}: forbidden rest', 
    'At #{}: forbidden duration',   
    'At #{}: missing melodic cadence',
    'At #{}: forbidden non-diatonic pitch',
    'At #{}: dissonant melodic interval',
    'At #{}: too many melodic unisons',         # 'MAX_UNI' setting
    'At #{}: too many leaps of a fourth',       # 'MAX_4TH' setting
    'At #{}: too many leaps of a fifth',        # 'MAX_5TH' setting
    'At #{}: too many leaps of a sixth',        # 'MAX_6TH' setting
    'At #{}: too many leaps of a seventh',      # 'MAX_7TH' setting
    'At #{}: too many leaps of an octave',      # 'MAX_8VA' setting
    'At #{}: too many large leaps',             # 'MAX_LRG' setting
    'At #{}: too many consecutive leaps'        # 'MAX_COtNSEC_LEAP' setting
    'At #{}: too many consecutive intervals in same direction', # 'MAX_SAMEDIR' setting
    'At #{}: missing reverse by step recovery', # 'STEP_THRESHOLD' setting
    'At #{}: forbidden compound melodic interval',
    ]


# A class that implements a species counterpoint analysis of a given score.
# A SpeciesAnalysis has at least 5 attributes, you will very likely add more:
#
# * self.score  The score being analyzed.
# * self.species  The integer species number of the analysis, either 1 or 2.
# * self.settings  A settings dict for the analysis, either s1_settings or s2_settings.
# * self.rules  An ordered list of Rules that constitute your analysis.
# * self.results  A list of strings (see below) that constitute your analysis findings.
#
# You should call your analysis like this:
#
#   score = import_score(species1_xmlfile)
#   analysis = SpeciesAnalysis(score, 1, s1_settings)
#   analysis.submit_to_grading()
class SpeciesAnalysis(Analysis):
    # Initializes a species analysis.
    # @param score A score containing a two-part species composition.
    # @param species A counterpoint species number, either 1 or 2.
    def __init__(self, score, species):
        # Call the superclass and give it the score.
        super().__init__(score)
        if species not in [1, 2]:
            raise ValueError(f"'{species}' is not a valid species number 1 or 2.")
        # The integer species number for the analysis.
        self.species = species

        # Adding variables needed for rules. (This could be done in setup() but it's easier
        # to have them as instance variables.
        self.timepoints = timepoints(score, measures=False, span=True)
        self.part1 = [t.nmap['P1.1'] for t in self.timepoints]
        self.part2 = [t.nmap['P2.1'] for t in self.timepoints]

        # Setting counterpoint and cantus firmus
        self.cp_is_above = score.parts[0].name == 'CP'
        self.cf = self.part2 if self.cp_is_above else self.part1
        self.cp = self.part1 if self.cp_is_above else self.part2

        # Getting pitches, intervals within melody, and intervals between parts
        self.cf_pitches = [n.pitch for n in self.cf]
        self.cp_pitches = [n.pitch for n in self.cp]

        self.cf_intervals_melody = [Interval(n1, n2) for n1, n2 in zip(self.cf_pitches, self.cf_pitches[1:])]
        self.cp_intervals_melody = [Interval(n1, n2) for n1, n2 in zip(self.cp_pitches, self.cp_pitches[1:])]

        self.cf_spans_melody = [i.lines_and_spaces() * i.sign for i in self.cf_intervals_melody]
        self.cp_spans_melody = [i.lines_and_spaces() * i.sign for i in self.cp_intervals_melody]

        self.intervals = [Interval(cp, cf) if self.cp_is_above else Interval(cf, cp)
                          for cf, cp in zip(self.cp_pitches, self.cf_pitches)]
        self.spans = [i.lines_and_spaces() * i.sign for i in self.intervals]

        # A local copy of the analysis settings.
        self.settings = copy(s1_settings) if species == 1 else copy(s2_settings)
        # Add your rules to this list.
        self.rules = [ConsecutiveUnisonsRule(self),
                      ConsecutiveFifthsRule(self),
                      ConsecutiveOctavesRule(self),
                      DirectUnisonsRule(self),
                      DirectFifthsRule(self),
                      DirectOctavesRule(self),
                      StartNoteRule(self),
                      MelodicCadenceRule(self)]
        # A list of strings that represent the findings of your analysis.
        self.results = []

    # Use this function to perform whatever setup actions your rules require.
    def setup(self, args, kwargs):
        pass
    
    # This function is given to you, it returns your analysis results
    # for the autograder to check.  You can also use this function as
    # a top level call for testing. Just make sure that it always returns
    # self.results after the analysis has been performed.
    def submit_to_grading(self):
        self.analyze()
        # When you return your results to the autograder make sure you convert
        # it to a Python set, like this:
        print('-------------------------------------------------------------------')
        return set(self.results)


################################################################################

# A short list of files that contain lots of issues (see comments below)
root_dir = "C:/Users/Renzo Ledesma/renzol2/finalproj/Species/"
samples = ['2-034-A_zawang2.musicxml', '2-028-C_hanzhiy2.musicxml', '2-000-B_sz18.musicxml',
           '2-003-A_cjrosas2.musicxml', '2-021-B_erf3.musicxml', '1-018-C_ajyanez2.musicxml',
           '2-003_A_chchang6.musicxml', '1-019-A_ajyanez2.musicxml', '2-009-C_mamn2.musicxml',
           '1-005-A_hanzhiy2.musicxml', '2-010-B_mamn2.musicxml', '1-008-C_davidx2.musicxml',
           '1-030_C_chchang6.musicxml', '2-034-C_zawang2.musicxml', '1-011-B_weikeng2.musicxml',
           '2-029-A_hanzhiy2.musicxml', '1-037-A_sz18.musicxml', '1-012-B_erf3.musicxml',
           '1-030-C_cjrosas2.musicxml', '2-009-B_mamn2.musicxml', '2-021-C_erf3.musicxml']

# Direct (parallel) 5ths, 8vas and unisons:
#     '1-037-A_sz18.musicxml'
#     '1-030-C_cjrosas2.musicxml'
#     '2-000-B_sz18.musicxml'
# Direct motion measure to measure (species 2):
#     '2-034-C_zawang2.musicxml'
#     '2-021-C_erf3.musicxml'
# Indirect (hidden) 5ths and 8vas:
#     '1-030_C_chchang6.musicxml'
#     '1-008-C_davidx2.musicxml'
#     '1-030-C_cjrosas2.musicxml'
#     '1-011-B_weikeng2.musicxml'
# Voice overlap:
#     '1-005-A_hanzhiy2.musicxml'
#     '1-019-A_ajyanez2.musicxml'
# Maximum parallel interval:
#     '1-037-A_sz18.musicxml'
# Voice crossing:
#     '1-019-A_ajyanez2.musicxml'
# Disjunction:
#     '1-008-C_davidx2.musicxml'
# Weak beat dissonance not passing tone (species 2):
#     '2-000-B_sz18.musicxml'
#     '2-034-C_zawang2.musicxml'
#     '2-021-C_erf3.musicxml'
# Strong beat dissonance (species 1 and 2):
#     '2-000-B_sz18.musicxml'
#     '2-034-C_zawang2.musicxml'
# Wrong durations:
#     '2-009-C_mamn2.musicxml'
#     '2-034-A_zawang2.musicxml'
#     '2-021-B_erf3.musicxml'
#     '2-009-B_mamn2.musicxml'
#     '2-021-C_erf3.musicxml'
# Not diatonic:
#     '1-018-C_ajyanez2.musicxml'
#     '2-003-A_cjrosas2.musicxml'
#     '2-003_A_chchang6.musicxml'
# Starting pitch:
#     '2-028-C_hanzhiy2.musicxml'  # this should be fine
#     '1-012-B_erf3.musicxml'
# Melodic cadence:
#     '1-018-C_ajyanez2.musicxml'
#     '1-030_C_chchang6.musicxml'
#     '2-034-A_zawang2.musicxml'
# Too many 'x':
#     '2-029-A_hanzhiy2.musicxml'
#     '2-003_A_chchang6.musicxml'
#     '2-010-B_mamn2.musicxml'
# Reverse after leap:
#     '2-029-A_hanzhiy2.musicxml'
#     '2-010-B_mamn2.musicxml'

################################################################################

# RULES
# All rules need a success (bool) and format string (string taken from result_strings) attribute


class ConsecutiveUnisonsRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Tests if there are no consecutive unisons between CP and CF")
        self.success = True
        self.incorrect_notes = []

    def apply(self):
        for i in range(1, len(self.analysis.intervals)):
            if self.analysis.intervals[i].lines_and_spaces() == 1 and \
                    self.analysis.intervals[i - 1].lines_and_spaces() == 1:
                self.success = False
                self.incorrect_notes.append(i + 1)

    def display(self, index):
        if not self.success:
            format_string = result_strings[index]
            print(f"Rule {index}: "
                  f"{format_string.format(self.incorrect_notes.__str__().replace('[', '').replace(']', ''))}")


class ConsecutiveFifthsRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Tests if there are no consecutive fifths between CP and CF")
        self.success = True
        self.incorrect_notes = []

    def apply(self):
        for i in range(1, len(self.analysis.intervals)):
            if self.analysis.intervals[i].lines_and_spaces() == 5 and \
                    self.analysis.intervals[i - 1].lines_and_spaces() == 5:
                self.success = False
                self.incorrect_notes.append(i + 1)

    def display(self, index):
        if not self.success:
            format_string = result_strings[index]
            print(f"Rule {index}: "
                  f"{format_string.format(self.incorrect_notes.__str__().replace('[', '').replace(']', ''))}")


class ConsecutiveOctavesRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Tests if there are no consecutive octaves between CP and CF")
        self.success = True
        self.incorrect_notes = []

    def apply(self):
        for i in range(1, len(self.analysis.intervals)):
            if self.analysis.intervals[i].lines_and_spaces() == 8 and \
                    self.analysis.intervals[i - 1].lines_and_spaces() == 8:
                self.success = False
                self.incorrect_notes.append(i + 1)

    def display(self, index):
        if not self.success:
            format_string = result_strings[index]
            print(f"Rule {index}: "
                  f"{format_string.format(self.incorrect_notes.__str__().replace('[', '').replace(']', ''))}")


class DirectUnisonsRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Tests if there are no illegal direct unisons between CP and CF")
        self.success = True
        self.incorrect_notes = []

    def apply(self):
        for i in range(1, len(self.analysis.intervals)):
            if self.analysis.intervals[i].lines_and_spaces() == 1:
                samedir = (self.analysis.cp_spans_melody[i-1] > 0 and self.analysis.cf_spans_melody[i-1] > 0) or \
                          (self.analysis.cp_spans_melody[i-1] < 0 and self.analysis.cf_spans_melody[i-1] < 0)
                if samedir:
                    self.success = False
                    self.incorrect_notes.append(i + 1)

    def display(self, index):
        if not self.success:
            format_string = result_strings[index]
            print(f"Rule {index}: "
                  f"{format_string.format(self.incorrect_notes.__str__().replace('[', '').replace(']', ''))}")


class DirectFifthsRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Tests if there are no illegal direct fifths between CP and CF")
        self.success = True
        self.incorrect_notes = []

    def apply(self):
        for i in range(1, len(self.analysis.intervals)):
            if self.analysis.intervals[i].lines_and_spaces() == 5:
                samedir = (self.analysis.cp_spans_melody[i-1] > 0 and self.analysis.cf_spans_melody[i-1] > 0) or \
                          (self.analysis.cp_spans_melody[i-1] < 0 and self.analysis.cf_spans_melody[i-1] < 0)
                if samedir:
                    self.success = False
                    self.incorrect_notes.append(i + 1)

    def display(self, index):
        if not self.success:
            format_string = result_strings[index]
            print(f"Rule {index}: "
                  f"{format_string.format(self.incorrect_notes.__str__().replace('[', '').replace(']', ''))}")


class DirectOctavesRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Tests if there are no illegal direct octaves between CP and CF")
        self.success = True
        self.incorrect_notes = []

    def apply(self):
        for i in range(1, len(self.analysis.intervals)):
            if self.analysis.intervals[i].lines_and_spaces() == 8:
                samedir = (self.analysis.cp_spans_melody[i-1] > 0 and self.analysis.cf_spans_melody[i-1] > 0) or \
                          (self.analysis.cp_spans_melody[i-1] < 0 and self.analysis.cf_spans_melody[i-1] < 0)
                if samedir:
                    self.success = False
                    self.incorrect_notes.append(i + 1)

    def display(self, index):
        if not self.success:
            format_string = result_strings[index]
            print(f"Rule {index}: "
                  f"{format_string.format(self.incorrect_notes.__str__().replace('[', '').replace(']', ''))}")


class StartNoteRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Tests if starting note of melody is valid")
        self.success = False
        self.format_string = result_strings[14]
        key = self.analysis.score.parts[0].staffs[0].bars[0].key
        cp_placement = 'START_ABOVE' if self.analysis.cp_is_above else 'START_BELOW'
        self.valid_starting_notes = [key.scale()[d - 1] for d in self.analysis.settings[cp_placement]]

    def apply(self):
        self.success = self.analysis.cp_pitches[0].pnum() in self.valid_starting_notes

    def display(self, index):
        if not self.success:
            print(f"Rule {index}: {self.format_string.format(1)}")


class MelodicCadenceRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Tests if ending cadence is 7 - 1 or 2 - 1")
        self.success = False
        self.format_string = result_strings[17]
        self.incorrect_notes = []
        self.key = self.analysis.score.parts[0].staffs[0].bars[0].key
        scale = self.key.scale()
        # Change to harmonic minor
        if self.key.mode == Mode.MINOR:
            scale[-1] = Interval('-m2').transpose(Interval('M2').transpose(scale[-1]))
        self.cadence = [p.pnum() for p in self.analysis.cp_pitches[-2:]]
        self.valid_cadences = [[scale[d - 1] for d in cadence]
                               for cadence in self.analysis.settings['CADENCE_PATTERNS']]

    def apply(self):
        self.success = self.cadence in self.valid_cadences
        if not self.success:
            if self.analysis.cp_pitches[-2].pnum() is not self.key.scale()[-1] or \
                    self.analysis.cp_pitches[-2].pnum() is not self.key.scale()[1]:
                self.incorrect_notes.append(len(self.analysis.cp_pitches) - 1)
            if self.analysis.cp_pitches[-1].pnum() is not self.key.tonic():
                self.incorrect_notes.append(len(self.analysis.cp_pitches))

    def display(self, index):
        if not self.success:
            print(
                f"Rule {index}: "
                f"{self.format_string.format(self.incorrect_notes.__str__().replace('[', '').replace(']', ''))}")


"""
CONSOLE TESTING
All scores:

from finalproj.species import *
for sample in samples:
    print(sample)
    s = import_score(root_dir + sample)
    a = SpeciesAnalysis(s, int(sample[0]))
    a.submit_to_grading()

One score (change sample):

from finalproj.species import *
sample = '1-030_C_chchang6.musicxml'
s = import_score(root_dir + sample)
a = SpeciesAnalysis(s, int(sample[0]))
a.submit_to_grading()

"""
