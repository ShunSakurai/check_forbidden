# check_forbidden
This is the code for checking if forbidden target terms are included in memoQ bilingual files (.mqxlz/.mqxliff).

## Getting started
The motivation for creating this tool is that memoQ can check forbidden source and target term pairs, but it cannot check **only forbidden target terms** .

For example, you can use this tool in the following situations:

* You can use "does not" and "cannot" in the translation but Style guide does not allow you to use "doesn't" or "can't."
* You can use "US$1,000" but the use of "US 1,000 dollar/Dollar" is forbidden.

What you have to prepare:

* memoQ bilingual .mqxlz or .mqxliff files
* A CSV or text file containing the forbidden term list

This tool will search for the forbidden terms in the bilingual files, and show the result on Command Prompt, and export it to CSV file.
I coded this tool in Python and it is distributed in .exe format, thanks to [py2exe](http://www.py2exe.org/).

## Installation
It is now available only for Windows.
Installer is now being developed. For the moment, please do the following:

* Download the whole "dist" folder.
* Rename the folder to "check_forbidden"
* Move it to C:\Program Files
* Add shortcut to C:\ProgramData\Microsoft\Windows\Start Menu\Programs

This program needs to stay in the folder to work. It does not work by itself.

## Usage

### Overview
You can open the program by double-clicking check_forbidden.exe

* Choose bilingual file(s) by clicking "Bilingual" or typing / pasting the file path
* Choose CSV or text file containing the forbidden term list
* Choose the path and the file name of the result file to be exported. The default is the first bilingual file's path + result.csv
* Click "Run!"

* You can press "Enter" key or click "X" (close) button to exit the program
* You can re-run the program without closing it
* If you choose an existing file as the exported file, the result will be added in the bottom of the file

### memoQ file types

* .mqxliff
* .mqxlz This is compressed file of document.mqxliff file and skeleton (formatting info). The program extract the document.mqxliff to a folder and removes it when everything is finished.

### CSV files format
The columns have to be separated by commas and formatted in either:

* One line of forbidden terms
* Two lines of forbidden terms and extra information (e.g. correct terms)
* The **first** column will be considered as the forbidden terms

or

* Three or more lines of index, source, target (NG), and target (OK)
* The **third** column will be considered as the forbidden terms


### Word separation is not taken in account
This program treats each segment as a string.
It does not distinguish each word.

* "play" matches "playing" and "display"

### Case sensitive

This program is case-sensitive. When adding terms in CSV file, prepare them in both cases.

### Beware of false positives

* Add " play" (space + play) in CSV in order not to match "display"
* JP: Avoid adding "等" (など). It matches "等級", for example.

## History

### ver.1.0.9 March 24, 2016
* Added to GitHub

## Features to come
### Working on

* Making it [readable](http://www.amazon.com/Art-Readable-Code-Theory-Practice/dp/0596802293)
* Preparing installer
* Preparing icon
* Resizable window
* File addition by dragging
* Keyboard shortcut
* More useful "Open files" dialog

### Maybe later

* Getting rid of { brackets } in the bilingual file field
* Settings to specify the row of forbidden terms
* Settings to specify csv delimiters
* Radio buttons to select export style (command prompt / csv file)
* Handling non-memoQ files

Push me if you need any features as soon as possible.

## Credits
Copyright: Shun Sakurai

## License
You can use it for free.
