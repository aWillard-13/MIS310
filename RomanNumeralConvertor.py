# Andrew Willard
# MIS-310
# IA2 - problem 2

""" Integer to Roman Numeral Convertor """

print("\n -- Integer to Roman Numeral Convertor -- \n ")

#future, might turn it into a GUI... maybe.

"""
This code takes a user input Integer, and outputs the Roman Numeral equivalent. 

for verification that it works correctly, see the following site for charts:
https://www.math-salamanders.com/roman-numerals-list.html

Unicode Charts: 
https://www.unicode.org/charts/PDF/U0300.pdf
"""


# Function to convert an integer to a Roman numeral
def int_to_roman(number):
    """ Lists of integer values and corresponding Roman numeral symbols """

    # Overline function: adds Unicode combining overline to each character
    def overline(s):
        return ''.join(char + '\u0304' for char in s) # have also used '\u0305'

    int_value = [
        1000000, 900000, 500000, 400000,
        100000, 90000, 50000, 40000,
        10000, 9000, 5000, 4000,
        1000, 900, 500, 400,
        100, 90, 50, 40,
        10, 9, 5, 4,
        1
    ]
    roman_num_symbol = [
        overline('M'), overline('CM'), overline('D'), overline('CD'),
        overline('C'), overline('XC'), overline('L'), overline('XL'),
        overline('X'), overline('IX'), overline('V'), overline('IV'),
        'M', 'CM', 'D', 'CD',
        'C', 'XC', 'L', 'XL',
        'X', 'IX', 'V', 'IV',
        'I']

    # Result string to build Roman numeral
    roman_numeral = ""

    # Loop through each value-symbol pair
    for i in range(len(int_value)):
        while number >= int_value[i]: roman_numeral += roman_num_symbol[i]; number -= int_value[i]
    return roman_numeral

# Function that runs a loop asking the user to enter numbers
def when_in_rome():
    while True:
        try:
            # Ask for user input and convert it to an integer
            user_input = int(input("Enter a number(Integer) or 0 to quit: "))
            if user_input <= 0: print("Exiting. Goodbye!"); break
            strRomanNumeral = int_to_roman(user_input)
            print(strRomanNumeral)
        except ValueError: print("Please enter a valid integer.")


when_in_rome()


"""
# if we wanted to flip the converter from roman numerals to it's Integer counterpart, 
# we can add a case that lets the user select from what to what (or put it in a GUI) ... 
# add a function like below, that takes the char then does the maths...
#                                  BUT
# because over-lined in text is difficult... (main reason why I stopped here) and honestly,
# between that and the error validation of it seemed like too much work, so I scrapped that idea.

def roman_values(overline_d=False):
    multiplier = 1000 if overline_d else 1
    return {
        'M': 1000 * multiplier,
        'CM': 900 * multiplier,
        'D': 500 * multiplier,
        'CD': 400 * multiplier,
        'C': 100 * multiplier,
        'XC': 90 * multiplier,
        'L': 50 * multiplier,
        'XL': 40 * multiplier,
        'X': 10 * multiplier,
        'IX': 9 * multiplier,
        'V': 5 * multiplier,
        'IV': 4 * multiplier,
        'I': 1 * multiplier,
    }
"""
