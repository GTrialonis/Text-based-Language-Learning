from tkinter import filedialog,re
from tkinter import *
import requests
from bs4 import BeautifulSoup
import os
import tkinter.messagebox
from tkinter.scrolledtext import *

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
##                        textArea1.insert(END, word+' = '+'\n') # ---- ADDED RECENTLY TO TEST EFFECTIVENESS -----
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
# -------------------- TEMPORARY SAVE WORDS from TextArea 2 -----------------------------------------------------
def temp_save():
    with open('C:\\Users\\user\\Desktop\\SAVE THESE\\temporary_save.txt', 'w+', encoding='utf-8') as temp_file:
        temp_file.write(textArea2.get("1.0", END))
                
# -----------------------------------------------------------------------------                     
def clear_unWords():
    tkinter.messagebox.showwarning("Save?", "Are you sure?")
    textArea2.delete('1.0', END)


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
    
    
    notesText.delete('1.0', END)
    
    lemma = fndWord.get()
    headers = {"Referer" : "TbLLT School of Languages"}
    url = "https://de.langenscheidt.com/deutsch-englisch/"+lemma
    
    try:
        response = requests.get(url, headers=headers).text
        soup = BeautifulSoup(response, "lxml")
        # ----- the code below is for the searched word ----
        summary = soup.find('div', class_='summary-inner').text
        words = summary.replace('Weitere Beispiele...', '')
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
            rpl = art_plu.replace(trr, 't/v, irregulär, <kein ge->')
        elif art_plu.startswith(ivn):
            rpl = art_plu.replace(ivn, 'i/v')
        elif art_plu.startswith(irr):
            rpl = art_plu.replace(irr, 'i/v, irregulär')
        elif art_plu.startswith(ttv):
            rpl = art_plu.replace(ttv, 't/v, separabletrennb; -ge-;')
        else:
            rpl = art_plu
        
        lemma = lemma+', '+rpl
        textArea1.insert(END, lemma+' = ')
        textArea1.insert(END, myStr+'\n')
        lemma = ''
        myStr = ''
    except:
        notesText.insert(END, 'Word not found! Please check\nspelling and try again, or\nsearch another dictionary.')
        
# --------------------------------- ENGLISH - GERMAN -----------------------------------
def langensch_ENDE():
    notesText.delete('1.0', END)
    
    lemma = fndWord.get()
    headers = {"Referer" : "TbLLT School of Languages"}
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

        # ---------------------------------------------------------------
        # ---- for the article / genitive / transitive, intransitive verbs / plural of the word above ----
##        lemma = lemma+', '+rpl
        
        textArea1.insert(END, lemma+' = ')
        textArea1.insert(END, myStr+'\n')
        lemma = ''
        myStr = ''
    except:
        notesText.insert(END, 'Word not found! Please check\nspelling and try again, or\nsearch another dictionary.')

# -------------------------------------------------------------------------------------------------------------------
# Root for main window
root = Tk()
root.title("TbLLT: Text-based Language Learning Tool")
root.geometry('1200x700+10+10')
root.state('zoomed')
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
leftWind=Frame(root, width=35, bg='navy') # for bar,
midWind1=Frame(root, width=700, bg='#B0C4DE') # for Vocab., Text, Translation areas
midWind2=Frame(root, width=55, bg='#B0C4DE') # for the buttons
midWind3=Frame(root, width=100, bg='#B0C4DE') # for the textbox, unknown words
rightWind= Frame(root, width=200, bg='#B0C4DE') # for the database
# -------------- CHILD FRAMES ---------------------
frame1 = Frame(midWind1) # for the Vocabulary, row,col = 0, 0
frame3 = Frame(midWind1) # for the Text, row,col = 1,0
frame4 = Frame(midWind1) # for the Translation, row,col = 2,0
#----------------------------------------------
frame1a= Frame(midWind2, bg='#B0C4DE') # for the buttons, row, col = 0,1
frame3a= Frame(midWind2, bg='#B0C4DE') # for the buttons, row, col = 1,1
frame4a= Frame(midWind2, bg='#B0C4DE') # for the buttons, row, col = 2,1
#-------------- The Texttbox andWeb-Scrapping Frames ---------------
frame2 = Frame(midWind3, bg='#B0C4DE') # for Textbox
frame5 = Frame(midWind3, bg='#B0C4DE') # for Webscraping
langDict = Label (frame5, text="Search an online Dictionary", font=("Tahoma", 10, 'bold'), bg='#B0C4DE')
langDict.pack(side=TOP, padx=10, pady=5)

fndWord = StringVar()
wordEntry = Entry(frame5, textvariable=fndWord, width=30, font=('Arial', '12'))
wordEntry.pack(side=TOP, padx=10, pady=4)

langBut = Button(frame5, text="GER ➡ ENG", font=("Tahoma", 10, 'bold'), command=langensch_DEEN, width=11, relief='raised', bg='#FF8C00')
langBut.pack(side=LEFT, padx=11)
langBut2 = Button(frame5, text="ENG ➡ GER", font=("Tahoma", 10, 'bold'), command=langensch_ENDE, width=11, fg='white', bg='#0066CC') # ////////////////////////////////////////////
langBut2.pack(side=RIGHT, padx=11) # ////////////////////////////////////////////////////////////////////
btnhide4 = Button(midWind3, text="", width=24, relief='flat', bg='#B0C4DE')
btnhide4.pack(side=BOTTOM, padx=10, pady=4)
btnhide5 = Button(midWind3, text="", width=24, relief='flat', bg='#B0C4DE')
btnhide5.pack(side=BOTTOM, padx=10, pady=4)
notesText = Text(midWind3, width=30, height=6, bg='black', fg='white', relief='sunken', bd='15')
notesText.pack(side=BOTTOM, padx=10, pady=9)

# ---------------- THE TEXTbox WIDGETS -----------------

textArea1 = ScrolledText(frame1, width=70, height=13, bd=2, padx=5, wrap=WORD) # for the Vocabulary
textArea3 = ScrolledText(frame3, width=70, height=14, bd=2, padx=5, wrap=WORD) # for the Text
textArea4 = ScrolledText(frame4, width=70, height=14, bd=2, padx=5, wrap=WORD) # for the Translation

butTA2 = Button(frame2, text="  ADD THE WORDS TO THE 'FILTER'  ", font=('Italics', 10, 'bold'), bg='#87CEFA', command=append_to_unknown)
butTA2.grid(row=0,column=0, pady=5)
textArea2 = ScrolledText(frame2, width=30, height=18, bd=2) # for the right textbox
textArea2.grid(row=1, column=0)
btnfr2 = Button(frame2, text="CLEAR", width=6, font=('Italics', 10, 'bold'), bg='#87CEFA', command=clear_unWords)
btnfr2.grid(row=2, column=0, sticky=W, pady=5)
btnfr2 = Button(frame2, text="SAVE", width=7, font=('Italics', 10, 'bold'), bg='#87CEFA', command=clear_unWords) # change command ////////////
btnfr2.grid(row=2, column=0, sticky=N, pady=5)
btnfr2 = Button(frame2, text="LOAD", width=6, font=('Italics', 10, 'bold'), bg='#87CEFA', command=clear_unWords) # change command ////////////
btnfr2.grid(row=2, column=0, sticky=E, pady=5)
# ---------------- THE BUTTONS ---------------------------------

btn1 = Button(frame1a, text="⬅ Load VOCab.", width=13, command=open_File).grid(row=1,column=3,pady=3)
btn2 = Button(frame1a, text="Update", width=13, command=lambda:save(voc_file_name)).grid(row=2,column=3)
btn3 = Button(frame1a, text="Save As",width=13, command=save_as).grid(row=3,column=3,pady=3)
btn4 = Button(frame1a, text="Clear",width=13, command=clear_VOC).grid(row=4,column=3,pady=3)
btnx = Button(frame1a, text="EXIT Program", width=13, fg='white', bg='#8B0000', relief='raised', command=exit_Progr).grid(row=5, column=3)
btn2x = Button(frame1a, text="READ ME", width=13, bg='#008080', fg='white', relief='raised', command=read_me).grid(row=6, column=3, pady=3)

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
btnhide1 = Button(frame4a, text="", width=13, relief='flat', bg='#B0C4DE').grid(row=13, column=3) # ************ latest addition ******
btnhide2 = Button(frame4a, text="", width=13, relief='flat', bg='#B0C4DE').grid(row=14, column=3) # ************ latest addition ******
btnhide3 = Button(frame4a, text="", width=13, relief='flat', bg='#B0C4DE').grid(row=15, column=3) # ************ latest addition ******



textL = ['V','O','C','A','B','U','L','A','R','Y','','','T','E','X','T','', 'A','R','E','A','','','T','R','A','N','S','/','T','I','O','N','','','']
for item in textL:
    lab1 = Label(leftWind, text=item, font=('Arial',9,'bold'),fg='white', bg='navy').pack(side=TOP)

leftWind.grid(row=0, column=0) # the vertical bar
midWind1.grid(row=0, column=1, sticky=NW) # the larger windows: vocabulary, text, translation
midWind2.grid(row=0, column=2) # the buttons to download vocab, text, transl
midWind3.grid(row=0, column=3) # the textbox for unknown words, etc
rightWind.grid(row=0, column=4)# the database

frame1.grid(row=0, column=0) # for the Text Areas
frame3.grid(row=1, column=0)
frame4.grid(row=2, column=0)

frame1a.grid(row=0, column=0) # for the buttons
frame3a.grid(row=1, column=0)
frame4a.grid(row=2, column=0)

frame2.pack(side=TOP) # for the Textbox area
frame5.pack(side=TOP) # for Web-scrapping

textArea1.pack(side=TOP)
textArea3.pack(side=TOP, pady=7)
textArea4.pack(side=TOP)




root.mainloop()
