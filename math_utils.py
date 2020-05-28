import math
import itertools
import pickle
import numpy


def weight(array):
    '''Finds the weight of the given binary array'''
    result = 0
    for digit in array:
        if digit:
            result += 1
    return result


def norm(array):
    '''Converts given vector to a binary vector'''
    for i in range(len(array)):
        array[i] = array[i]%2
    return array


def is_in(element, A):
    '''Determines if element is in given set (numpy specific)'''
    for vec in A:
        if (element == vec).all():
            return True

    return False


def find_in_dict(element, dictoinary):
    '''Determines if element is in given dectionary (numpy specific)'''
    for key, vecs in dictoinary.items():
        for vec in vecs:
            if (element == vec).all():
                return key

    return -1


def xor_sum(vectors, k: int):
    '''Finds xor of vectors set'''
    result = numpy.zeros(k, dtype=int)
    for vector in vectors:
        for i in range(len(vector)):
            result[i] = result[i] ^ vector[i]

    return result

def binary_to_num(array):
    '''Converts binary vector to a number'''
    result = 0
    for digit in array:
        digit = digit%2
        result = (result << 1)|digit

    return result
