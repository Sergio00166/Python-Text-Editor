# Code by Sergio00166

from functions import scr_arr2str, rscp, sscp, str_len
from functions1 import get_size, fixfilename
from sys import stdout


# Some ANSII ctrl codes
movcr = "\r\033[%d;%dH"
cls = movcr%(1,1)
scr = "\r\x1b[?25h"
hcr = "\r\x1b[?25l"

def print(text):
    stdout.write(text)
    stdout.flush()

def update_scr(black,bnc,slc,reset,status,banoff,offset,line,pointer,arr,banner,filename,rows,columns,status_st,rrw=False,select=[],hlg_str=None):
    # Create the string that represents on which line we are
    position=" "+str(line+offset-banoff)+"  "
    # Create a part of the banner (position and status strings)
    status= (" "+banner[1] if not status_st else "  "+status)
    outb=position+" "+banner[0]+status+"    "
    # Check if the space for the filename is too small
    length = columns-len(outb); small = length<24
    if small: outb,fix,length = "",1,columns
    # Fix the filename string to fit in the space
    filename = fixfilename(filename,length)
    # Use the fucking UNIX path separator
    filename = filename.replace(chr(92),"/")
    # Calculate blank space of necessary
    if small: filename+=" "*(columns-len(filename))
    # Get the separation between the Left and the filename
    if not small: fix=columns-len(outb)-len(filename)+1
    # Get the text that will be on screen and update the pointer value
    all_file,pointer = scr_arr2str(arr,line,offset,pointer,black,reset,columns,rows,banoff)
    # This is for the find str function page
    if not hlg_str is None:
        l_pointer = hlg_str[2]-1
        l_line = hlg_str[1]-banoff
        text = hlg_str[0]
        all_file = all_file.split("\n")
        t = all_file[l_line]
        t1 = t[:l_pointer-len(text)]
        t1 = t1.replace(text,black+text+reset)
        t2 = t[l_pointer:]
        t2 = t2.replace(text,black+text+reset)
        t = t[l_pointer-len(text):l_pointer]
        t = t1+slc+t+reset+t2
        del t1,t2,l_pointer,hlg_str
        p1 = "\n".join(all_file[:l_line])
        p1 = p1.replace(text,black+text+reset)
        p2 = "\n".join(all_file[l_line+1:])
        p2 = p2.replace(text,black+text+reset)
        all_file = p1+t+p2
        del p1,p2,t,l_line,text
        
    # Initialize the menu with all the banner
    menu=cls+bnc+outb+" "*fix

    # Highlight selector
    if len(select)>0:
        # Get values from the select list
        start=select[0][0]; end=select[1][0]
        if line < rows+banoff:
            end+=select[1][1]-select[0][1]
        start-=select[1][1]-select[0][1]
        # Fix start value
        if start<0: start=0
        # Split lines
        all_file=all_file.split("\n")
        # Get the text that is upper the selected region
        p0="\n".join(all_file[:start])
        # Get the text that is below the selected region
        p2="\n".join(all_file[end:])
        # Get the text that is selected
        p1=all_file[start:end]; out=[]
        # Get the len of the higligh ascii code
        length=len(black+"*"+reset)
        # For each line of p1
        for x in p1:
            x=rscp(x,[black,reset,slc])
            # Checks if the line rendered continues to the right
            # (having the flag that marks that)
            if x.endswith(black+">"+reset):
                out.append(x[:-length]+reset+">"+black)
            # Checks if the line rendered continues to the left
            # (having the flag that marks that)
            elif x.startswith(black+"<"+reset):
                out.append(x[:-length]+reset+"<"+black)
            # If none of the above simply add is to out dic
            else: out.append(x)
        # Create a string from the list
        p1="\n".join(out)
        # Now create the all file string. Adding the
        # ascii chars to p1 (the selected string)
        all_file=p0+black+p1+reset+p2
    # Now concatenate all to create the screen
    menu+=filename+" "+reset+"\n"+all_file
    # If raw mode is specified return the screen string
    if rrw: return menu
    else:
        # if not add the ansii code firstly to unshow
        # the tty cursor, then move the cursor to the
        # desired line, the show the cursor and move
        # it horizontally and then print to stdout
        line += banoff
        menu += movcr%(line,1)+scr
        menu += movcr%(line,pointer)
        print(hcr+menu)


def menu_updsrc(arg,mode=None,updo=False):
    # Extract args
    black,bnc,slc,reset,status,banoff,offset,line,pointer,\
    arr,banner,filename,rows,columns,status_st = arg
    # Save old vars and get new values
    old_rows=rows; old_columns=columns
    rows,columns=get_size()
    # Check if terminal is too small
    if rows<4 or columns<24: print("\r\033cTerminal too small")
    # Compare the old values with the new ones
    elif not (old_rows==rows and old_columns==columns) or updo:
        if not updo: print("\r\033c")
        if not mode==None or updo:
            # Set vars
            filetext,opentxt,wrtptr,length = mode
            out=opentxt+filetext
            # Calculate in what line it is
            fix=len(out)//(columns+2)
            # Calculate blank spaces
            full=((columns+2)*(fix+1))-len(out)
            # Get raw screen updated
            menu = update_scr(black,bnc,slc,reset,status,banoff,offset,\
            line,0,arr,banner,filename,rows,columns,status_st,True)
            # Cut menu to add the menu bar
            menu = "\n".join(menu.split("\n")[:rows+banoff-fix])
            # Fix weird chars
            out=sscp(out,[slc,reset+bnc])
            # Add menu to it
            menu+="\n"+bnc+out+(" "*(full))
            # Calculate cursor displacement
            text_size = len(out)//(columns+2)
            line_number = (wrtptr-1)//(columns+2)
            cursor_y = ((rows+2)-text_size)+line_number
            cursor_x = (wrtptr-1)%(columns+2)
            # Fix cursor xy displacement
            if cursor_x==0:
                cursor_x = columns+2
                cursor_y -= 1
            # Add scape secuence to move cursor
            menu+="\r\033[%d;%dH"%(cursor_y, cursor_x)
            # Print the whole screen
            print(menu)
            
    return rows,columns
