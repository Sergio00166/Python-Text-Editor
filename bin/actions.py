#Code by Sergio1260

from functions import *

def supr(pointer,offset,banoff,arr,line):
        text=arr[line+offset-banoff]
        if not pointer==len(text)+1:
            p1=list(text); p1.pop(pointer-1)
            arr[line+offset-banoff]="".join(p1)
        elif not line+offset==1: #move all to previous line
            seltext=arr[line+offset-banoff+1]
            arr[line+offset-banoff+1]=text+seltext
            arr.pop(line+offset-banoff+1)
            arr[line+offset-banoff]=text+seltext
        return arr

def down(line,offset,arr,banoff,oldptr,rows,pointer):
    if not line+offset==len(arr)+banoff-1:
        if not line==rows+banoff: line+=1
        elif not line+offset==len(arr)+1: offset+=1
        text=arr[line+offset-banoff]
        pointer,oldptrt=fixlenline(text,pointer,oldptr)
    return pointer, oldptr, offset, line

def up(line,offset,arr,banoff,oldptr,rows,pointer):
    if not line==banoff: line-=1
    elif offset>0: offset-=1
    text=arr[line+offset-banoff]
    pointer,oldptr=fixlenline(text,pointer,oldptr) 
    return pointer, oldptr, offset, line

def backspace(pointer,offset,line,arr,banoff):
    text=arr[line+offset-banoff]
    if not pointer==1: #Delete char   
        p1=list(text)+[""]
        p1.pop(pointer-2)
        arr[line+offset-banoff]="".join(p1)
        pointer-=1
        
    else: #move all to previous line
        if not offset+line==1:
            seltext=arr[line+offset-banoff-1]
            arr[line+offset-banoff-1]=seltext+text
            arr.pop(line+offset-banoff)
            pointer=len(seltext)+1
            arr[line+offset-banoff]=seltext+text
            if not offset==0: offset-=1
            else: line-=1
    return line, offset, arr, pointer

def newline(pointer, offset, banoff, line, arr, rows):
    p1=arr[:line+offset-banoff]
    p2=arr[line+offset-banoff:]
    text=arr[line+offset-banoff]
    #if not len(text)==0:
    seltext=[text[:pointer-1]]
    arr=p1+seltext+p2
    arr[line+offset-banoff]=text[pointer-1:]
    pointer=0
    #else: arr=p1+[""]+p2
    if not line>rows: line+=1
    else: offset+=1
    return line, offset, arr, pointer

def left(pointer,oldptr,line,offset,banoff,arr):
    max_len=len(arr[line+offset-banoff])
    if not pointer==1: pointer-=1; oldptr=pointer
    elif not line+offset==1:
        if offset==0: line-=1
        else: offset-=1
        pointer=max_len+1
    return pointer, oldptr, line, offset

def right(pointer,columns,offset,line,banoff,arr,rows,oldptr):
    max_len=len(arr[line+offset-banoff])
    if not pointer>max_len:
        pointer+=1
        oldptr=pointer
    else:
        if not offset+line>len(arr)-1:
            if not line>rows-2: line+=1
            else: offset+=1
            pointer=1
    return pointer, oldptr, line, offset

def goto(rows, banoff, line, arr, offset, black, reset):
    print("\r\033[%d;%dH"%(rows+banoff+2,1),end="")
    print(" "+black+"Go to line:"+reset, end=" "); p1=input()
    print("\r\033[%d;%dH"%(line, 1),end="")
    line,offset = CalcRelLine(p1,arr,offset,line,banoff,rows)
    print("\033c", end="")
    return line, offset

