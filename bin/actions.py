# Code by Sergio00166

from functions1 import *


def down(line,offset,arr,banoff,oldptr,rows,cursor,select,selected):
    if selected:
        selst=[line-banoff,offset]
        fix=line+offset
    if not line+offset==len(arr)+banoff-1:
        if not line==rows+banoff: line+=1
        elif not line+offset==len(arr)+1: offset+=1
        text=arr[line+offset-banoff]
        cursor=fixlenline(text,cursor,oldptr)
    if selected:
        seled=[line-banoff,offset]
        if sum(seled)<fix:
            seled[0]=seled[0]+1
        if len(select)==0:
            select=[selst,seled]
        else: select[1]=seled
    else: select=[]
    return cursor, oldptr, offset, line, select

def up(line,offset,arr,banoff,oldptr,rows,cursor,select,selected):
    if selected: seled=[line-banoff,offset]
    if not line==banoff: line-=1
    elif offset>0: offset-=1
    text=arr[line+offset-banoff]
    cursor=fixlenline(text,cursor,oldptr)
    if selected:
        selst=[line-banoff,offset]
        if len(select)==0:
            select=[selst,seled]
        else: select[0]=selst
    else: select=[]
    return cursor, oldptr, offset, line, select

def left(cursor,oldptr,line,offset,banoff,arr):
    if not cursor==1: cursor-=1; oldptr=cursor
    elif not line+offset==1:
        if offset==0: line-=1
        else: offset-=1
        text=arr[line+offset-banoff]
        cursor=len(text)+1
    return cursor, oldptr, line, offset

def right(cursor,columns,offset,line,banoff,arr,rows,oldptr):
    text=arr[line+offset-banoff]
    if not cursor>len(text):
        cursor+=1
        oldptr=cursor
    else:
        if not offset+line>len(arr)-1:
            if not line>rows-2: line+=1
            else: offset+=1
            cursor=1
    return cursor, oldptr, line, offset

def backspace(cursor,offset,line,arr,banoff,select):
    text=arr[line+offset-banoff]
    if len(select)==0:
        if not cursor==1: #Delete char
            p1=list(text)+[""]
            # Fix weird bug
            try: p1.pop(cursor-2)
            except: p1.pop(cursor-1)
            text="".join(p1)
            cursor-=1
        else: #move all to previous line
            if not offset+line==1:
                seltext=arr[line+offset-banoff-1]
                arr[line+offset-banoff-1]=seltext+text
                arr.pop(line+offset-banoff)
                cursor=len(seltext)+1
                text=seltext+text
                if not offset==0: offset-=1
                else: line-=1
                status_st=False
        arr[line+offset-banoff]=text
    else: select,arr,line,offset = del_sel(select,arr,banoff)
    return line, offset, arr, cursor, select

def goto(columns, rows, banoff, line, arr, offset, black):
    try:
        default = str(line+offset-banoff)
        p1 = chg_var_str(columns,rows,banoff,line,black,default,"Go to")
        p1 = len(arr)-1 if p1=="-" else int(p1)
        line,offset = CalcRelLine(p1,arr,offset,line,banoff,rows)
    except: pass
    return line, offset

def newline(cursor,offset,banoff,line,arr,rows,status,select):
    if not len(select)==0:
        select,arr,line,offset = del_sel(select,arr,banoff)
    text=arr[line+offset-banoff]
    p1=arr[:line+offset-banoff]
    p2=arr[line+offset-banoff:]
    if not len(text)==0:
        fix=1
        seltext=[text[:cursor-fix]]
        arr=p1+seltext+p2
        text=text[cursor-fix:]
        cursor=1
    else: arr=p1+[""]+p2
    if not line>rows: line+=1
    else: offset+=1
    status_st=False
    arr[line+offset-banoff]=text
    return line, offset, arr, cursor, status, select

def dedent(arr,line,offset,banoff,indent,cursor):
    text = arr[line+offset-banoff]
    p1 = text[:cursor-1]
    p2 = text[cursor-1:]
    if len(indent)>0 and p1.endswith(indent):
        p1 = p1[:-len(indent)]
        cursor-=len(indent)
        arr[line+offset-banoff] = p1+p2
    return arr,cursor

