#Code by Sergio1260

# Add the folder to import from here
from sys import path
from os import sep
path.append(path[0]+sep+"bin")
# Import everything from init.py
from init import *

def updscr_thr():
    global black,reset,status,banoff,offset,line,pointer,arr
    global banner,filename,rows,columns,run_thread,kill,p_offset
    if not sep==chr(92): #If OS is LINUX
        #Get default values for TTY
        import sys; import termios; import tty
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
    while not kill:
        delay(0.01)
        if run_thread:
            arg=(black,reset,status,banoff,offset,line,\
            pointer,arr,banner,filename,rows,columns)
            rows,columns = updscr(arg)

# Run the update Thread
update_thr=Thread(target=updscr_thr)
run_thread=True; kill=False
update_thr.start()

while True:
    try:
        # Fix for the pointer variable
        if pointer==0: pointer=1
        # If detected key to quickly (Ctrl + V)
        key_fast=end-start<0.01
        if not key_fast:
            # If status flag is 0 set save text to blank
            if status_st==0: status=saved_df 
            # Get the terminal size and set some values
            rows,columns=get_size(); max_len=len(text); arr[line+offset-banoff]=text
            # Call screen updater function
            update_scr(black,reset,status,banoff,offset,line,pointer,arr,banner,filename,rows,columns)
        if not key_fast: run_thread=True #Start update Thread
        # Set time after reading key from keyboard and stopping the update Thread
        start=time(); key=getch(); end=time(); run_thread=False
        # If key is Ctrl + Q (quit) exit the program and clear the screen
        if key==keys["ctrl+q"]:  kill=True; update_thr.join(); print("\033c",end=""); break    
        else: #Call keys functions (Yeah, its a lot of args and returned values)
            text,pointer,oldptr,line,offset,columns,banoff,arr,rows,\
            max_len,filename,status,status_st,copy_buffer,fixstr,fix,\
            ch_T_SP = keys_func(key,text,pointer,oldptr,line,offset,columns,\
            banoff,arr,rows,max_len,filename,status,status_st,copy_buffer,\
            fixstr,fix,black,reset,saved_txt,ch_T_SP,banner,getch,keys)
    except: pass
