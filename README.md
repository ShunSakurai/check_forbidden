# check_forbidden
A tool for checking if forbidden terms are included in the target segments of memoQ bilingual files (.mqxlz / .mqxliff)

[Japanese README](https://github.com/ShunSakurai/check_forbidden/blob/master/README_jpn.md) is also available.

![UI](https://raw.github.com/wiki/ShunSakurai/check_forbidden/check_forbidden_ui.png)

## Description
[memoQ](https://www.memoq.com/) allows us to check forbidden source and target term pairs using the term base, and check forbidden terms using the QA settings. However, it takes time to add each forbidden term one by one, choosing the settings.
Using this tool, you can quickly narrow down and spot the forbidden terms used in memoQ bilingual files, by using a term list in CSV format. You can use the regular expressions (regex). You can also call a function from an external Python script against the target segments. It helps you efficiently maintain the translation quality.
(memoQ recently did a great [update](https://www.memoq.com/memoq-build-june) and now allows us to check only forbidden target terms regardless of the corresponding source terms. Hope they will support CSV import to QA settings soon, like we do for term base.)

For example, you can use this tool in the following situations:

- The style guide does not allow you to use contractions such as "doesn't" and "can't" in the translation
- The style guide does not allow you to use a whitespace between a half-width character and a full-width character
- JP (Japanese): You can use "次の/次に", but you cannot use "以下の/以下に"
- JP: You have to keep "例えば" in kanji, and you cannot use "たとえば"

All you have to prepare are:

- memoQ bilingual .mqxlz or .mqxliff files
- A CSV file or a text file containing the list of forbidden terms

This tool searches for the forbidden terms in the bilingual files, displays the result on the Command Prompt, and exports it into a CSV file. Command Prompt is good for browsing the result and quickly checking what was detected. The CSV file is useful when you have many matches and when many non-printable characters are included in the bilingual file. The Summary result is useful when you are working on a "View.''

This program is coded in Python with tkinter and is distributed in .exe format through [py2exe](http://www.py2exe.org/).

The icon was created with [アイコン ウィザード](http://freewareplace.web.fc2.com/) and the installer is created with [Inno Setup](http://www.jrsoftware.org/isdl.php).

## Installation
This tool is currently only available for Windows at [Releases](https://github.com/ShunSakurai/check_forbidden/releases).

All you have to do for installation and upgrading is to download and run the installer.

This program needs to be **kept in the folder** to work. It does not work by itself.

If you have the Python environment installed, you can run the source code with `python(3) check_forbidden.py` or `import check_forbidden` even on Mac and on any OS.

## Build
To convert the Python code to an .exe file, and to create an installer, follow steps below.

Requirements and procedures for the .exe file:

- Python 3.4 (py2exe is not compatible with Python 3.5 as far as I know)
- [py2exe](http://www.py2exe.org/)
- Run `py -3.4 setup.py py2exe` on a Windows machine

Requirements and procedures for the installer:

- [Inno Setup](http://www.jrsoftware.org/isdl.php)
- Open setup_installer.iss with Inno Setup Compiler and click Build > Compile

## Usage

### Overview
- You can open the program by double-clicking Check Forbidden.exe or its alias
- Choose bilingual file(s) by clicking "Bilingual" or by typing / pasting the path to the file
- Choose a CSV file or a text file containing the list of forbidden terms
- Choose the path and the name of the result file to be exported or disable exporting by selecting the check box. The default is the first bilingual file's path + "checked_result.csv"
- Click "Run!"
- The result is displayed in the Command Prompt, and if any matches are found and exporting is enabled, they are also exported into the CSV file
- Press "Enter" key or click "X" (close) button to exit the program

![Result](https://raw.github.com/wiki/ShunSakurai/check_forbidden/check_forbidden_result.png)

### Tips
- If you type or paste a path into the entry field and press the button to choose the file(s) afterwards, browsing starts from the path in the field
- When any of the entry field is filled, you can open the folder by pressing the arrow on the right
- The result is displayed for both individual and whole files (as the "Summary")
- You can re-run the program without closing it
- If you choose an existing CSV file as the result file, the result will be added to the bottom of it

### Options
You can specify what kind of segments to include in the search range. To display the options pane, click on the gear ⚙ icon. To hide the pane, click on the triangle ▲ icon.

![Options](https://raw.github.com/wiki/ShunSakurai/check_forbidden/check_forbidden_options.png)

### memoQ file types
Two file types are supported:

- .mqxliff
- .mqxlz

A .mqxlz file is a compressed file of a document.mqxliff file, a skeleton (formatting information), and sometimes the version information. The program extracts the document.mqxliff to a folder and removes it when everything is finished.

### CSV file formats
The term items need to be separated by comma. The file needs to be encoded in UTF-8. All terms are considered as regex, so all the special characters ('(', ')', '[', ']', '.', '\*', '?', '!' ,etc.) used in regex need to be **escaped** with a backslash.

- Terms in the **first** column will be considered as the forbidden terms
- You can use the other columns to provide detailed information e.g. the index number, the source term, and the correct target term

![CSV](https://raw.github.com/wiki/ShunSakurai/check_forbidden/check_forbidden_csv.png)

The exported result CSV file is encoded in UTF-8 with BOM (Python utf-8-sig) with commas as the delimiters. Be careful about the encoding when opening the file with some programs.

### Regular expressions
- Add [0-9A-Za-z]\s[^!-~] and [^!-~]\s[0-9A-Za-z] to search for whitespace inserted between ASCII half-width characters and other characters including full-width characters
- Add \\)\S to search for a bracket without whitespace around it
- Currently memoQ's regex for tags (\tag) is not supported

### Call external functions
When the function check box is selected, you can call a function from an external Python script.

- Call a function named 'function' in an external Python script, which takes segment ID (integer) and the target segment (string)
- The function should return a list of lists for each segment, each inner list representing one line in the result display both on Command Prompt and in the CSV file

Code example:
calculate_width.py
```
import re
pattern_half_width = re.compile(r'[ -~]')

def function(seg_id, target):
    length_half = len(re.findall(pattern_half_width, target))
    length_full = len(target) - length_half
    length_total = length_half + length_full * 2
    return [[seg_id, target, length_full, length_half, length_total]]
```

### Keyboard shortcuts
Buttons and radio buttons can be selected by pressing the underlined characters on the keyboard. For other buttons without an underline, they can be invoked with the following keys:

- Run!: with the space bar
- Show / hide the options: with O
- Turn the export method check box on /off: with C
- Turn the function check box on /off: with F
- Open the folder: no shortcut key

The "Enter (Return)" key can be used to invoke the focused widget.

The shortcut keys are disabled when the cursor is in the entry fields. That allows you to type directly in the fields.

## Answers to FAQ, and known issues and workarounds

### Word separation is not taken in account
This program treats each segment just as a string. It does not distinguish each word.

- "play" matches both "playing" and "display"

### Case sensitive
This program is case-sensitive. If necessary, add terms to the CSV file in both upper and lower cases.

### Garbled display on Command Prompt
Sometimes multi-byte characters on Windows Command Prompt seem garbled. To correct this, right click on the title bar, select "Properties / Font," and choose a larger font or another font. The quickest way to open the Properties may be to press Alt + Space and then P.

![Garbled](https://raw.github.com/wiki/ShunSakurai/check_forbidden/check_forbidden_garbled.png)

### _extract folder is not deleted
_extract folders are created when opening the .mqxlz files. Sometimes the program fails to delete them, when an error happens. In that case, please delete them by yourself.

### &, >, and < are converted to special entities by memoQ
- Avoid adding &, ;, etc.
- Use `&amp;`, `&gt;`, and `&lt;` instead of &, >, and <
- If < is used in look behind (?<=) in regular expression, that is OK

### Some special characters in the CSV file cause an error
- When a comma is included in the CSV file, it may be interpreted as the delimiter
- When characters with accents are included in the CSV file, they can be used correctly for checking, but they are not printed correctly on Command Prompt
- When the following character is included in the CSV file, the program throws an error: 'μ'
- The program can handle the following characters without a problem: '©', '®', '™'

### False positives
Below are some best practices to avoid false positives.

- Add " play" or "\splay" (space + play) in CSV to avoid matching "display"
- Avoid using too short terms, such as "等" (など) in order avoid matching "等級"
- When many false positives are found for 1 term, consider dividing the CSV file

### Summary results are not in order
I use Python's "set" object to consolidate the results. This causes an issue where the Summary results are not displayed in the proper order. This issue will be addressed in the future.

## Features to come
### Working on
- Make the code more [readable](http://www.amazon.com/dp/0596802293)
- Sort the Summary results
- Make the window re-sizable
- Make the "Open files" dialog more useful
- Create a tk pane for displaying and filtering the result

### Maybe later
- Add an ability to choose multiple bilingual files from different folders
- Get rid of { brackets } in the bilingual file field
- Add settings to specify CSV delimiters
- Add an ability to handle non-memoQ files
- Create forbidden term list for [Microsoft Style Guide](https://www.microsoft.com/Language/en-US/StyleGuides.aspx) as an example
- Make the program callable from external programs
- Automate the test

### Features not coming
- Add file by dragging. The drag and drop feature is hard to use in tkinter
- Mark and ignore false positives. It is technically difficult
- Add settings to specify the row of forbidden terms
- Warn if non-escaped characters are included in the term list. `&lt;` and < cannot be distinguished

Please [let me know](https://app.asana.com/-/share?s=132227284282305-bvBtn99BajlghI1nePsyD62jRMGpbZdaHxdnO7Qps8Y-29199191293549) if you need any of the features as soon as possible.

## History
"*" at the beginning means bug-fixing.
For detailed history, please go to [Releases](https://github.com/ShunSakurai/check_forbidden/releases).

### Newest version
- * Resolve an issue where historical units are included

### v1.7.0, August 21, 2016
- Call external Python function against the target segment
- Exclude the blank segment <target xml:space="preserve"></target>
- Display the shortcut key when hovering over that UI element

### v1.6.8, July 29, 2016
- Add BOM to the result file to prevent garbled display on Excel
- Semiautomate the set-up process with shutil module

### v1.6.7, July 27, 2016
- Display the number of found matches
- Make segment ID visible when the target segment is non-printable

### v1.6.5, July 19, 2016
- Measure speed
- Make readability improvements and fix some bugs
- Reduce memory usage by loading the files iteratively
- * Resolve an issue where replacing slashes does not work

### v1.6.1, July 4, 2016
- Create the installer

### v1.6.0, June 30, 2016
- Display the memoQ segment ID in results
- Make small design improvements and fix some bugs

### v1.5.10, June 23, 2016
- Add buttons to open the folders from inside the program
- Display the version number
- Make the code more readable
- * Re-resolve an issue where printing a special character fails

### v1.5.6, June 21, 2016
- * Avoid errors caused by no-breaking spaces in the bilingual file

### v1.5.5, June 14, 2016
- Create the icon

### v1.5.4, June 8, 2016
- * Resolve an issue where printing a special character fails

### v.1.5.3, June 6, 2016
- Display the header row of the CSV file
- * Resolve an issue where the result path candidate is not displayed
- * Resolve an issue where the result button is pressable when disabled

### v1.5.0, June 1, 2016
- Always make the first column of the CSV or the text file the forbidden term
- Support regex in the forbidden term list
- Display the result within the context
- Make 'Command Prompt only.' the default choice
- Add contact information

### v1.4.16, May 12, 2016
- Implement Python's recommendations
- Add the link to memoQ
- * Resolve an issues around the result file path
- * Resolve an issues around the bilingual file path

### v1.4.14, May 6, 2016
- Exclude tags from searching
- Display the export path and the file name candidate when typing / pasting the path into the Bilingual file field
- Make the path in the entry fields the initial path when pressing buttons
- * Create test cases and resolve some issues

### v1.4.10, May 1, 2016
- Add a check box to select the exporting styles (Command Prompt only / CSV file)
- Keep the entry fields uncleared when open file dialog is canceled

### v1.4.8, April 29, 2016
- * Resolve an issue where the search fails when a br tag is in the target segment

### v1.4.7, April 28, 2016
- Display the current time, the CSV file's name, and the used options at the top of the result
- Assign the return (enter) key to each widget's event
- * Resolve an issue where folders are not deleted when the result CSV file is already open

### v1.4.4, April 28, 2016
- Add some information users need to know when they use this program for the first time
- Disable the keyboard shortcuts when the cursor is in the entry fields
- Change the label of the second button from CSV to Terms
- * Resolve an issue where multiple filetypes arguments prevent selecting files on Mac

### v1.4.0, April 23, 2016
- Change the application name to 'Check Forbidden'
- Ensure the name of the result file ends with .csv
- Reduce the size of the dist folder
- Enable choosing .mqxlz and .mqxliff files at the same time
- Add a splash message
- * Add a known issue: Avoid using single symbols used in tags and special characters

### v1.3.0, April 12, 2016
- Change the options icon
- Add keyboard shortcuts
- Add an ability to exclude 101% and 100% matches
- Add an ability to exclude locked segments
- Create an expanded pane for options
- Add and unify the text guides for the buttons
- Add a line break after the Summary results in the exported CSV file
- Divide the script part and UI part (UI part is main)
- * Exclude the TM entries attached to the bilingual files exported from WorldServer from searching
- * Resolve an issue where Run button is pressable when disabled

### v1.1.3, April 7, 2016
- Divide the Summary results in the CSV file
- Reduce the number of files in the dist folder
- Change button names and the default name of exported csv file
- * Add a known issue: Change the font of command prompt to correct garbled multi-byte characters

### v1.1.0, March 31, 2016
- Distribute the binaries
- Make small design improvements
- Create README_jpn.md

### v1.0.10, March 28, 2016
- Change the language pair from En->Jp to more general Source->Target
- Create README.md
- * Remove .txt format from the bilingual files choices, because the program started using regex when parsing the bilingual files

### v1.0.9, March 24, 2016
- * Resolve an issue where folders are not deleted when no forbidden term is found

### v1.0.8, March 24, 2016
- Add to GitHub

### v1.0.0, March 22, 2016
### v0.9.0, March 17, 2016
- Start using it at my company

### December 8, 2015
- Buy [a book about Python](http://www.amazon.co.jp/dp/4797371595)

### Jul 30, 2015
- Come up with the idea

## Contribution
This is just a personal project and I do not really know what kind of contribution I may get. Any [feedback](https://app.asana.com/-/share?s=132227284282305-bvBtn99BajlghI1nePsyD62jRMGpbZdaHxdnO7Qps8Y-29199191293549) and contribution is welcome!

Dear colleague translators and PMs, please help me brush up my English on this page.

## License
You can use it for free.

© 2016 Shun Sakurai
