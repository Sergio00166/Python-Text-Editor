#Code by Sergio1260

def updscr_thr():
    global black,reset,legacy,status,p_offset,banoff,offset,line,pointer,arr
    global banner,filename,bottom,rows,columns,run_thread,text, kill
    while not kill:
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
                if line>rows:
                    offset=offset+(line-rows)
                    line=rows
                
                update_scr(black,reset,legacy,status,p_offset,banoff,offset,line,
                           pointer,arr,banner,filename,bottom,rows,columns)

from sys import path
path.append(path[0]+"\\bin")
from init import *
update_thr=Thread(target=updscr_thr)
run_thread=True; kill=False
update_thr.start()

while True:
    try:
        if len(arr)==0: arr.append("")
        if pointer==0: pointer=1
        if status_st==0: status=saved_df
        max_len=len(text)
        arr[line+offset-banoff]=text
        if max_len<=columns-2: p_offset=0
        rows,columns=get_size()
        update_scr(black,reset,legacy,status,p_offset,banoff,offset,
                   line,pointer,arr,banner,filename,bottom,rows,columns)
        
        run=True #Start update Thread
        key=getch() #Read char
        run=False #Stop update Thread
       
        if key==b'\x11': #Ctrl + Q (EXIT)
            kill=True
            update_thr.join()
            print("\033c",end="")
            break
            
        else:
            #Call keys list and functions
            text,pointer,p_offset,oldptr,line,offset,columns,banoff,arr,\
            rows,max_len,filename,status,status_st,copy_buffer,fixstr,fix=\
            keys(key,text,pointer,p_offset,oldptr,line,offset,columns,banoff,\
            arr,rows,max_len,filename,status,status_st,copy_buffer,fixstr,\
            fix,black,reset,saved_txt,tab_len,tabchr)
        
    except: pass
