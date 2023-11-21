#Code by Sergio1260

from init import *

while True:
    #try:
        if len(arr)==0: arr.append("")
        if pointer==0: pointer=1
        if status_st==0: status=saved_df
          
        #A lot of stuff
        max_len=len(text); arr[line+offset-banoff]=text
        position="██"+black+str(line+offset-banoff)+reset+"█"*(4-len(str(line+offset-banoff)))
        all_file=fix_scr(arr[offset:rows+offset+1], arr, p_offset, black, reset, columns, line, offset, banoff)
        outb=position+"█"*5+status+banner
        cls()
        print(outb+"█"*(columns-len(outb)+len(filename)+3), end="")
        print(black+filename+reset+"█\n"+all_file, end="")
        print("\n"*(rows-len(arr)+1)+bottom+("\r\033[%d;%dH"%(line+1, pointer)), end="")

        if max_len<=columns-2: p_offset=0
        
        key=getch() #Read char
        
        if key==b'\xe0': #Special Keys
            text, pointer, p_offset, oldptr, line, offset =\
            special_keys(pointer,p_offset,text,columns,offset,line,banoff,arr,rows,oldptr)
            
        elif key==b'\x08': #Delete
            line, offset, text, arr, pointer, p_offset =\
            delete(pointer, text, offset, line, arr, banoff, p_offset)

        elif key==b'\r': #Return (adds new lines or moves text
            line, offset, arr, pointer, text =\
            newline(text, pointer, offset, banoff, line, arr, rows, p_offset)       

        elif key==b'\x13': #Ctrl + S (SAVE)
            out=open(filename,"w",encoding="UTF-8")
            out.write("\n".join(arr)); out.close()
            status=saved_txt; status_st=2
            
        elif key==b'\x11': print("\033c",end=""); break #Ctrl + Q (EXIT)

        elif key==b'\x18': #Ctrl + X (CUT LINE)
            copy_buffer=arr[line+offset-banoff][pointer+p_offset-1:]
            out=arr[line+offset-banoff][:pointer+p_offset-1]
            arr[line+offset-banoff]=text=out
            
        elif key==b'\x03': #Ctrl + C (COPY LINE)
            copy_buffer=arr[line+offset-banoff][pointer+p_offset-1:]
            
        elif key==b'\x10': #Ctrl + P (PASTE TEXT)
            if not len(copy_buffer)==0:
                p1=arr[:line+offset-banoff]; p2=arr[line+offset-banoff+1:]
                fix1=text[:p_offset+pointer-1]; fix2=text[p_offset+pointer-1:]
                out=fix1+copy_buffer+fix2; arr=p1+[out]+p2; text=out
        
        elif key==b'\x07': #Ctrl + G (go to line)
            line, offset, text = goto(rows, banoff, line, arr, offset, black, reset)

        elif key==b'\x01': #Ctrl + A (Save as)
            arr, status_st, filename, status =\
            save_as(filename,black,reset,rows,banoff,arr,saved_txt,status_st,columns,status)

        else: #All the other keys
            if key==b'\t': #Tab fix
                fix=tab_size
                out=" "*tab_size
            else: fix=1; out=decode(key)
            p1=text[:pointer+p_offset-1]
            p2=text[pointer+p_offset-1:]
            text=(p1+out+p2)
            if p_offset==0 and not pointer+fix>columns: pointer+=fix
            elif not p_offset+pointer>len(text)+2: p_offset+=fix
            else: pointer+=fix

        status_st-=1
    #except: pass
