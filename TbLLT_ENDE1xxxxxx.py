from tkinter import filedialog,re
from tkinter import *
import requests
import arrow
from bs4 import BeautifulSoup
import os
import tkinter.messagebox
from tkinter.scrolledtext import *
import sqlite3
import bkendTbLLT2
nw = arrow.now().format('DD-MM-YYYY')

file_name = None
lemma = ''
myStr = ''
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
        global file_name, voc_file_name, tex_file_name, ran_file_name
        global contVOC, contRAN, contTEX
        file_name = input_file_name
        if "-VOC" in input_file_name:
            textArea1.delete('1.0', END)
            with open(file_name, encoding='UTF-8') as file:
                contVOC = file.readlines() # this is the study file, referenced as 'text' below
                contVOC = ''.join(contVOC) # the study file, again
                textArea1.insert('1.0', contVOC) # opens file and places inside textArea1
                textArea1.tag_add("start", "1.0", "400.50") # --------------------------------
                textArea1.tag_config("start", font=('Calibri', 12)) # ------------------------
                voc_file_name = file_name
        elif "-TEX" in input_file_name:
            textArea3.delete('1.0', END)
            with open(file_name, encoding='UTF-8') as file:
                contTEX = file.readlines() # this is the study file, referenced as 'text' below
                contTEX = ''.join(contTEX) # the study file, again
                textArea3.insert('1.0', contTEX) # opens file and places inside textArea1
                textArea3.tag_add("start", "1.0", "150.100") # --------------------------------
                textArea3.tag_config("start", font=('Times New Roman', 13)) # ------------------------
                tex_file_name = file_name
        else: # this loads a file in the tRANslation area
            textArea4.delete('1.0', END)
            with open(file_name, encoding='UTF-8') as file:
                contRAN = file.readlines() # this is the study file, referenced as 'text' below
                contRAN = ''.join(contRAN) # the study file, again
                textArea4.insert('1.0', contRAN) # opens file and places inside textArea1
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
'filtered' through 'kn_wordsENDE.txt' below, which is created by
the student on a text editor and saved as .txt, UTF-8 file.
'''
def mkList_unWords():
    global contTEX, flag, clicked
    global input_Value, count
    if clicked > 0:
        textArea2.delete('1.0', END)
        textArea2.insert(END, info)
    elif file_name == None:
        tkinter.messagebox.showwarning("first SAVE AS, then LOAD", "You can create a list of uknown words\nfrom saved files.\
                                       \nPlease SAVE AS the pasted text then LOAD\nit back to then CREATE list of Unknown words")
    else:
        text = re.findall(r'\w+', contTEX)# contents of opened file are stripped of punctuation (i.e. all
                # characters and numbers ONLY are selected and changed to a list and placed in variable 'text'.
                # This is the study file processed, or changed.
            
    # The operation below acts as filter of the opened file (now referenced as 'text')      
        with open('C:\\Users\\user\\Desktop\\SAVE THESE\\kn_wordsENDE.txt', encoding='UTF-8') as file:
            knw_words_ende = file.read() # it reads the content of file 'kn_wordsENDE'
            mySet = set(text) # this converts the list of file 'text' to a set
                    # This operation removes double (and more) occurences of words
            
            finList =  list(mySet) # back to a list
            for word in finList: # refence to 'word' in the 'text' file (the study file)
                if word not in knw_words_ende:
                    if word.isalpha(): # removes numbers from the list of unknown words
                        textArea2.insert(END, word+'\n')
##                        textArea1.insert(END, word+' = '+'\n') # ---- ADDED RECENTLY TO TEST EFFECTIVENESS -----
                        flag += 1 # this is correct
                        clicked += 1 # increments to one (1) when unknown words are created for first time

# --------------------------------------------------
def append_to_known():
    global flag # this is correct
    comma_count = 0
    
    with open('C:\\Users\\user\\Desktop\\SAVE THESE\\drop_wordsENDE.txt', 'w+', encoding='utf-8') as drop_file:
        drop_file.write(textArea2.get("1.0", END))

    with open('C:\\Users\\user\\Desktop\\SAVE THESE\\drop_wordsENDE.txt', encoding='utf-8') as file:
        content = file.read()
        content = content.split()
        comma = ', '
        words = comma.join(content)
    

    file = open('C:\\Users\\user\\Desktop\\SAVE THESE\\kn_wordsENDE.txt', 'a', encoding='utf-8')
    file.write(words)                   
    file.close()
# -------------------- TEMPORARY SAVE WORDS from TextArea 2 -----------------------------------------------------
def temp_save():
    with open('C:\\Users\\user\\Desktop\\SAVE THESE\\temporary_saveENDE.txt', 'w+', encoding='utf-8') as temp_file:
        temp_file.write(textArea2.get("1.0", END))
                
# ----------------------  DELETE WORDS from TextArea 2   -------------------------------------------                     
def clear_unWords():
    tkinter.messagebox.askokcancel("Delete?", "Are you sure?")
    textArea2.delete('1.0', END)

# ------------------------ LOAD WORDS into TextArea 2----------------------------------------------
def load_unWords():
    with open('C:\\Users\\user\\Desktop\\SAVE THESE\\temporary_saveENDE.txt', encoding='utf-8') as temp_file:
        c = temp_file.read()
        textArea2.delete('1.0', END)
        textArea2.insert(END, c)
#--------------------------------------------------------------------------------
    
def exit_Progr():
    if tkinter.messagebox.askokcancel('EXIT Program?', 'If you wish to EXIT the program,\nmake sure you have saved\n your texts and vocabulary'):
        root.destroy()

# -------------------------------------------------------------------------------------------------------------------
#-------------- SEARCHING THE LANGENSCHEIDT DICTIONARY ----------------
def langensch_DEEN():
    der = 'Maskulinum | masculine m'
    die = 'Femininum | feminine f'
    das = 'Neutrum | neuter n'
    adj = 'Adjektiv | adjective adj'
    ajj = 'adjective | Adjektiv adj'
    adv = 'Adverb | adverb adv'
    trv = 'transitives Verb | transitive verb v/t <h>'
    trr = 'transitives Verb | transitive verb v/t <irregulär, unregelmäßig | irregularirr,untrennbar | inseparable untrennb, kein -ge-; h>'
    inv = 'intransitives Verb | intransitive verb v/i <h>'
    ivn = 'intransitives Verb | intransitive verb v/i'
    tve = 'transitives Verb | transitive verb v/t <kein ge-; h>'
    irr = '<irregulär, unregelmäßig | irregularirr,trennbar | separable trennb; -ge-; hund | and u. sein; h>'
    ttv = 'transitives Verb | transitive verb v/t <trennbar | separabletrennb; -ge-; h>'
    ttt = 'transitives Verb | transitive verb v/t <irregulär, unregelmäßig | irregularirr,trennbar | separable trennb; -ge-; h>'
    wbs = ',,Weitere Beispiele...'
    
    notesText.delete('1.0', END)
    
    lemma = fndWord.get()
    headers = {"Referer" : "TbLLT School of Languages", "User-Agent" : "Mozilla/5.0"}
    url = "https://de.langenscheidt.com/deutsch-englisch/"+lemma
    
    try:
        response = requests.get(url, headers=headers).text
        soup = BeautifulSoup(response, "lxml")
        # ----- the code below is for the searched word ----
        summary = soup.find('div', class_='summary-inner').text
        words = summary.replace(',,,Weitere Beispiele...', '')
        words = summary.replace(',,,Weitere Übersetzungen...', '')
        words = words.strip()
        myStr = words.replace('  ',',')

        # ---------------------------------------------------------------
        # ---- for the article / genitive / transitive, intransitive verbs / plural of the word above ----
        article = soup.find('span', class_='dict-additions').text
        art_plu = article.strip()
        if art_plu.startswith(der):
            rpl = art_plu.replace(der, 'der')
        elif art_plu.startswith(die):
            rpl = art_plu.replace(die, 'die')
        elif art_plu.startswith(das):
            rpl = art_plu.replace(das, 'das')
        elif art_plu.startswith(adj):
            rpl = art_plu.replace(adj, 'adj.')
        elif art_plu.startswith(ajj):
            rpl = art_plu.replace(ajj, 'adj.')
        elif art_plu.startswith(adv):
            rpl = art_plu.replace(adv, 'adv.')
        elif art_plu.startswith(trv):
            rpl = art_plu.replace(trv, 't/v.')
        elif art_plu.startswith(inv):
            rpl = art_plu.replace(inv, 'i/v.')
        elif art_plu.startswith(tve):
            rpl = art_plu.replace(tve, 't/v <kein ge->')
        elif art_plu.startswith(trr):
            rpl = art_plu.replace(trr, 't/v,')
        elif art_plu.startswith(ivn):
            rpl = art_plu.replace(ivn, 'i/v')
        elif art_plu.startswith(irr):
            rpl = art_plu.replace(irr, 'i/v,')
        elif art_plu.startswith(ttv):
            rpl = art_plu.replace(ttv, 't/v,')
        elif art_plu.startswith(ttt):
            rpl = art_plu.replace(ttt, 't/v,')
        elif art_plu.startswith(wbs):
            rpl = art_plu.replace(wbs, '')
        else:
            rpl = art_plu
        
        lemma = lemma+', '+rpl
        textArea1.insert(END, lemma+' = ')
        textArea1.insert(END, myStr+'\n')
        textArea1.see("end") # cursor goes to the end of the last word added --------/////-------/////-----
        lemma = ''
        myStr = ''
    except:
        notesText.insert(END, 'Word not found! Please check\nspelling and try again, or\nsearch another dictionary.')
        
# --------------------------------- ENGLISH - GERMAN -----------------------------------
def langensch_ENDE():
    notesText.delete('1.0', END)
    
    lemma = fndWord.get() # the word I am looking for
    headers = {"Referer" : "TbLLT School of Languages", "User-Agent" : "Mozilla/5.0"}
    url = "https://de.langenscheidt.com/englisch-deutsch/"+lemma
    
    try:
        response = requests.get(url, headers=headers).text
        soup = BeautifulSoup(response, "lxml")
        # ----- the code below is for the searched word ----
        summary = soup.find('div', class_='summary-inner').text
        words = summary.replace('Weitere Beispiele...', '')
        words = summary.replace('Weitere Übersetzungen...', '')
        words = words.strip()
        myStr = words.replace('  ',',')
# to find the article or part of speach (e.g. v/i, adj., n. etc.)
##        sumr = soup.find('div', class_='search-term')
##        smr = sumr.abbr.text
##        lemma = lemma+', '+smr
        
        textArea1.insert(END, lemma+' = ') # the word I am looking for
        textArea1.insert(END, myStr+'\n') # the meaning found
        textArea1.see("end") # cursor goes to the end of the last word added --------/////-------/////-----
        lemma = ''
        myStr = ''
    except:
        notesText.insert(END, 'Word not found! Please check\nspelling and try again, or\nsearch another dictionary.')
# ------------------------------------------------------------------------------------------------------------------
# ------------------------------ THE DATABASE ----------------------------------------------------------------------
def get_selected_row(event):
    try:
        global selected_tuple
        index = list1.curselection()[0]  # the entry's id has an index of zero
        selected_tuple = list1.get(index)
        e1.delete(0, END)
        e1.insert(END, selected_tuple[1])
        e2.delete(0, END)
        e2.insert(END, selected_tuple[2])
        e3.delete(0, END)
        e3.insert(END, selected_tuple[3])
        e4.delete(0, END)
        e4.insert(END, selected_tuple[4])
        e5.delete(0, END)
        e5.insert(END, selected_tuple[5])
        e6.delete(0, END)
        e6.insert(END, selected_tuple[6])
        e7.delete(0, END)
        e7.insert(END, selected_tuple[7])
    except IndexError:
        pass


def view_command():
    list1.delete(0, END)
    for row in bkendTbLLT2.view():
        list1.insert(END, row)


def search_command():
    list1.delete(0, END)
    for row in bkendTbLLT2.search(woRD_text.get(), partSpch_text.get(), plural_text.get(), pastPl_text.get(),
                              definition_text.get(), example1_text.get(), example2_text.get()):
        list1.insert(END, row)


def add_command():
    bkendTbLLT2.insert(woRD_text.get(), partSpch_text.get(), plural_text.get(), pastPl_text.get(),
                              definition_text.get(), example1_text.get(), example2_text.get())
    list1.delete(0, END)
    list1.insert(END, (woRD_text.get(), partSpch_text.get(), plural_text.get(), pastPl_text.get(),
                              definition_text.get(), example1_text.get(), example2_text.get()))


def delete_command():
    bkendTbLLT2.delete(selected_tuple[0])


def update_command():
    bkendTbLLT2.update(selected_tuple[0], woRD_text.get(), partSpch_text.get(), plural_text.get(), pastPl_text.get(),
                              definition_text.get(), example1_text.get(), example2_text.get())


def new_entry_command():
    e1.delete(0, END)
    e2.delete(0, END)
    e3.delete(0, END)
    e4.delete(0, END)
    e5.delete(0, END)
    e6.delete(0, END)
    e7.delete(0, END)

def clear_fields():
    list1.delete(0, END)
    
# --------LIST-----------------------------------------------------------------------------------------------------------
# Root for main window
root = Tk()
root.title("TbLLT: Text-based Language Learning Tool> PAIR is EN-DE")
root.geometry('1200x700+10+10')
root.state('zoomed')
root.configure(background='#778899')
# ---------------------------THE READ ME FUNCTION ----------------------------------------
def read_me():
    windo = Tk()
    windo.title("INFORMATION ABOUT THE PROGRAM")
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
# --------------------------------------------------------------------------------
# --------------- NOTEBOOK -----------------------------------------------------

def notebook():
    wnd = Tk()
    wnd.title('Notebook')
    global nw, scrTxt, txtAr
    
    ln = "--------------------------------"
    
    label = Label(wnd, width=68, height=2, fg='white', bg='#778899', padx=5)
    label.configure(text="Type your notes below the dotted line", font=('Arial', 10, 'bold'))

    scrTxt = ScrolledText(wnd, width=55, height=15, bg='#FAFAD2', wrap=WORD, padx=5)
    scrTxt.insert('1.0', 'Today is: '+nw+'\n')
    scrTxt.insert(END, ln+'\n')
    scrTxt.focus_set()

    butn = Button(wnd, width=60, bg='#F5F5F5', relief='flat')
    btn2 = Button(wnd, text='SAVE', width=12, font=('Tahoma', 10, 'bold'), fg='white', bg='#778899', pady=5, command=save_notes)

    with open('C:\\Users\\user\\Desktop\\SAVE THESE\\notes_ENDE.txt', encoding='utf-8') as notes_file:
        cnt = notes_file.read()
        scrTxt.insert('1.0', cnt)
        scrTxt.configure(font=('Tahoma', 11))
        scrTxt.see("end")

    label.grid(row=0)
    scrTxt.grid(row=1)
    butn.grid(row=2)
    btn2.grid(row=2, sticky=S)

        
    wnd.mainloop()
   
def save_notes():
    global nw, scrTxt, cnt
    ln = "--------------------------------"
    cnt = scrTxt.get('1.0', END)
    ctt = cnt+'\n'
    with open('C:\\Users\\user\\Desktop\\SAVE THESE\\notes_ENDE.txt', 'w+', encoding='utf-8') as notes_file:
        notes_file.write(ctt)

    
    
# ------------- THE PARENT FRAMES------------------
leftWind=Frame(root, width=35, bg='navy') # for bar,
midWind1=Frame(root, width=700, bg='#778899') # for Vocab., Text, Translation areas
midWind2=Frame(root, width=55, bg='#778899') # for the buttons
midWind3=Frame(root, width=100, bg='#778899') # for the textbox, unknown words
rightWind= Frame(root, width=200, bg='#778899') # for the database
rWind1 = Frame(rightWind, bg='#DCDCDC', relief=SUNKEN, bd=8) # division of right frame
rWind2 = Frame(rightWind, bg='#DCDCDC', relief=SUNKEN, bd=8) # division of right frame
rWind2a = Frame(rWind2, width=7, bg='#DCDCDC')  # subdivision of right frame LOCAL DATABASE
rWind2b = Frame(rWind2, width=30, bg='#DCDCDC')
rWind2c = Frame(rWind2, width=30, bg='#DCDCDC')

# -------------- CHILD FRAMES --------------------------------------------
frame1 = Frame(midWind1) # for the Vocabulary, row,col = 0, 0
frame3 = Frame(midWind1) # for the Text, row,col = 1,0
frame4 = Frame(midWind1) # for the Translation, row,col = 2,0
#-------------------------------------------------------------------------
frame1a= Frame(midWind2, bg='#778899') # for the buttons, row, col = 0,1
frame3a= Frame(midWind2, bg='#778899') # for the buttons, row, col = 1,1
frame4a= Frame(midWind2, bg='#778899') # for the buttons, row, col = 2,1
#-------------- The Texttbox andWeb-Scrapping child frames ---------------
frame2 = Frame(midWind3, bg='#778899') # for Textbox
frame5 = Frame(midWind3, bg='#778899') # for Webscraping
langDict = Label (frame5, text="Search an online Dictionary", font=("Tahoma", 10, 'bold'), fg='white', bg='#778899')
langDict.pack(side=TOP, padx=10, pady=5)
#---------------- The rightWind child frames -----------------------------
butDB = Button(rWind1, text='LOCAL DATABASE', font=('Arial', 14, 'bold'), width=34)
butDB.grid(row=0, columnspan=2, sticky=NSEW)

lab1 = Label(rWind1, text='Word: ', bg='#DCDCDC', font=('Times New Roman', 10, 'bold'))
lab1.grid(row=1, column=0, sticky=E)

woRD_text = StringVar()
e1 = Entry(rWind1, width=46, textvariable=woRD_text)
e1.grid(row=1, column=1, sticky=W)
#--------------------------------------------
lab2 = Label(rWind1, text='Art./Prt-Spch: ',bg='#DCDCDC', font=('Times New Roman', 10, 'bold'))
lab2.grid(row=2, column=0, sticky=E, pady=1)

partSpch_text = StringVar()
e2 = Entry(rWind1, width=13, textvariable=partSpch_text)
e2.grid(row=2, column=1, sticky=W)
#--------------------------------------------
lab3 = Label(rWind1, text='Plural : ',bg='#DCDCDC', font=('Times New Roman', 10, 'bold'))
lab3.grid(row=3, column=0,sticky=E)

plural_text = StringVar()
e3 = Entry(rWind1, width=40, textvariable=plural_text)
e3.grid(row=3, column=1, sticky=W)
#--------------------------------------------
lab4 = Label(rWind1, text='Past-Pl : ',bg='#DCDCDC', font=('Times New Roman', 10, 'bold'))
lab4.grid(row=4, column=0, sticky=E, pady=1)

pastPl_text = StringVar()
e4 = Entry(rWind1, width=40, textvariable=pastPl_text)
e4.grid(row=4, column=1, sticky=W)
#--------------------------------------------
lab5 = Label(rWind1, text='Definition : ',bg='#DCDCDC', font=('Times New Roman', 10, 'bold'))
lab5.grid(row=5, column=0, sticky=E)

definition_text = StringVar()
e5 = Entry(rWind1, width=46, textvariable=definition_text)
e5.grid(row=5, column=1, sticky=W)
#--------------------------------------------
lab6 = Label(rWind1, text='Example-1 : ',bg='#DCDCDC', font=('Times New Roman', 10, 'bold'))
lab6.grid(row=6, column=0, sticky=E, pady=1)

example1_text = StringVar()
e6 = Entry(rWind1, width=50, textvariable=example1_text)
e6.grid(row=6, column=1, sticky=W)
#--------------------------------------------
lab7 = Label(rWind1, text='Example-2 : ',bg='#DCDCDC', font=('Times New Roman', 10, 'bold'))
lab7.grid(row=7, column=0, sticky=E)

example2_text = StringVar()
e7 = Entry(rWind1, width=50, textvariable=example2_text)
e7.grid(row=7, column=1, sticky=W)
#--------------------------------------------
#------------------- The rWind2 frame with listbox list1-----------------------
sb1 = Scrollbar(rWind2a, orient=VERTICAL)
sb1.pack(side=LEFT, fill=Y, expand=1)
list1 = Listbox(rWind2a, width=65, height=18)
list1.pack(side=TOP)
list1.configure(yscrollcommand=sb1.set)
sb1.config(command=list1.yview)
sb2 = Scrollbar(rWind2a, orient=HORIZONTAL)
sb2.pack(side=TOP, fill=X, expand=1)
sb2.config(command=list1.xview)
list1.configure(xscrollcommand=sb2.set)
list1.bind('<<ListboxSelect>>', get_selected_row)
#---------------------------------------------------------------
butEd1=Button(rWind2b, text='View all\nentries',width=6,bg='#DCDCDC', command=view_command)
butEd1.pack(side=LEFT, padx=2)
butEd2=Button(rWind2b, text='Search\nentry',width=6,bg='#DCDCDC', command=search_command)
butEd2.pack(side=LEFT)
butEd3=Button(rWind2b, text='Add\nentry',width=6,bg='#DCDCDC', command=add_command)
butEd3.pack(side=LEFT, padx=2)
butEd4=Button(rWind2b, text='Update\nentry',width=6,bg='#DCDCDC', command=update_command)
butEd4.pack(side=LEFT)
butEd5=Button(rWind2b, text='Delete\nentry',width=6,bg='#DCDCDC', command = delete_command)
butEd5.pack(side=LEFT, padx=2)
butEd6=Button(rWind2b, text='New\nentry',width=6,bg='#DCDCDC', command=new_entry_command)
butEd6.pack(side=LEFT)
butEd7=Button(rWind2b, text='Clear all\nfields',width=6,bg='#DCDCDC', command=clear_fields)
butEd7.pack(side=LEFT)

fndWord = StringVar()
wordEntry = Entry(frame5, textvariable=fndWord, width=27, font=('Arial', '12'))
wordEntry.pack(side=TOP, padx=3, pady=4)

langBut = Button(frame5, text="DE➡EN", font=("Tahoma", 9, 'bold'), width=6, command=langensch_DEEN, relief='raised', bg='#FF8C00')
langBut.pack(side=LEFT, padx=2)
langBut2 = Button(frame5, text="EN➡GE", font=("Tahoma", 9, 'bold'), width=6, command=langensch_ENDE, relief='raised', fg='navy', bg='#FFA500') # ////////////////////////////////////////////
langBut2.pack(side=LEFT, padx=2) # ////////////////////////////////////////////////////////////////////
langBut3 = Button(frame5, text="DE➡GR", font=("Tahoma", 9, 'bold'), width=6, command=langensch_DEEN, relief='raised', fg='white', bg='#5F9EA0')
langBut3.pack(side=LEFT, padx=4)
langBut4 = Button(frame5, text="GR➡DE", font=("Tahoma", 9, 'bold'), width=6, command=langensch_ENDE, relief='raised', fg='white', bg='#4682B4') # ////////////////////////////////////////////
langBut4.pack(side=LEFT, padx=3) # ////////////////////////////////////////////////////////////////////


btnhide4 = Button(midWind3, text="", width=24, relief='flat', bg='#778899')
btnhide4.pack(side=BOTTOM, padx=10, pady=4)
btnhide5 = Button(midWind3, text="Example sentences ➡", font=('Arial', 12, 'bold'),width=24, relief='flat', bg='#778899')
btnhide5.pack(side=BOTTOM, padx=10, pady=4)
notesText = Text(midWind3, width=28, height=5, bg='black', fg='white', relief='sunken', bd='15')
notesText.pack(side=BOTTOM, padx=3, pady=9)

# ---------------- THE TEXTbox WIDGETS -----------------

textArea1 = ScrolledText(frame1, width=60, height=14, bd=2, padx=5, wrap=WORD) # for the Vocabulary
textArea3 = ScrolledText(frame3, width=60, height=14, bd=2, padx=5, wrap=WORD) # for the Text
textArea4 = ScrolledText(frame4, width=60, height=14, bd=2, padx=5, wrap=WORD) # for the Translation
dbtext = ScrolledText(rWind2c, width=50, height=8, wrap=WORD) # the textbox below the database

butTA2 = Button(frame2, text="  ADD THE WORDS TO THE 'FILTER'  ", font=('Italics', 10, 'bold'), bg='#87CEFA', command=append_to_known)
butTA2.grid(row=0,column=0, pady=5)
textArea2 = ScrolledText(frame2, width=30, height=18, bd=2) # for the right textbox
textArea2.grid(row=1, column=0, padx=3)
btnfr2 = Button(frame2, text="CLEAR", width=6, font=('Italics', 10, 'bold'), bg='#87CEFA', command=clear_unWords)
btnfr2.grid(row=2, column=0, sticky=W, pady=5)
btnfr2 = Button(frame2, text="SAVE", width=7, font=('Italics', 10, 'bold'), bg='#87CEFA', command=temp_save) # change command ////////////
btnfr2.grid(row=2, column=0, sticky=N, pady=5)
btnfr2 = Button(frame2, text="LOAD", width=6, font=('Italics', 10, 'bold'), bg='#87CEFA', command=load_unWords) # change command ////////////
btnfr2.grid(row=2, column=0, sticky=E, pady=5)
# ---------------- THE BUTTONS ---------------------------------

btn1 = Button(frame1a, text="", width=13, relief='flat', bg='#778899')
btn1.grid(row=1,column=3,pady=3)
btn2 = Button(frame1a, text="Update", width=13, command=lambda:save(voc_file_name)).grid(row=2,column=3)
btn3 = Button(frame1a, text="Save As",width=13, command=save_as).grid(row=3,column=3,pady=3)
btn4 = Button(frame1a, text="Clear",width=13, command=clear_VOC).grid(row=4,column=3,pady=3)
btnx = Button(frame1a, text=" EXIT ", width=13, font=('Tahoma',11,'bold'), fg='white', bg='#8B0000', relief='raised', command=exit_Progr)
btnx.grid(row=5, column=3)
btn2x = Button(frame1a, text="READ ME", width=13, bg='#008080', font=('Tahoma',11,'bold'), fg='white', relief='raised', command=read_me)
btn2x.grid(row=6, column=3, pady=3)

bt = [5,6,7,8,9,10,11,12,13]
for i in bt:
    btn=Button(frame3a, text="", width=13, relief='flat', bg='#778899').grid(row=i, column=3)
btnUnk = Button(frame3a, text="Create List of\nUnknown Words  ➡\n⬅       from TEXT", bg='#2E8B57',
                fg='white',width=17, font=('Tahoma', 8, 'bold'), command=mkList_unWords)
btnUnk.grid(row=6,column=3,pady=7)
btn1 = Button(frame3a, text="  LOAD  ", width=13, command=open_File, font=('Tahoma',11,'bold'), bg='#1E90FF', fg='white')
btn1.grid(row=7, column=3)
btn2 = Button(frame3a, text="Update", width=13, command=lambda:save(tex_file_name)).grid(row=8, column=3, pady=3)
btn3 = Button(frame3a, text="Save As",width=13, command=save_as).grid(row=9, column=3)
btn4 = Button(frame3a, text="Clear",width=13, command=clear_TEX).grid(row=10, column=3, pady=3)    
        
btn1 = Button(frame4a, text="NOTEBOOK", width=13, bg='#8B4513', command=notebook,font=('Tahoma',11,'bold'), fg='white')
btn1.grid(row=9, column=3)
btn2 = Button(frame4a, text="Update", width=13, command=lambda:save(ran_file_name)).grid(row=10, column=3, pady=5)
btn3 = Button(frame4a, text="Save As",width=13, command=save_as).grid(row=11, column=3)
btn4 = Button(frame4a, text="Clear",width=13, command=clear_RAN).grid(row=12, column=3,pady=5)
btnhide1 = Button(frame4a, text="", width=13, relief='flat', bg='#778899').grid(row=13, column=3) # ************ latest addition ******
btnhide2 = Button(frame4a, text="", width=13, relief='flat', bg='#778899').grid(row=14, column=3) # ************ latest addition ******
btnhide3 = Button(frame4a, text="", width=13, relief='flat', bg='#778899').grid(row=15, column=3) # ************ latest addition ******
textL = ['V','O','C','A','B','U','L','A','R','Y','','','T','E','X','T','', 'A','R','E','A','','','T','R','A','N','S','/','T','I','O','N','','','']
for item in textL:
    lab1 = Label(leftWind, text=item, font=('Arial',9,'bold'),fg='white', bg='navy').pack(side=TOP)

leftWind.grid(row=0, column=0) # the vertical bar
midWind1.grid(row=0, column=1, sticky=NW) # the larger windows: vocabulary, text, translation
midWind2.grid(row=0, column=2) # the buttons to download vocab, text, transl
midWind3.grid(row=0, column=3) # the textbox for unknown words, etc
rightWind.grid(row=0, column=4, sticky=NSEW)# the database
midWind3.grid(row=0, column=3) # the textbox for unknown words, etc
rightWind.grid(row=0, column=4, padx=2)# the database

frame1.grid(row=0, column=0) # for the Text Areas
frame3.grid(row=1, column=0)
frame4.grid(row=2, column=0)

frame1a.grid(row=0, column=0) # for the buttons
frame3a.grid(row=1, column=0)
frame4a.grid(row=2, column=0)

frame2.pack(side=TOP) # for the Textbox area
frame5.pack(side=TOP) # for Web-scrapping

textArea1.pack(side=TOP)
textArea3.pack(side=TOP, pady=5)
textArea4.pack(side=TOP)

rWind1.grid(row=0, column=0, sticky=W)
rWind2.grid(row=1, column=0, sticky=W)

rWind2a.pack(side=TOP)
rWind2b.pack(side=TOP)
rWind2c.pack(side=TOP)
dbtext.pack()

root.mainloop()
