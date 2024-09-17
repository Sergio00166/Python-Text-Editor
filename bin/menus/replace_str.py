# Code by Sergio00166

from upd_scr import update_scr,movcr,hcr,print
from functions1 import get_size,CalcRelLine
from chg_var_str import chg_var_str
from time import sleep as delay
from functions import str_len
from threading import Thread
from os import sep


if not sep==chr(92): #If OS is LINUX
    #Get default values for TTY
    from termios import TCSADRAIN,tcsetattr,tcgetattr
    from sys import stdin; from tty import setraw
    fd = stdin.fileno(); old_settings = tcgetattr(fd)


def updscr_thr():
    global rows,columns,black,reset,status,banoff,cursor
    global offset,line,banner,filename,rows,columns
    global kill,fd,thr,old_settings,status_st,bnc,slc
    global find_str,rel_cursor,run,arr,first_exec

    while not kill:
        delay(0.01)
        if run:
            # If OS is LINUX restore TTY to it default values
            if not sep==chr(92):
                old=(fd,TCSADRAIN,old_settings)
                tcsetattr(fd, TCSADRAIN, old_settings)
            # Save old vars and get new values
            old_rows=rows; old_columns=columns
            rows,columns=get_size()
            # Check if terminal is too small
            if rows<4 or columns<24: print("\r\033cTerminal too small")
            # Compare the old values with the new ones
            elif not (old_rows==rows and old_columns==columns):
                # Increment the offset if line is geeter than rows
                if line>rows: offset=offset+(line-rows); line=rows
                # If OS is LINUX restore TTY to it default values
                if not sep==chr(92): tcsetattr(fd, TCSADRAIN, old_settings)
                print("\r\033[3J") # Clear previous content
                # Call screen updater function
                rel_cursor = update_scr(
                black,bnc,slc,reset,status,banoff,offset,line,cursor,arr,\
                banner,filename,rows,columns,status_st,False,[],find_str)
                if not first_exec: chg_hlg(rel_cursor,find_str)
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
        i,start_string_pos = (i+1)%list_length,0

def search_substring_rev(lst, substring, start_list_pos=0, start_string_pos=None):
    list_length,i = len(lst),start_list_pos
    while True:
        start = start_string_pos if i == start_list_pos else len(lst[i])
        if start_string_pos is None: start = len(lst[i])
        else: start = start_string_pos-len(find_str)
        for j in range(start, -1, -1):
            if lst[i][j-len(substring):j] == substring: return i, j
        i,start_string_pos = (i-1)%list_length,None

def chg_hlg(rel_cursor,string):
    pos = rel_cursor-str_len(string)
    mov = movcr%(line+banoff,pos)
    if pos>0: print(mov+slc+string+reset+hcr)

def isin_arr(arr,string):
    for x in arr:
        if string in x: return True
    return False


def replace(arg):
    global rows,columns,black,reset,status,banoff,cursor
    global offset,line,banner,filename,rows,columns
    global kill,fd,thr,old_settings,status_st,bnc,slc
    global find_str,rel_cursor,run,arr,first_exec

    filename,black,bnc,slc,reset,rows,banoff,arr,columns,\
    status,offset,line,banner,status_st,keys,read_key,cursor = arg
    
    args = (filename,black,bnc,slc,reset,rows,banoff,arr,columns,status,\
            offset,line,banner,status_st,keys,cursor,[],read_key,"")

    try: find_str = find_str = chg_var_str((*args," [R] Find: "),True)
    except KeyboardInterrupt: return cursor,line,offset,arr,status_st
    try: replace_str = chg_var_str((*args," Replace with: "),True)
    except KeyboardInterrupt: return cursor,line,offset,arr,status_st

    thr=Thread(target=updscr_thr)
    run,kill = False,False
    thr.start()

    # Check if the str exists in arr
    if not isin_arr(arr,find_str):
        exit(); cursor,line,offset,arr,status_st
    # Find replace and move cursor to the first one
    pos,first_exec = line+offset-banoff,True
    cl_line,cursor = search_substring(arr,find_str,pos,cursor)
    line,offset = CalcRelLine(cl_line,arr,offset,line,banoff,rows)
    cursor -= len(find_str) # Move to the start of the string

    while True:
        try:
            # If OS is LINUX restore TTY to it default values
            if not sep==chr(92):
                old=(fd,TCSADRAIN,old_settings)
                tcsetattr(fd, TCSADRAIN, old_settings)
            # Call Screen updater
            rows,columns=get_size()
            # Call screen updater function
            rel_cursor = update_scr(
            black,bnc,slc,reset,status,banoff,offset,line,cursor,arr,\
            banner,filename,rows,columns,status_st,False,[],find_str)
            if first_exec: first_exec = False
            else: chg_hlg(rel_cursor,replace_str)
            # If OS is LINUX set TTY to raw mode
            if not sep==chr(92): setraw(fd,when=TCSADRAIN)
            
            run=True #Start update screen thread
            key=read_key() #Map keys
            run=False #Stop update screen thread
            pos = line+offset-banoff

            if key==keys["ctrl+c"]: exit(); break

            # Lock it if we cannot do anything more
            elif not isin_arr(arr,find_str): pass
            
            elif key==keys["arr_right"]:
                cl_line,cursor = search_substring(arr,find_str,pos,cursor)
                p1 = arr[cl_line][:cursor-len(find_str)]
                p2 = arr[cl_line][cursor:]
                arr[cl_line] = p1+replace_str+p2
                cursor = cursor+len(replace_str)-len(find_str)
                line,offset = CalcRelLine(cl_line,arr,offset,line,banoff,rows)
                cursor += 1 # Cursor starts in 1 not 0
                status_st = False # Reset status value
                
            elif key==keys["arr_left"]:
                cl_line,cursor = search_substring_rev(arr,find_str,pos,cursor-1)
                p1 = arr[cl_line][:cursor-len(find_str)]
                p2 = arr[cl_line][cursor:]
                arr[cl_line] = p1+replace_str+p2
                cursor = cursor+len(replace_str)-len(find_str)
                line,offset = CalcRelLine(cl_line,arr,offset,line,banoff,rows)
                cursor += 1 # Cursor starts in 1 not 0
                status_st = False # Reset status value

            elif key==keys["ctrl+a"]:
                for p,x in enumerate(arr):
                    arr[p] = x.replace(find_str,replace_str)
                status_st = False # Reset status value
                break # Exit this menu program
   
        except: pass

    return cursor,line,offset,arr,status_st
