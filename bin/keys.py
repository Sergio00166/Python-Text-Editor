#Code by Sergio1260

from special_keys import special_keys
from functions1 import *
from functions2 import *
from saveas import save_as
from openfile import open_file

def keys(key,text,pointer,p_offset,oldptr,line,offset,columns,banoff,arr,rows,max_len,filename,status,status_st,copy_buffer,fixstr,fix,black,reset,saved_txt):
        
        if key==b'\xe0': #Special Keys
            text, pointer, p_offset, oldptr, line, offset, status_st =\
            special_keys(pointer,p_offset,text,columns,offset,line,banoff,arr,rows,oldptr,max_len,status_st)
            
        elif key==b'\x08': #Delete
            line, offset, text, arr, pointer, p_offset =\
            delete(pointer, text, offset, line, arr, banoff, p_offset)
            status_st=False

        elif key==b'\r': #Return (adds new lines or moves text
            line, offset, arr, pointer, text =\
            newline(text, pointer, offset, banoff, line, arr, rows, p_offset)
            status_st=False

        elif key==b'\x13': #Ctrl + S (SAVE)
            out=open(filename,"w",encoding="UTF-8")
            out.write("\n".join(arr)); out.close()
            status=saved_txt; status_st=True

        elif key==b'\x18': #Ctrl + X (CUT LINE)
            copy_buffer=arr[line+offset-banoff][pointer+p_offset-1:]
            out=arr[line+offset-banoff][:pointer+p_offset-1]
            arr[line+offset-banoff]=text=out
            status_st=False
            
        elif key==b'\x03': #Ctrl + C (COPY LINE)
            copy_buffer=arr[line+offset-banoff][pointer+p_offset-1:]
            
        elif key==b'\x10': #Ctrl + P (PASTE TEXT)
            if not len(copy_buffer)==0:
                p1=arr[:line+offset-banoff]; p2=arr[line+offset-banoff+1:]
                fix1=text[:p_offset+pointer-1]; fix2=text[p_offset+pointer-1:]
                out=fix1+copy_buffer+fix2; arr=p1+[out]+p2; text=out
                status_st=False
        
        elif key==b'\x07': #Ctrl + G (go to line)
            line, offset, text = goto(rows, banoff, line, arr, offset, black, reset)

        elif key==b'\x01': #Ctrl + A (Save as)
            arr, status_st, filename, status =\
            save_as(filename,black,reset,rows,banoff,arr,saved_txt,status_st,columns,status)

        elif key==b'\x0f': #Ctlr + O (Open file)
            arr, filename = open_file(\
            filename,black,reset,rows,banoff,arr,columns)
        
        else: #All the other keys
            if not str(key)[4:6] in fixstr:
                out=decode(key)
                p1=text[:pointer+p_offset-1]
                p2=text[pointer+p_offset-1:]
                text=(p1+out+p2)
                if key==b'\t': #Tab fix
                    fix=tab_len(pointer+p_offset,text)
                    out=" "*fix; text=(p1+out+p2)
                else: fix=1
                
                if p_offset==0 and not pointer+fix>columns: pointer+=fix
                elif not p_offset+pointer>len(text)+2: p_offset+=fix
                else: pointer+=fix
                status_st=False

        return text,pointer,p_offset,oldptr,line,offset,columns,banoff,arr,rows,max_len,filename,status,status_st,copy_buffer,fixstr,fix

