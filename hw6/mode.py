###############################################################################

from enum import IntEnum


## An enumeration of all the 7-tone modes: MAJOR, MINOR, IONIAN, DORIAN,
# PHRYGIAN, LYDIAN, MIXOLYDIAN, AEOLIAN, and LOCRIAN. The value for each mode
# should be a number index 0-6 representing its diatonic scale degree C-B.
# For example, MAJOR will be 0 (C), MINOR is 5 (A) and Dorian is 1 (D).
# Define IONIAN and AEOLIAN as synonyms for MAJOR and MINOR by assigning
# them their corresponding enum value.
class Mode (IntEnum):
    # Create enums here...


    ## Returns only the first three characters of the mode's name.
    def short_name(self):
        pass

    ## Returns the integer degree number representing the starting
    # scale degree of the mode. Thus IONIAN and MAJOR are 0,
    # DORIAN is 1, LOCRIAN is 6 and so on.
    def tonic_degree(self):
        pass
