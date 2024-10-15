# Code by Sergio00166

from upd_scr import menu_updsrc,hcr,print
from time import sleep as delay
from functions1 import get_size
from threading import Thread
from os import sep


if not sep==chr(92): #If OS is LINUX
    #Get default values for TTY
    from termios import TCSADRAIN,tcsetattr,tcgetattr
    from sys import stdin; from tty import setraw
    fd = stdin.fileno(); old_settings = tcgetattr(fd)

def updscr_thr():
    global text,rows,columns,black,reset,status,banoff,arr
    global wrtptr,offset,line,banner,filename,rows,columns
    global run, kill, fd, old_settings, status_st, bnc, slc
    
    while not kill:
        delay(0.01)
        if run:
            # If OS is LINUX restore TTY to it default values
            if not sep==chr(92):
                old=(fd,TCSADRAIN,old_settings)
                tcsetattr(fd, TCSADRAIN, old_settings)
            # Call Screen updater
            mode=(text,"",wrtptr,0)
            arg=(black,bnc,slc,reset,status,banoff,offset,line,\
            wrtptr,arr,banner,filename,rows,columns,status_st)
            rows,columns = menu_updsrc(arg,mode)
            print(hcr) # Hide the cursor
            # If OS is LINUX set TTY to raw mode
            if not sep==chr(92): setraw(fd,when=TCSADRAIN)

def exit():
    global fd, old_settings, run, kill, thr
    run=False; kill=True; thr.join()
    if not sep == chr(92): tcsetattr(fd,TCSADRAIN,old_settings)


def show_help(arg):
    global text,rows,columns,black,reset,status,banoff,arr
    global wrtptr,offset,line,banner,filename,rows,columns
    global run,kill,fd,old_settings,thr,status_st,bnc,slc

    filename,black,bnc,slc,reset,rows,banoff,arr,columns,\
    status,offset,line,banner,status_st,keys,read_key,text = arg

    text = " Options: "+text
    wrtptr = columns
    thr=Thread(target=updscr_thr)
    run,kill = False,False
    thr.daemon = True; thr.start()
    print(hcr) # Hide the cursor
    
    while True:
        # Fix when the cursor is out
        if len(text)<wrtptr: wrtptr = len(text)
        try:
            # Force use LINUX dir separator
            text=text.replace(chr(92),"/")
            # If OS is LINUX restore TTY to it default values
            if not sep==chr(92):
                old=(fd,TCSADRAIN,old_settings)
                tcsetattr(fd, TCSADRAIN, old_settings)
            # Call Screen updater
            mode=(text,"",wrtptr,0)
            arg=(black,bnc,slc,reset,status,banoff,offset,line,\
            wrtptr,arr,banner,filename,rows,columns,status_st)
            rows,columns = menu_updsrc(arg,mode,True)
            print(hcr) # Hide the cursor
            # If OS is LINUX set TTY to raw mode
            if not sep==chr(92): setraw(fd,when=TCSADRAIN)
            
            run=True #Start update screen thread
            key=read_key() #Map keys
            run=False #Stop update screen thread

            if key==keys["arr_left"]:
                wrtptr -= columns
                if wrtptr<columns:
                    wrtptr = columns
                
            elif key==keys["arr_right"]:
                wrtptr+=columns
                if wrtptr>len(text):
                    wrtptr=len(text)

            else: break

        except: pass

    exit() # Reset

