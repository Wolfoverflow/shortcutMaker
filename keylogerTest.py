import os
try:
    from pynput import keyboard
except ModuleNotFoundError:
    os.system("py -m pip install pynput")
import csv
import time
import threading

os.chdir(os.path.dirname(__file__))

# check if keylogger.csv exists
if not os.path.exists("keylogger.csv"):
    with open("keylogger.csv", 'w') as f:
        f.write("")

recording = False

class KeyLogger:
    def __init__(self, keystrokes):
        self.currentKeys = []
        self.recordedKeys = []
        self.keystrokes = keystrokes

    def onPress(self, key):
        """
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
    keyLogger.onRelease(key)

def startRecording():
    global recording
    recording = True

def stopRecording():
    global recording
    recording = False
    return keyLogger.recordedKeys

# Usage
# Format for keystrokes: 
#   [[{'Key.ctrl', 'm'}, batchCommand], [{'Key.cmd', ';'}, batchCommand]... ]

# # CSV format
# | shortcutID | keys              | batchCommand | creationDate | shortcutName |
# |------------|-------------------|--------------|--------------|--------------|
# | 0          | {'Key.ctrl', 'm'} | echo Pass    | 1/1/1970     | Pass         |
# | 1          | {'Key.cmd', ';'}  | echo Pass1   | 1/1/2000     | Pass1        |
# |------------|-------------------|--------------|--------------|--------------|

def csvParser(filename):
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
            parsedData.append(parsedRow)

    return parsedData

def csvWriter(filename, parsedData):
    largestID = 0
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row == []:
                continue
            largestID = int(row[0])
    with open(filename, 'a') as f:
        writer = csv.writer(f)
        writer.writerow([largestID+1, parsedData[0], parsedData[1], parsedData[2], parsedData[3]])

        '''
        
        Note that the above code assumes that there is a newline created at the end of the file. Please check the file.
        
        Lucky me, it works.

        '''

def csvShortcutDeleter(filename, id, parsedData):
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


def keystrokeParser(parsedData):
    keystrokes = []
    for shortcut in parsedData:
        keystrokes.append(shortcut[0])
    return keystrokes

def commandRunner(id, parsedData):
    os.system(parsedData[id][1])

keystrokes = keystrokeParser(csvParser("keylogger.csv"))
keyLogger = KeyLogger(keystrokes)

# Start the listener
def keyboardListener():
    with keyboard.Listener(on_press=onPress, on_release=onRelease) as listener:
        listener.join()

thread = threading.Thread(target=keyboardListener)
thread.start()

def tkinterEditingMode(name, command):
    pass

def editingMode():
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
        csvWriter("keylogger.csv", shortcutData)
        print("The shortcut has been saved. Please restart the program for the changes to take effect.")
    else:
        id = int(input("Enter shortcut ID to delete: "))
        csvShortcutDeleter("keylogger.csv", id, csvParser("keylogger.csv"))

while True:
    editingMode() if "y"==input("Edit shortcuts? (y/n): ") else False

