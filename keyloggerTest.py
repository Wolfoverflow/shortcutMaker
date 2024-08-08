import os
import sys
try:
    from pynput import keyboard
except ModuleNotFoundError:
    os.system(f"{executable} -m pip install pynput")
    from pynput import keyboard
import csv
import time
import threading

os.chdir(os.path.dirname(__file__))

# check if keylogger.csv exists
if not os.path.exists("keylogger.csv"):
    with open("keylogger.csv", 'w') as f:
        f.write("")

recording = False
keystrokes = []

class KeyLogger:
    def __init__(self, keystrokes):
        self.currentKeys = []
        self.recordedKeys = []
        self.keystrokes = keystrokes

    def onPress(self, key):
        """
        Wolfoverflow
        Adds the given key to the currentKeys list if it is not already present.
        If recording is True, also adds the key to the recordedKeys list.

        Parameters:
            key (str): The key to be added to the currentKeys list.

        Returns:
            None
        """
        key = str(key).strip("'")
        if key not in self.currentKeys:
            self.currentKeys.append(key)
            if recording:
                self.recordedKeys.append(key)

    def onRelease(self, key):
        """
        Wolfoverflow
        Removes the given key from the currentKeys list if it is present.

        Parameters:
            key (str): The key to be removed from the currentKeys list.

        Returns:
            None
        """
        key = str(key).strip("'")
        if key in self.currentKeys:
            self.currentKeys.remove(key)

    def keystrokeRecorder(self, key, recording=False):
        """
        Wolfoverflow
        Passes the given key to the appropriate function, returning a shortcut ID or current keystrokes.

        Parameters:
            key (str): The key to be parsed.
            recording (bool, optional): Whether the key is being recorded. Defaults to False.

        Returns:
            int or None: The ID of the shortcut if detected, None otherwise.
            currentKeys (set): The current keys being pressed.
        """
        self.onPress(key)
        currentKeys = set(self.currentKeys)
        if recording:
            return currentKeys
        else:
            if currentKeys in self.keystrokes:
                for IDNumber,shortcutID in enumerate(self.keystrokes):
                    if currentKeys == shortcutID:
                        # print(f"Shortcut {shortcutID} with ID {IDNumber} was pressed")
                        return IDNumber

        # print("Current keys:", ", ".join(self.currentKeys))
        # print(self.currentKeys)

def onPress(key):
    """
    Wolfoverflow
    Adds the given key to the currentKeys list if it is not already present.

    Parameters:
        key (str): The key to be added to the currentKeys list.

    Returns:
        None
    """
    global recording
    id = keyLogger.keystrokeRecorder(key, recording)
    if id is not None and not recording:
        commandRunner(id, csvParser("keylogger.csv"))

def onRelease(key):
    """
    Wolfoverflow
    Release the given key by calling the `onRelease` method of the `keyLogger` object.

    Parameters:
        key (str): The key to be released.

    Returns:
        None
    """
    keyLogger.onRelease(key)

def startRecording():
    """
    Wolfoverflow
    Starts the keylogger recording process.

    Sets the global recording flag to True, indicating that the keylogger is actively recording keystrokes.

    Parameters:
        None

    Returns:
        None
    """
    global recording
    recording = True

def stopRecording():
    """
    Wolfoverflow
    Stop the recording and return the set of recorded keys.

    This function sets the global `recording` variable to `False`, which stops the keylogger from blocking macros

    Returns:
        set: The set of recorded keys.
    """
    global recording
    recording = False
    return set(keyLogger.recordedKeys)

# Usage
# Format for keystrokes:


# # CSV format
# | shortcutID | keys              | batchCommand | creationDate | shortcutName |
# |------------|-------------------|--------------|--------------|--------------|
# | 0          | {'Key.ctrl', 'm'} | echo Pass    | 1/1/1970     | Pass         |
# | 1          | {'Key.cmd', ';'}  | echo Pass1   | 1/1/2000     | Pass1        |
# |------------|-------------------|--------------|--------------|--------------|

def csvParser(filename, includeRowNumber = False):
    """
    Wolfoverflow
    This function parses a CSV file and returns the data in a structured format.

    Parameters:
        filename (str): The name of the CSV file to parse.
        includeRowNumber (bool): An optional parameter to include the row number in the parsed data. Defaults to False.

    Returns:
        list: A list of lists, where each sublist contains the parsed data for a row in the CSV file.
    """
    parsedData = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row == []:
                continue
            keys = set(eval(row[1]))
            batchCommand = row[2]
            creationDate = row[3]
            name = row[4]
            parsedRow = [keys, batchCommand, creationDate, name]
            if includeRowNumber:
                parsedRow.insert(0, int(row[0]))
            parsedData.append(parsedRow)

    return parsedData

def shortcutWriter(filename, parsedData):
    """
    Writes a new row to the given CSV file with the provided parsed data.

    Parameters:
        filename (str): The name of the CSV file to write to.
        parsedData (list): A list of data to write to the CSV file.

    Returns:
        None
    """
    allottedID = 0
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row == []:
                continue
            allottedID = int(row[0]) + 1
    with open(filename, 'a') as f:
        writer = csv.writer(f)
        writer.writerow([allottedID, parsedData[0], parsedData[1], parsedData[2], parsedData[3]])

def csvShortcutDeleter(filename, id, parsedData):
    """
    Wolfoverflow
    Deletes a shortcut from the specified CSV file.

    Args:
        filename (str): The name of the CSV file.
        id (int): The ID of the shortcut to delete.
        parsedData (list): The parsed data from the CSV file.

    Returns:
        None
    """
    global keystrokes
    correctedID = 0
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        for currentID, shortcut in enumerate(parsedData):
            if currentID != id:
                print([correctedID, shortcut[0], shortcut[1], shortcut[2], shortcut[3]])
                print("ID of", currentID)
                writer.writerow([correctedID, shortcut[0], shortcut[1], shortcut[2], shortcut[3]])
                correctedID += 1
            else:
                print("Skipping ID", id)
    keystrokes = keystrokeParser(csvParser("keylogger.csv"))


def keystrokeParser(parsedData):
    """
    Wolfoverflow
    Parses the given parsedData and returns a list of keystrokes.

    Parameters:
        parsedData (list): A list of lists, where each list represents a component of a shortcut.

    Returns:
        set: A set of keystrokes.
    """
    keystrokes = []
    for shortcut in parsedData:
        keystrokes.append(shortcut[0])
    return keystrokes

def commandRunner(id, parsedData):
    """
    Wolfoverflow
    Executes the command associated with the given shortcut.

    Parameters:
        id (int): The ID of the shortcut to execute.
        parsedData (list): A list of lists, where each list represents a component of a shortcut.

    Returns:
        None
    """
    global recording
    os.system(parsedData[id][1])

keystrokes = keystrokeParser(csvParser("keylogger.csv"))
keyLogger = KeyLogger(keystrokes)

# Start the listener
def keyboardListener():
    """
    Starts the keyboard listener.

    Parameters:
        None

    Returns:
        None
    """
    with keyboard.Listener(on_press=onPress, on_release=onRelease) as listener:
        listener.join()

thread = threading.Thread(target=keyboardListener)
thread.start()

def shortcutMaker(name, command, shortcut):
    global keystrokes
    shortcutData = [shortcut, command, time.strftime("%d/%m/%Y"), name]
    shortcutWriter("keylogger.csv", shortcutData)
    keystrokes = keystrokeParser(csvParser("keylogger.csv"))

def dataDictionary(filename):
    dataDictionary = {}
    records = csvParser(filename, True)
    for record in records:
        id = record[0]
        data = record[1::]
        dataDictionary[id] = data
    return dataDictionary

def dictionarySplitter(dictionary): # Extra complication by converting to and back from a dictionay
    keyArray = []                   # After all, why else does this branch exist?
    valueArray = []
    for id in dictionary:
        key = id
        value = dictionary[id]
        keyArray.append(key)
        valueArray.append(value)
    return keyArray, valueArray

def shortcutEditor(id, shortcutData):
    global keystrokes
    csvShortcutDeleter("keylogger.csv", id, shortcutData)
    shortcutWriter("keylogger.csv", shortcutData)
    csvCleaner("keylogger.csv")
    keystrokes = keystrokeParser(csvParser("keylogger.csv"))

def selectionSort(value, pair):
    collection = []
    
    length = len(value) # gets len of the list
    for i in range(length - 1): # Gets the actual length (index form)
        sortedItems = i
        for j in range(i + 1, length):
            if value[j] < value[sortedItems]:
                sortedItems = j
        if length != i:
            value[i], value[sortedItems] = value[sortedItems], value[i]
            pair[i], pair[sortedItems] = pair[sortedItems], pair[i]

    for id, data in zip(value, pair):
        data.insert(0, id)
        data.append(collection)
        
    return collection

def csvSorter(filename):
    return selectionSort(disctionarySplitter(dataDictionary(filename)))

def csvCleaner(filename):
    sortedData = csvSorter(filename)
    with open(filename, 'w') as w:
        writer = csv.writer(w)
        for formattedData in sortedData:
            writer.writerow([formattedData[0], formattedData[1], formattedData[2], formattedData[3], formattedData[4]])

def editingMode():
    global keystrokes
    if "y"==input("Create shortcut? (y/n): "):
        name = input("Enter shortcut name: ")
        startRecording()
        print("Recording started. Please hold shortcut for 3 seconds.")
        time.sleep(2.5)
        shortcut = stopRecording()
        time.sleep(0.5)
        print(f"Captured shortcut: {shortcut}")
        keyLogger.recordedKeys = []
        command = input("Enter action: ")
        shortcutData = [shortcut, command, time.strftime("%d/%m/%Y"), name]
        shortcutWriter("keylogger.csv", shortcutData)
        keystrokes = keystrokeParser(csvParser("keylogger.csv"))
        print("The shortcut has been saved.")
    else:
        id = int(input("Enter shortcut ID to delete: "))
        csvShortcutDeleter("keylogger.csv", id, csvParser("keylogger.csv"))

# Note: The following section will no longer be utilised in the tkinter version.
# while True:
#     try:
#         editingMode() if "y"==input("Edit shortcuts? (y/n): ") else False
#     except KeyboardInterrupt:
#         print("Quitting keylogger...")
#         os.kill(os.getpid(), 9)
# csvCleaner("keylogger.csv")
