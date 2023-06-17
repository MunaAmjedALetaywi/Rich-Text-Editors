from tkinter import *
from tkinter.ttk import *
from tkinter import font,colorchooser,filedialog,messagebox
from tkinter.ttk import Combobox
import os
import tkinter as tk
import tempfile
#from datetime import datetime 

#Functions Part
def toolbarFunction():
    if show_toolbar.get()==False:
        tool_bar.pack_forget()
    if show_toolbar.get()==True:
        textarea.pack_forget()
        tool_bar.pack(fill=X)
        textarea.pack(fill=BOTH,expand=1)

def statusbarFunction():
    if show_statusbar.get()==False:
        status_bar.pack_forget()
    else:
        status_bar.pack()

def change_theme(bg_color,fg_color):
    textarea.config(bg=bg_color,fg=fg_color)
    
#######################################################################################################
def select_word(event):
    # Get the index of the word at the cursor position
    index = textarea.index(INSERT + " wordstart")
    word_end = index + " wordend"
    # Add a tag to the selected word
    textarea.tag_add("sel", index, word_end)
    
def show_context_menu(event):
    # Check if a word is selected
    if textarea.tag_ranges("sel"):
        # Display the context menu at the mouse pointer's location
        context_menu.post(event.x_root, event.y_root)

def shade_text():
    # Get the current selection in the text area
    current_tags = textarea.tag_names("sel.first")
    # Otherwise, add the shading tag to the selected text
    textarea.tag_add("shaded", "sel.first", "sel.last")
    textarea.tag_config("shaded",foreground='black',background="black")


def remove_shade_text():
    # Get the starting and ending indices of the selected text
    start_index = textarea.index("sel.first")
    end_index = textarea.index("sel.last")

    # Remove the "shaded" tag from the selected text
    textarea.tag_remove("shaded", start_index, end_index)

def show_word_shaded():
    selected_text = textarea.selection_get()
    word_to_shade = selected_text.strip()
    messagebox.showinfo("Selected Word", word_to_shade)

#######################################################################################################
def find():
    def find_words():
        textarea.tag_remove('match',1.0,END)
        start_pos='1.0'
        word=findentryField.get()
        if word:
            while True: 
                start_pos=textarea.search(word,start_pos,stopindex=END) 
                if not start_pos:
                    break
                end_pos=f'{start_pos}+{len(word)}c' 
                textarea.tag_add('match',start_pos,end_pos)

                textarea.tag_config('match',foreground='red',background='yellow')
                start_pos=end_pos

    def replace_text():
        word = findentryField.get()
        replaceword = replaceentryField.get()
        content = textarea.get(1.0, END)
        new_content, count = content.replace(word, replaceword), content.count(word)
        textarea.delete(1.0, END)
        textarea.insert(1.0, new_content)
        start_pos = "1.0"
        while True:
            start_pos = textarea.search(word, start_pos, stopindex=END)
            if not start_pos:
                break
            end_pos = f"{start_pos}+{len(word)}c"
            textarea.tag_add("highlight", start_pos, end_pos)
            start_pos = end_pos
        messagebox.showinfo("Information", f"Replaced {count} occurrences of '{word}' with '{replaceword}'")
        start_pos = "1.0"
        while True:
            start_pos = textarea.search(replaceword, start_pos, stopindex=END)
            if not start_pos:
                break
            end_pos = f"{start_pos}+{len(replaceword)}c"
            textarea.tag_add("highlight", start_pos, end_pos)
            start_pos = end_pos
        textarea.tag_config("highlight", background="yellow")
    
    def remove_shade_word():
        textarea.tag_remove('match',1.0,END)

    def shade_word():
        remove_shade_word()
        start_pos='1.0'
        word=findentryField.get()
        if word:
            while True: 
                start_pos=textarea.search(word,start_pos,stopindex=END) #1.0
                if not start_pos:
                    break
                end_pos=f'{start_pos}+{len(word)}c' #1.0+1c
                textarea.tag_add('match',start_pos,end_pos)
                textarea.tag_config('match',foreground='black',background='black')
                start_pos=end_pos
    
        return textarea.get("1.0", "end-1c")

    def replace_select():
        word = findentryField.get()
        replaceword = combobox.get() 
        content = textarea.get(1.0, END)
        new_content, count = content.replace(word, replaceword), content.count(word)
        textarea.delete(1.0, END)
        textarea.insert(1.0, new_content)
        start_pos = "1.0"
        while True:
            start_pos = textarea.search(word, start_pos, stopindex=END)
            if not start_pos:
                break
            end_pos = f"{start_pos}+{len(word)}c"
            textarea.tag_add("highlight", start_pos, end_pos)
            start_pos = end_pos
        messagebox.showinfo("Information", f"Replaced {count} occurrences of '{word}' with '{replaceword}'")
        start_pos = "1.0"
        while True:
            start_pos = textarea.search(replaceword, start_pos, stopindex=END)
            if not start_pos:
                break
            end_pos = f"{start_pos}+{len(replaceword)}c"
            textarea.tag_add("highlight", start_pos, end_pos)
            start_pos = end_pos
        textarea.tag_config("highlight", background="yellow")


    root1=Tk()
    root1.title('Find')
    root1.geometry('450x250+500+200')
    root1.resizable(0,0)

    labelFrame=Label(root1)
    labelFrame.pack(pady=20)
    
    findLabel=Label(labelFrame,text='Find')
    findLabel.grid(row=0,column=0,padx=5,pady=5)
    findentryField=Entry(labelFrame)
    findentryField.grid(row=0,column=1,padx=5,pady=5)

    replaceLabel=Label(labelFrame,text='Replace')
    replaceLabel.grid(row=1,column=0,padx=5,pady=5)
    replaceentryField=Entry(labelFrame)
    replaceentryField.grid(row=1,column=1,padx=5,pady=5)

    select=Label(labelFrame, text='Select your state')
    select.grid(row=2,column=0,padx=5,pady=5)
    combobox = Combobox(labelFrame, values=['item1', 'item2', 'item3', 'item4'])
    combobox.grid(row=2,column=1,padx=5,pady=5)


    findButton=Button(labelFrame,text='FIND',command=find_words)
    findButton.grid(row=3,column=0,padx=2,pady=2)

    replaceButton = Button(labelFrame, text='REPLACE',command=replace_text)
    replaceButton.grid(row=3, column=1, padx=2, pady=2)

    shadingButton = Button(labelFrame, text='SHADING',command=shade_word)
    shadingButton.grid(row=3, column=2, padx=2, pady=2)

    shadingButton = Button(labelFrame, text='REMOVE SHADE',command=remove_shade_word)
    shadingButton.grid(row=4, column=0, padx=2, pady=2)

    selectgButton = Button(labelFrame, text='REPLACE SELECT',command=replace_select)
    selectgButton.grid(row=4, column=1, padx=2, pady=2)

    root1.mainloop()
        
#######################################################################################################
def statusBarFunc(event):
    if textarea.edit_modified():
        words=len(textarea.get(0.0,END).split())
        #print(words)
        characters=len(textarea.get(0.0,'end-1c').replace(' ','')) #1.0
        status_bar.config(text=f'Charecters: {characters} Words: {words}')

    textarea.edit_modified(False)
#######################################################################################################
url=''
def new_file(event):
    global url
    url=''
    textarea.delete(0.0,END)

def open_file():
    global url
    url=filedialog.askopenfilename(initialdir=os.getcwd,title='Select File',filetypes=(('Text File','txt'),
                                                                                     ('All Files','*.*')))
    if url != '':
        data=open(url,'r')
        textarea.insert(0.0,data.read())
    root.title(os.path.basename(url))

def save_file(event=None):
    if url =='':
        save_url=filedialog.asksaveasfile(mode='w',defaultextension='.txt',filetypes=(('Text File','txt'),
                                                                             ('All Files','*.*')))
        if save_url is None:
            pass
        else:
            content=textarea.get(0.0,END)
            save_url.write(content)
            save_url.close()

    else:
        content=textarea.get(0.0,END)
        file=open(url,'w')
        file.write(content)

    

def saveas_file(event=None):
    save_url = filedialog.asksaveasfile(mode='w', defaultextension='.txt', filetypes=(('Text File', 'txt'),
                                                                                      ('All Files', '*.*')))
    content = textarea.get(0.0, END)
    save_url.write(content)
    save_url.close()
    if url !='':
        os.remove(url)

def exit_file(event=None):
    if textarea.edit_modified():
        result=messagebox.askyesnocancel('Warning','Do you want to save the file?')
        if result is True:
            if url!='':
                content=textarea.get(0.0,END)
                file=open(url,'w')
                file.write(content)
                root.destroy()
            else:
                content=textarea.get(0.0,END)
                save_url = filedialog.asksaveasfile(mode='w', defaultextension='.txt', filetypes=(('Text File', 'txt'),
                                                                                                  ('All Files', '*.*')))
                save_url.write(content)
                save_url.close()
                root.destroy()

        elif result is False:
            root.destroy()
        else:
            pass
    else:
        root.destroy()

#######################################################################################################
fontSize=12
fontStyle='arial'
def font_style(event):
    global fontStyle
    fontStyle=font_family_variables.get()
    textarea.config(font=(fontStyle,fontSize))

def font_size(event):
    global fontSize

    sel_start = textarea.index("sel.first")
    sel_end = textarea.index("sel.last")
    tags = textarea.tag_names(sel_start)
    fontSize = size_variable.get()

    if "selected" in tags:
        textarea.tag_configure("selected", font=(fontStyle, fontSize))
    else:
        textarea.tag_add("selected", sel_start, sel_end)
        textarea.tag_configure("selected", font=(fontStyle, fontSize))


def bold_text():
    # Get the selected text and its properties
    sel_start = textarea.index("sel.first")
    sel_end = textarea.index("sel.last")
    tags = textarea.tag_names(sel_start)

    # Toggle the boldness of the selected text
    if "bold" not in tags:
        textarea.tag_add("bold", sel_start, sel_end)
        textarea.tag_configure("bold", font=(fontStyle, fontSize, 'bold'))
    else:
        textarea.tag_remove("bold", sel_start, sel_end)
        if "sel" in tags:
            textarea.tag_configure("sel", font=(fontStyle, fontSize, 'normal'))


def italic_text():
    # Get the selected text and its properties
    sel_start = textarea.index("sel.first")
    sel_end = textarea.index("sel.last")
    tags = textarea.tag_names(sel_start)

    # Toggle the italic style of the selected text
    if "italic" not in tags:
        textarea.tag_add("italic", sel_start, sel_end)
        textarea.tag_configure("italic", font=(fontStyle, fontSize, 'italic'))
    else:
        textarea.tag_remove("italic", sel_start, sel_end)
        if "sel" in tags:
            textarea.tag_configure("sel", font=(fontStyle, fontSize, 'normal'))
        

def underline_text():
    # Get the selected text and its properties
    sel_start = textarea.index("sel.first")
    sel_end = textarea.index("sel.last")
    tags = textarea.tag_names(sel_start)

    # Toggle the underline style of the selected text
    if "underline" not in tags:
        textarea.tag_add("underline", sel_start, sel_end)
        textarea.tag_configure("underline", font=(fontStyle, fontSize, 'underline'))
    else:
        textarea.tag_remove("underline", sel_start, sel_end)


def color_select():
    sel_start = textarea.index("sel.first")
    sel_end = textarea.index("sel.last")
    color = colorchooser.askcolor()

    if color[1] is not None:
        textarea.tag_add("selected", sel_start, sel_end)
        textarea.tag_configure("selected", foreground=color[1])
    

def align_right():
    # Get the selected text
    sel_start = textarea.index("sel.first")
    sel_end = textarea.index("sel.last")

    # Add a new tag for right alignment
    textarea.tag_add("right", sel_start, sel_end)
    textarea.tag_config("right", justify=RIGHT)

    # Remove any existing alignment tags and apply the new tag to the selected text
    for tag in ["left", "center", "right"]:
        textarea.tag_remove(tag, sel_start, sel_end)
    textarea.tag_add("right", sel_start, sel_end)


def align_left():
    # Get the selected text
    sel_start = textarea.index("sel.first")
    sel_end = textarea.index("sel.last")

    # Add a new tag for left alignment
    textarea.tag_add("left", sel_start, sel_end)
    textarea.tag_config("left", justify=LEFT)

    # Remove any existing alignment tags and apply the new tag to the selected text
    for tag in ["left", "center", "right"]:
        textarea.tag_remove(tag, sel_start, sel_end)
    textarea.tag_add("left", sel_start, sel_end)


def align_center():
    # Get the selected text
    sel_start = textarea.index("sel.first")
    sel_end = textarea.index("sel.last")

    # Add a new tag for center alignment
    textarea.tag_add("center", sel_start, sel_end)
    textarea.tag_config("center", justify=CENTER)

    # Remove any existing alignment tags and apply the new tag to the selected text
    for tag in ["left", "center", "right"]:
        textarea.tag_remove(tag, sel_start, sel_end)
    textarea.tag_add("center", sel_start, sel_end)


#######################################################################################################
root = Tk()
root.title("Rich Text Editor")
root.geometry('1200x620+10+10')
root.resizable(False,False)
menubar = Menu(root)
root.config(menu=menubar)

#File Menu
#######################################################################################################
filemenu =Menu(menubar,tearoff=False)
menubar.add_cascade(label='File',menu=filemenu)
newImage = PhotoImage(file='C:\\Users\\user\\Documents\\vs code file\\icons\\add.png')
openImage =PhotoImage(file='C:\\Users\\user\\Documents\\vs code file\\icons\\open-folder.png')
saveImage =PhotoImage(file='C:\\Users\\user\\Documents\\vs code file\\icons\\saveFile.png')
saveAsImage =PhotoImage(file='C:\\Users\\user\\Documents\\vs code file\\icons\\saveAs.png')
exitImage =PhotoImage(file='C:\\Users\\user\\Documents\\vs code file\\icons\\Exit1.png')


filemenu.add_command(label='New',accelerator='Ctrl+N',image=newImage,compound=LEFT,command=new_file)
filemenu.add_command(label='Open',accelerator='Ctrl+O',image=openImage,compound=LEFT,command=open_file)
filemenu.add_command(label='Save',accelerator='Ctrl+S',image=saveImage,compound=LEFT,command=save_file)
filemenu.add_command(label='Save As',accelerator='Ctrl+Alt+S',image=saveAsImage,compound=LEFT,command=saveas_file)
filemenu.add_separator()
filemenu.add_command(label='Exit',accelerator='Ctrl+Q',image=exitImage,compound=LEFT,command=exit_file)
#######################################################################################################

#Toolbar
tool_bar = Label(root)
tool_bar.pack(side=TOP,fill=X)

#Butons
#Bold
boldImage=PhotoImage(file='C:\\Users\\user\\Documents\\vs code file\\icons\\bold1.png')
boldButton=Button(tool_bar,image=boldImage,command=bold_text)
boldButton.grid(row=0,column=0,padx=5)
#italic 
italicImage=PhotoImage(file='C:\\Users\\user\\Documents\\vs code file\\icons\\italic.png')
italicButton=Button(tool_bar,image=italicImage,command=italic_text)
italicButton.grid(row=0,column=1,padx=5)
#Underline
underlineImage=PhotoImage(file='C:\\Users\\user\\Documents\\vs code file\\icons\\underline.png')
underlineButton=Button(tool_bar,image=underlineImage,command=underline_text)
underlineButton.grid(row=0,column=2,padx=5)

#Lift Align
liftAlignImage=PhotoImage(file='C:\\Users\\user\\Documents\\vs code file\\icons\\left-align.png')
liftAlignButton=Button(tool_bar,image=liftAlignImage,command=align_left)
liftAlignButton.grid(row=0,column=3,padx=5)
#center Align
centerAlignImage=PhotoImage(file='C:\\Users\\user\\Documents\\vs code file\\icons\\center-align.png')
centerAlignButton=Button(tool_bar,image=centerAlignImage,command=align_center)
centerAlignButton.grid(row=0,column=4,padx=5)
#Right Align
rightAlignImage=PhotoImage(file='C:\\Users\\user\\Documents\\vs code file\\icons\\right-align.png')
rightAlignButton=Button(tool_bar,image=rightAlignImage,command=align_right)
rightAlignButton.grid(row=0,column=5,padx=5)

#Font Color
fontColorImage=PhotoImage(file='C:\\Users\\user\\Documents\\vs code file\\icons\\font_color.png')
fontColorButton=Button(tool_bar,image=fontColorImage,command=color_select)
fontColorButton.grid(row=0,column=6,padx=5)
#Font Families
font_families= font.families()
font_family_variables=StringVar()
fontfamily_Combobox =Combobox(tool_bar,width=30,values=font_families,state='readonly',textvariable=font_family_variables)
fontfamily_Combobox.current(font_families.index('Arial'))
fontfamily_Combobox.grid(row=0,column=7,padx=5)
#Font Size 
size_variable = IntVar()
font_size_Combobox=Combobox(tool_bar,width=14,textvariable=size_variable,state='readonly',values=tuple(range(8,81)))
font_size_Combobox.current(4)
font_size_Combobox.grid(row=0,column=8,padx=5)

fontfamily_Combobox.bind('<<ComboboxSelected>>',font_style)
font_size_Combobox.bind('<<ComboboxSelected>>',font_size)

#######################################################################################################
#Text Area & Scrollbar
scrollbar=Scrollbar(root)
scrollbar.pack(side=RIGHT,fill=Y)
textarea=Text(root,yscrollcommand=scrollbar.set,font=('arial',12))
textarea.pack(fill=BOTH,expand=True)
scrollbar.config(command=textarea.yview)


# Create a context menu
context_menu = Menu(root, tearoff=0)
context_choice = StringVar()
radio1 = Radiobutton()
context_menu.add_radiobutton(label="Shading", variable=context_choice, command=shade_text)
context_menu.add_radiobutton(label="Remove Shading", variable=context_choice, command=remove_shade_text)
context_menu.add_radiobutton(label="Show the word", variable=context_choice,command=show_word_shaded)


# Bind the show_context_menu function to the mouse click event
textarea.bind("<ButtonRelease-1>", show_context_menu)


#######################################################################################################
#Status Bar
status_bar=Label(root,text='Status Bar')
status_bar.pack(side=BOTTOM)

textarea.bind('<<Modified>>',statusBarFunc)

#######################################################################################################
#Edit Menu
editmenu=Menu(menubar,tearoff=False)
menubar.add_cascade(label='Edit',menu=editmenu)
cutImage = PhotoImage(file='C:\\Users\\user\\Documents\\vs code file\\icons\\cut.png')
CopyImage =PhotoImage(file='C:\\Users\\user\\Documents\\vs code file\\icons\\copy.png')
PasteImage =PhotoImage(file='C:\\Users\\user\\Documents\\vs code file\\icons\\paste.png')
ClearImage =PhotoImage(file='C:\\Users\\user\\Documents\\vs code file\\icons\\clear_all.png')
FindImage =PhotoImage(file='C:\\Users\\user\\Documents\\vs code file\\icons\\find.png')


editmenu.add_command(label='Cut',accelerator='Ctrl+X',image=cutImage,compound=LEFT,
                     command=lambda :textarea.event_generate('<Control x>'))
editmenu.add_command(label='Copy',accelerator='Ctrl+C',image=CopyImage,compound=LEFT,
                     command=lambda :textarea.event_generate('<Control c>'))
editmenu.add_command(label='Paste',accelerator='Ctrl+V',image=PasteImage,compound=LEFT,
                     command=lambda :textarea.event_generate('<Control v>'))
editmenu.add_command(label='Clear',accelerator='Ctrl+Alt+X',image=ClearImage,compound=LEFT,
                     command=lambda :textarea.delete(0.0,END))
editmenu.add_command(label='Find Or Replace',accelerator='Ctrl+F',image=FindImage,compound=LEFT,command=find)

#######################################################################################################
#View Menu
show_toolbar = BooleanVar()
show_statusbar = BooleanVar()
toolImage = PhotoImage(file='C:\\Users\\user\\Documents\\vs code file\\icons\\tool_bar.png')
statusImage = PhotoImage(file='C:\\Users\\user\\Documents\\vs code file\\icons\\status_bar.png')
viewmenu=Menu(menubar,tearoff=False)
viewmenu.add_checkbutton(label='Tool Bar',variable=show_toolbar,onvalue=True,offvalue=False,image=toolImage,compound=LEFT,
                         command= toolbarFunction)
show_toolbar.set(True)
viewmenu.add_checkbutton(label='Status Bar',variable=show_statusbar,onvalue=True,offvalue=False,image=statusImage,compound=LEFT,
                         command=statusbarFunction)
show_statusbar.set(True)
menubar.add_cascade(label='View',menu=viewmenu)
#######################################################################################################
#Themes Menu
themesmenu=Menu(menubar,tearoff=False)
menubar.add_cascade(label='Themes',menu=themesmenu)
themes_choice=StringVar()
lightImage=PhotoImage(file='C:\\Users\\user\\Documents\\vs code file\\icons\\light_default.png')
darkImage=PhotoImage(file='C:\\Users\\user\\Documents\\vs code file\\icons\\dark.png')
redImage=PhotoImage(file='C:\\Users\\user\\Documents\\vs code file\\icons\\red.png')
monokaiImage=PhotoImage(file='C:\\Users\\user\\Documents\\vs code file\\icons\\monokai.png')

themesmenu.add_radiobutton(label='Light Default',image=lightImage,variable=themes_choice,compound=LEFT,
                           command=lambda :change_theme('white','black'))
themesmenu.add_radiobutton(label='Dark',image=darkImage,variable=themes_choice,compound=LEFT,
                           command=lambda :change_theme('gray20','white'))
themesmenu.add_radiobutton(label='Pink',image=redImage,variable=themes_choice,compound=LEFT,
                           command=lambda :change_theme('pink','blue'))
themesmenu.add_radiobutton(label='Monokai',image=monokaiImage,variable=themes_choice,compound=LEFT,
                           command=lambda :change_theme('orange','white'))
#######################################################################################################


root.bind("<Control-o>",open_file)
root.bind("<Control-n>",new_file)
root.bind("<Control-s>",save_file)
root.bind("<Control-Alt-s>",saveas_file)
root.bind("<Control-q>",exit)

root.mainloop()