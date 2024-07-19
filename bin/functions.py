#Code by Sergio1260

from os import sep
from sys import path
path.append(path[0]+sep+"lib.zip")
from wcwidth import wcwidth

ascii_map = { 0x00: '␀', 0x01: '␁', 0x02: '␂', 0x03: '␃', 0x04: '␄', 0x05: '␅', 0x06: '␆',
              0x07: '␇', 0x08: '␈', 0x0A: '␊', 0x0B: '␋', 0x0C: '␌', 0x0D: '␍', 0x0E: '␎',
              0x0F: '␏', 0x10: '␐', 0x11: '␑', 0x12: '␒', 0x13: '␓', 0x14: '␔', 0x15: '␕',
              0x16: '␖', 0x17: '␗', 0x18: '␘', 0x19: '␙', 0x1A: '␚', 0x1B: '␛', 0x1C: '␜',
              0x1D: '␝', 0x1E: '␞', 0x1F: '␟', 0x7F: '␡'
            }
ascii_replaced = [ascii_map[x] for x in ascii_map]+[">","<","�"]


def expandtabs(text, tabsize=8):
    result,col = [], 0
    for char in text:
        if char == '\t':
            space_count = tabsize - (col % tabsize)
            result.append(' ' * space_count)
            col += space_count
        else:
            result.append(char)
            char_width = wcwidth(char)
            if char_width > 0:
                col += char_width
            else: col += 1
    return ''.join(result)


# Now it seems to work
def wrap(text, columns):
    out,buffer,counter = [],"",-1
    text=expandtabs(text)
    for x in text:
        lenght=str_len(fscp(x))
        if counter+lenght>columns:
            out.append(buffer)
            buffer,counter = x,lenght
        else:
            buffer+=x
            counter+=lenght
    out.append(buffer)
    return out

def fix_arr_line_len(arr, columns, black, reset):
    out=[]; fix=0//(columns+2)
    for text in arr:
        text = text[:columns+2]
        wrapped_text = wrap(text,columns)
        if len(wrapped_text)==0: wrapped_text=""
        elif fix==len(wrapped_text):
            text=wrapped_text[fix-1]
        else: text=wrapped_text[fix]
        text=sscp(text,[black,reset])
        if (len(wrapped_text)-fix)>1:
            text+=black+">"+reset
        out.append(text)   
    return out

def str_len(text,pointer=None):
    lenght=0
    if not pointer==None:
        fix=text[:pointer-1]
    else: fix=text
    fix=expandtabs(fix)
    for x in fix: lenght+=wcwidth(x)
    return lenght

def fix_cursor_pos(text,pointer,columns,black,reset):
    # Set a lot of constants and vars
    len_arr,ptr,pos = [],pointer,0
    arr_l = black+"<"+reset
    arr_r = black+">"+reset
    text = text[:pointer+columns+2]
    trsl = str_len(fscp(text),pointer)
    wrapped_text = wrap(text,columns)
    # Get in which part the cursor is
    pos = (trsl-1)//columns
    if pos<0: pos = 0
    pointer = trsl-(pos*columns)
    # Now get the content
    lenght = len(wrapped_text)
    if not lenght==0:
        if pos>lenght-1: pos=-1
        text=wrapped_text[pos]
        text=sscp(text,[black,reset])
        # Add the < AND > indicators
        if pos>0:
            text=arr_l+text
            if not pos==lenght-1:
                text+=arr_r+reset
        elif lenght>1: text+=arr_r      
    else: text=""
                
    return pointer+1, text


def scr_arr2str(arr,line,offset,pointer,black,reset,columns,rows,banoff):
    uptr=pointer; out_arr=[]; sp=black+"<"+reset
    text = arr[line+offset-banoff]
    pointer, text = fix_cursor_pos(text,pointer,columns,black,reset)
    arr = arr[offset:rows+offset+banoff]
    arr = fix_arr_line_len(arr,columns,black,reset)
    arr[line-banoff] = text

    for x in arr:
        ln=str_len(rscp(x,[black,reset],True))
        if ln<(columns+2): x=x+(" "*(columns-ln+2))
        out_arr.append(x)
    if not len(arr)==rows:
        out_arr+=[" "*(columns+2)]*(rows-len(arr)+1)
    
    return "\n".join(out_arr), pointer


# Replaces ascii control chars to the highlighted visual version
def sscp(arg,color):
    global ascii_map
    b, r = color; ext = []
    arg=expandtabs(arg)
    for x in arg:
        if ord(x) in ascii_map:
            ext.append(b+ascii_map[ord(x)]+r)
        elif str_len(x)>0: ext.append(x)
        else: ext.append(b+"�"+r)
    return "".join(ext)

# Changes visual ascii chars to space (to read the real screen len)
def fscp(arg,null=False):
    global ascii_map
    r = "" if null else " "
    ext = []
    for x in arg:
        if ord(x) in ascii_map: ext.append(r)
        elif str_len(x)>0: ext.append(x)
        else: ext.append(r)
    return "".join(ext)

# Inverts the highlight (for the highlight selector)
def rscp(arg,color,mode=False):
    global ascii_replaced
    if len(color)==3:
        b,r,c = color
        b1,r1 = r+b,r+c
    else:
        b,r = color
        b1,r1 = b,r
    for x in ascii_replaced:
        arg=arg.replace(b+x+r, " " if mode else r1+x+b1)
    return arg
