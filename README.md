# check_forbidden
A tool for checking if forbidden terms are included in the target segments of memoQ bilingual files (.mqxlz / .mqxliff)

[Japanese README](https://github.com/ShunSakurai/check_forbidden/blob/master/README_jpn.md) is also available.

![UI](https://raw.github.com/wiki/ShunSakurai/check_forbidden/check_forbidden_ui.png)

## Description
The motivation behind this tool is that even though memoQ can check forbidden source and target term pairs, it cannot check **only forbidden target terms** regardless of the corresponding source terms.

For example, you can use this tool in the following situations:

- The style guide does not allow you to use contractions such as "doesn't" and "can't" in the translation
- You can use the currency format "US$1,000" but the use of "US 1,000 dollar/Dollar" is forbidden
- JP (Japanese): You can use "次の/次に", but you cannot use "以下の/以下に"
- JP: You have to keep "例えば" in kanji, and you cannot use "たとえば"

All you have to prepare are:

- memoQ bilingual .mqxlz or .mqxliff files
- A CSV or text file containing the list of forbidden terms

This tool searches for the forbidden terms in the bilingual files, displays the result on the Command Prompt, and exports it into a CSV file.

This tool is coded in Python with tkinter and is distributed in .exe format thanks to [py2exe](http://www.py2exe.org/).

## Installation
This tool is currently only available for Windows at [Releases](https://github.com/ShunSakurai/check_forbidden/releases).
Installer is now being developed. For the moment, please do the following:

- Download dist.zip and decompress it
- Rename the folder to "check_forbidden" or any name you like
- Move it to C:\Program Files
- Create a shortcut of the .exe file and add it to your Desktop, to your tools folder, or to C:\ProgramData\Microsoft\Windows\Start Menu\Programs

When you use an updated version, you only have to move the files and folders with newer dates.
This program needs to be **kept in the folder** to work. It does not work by itself.

If you have Python environment installed, you can run the source code with `python(3) check_forbidden.py` or `import check_forbidden` even on Mac and on any OS.

## Usage

### Overview
You can open the program by double-clicking check_forbidden.exe or its alias.

- Choose bilingual file(s) by clicking "Bilingual" or by typing / pasting the path to the file
- Choose a CSV or text file containing the list of forbidden terms
- Choose the path and the name of the result file to be exported. The default is the first bilingual file's path + "checked_result.csv"
- Click "Run!"

- The result is displayed in the Command Prompt, and if any matches are found, they are also exported to the CSV file
- Once the term is found in one file, the program stops searching for that term and starts searching for the next term in the file
- The result is displayed for both individual and whole files (as the "Summary")
- Press "Enter" key or click "X" (close) button to exit the program
- You can re-run the program without closing it
- If you choose an existing CSV file as the result file, the result will be added to the bottom of it

![Result](https://raw.github.com/wiki/ShunSakurai/check_forbidden/check_forbidden_result.png)

### Options
You can specify what kind of segments to include in the search range. To display the options pane, click on the gear ⚙ icon. To hide the pane, click on the triangle ▲ icon.

![Options](https://raw.github.com/wiki/ShunSakurai/check_forbidden/check_forbidden_options.png)

### memoQ file types
Two file types are supported:

- .mqxliff
- .mqxlz

A .mqxlz file is a compressed file of a document.mqxliff file, a skeleton (formatting information), and sometimes the version information. The program extracts the document.mqxliff to a folder and removes it when everything is finished

### CSV file formats
The items need to be separated by commas, and the file needs to be encoded in UTF-8, and formatted in either of the following:

- One column of forbidden terms
- Two columns of forbidden terms and extra information (e.g. correct terms)
- Terms in the **first** column will be considered as the forbidden terms

or

- Three or more columns of e.g. the index number, the source term, the target term (forbidden), and the target term (correct)
- Terms in the **third** column will be considered as the forbidden terms

![CSV](https://raw.github.com/wiki/ShunSakurai/check_forbidden/check_forbidden_csv.png)

### Keyboard shortcuts
Buttons and radio buttons can be selected by pressing the underlined characters on the keyboard. For other buttons without an underline, they can be invoked with the following keys:

- Run! - with Enter or the space bar
- Show / hide options - with O

## Known issues and workarounds

### Garbled display on Command Prompt
Sometimes multi-byte characters on Windows Command Prompt seem garbled. To correct this, right click on the title bar, select "Properties / Font," and choose another font.

![Garbled](https://raw.github.com/wiki/ShunSakurai/check_forbidden/check_forbidden_garbled.png)

### Word separation is not taken in account
This program treats each segment just as a string. It does not distinguish each word.

- "play" matches both "playing" and "display"

### Case sensitive
This program is case-sensitive. If necessary, add terms to the CSV file in both upper and lower cases.

### Beware of false positives
Below are some best practices to avoid false positives.

Do not use single symbols used in tags and special characters:

- Avoid using <, /, >, &, ;, etc.

Add spaces:

- Add " play" (space + play) in CSV to avoid matching "display", for example

Avoid using too short terms, such as one kanji character word:

- JP: Avoid adding "等" (など) in order not to match "等級", for example

### Summary results are not in order
I use Python's "set" object to consolidate the results. This causes an issue where the Summary results are not displayed in the proper order. I am working on this issue.

## Features to come
### Working on
- Make the code more [readable](http://www.amazon.com/dp/0596802293)
- Sort the Summary results
- Prepare the installer
- Prepare the icon
- Make the window re-sizable
- Make the "Open files" dialog more useful
- Display the export path and the file name candidate when typing / pasting the path into the Bilingual file field
- Display the information about the CSV file's name and the used options at the top of the result

### Maybe later
- Enable file addition by dragging
- Add the ability to choose multiple bilingual files from different folders
- Get rid of { brackets } in the bilingual file field
- Add settings to specify the row of forbidden terms
- Add settings to specify CSV delimiters
- Add radio buttons to select export style (command prompt / CSV file)
- Add the ability to handle non-memoQ files
- Support regex in forbidden term list
- Make the path in the entry fields the initial path when pressing buttons
- Create forbidden term list for [Microsoft Style Guide](https://www.microsoft.com/Language/en-US/StyleGuides.aspx) as an example

Please let me know if you need any of the features as soon as possible.

## History
"*" at the beginning means bug-fixing.
For detailed history, please go to [Releases](https://github.com/ShunSakurai/check_forbidden/releases).

### v1.3.0, April 12, 2016
- Change the options icon
- Add keyboard shortcuts
- Add the ability to exclude 101% and 100% matches
- Add the ability to exclude locked segments
- Create an expanded pane for options
- Add and unify the text guides for the buttons
- Add a line break after the Summary results in the exported CSV file
- Divide the script part and UI part (UI part is main)
- * Exclude the TM entries attached to the bilingual files exported from WorldServer from searching
- * Fix a bug where Run button is pressable when disabled

### v1.1.3, April 7, 2016
- Divide the Summary results in the CSV file
- Reduce the number of files in the dist folder
- Change button names and the default name of exported csv file
- * Add a known issue: Change the font of command prompt to correct garbled multi-byte characters

### v1.1.0, March 31, 2016
- Distribute the binaries
- Made small design improvements
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
This is just a personal project and I do not really know what kind of contribution I may get. Any feedback and contribution is welcome!

## License
You can use it for free.

© 2016 Shun Sakurai
