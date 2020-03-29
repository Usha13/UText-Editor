import tkinter as tk
from tkinter import ttk,font,colorchooser,messagebox,filedialog
import os
import speech_recognition as sr
# from pydub import AudioSegment

win = tk.Tk()
win.title('UText_Editor')
win.iconbitmap('icon2/ic.ico')
win.geometry('900x600')
# win.positionfrom(fill=tk.TOP)

#******************Main menu*************************
mainmenu = tk.Menu(win)

filemenu = tk.Menu(mainmenu,tearoff=0)
mainmenu.add_cascade(label= 'File',menu= filemenu)

editmenu = tk.Menu(mainmenu,tearoff=0)
mainmenu.add_cascade(label = "Edit" ,menu = editmenu)

viewmenu = tk.Menu(mainmenu,tearoff = 0)
mainmenu.add_cascade(label = "View" ,menu = viewmenu)

thememenu = tk.Menu(mainmenu,tearoff= 0)

color_var = tk.StringVar()
color_dict= {
    'Default' : ('#ffffff','#000000'),
    'Red' :   ('#ff0000', '#fff0f5'),
    'Yellow' : ('#ffff00', '#006400'),
    'Blue' : ('#00bfff', '#000000' ),
    'Dark' : ('#2d2d2d', '#c4c4c4')
     }

def color_theme():
    col_theme = color_var.get()
    col_tp = color_dict[col_theme]
    bg, fg = col_tp[0],col_tp[1]
    text_pad.config(background=bg, foreground = fg)


for i in color_dict:
    thememenu.add_radiobutton(label = i,variable= color_var,command = color_theme)

mainmenu.add_cascade(label = "Theme" ,menu = thememenu)
win.config(menu = mainmenu)
#**************************** end main menu***************************

#*************************** Tool Bar****************************
toolbar = ttk.Label(win)
toolbar.pack(side = tk.TOP,fill= tk.X)

#*********** Mike ****************
mike_icon = tk.PhotoImage(file="icon2/mike.png")
mike_btn = tk.Button(toolbar,image=mike_icon,width=30,height=30,compound=tk.CENTER)
mike_btn.grid(row= 0,column=0,padx=8, pady=10)
mk_lbl= ttk.Label(toolbar)
mk_lbl.grid(row=0, column= 10,padx=70,pady=10)

sr.Microphone(device_index=1)
r= sr.Recognizer()
r.energy_threshold = 5000

def voice2text():
    mk_lbl.config(text="Listening....")
    with sr.Microphone() as source:
        
        ado = r.listen(source)
        try:
            
            txt= r.recognize_google(ado)
            text_pad.insert(tk.END,txt+" ")
            mk_lbl.config(text="")
        except Exception as err:
            print(err)
            mk_lbl.config(text="Not Recognized !") 
   
mike_btn.config(command = voice2text)        

#****** Font family*************
family_var = tk.StringVar()
font_family = tk.font.families()
family_combo = ttk.Combobox(toolbar,width=30, textvariable= family_var, state= 'readonly')
family_combo['values'] = font_family
family_combo.current(font_family.index('Arial'))
family_combo.grid(row=0,column=1,padx= 8,pady= 10)

#****** Font size*************
size_var = tk.IntVar()
font_size = tuple(range(2,101,2))
size_combo = ttk.Combobox(toolbar,width=15,textvariable = size_var, state= 'readonly')
size_combo['values'] = font_size
size_combo.current(font_size.index(14))
size_combo.grid(row = 0, column= 2,padx = 8,pady= 10)

bicon = tk.PhotoImage(file= "icon2/bold.png")
iticon = tk.PhotoImage(file= "icon2/italic.png")
ulicon = tk.PhotoImage(file= "icon2/ul.png")
colicon = tk.PhotoImage(file= "icon2/color.png")
laicon = tk.PhotoImage(file= "icon2/la.png")
caicon = tk.PhotoImage(file= "icon2/ca.png")
raicon = tk.PhotoImage(file= "icon2/ra.png")


#************ Bold button********
bold_btn = tk.Button(toolbar,image= bicon,width=30,height=30,compound=tk.CENTER)
bold_btn.grid(row= 0,column= 3, padx= 8,pady= 10)

#************ Italic button********
italic_btn = tk.Button(toolbar,image= iticon,width=30,height=30,compound=tk.CENTER)
italic_btn.grid(row= 0,column= 4, padx= 8,pady= 10)

#************ Underline button********
underline_btn = tk.Button(toolbar,image= ulicon,width=30,height=30,compound=tk.CENTER)
underline_btn.grid(row= 0,column= 5, padx= 8,pady= 10)

#************ Colorchooser button********
color_btn = tk.Button(toolbar,image= colicon,width=30,height=30,compound=tk.CENTER)
color_btn.grid(row= 0,column= 6, padx= 8,pady= 10)

#************ Align left button********
left_btn = tk.Button(toolbar,image= laicon,width=30,height=30,compound=tk.CENTER)
left_btn.grid(row= 0,column= 7, padx= 8,pady= 10)

#************ Align center button********
center_btn = tk.Button(toolbar,image= caicon,width=30,height=30,compound=tk.CENTER)
center_btn.grid(row= 0,column= 8, padx= 8,pady= 10)

#************ Align right button********
right_btn = tk.Button(toolbar,image= raicon,width=30,height=30,compound=tk.CENTER)
right_btn.grid(row= 0,column= 9, padx= 8,pady= 10)
#***************************** End tool bar ***********************

#********************* Text Pad ********************************
text_pad = tk.Text(win,undo=True)
# text_pad.config(wrap= 'word', relief= tk.FLAT)
text_pad.pack(fill= tk.BOTH, expand= True)
scroll = tk.Scrollbar(text_pad)
scroll.pack(side= tk.RIGHT, fill= tk.Y)
scroll.config(command = text_pad.yview)
text_pad.config(yscrollcommand = scroll.set)
text_pad.focus()
#*********************End Text Pad ********************************

#*********************Status bar ********************************
status = ttk.Label(win, text= "Status bar")
status.pack(side = tk.BOTTOM)

text_changed = False 
def change(event= None):
    global text_changed
    if text_pad.edit_modified():
        text_changed = True
        words = len(text_pad.get(1.0, tk.END).split())
        characters = len(text_pad.get(1.0, tk.END).replace(' ',''))
        lines= len(text_pad.get(1.0,tk.END).split('\n'))
        status.config(text= f"characters: {characters-1}  words: {words} lines: {lines-1}")
    text_pad.edit_modified(False)

text_pad.bind("<<Modified>>", change)
#*********************End Status bar ********************************

#********************main menu functionality**************************
#******************file menu***************
#*****new file****
url =''
def new_file(event=None):
    global url
    url= ''
    text_pad.delete(1.0,tk.END)

flag= False
# ext = ('.mp3','.m4a','.wav','.flac')
def open_file(event=None):
    global url,flag
    url = filedialog.askopenfilename(initialdir = os.getcwd(), filetypes= (('Text Files','*.txt'),('All Files','*.*')))
    try:
        # r = sr.Recognizer()
        with open(url,'r') as fr:
            # dist = os.path.splitext(fr)[0]+".wav"
            # for i in ext:
            #     if os.path.splitext(fr)[1] == i:
            #         flag = True
            #         return
            # if flag:
            #     sd = AudioSegment.from_mp3(fr)
            #     sd.export(dist,format= "wav")
                    
            #     with sr.AudioFile(dist) as src:
            #         ado = r.record(src)
            #         txt= r.recognize_google(ado)
            #         text_pad.delete(1.0, tk.END)
            #         text_pad.insert(1.0,txt)
            # else:
                text_pad.delete(1.0, tk.END)
                text_pad.insert(1.0,fr.read())
        # flag= False            
    except:
        return
    win.title(os.path.basename(url))  

def save_file(event=None):
    global url
    try:
        if url:
            content1 = text_pad.get(1.0,tk.END)
            with open(url,'w',encoding='utf-8') as fw:
                fw.write(content1)
        else:
            url = filedialog.asksaveasfile(mode='w', defaultextension='.txt',filetypes=(('Text Files','*.txt'),('All Files','*.*')))
            content2 = text_pad.get(1.0,tk.END)        
            url.write(content2)
            url.close()
    except:
        return        

def saveas_file(event=None):
    url = filedialog.asksaveasfile(mode='w', defaultextension='.txt',filetypes=(('Text Files','*.txt'),('All Files','*.*')))
    content2 = text_pad.get(1.0,tk.END)        
    url.write(content2)
    url.close()

def exit_func(event=None):
    global url,text_changed
    try:
        if text_changed:
            mbox = messagebox.askyesnocancel('Warning', 'Do you want to save the file ?')
            if mbox is True:
                if url:
                    content1 = text_pad.get(1.0,tk.END)
                    with open(url,'w',encoding='utf-8') as fw:
                        fw.write(content1)
                        win.destroy()
                else:
                    url = filedialog.asksaveasfile(mode='w', defaultextension='.txt',filetypes=(('Text Files','*.txt'),('All Files','*.*')))
                    content2 = text_pad.get(1.0,tk.END)
                    url.write(content2)
                    url.close()
                    win.destroy()
            elif mbox is False:
                win.destroy()
        else:
            win.destroy()
    except:
        return                                


filemenu.add_command(label= 'New', accelerator= "CTRL+N",command= new_file)
filemenu.add_separator()
filemenu.add_command(label= 'Open', accelerator= "CTRL+O ",command= open_file)
filemenu.add_separator()
filemenu.add_command(label= 'Save', accelerator= "CTRL+S", command= save_file)
filemenu.add_command(label= 'Save As', accelerator= "CTRL+Shift+S",command= saveas_file)
filemenu.add_separator()
filemenu.add_command(label= 'Exit',accelerator= "CTRL+Q", command = exit_func)

#******************end file menu***************

#******************Edit menu***************
def find_func(event=None):
    find_dialog = tk.Toplevel(win)
    find_dialog.title("Find")
    find_dialog.geometry('400x200+600+200')
    find_dialog.resizable(0,0)

    find_frame = ttk.LabelFrame(find_dialog,text= "Find/Replace")
    find_frame.pack(pady= 10,padx=10,fill=tk.BOTH,expand=True) 

    f = tk.StringVar()
    r = tk.StringVar()
    flabel = ttk.Label(find_frame,text= "Find :")
    rlabel = ttk.Label(find_frame,text= "Replace :")
    finput = ttk.Entry(find_frame,width= 35,textvariable= f )
    rinput = ttk.Entry(find_frame,width= 35,textvariable= r )
    fbtn = ttk.Button(find_frame,text= "Find")
    rbtn = ttk.Button(find_frame,text= "Replace")

    flabel.grid(row=0,column=0,padx= 30,pady=10) 
    rlabel.grid(row=1,column=0,padx= 30,pady=10) 
    finput.grid(row=0,column=1,padx= 5,pady=10) 
    rinput.grid(row=1,column=1,padx= 5,pady=10) 
    fbtn.grid(row=2,column=0,padx= 30,pady=10) 
    rbtn.grid(row=2,column=1,padx= 30,pady=10) 

    def find():
        fword= f.get()
        text_pad.tag_remove('match',1.0,tk.END)
        start_pos = 1.0
        matches = 0
        while True:
            start_pos = text_pad.search(fword,start_pos,stopindex=tk.END)
            if not start_pos:
                break
            end_pos = f"{start_pos}+{len(fword)}c"
            text_pad.tag_add('match',start_pos,end_pos)
            matches+=1
            start_pos = end_pos
            text_pad.tag_config('match',foreground= 'red',background = 'yellow')

    fbtn.config(command = find)        

    def replace():
        fword = f.get()
        rword = r.get()
        content = text_pad.get(1.0,tk.END)
        new_con = content.replace(fword,rword)
        text_pad.delete(1.0,tk.END)
        text_pad.insert(1.0,new_con)

    rbtn.config(command = replace)    

editmenu.add_command(label = 'Undo', accelerator = "CTRL+Z",command= lambda: text_pad.event_generate("<<Undo>>"))
editmenu.add_command(label = 'Redo', accelerator = "CTRL+Y",command= lambda: text_pad.event_generate("<<Redo>>"))
editmenu.add_separator()
editmenu.add_command(label = 'Cut', accelerator = "CTRL+X",command= lambda: text_pad.event_generate("<Control x>"))
editmenu.add_command(label = 'Copy', accelerator = "CTRL+C",command= lambda: text_pad.event_generate("<Control c>"))
editmenu.add_command(label = 'Paste', accelerator = "CTRL+V",command= lambda: text_pad.event_generate("<Control v>"))
editmenu.add_command(label = 'Print', accelerator = "CTRL+P",command= lambda: text_pad.event_generate("<<Print>>"))
editmenu.add_separator()
editmenu.add_command(label = 'Find', accelerator = "CTRL+F", command= find_func)
#****************** end Edit menu***************

#*******************view menu*****************
show_tb = tk.BooleanVar()
show_tb.set(True)
show_sb = tk.BooleanVar()
show_sb.set(True)

def toolbar_func():
    global show_tb
    if show_tb:
        toolbar.pack_forget()
        show_tb= False
    else:
        text_pad.pack_forget()
        status.pack_forget()
        toolbar.pack(side=tk.TOP,fill= tk.X)
        text_pad.pack(fill=tk.BOTH, expand = True)
        status.pack(side= tk.BOTTOM)
        show_tb = True    

def statusbar_func():
    global show_sb
    if show_sb:
        status.pack_forget()
        show_sb = False
    else:
        status.pack(side= tk.BOTTOM)
        show_sb = True    

viewmenu.add_checkbutton(label='Show Toolbar', variable= show_tb, command = toolbar_func)
viewmenu.add_separator()
viewmenu.add_checkbutton(label='Show Statusbar', variable = show_sb, command = statusbar_func) 
#*******************end view menu*****************

#******************** End main menu functionality**************************

#**********************Buttons functionality*******************
#************font functionality****************
cur_family = 'Arial'
cur_size= '14'

def font_family_change(win):
    global cur_family
    cur_family = family_var.get()
    text_pad.configure(font= (cur_family, cur_size))

def font_size_change(win):
    global cur_size
    cur_size = size_var.get()
    text_pad.configure(font= (cur_family, cur_size))

family_combo.bind("<<ComboboxSelected>>",font_family_change)    
size_combo.bind("<<ComboboxSelected>>",font_size_change)    
#***********end font functionality***********

#********Bold button functionality***********
def bold_func():
    text_ppt = tk.font.Font(font = text_pad['font']).actual()
    if text_ppt['weight'] =='normal':
        text_pad.configure(font= (cur_family,cur_size,'bold'))
    if text_ppt['weight'] =='bold':
        text_pad.configure(font= (cur_family,cur_size,'normal'))    

bold_btn.configure(command = bold_func)    

#******** end Bold button functionality***********

#********Italic button functionality***********
def italic_func():
    text_ppt = tk.font.Font(font = text_pad['font']).actual()
    if text_ppt['slant'] =='roman':
        text_pad.configure(font= (cur_family,cur_size,'italic'))
    if text_ppt['slant'] =='italic':
        text_pad.configure(font= (cur_family,cur_size,'roman'))    

italic_btn.configure(command = italic_func)
#******** end Italic button functionality***********

#********Underline button functionality***********
def underline_func():
    text_ppt = tk.font.Font(font = text_pad['font']).actual()
    if text_ppt['underline'] == 0:
        text_pad.configure(font= (cur_family,cur_size,'underline'))
    if text_ppt['underline'] == 1:
        text_pad.configure(font= (cur_family,cur_size,'normal'))

underline_btn.config(command = underline_func)    
#********end Underline button functionality***********
text_pad.configure(font= (cur_family,cur_size ))

#***************Color button functionality************
def color_func():
    color = tk.colorchooser.askcolor()
    text_pad.config(fg = color[1])
color_btn.config(command = color_func)     
#***************end Color button functionality************

#***************Alignment button functionality************
# left align
def left_align_func():
    text_var = text_pad.get(1.0,'end')
    text_pad.tag_config('left', justify= tk.LEFT)
    text_pad.delete(1.0, tk.END)
    text_pad.insert(tk.INSERT,text_var, 'left')

left_btn.config(command = left_align_func)

# center align
def center_align_func():
    text_var = text_pad.get(1.0,'end')
    text_pad.tag_config('center', justify= tk.CENTER)
    text_pad.delete(1.0, tk.END)
    text_pad.insert(tk.INSERT,text_var, 'center')

center_btn.config(command = center_align_func)

# right align
def right_align_func():
    text_var = text_pad.get(1.0,'end')
    text_pad.tag_config('right', justify= tk.RIGHT)
    text_pad.delete(1.0, tk.END)
    text_pad.insert(tk.INSERT,text_var, 'right')

right_btn.config(command = right_align_func)
#***************end Alignment button functionality************
#**********************end button functionality*******************

win.bind("<Control-n>", new_file)
win.bind("<Control-o>", open_file)
win.bind("<Control-s>", save_file)
win.bind("<Control-Alt-s>", saveas_file)
win.bind("<Control-q>", exit_func)
win.bind("<Control-f>", find_func)


win.mainloop()