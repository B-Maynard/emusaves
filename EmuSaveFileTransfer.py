import os
import json
import shutil
import time

#create folder whereever the program is being executed
dataFilePath = 'emusavestransfer/emusavetransferdata.json'

def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')

def printHeader():
    print(" _______                _                        _______ _ _          _______                        ___    ")        
    print("(_______)              | |                      (_______|_) |        (_______)                      / __)       ")    
    print(" _____   ____  _   _    \ \   ____ _   _ ____    _____   _| | ____    _        ____ ____ ____   ___| |__ ____  ____ ")
    print("|  ___) |    \| | | |    \ \ / _  | | | / _  )  |  ___) | | |/ _  )  | |      / ___) _  |  _ \ /___)  __) _  )/ ___)")
    print("| |_____| | | | |_| |_____) | ( | |\ V ( (/ /   | |     | | ( (/ /   | |_____| |  ( ( | | | | |___ | | ( (/ /| |    ")
    print("|_______)_|_|_|\____(______/ \_||_| \_/ \____)  |_|     |_|_|\____)   \______)_|   \_||_|_| |_(___/|_|  \____)_|    ")
    print("                                                                                                                    ")
    print("                                                                                                                                                                                                                   ")

def transferSaves():
    validInitSelection = True

    with open(dataFilePath, 'r+') as f:
        dataFile = json.load(f)
        num = 1
        stringBuilder = ""

        for i in dataFile['emulators']:
            stringBuilder += str(num) + ". " + i['name'] + "\n"
            num += 1

        validEmuSelection = False
        validTransferSelection = False

        while not validEmuSelection:    
            emuSelection = input("Please select which emulator you'd like to transfer saves (select number): " + "\n" + stringBuilder + ": ")
            if int(emuSelection) > num or int(emuSelection) < 0:
                print("Invalid selection.")
                time.sleep(1)
                clearScreen()
                printHeader()
            else:
                validEmuSelection = True

        while not validTransferSelection:
            print("**NOTE** This will OVERWRITE save data you have in the destination folder. Please make sure you're transferring the LATEST data to the destination file.")
            print("Please select how you'd like to transfer files (select number):")
            print("1. Cloud to local")
            print("2. Local to cloud")
            transferSelection = input(": ")
            if transferSelection == '1':
                validTransferSelection = True
                sourceLocation = dataFile['emulators'][int(emuSelection) - 1]['cloudLocation']
                destLocation = dataFile['emulators'][int(emuSelection) - 1]['saveLocation']
            elif transferSelection == '2':
                validTransferSelection = True
                destLocation = dataFile['emulators'][int(emuSelection) - 1]['cloudLocation']
                sourceLocation = dataFile['emulators'][int(emuSelection) - 1]['saveLocation']
            else:
                print("Invalid selection.")
                time.sleep(1)
                clearScreen()
                printHeader()

        emuName = dataFile['emulators'][int(emuSelection) - 1]['name']

        try:
            shutil.copytree(sourceLocation, destLocation, dirs_exist_ok=True)
            print("Transfer of files successful!")
            time.sleep(1)
            print("Exiting program...")
            time.sleep(1)
        except Exception as e:
            print("Something went wrong when trying to copy files. If this continues, reach out to me on reddit (/u/Bk4180). Exception results:")
            print(e)
            input("(Press any button to continue...)")

def addEmulatorConfig():
    emuName = input("Please supply the name of the Emulator this config is for: ")
    saveLocation = input("Please supply the filepath to the savefile local directory: ")
    cloudLocation = input("Please supply the filepath to the cloud directory: ")

    if not os.path.exists(dataFilePath) or os.stat(dataFilePath).st_size == 0:
        with open(dataFilePath, 'a+') as f:
            data = {}
            data['emulators'] = [{}]
            data['emulators'][0]['name'] = emuName
            data['emulators'][0]['saveLocation'] = saveLocation
            data['emulators'][0]['cloudLocation'] = cloudLocation

            json.dump(data, f)
    else:
        with open(dataFilePath, 'r+') as f:
            dataFile = json.load(f)
            data = {}
            data['name'] = emuName
            data['saveLocation'] = saveLocation
            data['cloudLocation'] = cloudLocation
            dataFile['emulators'].append(data)

            f.seek(0)
            json.dump(dataFile, f)

def editEmulatorConfig():
    with open(dataFilePath, 'r+') as f:
        dataFile = json.load(f)
        
    num = 1
    stringBuilder = ""

    for i in dataFile['emulators']:
        stringBuilder += str(num) + ". " + i['name'] + "\n"
        num += 1

    validEmuSelection = False

    while not validEmuSelection:    
        emuSelection = input("Please select which emulator you'd like to edit (select number): " + "\n" + stringBuilder + ": ")
        if int(emuSelection) > num or int(emuSelection) < 0:
            print("Invalid selection.")
            time.sleep(1)
            clearScreen()
            printHeader()
        else:
            validEmuSelection = True

    exitProgram = False
    while not exitProgram:
        print("Please select which item you wish to edit for " + dataFile['emulators'][int(emuSelection) - 1]['name'] + ": ")
        print("1. Name")
        print("2. Local savefile directory")
        print("3. Cloud directory")
        print("4. Exit")
        progSelection = input(": ")

        if progSelection == '1':
            newName = input("Enter the new name you'd like to associate with this configuration: ")
            dataFile['emulators'][int(emuSelection) - 1]['name'] = newName
            with open(dataFilePath, 'w+') as f:
                json.dump(dataFile, f)

            print("Config file successfully updated!")
            time.sleep(1)

            clearScreen()
            printHeader()
        elif progSelection == '2':
            newLocalDirectory = input("Enter the new local savefile directory you'd like to associate with this configuration: ")
            dataFile['emulators'][int(emuSelection) - 1]['saveLocation'] = newLocalDirectory
            with open(dataFilePath, 'w+') as f:
                json.dump(dataFile, f)

            print("Config file successfully updated!")
            time.sleep(1)

            clearScreen()
            printHeader()
        elif progSelection == '3':
            newCloudDirectory = input("Enter the new cloud directory you'd like to associate with this configuration: ")
            dataFile['emulators'][int(emuSelection) - 1]['cloudLocation'] = newCloudDirectory
            with open(dataFilePath, 'w+') as f:
                json.dump(dataFile, f)

            print("Config file successfully updated!")
            time.sleep(1)

            clearScreen()
            printHeader()
        elif progSelection == '4':
            exitProgram = True
        else:
            print("Invalid selection.")
            clearScreen()
            printHeader()   

    

if __name__ == '__main__':
    clearScreen()
    printHeader()

    print("Checking files...")
    os.makedirs(os.path.dirname(dataFilePath), exist_ok=True)

    if not os.path.exists(dataFilePath):
        print("File not found, creating data file...")
        addEmulatorConfig()
    else:
        print("File found! Parsing data...")

    # if its an empty file/doesn't exist, we either need to create it or the content was removed
    if not os.path.exists(dataFilePath) or os.stat(dataFilePath).st_size == 0:
        with open(dataFilePath, 'a+') as f:
            
            print("Data file is empty, adding new entry...\n")

    else:
        endProgram = False
        while not endProgram:
            print("Please select option from list below:")
            print("1. Transfer saves")
            print("2. Add new emulator configuration")
            print("3. Edit emulator configuration")
            print("4. Exit")
            initSelection = input(": ")

            if initSelection == '1':
                transferSaves()
                clearScreen()
                printHeader()
            elif initSelection == '2':
                addEmulatorConfig()
                clearScreen()
                printHeader()
            elif initSelection == '3':
                editEmulatorConfig()
                clearScreen()
                printHeader()
            elif initSelection == '4':
                endProgram = True
            else:
                print("Invalid selection.")
                time.sleep(1)
                clearScreen()
                printHeader()