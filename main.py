from gui import *
import time

def exitOM():
    app.exec_()
    print('Shutting Down... No hard feelings')
    return

if __name__ == '__main__':
    print('+-------------------- ',date.today().isoformat(),time.strftime("%I:%M"),' --------------------+')
    print('This is Order Manager '+versionNumber)
    print('All debugging messages will appear here')
    print('Logs are not built in yet and are planned for later versions')
    print()
    for item in sqlConfig:
        if item == '':
            print('[ERROR]: Incomplete config file')
            exit()
    for item in wcAPIConfig:
        if item == '':
            print('[ERROR]: Incomplete config file')
            exit()
    for item in wcAPILegacyConfig:
        if item == '':
            print('[ERROR]: Incomplete config file')
            exit()
    for item in emailConfig:
        if item == '':
            print('[ERROR]: Incomplete config file')
            exit()
    for item in staffMembers:
        if item == '':
            print('[ERROR]: Incomplete config file')
            exit()
    for item in suppliers:
        if item == '':
            print('[ERROR]: Incomplete config file')
            exit()
    app = QApplication(sys.argv)
    ex = mainWindow()
    sys.exit(exitOM())
    