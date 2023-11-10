#Code by Sergio1260

def decode(key):
    for x in range(3):
        try: out=key.decode("UTF-8"); break
        except: key+=getch()
    return out

def fixlenline(text, pointer, oldptr):
    length=len(text)
    if pointer>length or oldptr>length:
        return length,oldptr
    elif oldptr>pointer: return oldptr,oldptr
    else: return pointer,oldptr

def down(line, offset, arr, text, banoff, oldptr, rows, pointer):
    if not line+offset==len(arr)+banoff-1:
        if not line==rows+banoff: line+=1
        elif not line+offset==len(arr)+1: offset+=1
        text=arr[line+offset-banoff]
        pointer,oldptr=fixlenline(text, pointer, oldptr)
    return pointer, oldptr, text, offset, line

def up(line, offset, arr, text, banoff, oldptr, rows, pointer):
    if not line==banoff: line-=1
    elif offset>0: offset-=1
    text=arr[line+offset-banoff]
    pointer,oldptr=fixlenline(text, pointer, oldptr)   
    return pointer, oldptr, text, offset, line

def fix_line(text, p_offset, black, reset, columns):
    if len(text)>columns:
        if p_offset < 0:
            p_offset = 0
        if p_offset + columns > len(text):
            p_offset = len(text) - columns+1
        fix_text = text[p_offset:p_offset + columns]

        if p_offset > 0:
            fix_text=black+'<'+reset+fix_text[1:]
        if p_offset+columns<len(text):
            fix_text=fix_text[:-1]+black+'>'+reset
    else: fix_text=text
    return fix_text

def fix_scr(arr, org_arr, p_offset, black, reset, columns, line, offset, banoff):
    out=[]
    for x in arr: out.append(fix_line(x, 0, black, reset, columns))
    x=org_arr[line+offset-banoff]
    out[line-banoff]=fix_line(x, p_offset, black, reset, columns)
    return "\n".join(out)
    
        
