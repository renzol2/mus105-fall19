###############################################################################

from .voice import Voice


## A class representing a measure of music.
class Bar:
    ## Initializes a Bar and its seven attributes self.id, self.clef,
    # self.key, self.meter, self.voices, self.barline, and self.partial.
    # @param bid  A unique integer identifier for the bar's id attribute.
    # @param clef A Clef for the bar's clef attribute. Defaults to None.
    # @param key A Key for the bar's measure attribute.  Defaults to None.
    # @param meter A Meter for the bar's meter attribute. Defaults to None.
    # @param barline A Barline for the bar's barline attribute.
    # Defaults to None.
    # @param partial A boolean value for the bar's partial attribute. If true
    # the bar is an incomplete (e.g. pickup) measure. Defaults to False.
    #
    # Initialize self.voices to an empty list and self.staff to None.
    # See also: Staff, Voice, https://en.wikipedia.org/wiki/Bar_(music)
    def __init__(self, bid, clef=None, key=None, meter=None, barline=None, partial=False):
        pass

    ## Returns a string showing the bars unique id and all attributes
    # except self.voices if that attribute is not None. The order of
    # printing is id, clef, key, meter, barline, followed by the
    # hex id of the instance.
    # Example: '<Bar: 0 Treble A-Major 2/4 STANDARD 0x109667790>'
    def __str__(self):
        return ''

    ## Define __repr__ to be the same as __str__ except there is
    # no hex id included.
    # Example: '<Bar: 0 Treble A-Major 2/4 STANDARD>'
    def __repr__(self):
        return ''

    ## Implements Bar iteration by returning an iterator for the bar's
    # voices. See: Python's iter() function.
    def __iter__(self):
        pass

    ## Appends a Voice to the bars's voice list and assigns
    # itself to the voice's bar attribute.
    # @param voice The Voice to append to the bar's voice list.
    # The method should raise a TypeError if voice is not a Voice instance.
    def add_voice(self, voice):
        pass

    ## Returns the bar's voice identifiers in the same order
    # that they occur in the voices list.
    def voice_ids(self):
        pass

    ## Returns the number of voices in the bar.
    def num_voices(self):
        pass

