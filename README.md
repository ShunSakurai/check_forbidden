# Check Forbidden
A tool for checking forbidden terms in target segments of translation files (.mqxlz, .mqxliff, .xlf, etc.), using CSV files

This project will be discontinued, and I'll develop an online tool: [yure-checker](https://github.com/ShunSakurai/yure-checker).

[Japanese README](https://github.com/ShunSakurai/check_forbidden/blob/master/README_jpn.md) is also available.

![UI](https://raw.github.com/wiki/ShunSakurai/check_forbidden/check_forbidden_ui.png)

## Description
[memoQ](https://www.memoq.com/) allows us to check forbidden source and target term pairs using the term base, and check forbidden terms using the QA settings. However, it takes time to add each forbidden term one by one, choosing the settings.
Using this tool, you can quickly spot the forbidden terms used in memoQ bilingual files, by using term lists in CSV format. You can use the regular expressions (regex). You can also call a function from an external Python script against the target segments. It helps you efficiently maintain the translation quality.
(memoQ recently brought us the functionality to check only forbidden target terms regardless of the corresponding source terms in their great [update](https://www.memoq.com/memoq-build-june). Hope they will support CSV import to QA settings soon, like we do for term base.)

For example, you can use this tool in the following situations:

- The style guide does not allow you to use contractions such as `doesn't` and `can't` in the translation
- The style guide does not allow you to use a whitespace between a half-width character and a full-width character
- JP (Japanese): You can use `次の/次に`, but you cannot use `以下の/以下に`
- JP: You have to keep `例えば` in kanji, and you cannot use `たとえば`

All you have to prepare are:

- memoQ bilingual .mqxlz or .mqxliff, version 1.2 XLIFF, or plain text file(s) which include translation
- CSV or text file(s) containing the list of forbidden terms

This tool searches for the forbidden terms in the target segments of bilingual files, segment by segment. It displays the result on the Command Prompt, and exports it into an HTML file. Command Prompt is good when the file is small and you want to quickly check what was detected. The Summary result is useful when you are working on a "View." Some characters are non-printable on Command Prompt. The HTML file is useful when you have many matches and you want to use filtering features.

This program is written in Python with tkinter and is distributed in .exe format through [PyInstaller](http://www.pyinstaller.org/) and [Verpatch](https://ddverpatch.codeplex.com/releases).

The icon was created with [アイコン ウィザード](http://freewareplace.web.fc2.com/) and the installer is created with [Inno Setup](http://www.jrsoftware.org/isdl.php).

## Installation
This tool is currently only available for Windows at [Releases](https://github.com/ShunSakurai/check_forbidden/releases). All you have to do for installation and upgrading is to download and run the installer. Both 32-bit and 64-bit environments are supported.

If you have the Python environment installed, you can run the source code with `python(3) check_forbidden.py` or `import check_forbidden` even on Mac and on any OS.

## Build
To convert the Python code to an .exe file, and to create an installer, follow the steps below.

### Requirements
- [Python 3](https://www.python.org/downloads/)
- [PyInstaller](http://www.pyinstaller.org/)
- [Verpatch](https://ddverpatch.codeplex.com/releases), add it to PATH
- [Inno Setup](http://www.jrsoftware.org/isdl.php)

### Procedures
- Run `py -B setup.py` on a Windows machine. `-B` is optional
- You may have to set alias to make py = python3

## Usage

### Overview
- Export bilingual file(s) from memoQ or other CAT tools (Transifex supported)
- Open the program by double-clicking Check Forbidden.exe or its alias
- Choose translation file(s) by clicking "Bilingual" or by typing / pasting the path to the file
- Choose CSV or text file(s) containing the list of forbidden terms, or a Python script
- Specify the path and the name of the result file to be exported if necessary. The default path is the first bilingual file's path + "checked_result.html"
- Click "Run!"
- The result is displayed in the Command Prompt. If exporting is enabled and any matches are found, they are also exported into an HTML file
- Click "X" (close) button to exit the program

![Result](https://raw.github.com/wiki/ShunSakurai/check_forbidden/check_forbidden_result.png)

### Options
To display the options pane, click on the gear ⚙ icon. To hide the pane, click on the triangle ▼ icon.

You can specify whether you save the last used options. A file named "cf_options.p" is created in "C:\Users\<UserName>\AppData\Roaming\Check Forbidden" (on Windows).

![Options](https://raw.github.com/wiki/ShunSakurai/check_forbidden/check_forbidden_options.png)

### Translation file types
Following file types are supported:

- .mqxliff
- .mqxlz
- .xlf ([XLIFF version 1.2](http://docs.oasis-open.org/xliff/v1.2/os/xliff-core.html))
- .txt
- .srt
- .po

A .mqxlz file is a compressed file of a document.mqxliff file, a skeleton (formatting information), and sometimes the version information. The program extracts the document.mqxliff to a folder and removes it when the processing is finished.

The text files need to be encoded in UTF-8.

### CSV file formats
The term list needs to meet the following specifications:

- You cannot use Comma in the file name
- Delimiter: comma
- Encoding: UTF-8
- All terms are considered as regex patterns and are case-sensitive
- Any special characters (`(`, `)`, `[`, `]`, `.`, `\*`, `?`, `!` ,etc.) used in regex need to be **escaped with a backslash**
- Terms in the **first** column will be considered as the forbidden terms
- You can use other columns to provide detailed information e.g. the index number, the source term, and the correct target term
- When a comma is included in the CSV file, it may be interpreted as the delimiter
- When characters with accents are included in the CSV file, they can be used correctly for checking, but they are not printed correctly on Command Prompt
- (txt file) Commas and double quotation marks need to be escaped as `""` and `"String, including comma"`

![CSV](https://raw.github.com/wiki/ShunSakurai/check_forbidden/check_forbidden_csv.png)

### Regular expressions
- This program uses the syntax in [re](https://docs.python.org/3/library/re.html) module
- memoQ's regex for tags `\tag` is not currently supported
- (Example) `[0-9A-Za-z]\s[^!-~]` and `[^!-~]\s[0-9A-Za-z]` search for whitespace inserted between ASCII half-width characters and other characters including full-width characters
- (Example) `\\)\S` searches for a bracket without whitespace around it

### Call external functions
When the function check box is selected, you can call a function from an external Python script.

- Call a function named "function" in an external Python script, which takes six arguments: segment ID (integer), the source segment (string), target segment (string), match percentage (integer), locked status (boolean), target same as source (boolean)
- The function should return a 2D list or None for each segment, each inner list representing one line in the result display both on Command Prompt and in the HTML table

Code example:
calculate_width.py
```python
import re
pattern_half_width = re.compile(r'[ -~]')

def function(str_seg_id, str_source, str_target, int_percent, bool_locked, bool_same):
    length_half = len(re.findall(pattern_half_width, str_target))
    length_full = len(str_target) - length_half
    length_total = length_half + length_full * 2
    return [[str_seg_id, str_target, length_full, length_half, length_total]]
```

### Keyboard shortcuts
Buttons can be selected by pressing the underlined characters along with Alt key. For other buttons without an underline, they can be invoked with the following keys:

- Run!: Alt + Return (Alt + Enter)
- Show or hide the options: Alt + o
- Clear three fields: Alt + c
- Open the folder: no shortcut key

You can move along the UI items with "Tab" key and invoke the focused item with the space bar.

### Tips
- The check is done quickly if all bilingual files are combined into a "view"
- The check is done quickly if the bilingual files are located on your local PC rather than on a shared drive
- If you type or paste a path into the entry fields and press the button to choose the file(s) afterwards, browsing starts from the folder written in the field
- If you save the last used term file name(s), their file path will be the default location to browse term files
- When any of the entry field is filled, you can open the folder by pressing the arrow on the right
- The result is displayed for both individual and whole files (as the "Summary")
- PyInstaller might create large folders named like "_MEI000000" in `C:\Users\%username%\AppData\Local\Temp` folder. They can be deleted safely

### Integration with XProof
If you have [XProof](https://github.com/AlissaSabre/XProof) installed on your Windows, you can call XProofCmd from Check Forbidden, against the bilingual files selected in the "Bilingual" field. If no bilingual file is selected in the field, XProof opens with any file path in the field copied to the clipboard. XProof supports xliff files (.mqxlz and .mqxliff), not .txt/.srt/.po.

## Troubleshooting

### Garbled display on Command Prompt
Sometimes multi-byte characters on Windows Command Prompt seem garbled. To correct this, right click on the title bar, select "Properties / Font," and choose a larger font or another font. Press Alt + Space and then P to quickly access the Properties.

![Garbled](https://raw.github.com/wiki/ShunSakurai/check_forbidden/check_forbidden_garbled.png)

### \_extract folder is not deleted
\_extract folders are created when opening the .mqxlz files in the same folder as the files. Sometimes the program fails to delete them, when an error happens. In that case, please delete them by yourself.

### False positives
Below are some best practices to avoid false positives.

- Add ` play` or `\splay` (space + play) in CSV to avoid matching `display`
- Avoid using too short terms, such as `等` (など) in order avoid matching `等級`
- When many false positives are found for 1 term, consider dividing the CSV file

### Things to do when searching takes too long time
- Consider creating a view for multiple documents (files)

## Features to come
### Working on
- Show whitespace characters in HTML file
- Support only registered memoQ tags
- Make the program window re-sizable
- Do more with external Python functions

### Features not coming
- Add file by dragging. The drag and drop feature is hard to use in tkinter
- Mark and ignore false positives. It is technically difficult
- Add settings to specify the row of forbidden terms
- Add an ability to choose multiple bilingual files from different folders. Not very important

Please let me know from [Github Issues](https://github.com/ShunSakurai/check_forbidden/issues) or [Asana](https://app.asana.com/0/264039980253157/list) if you need any of the features as soon as possible.

## History
For detailed history, please go to [Releases](https://github.com/ShunSakurai/check_forbidden/releases).

"*" at the beginning means bug-fixing.

## Contribution
This is just a personal project. Any feedback and contribution from [Github Issues](https://github.com/ShunSakurai/check_forbidden/issues) or [Asana](https://app.asana.com/0/264039980253157/list) and contribution is welcome!

## License
### Usage
You can use it for free.
© 2016-2019 Shun Sakurai

### MIT License
The code is protected under MIT License. Please see [license.md](https://github.com/ShunSakurai/check_forbidden/blob/master/license.md) for details.
