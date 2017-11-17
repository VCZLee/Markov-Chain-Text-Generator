# import the text file that the script will generate text based off of and store the text in a string variable

with open('YOUR TXT FILE HERE') as myfile:
    markov_text = myfile.read().replace('\n', '')


# this is the string splitting function. It splits string variables into words, punctuation, and numbers.
# it then adds the words, punctuation marks, and numbers into a list

def word_extract(sample_text):

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
               'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',

               'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
               'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    delimiters = ['.', ',']

    punctuation = ['.', ',', '?', '!', '(', ')', ':', ';', '-', '+', '&', '%', '$', '/', '\\', '\'', '\"', ' ']

    word_list = []
    word_start = 0
    word_end = 0

    #there's a bunch of rules in here that basically tell the function to not include spaces as 'words'
    #also, it considers punctuation marks, as 'words'
    #note: numbers like 1,000,000 will be considered as one 'word'

    for i, c in enumerate(sample_text):
        if len(sample_text) == 1:
            word_end = i + 1
            word_list.append(sample_text[word_start:word_end])

        elif i == 0:
            if sample_text[i] in numbers:
                if sample_text[i + 1] in (numbers + letters):
                    pass
                elif sample_text[i + 1] in delimiters:
                    if len(sample_text) == 2:
                        word_end = i + 1
                        word_list.append(sample_text[word_start:word_end])
                        word_start = i + 1
                    elif sample_text[i + 2] in numbers:
                        pass
                    else:
                        word_end = i + 1
                        word_list.append(sample_text[word_start:word_end])
                        word_start = i + 1
                else:
                    word_end = i + 1
                    word_list.append(sample_text[word_start:word_end])
                    word_start = i + 1

            elif sample_text[i] in letters:
                if sample_text[i + 1] in letters:
                    pass
                else:
                    word_end = i + 1
                    word_list.append(sample_text[word_start:word_end])
                    word_start = i + 1

            elif sample_text[i] in punctuation:
                word_end = i + 1
                word_list.append(sample_text[word_start:word_end])
                word_start = i + 1

            else:
                word_start = i + 1
                word_end = i + 1

        elif i == len(sample_text) - 1:
            if sample_text[i] in (letters + punctuation + numbers):
                word_end = i + 1
                word_list.append(sample_text[word_start:word_end])
            else:
                pass

        else:
            if sample_text[i] in numbers:
                if sample_text[i + 1] in (numbers + letters):
                    pass
                elif sample_text[i + 1] in delimiters:
                    if len(sample_text) == 2:
                        word_end = i + 1
                        word_list.append(sample_text[word_start:word_end])
                        word_start = i + 1
                    elif sample_text[i + 2] in numbers:
                        pass
                    else:
                        word_end = i + 1
                        word_list.append(sample_text[word_start:word_end])
                        word_start = i + 1
                else:
                    word_end = i + 1
                    word_list.append(sample_text[word_start:word_end])
                    word_start = i + 1

            elif sample_text[i] in letters:
                if sample_text[i + 1] not in letters:
                    word_end = i + 1
                    word_list.append(sample_text[word_start:word_end])
                    word_start = i + 1
                else:
                    pass

            elif sample_text[i] in delimiters:
                if sample_text[i - 1] in numbers:
                    if sample_text[i + 1] in numbers:
                        pass
                    else:
                        word_end = i + 1
                        word_list.append(sample_text[word_start:word_end])
                        word_start = i + 1
                else:
                    word_end = i + 1
                    word_list.append(sample_text[word_start:word_end])
                    word_start = i + 1

            elif sample_text[i] in punctuation:
                word_end = i + 1
                word_list.append(sample_text[word_start:word_end])
                word_start = i + 1

            else:
                word_start = i + 1
                word_end = i + 1
    return word_list

# the above string splitting function will return a list variable, which will be called 'corpus'
# python dictionaries can only take tuples as dictionary keys, and not lists

corpus = word_extract(markov_text)
corpus = tuple(corpus)

# the markov order variable will tell the text generator how many words to look back on when it comes to generating text
# this is also known as order of a Markov model, or how many consecutive elements a markov model will use when generating text
markov_order = 8
markov_corpus = []
markov_dict = {}

# this loop will break the list of words in the 'corpus' variable into overlapping tuples, or n-grams

for i, c in enumerate(corpus):
    if markov_order >= len(corpus):
        raise ValueError('The order of the Markov Text Generator is greater than the corpus size')
    elif i > len(corpus) - markov_order - 1:
        pass
    else:
        markov_corpus.append(corpus[i:i + markov_order])

# this loop pairs each of the previous tuples with the word immediately following them

for i, c in enumerate(corpus):
    if markov_order >= len(corpus):
        raise ValueError('The order of the Markov Text Generator is greater than the corpus size')
    elif i > len(corpus) - markov_order - 1:
        pass
    elif corpus[i:i + markov_order] in markov_dict:
        markov_dict[corpus[i:i + markov_order]].append(corpus[i + markov_order])
    else:
        markov_dict[corpus[i:i + markov_order]] = []
        markov_dict[corpus[i:i + markov_order]].append(corpus[i + markov_order])

import random

# this creates a variable called keys which has all the keys in the dictionary
# the loop looks through the dictionary and pulls all the keys whose last element is a period
# this will be used in starting the generated text



keys = [i for i in markov_dict.keys()]
periods = []
for i, c in enumerate(keys):
    if keys[i][-1] == '.':
        periods.append(keys[i])

markov_length = 10000

keys = [i for i in markov_dict.keys()]

markov_output = []
markov_output[0: markov_order] = random.choice(periods)


while i < markov_length:
    markov_output.append(random.choice(markov_dict[tuple(markov_output[i: i + markov_order])]))
    # print(markov_output)
    i = i + 1

del markov_output[0: markov_order]
markov_output = ''.join(markov_output)
markov_file = open('YOUR OUTPUT TXT FILE HERE', 'w')
markov_file.write(markov_output)
markov_file.close()
