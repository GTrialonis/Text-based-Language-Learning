from tkinter import filedialog, sys, END, re
from tkinter import *
from tkinter.scrolledtext import *

input_Value = ''' '''

# FUNCTIONS
def doNothing():
    pass

def open_txt_File():
    root.filename = filedialog.askopenfilename(initialdir='/', title='Select File',
                                    defaultextension='txt', filetypes=(('Text Files ', '*.txt'), ('All Files ', '*.*')))
    with open(root.filename, encoding='UTF-8') as file:
        contents = file.readlines() # this is the study file, referenced as 'text' below
        contents = ''.join(contents) # the study file, again
        textArea1.insert('1.0', contents) # opened file and placed inside textArea1
        
    # Program starts to find unknown words from opened file above. The file is
        # 'filtered' through 'known_words.txt' below.

    text = re.findall(r'\w+', contents) # contents of opened file are stripped of
            # punctuation, changed to a list and placed in variable 'text'.
            # This is the study file processed, or changed.
            
    # The operation below acts as filter of the opened file (now referenced as 'text')      
    with open('known_words.txt', encoding='UTF-8') as file:
        kn_wrds = file.read() # it reads the content of file 'known_words'
        mySet = set(text) # this converts the list of file 'text' to a set
                # This operation removes double (and more) occurences of words
        finList =  list(mySet) # back to a list
        for word in finList: # refence to 'word' in the 'text' file (the study file)
            if word not in kn_wrds:
                textArea2.insert(END, word+' = '+'\n')
                
# Let's retrieve PASTED study text from textArea1
def retrieveInput():
    global input_Value
    input_Value = textArea1.get('1.0', 'end-1c') # a string is generated
    

# Let's write the retrieved text in a file somewhere
def save_As_File():
    root.filename = filedialog.asksaveasfilename(initialdir = "/", defaultextension='.txt',
                filetypes = (("all files","*.*"),("jpeg files","*.jpg")))
    with open(root.filename, 'w', encoding='utf-8') as txt_file:
        txt_file.write(textArea1.get('1.0', END))
    
    
# Root for main window
root = Tk()
root.title("Text-based Language Learning Tool")

frame1 = Frame(root) # for Text Area 1
frame2 = Frame(root) # for Text Area 2
frame3 = Frame(root) # for Label

btn1 = Button(root, text="Make list of unknown words from text below",
              bg='#E5FFCC', command=lambda: doNothing())
btn2 = Button(root, text="Clear text below", bg='#CCFFCC')
textArea1 = ScrolledText(frame1, width=80, height=20, bd=2, padx=5, wrap=WORD)
textArea2 = ScrolledText(frame2, width=80, height=20, bd=2, padx=5, wrap=WORD)
label1 = Label(frame3, text="Test Area below")
    
frame1.grid(row=0, column=0, padx=10, pady=30)
frame2.grid(row=0, column=1, padx=7)
frame3.grid(row=1, column=0, columnspan=2)

textArea1.grid(row=0, column=0)
textArea2.grid(row=0, column=1)
btn1.place(x=130, y=2)
btn2.place(x=410, y=2)
label1.pack(side=LEFT)

# Adding Menus
menu = Menu(root)
root.config(menu=menu)
subMenu = Menu(menu)
menu.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Open .txt File", command=open_txt_File)
subMenu.add_separator()
subMenu.add_command(label="Save", command=doNothing)
subMenu.add_command(label="Save as..", command=save_As_File)
subMenu.add_command(label="Print", command=doNothing)
subMenu.add_separator()
subMenu.add_command(label="Retrieve", command=retrieveInput)
subMenu.add_command(label="Exit", command=doNothing)

root.mainloop()
