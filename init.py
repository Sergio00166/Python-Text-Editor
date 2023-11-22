#Code by Sergio1260


def get_size():
    size=get_terminal_size()
    columns=size[0]-2
    rows=size[1]-4
    return rows, columns

if not __name__=="__main__":

    from msvcrt import getch
    from os import get_terminal_size, getcwd
    from sys import argv
    from os.path import exists
    from functions1 import *
    from functions2 import *
    from saveas import *
    from subprocess import check_output
    from colorama import init, Fore, Back, Style
    
    init(autoreset=False,convert=True); reset=Style.RESET_ALL
    black=Back.WHITE+Style.DIM+Fore.BLACK+Style.DIM
    
    version="v0.2.3"  ;  tab_size=4

    rows,columns=get_size()

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

    #Define a lot of stuff
    text=arr[0]; pointer=offset=0; line=banoff=1
    
    banner=black+" "*8+"pBTE "+version+reset
    bottom="\n\n\t"+black+"^Q"+reset+" EXIT    "+black+"^S"+reset+" SAVE    "
    bottom+=black+"^A"+reset+" Save as    "+black+"^C"+reset+" COPY    "
    bottom+=black+"^X"+reset+" CUT    "+black+"^P"+reset+" PASTE    "
    bottom+=black+"^G"+reset+" GOTO    "
    copy_buffer=""; fix=False; oldptr=0

    #Flag to show after saving the file
    saved_txt=black+"SAVED"+reset; status=saved_df=black+" "*5+reset; status_st=0

    p_offset=0


def special_keys(pointer,p_offset,text,columns,offset,line,banoff,arr,rows,oldptr):
    special_key=getch()
    if special_key==b'H': #Up
        pointer, oldptr, text, offset, line, p_offset =\
        up(line,offset,arr,text,banoff,oldptr,rows,pointer,p_offset)

    elif special_key==b'P': #Down
        pointer, oldptr, text, offset, line, p_offset =\
        down(line,offset,arr,text,banoff,oldptr,rows,pointer,p_offset)

    elif special_key==b'M': #Right
        text, pointer, p_offset, oldptr, line, offset =\
        right(pointer,p_offset,text,columns,offset,line,banoff,arr,rows,oldptr)
            
    elif special_key==b'K': #Left
        pointer, oldptr, p_offset, text, line, offset =\
        left(pointer,oldptr,line,offset,banoff,columns,p_offset,text,arr)
        
    elif special_key==b'S': #Supr
        text, arr = supr(pointer,max_len,text,offset,banoff,arr,line,p_offset)

    elif special_key==b'G': #Start
        pointer=1; p_offset=0
        oldptr=pointer
    
    elif special_key==b'O': #End
        if len(text)>columns+1: p_offset=len(text)-columns+2; pointer=columns
        else: pointer=len(text)+1
        oldptr=pointer

    return text, pointer, p_offset, oldptr, line, offset
