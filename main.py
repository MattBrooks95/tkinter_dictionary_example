from tkinter import *
from tkinter import ttk

import csv

# https://pythonprogramminglanguage.com/read-csv/
def readCsv():
	with open('dummy.csv') as csvfile:
		#if you add a row to your csv file that is the header names,
		#you can use this dictreader function to read the csv contents
		#into an array of dictionaries
		#https://docs.python.org/3/library/csv.html#csv.DictReader
		csvReader = csv.DictReader(csvfile, delimiter=',')
		personDicts = []
		for row in csvReader:
			print(row)
			personDicts.append(row)
		return personDicts

#the tkinter window instance
def buildRoot():
	root = Tk()
	root.title('Dict of Tkinter Objects')
	root.geometry('800x600')
	#frame = ttk.Frame(root, padding=10)
	#frame.grid()
	return root

#the tree view that we'll use to store and show the values
#from the csv that we've read
#https://pythonguides.com/python-tkinter-treeview/
def buildTable(root, headers, csvContents):
	table = ttk.Treeview(root)
	table['columns'] = headers
	#I guess this ID column is mandatory???
	table.column("#0", width=0, stretch=NO)
	table.heading("#0", text='', anchor=CENTER)
	#print(table['columns'])
	for header in headers:
		table.column(header, anchor=CENTER, width=80)
		table.heading(header, text=header, anchor=CENTER)

	loopIndex = 0
	for personData in csvContents:
		print(personData)
		values = [
			personData['person'],
			personData['sex'],
			personData['hair_color'],
		]
		table.insert(
				parent='',
				index=loopIndex,
				iid=loopIndex, 
				values=values
		)
		loopIndex += 1

	return table

def buildAddElementsUi(root, headers):
	frame = ttk.LabelFrame(root, text='Add a record')
	#dictionary that maps header names to the corresponding text field
	textInputs = {}
	loopIndex = 0
	for header in headers:
		newEntry = ttk.Entry(frame)
		newEntry.grid(row=1, column=loopIndex + 1)
		textInputs[header] = newEntry
		textInputs
		loopIndex += 1
	return { 'container': frame, 'entryFieldsMap': textInputs }

def addRecord(textEntryMap, treeView):
	#hard coded way
	#addRecordWay1(textEntryMap, treeView)
	# let's try to do this dynamically
	addRecordWay2(textEntryMap, treeView)

def addRecordWay1(textEntryMap, treeView):
	#because we stored the references to the text input fields in our dictionary,
	#we can use that map and the header name to get that reference, and then use the
	#widget's 'get' file to grab the file
	newRecordName = textEntryMap['person'].get()
	newRecordSex = textEntryMap['sex'].get()
	newRecordHairColor = textEntryMap['hair_color'].get()
	#this syntax is neat for printing strings to the console
	#the items in the #{} part will be interpreted as variable names, and that
	#variable's value will be converted to a string and then inserted into this 
	#string that we are printing
	print(f'newRecordName:{newRecordName} newRecordSex:{newRecordSex} newRecordHairColor:{newRecordHairColor}')

	#I didn't know how to get the current number of rows in the table, so that
	#I could set the index for the newly created row
	#https://stackoverflow.com/questions/32525161/how-to-get-the-item-count-in-tkinter-treeview
	currentNumberOfRecords = len(treeView.get_children())
	treeView.insert(parent='', index=currentNumberOfRecords, iid=currentNumberOfRecords, values=[
		newRecordName,
		newRecordSex,
		newRecordHairColor
	])

def addRecordWay2(textEntryMap, treeView):
	newValues = []
	#items() returns a list of (key, value) tuples
	for item in textEntryMap.items():
		#we can print them
		print(item)
		#item[1] gets the second value in the tuple, which is the text entry object
		textEntryWidget = item[1]
		#get the string from the text entry widget
		newValues.append(textEntryWidget.get())
	print(newValues)
	#add the values to the treeview
	currentNumberOfRecords = len(treeView.get_children())
	treeView.insert(
		parent='',
		index=currentNumberOfRecords,
		iid=currentNumberOfRecords,
		values=newValues
	)

#entry point for the program
def main():
	csvContents = readCsv()
	if len(csvContents) <= 0:
		print('no csv file found!!! make sure to run this program from the directory you downloaded it to that contains the dummy.csv file')
		return
	#get the column headers out of the first object
	keysAsStrings = []
	#I guess the python keys method doesn't just return the dictionary keys
	#as strings anymore, it was returning a live view object. I guess to turn
	#the keys into real strings you have to write a loop
	#seems kinda dumb
	for key in csvContents[0].keys():
		keysAsStrings.append(key)
	headers = keysAsStrings
	#print(headers)
	#print(csvContents)

	#build the tkinter ui, returning the root instance
	root = buildRoot()
	#exit button so we can close it
	exitButton = ttk.Button(root, text="quit", command=root.destroy)
	exitButton.pack()

	#build a tree view (table)
	treeView = buildTable(root, headers, csvContents)
	treeView.pack()

	#I returned a dictionary, so that I could return the container widget
	#for the add record container, and for the map of header names to their
	#text entry fields
	addElementsUi = buildAddElementsUi(root, headers)
	#tkinter widget reference
	addRecordFrame = addElementsUi['container']
	#map from csv header names to the text entry field widgets
	textEntryMap = addElementsUi['entryFieldsMap']
	print(textEntryMap)
	addRecordFrame.pack()

	#use the 'lambda' keyword to create an anonymous function that passes the
	#map of header names to text entry widgets
	#into the add record method
	#you could just make this map a global variable, or use a class somehow but this would
	#be the functional programming way to do it
	#it's nice because the addRecord function has references to only the values that it needs
	#it avoids a soup of global variable names
	newRecordButton = ttk.Button(
		root,
		text='add a new record',
		command=lambda: addRecord(textEntryMap, treeView)
	)

	newRecordButton.pack()
	root.mainloop()

main()

