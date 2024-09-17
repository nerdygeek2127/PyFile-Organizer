
# PyFile Organizer

**PyFile Organizer** is a Python application that allows users to search, list, organize, and manage `.py` files. With features like bookmarking directories, tagging files, and running or editing them directly from the interface, PyFile Organizer helps streamline Python project management.

## Features

- **Search Folder**: Browse and list all `.py` files in the selected folder.
- **Bookmark Folders**: Easily bookmark directories for quick access.
- **Tag Files**: Add custom tags to files for easy identification.
- **Run or Edit Files**: Run Python files directly or open them in Notepad++ for editing.
- **Customizable Interface**: Built with `ttkbootstrap`, providing a modern look and feel.

[![IMG-20240917-WA0003.jpg](https://i.postimg.cc/L4tJFP94/IMG-20240917-WA0003.jpg)](https://postimg.cc/rzpVSKR7)


## Installation

1. Clone the repository or download the project files.
   
   ```bash
   git clone https://github.com/your-username/pyfile-organizer.git
   ```

2. Install the required dependencies:

   ```bash
   pip install ttkbootstrap
   ```

3. Make sure Notepad++ is installed on your system, and update the path in the code if necessary:
   
   ```python
   NOTEPAD_PLUS_PATH = r"C:\Program Files\Notepad++\notepad++.exe"
   ```

## Usage

1. Run the `pyfile_organizer.py` script:
   
   ```bash
   python pyfile_organizer.py
   ```

2. Use the **Search Folder** button to browse and list Python files.
3. Bookmark folders for quick access.
4. Tag files by selecting a file and clicking the **Tag** button.
5. Run or edit Python files directly from the app.

## Requirements

- Python 3.x
- `ttkbootstrap` package
- Notepad++ (for editing files)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
