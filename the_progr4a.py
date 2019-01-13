from tkinter import filedialog, END, re
from tkinter import *
from tkinter import messagebox
from tkinter.scrolledtext import *
from ctypes import windll
##from testengger_6 import *

input_Value = ''' '''
contents = ''' '''
assted_vocab=''' '''
assted_transl=''' '''

# FUNCTIONS
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

        
# Let's open the associated vocabulary
def open_txt_ass_vocab():
    global assted_vocab
    root.filename = filedialog.askopenfilename(initialdir='/', title='Select File',
                                    defaultextension='txt', filetypes=(('Text Files ', '*.txt'), ('All Files ', '*.*')))
    with open(root.filename, encoding='UTF-8') as file:
        assted_vocab = file.readlines() # this is the study file, referenced as 'text' below
        assted_vocab = ''.join(assted_vocab) # the study file, again
        textArea3.insert('1.0', assted_vocab) # opened file and placed inside textArea1
    
def open_txt_ass_transl():
    global assted_transl
    root.filename = filedialog.askopenfilename(initialdir='/', title='Select File',
                                    defaultextension='txt', filetypes=(('Text Files ', '*.txt'), ('All Files ', '*.*')))
    with open(root.filename, encoding='UTF-8') as file:
        assted_transl = file.readlines() # this is the study file, referenced as 'text' below
        assted_transl = ''.join(assted_transl) # the study file, again
        textArea4.insert('1.0', assted_transl) # opened file and placed inside textArea1
        
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
root.title("Text-based Language Learning Tool")
root.geometry('1000x610+10+10')
root.configure(background='#BDB76B')

frame1 = Frame(root) # for Text Area 1
frame2 = Frame(root) # for Text Area 2
frame3 = Frame(root) # for associated Vocabulary display
frame4 = Frame(root)
frame5 = Frame(root) # for Translated Text display

btn1 = Button(root, text="Make list of unknown words from text below",
              bg='#556B2F', fg='white', command=lambda: mkList_unWords())
btn2 = Button(root, text="Clear text below", bg='#556B2F', fg='white', command=clear_Text)
btn3 = Button(root, text="Clear list below", bg='#556B2F', fg='white', command=clear_unWords)
btn4 = Button(root, text="OPEN Text associated vocabulary", bg='#556B2F', fg='white', command=open_txt_ass_vocab)
btn5 = Button(root, text="OPEN associated\nTranslation", bg='#556B2F', fg='white', command=open_txt_ass_transl)

textArea1 = ScrolledText(frame1, width=85, height=13, bd=2, padx=5, wrap=WORD)
textArea2 = ScrolledText(frame2, width=28, height=13, bd=2, padx=5, wrap=WORD)
textArea3 = ScrolledText(frame3, width=70, height=8, bd=2, wrap=WORD)
textArea5 = ScrolledText(frame5, width=85, height=10, bd=2, wrap=WORD)
lbl = Label(frame4, width=90, height=0, bg='#BDB76B')

frame1.grid(row=0, column=0, padx=10, pady=30)
frame2.grid(row=0, column=1, padx=7)
frame3.grid(row=1, column=0, columnspan=2)
frame4.grid(row=2, column=0, columnspan=2)
frame5.grid(row=3, column=0, columnspan=2)

textArea1.grid(row=0, column=0)
textArea2.grid(row=0, column=1)
textArea3.grid(row=1, column=0, sticky=NW)
textArea5.grid(row=3, column=0, sticky=NW)
lbl.grid(row=2, column=0)
         
btn1.place(x=115, y=2)
btn2.place(x=363, y=2)
btn3.place(x=750, y=2)
btn4.grid(row=1, column=0, padx=10, sticky=NW)
btn5.grid(row=3, column=0, padx=35, sticky=NW)


# Adding Menus
menu_bar = Menu(root)
root.config(menu=menu_bar)
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Open .txt File", command=open_txt_File)
file_menu.add_command(label="Save as..", command=save_As_File)
file_menu.add_command(label="Exit", command=exit_Progr)
menu_bar.add_cascade(label='File', menu=file_menu)

help_menu = Menu(menu_bar, tearoff=0)
help_menu.add_command(label='Read me', command=doNothing)
menu_bar.add_cascade(label='Help', menu=help_menu)

root.mainloop()


