from tkinter import filedialog
from tkinter import *
from tkinter.scrolledtext import *
import random
##from time import sleep
 


global word, answ, lgth_file, num, chunk, cont, canMoveToNextWord
test_question = count = perc_success = cor_answ = 0

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
    textArea1.insert(END, chunk_left)


def next_word():
    global chunk_left, chunk_right
    num = random.randint(0, lgth_file)  # obtain a random number in
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
    global test_question, perc_success, cor_answ
    if canMoveToNextWord == True:
        moveToNext(event)
    else:
        user_input = word_to_transl.get()
        test_question += 1
        if user_input in chunk_right:
            cor_answ = cor_answ+1
            perc_success = round((cor_answ/test_question)*100) # calculating SUCCESS RATE
            textArea1.insert(END, '\nYES, the correct answer is:---->> ')
            textArea1.insert(END, chunk_right)
            textArea1.tag_add("start", "2.33", "2.80") # for user input above
            textArea1.tag_config("start", background="white", foreground="green") # for user_input above ???????
##            textArea1.tag_config("end", "2.81") # for user_input above <-------------------------
            textArea1.insert(END, '\nWELL DONE!')
##            textArea1.tag_add(start="3.0", end="3.10") #
            textArea1.tag_config("white", foreground="blue") #
            textArea1.insert(END, '\n--------------------------------------------------------- average success rate %: ')
            textArea1.insert(END, perc_success)
            textArea1.insert(END, '\nPress the ENTER key to continue')
            textArea1.tag_add("start", "5.0", "5.31") #
            textArea1.tag_config("start", background="white", foreground="green") #
            textArea1.tag_config("end") # for user_input above <-------------------------
            entryArea.delete(0, END)
            
        else:
            perc_success = round((cor_answ/test_question)*100)
            textArea1.insert(END, '\nSorry, the correct answer is:---->> ')
            textArea1.tag_add("start", "2.0", "2.6") # for Sorry ????
            textArea1.tag_config("start", background="white", foreground="red") # for Sorry ????
            textArea1.insert(END, chunk_right)
            textArea1.insert(END, '\n--------------------------------------------------------- average success rate %: ')
            textArea1.insert(END, perc_success)
            textArea1.insert(END, '\nPress the ENTER key to continue')
            textArea1.tag_add("start", "4.0", "4.31") # this is OK
            textArea1.tag_config("start", background="white", foreground="green") # this is OK
            entryArea.delete(0, END)
        canMoveToNextWord = True

root = Tk()
root.title("Take a Test Area")
root.configure(background='#E6E6FA')
root.geometry('1000x300')

sidebar1 = Text(root, width=4, padx=3, takefocus=0,  border=0,
background='#E6E6FA', state='disabled',  wrap='none')
sidebar1.pack(side='left',  fill='y')

sidebar2 = Text(root, width=4, padx=3, takefocus=0,  border=0,
background='#E6E6FA', state='disabled',  wrap='none')
sidebar2.pack(side='right',  fill='y')

frame1 = Frame(root, width=10000, height=35, bg='#E6E6FA')
frame1.pack(side=TOP)

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

btn1 = Button(root, text='Select TEST', font=('Arial', '13', 'bold'), fg='white', padx=10, bg='#000080', command=openfile)
btn1.pack(side=LEFT)
entryArea.pack(expand='yes', fill='both', side=LEFT)

lbl1 = Label(root, text="<<<< Translate here", font=('Arial','12','bold'), fg='white', bg='#778899', padx=10, pady=10)
lbl1.pack()

##textArea1.tag_add("start", "2.0", "2.10")#
##textArea1.tag_config("start", background="cyan") #

root.mainloop()

##if __name__ == "__main__":
##    
