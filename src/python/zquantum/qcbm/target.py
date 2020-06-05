import itertools
import numpy as np
import math
import random
from typing import List

from zquantum.core.bitstring_distribution import BitstringDistribution

def get_bars_and_stripes_target_distribution(nrows, ncols, percentage=1., method="zigzag"):
    ''' Generates bars and stripes data in zigzag pattern
    Args: 
        nrows (int): number of rows in BAS dataset 
        ncols (int): number of columns in BAS dataset 
        percentage (float): maximum percentage of patterns to include (at least one pattern will always be included)
        method (string): the method to use to label the qubits
    Returns: 
        Array of list of BAS pattern. 
    '''
    if method == "zigzag":
        data = bars_and_stripes_zigzag(nrows, ncols)
    else:
        raise RuntimeError("Method: {} is not supported for generated a target distribution for bars and stripes".format(method))

    # Remove patterns until left with a subset that has cardinality less than or equal to the percentage * total number of patterns
    num_desired_patterns = int(len(data) * percentage)
    num_desired_patterns = max(num_desired_patterns, 1)
    data = random.sample(list(data), num_desired_patterns)

    distribution_dict = {}
    for pattern in data: 
        bitstring = ""
        for qubit in pattern:
            bitstring += str(qubit)

        distribution_dict[bitstring] = 1.

    return BitstringDistribution(distribution_dict)


# Generate BAS with specified rows and columns in zigzag pattern (taken from Vicente's code, would be careful about ownership of code)
def bars_and_stripes_zigzag(nrows, ncols, percentage=1.):
    ''' Generates bars and stripes data in zigzag pattern
    Args: 
        nrows (int): number of rows in BAS dataset 
        ncols (int): number of columns in BAS dataset 
        percentage (float): maximum percentage of patterns to include
    Returns: 
        Array of list of BAS pattern. 
    '''

    data = [] 
    
    for h in itertools.product([0,1], repeat=ncols):
        pic = np.repeat([h], nrows, 0)
        data.append(pic.ravel().tolist())
          
    for h in itertools.product([0,1], repeat=nrows):
        pic = np.repeat([h], ncols, 1)
        data.append(pic.ravel().tolist())
    
    data = np.unique(np.asarray(data), axis=0)

    return data


def get_num_bars_and_stripes_patterns(nrows, ncols) -> int:
    ''' Get the number of bars and stripes patters for a 2-dimensional grid.
    Args:
        nrows (int): number of rows in BAS dataset 
        ncols (int): number of columns in BAS dataset 
    Returns: 
        (int): number of bars and stripes patterns
    '''
    # Always have all blank and all filled
    num_patterns = 2

    for dimension in [nrows, ncols]: 
        for num_choices in range(1, dimension):
            # nCr = n! / (n-r)! * r!
            num_patterns += math.factorial(dimension) // (math.factorial(dimension-num_choices) * math.factorial(num_choices))

    return num_patterns


def get_subset_of_patterns(data, percentage):
    ''' Given a list of patterns, continually remove patterns until the remaining subset has cardinality which is 
        less than or equal to the percentage.

    Args:
        data (2-d list of integers): the patterns
        percentage (float): maximum percentage of patterns to include
    '''




# #Generate BAS with specified rows and columns in snake pattern 
# def bars_and_stripes_snake(rows, cols): 
#     ''' Generates bars and stripes data in zigzag pattern
#     Args: 
#         rows (int): number of rows in BAS dataset 
#         cols (int): number of columns in BAS dataset 
#     Returns: 
#         Array of list of BAS pattern. 
#     '''
#     data = []

#     for h in itertools.product([0,1], repeat=rows):
#         pic = np.repeat([h], rows, 0)
#         data.append(pic.ravel().tolist())
          
#     for h in itertools.product([0,1], repeat=cols):
#         pic = np.repeat([h], cols, 1)
#         data.append(pic.ravel().tolist())
    
#     # data = np.unique(np.asarray(data), axis=0)
    
#     return data


# #Generate BAS with all patterns 
# def bars_and_stripes_full_dataset(rows, cols): 
#     ''' Generates bars and stripes data in zigzag pattern
#     Args: 
#         rows (int): number of rows in BAS dataset 
#         cols (int): number of columns in BAS dataset
#     Returns: 
#         Array of list of BAS pattern. 
#     '''
#     data = []

#     for h in itertools.product([0,1], repeat=cols):
#         pic = np.repeat([h], rows, 0)
#         data.append(pic.ravel().tolist())
          
#     for h in itertools.product([0,1], repeat=rows):
#         pic = np.repeat([h], cols, 1)
#         data.append(pic.ravel().tolist())

#     for h in itertools.product([0,1], repeat=rows):
#         pic = np.repeat([h], rows, 0)
#         data.append(pic.ravel().tolist())
          
#     for h in itertools.product([0,1], repeat=cols):
#         pic = np.repeat([h], cols, 1)
#         data.append(pic.ravel().tolist())

#     for h in itertools.product([0,1], repeat=None):
#         pic = np.repeat([h], rows, 0)
#         data.append(pic.ravel().tolist())
          
#     for h in itertools.product([0,1], repeat=None):
#         pic = np.repeat([h], cols, 1)
#         data.append(pic.ravel().tolist())

#     data = np.unique(np.asarray(data), axis=0)
    
#     return data


# #Generate BAS based on how many samples user defines based on given percentage  
# def bars_and_stripes_sampler(rows, cols, percentage): 
#     ''' Create a data sampler than takes only a percentage of patterns specified by user 
#     Args: 
#         rows (int): number of rows in BAS pattern
#         cols (int): number of cols in BAS pattern
#         percentage (int): number of patterns to be used 
#     Returns: 
#         Array of list of BAS pattern. 
#     '''
#     n = int(rows)
#     m = int(cols)

#     nbas = 2**n + 2**m - 2 

#     n_pattern = int(random.sample(nbas))