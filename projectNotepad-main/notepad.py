from tkinter import *
from tkinter import messagebox,ttk,font,filedialog,colorchooser
from PIL import ImageTk,Image
from os import getcwd

root = Tk()
root.geometry('800x600')
root.title('Notepad')
num = 1
current_open_file = ''
def new(event = None):
    global num

    root.title(f'{getcwd()}\\untitled{num}-Notepad')
    text_area.delete("1.0", END)
    current_open_file =f'{getcwd()}\\untitled{num}'
    num+=1
def Open(event = None):
    global current_open_file 
    
    f = filedialog.askopenfile(title = 'Select file to open')
    if f !=None:
        text_area.delete("1.0", END)
        text_area.insert(END,f.read())
        root.title(f'{f.name}-Notepad')
        current_open_file = f'{f.name}'

        f.close()


def save(event = None):
    global current_open_file

    if current_open_file:
        content = str(text_area.get(1.0, END))

        fw=open(rf'{current_open_file}','w')
        fw.write(content)
        fw.close()
    else:
        save_as()



def save_as(event = None):
    f = filedialog.asksaveasfile(title = 'Save As',mode = 'w',defaultextension = '.txt')
    if f !=None:
        current_open_file = f.name

        f.write(text_area.get('1.0',END))
        f.close()
def cut():
    text_area.event_generate(('<<Cut>>'))
def copy():
    text_area.event_generate(('<<Copy>>'))
def paste():
    text_area.event_generate(('<<Paste>>'))
def select_all():
    text_area.tag_add(SEL, "1.0", END)

def fontfun(n):
    if n ==0:
        text_area.configure(font = font.BOLD)
    elif n ==1:
        text_area.configure(font = font.ITALIC)

def colorfont():
    msg=messagebox.askyesnocancel('color selector','for background color selection select yes and for foreground select no')

    if msg ==False:
        color = colorchooser.askcolor()
        text_area['fg'] = color[1]
    elif msg ==True:
        color = colorchooser.askcolor()
        text_area['bg'] =color[1]
    else:
        pass


def _help():
    messagebox.showinfo('help','gui text pad for more info googled it')

def Quit():
    msg = messagebox.askyesnocancel('Quit Menu','Do you want to save changes to this file')

    if msg:
        save()
        root.destroy()
    elif msg == False:
        root.destroy()
    else:
        pass

#adding label
toolview = Label(root)
toolview.pack(fill = X,pady = 8,side=TOP)


#adding text area and scroll bar on both x and y view
text_area = Text(root,undo = True)
yscrollbar = Scrollbar(text_area)
text_area.pack(fill = BOTH ,expand = True)
yscrollbar.pack(side = RIGHT,fill = Y)
yscrollbar.config(command = text_area.yview)
text_area.config(yscrollcommand= yscrollbar.set)


#creating overall icons
coloriconlist = [ImageTk.PhotoImage(Image.open(rf"color\{i}.png") )for i in range(17)]
#adding colorchooser_button image
colorchooser_button = Button(toolview,image = coloriconlist[5])






#for fg color button fun
colorchooser_button.config(command =colorfont)
colorchooser_button.grid(row=0,column =4)






#adding combobox for font style inside toolview
fontvar = StringVar()

fontsize = IntVar()
fontvar.set('Arial')
fontsize.set(25)




def fontchange(e):
    global text_area
    text_area.configure(font= (fontvar.get(),fontsize.get()))



fontbox =ttk.Combobox(toolview,state = 'readonly',value = font.families(),textvariable = fontvar)

#adding font size box
sizebox =ttk.Combobox(toolview,state = 'readonly',value = [i for i in range(1,100)],textvariable = fontsize)
fontbox.bind('<<ComboboxSelected>>',fontchange)
sizebox.bind('<<ComboboxSelected>>',fontchange)
fontbox.grid(row = 0,column=0)
sizebox.grid(row = 0,column=1)

#adding menubar
main_menu = Menu(root)

#adding file menu in menubar
file_menu = Menu(main_menu,tearoff = 0)
file_menu.add_command(label = 'New',image = coloriconlist[9],compound = 'left',accelerator='Ctrl+n' )
file_menu.add_command(label = 'Open',image = coloriconlist[10],compound = 'left',accelerator = 'Ctrl + o')
file_menu.add_command(label = 'Save',image = coloriconlist[16],command = save,compound = 'left',accelerator = 'Ctrl + s')
file_menu.add_command(label = 'Save As',image = coloriconlist[11],command = save_as,compound = 'left',accelerator = 'F12')
main_menu.add_cascade(label = 'File',menu = file_menu)

#creating shortcuts
root.bind_all('<Control-n>',new)
root.bind_all('<Control-o>',Open)
root.bind_all('<F12>',save_as)
root.bind_all('<Alt-F4>',quit)


root.bind_all('<Control-s>',save)

#redo function
def Redo():
    try:
        text_area.redo()
    except:
        return
#adding edit menu in menubar
edit_menu = Menu(main_menu,tearoff = 0)
edit_menu.add_command(label = 'Cut',image = coloriconlist[6],command = cut,accelerator = 'Ctrl+ X')
edit_menu.add_command(label = 'Copy',image = coloriconlist[7],command = copy,accelerator = 'Ctrl+ C')
edit_menu.add_command(label = 'Paste',image = coloriconlist[13],command = paste,accelerator = 'Ctrl+ V')
edit_menu.add_command(label = 'Select All',image = coloriconlist[15],command =select_all,accelerator = 'Ctrl+ A')
edit_menu.add_command(label = 'Redo',image = coloriconlist[12],command = Redo,accelerator= 'Ctrl+ Y')
edit_menu.add_command(label = 'Undo',image = coloriconlist[14],command = text_area.edit_undo,accelerator = 'Ctrl+ Z')

main_menu.add_cascade(label = 'Edit',menu = edit_menu)

#adding themes menu in menubar
#for adding themes, adding icons of colors



theme_menu = Menu(main_menu,tearoff = 0)
theme_menu.add_command(label = 'White',image = coloriconlist[0],compound = 'left',command= lambda :text_area.config(bg = "White",fg = 'Black',insertbackground ='black' ))
theme_menu.add_command(label = 'Black',image = coloriconlist[1],compound = 'left',command =lambda :text_area.config(bg = "Black",fg = 'White',insertbackground ='white'))
theme_menu.add_command(label = 'Orange',image = coloriconlist[2],compound = 'left',command =lambda :text_area.config(bg = "Orange",fg = 'Black',insertbackground ='black'))
theme_menu.add_command(label = 'Blue',image = coloriconlist[3],compound = 'left',command =lambda :text_area.config(bg = "Blue",fg = 'Black',insertbackground ='white'))
theme_menu.add_command(label = 'Cyan',image = coloriconlist[4],compound = 'left',command =lambda :text_area.config(bg = "Cyan",fg = 'Black',insertbackground ='black'))
main_menu.add_cascade(label = 'Themes',menu = theme_menu)

#creating help menu inside main_menu
main_menu.add_command(label = 'Help',command = _help)

#creating quit menu inside main menu
main_menu.add_command(label = 'Quit',command = Quit,compound = 'left')

##############################################  status bar ###################################################

status_bar = ttk.Label(root, text = 'Status Bar')
status_bar.pack(anchor = 's')


def changed(event=None):
    if text_area.edit_modified():
        words = len(text_area.get(1.0, END).split())
        characters = (len(text_area.get(1.0, END))-1)
        status_bar.config(text=f'Characters : {characters} Words : {words}')
    text_area.edit_modified(False)

text_area.bind('<<Modified>>', changed)

# -------------------------------------&&&&&&&& End  status bar &&&&&&&&&&& ----------------------------------



root.config(menu = main_menu)
root.mainloop()
