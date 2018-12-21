# This program FLIPS vocabulary listings on the axis of the equal (=) sign.
# For example: speak = sprechen, reden --> becomes: sprechen, reden = speak

# Access and open a file

with open('English_Deutsch_WB.txt', encoding = 'UTF-8') as file:
    cont = file.readlines() # reads the contents of the file
    lgth_file = len(cont) # finds the length of the file
    for line in range(1, lgth_file):
        with open('Deutsch_English_WB.txt', 'a', encoding = 'UTF-8') as file: # create a new file
            chunk = cont[line] # pick lines one by one of the previous file
            indx = chunk.index('=') # find the index of the = sign inside lines of previous file
            left_side = list(chunk[:(indx)])
            left_side = ''.join(left_side)
                                
            right_side = list(chunk[(indx+2):-1])
            right_side = ''.join(right_side)
            
            new_lines = list(right_side + ' = ' + left_side)
            new_lines = ''.join(new_lines)
            
            file.writelines(new_lines) # write the new lines in the new file
            file.writelines('\n') # add a carriage return
            
