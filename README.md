# pBTE
python-based Basic Text Editor

A a basic terminal text editor with python using the minimun external libraries as possible (only wcwidth and colorama) 

Only supports UTF-8 (normal mode) and ASCII (for reading bin files)

Basic functionalities currently available such as copy, cut, paste lines, find string, and the basic for a text editor

Due to limitations with msvcrt.getch() on windows to select (highlight) lines you must use Ctrl+arrows instead of Shift+arrows 

<h3>Requirements:</h3>
Python 3 (tested under python 3.12)<br>
No dependencies<br>
Windows or Linux with UTF-8 keyboard <br>

<br><h2>OPTIONS</h2>
<br>*NORMAL*<br>
^Q QUIT | ^S SAVE | ^A Save as | ^O OPEN | ^C COPY | ^X CUT | ^P PASTE <br>
^G GOTO | ^D DEDENT | ^I INDENT | ^K COMMENT | ^U UNCOMMENT <br>
F1 toggle between 4 spaces or tab | F2 change start comment str <br>
F3 change end comment str | F4 change indent str<br>
<br>*Open file menu*<br>
^C CANCEL | ^O OPEN  | ^N NEW FILE <br>
<br>*Save as menu*<br>
^C CANCEL | ^S SAVE | ^B BACKUP | ^A APPEND | ^P PREPEND
<br><br>
For menus like ^G, F2, F3, and F4 you can use ^C to exit that menu and<br>
Return to leave that value blank (if no text is writed)<br>
