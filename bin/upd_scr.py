# Code by Sergio1260

from functions import fix_cursor_pos, get_size, fixfilename, fix_arr_line_len, scr_arr2str
from os import sep

if not sep==chr(92): import termios; import tty


def update_scr(black,reset,status,banoff,offset,line,pointer,arr,banner,filename,rows,columns,rrw=False):
    position=black+"  "+str(line+offset-banoff)+" "*(4-len(str(line+offset-banoff)))
    cls="\r\033[%d;%dH"%(1, 1)
    outb=position+black+" "+reset+status+banner+black+"    "+reset
    filename = fixfilename(filename, columns)
    all_file,pointer = scr_arr2str(arr,line,offset,pointer,black,reset,columns,rows)
    menu=cls+outb+black+" "*(columns-31-len(filename))
    menu+=filename+" "+reset+"\n"+all_file
    
    if rrw: return menu
    else:
        menu+=("\r\033[%d;%dH"%(line+1, pointer))
        print(menu, end="")


def menu_updsrc(arg,mode=None,updo=False):
    black,reset,status,banoff,offset,line,\
    pointer,arr,banner,filename,rows,columns=arg
    # Save old vars and get new values
    old_rows=rows; old_columns=columns
    rows,columns=get_size()
    # Check if terminal is too small
    if rows<4: print("\r\033cTerminal too small")
    # Compare the old values with the new ones
    elif not (old_rows==rows and old_columns==columns) or updo:
        # Increment the offset if line is geeter than rows
        if line>rows: offset=offset+(line-rows); line=rows
        if not updo: print("\r\033c",end="")
        # If OS is LINUX restore TTY to it default values
        if not sep==chr(92): termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        if not mode==None or updo:
            # Set vars
            filetext,opentxt,wrtptr,lenght = mode
            out=opentxt+filetext
            # Calculate in what line it is
            fix=len(out)//(columns+2)
            # Calculate blank spaces
            full=((columns+2)*(fix+1))-len(out)
            # Get raw screen updated
            menu = update_scr(black,reset,status,banoff,\
            offset,line,0,arr,banner,filename,rows,columns,True)
            # Cut menu to add the menu bar
            menu="\n".join(menu.split("\n")[:rows+banoff+2-fix-1])
            # Add menu to it
            menu+=black+out+(" "*full)
            # Calculate pointer y displacement
            fix_lip = rows+banoff+2-fix+((wrtptr-1)//(columns+2))
            # Calculate pointer x displacement
            fix_wrtptr = (columns+2)*fix
            # Some pointer x displacement fix
            while True:
                if wrtptr-1-fix_wrtptr<0:
                    fix-=1
                    fix_wrtptr=(columns+2)*fix
                else: break
            # Add scape secuence to move cursor
            menu+="\r\033[%d;%dH"%(fix_lip, wrtptr-1-fix_wrtptr)
            # Print the whole screen
            print(menu, end="")
        # If OS is LINUX set TTY to raw mode
        if not sep==chr(92): tty.setraw(fd)
    return rows,columns
