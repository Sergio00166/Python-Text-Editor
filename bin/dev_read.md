pBTE: Python Based Text Editor for TTY
======================================

1. Introduction
---------------

This document describes a modular text editor designed to run on any Linux or Windows modern TTY emulator. It operates
independently of specific libraries like `ncurses`, focusing on core functionality and flexible modules for expanded
features. This editor provides essential text editing operations, with the ability to extend its capabilities through 
modular components.

2. Screen Layout
----------------

The editor dynamically adapts to the available terminal size. The first line is reserved for a banner that includes
file-related information, such as the filename. The rest of the screen displays file content, processed and formatted 
to fit the current terminal dimensions using core display management techniques.

3. File Handling and Display
----------------------------

File content is stored in an array and rendered on the screen, ensuring proper handling of character encoding 
(e.g., UTF-8) and complex formatting such as multi-space characters. The display adjusts based on screen size, with 
calculations ensuring accurate content rendering regardless of terminal dimensions.

4. Modular Design and Core Features
-----------------------------------

The editor is built with modularity in mind, relying on core components to handle essential tasks, while additional 
modules can be developed to extend its functionality.

### 4.1 Core Features

* **Text editing**: Basic editing functions including cut, copy, paste, and file navigation.
* **File operations**: Open, save, and manage files.
* **Cursor management**: Displacement controls for both vertical and horizontal movements, ensuring proper positioning 
  even with characters with a width greater than 1.
* **Screen redraw**: Full-screen redraws by moving the cursor to the top-left corner and overwriting previous content 
  with spaces to ensure old information is cleared.

### 4.2 Vertical and Horizontal DDC

* **Vertical DDC**: Uses two variables—one to track the cursor’s vertical position and another to manage the displacement 
  from the top or bottom of the viewable area.
* **Horizontal DDC**: Handles complex cases like UTF-8 multi-space characters by dividing content into blocks that fit 
  the screen and recalculating the relative cursor position.

5. TTY Management
-----------------

The editor directly manages the TTY screen without using advanced libraries like `ncurses`. It handles raw TTY control 
for cursor movement and screen updates, ensuring compatibility with most modern terminal emulators.

6. Modularity and Extensibility
-------------------------------

The core design of the editor is modular, with the ability to add or modify features through separate modules. This 
allows developers to implement new functionalities without altering the core.

### Example Modules:

* **Menu systems**: Each menu is treated as a separate module that controls the TTY when activated, returning control to 
  the main editor after use.

7. File Structure
-----------------

* **`bin/core/actions*.py`**: Core keyboard action mappings.
* **`bin/core/functions.py`**: Main functions for screen handling and core operations.
* **`bin/core/functions1.py`**: Shared utilities.
* **`bin/core/keys_func.py`**: Keyboard mapping to actions.
* **`bin/menus/`**: Contains modular menus for different actions.
* **`bin/data.py`**: ASCII and key-handling configurations.
* **`bin/init.py`**: Startup definitions for initializing the editor.

8. Conclusion
-------------

This modular text editor provides a core set of features for text manipulation, file handling, and screen management, 
adaptable to any modern TTY emulator on Linux or Windows. Its extensible nature allows for easy customization and 
expansion through separate modules, making it highly flexible for various use cases.
