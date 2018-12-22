import random
import sys
try: color = sys.stdout.shell
except AttributeError: raise RuntimeError("Use IDLE")
from decimal import Decimal
count = 0
coransw = 0 # correct answers set to zero
test_question = 0 # tested questions to zero
perc_success = 0 # percentage of success set to zero
repeat = 0 # ask for one more word

with open('English_Deutsch_WB.txt', encoding = "UTF-8") as file:
    
    cont = file.readlines() # reads the contents of the file
    lgth_file = len(cont) # finds the length in lines of the file
    while repeat <= lgth_file:
        num = random.randint(0, lgth_file-1) # obtain a random number in
                            # in the range of the length of the file length
        chunk = cont[num] # extract a line from the lines of the file
        indx = chunk.index('=') # find the index of the = sign inside the chunk
        cor_word = list(chunk[(indx):]) # pick the characters to the left of the = sign
        corword =  ''.join(cor_word) # it joints the individual characters to words
                                     # into the correct word

        word_to_transl = input("Please translate: " + (chunk[:(indx-1)])+ ' = ')
        test_question += 1
        if word_to_transl in corword:
            coransw += 1
            perc_success = round((coransw/test_question)*100,2)
            color.write('You are right! ', "STRING")
            print(corword)
            print('Success rate: ', perc_success, '%')
            print('-----------------------------------------------')
     
        else:
            perc_success = round((coransw/test_question)*100,2) # How does this affect the score?
            color.write('The correct answer ', "COMMENT")
            print(corword)
            print('Success rate: ', perc_success)
            print('-----------------------------------------------')

        repeat = repeat +1
    
