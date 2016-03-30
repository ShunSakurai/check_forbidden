# check_forbidden
This code is for checking if forbidden terms are included in the target segments of memoQ bilingual files (.mqxlz / .mqxliff).

[Japanese README](https://github.com/ShunSakurai/password/blob/master/README_jpn.md) is also available.

## Description
The motivation behind this tool is that even though memoQ can check forbidden source and target term pairs, it cannot check **only forbidden target terms** regardless of the corresponding source terms.

For example, you can use this tool in the following situations:

- Style guide does not allow you to use contractions such as "doesn't" and "can't" in the translation
- You can use "US$1,000" but the use of "US 1,000 dollar/Dollar" is forbidden
- JP (Japanese): You can use "次の/次に", but you cannot use "以下の/以下に"
- JP: You have to keep "例えば" in kanji, you cannot use "たとえば"

You have to prepare:

- memoQ bilingual .mqxlz or .mqxliff files
- A CSV or text file containing the list of forbidden terms

This tool searches for the forbidden terms in the bilingual files, displays the result on Command Prompt, and exports it to CSV file.

This tool is coded in Python with tkinter and is distributed in .exe format thanks to [py2exe](http://www.py2exe.org/).

## Installation
It is currently only available for Windows at [Releases](https://github.com/ShunSakurai/check_forbidden/releases).
Installer is now being developed. For the moment, please do the following:

- Download dist.zip and decompress it
- Rename the folder to "check_forbidden" or any name you like
- Move it to C:\Program Files
- Create a shortcut of the .exe file and add it to your Desktop, to your tools folder, or to C:\ProgramData\Microsoft\Windows\Start Menu\Programs

This program needs to be **kept in the folder** to work. It does not work by itself.

## Usage

### Overview
You can open the program by double-clicking check_forbidden.exe or its alias.

- Choose bilingual file(s) by clicking "Bilingual" or type / paste the path to the file
- Choose CSV or text file containing the list of forbidden terms
- Choose the path and the file name of the result file to be exported. The default is the first bilingual file's path + result.csv
- Click "Run!"

![UI](https://raw.github.com/wiki/ShunSakurai/check_forbidden/check_forbidden_ui.png)

- Result is displayed in Command Prompt, and if any match is found, it is also exported to CSV file
- Once the term is found in one file, the program stops searching for that term and starts searching for it in the next file
- Result is displayed for each file, and for the whole files (as the "Summary")
- You can press "Enter" key or click "X" (close) button to exit the program
- You can re-run the program without closing it
- If you choose an existing CSV file as the result file, the result will be added to the bottom of it

![Result](https://raw.github.com/wiki/ShunSakurai/check_forbidden/check_forbidden_result.png)

### memoQ file types
Two file types are supported:

- .mqxliff
- .mqxlz, which is a compressed file of document.mqxliff file and skeleton (formatting information). The program extracts the document.mqxliff to a folder and removes it when everything is finished

### CSV files format
The items need to be encoded in UTF-8, separated by commas, and formatted in either:

- One line of forbidden terms
- Two lines of forbidden terms and extra information (e.g. correct terms)
- Terms in the **first** column will be considered as the forbidden terms

or

- Three or more lines of e.g. index, source term, target term (forbidden), and target term (correct)
- Terms in the **third** column will be considered as the forbidden terms

![CSV](https://raw.github.com/wiki/ShunSakurai/check_forbidden/check_forbidden_csv.png)

### Word separation is not taken in account
This program treats each segment just as a string. It does not distinguish each word.

- "play" matches both "playing" and "display"

### Case sensitive
This program is case-sensitive. When adding terms in the CSV file, prepare them in both cases.

### Beware of false positives
Below are some best practices to avoid false positives.
Add spaces:

- Add " play" (space + play) in CSV to avoid matching "display", for example

Avoid using too short terms, such as one kanji character word:

- JP: Avoid adding "等" (など) in order not to match "等級", for example

## Features to come
### Working on
- Making it [readable](http://www.amazon.com/dp/0596802293)
- Preparing installer
- Preparing icon
- Resizable window
- Keyboard shortcuts
- More useful "Open files" dialog
- Sorting Summary results on Command Prompt
- Dividing Summary results in the CSV file

### Maybe later
- File addition by dragging
- Choosing multiple bilingual files from different folders
- Getting rid of { brackets } in the bilingual file field
- Settings to specify the row of forbidden terms
- Settings to specify CSV delimiters
- Radio buttons to select export style (command prompt / CSV file)
- Handling non-memoQ files
- Support regex in forbidden term list

Please let me know if you need any of the features as soon as possible.

## History
"*" at the beginning means bug-fixing.
For detailed history, please go to [Releases](https://github.com/ShunSakurai/check_forbidden/releases).

### v1.1.0, March 31, 2016
- Distributed the binaries
- Small design improvements

### v1.0.10, March 28, 2016
- Changed the language pair from En->Jp to general Source->Target
- * Removed .txt format from the bilingual files choices, because the program started using regex when parsing the bilingual files
- Created Readme.md

### v1.0.9, March 24, 2016
- * Resolved an issue where folders are not deleted when no forbidden term is found

### v1.0.8, March 24, 2016
- Added to GitHub

### v1.0.0, March 22, 2016
### v0.9.0, March 17, 2016
- Started using it at my company

### December 8, 2015
- Bought [a book about Python](http://www.amazon.co.jp/dp/4797371595)

### Jul 30, 2015
- Came up with the idea

## Contribution
This is just a personal project and I do not really know what kind of contribution I may get. Any feedback and contribution is welcome!

## License
You can use it for free.

© 2016 Shun Sakurai
