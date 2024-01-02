#Code by Sergio1260

from os import get_terminal_size
from msvcrt import getch
from sys import path
path.append(path[0]+"\\lib.zip")
from wcwidth import wcwidth


def wrap(text, columns):
    out=[]; counter=-1; buffer=""
    for x in text:
        if counter>=columns-1:
            lenght=str_len(x)
            if lenght>1:
                ext=buffer
                buffer=x
            else:
                ext=buffer+x
                buffer=""
                
            out.append(ext)
            counter=0
        else:
            buffer+=x
            counter+=str_len(x)
    if not buffer=="": out.append(buffer)
    return out

def decode(key):
    for x in range(3):
        try: out=key.decode("UTF-8"); break
        except: key+=getch()
    return out

def get_size():
    size=get_terminal_size()
    return size[1]-3,size[0]-2

def fix_arr_line_len(arr, columns, black, reset):
    out=[]; fix=0//(columns+2)
    for text in arr:
        wrapped_text = wrap(text,columns)
        if len(wrapped_text)==0: wrapped_text=""
        elif fix==len(wrapped_text):
            text=wrapped_text[fix-1]
        else: text=wrapped_text[fix]
        if (len(wrapped_text)-fix)>1:
            text+=black+">"+reset
        out.append(text)   
    return out

def str_len(text,pointer=None):
    lenght=0
    if not pointer==None:
        fix=text[:pointer-1]
    else: fix=text
    fix=fix.expandtabs(8)
    for x in fix: lenght+=wcwidth(x)
    return lenght

def fixlenline(text, pointer, oldptr):
    length=len(text)+1
    if pointer>length or oldptr>length:
        return length,oldptr
    elif oldptr>pointer: return oldptr,oldptr
    else: return pointer,oldptr


def fix_cursor_pos(text,pointer,columns,black,reset):
    
    len_arr=[]; ptr=pointer; pos=0
    pointer=str_len(text,pointer)
    
    fix=pointer//(columns+2)
    wrapped_text = wrap(text,columns)
    
    for x in wrapped_text:
        if pointer-str_len(x)<1:
            break
        else: pos+=1
        pointer-=str_len(x)

    if pos>0: pointer+=1
    
    if len(wrapped_text)==0:
        wrapped_text==""
    else: text=wrapped_text[pos]
    if fix>0: text=black+"<"+reset+text
    if (len(wrapped_text)-fix)>1:
        text+=black+">"+reset

    return pointer+1, text

def update_scr(black,reset,status,banoff,offset,line,pointer,arr,banner,filename,rows,columns):
    
    position=black+"  "+str(line+offset-banoff)+" "*(4-len(str(line+offset-banoff)))
    text=arr[line+offset-1]
    pointer, text = fix_cursor_pos(text,pointer,columns,black,reset)
    out_arr=arr[offset:rows+offset+1]
    out_arr=fix_arr_line_len(out_arr, columns, black, reset)
    out_arr[line-1]=text
    all_file="\n".join(out_arr).expandtabs(8)
    outb=position+black+" "+reset+status+banner
    outb=outb+black+"    "+reset
    
    cls="\033c"
    
    if len(filename)+31>columns: #If filename overflows
        flfix=filename.split("\\")
        filename=flfix[len(flfix)-1]
        if len(filename)+31>columns: #If still not fiting
            filename=filename[:5]+"*"+filename[len(filename)-4:]
            
    print(cls+outb+black+" "*(columns-31-len(filename))+reset, end="")
    print(black+filename+reset+black+" "+reset+"\n"+all_file, end="")
    print(("\r\033[%d;%dH"%(line+1, pointer)), end="")




