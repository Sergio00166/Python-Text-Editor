# Code by Sergio00166

from functions1 import get_size,CalcRelLine
from upd_scr import update_scr,movcr
from chg_var_str import chg_var_str
from time import sleep as delay
from threading import Thread
from os import sep



if not sep==chr(92): #If OS is LINUX
    #Get default values for TTY
    from termios import TCSADRAIN,tcsetattr,tcgetattr
    from sys import stdin; from tty import setraw
    fd = stdin.fileno(); old_settings = tcgetattr(fd)

def updscr_thr():
    global rows,columns,black,reset,status,banoff,pointer
    global offset,line,arr,banner,filename,rows,columns,run
    global kill,fd,thr,old_settings,status_st,bnc,slc,find_str
    
    while not kill:
        delay(0.01)
        if run:
            # If OS is LINUX restore TTY to it default values
            if not sep==chr(92):
                old=(fd,TCSADRAIN,old_settings)
                tcsetattr(fd, TCSADRAIN, old_settings)
            # Call Screen updater
            rows,columns=get_size()
            # Call screen updater function
            update_scr(black,bnc,slc,reset,status,banoff,offset,line,pointer,arr,banner,\
                       filename,rows,columns,status_st,False,[],[find_str,line,pointer])
            # If OS is LINUX set TTY to raw mode
            if not sep==chr(92): setraw(fd,when=TCSADRAIN)


def exit():
    global fd, old_settings, run, kill, thr
    run=False; kill=True; thr.join()
    if not sep == chr(92): tcsetattr(fd,TCSADRAIN,old_settings)


def search_substring(lst, substring, start_list_pos=0, start_string_pos=0):
    list_length,i = len(lst),start_list_pos
    while True:
        start = start_string_pos if i == start_list_pos else 0
        for j in range(start, len(lst[i])):
            if lst[i][j:j+len(substring)] == substring:
                return i, j+len(substring)
        i,start_string_pos = (i+1)%list_length,None

def search_substring_rev(lst, substring, start_list_pos=0, start_string_pos=None):
    list_length,i = len(lst),start_list_pos
    while True:
        start = start_string_pos if i == start_list_pos else len(lst[i])
        if start_string_pos is None: start = len(lst[i])
        else: start = start_string_pos-len(find_str)
        for j in range(start, -1, -1):
            if lst[i][j-len(substring):j] == substring: return i, j
        i,start_string_pos = (i-1)%list_length,None


def find(arg):
    global rows,columns,black,reset,status,banoff,pointer
    global offset,line,arr,banner,filename,rows,columns,run
    global kill,fd,thr,old_settings,status_st,bnc,slc,find_str

    filename,black,bnc,slc,reset,rows,banoff,arr,columns,\
    status,offset,line,banner,status_st,keys,read_key,pointer = arg

    args = (filename,black,bnc,slc,reset,rows,banoff,arr,columns,status,offset,\
            line,banner,status_st,keys,pointer,[],read_key,""," Find: ")    
    find_str = chg_var_str(args)

    thr=Thread(target=updscr_thr)
    run,kill = False,False
    thr.start()

    # Find and move cursor to the fist one
    pos = line+offset-banoff
    try: p1,pointer = search_substring(arr,find_str,pos,pointer)
    except: exit(); return pointer,line,offset
    line,offset = CalcRelLine(p1,arr,offset,line,banoff,rows)
    pointer += 1 # Pointer starts on 1 not 0
    
    while True:
        try:
            # If OS is LINUX restore TTY to it default values
            if not sep==chr(92):
                old=(fd,TCSADRAIN,old_settings)
                tcsetattr(fd, TCSADRAIN, old_settings)
            # Call Screen updater
            rows,columns=get_size()
            # Call screen updater function
            update_scr(black,bnc,slc,reset,status,banoff,offset,line,pointer,arr,banner,\
                       filename,rows,columns,status_st,False,[],[find_str,line,pointer])
            # If OS is LINUX set TTY to raw mode
            if not sep==chr(92): setraw(fd,when=TCSADRAIN)
            
            run=True #Start update screen thread
            key=read_key() #Map keys
            run=False #Stop update screen thread

            pos = line+offset-banoff
    
            if key==keys["arr_right"]:
                p1,pointer = search_substring(arr,find_str,pos,pointer)
                line,offset = CalcRelLine(p1,arr,offset,line,banoff,rows)
                pointer += 1 # Pointer starts on 1 not 0
                
            elif key==keys["arr_left"]:
                p1,pointer = search_substring_rev(arr,find_str,pos,pointer-1)
                line,offset = CalcRelLine(p1,arr,offset,line,banoff,rows)
                pointer += 1 # Pointer starts on 1 not 0

            elif key==keys["ctrl+c"]: exit(); break
   
        except: pass

    return pointer,line,offset
