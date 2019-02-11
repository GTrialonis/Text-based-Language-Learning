from tkinter import filedialog,re
from tkinter import *
##import pyperclip
import os
import tkinter.messagebox
from tkinter.scrolledtext import *

file_name = None

voc_file_name = ''
tex_file_name = ''
ran_file_name = ''
clicked = 0
info = "No more unknown words"
input_Value = ''' '''
contents = ''' '''
assted_vocab=''' '''
assted_transl=''' '''
update_vocab = update_trans = 0
flag = 0
count = 0

# ------------------------------------------ FUNCTIONS ------------------------------

# ----------------------------- SELECTION - DELETION ------------------------------

# -------------------------------- LOAD FILES ---------------------------------------
def open_File():
    input_file_name = filedialog.askopenfilename(initialdir='/', title='Select File',
                                    defaultextension='.txt', filetypes=(('Text Files ', '*.txt'), ('All Files ', '*.*')))
    if input_file_name:
        global file_name, contents, voc_file_name, tex_file_name, ran_file_name
        file_name = input_file_name
        if "-VOC" in input_file_name:
            textArea1.delete('1.0', END)
            with open(file_name, encoding='UTF-8') as file:
                contents = file.readlines() # this is the study file, referenced as 'text' below
                contents = ''.join(contents) # the study file, again
                textArea1.insert('1.0', contents) # opens file and places inside textArea1
                textArea1.tag_add("start", "1.0", "400.50") # --------------------------------
                textArea1.tag_config("start", font=('Tahoma', 12)) # ------------------------
                voc_file_name = file_name
        elif "-TEX" in input_file_name:
            textArea3.delete('1.0', END)
            with open(file_name, encoding='UTF-8') as file:
                contents = file.readlines() # this is the study file, referenced as 'text' below
                contents = ''.join(contents) # the study file, again
                textArea3.insert('1.0', contents) # opens file and places inside textArea1
                textArea3.tag_add("start", "1.0", "150.100") # --------------------------------
                textArea3.tag_config("start", font=('Helvetica', 12)) # ------------------------
                tex_file_name = file_name
        else: # this loads a file in the tRANslation area
            textArea4.delete('1.0', END)
            with open(file_name, encoding='UTF-8') as file:
                contents = file.readlines() # this is the study file, referenced as 'text' below
                contents = ''.join(contents) # the study file, again
                textArea4.insert('1.0', contents) # opens file and places inside textArea1
                textArea4.tag_add("start", "1.0", "150.100") # --------------------------------
                textArea4.tag_config("start", font=('Times New Roman', 13)) # ------------------------
                ran_file_name = file_name

# ------------------ CLEAR INFORMATION IN VOC., TEXT, and TRANSLATION areas -----------------
def clear_VOC():
    textArea1.delete('1.0', END) # opens file and places inside textArea1

def clear_TEX():
    textArea3.delete('1.0', END) # opens file and places inside textArea3

def clear_RAN():
    textArea4.delete('1.0', END) # opens file and places inside textArea4

# ------------------------ SAVE FILES -------------------------------------
def save(file_name):
    if not file_name:
        save_as()
    else:
        write_to_file(file_name)

def write_to_file(file_name):
    try:
        if "-VOC" in file_name:
            content = textArea1.get('1.0', END)
            with open(file_name, 'w', encoding='utf-8') as the_file:
                the_file.write(content)
        elif "-TEX" in file_name:
            content = textArea3.get('1.0', END)
            with open(file_name, 'w', encoding='utf-8') as the_file:
                the_file.write(content)
        else:
            content = textArea4.get('1.0', END)
            with open(file_name, 'w', encoding='utf-8') as the_file:
                the_file.write(content)
    except IOError:
        tkinter.messagebox.showwarning("Save", "Could not save the file")
    
def save_as():
    tkinter.messagebox.showwarning("Save as", "Please, remember to use suffix\n'-VOC for Vocabularies, or\n'-TEX' for Text files,\nor '-RAN' for translation files.")
    input_file_name = filedialog.asksaveasfilename(initialdir = "/", defaultextension='*.txt',
                filetypes = (("Text Documents","*.txt"), ("all files","*.*")))
    
    if input_file_name:
        global file_name
        file_name = input_file_name
        with open(file_name, 'w', encoding='utf-8') as txt_file:
            if "-VOC" in file_name:
                txt_file.write(textArea1.get('1.0', END))
            elif "-TEX" in file_name:
                txt_file.write(textArea3.get('1.0', END))
            else:
                txt_file.write(textArea4.get('1.0', END))
#--------------------------- UNKNOWN WORDS AREA ------------------------------------
'''  
This is to find unknown words from opened file above. The file is
'filtered' through 'known_words.txt' below, which is created by
the student on a text editor and saved as .txt, UTF-8 file.
'''
def mkList_unWords():
    global contents, flag, clicked
    global input_Value, count
    if clicked > 0:
        textArea2.delete('1.0', END)
        textArea2.insert(END, info)
    elif file_name == None:
        tkinter.messagebox.showwarning("first SAVE AS, then LOAD", "You can create a list of uknown words\nfrom saved files.\
                                       \nPlease SAVE AS the pasted text then LOAD\nit back to then CREATE list of Unknown words")
    else:
        text = re.findall(r'\w+', contents)# contents of opened file are stripped of punctuation (i.e. all
                # characters and numbers ONLY are selected and changed to a list and placed in variable 'text'.
                # This is the study file processed, or changed.
            
    # The operation below acts as filter of the opened file (now referenced as 'text')      
        with open('C:\\Users\\user\\Desktop\\SAVE THESE\\known_words.txt', encoding='UTF-8') as file:
            kn_wrds = file.read() # it reads the content of file 'known_words'
            mySet = set(text) # this converts the list of file 'text' to a set
                    # This operation removes double (and more) occurences of words
            
            finList =  list(mySet) # back to a list
            for word in finList: # refence to 'word' in the 'text' file (the study file)
                if word not in kn_wrds:
                    if word.isalpha(): # removes numbers from the list of unknown words
                        textArea2.insert(END, word+'\n')
                        textArea1.insert(END, word+' = '+'\n') # ---- ADDED RECENTLY TO TEST EFFECTIVENESS -----
                        flag += 1 # this is correct
                        clicked += 1 # increments to one (1) when unknown words are created for first time

# --------------------------------------------------
def append_to_unknown():
    global flag # this is correct
    comma_count = 0
    
    with open('C:\\Users\\user\\Desktop\\SAVE THESE\\drop_words.txt', 'w+', encoding='utf-8') as drop_file:
        drop_file.write(textArea2.get("1.0", END))

    with open('C:\\Users\\user\\Desktop\\SAVE THESE\\drop_words.txt', encoding='utf-8') as file:
        content = file.read()
        content = content.split()
        comma = ', '
        words = comma.join(content)
    

    file = open('C:\\Users\\user\\Desktop\\SAVE THESE\\known_words.txt', 'a', encoding='utf-8')
    file.write(words)                   
    file.close()
                       
                        
def clear_unWords():
    tkinter.messagebox.showwarning("Save?", "Are you sure?")
    textArea2.delete('1.0', END)


def exit_Progr():
    if tkinter.messagebox.askokcancel('EXIT Program?', 'If you wish to EXIT the program,\nmake sure you have saved\n your texts and vocabulary'):
        root.destroy()
    
# Root for main window
root = Tk()
root.title("TbLLT: Text-based Language Learning Tool")
root.geometry('1100x680+10+10')
root.configure(background='#B0C4DE')
# ---------------------------THE READ ME FUNCTION ----------------------------------------
def read_me():
    windo = Tk()
    windo.title("ΠΛΗΡΟΦΟΡΙΕΣ ΚΑΙ ΧΡΗΣΗ ΤΟΥ ΠΡΟΓΡΑΜΜΑΤΟΣ")
    S = Scrollbar(windo)
    T = Text(windo, height=4, width=70, bg='#F5FFFA')
    S.pack(side=RIGHT, fill=Y)
    T.pack(side=LEFT, fill=Y)
    S.config(command=T.yview)
    T.config(yscrollcommand=S.set)
    with open('C:\\Users\\user\\Desktop\\SAVE THESE\\readme_file.txt') as file:
        readme_info = file.read()
    T.insert(END, readme_info)
    windo.mainloop()
# ------------- THE PARENT FRAMES------------------
leftWind = Frame(root, width=30, bg='navy') # for labeled areas, e.g. 'Vocabulary', etc
midWind= Frame(root, width=700, bg='#B0C4DE') # for Vocab., Text, Translation areas
midbWind=Frame(root, width=50, bg='#B0C4DE') # for the buttons
rightWind= Frame(root, width=300, bg='#B0C4DE') # for the listbox
# -------------- CHILD FRAMES ---------------------
frame1 = Frame(midWind) # for the Vocabulary
frame3 = Frame(midWind) # for the Text
frame4 = Frame(midWind) # for the Translation
#----------------------------------------------
frame1a= Frame(midbWind, bg='#B0C4DE') # for the buttons
frame3a= Frame(midbWind, bg='#B0C4DE')
frame4a= Frame(midbWind, bg='#B0C4DE')
#-------------- The listbox Frame ---------------
frame2 = Frame(rightWind, bg='#B0C4DE') # for Listbox1
frame5 = Frame(rightWind, bg='#B0C4DE') # for Listbox2

# ---------------- THE TEXT WIDGETS -----------------

textArea1 = ScrolledText(frame1, width=80, height=13, bd=2, padx=2, wrap=WORD) # for the Vocabulary
textArea3 = ScrolledText(frame3, width=80, height=13, bd=2, padx=2, wrap=WORD) # for the Text
textArea4 = ScrolledText(frame4, width=80, height=20, bd=2, padx=2, wrap=WORD) # for the Translation
butTA2 = Button(frame2, text="ADD THE WORDS TO THE 'FILTER'", font=('Italics', 10, 'bold'), bg='#87CEFA', command=append_to_unknown).pack(side=TOP, pady=5)
textArea2 = ScrolledText(frame2, width=55, height=25, bd=2) # for the right textbox

# ---------------- THE BUTTONS ---------------------------------

btn1 = Button(frame1a, text="⬅ Load VOCab.", width=13, command=open_File).grid(row=1,column=3,pady=3)
btn2 = Button(frame1a, text="Update", width=13, command=lambda:save(voc_file_name)).grid(row=2,column=3)
btn3 = Button(frame1a, text="Save As",width=13, command=save_as).grid(row=3,column=3,pady=3)
btn4 = Button(frame1a, text="Clear",width=13, command=clear_VOC).grid(row=4,column=3,pady=3)
btnx = Button(frame1a, text="EXIT Program", width=13, fg='white', bg='#8B0000', relief='raised', command=exit_Progr).grid(row=5, column=3)
btn2x = Button(frame1a, text="READ ME", width=13, bg='#008080', fg='white', relief='raised', command=read_me).grid(row=6, column=3, pady=3)
btnfr2 = Button(frame5, text="CLEAR", width=13, font=('Italics', 10, 'bold'), bg='#87CEFA', command=clear_unWords).pack(side=TOP, pady=5)
bt = [5,6,7,8,9,10,11,12,13]
for i in bt:
    btn=Button(frame3a, text="", width=13, relief='flat', bg='#B0C4DE').grid(row=i, column=3)
btnUnk = Button(frame3a, text="Create List of\nUnknown Words  ➡\n⬅       from TEXT", bg='navy', fg='white',width=17,
                command=mkList_unWords).grid(row=6,column=3,pady=10)
btn1 = Button(frame3a, text="⬅ Load TEXt.", width=13, command=open_File).grid(row=7, column=3)
btn2 = Button(frame3a, text="Update", width=13, command=lambda:save(tex_file_name)).grid(row=8, column=3, pady=3)
btn3 = Button(frame3a, text="Save As",width=13, command=save_as).grid(row=9, column=3)
btn4 = Button(frame3a, text="Clear",width=13, command=clear_TEX).grid(row=10, column=3, pady=3)    
        
btn1 = Button(frame4a, text="⬅ Load tRANsl.", width=13, command=open_File).grid(row=9, column=3)
btn2 = Button(frame4a, text="Update", width=13, command=lambda:save(ran_file_name)).grid(row=10, column=3, pady=5)
btn3 = Button(frame4a, text="Save As",width=13, command=save_as).grid(row=11, column=3)
btn4 = Button(frame4a, text="Clear",width=13, command=clear_RAN).grid(row=12, column=3,pady=5)
btnhide = Button(frame4a, text="", width=13, relief='flat', bg='#B0C4DE').grid(row=13, column=3) # ************ latest addition ******

textL = ['V','O','C','A','B','U','L','A','R','Y','','T','E','X','T','', 'A','R','E','A','','T','R','A','N','S','/','T','I','O','N']
for item in textL:
    lab1 = Label(leftWind, text=item, font=('Arial',8,'bold'),fg='white', bg='navy').pack(side=TOP)

leftWind.pack(side=LEFT, padx=5)
midWind.pack(side=LEFT)
midbWind.pack(side=LEFT, padx=5)
rightWind.pack(side=LEFT, padx=5)

frame1.pack(side=TOP) # for the Text Areas
frame3.pack(side=TOP)
frame4.pack(side=TOP)

frame1a.pack(padx=5) # for the buttons
frame3a.pack(padx=5)
frame4a.pack(padx=5)

frame2.pack() # for the Listbox areas
frame5.pack()

textArea1.pack(side=TOP, pady=5)
textArea3.pack(side=TOP)
textArea4.pack(side=TOP, pady=5)

textArea2.pack(side=TOP, padx=10)


root.mainloop()


