#Code by Sergio1260


def updscr_thr():
    global black,reset,legacy,status,p_offset,banoff,offset,line,pointer,arr,banner,filename,bottom,rows,columns,run_thread,text
    open("debug.txt","w")
    while True:
        if run_thread:
            delay(0.1)
            old_rows=rows; old_columns=columns
            rows,columns=get_size()
            if not (old_rows==rows and old_columns==columns):
                if len(arr)==0: arr.append("")
                if pointer==0: pointer=1
                if status_st==0: status=saved_df
                max_len=len(text)
                arr[line+offset-banoff]=text
                if max_len<=columns-2: p_offset=0
                if pointer>columns+2:
                    p_offset=len(text)-columns+2
                    pointer=columns
        
                debug=open("debug.txt","a")
                debug.write(f"\n----UPDATE -------------------------------\n")
                debug.write(f"  old: {old_rows}rows {old_columns}columns\n")
                debug.write(f"  new: {rows}rows {columns}columns\n")
                debug.write(f"  OTHER: {line}line {offset}offset\n")

                update_scr(black,reset,legacy,status,p_offset,banoff,offset,line,
                           pointer,arr,banner,filename,bottom,rows,columns)
                print(("\r\033[%d;%dH"%(line+1, pointer)),end="")
            
if not __name__=="__main__":

    from msvcrt import getch
    from os import getcwd
    from sys import argv
    from os.path import exists
    from functions1 import *
    from functions2 import *
    from special_keys import special_keys
    from saveas import *
    from subprocess import check_output
    from colorama import init, Fore, Back, Style
    from threading import Thread
    from time import sleep as delay
    
    init(autoreset=False,convert=True); reset=Style.RESET_ALL
    black=Back.WHITE+Style.DIM+Fore.BLACK+Style.DIM
    
    version="v0.2.3"  ;  tab_size=4

    rows,columns=get_size()

    update_thr=Thread(target=updscr_thr)
    run_thread=True; update_thr.start()

    # FIXES WHEN USING LEGACY CMD
    fix_oldcmd=str(check_output("mode con", shell=True)).split("\\r\\n")[3].replace(" ","")
    fix_oldcmd=int(fix_oldcmd[fix_oldcmd.find(":")+1:])
    if fix_oldcmd>rows+4: legacy=True
    else: legacy=False
        
    #Check if we have arguments via cli, if not ask the user for a file to open
    if not len(argv)==1: filename=" ".join(argv[1:])
    else: filename=str(input("File to open: "))
    if not ":\\" in filename: filename=getcwd()+"\\"+filename

    #If file exist open it if not create an empty list
    if exists(filename): 
        tmp=open(filename, "r", encoding="UTF-8").readlines(); arr=[]
        for x in tmp: arr.append(x.replace("\r","").replace("\n","").replace("\f",""))
        arr.append("")
    else: arr=[""]

    # Creates a list of banned chars code
    values=["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]
    fixstr=[]
    for x in range(0,2):
        for y in values:
            fixstr.append(str(x)+y)
    
    #Define a lot of stuff
    text=arr[0]; pointer=offset=0; line=banoff=1
    banner=black+" "*8+"pBTE "+version+reset
    bottom="\n\n\t"+black+"^Q"+reset+" EXIT    "+black+"^S"+reset+" SAVE    "
    bottom+=black+"^A"+reset+" Save as    "+black+"^C"+reset+" COPY    "
    bottom+=black+"^X"+reset+" CUT    "+black+"^P"+reset+" PASTE    "
    bottom+=black+"^G"+reset+" GOTO    "
    copy_buffer=""; fix=False; oldptr=0; p_offset=0

    #Flag to show after saving the file
    saved_txt=black+"SAVED"+reset; status=saved_df=black+" "*5+reset; status_st=0

    

    

