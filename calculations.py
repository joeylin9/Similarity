"""
Description:
    Computes the similarity between two texts using two different metrics:
    (1) shared words, and (2) term frequency-inverse document
    frequency (TF-IDF).
"""

import string
import math
import re

### DO NOT MODIFY THIS FUNCTION
def load_file(filename):
    """
    Args:
        filename: string, name of file to read
    Returns:
        string, contains file contents
    """
    # print("Loading file %s" % filename)
    inFile = open(filename, 'r')
    line = inFile.read().strip()
    for char in string.punctuation:
        line = line.replace(char, "")
    inFile.close()
    return line.lower()


### Problem 1: Prep Data ###
def prep_data(input_text):
    """
    Args:
        input_text: string representation of text from file,
                    assume the string is made of lowercase characters
    Returns:
        list representation of input_text, where each word is a different element in the list
    """
    list_text = input_text.split() #splits the string of words into a list, seperating based on the spaces between the words
    return list_text

    pass


### Problem 2: Get Frequency ###
def get_frequencies(word_list):
    """
    Args:
        word_list: list of strings, all are made of lowercase characters
    Returns:
        dictionary that maps string:int where each string
        is a word in l and the corresponding int
        is the frequency of the word in l
    """

    freqs = {}
    for i in word_list:
        if i not in freqs:
            freqs[i] = 1 #create a new key in the freqs dict, starting with a frequency of 1
        else:
            freqs[i] += 1 #adds one to the value of an existing key

    return freqs

    pass


### Problem 3: Get Words Sorted by Frequency
def get_words_sorted_by_frequency(frequencies_dict):
    """
    Args:
        frequencies_dict: dictionary that maps a word to its frequency
    Returns:
        list of words sorted by decreasing frequency with ties broken
        by alphabetical order
    """

    frequencies_dict = sorted(frequencies_dict.items()) #puts the dict in alphabetically order first

    sorted_freq = sorted(frequencies_dict, key = lambda x:x[1], reverse = True)  #sorts the dictionary numerically based on the values, and reverses it to be in descending order
    sorted_freq = dict(sorted_freq)
    sorted_freq = list(sorted_freq.keys()) #converts the sorted_freq dict into a list of only the keys

    return sorted_freq

    pass


### Problem 4: Most Frequent Word(s) ###
def get_most_frequent_words(dict1, dict2):
    """
    The keys of dict1 and dict2 are all lowercase,
    you will NOT need to worry about case sensitivity.

    Args:
        dict1: frequency dictionary for one text
        dict2: frequency dictionary for another text
    Returns:
        list of the most frequent word(s) in the input dictionaries

    The most frequent word:
        * is based on the combined word frequencies across both dictionaries.
          If a word occurs in both dictionaries, consider the sum the
          frequencies as the combined word frequency.
        * need not be in both dictionaries, i.e it can be exclusively in
          dict1, dict2, or shared by dict1 and dict2.
    If multiple words are tied (i.e. share the same highest frequency),
    return an alphabetically ordered list of all these words.
    """

    for i in dict1:
        if i not in dict2:
            dict2[i] = dict1[i] #adding the word with its frequency into dictionary 2 if it is not in dict2 to begin with
        else:
            dict2[i] += dict1[i] #if the word is already in dict2, add the frequency of the word in dict1 to the frequency value of the word in dict2

    dict2 = sorted(dict2.items())
    dict2 = dict(dict2) #create an alphabetically ordered dictionary of dict2

    most_freq = []
    most_freq_num = max(dict2.values()) #value of the greatest frequency
    for i in dict2:
        if dict2[i] == most_freq_num: #if the frequency of the certain word is the greatest frequency, add it to the list, most_freq, which will be returned
            most_freq.append(i)

    return(most_freq)

    pass


### Problem 5: Similarity ###
def calculate_similarity_score(dict1, dict2):
    """
    The keys of dict1 and dict2 are all lowercase,
    you will NOT need to worry about case sensitivity.

    Args:
        dict1: frequency dictionary of words of text1
        dict2: frequency dictionary of words of text2
    Returns:
        float, a number between 0 and 1, inclusive
        representing how similar the words/texts are to each other

        The difference in words/text frequencies = DIFF sums "frequencies"
        over all unique elements from dict1 and dict2 combined
        based on which of these three scenarios applies:
        * If an element occurs in dict1 and dict2 then
          get the difference in frequencies
        * If an element occurs only in dict1 then take the
          frequency from dict1
        * If an element occurs only in dict2 then take the
          frequency from dict2
         The total frequencies = ALL is calculated by summing
         all frequencies in both dict1 and dict2.
        Return 1-(DIFF/ALL) rounded to 2 decimal places
    """

    dict1copy = dict1.copy() #create copies of each dict so that functions on one does not interfere with the other during the calculations
    dict2copy = dict2.copy()

    #for delta
    for i in dict1copy:
        if i not in dict2copy:
            dict2copy[i] = dict1copy[i] #create a new key of the word found in dict1 but not in dict2, with the value as its frequency
        else:
            dict2copy[i] -= dict1copy[i] #if the word is in both dictionaries, subtract the frequencies (stored into dict2) to find the difference

    delta_sum = 0
    for i in dict2copy:
        delta_sum += abs(dict2copy[i]) #add up all the frequency differences, absolute valued because negative values could exist from code above

    #for sigma
    for i in dict1:
        if i not in dict2:
            dict2[i] = dict1[i] #create a new key of the word found in dict1 but not in dict2, with the value as its frequency
        else:
            dict2[i] += dict1[i] #if the word is in both dictionaries, add the frequencies (stored into dict2) together to find the toal frequency of the word

    sigma_sum = 0
    for i in dict2:
        sigma_sum += dict2[i] #add up the frequencies of all the words

    similarity = 1-(delta_sum/sigma_sum) #calculate similarity
    similarity = round(similarity,2) #round similarity to 2 decimal places
    return similarity

    pass


### Problem 6: Finding TF-IDF ###
def get_tf(text_file):
    """
    Args:
        text_file: name of file in the form of a string
    Returns:
        a dictionary mapping each word to its TF

    * TF is calculated as TF(i) = (number times word *i* appears
        in the document) / (total number of words in the document)
    * Think about how we can use get_frequencies from earlier
    """

    text = prep_data(load_file(text_file))
    freq_dict = get_frequencies(text)  #creates a dictionary with {word:frequency}

    words = len(text) #total number of words

    tf = {}
    for w in freq_dict:
        tf[w] = freq_dict[w]/words #creates a dicitionary with {word:tf}

    return tf

    pass


def get_idf(text_files):
    """
    Args:
        text_files: list of names of files, where each file name is a string
    Returns:
       a dictionary mapping each word to its IDF

    * IDF is calculated as IDF(i) = log_10(total number of documents / number of
    documents with word *i* in it), where log_10 is log base 10 and can be called
    with math.log10()

    """

    num_docs = len(text_files) #total number of documents

    dict_texts = {}
    for i in range(num_docs):
        text = list(set(prep_data(load_file(text_files[i])))) #creates a list of the words in a certain file, without duplicates

        for x in text:
            if x in dict_texts:
                dict_texts[x] += 1 #if the word exists in the dictionary, add one to keep track of how many documents have that word
            else:
                dict_texts[x] = 1 #if the word is not in the dictionary, set its value to one

    words = list(dict_texts.keys()) #create a list of the words in the documents
    docs_with_w = list(dict_texts.values()) #create a list of values which are the number of documents that have the certain word in it, each value corresponding to a certain word that is at the same index as the above list
    idf = {}
    for i in range(len(dict_texts)):
        idf[words[i]] = abs(math.log10(num_docs/docs_with_w[i])) #create a dictionary that maps words to its calculated idf

    return idf

    pass


def get_tfidf(text_file, text_files):
    """
    Args:
        text_file: name of file in the form of a string (used to calculate TF)
        text_files: list of names of files, where each file name is a string
        (used to calculate IDF)
    Returns:
       a sorted list of tuples (in increasing TF-IDF score), where each tuple is
       of the form (word, TF-IDF). In case of words with the same TF-IDF, the
       words should be sorted in increasing alphabetical order.

    * TF-IDF(i) = TF(i) * IDF(i)
    """

    text = prep_data(load_file(text_file))

    tf = get_tf(text_file)
    idf = get_idf(text_files)

    #creats tfidf dictionary with {word:tf-idf}
    tfidf = {}
    for i in text:
        tfidf[i] = tf[i] * idf[i]

    tfidf = sorted(tfidf.items())  #puts the dict in alphabetically order first
    sorted_tfidf = sorted(tfidf, key = lambda x:x[1])  #sorts the dictionary numerically based on the values, in ascending order
    sorted_tfidf = dict(sorted_tfidf) #puts the sorted_tfidf into dict type

    #put keys and values into lists then pair them into tuples inside a larger list
    tfidf_value = list(sorted_tfidf.values())
    tfidf_word = list(sorted_tfidf.keys())
    tf_idf = []
    for i in range(len(tfidf_word)):
        tf_idf.append((tfidf_word[i],tfidf_value[i]))

    return tf_idf

    pass
