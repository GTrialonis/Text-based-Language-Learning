from tkinter import filedialog, re
from tkinter import *
from tkinter import messagebox
from tkinter.scrolledtext import *
##import testmodule_5b

input_Value = ''' '''
contents = ''' '''


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

def taketest():
    import testengger_5b
##    from testengger_5b import openfile, translatethis, enter_transl
    
# Root for main window
root = Tk()
root.title("Text-based Language Learning Tool")
root.configure(background='#E6E6FA')

frame1 = Frame(root) # for Text Area 1
frame2 = Frame(root) # for Text Area 2
##frame3 = Frame(root) # for Label
##frame4 = Frame(root) # for Test Area

btn1 = Button(root, text="Make list of unknown words from text below",
              bg='#E5FFCC', command=lambda: mkList_unWords())
btn2 = Button(root, text="Clear text below", bg='#CCFFCC', command=clear_Text)
btn4 = Button(root, text="Take a Test", fg='white', bg='#006633', command=taketest)
btn3 = Button(root, text="Clear list below", bg='#CCFFCC', command=clear_unWords)

textArea1 = ScrolledText(frame1, width=80, height=20, bd=2, padx=5, wrap=WORD)
textArea2 = ScrolledText(frame2, width=80, height=20, bd=2, padx=5, wrap=WORD)
##label1 = Label(frame3, text="Test Area below")
##textArea3 = ScrolledText(frame4, width = 160, height=10, bd=3, padx=5, pady=5, wrap=WORD)

frame1.grid(row=0, column=0, padx=10, pady=30)
frame2.grid(row=0, column=1, padx=7)
##frame3.grid(row=1, column=0, columnspan=2)
##frame4.grid(row=2, column=0, columnspan=2)

textArea1.grid(row=0, column=0)
textArea2.grid(row=0, column=1)
btn1.place(x=115, y=2)
btn2.place(x=363, y=2)
btn3.place(x=750, y=2)
btn4.place(x=460, y=2)
##label1.pack(side=LEFT)
##textArea3.pack(side=LEFT)

# Adding Menus
menu = Menu(root)
root.config(menu=menu)
subMenu = Menu(menu)
menu.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Open .txt File", command=open_txt_File)
subMenu.add_separator()
# subMenu.add_command(label="Save", command=doNothing)
subMenu.add_command(label="Save as..", command=save_As_File)
subMenu.add_command(label="Print", command=doNothing)
subMenu.add_separator()
subMenu.add_command(label="Retrieve", command=retrieveInput)
subMenu.add_command(label="Exit", command=exit_Progr)


root.mainloop()


