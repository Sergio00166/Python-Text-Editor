#!/usr/bin/env python3
# Code by Sergio00166

def updscr_thr():
    global black,reset,status,banoff,offset,line,pointer
    global banner,filename,rows,columns,run_thread,text
    global kill,p_offset,arr,select
    
    while not kill:
        delay(0.01)
        if run_thread:
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
                print("\r\033[3J",end="") # Clear previous content
                # Call screen updater function
                update_scr(black,bnc,slc,reset,status,banoff,offset,line,pointer,\
                           arr,banner,filename,rows,columns,status_st,False,select)
                # If OS is LINUX set TTY to raw mode
                if not sep==chr(92): setraw(fd,when=TCSADRAIN)


if __name__=="__main__":
    
    from sys import path
    from os import sep
    # Add the folder to import from here
    path.append(path[0]+sep+"bin")
    from init import *
    
    # Run the update Thread
    update_thr=Thread(target=updscr_thr)
    run_thread=True; kill=False
    update_thr.start()
    
    while True:
        try:
            # Fix arr when empty
            if len(arr)==0: arr=[""]
            # If status flag is 0 set save text to blank
            if status_st==0: status=saved_df 
            # Get the terminal size
            rows,columns=get_size()
            # Call screen updater function
            print("\033[0 q",end="") # Change cursor
            update_scr(black,bnc,slc,reset,status,banoff,offset,line,pointer,arr,\
                       banner,filename,rows,columns,status_st,False,select)
            # Set time after reading key from keyboard and stopping the update Thread
            run_thread=True; key=getch(); run_thread=False
            # If key is Ctrl + Q (quit) exit the program and clear the screen
            if key==keys["ctrl+q"]:
                if len(files)>0:
                    filename,files = files[0],files[1:]
                    arr,codec,lnsep = read_UTF8(filename)
                    pointer,line,offsetstatus_st = 1,1,0,False
                else: kill=True; update_thr.join(); break
            #Call keys functions (Yeah, its a lot of args and returned values)
            args = (
                key,pointer,oldptr,line,offset,columns,banoff,arr,rows,
                filename,status,status_st,copy_buffer,black,bnc,slc,reset,
                saved_txt,indent,banner,getch,keys,select,codec,lnsep,comment
            )
            pointer,oldptr,line,offset,columns,banoff,arr,\
            rows,filename,status,status_st,copy_buffer,\
            indent,select,codec,lnsep,comment = keys_func(*args)
                         
        except: pass


    # Clear and reset the terminal
    if not sep==chr(92):
        print("\x1b[H\x1b[2J\x1b[3J")
    print("\r\033c",end="")
