#############################################################################################################
#
#  Homework 1 (Python Intro pt. 2)
#  MUS105 Fall 2019
#  Functions, Exceptions Object Oriented
#
#  DUE: Wednesday, September 18
#
#  Instructions:
#    * for each of the functions below, read the docstring and implement the function as described.
#    * feel free to to add helper functions, but DO NOT MODIFY the descriptions of the original functions.
#
#    * absolutely NO import statements should be added, they will result in an automatic 0 (the autograder
#    will break)
#
#    * Some functions specify that certain built in functions may not be used. BE WARY OF THIS.
#
#    * if for whatever reason, an implementation detail is unclear, feel free to email:
#      shijiel2@illinois.edu
#    for clarification.
#
#    * Have Fun!
#
#############################################################################################################

def is_palindrome(s):
    """
    given a string s, output whether or not s is a palindrome. A palindrome is defined as a string that is identical
    read forwards or backwards. for example:
        'racecar' is a palindrome.
        'race car' is NOT a palindrome
        'rac e car' is a palindrome
    *for out purposes, spaces matter

    :param s: string to test for a palindrome
    :type s: str
    :return: whether or not s is a palindrome
    :rtype: bool
    """
    new_list = []
    new_str = ""
    for i in range(0, len(s)):  # add all chars in s to new_list
        new_list.append(s[i])
    reverse_list = new_list[::-1]  # reverses the chars in new_list
    for c in range(0, len(s)):  # adds all chars in reverse_list to a new string
        new_str += reverse_list[c]
    if new_str == s:  # compares the original and reversed string
        return True
    else:
        return False


def is_in(a, b):
    """
    given a sequence of characters (string) b, output whether or not string a can be constructed with the letters of
    string b. For example:
        is_in('cab', 'aabbcc') should output true
        is_in('hello world', 'helo world') should output false

    1. put all of chars from A and B to separate lists
    2. iterate through all of A and B
    3. when there's a match, remove the matching item from both A and B and break immediately
    4. if A is empty, is_in returns true; else, returns false

    :param a: string to try and construct
    :type a: str
    :param b: string to clip characters from
    :type b: str
    :return: whether or not a can be constructed from b
    :rtype: bool
    """

    list_a = []  # creates lists for both a and b
    list_b = []
    for chars_a in a:
        list_a.append(chars_a)
    for chars_b in b:
        list_b.append(chars_b)

    length_list_a_before = len(list_a)  # setting up variables for the loop
    length_list_a_after = len(list_a) - 1

    while length_list_a_after != length_list_a_before:  # if no chars were similar the last time, stop checking
        length_list_a_before = len(list_a)
        for i in range(0, len(list_b)):  # iterates through every char in b and compares it to every char in a
            for j in range(0, len(list_a)):
                if list_a[j] == list_b[i]:  # if a similar char is found, removes the char from both lists
                    list_a.remove(list_a[j])
                    list_b.remove(list_b[i])
                    break  # immediately breaks checking
            break
        length_list_a_after = len(list_a)  # updates the length of list a

    if len(list_a) == 0:  # if a was in b, then all the chars in list_a should be gone
        return True
    else:
        return False


def is_set(l):
    """
    given a list of integers l, output whether or not l is a set. Recall that a set is a collection of UNIQUE items.
    the type of l will be list. When we say 'is l a set?' we mean in the mathematical sense, not the data type sense!

    :param l: list to check uniqueness on
    :type l: list
    :return: whether or not l is a set
    :rtype: bool
    """
    not_unique = False
    for i in range(0, len(l)):  # compares every item in list to every other item in list
        for j in range(0, len(l)):
            if i != j and l[i] == l[j]:  # if two items are not same index but are similar, list is not unique
                not_unique = True
                break
    if not_unique:
        return False
    else:
        return True


def str_to_int2(num_string):
    """
    recall str_to_int from hw0. Re-implement that function, but instead of returning -1 in the case of unrecognized
    bases, raise a ValueError, with the message "unrecognized base". If the base is recognized, but the actual 
    representation is wrong, for example:
        0b123
    (binary numbers should only have 0 and 1), then raise a ValueError with the message "incorrect formatting"

    the rest of the functionality should be identical to hw0

    :param num_string: string representing an integer
    :type num_string: str
    :return: an integer with the value denoted by the string
    :rtype: int
    """

    if num_string.isalnum():
        if num_string.isnumeric():
            answer = int(num_string, 10)
        elif len(num_string) < 2:
            raise ValueError("unrecognized base")
        elif num_string.find("0b") != -1 and num_string[2:len(num_string)].isnumeric():
            # second conditional checks if there are letters after the first two chars
            answer = int(num_string, 2)
        elif num_string.find("0o") != -1 and num_string[2:len(num_string)].isnumeric():
            answer = int(num_string, 8)
        elif num_string.find("0x") != -1 and num_string[2:len(num_string)].isalnum():
            answer = int(num_string, 16)
        else:
            raise ValueError("incorrect formatting")
    else:
        raise ValueError("incorrect formatting")
    return answer


def nth_element(n, my_list):
    """
    given a list my_list, return the nth element in the list. If the list does not have an nth element,
    i.e. it is too small, you should raise a TypeError with the message:

        "Cannot find nth element of inputs ({}, {})".format(n, my_list)

    the nth element of the list is defined to be list[n - 1], if list is sorted (i.e. the nth smallest item)

    *The naive implementation of this function is just fine, but if you're feeling adventurous, there is an O(n)
    implementation of this. Look into the 'quick select' algorithm!

    :param n: the 'nth' element in a list. For example the 3rd element would be sorted_list[2]
    :type n: int
    :param my_list: input list
    :type my_list: list
    :return: nth element in my_list
    :rtype: float
    """
    try:
        return my_list[n - 1]
    except IndexError:
        raise TypeError("Cannot find nth element of inputs ({}, {})".format(n, my_list))


class Course:
    """
    the Course class describes a college course. Each course should contain:
        - a course code as a string (i.e. MUS105)
        - a CRN as an integer (i.e. 43357)
        - a course description as a string (i.e. Computation and Music 1)
        - a roster of students as a list
    check the parameter list for exact names of each of these variables

    the Course class as a whole should have a string that describes what university the course
    is in. this class variable should be called university. It should be initialized to "UIUC"

    the Course class should have one static method declared: print_school(), which is defined in more detail below.

    the Course class should have a few instance methods:
        *add_student, which adds a student to a course by netID
        *remove_student, which does the opposite
        *get_description, which prints out some information about the course.

    below, the class skeleton has been written for you. It is up to you to fill out the static members, and all
    of the functions.
    """

    university = "UIUC"

    @staticmethod
    def print_school():
        """
        This function takes no parameters and returns nothing. The only thing it should do is print:
            "The University is: {Course.university}"
        """
        print("The University is: " + Course.university)

    def __init__(self, code, crn, description):
        """
        Initializer, your code should set instance variables with the same name as the parameters to their respective
        parameter. The first one is done for you.

        **It should also initialize one more instance variable, roster, to an empty list**

        :param code: course code
        :type code: str
        :param crn: course CRN
        :type crn: int
        :param description: course description
        :type description: str
        """

        self.code = code
        self.crn = crn
        self.description = description

    def add_student(self, student):
        """
        adds a student to the roster, by appending their netID to the end of the list

        :param student: netID of student to add
        :type student: str
        """
        pass

    def remove_student(self, student):
        """
        removes a student from the roster, by finding their index, and removing them from the roster list.
        if the function is called on a student who is not enrolled in a course (i.e. they cannot be found in the roster)
        raise a ValueError with the message: "student is not enrolled in course"

        :param student: netID of student to remove
        :type student: str
        """
        pass

    def get_description(self):
        """

        :return: a description of the course, as described above
        :rtype: str
        """


CS125 = Course("125", 1, "hi")
CS125.print_school()
