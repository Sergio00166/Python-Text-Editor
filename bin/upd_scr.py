# Code by Sergio1260

from functions import fix_cursor_pos, get_size, fixfilename, arr2str, fix_arr_line_len, str_len
from os import sep

if not sep==chr(92): import termios; import tty


def update_scr(black,reset,status,banoff,offset,line,pointer,arr,banner,filename,rows,columns):
    position=black+"  "+str(line+offset-banoff)+" "*(4-len(str(line+offset-banoff)))
    all_file,pointer = arr2str(arr,columns,rows,line,offset,black,reset,pointer)
    cls="\r\033[%d;%dH"%(1, 1); gpos="\r\033[%d;%dH"%(line+1, pointer)
    filename = fixfilename(filename, columns)
    banner=position+black+" "+reset+status+banner+black+"    "
    banner+=" "*(columns-31-len(filename))+filename+" "+reset+"\n"
    
    print(cls+banner+all_file+gpos, end="", flush=True)
    
    
def updscr(arg,mode=None):
    black,reset,status,banoff,offset,line,\
    pointer,arr,banner,filename,rows,columns=arg
    # Save old vars and get new values
    old_rows=rows; old_columns=columns
    rows,columns=get_size()
    # Check if terminal is too small
    if rows<4: print("\r\033cTerminal too small")
    # Compare the old values with the new ones
    elif not (old_rows==rows and old_columns==columns):
        # Increment the offset if line is geeter than rows
        if line>rows: offset=offset+(line-rows); line=rows	
        print("\r\033c",end="") #Clear screen
        # If OS is LINUX restore TTY to it default values
        if not sep==chr(92): termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        # Call screen updater function
        update_scr(black,reset,status,banoff,offset,line,pointer,arr,banner,filename,rows,columns)
        if not mode==None:
            filetext,opentxt,wrtptr,lenght = mode
            out=opentxt+filetext
            full=columns-len(out)+2
            fix=len(out)//(columns+2)
            update_scr(black,reset,status,banoff,\
            offset,line,0,arr,banner,filename,rows,columns)
            print("\r\033[%d;%dH"%(rows+banoff+2, 1),end="")
            print("\r"+black+" "*(columns+2)+reset, end="")
            print("\r\033[%d;%dH"%(rows+banoff+2-fix, 1),end="")
            print("\r"+black+out+(" "*full)+reset,end="")
            print("\r\033[%d;%dH"%(rows+banoff+2-fix, wrtptr-1),end="")
        # If OS is LINUX set TTY to raw mode
        if not sep==chr(92): tty.setraw(fd)
    return rows,columns
