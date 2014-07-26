"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    result = []
    
    # Empty list case
    if len(list1) == 0:
        return []
    # List with a single item case
    elif len(list1) == 1:
        return [list1[len(list1) - 1]]
    # Larger lists case
    else:
        for item in list1:
            if item not in result:
                result.append(item)
        return result 

    
def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    result = []
    
    # Create copies for not mutating the input lists
    first_list = list(list1)
    second_list = list(list2)
    
    # Compare first element in the lists, popping 
    # results if there's a match and reducing the 
    # list length
    while len(first_list) > 0 and len(second_list) > 0:
        if first_list[0] <= second_list[0]:
            if first_list[0] == second_list[0]:
                result.append(first_list.pop(0))
                second_list.pop(0)
            else:
                first_list.pop(0)
        else: 
            if first_list[0] == second_list[0]:
                result.append(second_list.pop(0))
                first_list.pop(0)
            else:
                second_list.pop(0)
    
    return result


# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in both list1 and list2.

    This function can be iterative.
    """   
    result = []  
    
    # Create copies for not mutating the input lists
    first_list = list(list1)
    second_list = list(list2)
    
    # Compare and pop the minimum element of the corresponding list
    while len(first_list) > 0 and len(second_list) > 0:   
        if first_list[0] < second_list[0]:
            result.append(first_list.pop(0))
        else:
            result.append(second_list.pop(0))
    
    # Add the remaining items in the list
    if len(second_list) == 0:
        result.extend(first_list)
    elif len(first_list) == 0:
        result.extend(second_list)
        
    return result
                
    
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    
    # Create a copy for not mutating the input list
    a_list = list(list1)
    
    if len(a_list) <= 1:
        # Base case
        return a_list
    else:
        # Recursive case
        mid = len(a_list) / 2
        
        first_half = a_list[:mid]
        second_half = a_list[mid:]
        
        return merge(merge_sort(first_half), merge_sort(second_half))

    
# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    
    # Base cases
    if len(word) == 0:
        return [""]
    if len(word) == 1:
        return ["", word]
    else:
        # Recursive Case
        # Split the word into 2 parts
        first = word[0]
        rest = word[1:]
        
        # Generate strings for rest
        rest_strings = gen_all_strings(rest)
        
        # Insert the first character in every position on each string in rest_strings
        concat_strings = []
        for string in rest_strings:
            for idx in range(len(string) + 1):
                concat_strings.append(string[:idx] + first + string[idx:])
            
        # Return a list containing the strings in rest_strings as well as the new strings
        # generated in the loop
        return rest_strings + concat_strings

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    
    # Open the file in the specified URL
    url = codeskulptor.file2url(filename)
    netfile = urllib2.urlopen(url)
    
    # Read all the words in that file
    words = netfile.read()
    
    # Return the words in a list of words
    return words.split("\n")


def run():
    """
    Run game.
    """
    
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

    
# Uncomment when you are ready to try the game
run()

#import user36_YLM2lAYOPYukMqi as unit_test
#unit_test.test_remove_duplicates(remove_duplicates)
#unit_test.test_intersect(intersect)
#unit_test.test_merge(merge)
#unit_test.test_merge_sort(merge_sort)
#unit_test.test_gen_all_strings(gen_all_strings)