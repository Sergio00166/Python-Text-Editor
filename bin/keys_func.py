#Code by Sergio1260

from functions import *
from actions import *
from saveas import save_as
from openfile import open_file

def keys_func(key,pointer,oldptr,line,offset,columns,banoff,arr,rows,filename,status,status_st,copy_buffer,fixstr,fix,black,reset,saved_txt,ch_T_SP,banner,getch,keys):
        
    if key==keys["special"]:
        if not sep==chr(92): special_key=getch()
        special_key=getch() #Read char
        if special_key==keys["arr_up"]: pointer,oldptr,offset,line = up(line,offset,arr,banoff,oldptr,rows,pointer)
        elif special_key==keys["arr_down"]: pointer,oldptr,offset,line = down(line,offset,arr,banoff,oldptr,rows,pointer)
        elif special_key==keys["arr_right"]: pointer,oldptr,line,offset =  right(pointer,columns,offset,line,banoff,arr,rows,oldptr)          
        elif special_key==keys["arr_left"]: pointer,oldptr,line,offset = left(pointer,oldptr,line,offset,banoff,arr)     
        elif special_key==keys["supr"]: arr = supr(pointer,offset,banoff,arr,line); status_st=False
        elif special_key==keys["start"]:  pointer=1; p_offset=0; oldptr=pointer    
        elif special_key==keys["end"]: pointer=len(arr[line+offset-banoff])+1; oldptr=pointer
        elif special_key==b'I' and not offset-rows<0: offset-=rows
        elif special_key==b'Q' and not pointer+offset+rows>len(arr): offset+=rows
        
    elif key==keys["delete"]:
        line, offset, arr, pointer =\
        backspace(pointer,offset,line,arr,banoff)
        status_st=False
        
    elif key==keys["return"]:
        line, offset, arr, pointer =\
        newline(pointer,offset,banoff,line,arr,rows)
        status_st=False
        
    elif key==keys["ctrl+s"]:
        out=open(filename,"w",encoding="UTF-8")
        out.write("\n".join(arr)); out.close()
        status=saved_txt; status_st=True
        out=open(filename,"r",encoding="UTF-8")
        
    elif key==keys["ctrl+x"]:
        if line+offset>len(arr)-1:
            copy_buffer=text[pointer-1:]
        else:
            copy_buffer=arr[line+offset-banoff]
            arr.pop(line+offset-banoff)
        status_st=False
        
    elif key==keys["ctrl+c"]:
        copy_buffer=arr[line+offset-banoff][pointer-1:]
        
    elif key==keys["ctrl+p"]:
        text=arr[offset:offset+rows]
        if not len(copy_buffer)==0:
            p1=arr[:line+offset-banoff]; p2=arr[line+offset-banoff+1:]
            fix1=text[:pointer-1]; fix2=text[pointer-1:]
            out=fix1+copy_buffer+fix2; arr=p1+[out]+p2; text=out
            pointer=len(fix1+copy_buffer)
            status_st=False

    elif key==keys["ctrl+g"]:
        line,offset = goto(rows,banoff,line,arr,offset,black,reset)

    elif key==keys["ctrl+a"]:
        args=(filename,black,reset,rows,banoff,arr,columns,\
        status,offset,line,banner,status_st,saved_txt,getch,keys)
        status_st, filename, status = save_as(args)

    elif key==keys["ctrl+o"]:
        args = (filename,black,reset,rows,banoff,arr,columns,\
        status,offset,line,banner,status_st,getch,keys,pointer)
        arr,filename,status_st,pointer,line,offset = open_file(args)
        text=arr[line+offset-1]
        
    elif key==keys["ctrl+t"]:
        if ch_T_SP: ch_T_SP=False
        else: ch_T_SP=True

    else: #All the other keys
        if not str(key)[4:6] in fixstr:
            out=decode(key,getch)
            text=arr[line+offset-banoff]
            p1=text[:pointer-1]
            p2=text[pointer-1:]
            if out=="\t" and ch_T_SP:
                out=" "*4
                pointer+=3
            arr[line+offset-banoff]=(p1+out+p2)
            pointer+=1
            status_st=False

    return pointer,oldptr,line,offset,columns,banoff,arr,rows,filename,status,status_st,copy_buffer,fixstr,fix,ch_T_SP

