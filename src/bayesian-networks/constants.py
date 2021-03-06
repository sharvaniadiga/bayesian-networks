'''
Created on Apr 11, 2016

@author: sharvani
'''

INPUT_FILE_QUERY_END_BAYESNET_BEGIN = "******"
INPUT_FILE_END_OF_PROB_TABLE = "***"

PROBABILITY = 'P'
EXPECTED_UTILITY = 'EU'
MAX_EXPECTED_UTILITY = 'MEU'

BAYESNET_VARIABLES_REGEX = "[A-Z]([a-zA-Z])*"

CONDITIONAL_PROBABILITY_SYMBOL = "|"
NULL_STRING = ""
SPACE = " "

CONDITIONAL_PROBABILITY_VALUE_INDEX = 0
CONDITIONAL_PROBABILITY_FIRST_PARENT_VALUE_INDEX = 1
CONDITIONAL_PROBABILITY_SECOND_PARENT_VALUE_INDEX = 2
CONDITIONAL_PROBABILITY_THIRD_PARENT_VALUE_INDEX = 3

NO_PARENT = "no-parent"

OPEN_BRACKET = "("
CLOSE_BRACKET = ")"

QUERY_SEPERATOR = ", "

PLUS = "+"
MINUS = "-"
NUM_OF_VALUES_PER_VARIABLE = 2

OUTPUT_TXT = "output.txt"

DECISION = "decision"
UTILITY = "utility"

BEFORE = "before"
AFTER = "after"