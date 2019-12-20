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
s2_settings['MAX_UNI'] = 0  # no melodic unisons allowed

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
    'At #{}: consecutive fifths in cantus firmus notes',  # if species 2
    'At #{}: consecutive octaves in cantus firmus notes',  # if species 2
    'At #{}: voice overlap',  # 2 gram
    'At #{}: voice crossing',  # 1 gram
    'At #{}: forbidden weak beat dissonance',  # vertical dissonance
    'At #{}: forbidden strong beat dissonance',  # vertical dissonance
    'At #{}: too many consecutive parallel intervals',  # parallel vertical intervals

    # MELODIC RESULTS
    'At #{}: forbidden starting pitch',  # 14
    'At #{}: forbidden rest',
    'At #{}: forbidden duration',
    'At #{}: missing melodic cadence',
    'At #{}: forbidden non-diatonic pitch',
    'At #{}: dissonant melodic interval',  # 19
    'At #{}: too many melodic unisons',  # 'MAX_UNI' setting
    'At #{}: too many leaps of a fourth',  # 'MAX_4TH' setting
    'At #{}: too many leaps of a fifth',  # 'MAX_5TH' setting
    'At #{}: too many leaps of a sixth',  # 'MAX_6TH' setting
    'At #{}: too many leaps of a seventh',  # 'MAX_7TH' setting
    'At #{}: too many leaps of an octave',  # 'MAX_8VA' setting
    'At #{}: too many large leaps',  # 'MAX_LRG' setting 26
    'At #{}: too many consecutive leaps',  # 'MAX_CONSEC_LEAP' setting
    'At #{}: too many consecutive intervals in same direction',  # 'MAX_SAMEDIR' setting
    'At #{}: missing reverse by step recovery',  # 'STEP_THRESHOLD' setting
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
        self.timepoints_measures = timepoints(score, measures=True, span=True)
        self.part1 = [t.nmap['P1.1'] for t in self.timepoints]
        self.part2 = [t.nmap['P2.1'] for t in self.timepoints]

        # Setting counterpoint and cantus firmus
        self.cp_is_above = score.parts[0].name == 'CP'
        self.cf = self.part2 if self.cp_is_above else self.part1
        self.cp = self.part1 if self.cp_is_above else self.part2

        # Getting pitches, intervals within melody, and intervals between parts
        self.cf_pitches = [n.pitch if not isinstance(n, Rest) else Pitch() for n in self.cf]
        self.cp_pitches = [n.pitch if not isinstance(n, Rest) else Pitch() for n in self.cp]

        # This part removes rests, because any rule that needs rests will take them from timepoints directly.
        # I don't know if this will work but we'll see!
        i = 0
        while i < len(self.cp_pitches):
            if self.cp_pitches[i].is_empty():
                self.cp_pitches.pop(i)
                self.cf_pitches.pop(i)
                i -= 1
            i += 1

        self.cf_intervals_melody = [Interval(n1, n2) for n1, n2 in zip(self.cf_pitches, self.cf_pitches[1:])]
        self.cp_intervals_melody = [Interval(n1, n2) for n1, n2 in zip(self.cp_pitches, self.cp_pitches[1:])]

        self.cf_spans_melody = [i.lines_and_spaces() * i.sign for i in self.cf_intervals_melody]
        self.cp_spans_melody = [i.lines_and_spaces() * i.sign for i in self.cp_intervals_melody]

        self.intervals = [Interval(cp, cf) if self.cp_is_above else Interval(cf, cp)
                          for cf, cp in zip(self.cp_pitches, self.cf_pitches)]
        self.spans = [i.lines_and_spaces() * i.sign for i in self.intervals]

        # Setting downbeats and weakbeats for second species scores.
        if self.species == 2:
            # Getting timepoints separated by measure and populating downbeats/weakbeats with timepoints.
            self.downbeats = [measure[0] for measure in self.timepoints_measures]
            self.weakbeats = []
            for measure in self.timepoints_measures:
                try:
                    self.weakbeats.append(measure[1])
                except IndexError:
                    pass
            # Getting notes.
            # Also preserving the index of each timepoint because rules need to know the positions of notes that
            # violate that specific rule.
            self.part1_downbeats = [(t.nmap['P1.1'], t.index) for t in self.downbeats]
            self.part1_weakbeats = [(t.nmap['P1.1'], t.index) for t in self.weakbeats]
            self.part2_downbeats = [(t.nmap['P2.1'], t.index) for t in self.downbeats]
            self.part2_weakbeats = [(t.nmap['P2.1'], t.index) for t in self.weakbeats]

            # Distinguishing between CF and CP.
            self.cf_downbeats = self.part2_downbeats if self.cp_is_above else self.part1_downbeats
            self.cf_weakbeats = self.part2_weakbeats if self.cp_is_above else self.part1_weakbeats
            self.cp_downbeats = self.part1_downbeats if self.cp_is_above else self.part2_downbeats
            self.cp_weakbeats = self.part1_weakbeats if self.cp_is_above else self.part2_weakbeats

            # Getting pitches and intervals from notes.
            # 0 = Object (note/pitch), 1 = index of that object's original timepoint
            self.cf_downbeats_pitches = [(n[0].pitch if not isinstance(n[0], Rest) else Pitch(), n[1])
                                         for n in self.cf_downbeats]
            self.cf_weakbeats_pitches = [(n[0].pitch if not isinstance(n[0], Rest) else Pitch(), n[1])
                                         for n in self.cf_weakbeats]
            self.cp_downbeats_pitches = [(n[0].pitch if not isinstance(n[0], Rest) else Pitch(), n[1])
                                         for n in self.cp_downbeats]
            self.cp_weakbeats_pitches = [(n[0].pitch if not isinstance(n[0], Rest) else Pitch(), n[1])
                                         for n in self.cp_weakbeats]

            # Rid of any rests (don't know if this works.. but it seems to for now!)
            i = 0
            while i < len(self.cp_downbeats_pitches):
                if self.cp_downbeats_pitches[i][0].is_empty():
                    self.cp_downbeats_pitches.pop(i)
                    self.cf_downbeats_pitches.pop(i)
                    i -= 1
                i += 1
            i = 0
            while i < len(self.cp_weakbeats_pitches):
                if self.cp_weakbeats_pitches[i][0].is_empty():
                    self.cp_weakbeats_pitches.pop(i)
                    self.cf_weakbeats_pitches.pop(i)
                    i -= 1
                i += 1

            self.intervals_downbeats = [(Interval(cp[0], cf[0]), cp[1]) if self.cp_is_above
                                        else (Interval(cf[0], cp[0]), cp[1])
                                        for cf, cp in zip(self.cp_downbeats_pitches, self.cf_downbeats_pitches)]
            self.intervals_weakbeats = [(Interval(cp[0], cf[0]), cp[1]) if self.cp_is_above
                                        else (Interval(cf[0], cp[0]), cp[1])
                                        for cf, cp in zip(self.cp_weakbeats_pitches, self.cf_weakbeats_pitches)]

        # A local copy of the analysis settings.
        self.settings = copy(s1_settings) if species == 1 else copy(s2_settings)
        # Add your rules to this list.
        self.rules = [ConsecutiveUnisonsRule(self),
                      ConsecutiveFifthsRule(self),
                      ConsecutiveOctavesRule(self),
                      DirectUnisonsRule(self),
                      DirectFifthsRule(self),
                      DirectOctavesRule(self),
                      ConsecutiveUnisonsDownbeatRule(self),
                      ConsecutiveFifthsDownbeatRule(self),
                      ConsecutiveOctavesDownbeatRule(self),
                      VoiceOverlappingRule(self),
                      VoiceCrossingRule(self),
                      WeakBeatDissonanceRule(self),
                      StrongBeatDissonanceRule(self),
                      ConsecutiveParallelIntervalsRule(self),
                      StartNoteRule(self),
                      ForbiddenRestRule(self),
                      ForbiddenDurationRule(self),
                      MelodicCadenceRule(self),
                      ForbiddenNonDiatonicPitchRule(self),
                      DissonantMelodicIntervalRule(self),
                      MelodicUnisonsRule(self),
                      MelodicFourthsRule(self),
                      MelodicFifthsRule(self),
                      MelodicSixthRule(self),
                      MelodicSeventhRule(self),
                      MelodicOctaveRule(self),
                      LargeLeapsRule(self),
                      LeapConsecutiveRule(self),
                      IntervalsSameDirectionRule(self),
                      ReverseByStepRecoveryRule(self),
                      ForbiddenCompoundIntervalRule(self)]
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
INTERVAL_INDEX, PITCH_INDEX = 0, 0
NOTE_INDEX = 1


class ConsecutiveUnisonsRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Tests if there are no consecutive unisons between CP and CF")
        self.success = True
        self.incorrect_notes = []

    def apply(self):
        for i in range(1, len(self.analysis.intervals)):
            interval = 1
            weak_to_downbeat = False
            is_consecutive = self.analysis.intervals[i].lines_and_spaces() == interval and \
                             self.analysis.intervals[i - 1].lines_and_spaces() == interval
            if is_consecutive and self.analysis.species == 2:
                weakbeat_intervals = [i[INTERVAL_INDEX] for i in self.analysis.intervals_weakbeats]
                downbeat_intervals = [i[INTERVAL_INDEX] for i in self.analysis.intervals_downbeats]
                # these are checking references to variables, not the variable's contents
                prev_interval_in_weak = True in [self.analysis.intervals[i - 1] is weak for weak in weakbeat_intervals]
                curr_interval_in_down = True in [self.analysis.intervals[i] is down for down in downbeat_intervals]
                weak_to_downbeat = prev_interval_in_weak and curr_interval_in_down
            elif self.analysis.species == 1:
                weak_to_downbeat = True
            if is_consecutive and weak_to_downbeat:
                self.success = False
                self.incorrect_notes.append(i + 1)

    def display(self, index):
        if not self.success:
            format_string = result_strings[index]
            for note in self.incorrect_notes:
                self.analysis.results.append(format_string.format(note))


class ConsecutiveFifthsRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Tests if there are no consecutive fifths between CP and CF")
        self.success = True
        self.incorrect_notes = []

    def apply(self):
        for i in range(1, len(self.analysis.intervals)):
            interval = 5
            weak_to_downbeat = False
            is_consecutive = self.analysis.intervals[i].lines_and_spaces() == interval and \
                             self.analysis.intervals[i - 1].lines_and_spaces() == interval
            if is_consecutive and self.analysis.species == 2:
                weakbeat_intervals = [i[INTERVAL_INDEX] for i in self.analysis.intervals_weakbeats]
                downbeat_intervals = [i[INTERVAL_INDEX] for i in self.analysis.intervals_downbeats]
                # these are checking references to variables, not the variable's contents
                prev_interval_in_weak = True in [self.analysis.intervals[i - 1] is weak for weak in weakbeat_intervals]
                curr_interval_in_down = True in [self.analysis.intervals[i] is down for down in downbeat_intervals]
                weak_to_downbeat = prev_interval_in_weak and curr_interval_in_down
            elif self.analysis.species == 1:
                weak_to_downbeat = True
            if is_consecutive and weak_to_downbeat:
                self.success = False
                self.incorrect_notes.append(i)

    def display(self, index):
        if not self.success:
            format_string = result_strings[index]
            for note in self.incorrect_notes:
                self.analysis.results.append(format_string.format(note))


class ConsecutiveOctavesRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Tests if there are no consecutive octaves between CP and CF")
        self.success = True
        self.incorrect_notes = []

    def apply(self):
        for i in range(1, len(self.analysis.intervals)):
            interval = 8
            weak_to_downbeat = False
            is_consecutive = self.analysis.intervals[i].lines_and_spaces() == interval and \
                             self.analysis.intervals[i - 1].lines_and_spaces() == interval
            if is_consecutive and self.analysis.species == 2:
                weakbeat_intervals = [i[INTERVAL_INDEX] for i in self.analysis.intervals_weakbeats]
                downbeat_intervals = [i[INTERVAL_INDEX] for i in self.analysis.intervals_downbeats]
                # these are checking references to variables, not the variable's contents
                prev_interval_in_weak = True in [self.analysis.intervals[i - 1] is weak for weak in weakbeat_intervals]
                curr_interval_in_down = True in [self.analysis.intervals[i] is down for down in downbeat_intervals]
                weak_to_downbeat = prev_interval_in_weak and curr_interval_in_down
            elif self.analysis.species == 1:
                weak_to_downbeat = True
            if is_consecutive and weak_to_downbeat:
                self.success = False
                self.incorrect_notes.append(i + 1)

    def display(self, index):
        if not self.success:
            format_string = result_strings[index]
            for note in self.incorrect_notes:
                self.analysis.results.append(format_string.format(note))


class DirectUnisonsRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Tests if there are no illegal direct unisons between CP and CF")
        self.success = True
        self.incorrect_notes = []

    def apply(self):
        for i in range(1, len(self.analysis.intervals)):
            if self.analysis.intervals[i].lines_and_spaces() == 1:
                samedir = (self.analysis.cp_spans_melody[i - 1] > 1 and self.analysis.cf_spans_melody[i - 1] > 1) or \
                          (self.analysis.cp_spans_melody[i - 1] < -1 and self.analysis.cf_spans_melody[i - 1] < -1)
                valid = self.analysis.cp_is_above and abs(self.analysis.cp_spans_melody[i - 1]) == 2
                if samedir and not valid:  # stepwise motion is okay
                    self.success = False
                    self.incorrect_notes.append(i)

    def display(self, index):
        if not self.success:
            format_string = result_strings[index]
            for note in self.incorrect_notes:
                self.analysis.results.append(format_string.format(note))


class DirectFifthsRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Tests if there are no illegal direct fifths between CP and CF")
        self.success = True
        self.incorrect_notes = []

    def apply(self):
        for i in range(1, len(self.analysis.intervals)):
            if self.analysis.intervals[i].lines_and_spaces() == 5:
                samedir = (self.analysis.cp_spans_melody[i - 1] > 1 and self.analysis.cf_spans_melody[i - 1] > 1) or \
                          (self.analysis.cp_spans_melody[i - 1] < -1 and self.analysis.cf_spans_melody[i - 1] < -1)
                valid = self.analysis.cp_is_above and abs(self.analysis.cp_spans_melody[i - 1]) == 2
                if samedir and not valid:
                    self.success = False
                    self.incorrect_notes.append(i)

    def display(self, index):
        if not self.success:
            format_string = result_strings[index]
            for note in self.incorrect_notes:
                consec_fifths_string = result_strings[1].format(note)
                if self.analysis.results.count(consec_fifths_string) == 0:
                    self.analysis.results.append(format_string.format(note))


class DirectOctavesRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Tests if there are no illegal direct octaves between CP and CF")
        self.success = True
        self.incorrect_notes = []

    def apply(self):
        for i in range(1, len(self.analysis.intervals)):
            if self.analysis.intervals[i].lines_and_spaces() == 8:
                samedir = (self.analysis.cp_spans_melody[i - 1] > 1 and self.analysis.cf_spans_melody[i - 1] > 1) or \
                          (self.analysis.cp_spans_melody[i - 1] < -1 and self.analysis.cf_spans_melody[i - 1] < -1)
                valid = self.analysis.cp_is_above and abs(self.analysis.cp_spans_melody[i - 1]) == 2
                if samedir and not valid:
                    self.success = False
                    self.incorrect_notes.append(i)

    def display(self, index):
        if not self.success:
            format_string = result_strings[index]
            for note in self.incorrect_notes:
                self.analysis.results.append(format_string.format(note))


class ConsecutiveUnisonsDownbeatRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Tests if there are no consecutive unisons on downbeats "
                                   "between CP and CF (second species only)")
        self.success = True
        self.incorrect_notes = []

    def apply(self):
        if self.analysis.species == 2:
            for i in range(1, len(self.analysis.intervals_downbeats)):
                if self.analysis.intervals_downbeats[i][INTERVAL_INDEX].lines_and_spaces() == 1 and \
                        self.analysis.intervals_downbeats[i - 1][INTERVAL_INDEX].lines_and_spaces() == 1:
                    self.success = False
                    self.incorrect_notes.append(self.analysis.intervals_downbeats[i][NOTE_INDEX] + 1)

    def display(self, index):
        if not self.success:
            format_string = result_strings[index]
            for note in self.incorrect_notes:
                self.analysis.results.append(format_string.format(note))


class ConsecutiveFifthsDownbeatRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Tests if there are no consecutive fifths on downbeats "
                                   "between CP and CF (second species only)")
        self.success = True
        self.incorrect_notes = []

    def apply(self):
        if self.analysis.species == 2:
            for i in range(1, len(self.analysis.intervals_downbeats)):
                if self.analysis.intervals_downbeats[i][INTERVAL_INDEX].lines_and_spaces() == 5 and \
                        self.analysis.intervals_downbeats[i - 1][INTERVAL_INDEX].lines_and_spaces() == 5:
                    self.success = False
                    self.incorrect_notes.append(self.analysis.intervals_downbeats[i][NOTE_INDEX] + 1)

    def display(self, index):
        if not self.success:
            format_string = result_strings[index]
            for note in self.incorrect_notes:
                self.analysis.results.append(format_string.format(note))


class ConsecutiveOctavesDownbeatRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Tests if there are no consecutive octaves on downbeats "
                                   "between CP and CF (second species only)")
        self.success = True
        self.incorrect_notes = []

    def apply(self):
        if self.analysis.species == 2:
            for i in range(1, len(self.analysis.intervals_downbeats)):
                if self.analysis.intervals_downbeats[i][INTERVAL_INDEX].lines_and_spaces() == 8 and \
                        self.analysis.intervals_downbeats[i - 1][INTERVAL_INDEX].lines_and_spaces() == 8:
                    self.success = False
                    self.incorrect_notes.append(self.analysis.intervals_downbeats[i][NOTE_INDEX] + 1)

    def display(self, index):
        if not self.success:
            format_string = result_strings[index]
            for note in self.incorrect_notes:
                self.analysis.results.append(format_string.format(note))


class VoiceOverlappingRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Tests that there are no instances of voice overlapping")
        self.success = True
        self.incorrect_notes = []

    def apply(self):
        # iterate through each index of both CF and CP
        # if CP is higher:
        #   if CP's note is lower than than the CF's previous note, OVERLAP
        # else CP is lower:
        #   if CP's note is higher than the CF's previous note, OVERLAP
        for i in range(1, len(self.analysis.cp_pitches)):
            overlap = self.analysis.cp_pitches[i] < self.analysis.cf_pitches[i - 1] or \
                      self.analysis.cf_pitches[i] > self.analysis.cp_pitches[i - 1] if self.analysis.cp_is_above \
                      else self.analysis.cp_pitches[i] > self.analysis.cf_pitches[i - 1]
            if overlap:
                self.success = False
                self.incorrect_notes.append(i + 1)

    def display(self, index):
        if not self.success:
            format_string = result_strings[index]
            for note in self.incorrect_notes:
                self.analysis.results.append(format_string.format(note))


class VoiceCrossingRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Tests that there are no instances of voice crossing")
        self.success = True
        self.incorrect_notes = []

    def apply(self):
        for i in range(len(self.analysis.spans)):
            if self.analysis.spans[i] < 0:
                self.success = False
                self.incorrect_notes.append(i + 1)

    def display(self, index):
        if not self.success:
            format_string = result_strings[index]
            for note in self.incorrect_notes:
                self.analysis.results.append(format_string.format(note))


class WeakBeatDissonanceRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Tests that weak beat dissonances are only passing tone dissonances "
                                   "(second species only)")
        self.success = True
        self.incorrect_notes = []

    def apply(self):
        if self.analysis.species == 2:
            for interval in self.analysis.intervals_weakbeats:
                if interval[INTERVAL_INDEX].is_dissonant() or interval[INTERVAL_INDEX].is_fourth():
                    index = interval[NOTE_INDEX]
                    previous_interval = self.analysis.cp_spans_melody[index - 1]
                    next_interval = self.analysis.cp_spans_melody[index]
                    # Check if steps:
                    are_steps = abs(previous_interval) == 2 and abs(next_interval) == 2
                    # Check if same direction (passing motion):
                    is_passing = (previous_interval > 0 and next_interval > 0) or \
                                 (previous_interval < 0 and next_interval < 0)
                    if not (are_steps and is_passing):
                        self.success = False
                        self.incorrect_notes.append(index + 1)

    def display(self, index):
        if not self.success:
            format_string = result_strings[index]
            for note in self.incorrect_notes:
                self.analysis.results.append(format_string.format(note))


class StrongBeatDissonanceRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Tests that there are no dissonances on strong beats "
                                   "(second species only)")
        self.success = True
        self.incorrect_notes = []

    def apply(self):
        intervals_list = self.analysis.intervals if self.analysis.species == 1 else self.analysis.intervals_downbeats
        for interval in intervals_list:
            interval_test = interval if self.analysis.species == 1 else interval[INTERVAL_INDEX]
            if interval_test.is_dissonant() or interval_test.is_fourth():
                self.success = False
                if self.analysis.species == 1:
                    interval_index = [i is interval_test for i in intervals_list].index(True)
                else:
                    index_in_downbeats = [i[INTERVAL_INDEX] is interval_test for i in intervals_list].index(True)
                    interval_index = self.analysis.intervals_downbeats[index_in_downbeats][NOTE_INDEX]
                self.incorrect_notes.append(interval_index + 1)

    def display(self, index):
        if not self.success:
            format_string = result_strings[index]
            for note in self.incorrect_notes:
                self.analysis.results.append(format_string.format(note))


class ConsecutiveParallelIntervalsRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Tests that there are no instances of too many parallel "
                                   "consecutive harmonic thirds/sixths ")
        self.success = True
        self.incorrect_notes = []

    def apply(self):
        max_parallel = s1_settings['MAX_PARALLEL'] if self.analysis.species == 1 else s2_settings['MAX_PARALLEL']
        consecutive_parallel_intervals = 0
        previous_interval = None
        index = 0
        spans = [3, 6]
        for span in self.analysis.spans:
            if span in spans and (previous_interval is None or span == previous_interval):
                consecutive_parallel_intervals += 1
            else:
                consecutive_parallel_intervals = 0
            previous_interval = span
            if consecutive_parallel_intervals > max_parallel:
                self.success = False
                self.incorrect_notes.append(index + 1)
            index += 1

    def display(self, index):
        if not self.success:
            format_string = result_strings[index]
            for note in self.incorrect_notes:
                self.analysis.results.append(format_string.format(note))


class StartNoteRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Tests if starting note of melody is valid")
        self.success = False
        key = self.analysis.score.parts[0].staffs[0].bars[0].key
        cp_placement = 'START_ABOVE' if self.analysis.cp_is_above else 'START_BELOW'
        self.valid_starting_notes = [key.scale()[d - 1] for d in self.analysis.settings[cp_placement]]

    def apply(self):
        self.success = self.analysis.cp_pitches[0].pnum() in self.valid_starting_notes

    def display(self, index):
        format_string = result_strings[index]
        if not self.success:
            self.analysis.results.append(f"{format_string.format(1)}")


class ForbiddenRestRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Tests that there are no forbidden rests")
        self.success = True
        self.incorrect_notes = []

    def apply(self):
        valid_rest_indices = [0] if self.analysis.species == 2 else []
        for i in range(len(self.analysis.cp)):
            if isinstance(self.analysis.cp[i], Rest) and i not in valid_rest_indices:
                self.success = False
                self.incorrect_notes.append(i + 1)

    def display(self, index):
        if not self.success:
            format_string = result_strings[index]
            for note in self.incorrect_notes:
                self.analysis.results.append(format_string.format(note))


class ForbiddenDurationRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Tests that there are no forbidden note durations")
        self.success = True
        self.incorrect_notes = []

    def apply(self):
        # first species: all CP notes must be same duration as CF notes
        # second species: all CP notes must be HALF duration as CF notes
        #   UNLESS: they are same duration AND in the last two measures
        #   BUT: last note MUST be same duration
        accepted_ratio = Ratio(1, self.analysis.species)
        if self.analysis.species == 1:
            for i in range(len(self.analysis.cp)):
                if self.analysis.cp[i].dur / self.analysis.cf[i].dur != accepted_ratio:
                    self.success = False
                    self.incorrect_notes.append(i + 1)
        else:  # if species 2, need to take into account ending rules for species 2
            i = 0
            for measure in self.analysis.timepoints_measures:
                in_final_measure = measure is self.analysis.timepoints_measures[-1]
                for timepoint in measure:
                    cp_note = timepoint.nmap['P1.1'] if self.analysis.cp_is_above else timepoint.nmap['P2.1']
                    cf_note = timepoint.nmap['P2.1'] if self.analysis.cp_is_above else timepoint.nmap['P1.1']
                    in_penultimate_measure = measure is self.analysis.timepoints_measures[-2]
                    is_valid = cp_note.dur / cf_note.dur == accepted_ratio or \
                               (in_penultimate_measure and cp_note.dur / cf_note.dur == Ratio(1, 1))
                    if in_final_measure:
                        # valid only if: length of measure (list) is 1
                        # only want the last of the invalid notes
                        is_valid = len(measure) == 1 or timepoint is not measure[-1]
                    if not is_valid:
                        self.success = False
                        self.incorrect_notes.append(i + 1)
                    i += 1

    def display(self, index):
        if not self.success:
            format_string = result_strings[index]
            for note in self.incorrect_notes:
                self.analysis.results.append(format_string.format(note))


class MelodicCadenceRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Tests if ending cadence is 7 - 1 or 2 - 1")
        self.success = False
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
        format_string = result_strings[index]
        if not self.success:
            for note in self.incorrect_notes:
                self.analysis.results.append(format_string.format(note))


class ForbiddenNonDiatonicPitchRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Tests that there are no forbidden diatonic pitches")
        self.success = True
        self.incorrect_notes = []
        self.key = self.analysis.score.parts[0].staffs[0].bars[0].key
        self.scale = self.key.scale()
        # Change to harmonic minor
        if self.key.mode == Mode.MINOR:
            self.harmonic_minor_scale = copy(self.scale)
            self.harmonic_minor_scale[-1] = Interval('-m2').transpose(Interval('M2').transpose(self.scale[-1]))
            self.harmonic_minor_scale[-2] = Interval('-m2').transpose(Interval('M2').transpose(self.scale[-2]))

    def apply(self):
        penultimate_measure = self.analysis.timepoints_measures[-2]
        penultimate_measure_notes = [t.nmap['P1.1'].pitch.pnum() if self.analysis.cp_is_above
                                     else t.nmap['P2.1'].pitch.pnum() for t in penultimate_measure]
        for i in range(len(self.analysis.cp_pitches)):
            is_diatonic = self.analysis.cp_pitches[i].pnum() in self.scale
            if self.key.mode == Mode.MINOR:
                valid_raised_seventh = self.analysis.cp_pitches[i].pnum() == self.harmonic_minor_scale[-1] and \
                                       self.analysis.cp_pitches[i].pnum() in penultimate_measure_notes
                valid_raised_sixth = self.analysis.cp_pitches[i].pnum() == self.harmonic_minor_scale[-2] and \
                                     self.analysis.cp_pitches[i + 1].pnum() == self.harmonic_minor_scale[-1]
                if valid_raised_seventh or valid_raised_sixth:
                    is_diatonic = True
            if not is_diatonic:
                self.success = False
                self.incorrect_notes.append(i + 1)

    def display(self, index):
        format_string = result_strings[index]
        if not self.success:
            for note in self.incorrect_notes:
                self.analysis.results.append(format_string.format(note))


class DissonantMelodicIntervalRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Tests that there are no dissonant melodic intervals in CP")
        self.success = True
        self.incorrect_notes = []

    def apply(self):
        valid_seconds = [Interval('m2'), Interval('-m2'), Interval('M2'), Interval('-M2')]
        is_consonant = [i.is_consonant() or i in valid_seconds for i in self.analysis.cp_intervals_melody]
        self.success = not (False in is_consonant)
        if not self.success:
            self.incorrect_notes = [i + 1 for i in range(len(is_consonant)) if is_consonant[i] is False]

    def display(self, index):
        format_string = result_strings[index]
        if not self.success:
            for note in self.incorrect_notes:
                self.analysis.results.append(format_string.format(note))


class MelodicUnisonsRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Tests that there are not too many melodic unisons")
        self.success = True
        self.incorrect_notes = []

    def apply(self):
        max_unisons = s1_settings['MAX_UNI'] if self.analysis.species == 1 else s2_settings['MAX_UNI']
        is_unison = [i.lines_and_spaces() == 1 for i in self.analysis.cp_intervals_melody]
        self.success = is_unison.count(True) <= max_unisons
        if not self.success:
            self.incorrect_notes = [i + 1 for i in range(len(is_unison)) if is_unison[i] is True][max_unisons:]

    def display(self, index):
        format_string = result_strings[index]
        if not self.success:
            for note in self.incorrect_notes:
                self.analysis.results.append(format_string.format(note))


class MelodicFourthsRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Tests that there are not too many melodic fourths")
        self.success = True
        self.incorrect_notes = []
        self.max_fourths = self.analysis.settings['MAX_4TH']

    def apply(self):
        is_fourth = [i.lines_and_spaces() == 4 for i in self.analysis.cp_intervals_melody]
        self.success = is_fourth.count(True) <= self.max_fourths

    def display(self, index):
        format_string = result_strings[index]
        if not self.success:
            max_leaps = s1_settings['MAX_LRG'] if self.analysis.species == 1 else s2_settings['MAX_LRG']
            leaps = [(self.analysis.cp_intervals_melody[i].lines_and_spaces(), i)
                     for i in range(len(self.analysis.cp_intervals_melody))
                     if self.analysis.cp_intervals_melody[i].lines_and_spaces() > 3]
            num_fourths = 0
            for i in range(len(leaps)):
                err_msg = format_string if i + 1 < max_leaps else result_strings[26]
                if leaps[i][INTERVAL_INDEX] == 4:
                    num_fourths += 1
                    if num_fourths > self.max_fourths:
                        self.analysis.results.append(err_msg.format(leaps[i][NOTE_INDEX] + 1))


class MelodicFifthsRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Tests that there are not too many melodic fifths")
        self.success = True
        self.incorrect_notes = []
        self.max_fifths = self.analysis.settings['MAX_5TH']

    def apply(self):
        is_fifth = [i.lines_and_spaces() == 5 for i in self.analysis.cp_intervals_melody]
        self.success = is_fifth.count(True) <= self.max_fifths

    def display(self, index):
        format_string = result_strings[index]
        if not self.success:
            max_leaps = s1_settings['MAX_LRG'] if self.analysis.species == 1 else s2_settings['MAX_LRG']
            leaps = [(self.analysis.cp_intervals_melody[i].lines_and_spaces(), i)
                     for i in range(len(self.analysis.cp_intervals_melody))
                     if self.analysis.cp_intervals_melody[i].lines_and_spaces() > 3]
            num_fifths = 0
            for i in range(len(leaps)):
                err_msg = format_string if i + 1 <= max_leaps else result_strings[26]
                if leaps[i][INTERVAL_INDEX] == 5:
                    num_fifths += 1
                    if num_fifths > self.max_fifths:
                        self.analysis.results.append(err_msg.format(leaps[i][NOTE_INDEX] + 1))


class MelodicSixthRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Tests that there are not too many melodic sixths")
        self.success = True
        self.incorrect_notes = []
        self.max_sixths = self.analysis.settings['MAX_6TH']

    def apply(self):
        is_sixth = [i.lines_and_spaces() == 6 for i in self.analysis.cp_intervals_melody]
        self.success = is_sixth.count(True) <= self.max_sixths

    def display(self, index):
        format_string = result_strings[index]
        if not self.success:
            max_leaps = s1_settings['MAX_LRG'] if self.analysis.species == 1 else s2_settings['MAX_LRG']
            leaps = [(self.analysis.cp_intervals_melody[i].lines_and_spaces(), i)
                     for i in range(len(self.analysis.cp_intervals_melody))
                     if self.analysis.cp_intervals_melody[i].lines_and_spaces() > 3]
            num_sixths = 0
            for i in range(len(leaps)):
                err_msg = format_string if i + 1 < max_leaps else result_strings[26]
                if leaps[i][INTERVAL_INDEX] == 6:
                    num_sixths += 1
                    if num_sixths > self.max_sixths:
                        self.analysis.results.append(err_msg.format(leaps[i][NOTE_INDEX] + 1))


class MelodicSeventhRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Tests that there are not too many melodic sevenths")
        self.success = True
        self.incorrect_notes = []
        self.max_sevenths = self.analysis.settings['MAX_7TH']

    def apply(self):
        is_seventh = [i.lines_and_spaces() == 7 for i in self.analysis.cp_intervals_melody]
        self.success = is_seventh.count(True) <= self.max_sevenths

    def display(self, index):
        format_string = result_strings[index]
        if not self.success:
            max_leaps = s1_settings['MAX_LRG'] if self.analysis.species == 1 else s2_settings['MAX_LRG']
            leaps = [(self.analysis.cp_intervals_melody[i].lines_and_spaces(), i)
                     for i in range(len(self.analysis.cp_intervals_melody))
                     if self.analysis.cp_intervals_melody[i].lines_and_spaces() > 3]
            num_sevenths = 0
            for i in range(len(leaps)):
                err_msg = format_string if i + 1 < max_leaps else result_strings[26]
                if leaps[i][INTERVAL_INDEX] == 7:
                    num_sevenths += 1
                    if num_sevenths > self.max_fifths:
                        self.analysis.results.append(err_msg.format(leaps[i][NOTE_INDEX] + 1))


class MelodicOctaveRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Tests that there are not too many melodic octaves")
        self.success = True
        self.incorrect_notes = []
        self.max_octs = self.analysis.settings['MAX_8VA']

    def apply(self):
        is_oct = [i.lines_and_spaces() == 8 for i in self.analysis.cp_intervals_melody]
        self.success = is_oct.count(True) <= self.max_octs

    def display(self, index):
        format_string = result_strings[index]
        if not self.success:
            max_leaps = s1_settings['MAX_LRG'] if self.analysis.species == 1 else s2_settings['MAX_LRG']
            leaps = [(self.analysis.cp_intervals_melody[i].lines_and_spaces(), i)
                     for i in range(len(self.analysis.cp_intervals_melody))
                     if self.analysis.cp_intervals_melody[i].lines_and_spaces() > 3]
            num_octs = 0
            for i in range(len(leaps)):
                err_msg = format_string if i + 1 < max_leaps else result_strings[26]
                if leaps[i][INTERVAL_INDEX] == 8:
                    num_octs += 1
                    if num_octs > self.max_fifths:
                        self.analysis.results.append(err_msg.format(leaps[i][NOTE_INDEX] + 1))


class LargeLeapsRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Tests that there are not too many leaps larger than a third")
        self.success = True
        self.incorrect_notes = []

    def apply(self):
        max_leaps = s1_settings['MAX_LRG'] if self.analysis.species == 1 else s2_settings['MAX_LRG']
        is_leap = [i.lines_and_spaces() > 3 for i in self.analysis.cp_intervals_melody]
        self.success = is_leap.count(True) <= max_leaps
        if not self.success:
            self.incorrect_notes = [i + 1 for i in range(len(is_leap)) if is_leap[i] is True][max_leaps:]

    def display(self, index):
        format_string = result_strings[index]
        if not self.success:
            for note in self.incorrect_notes:
                self.analysis.results.append(format_string.format(note))


class LeapConsecutiveRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Tests that there are not too many consecutive leaps greater than third")
        self.success = True
        self.incorrect_notes = []

    def apply(self):
        max_consec_leaps = s1_settings['MAX_CONSEC_LEAP'] \
            if self.analysis.species == 1 else s2_settings['MAX_CONSEC_LEAP']
        consecutive_leaps = []
        counter = 0
        for i in range(len(self.analysis.cp_spans_melody)):
            if abs(self.analysis.cp_spans_melody[i]) <= 2:
                counter = 0
            else:
                counter += 1
                if counter > max_consec_leaps:
                    consecutive_leaps.append(i + 1)
        self.success = len(consecutive_leaps) == 0
        if not self.success:
            self.incorrect_notes = consecutive_leaps

    def display(self, index):
        format_string = result_strings[index]
        if not self.success:
            for note in self.incorrect_notes:
                self.analysis.results.append(format_string.format(note))


class IntervalsSameDirectionRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Tests that there are not too many intervals going same direction")
        self.success = True
        self.incorrect_notes = []

    def apply(self):
        max_samedir = s1_settings['MAX_SAMEDIR'] if self.analysis.species == 1 else s2_settings['MAX_SAMEDIR']
        consecutive_intervals = []
        current_sign = 0
        counter = 0
        for i in range(len(self.analysis.cp_intervals_melody)):
            if current_sign == 0 or self.analysis.cp_intervals_melody[i].sign != current_sign:
                counter = 1
                current_sign = self.analysis.cp_intervals_melody[i].sign
            elif self.analysis.cp_intervals_melody[i].sign == current_sign:
                counter += 1
                if counter > max_samedir:
                    consecutive_intervals.append(i + 1)
        self.success = len(consecutive_intervals) == 0
        if not self.success:
            self.incorrect_notes = consecutive_intervals

    def display(self, index):
        format_string = result_strings[index]
        if not self.success:
            for note in self.incorrect_notes:
                self.analysis.results.append(format_string.format(note))


class ReverseByStepRecoveryRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Tests that leaps are appropriately recovered by reverse steps")
        self.success = True
        self.incorrect_notes = []

    def apply(self):
        step_threshold = s1_settings['STEP_THRESHOLD'] if self.analysis.species == 1 else s2_settings['STEP_THRESHOLD']
        failed_leaps = []
        leap = 0  # temporary variable
        for i in range(1, len(self.analysis.cp_spans_melody)):
            if leap == 0:  # only not 0 if there are two consecutive, same direction thirds
                leap = self.analysis.cp_spans_melody[i]
            if abs(leap) <= 2:  # stepwise, not a leap: ignore and move on
                leap = 0
            else:  # interval is a leap, inspect for leap recovery
                if abs(leap) == 4:
                    if i != len(self.analysis.cp_spans_melody) - 1:
                        if (self.analysis.cp_spans_melody[i + 1] > 0 and leap > 0) \
                                or (self.analysis.cp_spans_melody[i + 1] < 0 and leap < 0):
                            self.success = False
                            failed_leaps.append(i + 1)  # adding 2 because we want the ending note of the interval
                    else:
                        self.success = False
                        failed_leaps.append(i + 1)
                    leap = 0
                elif abs(leap) >= step_threshold:
                    if i != len(self.analysis.cp_spans_melody) - 1:
                        # if both spans go the same dir OR if the next span is not a second, fails
                        if ((self.analysis.cp_spans_melody[i + 1] > 0 and leap > 0)
                            or (self.analysis.cp_spans_melody[i + 1] < 0 and leap < 0)) \
                                or abs(self.analysis.cp_spans_melody[i + 1]) != 2:
                            self.success = False
                            failed_leaps.append(i + 1)
                    else:
                        self.success = False
                        failed_leaps.append(i + 1)
                    leap = 0
        if not self.success:
            self.incorrect_notes = failed_leaps

    def display(self, index):
        format_string = result_strings[index]
        if not self.success:
            for note in self.incorrect_notes:
                override_strings_formats = [result_strings[1], result_strings[14], result_strings[19]]
                override_strings = [s.format(note) for s in override_strings_formats]
                override = True in [self.analysis.results.count(s) > 0 for s in override_strings]
                if not override:
                    self.analysis.results.append(format_string.format(note))


class ForbiddenCompoundIntervalRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Tests that there are no compound melodic intervals")
        self.success = True
        self.incorrect_notes = []

    def apply(self):
        is_simple = [i.is_simple() for i in self.analysis.cp_intervals_melody]
        self.success = not (False in is_simple)
        if not self.success:
            self.incorrect_notes = [i + 1 for i in range(len(is_simple)) if is_simple[i] is False]

    def display(self, index):
        format_string = result_strings[index]
        if not self.success:
            for note in self.incorrect_notes:
                self.analysis.results.append(format_string.format(note))


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
sample = '1-001-B_zawang2.musicxml'
s = import_score(root_dir + sample)
a = SpeciesAnalysis(s, int(sample[0]))
a.submit_to_grading()

"""
