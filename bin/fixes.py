#Code by Sergio1260

from msvcrt import getch
from os import get_terminal_size
from sys import path
path.append(path[0]+"\\lib.zip")
from wcwidth import wcwidth
from textwrap import wrap

def tab_len(pointer,text):
    fix=text[:pointer+1]+"\f"+text[pointer+1:]
    fix=fix.expandtabs(8); length=fix[pointer:]
    length=length[:length.find("\f")]   
    return len(length)

def text_real_size(text):
    lenght=0
    for x in text:
        if x=="\t": lenght+=tab_len(text.index(x),text)
        else: lenght+=wcwidth(x)
    return lenght

def fix_cursor_pos(text,pointer,columns,black,reset):
    len_arr=[]; ptr=pointer
    #Generate arr lenght dictionary
    for x in text[:pointer-1]:
        if not x=="\t": len_arr.append(wcwidth(x))
        else: len_arr.append(tab_len(text.index(x),text))
    pointer=sum(len_arr)
    fix=pointer//columns
    wrapped_text = wrap(text,columns)
    if len(text)==0: text=""
    elif fix==len(wrapped_text):
        text=wrapped_text[fix-1]
    else: text=wrapped_text[fix]
    if (len(wrapped_text)-fix)>1: text+=black+">"+reset
    if fix>0: text=black+"<"+reset+text
    pointer-=(fix*columns)
    if fix>0: pointer+=1
    return pointer+1, text

def fix_arr_line_len(arr, columns, black, reset):
    out=[]
    for x in arr:
        bigger=text_real_size(x)>columns
        if bigger: out.append(x[:columns-1]+black+">"+reset)
        else: out.append(x)
    return out

def decode(key):
    for x in range(3):
        try: out=key.decode("UTF-8"); break
        except: key+=getch()
    return out

def get_size():
    size=get_terminal_size()
    return size[1]-4,size[0]-2

def update_scr(black,reset,legacy,status,banoff,offset,line,pointer,arr,banner,filename,bottom,rows,columns):
    position=black+"  "+str(line+offset-banoff)+" "*(4-len(str(line+offset-banoff)))
    text=arr[line+offset-1]
    pointer, text = fix_cursor_pos(text,pointer,columns,black,reset)
    out_arr=arr[offset:rows+offset+1]
    out_arr=fix_arr_line_len(out_arr, columns, black, reset)
    out_arr[line-1]=text
    all_file="\n".join(out_arr)
    outb=position+black+" "*5+reset+status+banner
    outb=position+black+" "+reset+status+banner
    if not legacy: cls="\033c"
    else: cls=("\r\033[%d;%dH"%(rows+4, columns+2))+"\n"
    fix=("\r\033[%d;%dH"%(1, 1))
    print(cls+"\n"*(rows+3)+bottom, end="")
    print(fix+outb+black+" "*(columns-27-len(filename))+reset, end="")
    print(black+filename+reset+black+" "+reset+"\n"+all_file, end="")
    print(("\r\033[%d;%dH"%(line+1, pointer)), end="")

def fixlenline(text, pointer, oldptr):
    length=len(text)+1
    if pointer>length or oldptr>length:
        return length,oldptr
    elif oldptr>pointer: return oldptr,oldptr
    else: return pointer,oldptr



