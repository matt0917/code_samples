

### TEST NOTES

## Steps to Run File Finder

# No Primary key is set in the DB due to the lack of identification with fiie path
- dependencies: python2.7 pyside, pysqlite3
- Locate the 'work' folder under your venv container folder has "get-pip.py"
- I recommend using Powershell like terminals
- `cd [Your venv container folder]:\work`
- Set the virtual environment in the current sesson
- `.\Scripts\activate`
- Run file finder main gui
- `py .\file_finder\app\gui\main.pyw`
- Once you lauch the file_finder GUI, **found_files.db** will be created under file_finder folder automatically.
- 1. Select a desire file type to search in the /files folder
- 2. Press Search button to find the selected type files
- Submit button should be active state at that point.
- 3. Press Submit button to add listed files data to the DB
- 4. Confirm the submitted file data in the list widget of the window. Now all newly fetched data from DB are listed in the list widget with colored **green**.
- Repeat step 1 - 4 to test for different types of files as neccessary.
- Finally, you can see the newly created "found_files.db" in the **"work\file_finder"** folder
- To check the data in the table, use a DB engine applcation such as **sqLiteStudio**.
- **Every time when the GUI session is closed, found_files.db is deleted automatically and tool creates a new table with a new GUI session**
