# Code by Sergio00166

from actions import *
from actions1 import *
from saveas import save_as
from openfile import open_file
from find_str import find
from replace_str import replace
from chg_var_str import chg_var_str
from opt_menu import opt_menu
from show_help import show_help


def keys_func(key,cursor,oldptr,line,offset,columns,banoff,arr,rows,
              filename,status,status_st,copy_buffer,black,bnc,slc,reset,
              saved_txt,indent,banner,read_key,keys,select,codec,lnsep,comment):

    if key==keys["supr"]:
        args=(cursor,offset,banoff,arr,line,select)
        arr, line, offset, select = supr(*args)
        status_st = False

    elif key==keys["arr_up"] or key==keys["ctrl+arr_up"]:
        selected = key==keys["ctrl+arr_up"]
        args=(line,offset,arr,banoff,oldptr,rows,cursor,select,selected)
        cursor, oldptr, offset, line, select = up(*args)
        
    elif key==keys["arr_down"] or key==keys["ctrl+arr_down"]:
        selected = key==keys["ctrl+arr_down"]
        args=(line,offset,arr,banoff,oldptr,rows,cursor,select,selected)
        cursor, oldptr, offset, line, select = down(*args)

    elif key==keys["arr_right"] or key==keys["ctrl+arr_right"]:
        times = 4 if key==keys["ctrl+arr_right"] else 1
        for x in range(times):
            args=(cursor,columns,offset,line,banoff,arr,rows,oldptr)
            cursor, oldptr, line, offset = right(*args)
        select=[]
        
    elif key==keys["arr_left"] or key==keys["ctrl+arr_left"]:
        times = 4 if key==keys["ctrl+arr_left"] else 1
        for x in range(times):
            args=(cursor,oldptr,line,offset,banoff,arr)
            cursor,oldptr,line,offset = left(*args)
        select=[]
        
    elif key in keys["start"]: cursor,oldptr,select = 1,1,[]
        
    elif key in keys["end"]:
        text=arr[line+offset-banoff]
        cursor = len(text)+1
        oldptr,select = cursor,[]
        
    elif key==keys["repag"] or key==keys["ctrl+repag"]:
        fix = key==keys["ctrl+repag"]
        args=(line,offset,banoff,rows,arr,sep,cursor,oldptr,select,fix)
        line,offset,cursor,oldptr,select = repag(*args)
        
    elif key==keys["avpag"] or key==keys["ctrl+avpag"]:
        fix = key==keys["ctrl+avpag"]
        args=(line,offset,banoff,rows,arr,sep,cursor,oldptr,select,fix)
        line,offset,cursor,oldptr,select = avpag(*args)
            
    elif key==keys["delete"]:
        args=(cursor,offset,line,arr,banoff,select)
        line,offset,arr,cursor,select = backspace(*args)
        status_st = False

    elif key==keys["return"]:
        args=(cursor,offset,banoff,line,arr,rows,status,select)
        line,offset,arr,cursor,staus,select = newline(*args)
        status_st = False

    elif key==keys["ctrl+s"]:
        out=open(filename,"w",encoding=codec,newline='')
        out.write(lnsep.join(arr)); out.close()
        status=saved_txt; status_st=True
        
    elif key==keys["ctrl+x"]:
        args=(select,arr,line,offset,banoff,copy_buffer,cursor)
        copy_buffer,arr,line,offset,select = cut(*args)
        status_st = False
        
    elif key==keys["ctrl+c"]:
        args=(select,arr,line,offset,banoff,cursor)
        copy_buffer = copy(*args)
        
    elif key==keys["ctrl+p"]:
        args=(copy_buffer,arr,line,offset,banoff,cursor,select,rows,status_st)
        cursor,arr,copy_buffer,line,offset,select,status_st = paste(*args)
            
    elif key==keys["ctrl+g"]:
        args = (filename,black,bnc,slc,reset,rows,banoff,arr,columns,status,offset,line,\
                banner,status_st,keys,cursor,select,read_key,""," Go to: ")
        p1 = chg_var_str(args) # Get user input
        p1 = len(arr)-1 if p1 == "-" else int(p1) if p1.isdigit() else line+offset-banoff
        line,offset = CalcRelLine(p1,arr,offset,line,banoff,rows)

    elif key==keys["ctrl+a"]:
        args = (filename,black,bnc,slc,reset,rows,banoff,arr,columns,status,\
                offset,line,banner,status_st,saved_txt,keys,read_key,codec,lnsep)
        status_st,filename,status,codec,lnsep = save_as(args)

    elif key==keys["ctrl+o"]:
        args = (filename,black,bnc,slc,reset,rows,banoff,arr,columns,status,offset,\
                line,banner,status_st,keys,cursor,oldptr,select,read_key,codec,lnsep)
        arr,filename,status_st,cursor,oldptr,line,offset,select,codec,lnsep = open_file(args)

    elif key==keys["ctrl+f"]:
        args = (filename,black,bnc,slc,reset,rows,banoff,arr,columns,\
                status,offset,line,banner,status_st,keys,read_key,cursor)
        cursor,line,offset = find(args)

    elif key==keys["ctrl+r"]:
        args = (filename,black,bnc,slc,reset,rows,banoff,arr,columns,\
                status,offset,line,banner,status_st,keys,read_key,cursor)
        cursor,line,offset,arr,status_st = replace(args)  

    elif key==keys["ctrl+d"]:
        if len(select)>0:
            arr = select_add_start_str(arr,line,offset,select,indent,True)
        else: arr,cursor = dedent(arr,line,offset,banoff,indent,cursor)
    
    elif key==keys["ctrl+k"]:
        if len(select)>0: slt = select
        else:
            slt = [[line-banoff,offset],[line,offset]]
            cursor += len(comment[0])
        arr = select_add_start_str(arr,line,offset,slt,comment)
    
    elif key==keys["ctrl+u"]:    
        if len(select)>0: slt = select
        else: 
            slt = [[line-banoff,offset],[line,offset]]
            x = arr[line+offset-banoff]
            if x.startswith(comment[0]) and x.endswith(comment[1]):
                cursor -= len(comment[0])
        arr = select_add_start_str(arr,line,offset,slt,comment,True)

    elif key==keys["ctrl+t"]:
        args = (filename,black,bnc,slc,reset,rows,banoff,arr,columns,status,offset,\
                line,banner,status_st,keys,cursor,select,read_key,comment,indent)
        comment,indent = opt_menu(args)

    elif key==keys["help"]:
        text = "^Q [Quit], ^S [Save], ^A [Save as], ^O [Open], ^C [Copy], ^X [Cut], ^P [Paste], ^G [GOTO]"
        text += ", ^D [Dedent], ^I [Ident], ^K [Comment], ^U [Uncomment], ^F [Find], ^R [Replace]"
        args = (filename,black,bnc,slc,reset,rows,banoff,arr,columns,\
                status,offset,line,banner,status_st,keys,read_key,text)
        show_help(args)

    else: #All the other keys
        args=(arr,key,select,cursor,line,offset,banoff,indent,rows,keys)
        arr, cursor, line, offset, select = get_str(*args)
        status_st = False
                
    return cursor,oldptr,line,offset,columns,banoff,arr,rows,filename,\
           status,status_st,copy_buffer,indent,select,codec,lnsep,comment

