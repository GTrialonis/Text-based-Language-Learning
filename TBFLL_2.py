from tkinter import filedialog, END, messagebox, simpledialog
from tkinter import *
from tkinter.scrolledtext import *
from ftfy import fix_encoding

# FUNCTIONS

def doNothing():
    print("I do nothing")

def newFile():
    if len(textArea1.get('1.0', END+'-1c')) > 0:
        if messagebox.askyesno("Save?", "Do you want to save?"):
            saveFile()
        else:
            textArea1.delete('1.0', END)
            
def openFile():
    textArea1.delete('1.0', END)
    file = filedialog.askopenfile(parent=root, mode='rb', title='Select a text file',filetypes=(('Text file', '*.txt'), ('All files', '*.*')))
    
    if file != None:
        contents = file.read()
        textArea1.insert('1.0', contents.decode('utf-8'))
        file.close()

def saveasFile():
    file = filedialog.asksaveasfile(mode='wb')

    if file != None:
        # slice off the last character from get, as an extra return(enter) is added
        data = textArea1.get('1.0', END+'-1c')
        file.write(data.encode("utf-8"))
        file.close()
        
# Root for main window
root = Tk()
root.title("Text-based Language Learning Tool")

frame1 = Frame(root) # for Text Area 1
frame2 = Frame(root) # for Text Area 2
frame3 = Frame(root) # for Label

textArea1 = ScrolledText(frame1, width=80, height=20)
textArea2 = ScrolledText(frame2, width=80, height=20)
label1 = Label(frame3, text="Test Area below")
    
frame1.grid(row=0, column=0, padx=10, pady=10)
frame2.grid(row=0, column=1, padx=7)
frame3.grid(row=1, column=0, columnspan=2)

textArea1.grid(row=0, column=0)
textArea2.grid(row=0, column=1)
label1.pack(side=LEFT)

# Adding Menus
menu = Menu(root)
root.config(menu=menu)
subMenu = Menu(menu)
menu.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="New File", command=newFile)
subMenu.add_separator()
subMenu.add_command(label="Open", command=openFile)
subMenu.add_command(label="Save as..", command=saveasFile)
subMenu.add_command(label="Save", command=doNothing)
subMenu.add_command(label="Print", command=doNothing)
subMenu.add_separator()
subMenu.add_command(label="Exit", command=doNothing)

root.mainloop()
