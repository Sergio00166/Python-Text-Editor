#Code by Sergio1260

from os import get_terminal_size,sep
from os.path import split as psplit
from multiprocessing import cpu_count, Pool
from re import split as resplit


def get_size():
    size=get_terminal_size()
    return size[1]-2,size[0]-2

def decode(key): return key.decode("UTF-8")

def fixlenline(text,pointer,oldptr):
    length=len(text)+1
    if pointer>length or oldptr>length:
        return length
    elif oldptr>pointer: return oldptr
    else: return pointer

def CalcRelLine(p1,arr,offset,line,banoff,rows):
    if p1=="-": p1=len(arr)-1
    try:
        p1=int(p1)
        if p1<len(arr):
            if p1<rows: offset=0; line=p1+banoff
            else: offset=p1-rows; line=rows+banoff
    except: pass
    return line, offset


def fixfilename(path, columns, length):
    if len(path) <= length: return path
    dirname, basename = psplit(path)
    if len(path) <= length: return path
    available_length = length - len(basename) - 1
    if available_length <= 0: return basename[:length - 1]+'*'
    parts = dirname.split(sep)
    while len(parts) > 0 and len(sep.join(parts)) > available_length: parts.pop(0)
    if len(parts) == 0: compacted_path=basename
    else: compacted_path = sep.join(parts) + sep + basename
    
    return compacted_path
   

def del_sel(select, arr, banoff):
    p1=arr[:sum(select[0])]; p2=arr[sum(select[1]):]
    line=select[0][0]+banoff; offset=select[0][1]
    select=[]; arr=p1+p2
    # Fix when selection is on bottom
    if line>banoff and line+offset-banoff>len(arr)-1:
        if offset>0: offset-=1
        else: line-=1
    return select, arr, line, offset


def select_add_start_str(arr,line,offset,select,text,remove=False):
    # Get the values from select
    start=sum(select[0]); end=sum(select[1])
    # Get the text that is upper and below the selected region
    p0=arr[:start]; p2=arr[end:]
    # Get the text that is selected
    p1=arr[start:end]
    if isinstance(text, list):
        if not remove: p1=[text[0]+x+text[1] for x in p1]
        else:
            p1 = [
                x[len(text[0]):] if len(text[1])==0 and x.startswith(text[0])
                else x[len(text[0]):-len(text[1])]
                if x.startswith(text[0]) and x.endswith(text[1])
                else x for x in p1
            ]
    else:
        if not remove: p1=[text+x for x in p1]
        else: p1 = [x[len(text):] if x.startswith(text) else x for x in p1]
    
    # Now reconstruct all arr
    return p0+p1+p2


def get_str(arr,key,select,pointer,line,offset,banoff,indent,rows,keys,codec):
    out,skip = decode(key),False
    if select:
        if not out=="\t": 
            select,arr,line,offset = del_sel(select,arr,banoff)
            if not key in [keys["return"], keys["supr"]]:
                arr.insert(line+offset-banoff, "")
                select = []
        else: arr,skip = select_add_start_str(arr,line,offset,select,indent),True
       
    if not skip:
        pos=line+offset-banoff; text=arr[pos]
        p1,p2 = text[:pointer-1], text[pointer-1:]
        out=out.replace("\t",indent)
        out_lines = resplit(r'[\n\r]',out)
        arr[pos] = p1+out_lines[0]+p2
        if len(out_lines) > 1:
            arr[pos+1:pos+1] = out_lines[1:]
            # Calculate displacement
            line+=len(out_lines)-1
            if line>rows+1:
                offset+=line-rows
                line=rows
            pointer += len(out_lines[-1])
        else: pointer += len(out_lines[0])

    return arr, pointer, line, offset, select


def detect_line_ending_char(file_path):
    c = open(file_path, 'rb').read()
    crlf = c.count(b'\r\n')
    c=c.replace(b'\r\n',b'')
    cr = c.count(b'\r')
    lf = c.count(b'\n')
    
    if crlf>cr and crlf>lf:
        return '\r\n'
    elif cr>lf: return '\r'
    else: return '\n'


# Try to read in UTF-8, if cannot read in extended ascii
def read_UTF8(path):
    lnsep = detect_line_ending_char(path)
    try:
        file = open(path,"r", encoding="UTF-8",newline="")
        file,codec = file.read(),"UTF-8"
    except:
        file = open(path,"r", encoding="latin_1",newline="")
        file,codec = file.read(),"latin_1"
        
    return file.split(lnsep), codec, lnsep

