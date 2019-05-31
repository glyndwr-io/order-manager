from gui import *
import time

def exitOM():
    app.exec_()
    print('Shutting Down... No hard feelings')
    return

def noConfig():
    print('[ERROR]: Incomplete config file')
    ex = QMessageBox()
    ex.setText("ERROR: Your config file is incomplete! Please refer to the README for Setup and Troubleshooting.")
    ex.setWindowTitle("Incomplete Config")
    ex.setIcon(QMessageBox().Critical)
    ex.exec()
    exit()

if __name__ == '__main__':
    print('+-------------------- ',date.today().isoformat(),time.strftime("%I:%M"),' --------------------+')
    print('This is Order Manager '+versionNumber)
    print('All debugging messages will appear here')
    print('Logs are not built in yet and are planned for later versions')
    print()
    app = QApplication(sys.argv)
    for item in sqlConfig:
        if item == '':
            noConfig()
    for item in wcAPIConfig:
        if item == '':
            noConfig()
    for item in wcAPILegacyConfig:
        if item == '':
            noConfig()
    for item in emailConfig:
        if item == '':
            noConfig()
    for item in staffMembers:
        if item == '':
            noConfig()
    for item in suppliers:
        if item == '':
            noConfig()
    ex = mainWindow()
    sys.exit(exitOM())
    
