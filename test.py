from msvcrt import getch

try:
    while True:
        while True:
            inp=getch()
            try:
                out=inp.decode("UTF-8")
                break
            except:
                in2=getch()
                out=inp+in2
                out=out.decode("UTF-8")
                break
        print(out)
        
except Exception as e: print(e)
input()
    

