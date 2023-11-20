#Code by Sergio1260

from msvcrt import getch

def decode(key):
    for x in range(3):
        try: out=key.decode("UTF-8"); break
        except: key+=getch()
    return out

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


def save_as(filename, black, reset, rows, banoff, arr, saved_txt, status_st, columns):
    
    saveastxt="Save as: "; lenght=len(saveastxt)+2; filewrite=filename; wrtptr=lenght+len(filewrite)
    bottom="\n\t"+black+"^Q"+reset+" CANCEL        "+black+"^S"+reset+" SAVE        "
    bottom+=black+"^B"+reset+" BACKUP        "+black+"^A"+reset+" APPEND        "
    bottom+=black+"^P"+reset+" PREPEND                    "
    
    while True:
        out=saveastxt+filewrite; full=columns-len(out)
        print("\r\033[%d;%dH"%(rows+banoff+2, 1),end="")
        print("\r"+" "*(len(filewrite)+lenght+1), end="")
        print("\r"+black+out+(" "*full)+reset+bottom,end="")
        print("\r\033[%d;%dH"%(rows+banoff+2, wrtptr),end="")
        
        key=getch() #Map keys
        
        #Ctrl + S (confirms) or Ctrl + B backup
        if key==b'\x13' or key==b'\x02':
            try:
                
                if key==b'\x02' and filewrite==filename:
                    filewrite+=".bak" #Ctrl+B and if same name
                    
                out=open(filewrite,"w",encoding="UTF-8")
                out.write("\n".join(arr)); out.close(); status_st=2
                
                if key==b'\x13': #Ctr + S
                    status=saved_txt; tmp=open(filewrite, "r", encoding="UTF-8").readlines(); arr=[]
                    for x in tmp: arr.append(x.replace("\r","").replace("\n","").replace("\f",""))
                    arr.append(""); filename=filewrite; break
                    
                else: status=black+"Backed UP"+reset; break
                
            except: pass
            
        #Ctrl + Q (cancel)
        elif key==b'\x11': break
    
        elif key==b'\x08': #Delete
            if not wrtptr==lenght:
                p1=list(filewrite); p1.pop(wrtptr-lenght-1)
                filewrite="".join(p1); wrtptr-=1

        elif key==b'\xe0': #Arrows
            arrow=getch()
            if arrow==b'K': #Left
                if not wrtptr==lenght:
                    wrtptr-=1
            elif arrow==b'M': #Right
                if not wrtptr>len(filewrite)+lenght-1:
                    wrtptr+=1
     
        elif key==b'\r': pass

        elif key==b'\x10' or key==b'\x01': #Ctrl + P or Ctrl + A
            try:
                tmp=open(filewrite, "r", encoding="UTF-8").readlines()
                status=saved_txt
                if key==b'\x01': output=list(arr+tmp)
                elif key==b'\x10': output=list(tmp+arr)
                out=open(filewrite, "w", encoding="UTF-8")
                out.write("\n".join(output)); break
            except: pass
        
        else: #Rest of keys
            if not wrtptr>columns-1:
                out=decode(key)
                p1=filewrite[:wrtptr-lenght]
                p2=filewrite[wrtptr-lenght:]
                filewrite=p1+out+p2
                wrtptr+=1

    return arr, status_st, filename, status
