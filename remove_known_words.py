# This program takes a whole text in German and
# changes text to words but with SAME words removed from the text.
# Then the remaining words are converted back to a list for printing
# on separate lines

# I use this program to create vocabularies of unknown German words.
# I also created a txt file with German words that I know. This file
# is very small and increases with new words that I learn every day.

#.....................IT WORKS................

import re

text_DE = ''' '''

text = re.findall(r'\w+', text_DE)  # allows the text to be printed
                                    # without the punctuation and
                                    # changes text to a list.
                                    
with open('known_words.txt', encoding="UTF-8") as file: 
    content = file.read()
    
# myList = text_DE.split() # This converts the text to a list of words

mySet = set(text)      # This converts the list to a set

finList = list(mySet)    # and the set is converted back to a list as final list

# srtList = sorted(finList, key=lambda s: s.casefold())  # Absolutely alphabetical

for word in finList: # this prints all words of the text
    if not word in content: # This does not allow printing of known words
        print(word)      # but without the duplicate words
