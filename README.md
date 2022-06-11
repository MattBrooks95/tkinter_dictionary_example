how it works
1. buildAddElementsUI creates the text entry widgets for the columns we can input
2. buildAddElementsUI needs to return to values, the Tkinter widget that holds the entries, and a dictionary that contains a reference to each text entry widget
3. the 'entryFieldsMap' dictionary is eventually passed to the 'add a record button' as a parameter
4. then, in the addRecord function, we use the header names to grab the reference to the tkinter widget
	* I ended up hardcoding the header strings, I don't think there is a way to do it dynamically without a lot more work)
	* I guess we could loop over them in order somehow, whatever
5. since we have the reference to the tkinter entry field, we can use its 'get' method to grab the user entered value
6. then, we just insert the data into the treeview as a new row




