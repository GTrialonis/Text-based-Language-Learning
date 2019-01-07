from tkinter import filedialog
from tkinter import *
from tkinter.scrolledtext import *
import random
##from time import sleep
 
root = Tk()
root.title("Take a Test Area")
root.configure(background='#E6E6FA')
root.geometry('1000x300')
 
global word, answ, lgth_file, num, chunk, cont, canMoveToNextWord
count = 0

canMoveToNextWord = False

def openfile():
    global count, cont
    global word, lgth_file, num, chunk, chunk_list
    root.filename = filedialog.askopenfilename(title='Select file',
    defaultextension='txt', filetypes=(('Text files', '*.txt'), ('All files', '*.*')))
   
    with open(root.filename, encoding="UTF-8") as file:
      cont = file.readlines()  # reads the contents of the file
      lgth_file = len(cont)  # finds the length in lines of the file
      next_word()
      display_word()
 
 
def display_word():
    textArea1.delete('1.0', END)
##    textArea1.insert('1.0', chunk_left)
    textArea1.insert(END, chunk_left)


def next_word():
    global chunk_left, chunk_right
    num = random.randint(0, lgth_file - 1)  # obtain a random number in
    # in the range of the length of the file length
    chunk = cont[num]  # extracts a line from the lines of the file
    chunk_list = chunk.split(' = ')  # splits the line at the = sign and produces a list
    chunk_left = chunk_list[0].strip()  # this is the left side, a string
    chunk_right = chunk_list[1].strip()  # this is the right side, a string
    display_word()

def moveToNext(event):
    global canMoveToNextWord
    if canMoveToNextWord == True:
        next_word()
        canMoveToNextWord = False
        entryArea.delete(0, END)


def translate_this(event):
    global canMoveToNextWord
    if canMoveToNextWord == True:
        moveToNext(event)
    else:
        user_input = word_to_transl.get()
        if user_input in chunk_right:
            textArea1.insert(END, '\nYES, the correct answer is: ')
            textArea1.insert(END, user_input)
            textArea1.insert(END, '\nWELL DONE!')
            textArea1.insert(END, '\n---------------------------------------------------------')
            textArea1.insert(END, '\nPress the ENTER key to continue')
            entryArea.delete(0, END)
        else:
            textArea1.insert(END, '\nSorry, the correct answer is: ')
            textArea1.insert(END, chunk_right)
            textArea1.insert(END, '\n---------------------------------------------------------')
            textArea1.insert(END, '\nPress the ENTER key to continue')
            entryArea.delete(0, END)
        canMoveToNextWord = True
 
sidebar = Text(root, width=4, padx=3, takefocus=0,  border=0,
background='#E6E6FA', state='disabled',  wrap='none')
sidebar.pack(side='left',  fill='y')

textArea1 = Text(root, bg='#FFFAFA', wrap='word', undo=1)  # define textArea1
textArea1.pack(expand='yes', fill='both')
textArea1.configure(font='Tahoma') #
scroll_bar=Scrollbar(textArea1)
textArea1.configure(yscrollcommand=scroll_bar.set)
scroll_bar.configure(command=textArea1.yview)
scroll_bar.pack(side='right', fill='y')
                
word_to_transl = StringVar() 
entryArea = Entry(root, textvariable=word_to_transl, font=('Arial', '13'), bg='#F8F8FF', width=70, bd=4)  # define entryArea
entryArea.focus_set()
entryArea.bind('<Return>', translate_this)

btn1 = Button(root, text='Select TEST', font=('Arial', '13', 'bold'), fg='white', padx=10, bg='#B0C4DE', command=openfile)
btn1.pack(side=LEFT)
entryArea.pack(expand='yes', fill='both', side=LEFT)

lbl1 = Label(root, text="<<<< Translate here", font=('Arial','12','bold'), fg='white', bg='#778899', padx=10, pady=10)
lbl1.pack()
 
root.mainloop()
