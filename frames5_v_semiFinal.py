from tkinter import *
from tkinter import filedialog
from tkinter.scrolledtext import *
from tkinter import Scrollbar
import random

# ----------- THE START OF VOCABULARY TESTING PYTHON PROGRAM -------------
global word, answ, lgth_file, num, chunk, cont, canMoveToNextWord
count = 0
user_input = ''
canMoveToNextWord = False
# --------------- values for the TbLLT -----------------
input_Value = ''' '''
contents = ''' '''
# ------------------------------------------------------
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
    textArea4.delete('1.0', END)
    textArea4.insert(END, chunk_left)


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
        entryArea1.delete(0, END)


def translate_this(event):
    global canMoveToNextWord
    if canMoveToNextWord == True:
        moveToNext(event)
    else:
        user_input = word_to_transl.get()
        if user_input in chunk_right:
            textArea4.insert(END, '\nYES, the correct answer is:---->> ')
            textArea4.insert(END, chunk_right)
            textArea4.insert(END, '\nWELL DONE!')
            textArea4.tag_add("start", "3.0", "3.10") #
            textArea4.tag_config("start", background="white", foreground="blue") #
            textArea4.insert(END, '\n---------------------------------------------------------')
            textArea4.insert(END, '\nPress the ENTER key to continue')
            textArea4.tag_add("start", "5.0", "5.31") #
            textArea4.tag_config("start", background="white", foreground="green") #
            textArea4.tag_config("end") # for user_input above <-------------------------
            entryArea.delete(0, END)

        else:
            textArea4.insert(END, '\nSorry, the correct answer is:---->> ')
            textArea4.tag_add("start", "2.0", "2.6") # for Sorry ????
            textArea4.tag_config("start", background="white", foreground="red") # for Sorry ????
            textArea4.insert(END, chunk_right)
            textArea4.insert(END, '\n---------------------------------------------------------')
            textArea4.insert(END, '\nPress the ENTER key to continue')
            textArea4.tag_add("start", "4.0", "4.31") # this is OK
            textArea4.tag_config("start", background="white", foreground="green") # this is OK
            entryArea1.delete(0, END)
        canMoveToNextWord = True
# ----------------- END OF VOCABULARY TESTING PROGRAM -----------------
# ---------========-------- START OF TbLLT ----------------------------
def doNothing():
    pass

def open_txt_File():
    global contents
    root.filename = filedialog.askopenfilename(initialdir='/', title='Select File',
                                    defaultextension='txt', filetypes=(('Text Files ', '*.txt'), ('All Files ', '*.*')))
    with open(root.filename, encoding='UTF-8') as file:
        contents = file.readlines() # this is the study file, referenced as 'text' below
        contents = ''.join(contents) # the study file, again
        textArea1.insert('1.0', contents) # opened file and placed inside textArea1

def clear_Text():
    textArea1.delete('1.0', END)
  
# This is to find unknown words from opened file above. The file is
# 'filtered' through 'known_words.txt' below, which is created by
# the student on a text editor and saved as .txt, UTF-8 file.

def mkList_unWords():
    global contents
    global input_Value

    text = re.findall(r'\w+', contents)# contents of opened file are stripped of punctuation (i.e. all
            # characters and numbers ONLY are selected and changed to a list and placed in variable 'text'.
            # This is the study file processed, or changed.
            
    # The operation below acts as filter of the opened file (now referenced as 'text')      
    with open('known_words.txt', encoding='UTF-8') as file:
        kn_wrds = file.read() # it reads the content of file 'known_words'
        mySet = set(text) # this converts the list of file 'text' to a set
                # This operation removes double (and more) occurences of words
        
        finList =  list(mySet) # back to a list
        for word in finList: # refence to 'word' in the 'text' file (the study file)
            if word not in kn_wrds:
                if word.isalpha(): # removes numbers from the list of unknown words
                    textArea2.insert(END, word+' = '+'\n')
                    contents = ' '

def clear_unWords():
    textArea2.delete('1.0', END)

        
# Let's retrieve PASTED study text from textArea1
def retrieveInput():
    global input_Value
    global contents
    input_Value = textArea1.get('1.0', 'end-1c') # a string is generated
    save_As_File()
    

# Let's write the retrieved text and save it somewhere on the drive
def save_As_File():
    root.filename = filedialog.asksaveasfilename(initialdir = "/", defaultextension='.txt',
                filetypes = (("all files","*.*"),("jpeg files","*.jpg")))
    with open(root.filename, 'w', encoding='utf-8') as txt_file:
        txt_file.write(textArea1.get('1.0', END))


def exit_Progr():
    if messagebox.askokcancel('Quit?', 'If OK make sure you have saved\n your text and list of words'):
        root.destroy()
        

root = Tk()
root.geometry('1400x700+20+20')
root.state('zoomed')
root.config(bg='#E6E6FA') # dim gray


#-------------- TOP FRAME ------------------------
topFrame = Frame(root, width=1400, height=30)
topFrame.grid(row=0, column=0, columnspan=3)
topFrame.grid_propagate(False)

bar1 = Frame(topFrame, width=650, height=20)
bar1.grid(row=0, column=0)
##bar1.grid_propagate(False) #

bar2 = Frame(topFrame, width=320, height=20)
bar2.grid(row=0, column=1)

bar3 = Frame(topFrame, width=380, height=20)
bar3.grid(row=0, column=2)

label1 = Label(bar1, text="Text to study", fg='blue', font=('Arial', 11, 'bold'), padx=240)
label1.grid(row=0, column=0)

label2 = Label(bar2, text="Unknown Words", fg='red', font=('Arial', 11, 'bold'), padx=87)
label2.grid(row=0, column=1)

label3 = Label(bar3, text="Edit Unknown Words", fg='brown',
               font=('Arial', 11, 'bold'), padx=117)
label3.grid(row=0, column=2)

# -------------------------- MIDDLE FRAME A, TEXT AREA --------------------
textArea1 = ScrolledText(root, width=70, height=20, bg='#FFFAFA', bd=3, wrap=WORD)
textArea1.grid(row=2, column=0, sticky=NSEW, padx=3)

textArea2 = ScrolledText(root, width=30, height=20, bg='#FFFFF0')
textArea2.grid(row=2, column=1,sticky=W) #

textArea3 = ScrolledText(root, width=43, height=20, bg='#FFFFE0', wrap=WORD)
textArea3.grid(row=2, column=1, columnspan=2, padx=262, sticky=W)

##btn1 = Button(root, text='Open File', fg='black', bg='#E0FFFF')
##btn1.grid(row=3, column=0, sticky=NW, padx=10)

btn2 = Button(root, text='Create Unknown Words from above Text',
              bg='#FFF8DC',fg='black', command=lambda: mkList_unWords())
btn2.grid(row=3, column=0, sticky=NW, padx=73)

btn3 = Button(root, text='Clear Text above', fg='black', command=clear_Text)
btn3.grid(row=3, column=0, sticky=NW, padx=300)

btn4 = Button(root, text='Clear Unknown Words', fg='black',
              bg='#FFE4C4', command=clear_unWords)
btn4.grid(row=3, column=1, sticky=NW, padx=65)
# ------------------------------ BOTTOM FRAME 1 -----------------------------
btmFrame1 = Frame(root, width=1400, height=35, bg='#708090')
btmFrame1.grid(row=4, column=0, columnspan=3, sticky=W)
btmFrame1.grid_propagate(False)

label4 = Label(btmFrame1, text='TEST YOUR KNOWLEDGE IN FOREIGN LANGUAGE VOCABULARIES',
               font=('Arial', 11, 'bold'), fg='white', bg='#708090', padx=420, pady=6)
label4.grid(row=4, column=0)

btn5 = Button(root, text='Select Vocabulary TEST', font=('Arial', '11', 'bold'), fg='white',
              bg='#778899', command=openfile)
btn5.grid(row=7, column=0, padx=10)
          

# --------------- BOTTOM FRAME B / VOCABULARY TESTING AREA -----------------------------
# ------ Text ------
##sidebar = Text(root, width=4, padx=3, takefocus=0,  border=0,
##background='#E6E6FA', state='disabled',  wrap='none')
##sidebar.grid(column=0, columnspan=2, row=5)

textArea4 = ScrolledText(root, width=78, height=8, bg='#FFFFE0', bd=3, wrap=WORD)
textArea4.grid(row=5, column=0, sticky=W, padx=3)
textArea4.configure(font='Tahoma') #
##scroll_bar=Scrollbar(textArea4)
##textArea4.configure(yscrollcommand=scroll_bar.set)
##scroll_bar.configure(command=textArea4.yview)
##scroll_bar.grid(column=0, columnspan=2, row=5)
#------ Entry ------

label5 = Label(root, text="Translate here", font=('Arial','12','bold'), bg='#696969', fg='white')
label5.grid(row=7, column=0, padx=3, sticky=W)

word_to_transl = StringVar()
entryArea1 = Entry(root, textvariable=word_to_transl,font=('Arial', '12'), bg='white', width=80, bd=3)  # define entryArea
entryArea1.grid(row=6, column=0)
entryArea1.focus_set()
entryArea1.bind('<Return>', translate_this)
# -----------------------------------------------------------------------

menu = Menu(root)
root.config(menu=menu)
subMenu = Menu(menu)
menu.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Open .txt File", command=open_txt_File)
subMenu.add_separator()
subMenu.add_command(label="Save as..", command=save_As_File)
subMenu.add_separator()
subMenu.add_command(label="Exit", command=exit_Progr)

root.mainloop()
