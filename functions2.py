#Code by Sergio1260


def newline(text, pointer, offset, banoff, line, arr, rows, p_offset):
    p1=arr[:line+offset-banoff]
    p2=arr[line+offset-banoff:]
    if not len(text)==0:
        if p_offset>0: fix=2
        else: fix=1
        seltext=[text[:pointer+p_offset-fix]]
        arr=p1+seltext+p2
        text=text[pointer+p_offset-fix:]
        pointer=0
    else: arr=p1+[""]+p2
    if not line>rows+1: line+=1
    else: offset+=1
    return line, offset, arr, pointer, text

def supr(pointer, max_len, text, offset, banoff, arr, line, p_offset):
    if not pointer==max_len+1:
        p1=list(text); p1.pop(pointer+p_offset-1)
        text="".join(p1)
    elif not line+offset==1: #move all to previous line
        seltext=arr[line+offset-banoff+1]
        arr[line+offset-banoff+1]=text+seltext
        arr.pop(line+offset-banoff+1)
        text=text+seltext
    return text, arr

def delete(pointer, text, offset, line, arr, banoff, p_offset):
    if not pointer==1: #Delete char
        p1=list(text)+[""]
        if p_offset>0: fix=1
        else: fix=0
        p1.pop(pointer+p_offset-2-fix)
        text="".join(p1)
        if p_offset==0: pointer-=1
        else: p_offset-=1
    else: #move all to previous line
        if not offset+line==1:
            seltext=arr[line+offset-banoff-1]
            arr[line+offset-banoff-1]=seltext+text
            arr.pop(line+offset-banoff)
            pointer=len(seltext)+1
            text=seltext+text
            if not offset==0: offset-=1
            else: line-=1
    return line, offset, text, arr, pointer, p_offset

def left(pointer,oldptr,line,offset,banoff,columns,p_offset,text,arr):
    if not pointer==1: pointer-=1; oldptr=pointer
    elif not p_offset==0: p_offset-=1; oldptr=pointer
    elif not line+offset==1:
        if offset==0: line-=1
        else: offset-=1
        text=arr[line+offset-banoff]
        pointer=len(text)+1
        if pointer>columns+2:
            p_offset=len(text)-columns+2
            pointer=columns
    return pointer, oldptr, p_offset, text, line, offset

def right(pointer,p_offset,text,columns,offset,line,banoff,arr,rows,oldptr):
    if not pointer+p_offset>len(text):
        if not pointer>columns-1: pointer+=1
        else: p_offset+=1
        oldptr=pointer
    else:
        if not line>rows-2: line+=1
        else: offset+=1
        pointer=1; p_offset=0
        text=arr[line+offset-banoff]
    return text, pointer, p_offset, oldptr, line, offset

