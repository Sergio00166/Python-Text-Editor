#Code by Sergio1260

from msvcrt import getch
from os import get_terminal_size
from sys import path
path.append(path[0]+"\\lib.zip")
from wcwidth import wcwidth


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

def fix_cursor_pos(text, pointer):
    lenght_arr=[]
    pointer-=1
    #Generate arr lenght dictionary
    for x in text[:pointer]:
        if x=="\t":
            lenght_arr.append(tab_len(text.index(x),text))
        else: lenght_arr.append(wcwidth(x))

    return sum(lenght_arr)+1

def decode(key):
    for x in range(3):
        try: out=key.decode("UTF-8"); break
        except: key+=getch()
    return out

def get_size():
    size=get_terminal_size()
    return size[1]-4,size[0]-2

def update_scr(black,reset,legacy,status,p_offset,banoff,offset,line,pointer,arr,banner,filename,bottom,rows,columns):
    position=black+"  "+str(line+offset-banoff)+" "*(4-len(str(line+offset-banoff)))
    all_file="\n".join(arr[offset:rows+offset+1])
    outb=position+black+" "*5+reset+status+banner
    outb=position+black+" "+reset+status+banner
    if not legacy: cls="\033c"
    else: cls=("\r\033[%d;%dH"%(rows+4, columns+2))+"\n"
    fix=("\r\033[%d;%dH"%(1, 1))
    print(cls+"\n"*(rows+3)+bottom, end="")
    print(fix+outb+black+" "*(columns-27-len(filename))+reset, end="")
    print(black+filename+reset+black+" "+reset+"\n"+all_file, end="")

    pointer = fix_cursor_pos(arr[line+offset-1], pointer)
    
    print(("\r\033[%d;%dH"%(line+1, pointer)), end="")
    
def fix_line(text, black, reset, columns):
    if len(text)>columns:
        if p_offset < 0: p_offset = 0
        if p_offset + columns > len(text): p_offset = len(text) - columns+1
        fix_text = text[p_offset:p_offset + columns]
        if p_offset > 0: fix_text=black+'<'+reset+fix_text[1:]
        if p_offset+columns<len(text): fix_text=fix_text[:-1]+black+'>'+reset
    else: fix_text=text
    return fix_text

def fixlenline(text, pointer, oldptr):
    length=len(text)+1
    if pointer>length or oldptr>length:
        return length,oldptr
    elif oldptr>pointer: return oldptr,oldptr
    else: return pointer,oldptr

