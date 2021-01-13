from tkinter import * 
from tkinter.ttk import *
from google_trans_new import google_translator  
from tkinter.filedialog import askopenfile 
import googletrans


root = Tk() 
translator = google_translator()
CodeVsLanguageDict = googletrans.LANGUAGES
LanguageVsCodeDict = {v: k for k, v in CodeVsLanguageDict.items()}
languages = [x.upper() for x in LanguageVsCodeDict.keys()]


def open_file(): 
    file = askopenfile(mode ='r', filetypes =[('Python Files', '*.srt')]) 
    if file is not None: 
        file_path.delete(1.0,END)
        file_path.insert(END,file.name)
        info.config(text="File selected",background='green',foreground="white")

def convert_file():
    srt_file = file_path.get(1.0,END)
    if(len(srt_file)<5):
        info.config(text="File not Selected",background='red',foreground="white")
        return
    try:
        srt_file = srt_file[:len(srt_file)-1]
        english_file = open(srt_file)
        english_txt = english_file.readlines()
        english_file.close()
        other_info=""
        hindi_txt=""
        to_convert = ""
        to_lang = LanguageVsCodeDict[language_box.get().lower()]
        i=0
        while i<len(english_txt):
            other_info += english_txt[i]
            i+=1
            other_info += english_txt[i]
            i += 1
            while(english_txt[i]!='\n'):
                to_convert += english_txt[i]
                i+=1
            to_convert += english_txt[i]
            i += 1
            if(len(to_convert)>4800):
                hindi_txt += translator.translate(to_convert,lang_tgt=to_lang)
                hindi_txt+="\n"
                hindi_txt+="\n"
                to_convert=""

        if(len(to_convert)>0):
            hindi_txt += translator.translate(to_convert,lang_tgt=to_lang)
            hindi_txt += "\n"
            hindi_txt += "\n"

        temp = ""
        hindi_txt = hindi_txt.split('\n')
        other_info = other_info.split('\n')
        i=0
        j=0
        while i<len(hindi_txt) and j<len(other_info)-1:
            temp += other_info[j] +"\n"
            j += 1
            temp += other_info[j] + "\n"
            j += 1
            while(i<len(hindi_txt) and hindi_txt[i]!=''):
                temp += hindi_txt[i]+"\n"
                i += 1
            i += 1
            temp += "\n"

        output_path = srt_file.split("/")
        hindi_srt = ""
        for i in range(len(output_path)-1):
            hindi_srt += output_path[i]
            hindi_srt+="/"
        hindi_srt += output_path[-1][:-4]
        hindi_srt += "_"+language_box.get()+".srt"
        hindi_file=open(hindi_srt,'w',encoding='utf8')
        hindi_file.write(temp)
        hindi_file.close()
        info.config(text="Subtitle Converted to "+ language_box.get(),background='green',foreground="black")
    except Exception as e:
        info.config(text= str(e),background='red',foreground="black",font=("Courier",10,"bold"))
    




root.geometry('500x500') 
root.title("Change Subtitle Language")

greeting = Label(root,text="Hello User",font =("Courier", 30,'bold','italic'),foreground='#39CCCC',)
file_path_label = Label(root,text="File path",font =("Courier", 10,'bold'),foreground='#85144b')
file_path = Text(root, height = 5, width = 52) 


Language_select_label = Label(root,text="Select Lannguage",font =("Courier", 10,'bold'),foreground='#85144b')
language_box = Combobox(root,values=languages,state='readonly')
language_box.current(languages.index("HINDI"))
selected_lang = language_box.get()
def callbackFunc(event):
    btn_convert.config(text='Convert to '+ language_box.get())

language_box.bind("<<ComboboxSelected>>", callbackFunc)


info = Message(root,width="400",text="",font =("Courier", 15,'bold'))
  
btn_open = Button(root, text ='Select English subtitle (.srt) file', command = lambda:open_file()) 
btn_convert = Button(root, text ='Convert to HINDI', command = lambda:convert_file()) 
btn_exit = Button(root, text = "Exit",command = root.destroy) 
greeting.pack(side=TOP,pady = 20)
file_path_label.pack(side=TOP)
file_path.pack(side=TOP)
Language_select_label.pack()
language_box.pack()
info.pack(side=TOP,pady = 10)
btn_open.pack(side = TOP, pady = 10) 
btn_convert.pack(side = TOP, pady = 10) 
btn_exit.pack(side = TOP,pady=10)

mainloop() 