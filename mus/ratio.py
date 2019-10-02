
###############################################################################
## @file
#  A class that implements fractional numbers.
#  The Ratio class provides exact arithmetic for representing exact musical
#  quantities such as proportional (metric) time, duration, and 'just' tuning
#  intervals. Ratios can be created from two integers or from a string.
#  Ratios are compared and combined using the standard math operators.

import math
from decimal import Decimal


class Ratio:
    num = 0
    den = 1

    # Creates a Ratio from integers, a floating point number, or a string name.
    #  * Ratio(int, int) - creates a ratio from an integer numerator and denominator.
    #  * Ratio(int) - creates a ratio from an integer numerator with the denominator
    #  set to 1.
    #  * Ratio(float) - creates a ratio from a floating point number
    #  (see: as_integer_ratio())
    #  * Ratio(string) -  creates a ratio from a string 'num/den'. Both num and
    #  den must produce valid integers.
    #
    #  @param num If only num is specified it must be either an integer, float,
    #  or a string containing a valid ratio expression 'a/b'. If both num and
    #  den are provided they must both be integer value.
    #  @param den If specified den must be a non-zero integer denominator
    #
    #  Upon construction the new ratio will always be expressed in its most simple
    #  form, for example Ratio(6,12) will become Ratio(1/2), See: gcd().
    #  If both the numerator and denominator are negative the ratio should be
    #  converted to positive by the constructor.
    #
    #  The constructor should raise a TypeError if the num or den is not a integer,
    #  string or float and a DivisionByZero error if the denominator is 0.
    def __init__(self, num, den=None):
        if den is None:
            if type(num) == int:
                self.num = num
            elif type(num) == float:
                nums = Decimal(f"{num}").as_integer_ratio()
                self.num = nums[0]
                self.den = nums[1]
            elif type(num) == str:
                # check if a backslash is used and that at least two values are used
                if num.find("/") != -1 and len(num) > 2:
                    vals = num.split("/")  # separate num and den
                    # check if only one backslash is used
                    if len(vals) == 2:
                        # check if both num and den are numbers
                        # !!!!!! NEED TO HANDLE NEGATIVE VALUES IN STRING
                        negatives = [1, 1]
                        for i in range(len(vals)):
                            if vals[i].find("-") != -1:
                                negatives[i] *= -1
                                vals[i] = vals[i].replace("-", "")
                        if vals[0].isnumeric() is True and vals[1].isnumeric() is True:
                            if negatives[0] == negatives[1] == -1:
                                negatives[0] = negatives[1] = 1
                            elif negatives[0] == 1 and negatives[1] == -1:
                                negatives[0] *= -1
                                negatives[1] *= -1
                            num_val = int(vals[0]) * negatives[0]
                            den_val = int(vals[1]) * negatives[1]
                            self.num = num_val // math.gcd(num_val, den_val)
                            self.den = den_val // math.gcd(num_val, den_val)
                        else:
                            raise ValueError(f"{num} is not a valid parameter"
                                             "\nWhen instantiating a Ratio with a string, "
                                             "only use integer values for the numerator "
                                             "and denominator.")
                    else:
                        raise ValueError(f"{num} is not a valid parameter."
                                         "\nWhen instantiating a Ratio with a string, "
                                         "only use one backslash '/'.")
                else:
                    raise ValueError(f"{num} is not a valid parameter."
                                     "\nWhen instantiating a Ratio with a string, "
                                     "it must follow the format 'a/b', where a and b "
                                     "are integers.")
            else:
                raise TypeError(f"{num} is not a valid parameter."
                                "\nWhen instantiating a Ratio with just a numerator, "
                                "valid types only include integers, floating point "
                                "numbers, and strings.")
        else:
            if type(num) == type(den) == int:
                if den == 0:
                    raise ZeroDivisionError("The denominator cannot be 0.")
                if (num < 0 and den < 0) or (num > 0 and den < 0):
                    num *= -1
                    den *= -1
                self.num = num // math.gcd(num, den)
                self.den = den // math.gcd(num, den)
            else:
                raise TypeError(f"{num} and {den} are not valid parameters."
                                "\nWhen instantiating a Ratio with a numerator and "
                                "denominator, both parameters must be integers.")

    # Returns a string showing the ratio's fraction and the hex
    #  hex value of the ratio's memory address.
    #  Example: <Ratio: 1/4 0x10610d2b0>
    def __str__(self):
        # should be done
        return "<Ratio: " + str(self.num) + "/" + str(self.den) + " " + str(hex(id(self))) + ">"

    # Returns a string expression that will evaluate to this ratio.
    def __repr__(self):
        # should be done
        return "Ratio(" + str(self.num) + "/" + str(self.den) + ")"

    # Implements Ratio*Ratio, Ratio*int and Ratio*float.
    # @param other An Ratio, int or float.
    # @returns A Ratio if other is a Ratio or an int, otherwise a float.
    #
    # A TypeError should be raised if other is not a Ratio, int or float.
    def __mul__(self, other):
        # should be done
        if type(other) == Ratio:
            return Ratio(self.num * other.num, self.den * other.den)
        elif type(other) == int:
            return Ratio(self.num * other, self.den)
        elif type(other) == float:
            return (self.num / self.den) * other
        else:
            raise TypeError("Ratios can only be multiplied by other Ratios, integers, or floats.")

    # Implements right side multiplication by calling __mul__
    __rmul__ = __mul__
    # should be done

    # Implements Ratio/Ratio, Ratio/int and Ratio/float.
    # @param other A Ratio, int or float.
    # @returns A Ratio if other is a Ratio or an int, otherwise a float.
    #
    # A TypeError should be raised if other is not a Ratio, int or float.
    def __truediv__(self, other):
        # should be done
        if type(other) == Ratio:
            return self * other.reciprocal()
        elif type(other) == int:
            return Ratio(self.num, self.den * other)
        elif type(other) == float:
            return (self.num / self.den) / other
        else:
            raise TypeError("Ratios on the left can only be divided by other Ratios, integers, or floats.")

    # Implements int / Ratio or float / Ratio (right side division).
    #  @returns A new Ratio.
    def __rtruediv__(self, other):
        # should be done
        if type(other) == int:
            return Ratio(other * self.den, self.num)
        elif type(other) == float:
            return other / (self.num / self.den)
        else:
            raise TypeError("Ratios on the right can only be divided integers or floats.")

    # Implements 1 / ratio (reciprocal).
    #  @returns A new Ratio.
    def __invert__(self):
        # should be done
        return Ratio(self.den, self.num)

    # Implements Ratio + Ratio, Ratio + int and Ratio + float. In order to
    #  add two ratios their denominators must be converted to the
    #  least common multiple of the current denominator. See: lcm().
    #  @returns A new Ratio.
    def __add__(self, other):
        if type(other) == Ratio:
            return Ratio(self.num * Ratio.lcm(self.den, other.den) // self.den +
                         other.num * Ratio.lcm(self.den, other.den) // other.den,
                         Ratio.lcm(self.den, other.den))
        elif type(other) == int:
            return Ratio(self.num, self.den) + Ratio(other)
        elif type(other) == float:
            return Ratio((self.num / self.den) + other)
        else:
            raise TypeError("Ratios can only be added on or subtracted by other Ratios, integers, or floats.")

    # Implements right side addition by calling __add__.
    #  @returns A new Ratio.
    __radd__ = __add__

    # Implements -ratio (negation).
    #  @returns A new Ratio.
    def __neg__(self):
        return Ratio(-self.num, self.den)

    # Implements ratio - ratio, ratio - int and ratio - float.
    #  @returns A new Ratio.
    def __sub__(self, other):
        # i think this is done? not sure
        return self.__add__(other.__neg__())

    # Implements int - ratio and float-ratio (right side subtraction).
    #  @returns A new Ratio.
    def __rsub__(self, other):
        # i think this is done? not sure
        if type(other) == int or type(other) == float:
            return other + -self
        else:
            raise ValueError("Ratios on the right can only subtract from integers or floats.")

    # Implements ratio % ratio.
    #  @returns A new Ratio.
    def __mod__(self, other):
        if other.num == 0:
            raise ZeroDivisionError("Cannot divide/modulo by 0")
        if type(other) == Ratio:
            return Ratio((self * 1.0) % (other * 1.0))
        else:
            raise TypeError("Modulus operations with Ratios can only be performed in Ratio % Ratio format")

    # Implements Ratio**int, Ratio**float, and Ratio**Ratio.
    #  @returns If the exponent is a positive or negative int
    #  a Ratio should be returned. Otherwise for Ratio or float
    #  exponents a float should be returned. See: math.pow().
    def __pow__(self, other):
        if type(other) == int:
            return Ratio((self * 1.0) ** other)
        elif type(other) == Ratio:
            return math.pow(self * 1.0, other * 1.0)
        elif type(other) == float:
            return math.pow(self * 1.0, other)
        else:
            raise TypeError("Ratios can only be raised to powers of integers, floats, or other Ratios")

    # Implements an int**ratio or float**ratio
    #  @param other  The base integer or float.
    #  @returns A floating point number.
    #
    #  The function can be implemented using math.pow().
    def __rpow__(self, other):
        if type(other) == int:
            return math.pow(other, self * 1.0)
        elif type(other) == float:
            return math.pow(other, self * 1.0)
        else:
            raise TypeError("Only integers and floats can be raised to Ratio powers")

    # Implements Ratio < Ratio, Ratio < int, Ratio < float. See: compare().
    def __lt__(self, other):
        if type(other) == Ratio:
            compare_value = Ratio.compare(self, other)
        else:
            compare_value = Ratio.compare(self, Ratio(other))
        if compare_value < 0:
            return True
        else:
            return False

    # Implements Ratio <= Ratio, Ratio <= int, Ratio <= float. See: compare().
    def __le__(self, other):
        if type(other) == Ratio:
            compare_value = Ratio.compare(self, other)
        else:
            compare_value = Ratio.compare(self, Ratio(other))
        if compare_value <= 0:
            return True
        else:
            return False

    # Implements Ratio <= Ratio, Ratio <= int, Ratio <= float. See: compare().
    def __eq__(self, other):
        if type(other) == Ratio:
            compare_value = Ratio.compare(self, other)
        else:
            compare_value = Ratio.compare(self, Ratio(other))
        if compare_value == 0:
            return True
        else:
            return False

    # Implements Ratio != Ratio, Ratio != int, Ratio != float. See: compare().
    def __ne__(self, other):
        if type(other) == Ratio:
            compare_value = Ratio.compare(self, other)
        else:
            compare_value = Ratio.compare(self, Ratio(other))
        if compare_value != 0:
            return True
        else:
            return False

    # Implements Ratio >= Ratio, Ratio >= int, Ratio >= float. See: compare().
    def __ge__(self, other):
        if type(other) == Ratio:
            compare_value = Ratio.compare(self, other)
        else:
            compare_value = Ratio.compare(self, Ratio(other))
        if compare_value >= 0:
            return True
        else:
            return False

    # Implements Ratio>Ratio, Ratio > int, Ratio > float. See: compare().
    def __gt__(self, other):
        if type(other) == Ratio:
            compare_value = Ratio.compare(self, other)
        else:
            compare_value = Ratio.compare(self, Ratio(other))
        if compare_value > 0:
            return True
        else:
            return False

    # Returns a single integer hash value for the ratio: (num<<16 + den)
    def __hash__(self):
        # i didn't do this right lol
        return hex(id(self))

    # Helper method implements ratio comparison. Returns 0 if the ratios are equal,
    # a negative value if self is less than other and a positive value if self is
    # GEQ other. Given two ratios the comparison is (num1*den2) - (num2*den1)
    def compare(self, other):
        return self.num * other.den - other.num * self.den

    # A static method that returns the lowest common multiple of two integers
    # a and b. lcm be calculated using gcd(): (a*b) // gcd(a,b)
    @staticmethod
    def lcm(a, b):
        return (a * b) // math.gcd(a, b)

    # Returns the string name of the ratio 'num/den'.
    def string(self):
        return str(self.num) + "/" + str(self.den)

    # Returns 1/ratio.
    def reciprocal(self):
        return Ratio(self.den, self.num)

    # Returns the musical 'dotted' value of the ratio, e.g. 1/4 with
    #  one dot is 1/4 + 1/8 = 3/8.
    #  @param dots  The number of dots to apply, each dot adds half the
    #  previous value of the ratio.
    #  @return A new ratio representing the dotted value.

    # The method should raise a ValueError if dots is not a positive integer.
    def dotted(self, dots=1):
        if dots < 1 or type(dots) != int:
            raise TypeError("The number of dots must be a positive integer")
        ratio = self
        for i in range(dots):
            ratio += Ratio(self.num, self.den * 2 ** (i + 1))
        return ratio

    # Returns a list of num sub-divisions (metric 'tuples') that sum to
    #  value of ratio*num.
    #  @param num  The number of tuples to return.
    #  @param intimeof  A number that, when multiplied by the fraction
    #  itself, represents the sum of all the tuplets returned.
    #  @returns A list of num ratios that sum to the value of the Ratio.
    #
    #  Examples: Ratio(1,4).tuplets(3) returns three tuplets [1/12, 1/12, 1/12]
    #  which sum to Ratio(1,4).  Ratio(1,4).tuplets(3,2) returns three
    #  tuplets [1/6, 1/6, 1/6] which sum to ratio*2, or 1/2.
    def tuplets(self, num, intimeof=1):
        if type(num) == int and type(intimeof) == int:
            list_tuplets = []
            for i in range(num):
                list_tuplets.append(self * intimeof / num)
            return list_tuplets
        else:
            raise TypeError("Number of tuples must be an integer")


    # Returns the ratio representing num divisions of this ratio.
    #  @param num  The number to divide this ratio by.
    #  @return The new tuple value ratio.
    #
    #  Example:  Ratio(1,4).tup(5) is 1/20
    def tup(self, num):
        if type(num) == int or type(num) == float:
            return Ratio(self.num, self.den * num)

    # Returns the ratio as a floating point number.
    def float(self):
        return float(self.num / self.den)

    # Converts the ratio to floating point seconds according to a
    #  given tempo and beat:
    #  @param tempo  The tempo in beats per minute. Defaults to 60.
    #  @param beat  A ratio representing the beat. Defaults to 1/4 (quarter note).
    def seconds(self, tempo=60, beat=None):
        if (type(tempo) == float or type(tempo) == int) and (type(beat) == Ratio or beat is None):
            if beat is None:
                beat = Ratio(1/4)
            total_beats_passed = self / beat
            total_seconds_passed = (total_beats_passed * 60 / tempo) * 1.0
            return total_seconds_passed
        else:
            raise TypeError("The tempo must be in BPM (integer or floats). The beat must be a Ratio")


if __name__ == '__main__':
    print(Ratio("15/-25"))
