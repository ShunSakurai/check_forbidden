# Check Forbidden
A tool for checking forbidden terms included in the target segments of memoQ bilingual files (.mqxlz / .mqxliff), using CSV files

[Japanese README](https://github.com/ShunSakurai/check_forbidden/blob/master/README_jpn.md) is also available.

![UI](https://raw.github.com/wiki/ShunSakurai/check_forbidden/check_forbidden_ui.png)

## Description
[memoQ](https://www.memoq.com/) allows us to check forbidden source and target term pairs using the term base, and check forbidden terms using the QA settings. However, it takes time to add each forbidden term one by one, choosing the settings.
Using this tool, you can quickly narrow down and spot the forbidden terms used in memoQ bilingual files, by using a term list in CSV format. You can use the regular expressions (regex). You can also call a function from an external Python script against the target segments. It helps you efficiently maintain the translation quality.
(memoQ recently brought us the functionality to check only forbidden target terms regardless of the corresponding source terms in their great [update](https://www.memoq.com/memoq-build-june). Hope they will support CSV import to QA settings soon, like we do for term base.)

For example, you can use this tool in the following situations:

- The style guide does not allow you to use contractions such as `doesn't` and `can't` in the translation
- The style guide does not allow you to use a whitespace between a half-width character and a full-width character
- JP (Japanese): You can use `次の/次に`, but you cannot use `以下の/以下に`
- JP: You have to keep `例えば` in kanji, and you cannot use `たとえば`

All you have to prepare are:

- memoQ bilingual .mqxlz or .mqxliff file(s)
- CSV or text file(s) containing the list of forbidden terms

This tool searches for the forbidden terms in the bilingual files, displays the result on the Command Prompt, and exports it into an HTML file. Command Prompt is good when the file is small and you want to quickly check what was detected. The Summary result is useful when you are working on a "View." Some characters are non-printable on Command Prompt. The HTML file is useful when you have many matches and you want to use filtering features.

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
- Export bilingual file(s) from memoQ
- Open the program by double-clicking Check Forbidden.exe or its alias
- Choose bilingual file(s) by clicking "Bilingual" or by typing / pasting the path to the file
- Choose CSV or text file(s) containing the list of forbidden terms, or a Python script
- Specify the path and the name of the result file to be exported if necessary. The default path is the first bilingual file's path + "checked_result.html"
- Adjust other options as needed
- Click "Run!"
- The result is displayed in the Command Prompt. If exporting is enabled and any matches are found, they are also exported into an HTML file
- Click "X" (close) button to exit the program

![Result](https://raw.github.com/wiki/ShunSakurai/check_forbidden/check_forbidden_result.png)

### Tips
- The check is done quickly if all bilingual files are combined into a "view"
- The check is done quickly if the bilingual files are located on your local PC rather than on a shared drive
- If you type or paste a path into the entry field and press the button to choose the file(s) afterwards, browsing starts from the folder written in the field
- When any of the entry field is filled, you can open the folder by pressing the arrow on the right
- The result is displayed for both individual and whole files (as the "Summary")

### Options
You can specify what kind of segments to include in the search range. To display the options pane, click on the gear ⚙ icon. To hide the pane, click on the triangle ▼ icon.

You can also specify whether you save the last used options. A file named "cf_options.p" is created in "C:\Users\<UserName>\AppData\Roaming\Check Forbidden" (on Windows).

![Options](https://raw.github.com/wiki/ShunSakurai/check_forbidden/check_forbidden_options.png)

### memoQ file types
Two file types are supported:

- .mqxliff
- .mqxlz

A .mqxlz file is a compressed file of a document.mqxliff file, a skeleton (formatting information), and sometimes the version information. The program extracts the document.mqxliff to a folder and removes it when the processing is finished.

### CSV file formats
The term list needs to meet the following specifications:

- Delimiter: comma
- Encoding: UTF-8
- Any special characters (`(`, `)`, `[`, `]`, `.`, `\*`, `?`, `!` ,etc.) used in regex need to be **escaped with a backslash**. All terms are considered as regex patterns
- Terms in the **first** column will be considered as the forbidden terms
- You can use other columns to provide detailed information e.g. the index number, the source term, and the correct target term
- Comma cannot be used in the file name

![CSV](https://raw.github.com/wiki/ShunSakurai/check_forbidden/check_forbidden_csv.png)

### Regular expressions
- This program uses the syntax in [re](https://docs.python.org/3/library/re.html) module
- memoQ's regex for tags `\tag` is not currently supported
- (Example) `[0-9A-Za-z]\s[^!-~]` and `[^!-~]\s[0-9A-Za-z]` search for whitespace inserted between ASCII half-width characters and other characters including full-width characters
- (Example) `\\)\S` searches for a bracket without whitespace around it

### Call external functions
When the function check box is selected, you can call a function from an external Python script. *Specifications below are to be changed soon.*

- Call a function named "function" in an external Python script, which takes six arguments: segment ID (integer), the source segment (string), target segment (string), match percentage (integer), locked status (boolean), target same as source (boolean)
- The function should return a 2D list for each segment, each inner list representing one line in the result display both on Command Prompt and in the HTML table

Code example:
calculate_width.py
```python
import re
pattern_half_width = re.compile(r'[ -~]')

def function(seg_id, source, target, percent, locked, same):
    length_half = len(re.findall(pattern_half_width, target))
    length_full = len(target) - length_half
    length_total = length_half + length_full * 2
    return [[seg_id, target, length_full, length_half, length_total]]
```

### Keyboard shortcuts
Buttons can be selected by pressing the underlined characters on the keyboard. For other buttons without an underline, they can be invoked with the following keys:

- Run!: Return (Enter)
- Show or hide the options: O
- Open the folder: no shortcut key

You can move along the UI items with "Tab" key and invoke the focused item with the space bar.

The shortcut keys are disabled when the cursor is in the entry fields. That allows you to type directly in the fields.

## Answers to FAQ, and known issues and workarounds

### Word separation is not taken in account
This program treats each segment just as a string. It does not distinguish each word.

- `play` matches both `playing` and `display`

### Case sensitive
This program is case-sensitive. If necessary, add terms to the CSV file in both upper and lower cases.

### Garbled display on Command Prompt
Sometimes multi-byte characters on Windows Command Prompt seem garbled. To correct this, right click on the title bar, select "Properties / Font," and choose a larger font or another font. Press Alt + Space and then P to quickly access the Properties.

![Garbled](https://raw.github.com/wiki/ShunSakurai/check_forbidden/check_forbidden_garbled.png)

### _extract folder is not deleted
_extract folders are created when opening the .mqxlz files in the same folder as the files. Sometimes the program fails to delete them, when an error happens. In that case, please delete them by yourself.

### &, >, and < are converted to special entities by memoQ
- Avoid adding `&`, `;`, etc.
- Use `&amp;`, `&gt;`, and `&lt;` instead of `&`, `>`, and `<`
- If `<` is used in look behind `(?<=)` in regular expression, that is OK

### Some special characters in the CSV file cause an error
- When a comma is included in the CSV file, it may be interpreted as the delimiter
- When characters with accents are included in the CSV file, they can be used correctly for checking, but they are not printed correctly on Command Prompt
- When the following character is included in the CSV file, the program throws an error: `μ`

### False positives
Below are some best practices to avoid false positives.

- Add ` play` or `\splay` (space + play) in CSV to avoid matching `display`
- Avoid using too short terms, such as `等` (など) in order avoid matching `等級`
- When many false positives are found for 1 term, consider dividing the CSV file

### Things to do when searching takes too long time
- Consider using Exclude 100%/101% matches or Exclude Locked options
- Consider creating a view for multiple documents (files)

## Features to come
### Working on
- Show whitespace characters in HTML file
- Save term lists and their paths as favorites
- Make the program window re-sizable
- Exclude memoQ tags `{1}`, which is `<x id="1" />` in mqxliff file

### Maybe later
- Add an ability to handle non-memoQ files
- Create forbidden term list for [Microsoft Style Guide](https://www.microsoft.com/Language/en-US/StyleGuides.aspx) as an example
- Make the program callable from external programs

### Features not coming
- Add file by dragging. The drag and drop feature is hard to use in tkinter
- Mark and ignore false positives. It is technically difficult
- Add settings to specify the row of forbidden terms
- Warn if non-escaped characters are included in the term list. `&lt;` and `<` cannot be distinguished
- Add an ability to choose multiple bilingual files from different folders. Not very important

Please let me know from [Github Issues](https://github.com/ShunSakurai/check_forbidden/issues) or [Asana](https://app.asana.com/0/264039980253157/list) if you need any of the features as soon as possible.

## History
For detailed history, please go to [Releases](https://github.com/ShunSakurai/check_forbidden/releases).

"*" at the beginning means bug-fixing.

## Contribution
This is just a personal project. Any feedback and contribution from [Github Issues](https://github.com/ShunSakurai/check_forbidden/issues) or [Asana](https://app.asana.com/0/264039980253157/list) and contribution is welcome!

Dear colleague translators and PMs, please help me brush up my English on this page.

## License
### Usage
You can use it for free.
© 2016-2018 Shun Sakurai

### MIT License
The code is protected under MIT License. Please see license.md for details.
