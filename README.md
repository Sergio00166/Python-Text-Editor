# pBTE
python-based Basic Text Editor

A a basic terminal text editor with python using the minimun external libraries as possible (only wcwidth and colorama) 

Only supports UTF-8 (normal mode) and ASCII (for reading bin files)

Basic functionalities currently available such as copy, cut, paste lines, find string, and replaced string.
<br>Currently ctrl+Z is not available a workaround is using ctrl+a and then ctrl+b to create a .bak file

Due to limitations with msvcrt.getch() on windows to select (highlight) lines you must use Ctrl+arrows instead of Shift+arrows 

<h3>Requirements:</h3>
Python 3 (tested under python 3.12)<br>
No dependencies<br>
Windows or Linux with UTF-8 keyboard <br>

<br><h2>OPTIONS</h2>
<br>*NORMAL*<br>
^Q QUIT | ^S SAVE | ^A Save as | ^O OPEN | ^C COPY | ^X CUT | ^P PASTE | ^G GOTO <br>
^D DEDENT | ^I INDENT | ^K COMMENT | ^U UNCOMMENT | ^F FIND | ^R REPLACE <br>
Alt+D toggle between 4 spaces or tab | Alt+K change start comment str <br>
Alt+U change end comment str | Alt+I change indent str<br>
<br>*Open file menu*<br>
^C CANCEL | ^O OPEN  | ^N NEW FILE <br>
<br>*Save as menu*<br>
^C CANCEL | ^S SAVE | ^B BACKUP | ^A APPEND | ^P PREPEND
<br><br>
Return to leave that value blank (if no text is writed)<br>
