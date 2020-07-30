import tkinter as tk
from tkinter import ttk
from tkinter import font, colorchooser, filedialog, messagebox
import os


main_application = tk.Tk()
main_application.geometry('1080x1920')
main_application.title('Writepad Text editor')
main_application.wm_iconbitmap('icon.ico')


# ************************************* main menu **********************************
main_menu = tk.Menu()
file = tk.Menu(main_menu, tearoff=False)
edit = tk.Menu(main_menu, tearoff=False)
theme = tk.Menu(main_menu, tearoff=False)

main_menu.add_cascade(label='File', menu=file)
main_menu.add_cascade(label='Edit', menu=edit)
main_menu.add_cascade(label='Theme', menu=theme)
# *********************************** end main menu *********************************


# color icons code
light_default = tk.PhotoImage(file='icons2/light_default.png')
dark_icon = tk.PhotoImage(file='icons2/dark.png')
monokai_icon = tk.PhotoImage(file='icons2/monokai.png')
night_blue = tk.PhotoImage(file='icons2/night_blue.png')

theme_choice= tk.StringVar() # variable for store which color theme choice by user
color_icons=(light_default, dark_icon, monokai_icon, night_blue)

color_dict={
    'Light default': ('#000000', '#ffffff'),
    'dark': ('#c4c4c4', '#2d2d2d'),
    'monokai': ('#d3b778', '#474747'),
    'Night blue': ('#ededed', '#6b9dc2')
}
# ******************************************* end color theme menu *****************************************************


# **********************************************start tool bar *********************************************************
# font box
tool_bar = ttk.Label(main_application)
tool_bar.pack(side=tk.TOP, fill= tk.X)

fonts = tk.font.families()
font_family = tk.StringVar()
font_box = ttk.Combobox(tool_bar, width=35, textvariable=font_family, state='readonly')
font_box['values']= fonts
font_box.current(0)
font_box.grid(row=0, column=0, padx=5)

# size box
size_var = tk.IntVar()
size_box = ttk.Combobox(tool_bar, width=15, textvariable=size_var, state='readonly')
size_box['values'] = tuple(range(8, 81, 2))
size_box.current(4)
size_box.grid(row=0, column=1, padx=5)

# Bold button
bold_button = tk.PhotoImage(file='icons2/bold.png')
bld_button = ttk.Button(tool_bar, image=bold_button)
bld_button.grid(row=0, column=2, padx=5)

# Italic button
italic_button = tk.PhotoImage(file='icons2/italic.png')
itl_button= ttk.Button(tool_bar, image=italic_button)
itl_button.grid(row=0, column=3, padx=5)

# font color button
font_icon = tk.PhotoImage(file='icons2/font_color.png')
fnt_button = ttk.Button(tool_bar, image=font_icon)
fnt_button.grid(row=0, column=4, padx=5)


# ******************************************end tool bar ***************************************************************

# ***************************************** start text editor **********************************************************
text_editor = tk.Text(main_application)
text_editor.config(wrap='word', relief=tk.FLAT)
scroll_bar = ttk.Scrollbar(main_application)
scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
text_editor.focus_set()
text_editor.pack(fill=tk.BOTH, expand=True)
scroll_bar.config(command=text_editor.yview)
text_editor.config(yscrollcommand=scroll_bar.set)

#  font_box and size_box functionality
current_font_family = 'System'
current_font_size = '16'

def font_changer(event=None):
    """ this function is use for change font type """
    global current_font_family
    current_font_family = font_family.get()
    text_editor.configure(font=(current_font_family, current_font_size))

def size_changer(event=None):
    """ this function is use for change font size """
    global current_font_size
    current_font_size = size_var.get()
    text_editor.configure(font=(current_font_family, current_font_size))

font_box.bind("<<ComboboxSelected>>", font_changer)
size_box.bind("<<ComboboxSelected>>", size_changer)

#******* bold button functionality
def bold_func():
    """use for text bold"""
    text_prop1 = tk.font.Font(font=text_editor['font'])
    if text_prop1.actual()['weight'] == 'normal':
        text_editor.configure(font=(current_font_family, current_font_size, 'bold'))
    if text_prop1.actual()['weight'] == 'bold':
        text_editor.configure(font=(current_font_family, current_font_size, 'normal'))

bld_button.configure(command=bold_func)

# ******* italic functionality

def italic_func():
    """use for italic text"""
    text_prop2 = tk.font.Font(font=text_editor['font'])
    if text_prop2.actual()['slant'] == 'roman':
        text_editor.configure(font=(current_font_family, current_font_size, 'italic'))
    if text_prop2.actual()['slant'] == 'italic':
        text_editor.configure(font=(current_font_family, current_font_size, 'normal'))

itl_button.configure(command=italic_func)

## font color functionality
def change_font_color():
    color_var = tk.colorchooser.askcolor()
    text_editor.configure(fg=color_var[1])

fnt_button.configure(command=change_font_color)

text_editor.configure(font=('System', 16))

# ******************************************main menu functionality ****************************************************
#  file menu -----> new, open, save, save as
## variable
url = ''

## new functionality
def new_file(event=None):
    global url
    url = ''
    text_editor.delete(1.0, tk.END)

file.add_command(label='new', compound= tk.LEFT, accelerator= 'ctrl+N', command=new_file)

## open functionality

def open_file(event=None):
    global url
    url = filedialog.askopenfilename(initialdir=os.getcwd(), title='Select File', filetypes=(('Text File', '*.txt'), ('All files', '*.*')))
    try:
        with open(url, 'r') as fr:
            text_editor.delete(1.0, tk.END)
            text_editor.insert(1.0, fr.read())
    except FileNotFoundError:
        return
    except:
        return
    main_application.title(os.path.basename(url))


file.add_command(label='open',compound= tk.LEFT, accelerator= 'ctrl+O', command=open_file)

## save file

def save_file(event=None):
    global url
    try:
        if url:
            content = str(text_editor.get(1.0, tk.END))
            with open(url, 'w', encoding='utf-8') as fw:
                fw.write(content)
        else:
            url = filedialog.asksaveasfile(mode = 'w', defaultextension='.txt', filetypes=(('Text File', '*.txt'), ('All files', '*.*')))
            content2 = text_editor.get(1.0, tk.END)
            url.write(content2)
            url.close()
    except:
        return

file.add_command(label='save',compound= tk.LEFT, accelerator= 'ctrl+S', command = save_file)

## save as functionality
def save_as(event=None):
    global url
    try:
        content = text_editor.get(1.0, tk.END)
        url = filedialog.asksaveasfile(mode = 'w', defaultextension='.txt', filetypes=(('Text File', '*.txt'), ('All files', '*.*')))
        url.write(content)
        url.close()
    except:
        return

file.add_command(label='save as',compound= tk.LEFT, accelerator= 'ctrl+Alt+S', command=save_as)


# ****************************** end file menu ************************************

# edit menu -----> copy, paste, cut, clear
edit.add_command(label='copy', compound=tk.LEFT, accelerator= 'ctrl+C', command=lambda:text_editor.event_generate("<Control c>"))
edit.add_command(label='paste', compound=tk.LEFT, accelerator= 'ctrl+V', command=lambda:text_editor.event_generate("<Control v>"))
edit.add_command(label='cut', compound=tk.LEFT, accelerator= 'ctrl+X', command=lambda:text_editor.event_generate("<Control x>"))
edit.add_command(label='clear', compound=tk.LEFT, accelerator= 'ctrl+Alt+B', command= lambda:text_editor.delete(1.0, tk.END))
# ****************************** end edit menu **************************************


# color theme
def change_theme():
    chosen_theme = theme_choice.get()
    color_tuple = color_dict.get(chosen_theme)
    fg_color, bg_color = color_tuple[0], color_tuple[1]
    text_editor.config(background=bg_color, fg=fg_color)
count=0
for i in color_dict:
    theme.add_radiobutton(label=i, image=color_icons[count], variable= theme_choice, compound=tk.LEFT, command=change_theme)
    count += 1
# end color theme
# ******************************* end main menu functionality **********************************************************


main_application.config(menu=main_menu)
#### bind shortcut keys
main_application.bind("<Control-n>", new_file)
main_application.bind("<Control-o>", open_file)
main_application.bind("<Control-s>", save_file)
main_application.bind("<Control-Alt-s>", save_as)

main_application.mainloop()