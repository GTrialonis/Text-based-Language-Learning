from tkinter import filedialog
from tkinter import *
from tkinter.scrolledtext import *
import random
 
root = Tk()
root.title("Take a Test Area")
root.configure(background='#B0C4DE')
 
global word, answ, lgth_file, num, chunk, indx, cor_word, corword
count = 0


def openfile():
    global count
    global word, lgth_file, num, chunk, indx, cor_word, corword
    root.filename = filedialog.askopenfilename(title='Select file',
                    defaultextension = 'txt', filetypes=(('Text files', '*.txt'), ('All files', '*.*')))

    with open(root.filename, encoding = "UTF-8") as file:
        cont = file.readlines() # reads the contents of the file
        lgth_file = len(cont) # finds the length in lines of the file
        while count <= 4:
            num = random.randint(0, lgth_file-1) # obtain a random number in
                                   # in the range of the length of the file length
            chunk = cont[num] # extract a line from the lines of the file
            indx = chunk.index('=') # find the index of the = sign inside the chunk
            cor_word = list(chunk[(indx-1):]) # pick the characters to the right of the = sign
            corword =  ''.join(cor_word) # it joints the individual characters to words
                                         # into the correct word

            
            count += 1
            translatethis()
            
##def contin(event):
##    global count
##    translatethis()
 
def translatethis():
    global word
    textArea1.delete('1.0', END)
    word = chunk[:(indx+1)].strip() # corword.strip()
    textArea1.insert('1.0', word) # it pops up a word in text area for translation
    
def enter_transl(event):
    global chunk, answ
##    text.delete('1.0', END) # deletes any previous word
    answ = word_to_transl.get() # asks user imput in entry field
    if answ in chunk:
        textArea1.insert(END, '\nWell done')
    else:
        textArea1.insert(END, '\nTry again')

 
frame1 = Frame(root)  # reserved for Text Area 1
frame2 = Frame(root)  # reserved for Entry Area
 
frame1.grid(row=1, column=0, padx=30, pady=30)  # place frame1
frame2.grid(row=2, column=0, padx=30, pady=10)  # place frame2, keep pady=10
 
textArea1 = ScrolledText(frame1, width=100, height=10, bd=2, padx=5, wrap=WORD)  # define textArea1
word_to_transl=StringVar()
entryArea = Entry(frame2, textvariable=word_to_transl, width=120, bd=3)  # define entryArea
entryArea.focus_set()
entryArea.bind('<Return>', enter_transl)

textArea1.grid(row=1, column=0)  # place Text Area1
entryArea.grid(row=2, column=1)  # place Entry Area

lbl1 = Label(frame2, text="Translate here -->", padx=3)
lbl1.grid(row=2,column=0, sticky='sw')
 
btn1 = Button(frame1, text='Select test', bg='#FFE4B5', command=openfile)
btn1.grid(row=0, column=0, sticky=W)

root.mainloop()

##if __name__ == '__main__':
##    testengger_5b
