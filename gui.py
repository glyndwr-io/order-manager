import sys
from time import sleep
from pprint import *
from woocommerce import *
from sql import *
from sendemail import *

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont, QStandardItemModel, QStandardItem, QColor, QBrush, QStaticText
from PyQt5.QtCore import (QDate, QDateTime, QRegExp, QSortFilterProxyModel, Qt, QTime)

from sql import *

class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
    #Setting up the menu bar
        menubar=self.menuBar()
        self.statusBar = QStatusBar()
        self.theWindowArea = mainWindowArea(self)
        self.buttonBox = QDialogButtonBox()
        self.groupBox = QWidget()
        self.inner = QVBoxLayout()
        
    #File Menu Operations
        #Object Declarations
        fileMenu = menubar.addMenu('File')
        newMenu = QMenu('New', self)
        newSpecOrd = QAction('Special Order', self)
        newWarClaim = QAction('Warranty Claims', self)
        newOnOrd = QAction('Payment Request', self)
        newProdInfoReq = QAction('Product Info Request', self)
        refresh = QAction('Refresh', self)
        exit = QAction('Exit', self)

        #Trigger Action Assignments
        exit.triggered.connect(self.close)
        refresh.triggered.connect(self.reloadOrders)
        
        #Add objects to menus
        newMenu.addAction(newSpecOrd)
        newMenu.addAction(newWarClaim)
        newMenu.addAction(newOnOrd)
        newMenu.addAction(newProdInfoReq)
        newSpecOrd.triggered.connect(self.theWindowArea.createSpecialOrder)
        newWarClaim.triggered.connect(self.theWindowArea.createWarrantyClaim)
        newOnOrd.triggered.connect(self.theWindowArea.createOnlineOrder)
        newProdInfoReq.triggered.connect(self.theWindowArea.createInfoRequest)
        fileMenu.addMenu(newMenu)
        fileMenu.addAction(refresh)
        fileMenu.addAction(exit)
    
    #Edit Menu Operations
        #Object Declarations
        editMenu = menubar.addMenu('Edit')
        editSelected = QAction('Selected Order...', self)
        editPrefrences = QAction('Prefrences', self)
        editSettings = QAction('Settings', self)
        
        #Add objects to menus
        editMenu.addAction(editSelected)
        editMenu.addAction(editPrefrences)
        editMenu.addAction(editSettings)

        #Trigger Action Assignments
        editSelected.triggered.connect(self.theWindowArea.editSpecialOrder)
        editPrefrences.triggered.connect(self.prefrencesWindow)
        editSettings.triggered.connect(self.settingsWindow)

    #Help Menu Operations
        #Object Declarations
        helpMenu = menubar.addMenu('Help')
        helpAbout = QAction('About', self)

        #Trigger Action Assignments
        helpAbout.triggered.connect(self.aboutDialog)

        #Add objects to menus
        helpMenu.addAction(helpAbout)

    #Draw the window
        create = self.buttonBox.addButton(QDialogButtonBox.Ok)
        edit = self.buttonBox.addButton(QDialogButtonBox.Cancel)
        delete = self.buttonBox.addButton(QDialogButtonBox.Ok)

        create.setText('Create')
        edit.setText('Edit')
        delete.setText('Delete')

        create.clicked.connect(self.theWindowArea.createByContext)
        edit.clicked.connect(self.theWindowArea.editByContext)
        delete.clicked.connect(self.theWindowArea.deleteByContext)

        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('Order Manager '+versionNumber)
        self.setWindowIcon(QIcon('web.png'))
        self.inner.addWidget(self.theWindowArea)
        self.inner.addWidget(self.buttonBox)
        self.groupBox.setLayout(self.inner)
        self.setCentralWidget(self.groupBox)
        #self.setStatusBar(self.statusBar)

        self.statusBar.showMessage('Status: Online')
        
        self.show()
        self.w = None  

    def reloadOrders(self):
        print('Refreshing Orders')
        self.theWindowArea.tableWidgetSO.clear()
        self.theWindowArea.tableWidgetWC.clear()
        self.statusBar.showMessage('Status: Loading Orders')
        self.theWindowArea.addOrdersLoop()
        self.theWindowArea.addClaimsLoop()
        self.statusBar.showMessage('Status: Online') 
        print('Orders Refreshed')
        return

    def aboutDialog(self):
        about = QMessageBox.about(self, 'About', "ORDER MANAGER "+versionNumber+
            "\nDeveloped by Glyndwr Morris"
            "\n"
            "\nOrder Manager relies on these technologies:"
            "\n-Python 3"
            "\n-Qt 5"
            "\n-MySQL"
            "\n"
            "\n(C) Glyndwr Morris 2017 All rights reserved")

    def prefrencesWindow(self):
        about = QMessageBox.about(self, 'Prefrences', "Coming Soon! :)")
        return

    def settingsWindow(self):
        self.w=newOrderWindow()
        
        self.user = QLineEdit()
        self.user.setText(sqlConfig['user'])
        self.pword = QLineEdit()
        self.pword.setText(sqlConfig['password'])
        self.pword.setEchoMode(QLineEdit.Password)
        self.host = QLineEdit()
        self.host.setText(sqlConfig['host'])
        self.dataBase = QLineEdit()
        self.dataBase.setText(sqlConfig['database'])

        url = QLineEdit()
        url.setText(wcAPIConfig['url'])
        consumerKey = QLineEdit()
        consumerKey.setText(wcAPIConfig['consumer_key'])
        consumerSecret = QLineEdit()
        consumerSecret.setEchoMode(QLineEdit.Password)
        consumerSecret.setText(wcAPIConfig['consumer_secret'])
        version = QLineEdit()
        version.setText(wcAPIConfig['version'])

        self.title1 = QLabel('Database Connection Settings:')
        self.title2 = QLabel('WooCommerce Connection Settings:')
        
        self.wLayout = QFormLayout()
        self.wLayout.addRow(self.title1)
        self.wLayout.addRow('Username:', self.user)
        self.wLayout.addRow('Password:', self.pword)
        self.wLayout.addRow('Host:', self.host)
        self.wLayout.addRow('Database:', self.dataBase)
        self.wLayout.addRow(self.title2)
        self.wLayout.addRow('WooCommerce URL', url)
        self.wLayout.addRow('Consumer Key', consumerKey)
        self.wLayout.addRow('Consumer Secret', consumerSecret)
        self.wLayout.addRow('API Version', version)

        self.w.setGeometry(500, 400, 400, 300)
        self.w.setWindowTitle('Settings')
        self.w.setLayout(self.wLayout)

        self.w.show()
        return

    def editWarrantyClaim(self):
        self.w = newOrderWindow()
        self.w.setGeometry(500, 400, 400, 400)
        self.w.setWindowTitle('Edit Warranty Claim')
        self.w.show()
        return

    def editOnlineOrder(self):
        self.w = newOrderWindow()
        self.w.setGeometry(500, 400, 400, 400)
        self.w.setWindowTitle('Edit Online Order')
        self.w.show()
        return

    def editSpecialOrder(self):
        self.w = newOrderWindow()
        self.w.setGeometry(500, 400, 400, 400)
        self.w.setWindowTitle('Edit Special Order')
        self.w.show()
        return

class mainWindowArea(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

    # Initialize tab screen
        self.orderStatus = ['Requested','Order Placed','Order Recieved',
        'Backordered','Not Available', 'Info Requested', 'Insuffecient Information']
        self.search = QLineEdit()
        self.filterOrderStatus = QComboBox()
        self.filterOrderStatusLabel = QLabel('Filter by Order Status:')
        self.filterOrderStatus.setMaximumWidth(140)
        self.filterOrderStatusLabel.setMaximumWidth(108)
        self.search.setPlaceholderText('[Press Enter to Search] First and Last name, '
            'Phone Number, Email, Product, Part Number, or Order Notes.')
        self.search.returnPressed.connect(self.searchOrders)
        self.search.setDisabled(False)
        self.searchArea=QFormLayout()
        self.searchAreaFilters=QHBoxLayout()
        self.searchAreaFilters.addWidget(self.filterOrderStatusLabel)
        self.searchAreaFilters.addWidget(self.filterOrderStatus)
        self.searchArea.addRow(self.searchAreaFilters)
        self.searchArea.addRow('Search:', self.search)
        self.filterOrderStatus.addItem('')
        self.filterOrderStatus.addItems(self.orderStatus)
        self.filterOrderStatus.currentIndexChanged.connect(self.filterOrders)
        self.tabs = QTabWidget()
        self.tab1 = QWidget()   
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tabs.resize(300,200) 
        self.tabs.addTab(self.tab3,"Special Orders")
        self.tabs.addTab(self.tab1,"Online Orders")
        self.tabs.addTab(self.tab2,"Warranty Claims")
         
    # Build Online Order Tab.
        #Widget declaration
        self.tab1.layout = QVBoxLayout(self)
        self.tab1Splitter = QSplitter()
        self.tableWidgetOO = QTreeWidget()
        self.tableWidgetOO2 = QTreeWidget()
        self.headerListOO = ['First Name',
        'Last Name','Phone Number','Email','Product Name','Quantity', 
        'Price','UPC','Date Requested','Date Ordered','Order Number',
        'Order Status','Price','Payment Status',
        'Order Type','Sales Rep']
        self.tableWidgetOO.setHeaderLabels(self.headerListOO)
        self.tableWidgetOO2.setHeaderLabels(self.headerListOO)
        self.tableWidgetOO.setSortingEnabled(True)
        self.tableWidgetOO2.setSortingEnabled(True)

        self.addOnlineLoop()

        self.tab1Splitter.addWidget(self.tableWidgetOO)
        self.tab1Splitter.addWidget(self.tableWidgetOO2)
        self.tab1Splitter.setOrientation(Qt.Vertical)
        self.tab1Splitter.setCollapsible(0,False)
        self.tab1Splitter.setCollapsible(1,False)
        self.tab1Splitter.setSizes([400,400])
        self.tab1.layout.addWidget(self.tab1Splitter)
        self.tab1.setLayout(self.tab1.layout)

    # Build Warranty Claim Tab.
        self.tab2.layout = QVBoxLayout(self)
        self.tab2Splitter = QSplitter()
        self.tableWidgetWC = QTreeWidget()
        self.headerListWC = ['First Name',
        'Last Name','Phone Number','Email','Product Name','Part Number',
        'Supplier','Date Requested','Date Ordered','Order Number',
        'Order Status','Price','Payment Status',
        'Order Type','Sales Rep']
        self.tableWidgetWC.setHeaderLabels(self.headerListWC)
        self.tableWidgetWC.setSortingEnabled(True)

        self.addClaimsLoop()       

        self.tableWidgetWC.itemDoubleClicked.connect(self.editWarrantyClaim)
        
        #self.deleteSOButton.clicked.connect(self.delete)
        #self.addSOButton.clicked.connect(self.createSpecialOrder)
        #self.editSOButton.clicked.connect(self.editSpecialOrder)
        
        #Widget Organization
        self.tab2Splitter.addWidget(self.tableWidgetWC)
        self.notesSectionWC = QTextEdit()
        self.notesSectionWC.setReadOnly(True)
        
        self.tab2Splitter.addWidget(self.notesSectionWC)
        self.tab2Splitter.setOrientation(Qt.Vertical)
        self.tab2Splitter.setCollapsible(0,False)
        self.tab2Splitter.setCollapsible(1,False)
        self.tab2Splitter.setSizes([400,20])
        self.tab2.layout.addWidget(self.tab2Splitter)
        self.tab2.setLayout(self.tab2.layout)

        print('Reading claim entrys from database')
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        #self.tableWidgetSO.itemClicked.connect(self.setNotesSection)

    # Build Special Order Tab.
        self.tab3.layout = QVBoxLayout(self)
        self.tab3Splitter = QSplitter()
        self.addSOButton = QPushButton("Create")
        self.editSOButton = QPushButton("Edit")
        self.deleteSOButton = QPushButton("Delete")
        self.tableWidgetSO = QTreeWidget()
        self.headerListSO = ['First Name',
        'Last Name','Phone Number','Email','Product Name','Part Number',
        'Supplier','Date Requested','Date Ordered','Order Number',
        'Order Status','Price','Payment Status',
        'Order Type','Sales Rep']
        self.tableWidgetSO.setHeaderLabels(self.headerListSO)
        self.tableWidgetSO.setSortingEnabled(True)

        self.addOrdersLoop()       

        self.tableWidgetSO.itemDoubleClicked.connect(self.editSpecialOrder)
        
        self.deleteSOButton.clicked.connect(self.delete)
        self.addSOButton.clicked.connect(self.createSpecialOrder)
        self.editSOButton.clicked.connect(self.editSpecialOrder)
        
        #Widget Organization
        self.tab3Splitter.addWidget(self.tableWidgetSO)
        self.notesSectionSO = QTextEdit()
        self.notesSectionSO.setReadOnly(True)
        
        self.tab3Splitter.addWidget(self.notesSectionSO)
        self.tab3Splitter.setOrientation(Qt.Vertical)
        self.tab3Splitter.setCollapsible(0,False)
        self.tab3Splitter.setCollapsible(1,False)
        self.tab3Splitter.setSizes([400,20])
        self.tab3.layout.addWidget(self.tab3Splitter)
        self.tab3.setLayout(self.tab3.layout)

    # Finish up everything and present.
        print('Reading order entrys from database')
        self.layout.addLayout(self.searchArea)
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        self.tableWidgetSO.itemClicked.connect(self.setNotesSection)
        
        
# Order Realted Functions
    def addOrdersLoop(self):
        self.orderList = []
        self.objectIDs = {}
        matrixOrders = {}
        matrixParents = {}
        self.paymentStatus = ['Pending Payment','Partially Paid','Fully Paid']
        self.orderStatus = ['Requested','Order Placed','Order Recieved',
        'Backordered','Not Available', 'Info Requested', 'Insuffecient Information']

        specialOrders = fetchOrders() #fetchOrders[x][9] is the Layaway Number
        importantFont = QFont()

        for stuff in specialOrders:
            if stuff[9] in matrixOrders:
                matrixOrders[stuff[9]].append(stuff[15])
            else:
                matrixOrders[stuff[9]] = [stuff[15]]
        
        for obj in matrixOrders:
            if len(matrixOrders[obj]) > 1:
                matrixParents[obj] = QTreeWidgetItem()
                self.tableWidgetSO.addTopLevelItem(matrixParents[obj])
                matrixParents[obj].setText(4, 'Multi-part Order')
                for i in range(15):
                    matrixParents[obj].setBackground(i,QColor(255, 255, 150))

        j=0
        for item in specialOrders:
            if self.orderStatus[item[10]] == 'Requested' or self.orderStatus[item[10]] == 'Info Requested':
                importantFont.setBold(True)
            else:
                importantFont.setBold(False)
            
            if len(matrixOrders[item[9]]) > 1:
                
                #Scan array to see if there are any entries for this is objectIDs

                #if there isnt, we need to make a new QTreeWidgetItem and add an
                #an order as a child

                #if there is, we add the order as a child to the existing QTreeWidgetItem

                self.orderList.append(QTreeWidgetItem())
                matrixParents[item[9]].addChild(self.orderList[len(self.orderList)-1])
                matrixParents[item[9]].setText(0, str(item[0]))
                matrixParents[item[9]].setFont(0, importantFont)
                matrixParents[item[9]].setText(1, str(item[1]))
                matrixParents[item[9]].setFont(1, importantFont)
                matrixParents[item[9]].setText(2, self.parsePhoneNumber(str(item[2])))
                matrixParents[item[9]].setFont(2, importantFont)
                matrixParents[item[9]].setText(3, str(item[3]))
                matrixParents[item[9]].setFont(3, importantFont)
                matrixParents[item[9]].setFont(4, importantFont)
                matrixParents[item[9]].setText(9, str(item[9]))
                matrixParents[item[9]].setFont(9, importantFont)
                if item[13] == 1:
                    matrixParents[item[9]].setText(13, "Workorder")
                    matrixParents[item[9]].setForeground(13,QColor("Blue"))
                    matrixParents[item[9]].setFont(13, importantFont)
                else:
                    matrixParents[item[9]].setText(13, "Layaway")
                    matrixParents[item[9]].setForeground(13,QColor("Green"))
                    matrixParents[item[9]].setFont(13, importantFont)

                self.objectIDs[j] = item[15]
                #First Name Column
                self.orderList[j].setText(0, str(item[0]))
                self.orderList[j].setFont(0, importantFont)
                #Last Name Column
                self.orderList[j].setText(1, str(item[1]))
                self.orderList[j].setBackground(1,QColor("lightGray"))
                self.orderList[j].setFont(1, importantFont)
                #Phone Column
                self.orderList[j].setText(2, self.parsePhoneNumber(str(item[2])))
                self.orderList[j].setFont(2, importantFont)
                #Email Column
                self.orderList[j].setText(3, str(item[3]))
                self.orderList[j].setBackground(3,QColor("lightGray"))
                self.orderList[j].setFont(3, importantFont)
                #Things
                self.orderList[j].setText(4, str(item[4]))
                self.orderList[j].setFont(4, importantFont)
                #Things
                self.orderList[j].setText(5, str(item[5]))
                self.orderList[j].setBackground(5,QColor("lightGray"))
                self.orderList[j].setFont(5, importantFont)
                #Things
                self.orderList[j].setText(6, str(item[6]))
                self.orderList[j].setFont(6, importantFont)
                #Things
                self.orderList[j].setText(7, str(item[7]))
                self.orderList[j].setBackground(7,QColor("lightGray"))
                self.orderList[j].setFont(7, importantFont)
                #Date Ordered
                if self.orderStatus[item[10]] == 'Requested':
                    self.orderList[j].setText(8, '')
                elif item[8] == None:
                    self.orderList[j].setText(8, '')
                else:
                    self.orderList[j].setText(8, str(item[8]))
                self.orderList[j].setFont(8, importantFont)
                #Things
                self.orderList[j].setText(9, str(item[9]))
                self.orderList[j].setBackground(9,QColor("lightGray"))
                self.orderList[j].setFont(9, importantFont)
                #Order Status Column
                self.orderList[j].setText(10, self.orderStatus[item[10]])
                self.orderList[j].setFont(10, importantFont)
                #Order Status Column
                self.orderList[j].setText(11, str(round(item[16], 3)))
                self.orderList[j].setBackground(11,QColor("lightGray"))
                self.orderList[j].setFont(11, importantFont)
                #Payment Status Colum
                self.orderList[j].setText(12, self.paymentStatus[item[12]])
                self.orderList[j].setFont(12, importantFont)
                #Order Type Column
                if item[13] == 1:
                    self.orderList[j].setText(13, "Workorder")
                    self.orderList[j].setForeground(13,QColor("Blue"))
                    self.orderList[j].setBackground(13,QColor("lightGray"))
                else:
                    self.orderList[j].setText(13, "Layaway")
                    self.orderList[j].setForeground(13,QColor("Green"))
                    self.orderList[j].setBackground(13,QColor("lightGray"))
                self.orderList[j].setFont(13, importantFont)
                #Things
                self.orderList[j].setText(14, str(item[14]))
                self.orderList[j].setFont(14, importantFont)
                
                self.tableWidgetSO.addTopLevelItem(self.orderList[j])
            
            else:
                self.orderList.append(QTreeWidgetItem())
                self.objectIDs[j] = item[15]
                #First Name Column
                self.orderList[j].setText(0, str(item[0]))
                self.orderList[j].setFont(0, importantFont)
                #Last Name Column
                self.orderList[j].setText(1, str(item[1]))
                self.orderList[j].setBackground(1,QColor("lightGray"))
                self.orderList[j].setFont(1, importantFont)
                #Phone Column
                self.orderList[j].setText(2, self.parsePhoneNumber(str(item[2])))
                self.orderList[j].setFont(2, importantFont)
                #Email Column
                self.orderList[j].setText(3, str(item[3]))
                self.orderList[j].setBackground(3,QColor("lightGray"))
                self.orderList[j].setFont(3, importantFont)
                #Things
                self.orderList[j].setText(4, str(item[4]))
                self.orderList[j].setFont(4, importantFont)
                #Things
                self.orderList[j].setText(5, str(item[5]))
                self.orderList[j].setBackground(5,QColor("lightGray"))
                self.orderList[j].setFont(5, importantFont)
                #Things
                self.orderList[j].setText(6, str(item[6]))
                self.orderList[j].setFont(6, importantFont)
                #Things
                self.orderList[j].setText(7, str(item[7]))
                self.orderList[j].setBackground(7,QColor("lightGray"))
                self.orderList[j].setFont(7, importantFont)
                #Date Ordered
                if self.orderStatus[item[10]] == 'Requested':
                    self.orderList[j].setText(8, '')
                elif item[8] == None:
                    self.orderList[j].setText(8, '')
                else:
                    self.orderList[j].setText(8, str(item[8]))
                self.orderList[j].setFont(8, importantFont)
                #Things
                self.orderList[j].setText(9, str(item[9]))
                self.orderList[j].setBackground(9,QColor("lightGray"))
                self.orderList[j].setFont(9, importantFont)
                #Order Status Column
                self.orderList[j].setText(10, self.orderStatus[item[10]])
                self.orderList[j].setFont(10, importantFont)
                #Order Status Column
                self.orderList[j].setText(11, str(round(item[16], 3)))
                self.orderList[j].setBackground(11,QColor("lightGray"))
                self.orderList[j].setFont(11, importantFont)
                #Payment Status Colum
                self.orderList[j].setText(12, self.paymentStatus[item[12]])
                self.orderList[j].setFont(12, importantFont)
                #Order Type Column
                if item[13] == 1:
                    self.orderList[j].setText(13, "Workorder")
                    self.orderList[j].setForeground(13,QColor("Blue"))
                    self.orderList[j].setBackground(13,QColor("lightGray"))
                else:
                    self.orderList[j].setText(13, "Layaway")
                    self.orderList[j].setForeground(13,QColor("Green"))
                    self.orderList[j].setBackground(13,QColor("lightGray"))
                self.orderList[j].setFont(13, importantFont)
                #Things
                self.orderList[j].setText(14, str(item[14]))
                self.orderList[j].setFont(14, importantFont)
                
                self.tableWidgetSO.addTopLevelItem(self.orderList[j])
            
            j+=1
        #print(self.objectIDs)
        for i in range(len(self.headerListSO)):
                self.tableWidgetSO.resizeColumnToContents(i)

    def searchedOrdersLoop(self):
        self.orderList = []
        self.objectIDs = {}
        matrixOrders = {}
        matrixParents = {}
        self.orderStatus = ['Requested','Order Placed','Order Recieved',
        'Backordered','Not Available', 'Info Requested', 'Insuffecient Information']
        self.paymentStatus = ['Pending Payment','Partially Paid','Fully Paid']

        specialOrders = findOrder(self.search.text())
        importantFont = QFont()

        for stuff in specialOrders:
            if stuff['orderID'] in matrixOrders:
                matrixOrders[stuff['orderID']].append(stuff['orderID'])
            else:
                matrixOrders[stuff['orderID']] = [stuff['objectID']]
        
        for obj in matrixOrders:
            if len(matrixOrders[obj]) > 1:
                matrixParents[obj] = QTreeWidgetItem()
                self.tableWidgetSO.addTopLevelItem(matrixParents[obj])
                matrixParents[obj].setText(4, 'Multi-part Order')
                for i in range(15):
                    matrixParents[obj].setBackground(i,QColor(255, 255, 150))

        j=0
        for item in specialOrders:
            if self.orderStatus[item['orderStatus']] == 'Requested' or \
            self.orderStatus[item['orderStatus']] == 'Info Requested':
                importantFont.setBold(True)
            else:
                importantFont.setBold(False)
            
            if len(matrixOrders[item['orderID']]) > 1:
                
                #Scan array to see if there are any entries for this is objectIDs

                #if there isnt, we need to make a new QTreeWidgetItem and add an
                #an order as a child

                #if there is, we add the order as a child to the existing QTreeWidgetItem

                self.orderList.append(QTreeWidgetItem())
                matrixParents[item['orderID']].addChild(self.orderList[len(self.orderList)-1])
                matrixParents[item['orderID']].setText(0, str(item['customerFirstName']))
                matrixParents[item['orderID']].setFont(0, importantFont)
                matrixParents[item['orderID']].setText(1, str(item['customerLastName']))
                matrixParents[item['orderID']].setFont(1, importantFont)
                matrixParents[item['orderID']].setText(2, self.parsePhoneNumber(str(item['customerPhoneNo'])))
                matrixParents[item['orderID']].setFont(2, importantFont)
                matrixParents[item['orderID']].setText(3, str(item['customerEmail']))
                matrixParents[item['orderID']].setFont(3, importantFont)
                matrixParents[item['orderID']].setFont(4, importantFont)
                matrixParents[item['orderID']].setText(9, str(item['orderID']))
                matrixParents[item['orderID']].setFont(9, importantFont)
                if item['isWorkOrder'] == 1:
                    matrixParents[item['orderID']].setText(13, "Workorder")
                    matrixParents[item['orderID']].setForeground(13,QColor("Blue"))
                    matrixParents[item['orderID']].setFont(13, importantFont)
                else:
                    matrixParents[item['orderID']].setText(13, "Layaway")
                    matrixParents[item['orderID']].setForeground(13,QColor("Green"))
                    matrixParents[item['orderID']].setFont(13, importantFont)

                self.objectIDs[j] = item['objectID']
                #First Name Column
                self.orderList[j].setText(0, str(item['customerFirstName']))
                self.orderList[j].setFont(0, importantFont)
                #Last Name Column
                self.orderList[j].setText(1, str(item['customerLastName']))
                self.orderList[j].setBackground(1,QColor("lightGray"))
                self.orderList[j].setFont(1, importantFont)
                #Phone Column
                self.orderList[j].setText(2, self.parsePhoneNumber(str(item['customerPhoneNo'])))
                self.orderList[j].setFont(2, importantFont)
                #Email Column
                self.orderList[j].setText(3, str(item['customerEmail']))
                self.orderList[j].setBackground(3,QColor("lightGray"))
                self.orderList[j].setFont(3, importantFont)
                #Things
                self.orderList[j].setText(4, str(item['productDesc']))
                self.orderList[j].setFont(4, importantFont)
                #Things
                self.orderList[j].setText(5, str(item['productPartNo']))
                self.orderList[j].setBackground(5,QColor("lightGray"))
                self.orderList[j].setFont(5, importantFont)
                #Things
                self.orderList[j].setText(6, str(item['productSupplier']))
                self.orderList[j].setFont(6, importantFont)
                #Things
                self.orderList[j].setText(7, str(item['dateRequested']))
                self.orderList[j].setBackground(7,QColor("lightGray"))
                self.orderList[j].setFont(7, importantFont)
                #Date Ordered
                if self.orderStatus[item['orderStatus']] == 'Requested':
                    self.orderList[j].setText(8, '')
                elif item['dateOrdered'] == None:
                    self.orderList[j].setText(8, '')
                else:
                    self.orderList[j].setText(8, str(item['dateOrdered']))
                self.orderList[j].setFont(8, importantFont)
                #Things
                self.orderList[j].setText(9, str(item['orderID']))
                self.orderList[j].setBackground(9,QColor("lightGray"))
                self.orderList[j].setFont(9, importantFont)
                #Order Status Column
                self.orderList[j].setText(10, self.orderStatus[item['orderStatus']])
                self.orderList[j].setFont(10, importantFont)
                #Order Status Column
                self.orderList[j].setText(11, str(round(item['price'], 3)))
                self.orderList[j].setBackground(11,QColor("lightGray"))
                self.orderList[j].setFont(11, importantFont)
                #Payment Status Colum
                self.orderList[j].setText(12, self.paymentStatus[item['paymentStatus']])
                self.orderList[j].setFont(12, importantFont)
                #Order Type Column
                if item['isWorkOrder'] == 1:
                    self.orderList[j].setText(13, "Workorder")
                    self.orderList[j].setForeground(13,QColor("Blue"))
                    self.orderList[j].setBackground(13,QColor("lightGray"))
                else:
                    self.orderList[j].setText(13, "Layaway")
                    self.orderList[j].setForeground(13,QColor("Green"))
                    self.orderList[j].setBackground(13,QColor("lightGray"))
                self.orderList[j].setFont(13, importantFont)
                #Things
                self.orderList[j].setText(14, str(item['salesRep']))
                self.orderList[j].setFont(14, importantFont)
                
                self.tableWidgetSO.addTopLevelItem(self.orderList[j])
            
            else:
                self.orderList.append(QTreeWidgetItem())
                self.objectIDs[j] = item['objectID']
                #First Name Column
                self.orderList[j].setText(0, str(item['customerFirstName']))
                self.orderList[j].setFont(0, importantFont)
                #Last Name Column
                self.orderList[j].setText(1, str(item['customerLastName']))
                self.orderList[j].setBackground(1,QColor("lightGray"))
                self.orderList[j].setFont(1, importantFont)
                #Phone Column
                self.orderList[j].setText(2, self.parsePhoneNumber(str(item['customerPhoneNo'])))
                self.orderList[j].setFont(2, importantFont)
                #Email Column
                self.orderList[j].setText(3, str(item['customerEmail']))
                self.orderList[j].setBackground(3,QColor("lightGray"))
                self.orderList[j].setFont(3, importantFont)
                #Things
                self.orderList[j].setText(4, str(item['productDesc']))
                self.orderList[j].setFont(4, importantFont)
                #Things
                self.orderList[j].setText(5, str(item['productPartNo']))
                self.orderList[j].setBackground(5,QColor("lightGray"))
                self.orderList[j].setFont(5, importantFont)
                #Things
                self.orderList[j].setText(6, str(item['productSupplier']))
                self.orderList[j].setFont(6, importantFont)
                #Things
                self.orderList[j].setText(7, str(item['dateRequested']))
                self.orderList[j].setBackground(7,QColor("lightGray"))
                self.orderList[j].setFont(7, importantFont)
                #Date Ordered
                if self.orderStatus[item['orderStatus']] == 'Requested':
                    self.orderList[j].setText(8, '')
                elif item['dateOrdered'] == None:
                    self.orderList[j].setText(8, '')
                else:
                    self.orderList[j].setText(8, str(item['dateOrdered']))
                self.orderList[j].setFont(8, importantFont)
                #Things
                self.orderList[j].setText(9, str(item['orderID']))
                self.orderList[j].setBackground(9,QColor("lightGray"))
                self.orderList[j].setFont(9, importantFont)
                #Order Status Column
                self.orderList[j].setText(10, self.orderStatus[item['orderStatus']])
                self.orderList[j].setFont(10, importantFont)
                #Order Status Column
                self.orderList[j].setText(11, str(round(item['price'], 3)))
                self.orderList[j].setBackground(11,QColor("lightGray"))
                self.orderList[j].setFont(11, importantFont)
                #Payment Status Colum
                self.orderList[j].setText(12, self.paymentStatus[item['paymentStatus']])
                self.orderList[j].setFont(12, importantFont)
                #Order Type Column
                if item['isWorkOrder'] == 1:
                    self.orderList[j].setText(13, "Workorder")
                    self.orderList[j].setForeground(13,QColor("Blue"))
                    self.orderList[j].setBackground(13,QColor("lightGray"))
                else:
                    self.orderList[j].setText(13, "Layaway")
                    self.orderList[j].setForeground(13,QColor("Green"))
                    self.orderList[j].setBackground(13,QColor("lightGray"))
                self.orderList[j].setFont(13, importantFont)
                #Things
                self.orderList[j].setText(14, str(item['salesRep']))
                self.orderList[j].setFont(14, importantFont)
                
                self.tableWidgetSO.addTopLevelItem(self.orderList[j])
            
            j+=1
        #print(self.objectIDs)
        for i in range(len(self.headerListSO)):
                self.tableWidgetSO.resizeColumnToContents(i)

    def filteredOrdersLoop(self):
        self.orderList = []
        self.objectIDs = {}
        matrixOrders = {}
        matrixParents = {}
        self.orderStatus = ['Requested','Order Placed','Order Recieved',
        'Backordered','Not Available', 'Info Requested', 'Insuffecient Information']
        self.paymentStatus = ['Pending Payment','Partially Paid','Fully Paid']

        specialOrders = filterOrders('orderStatus', str(self.filterOrderStatus.currentIndex()-1))
        importantFont = QFont()

        for stuff in specialOrders:
            if stuff['orderID'] in matrixOrders:
                matrixOrders[stuff['orderID']].append(stuff['orderID'])
            else:
                matrixOrders[stuff['orderID']] = [stuff['objectID']]
        
        for obj in matrixOrders:
            if len(matrixOrders[obj]) > 1:
                matrixParents[obj] = QTreeWidgetItem()
                self.tableWidgetSO.addTopLevelItem(matrixParents[obj])
                matrixParents[obj].setText(4, 'Multi-part Order')
                for i in range(15):
                    matrixParents[obj].setBackground(i,QColor(255, 255, 150))

        j=0
        for item in specialOrders:
            if self.orderStatus[item['orderStatus']] == 'Requested' or \
            self.orderStatus[item['orderStatus']] == 'Info Requested':
                importantFont.setBold(True)
            else:
                importantFont.setBold(False)
            
            if len(matrixOrders[item['orderID']]) > 1:
                
                #Scan array to see if there are any entries for this is objectIDs

                #if there isnt, we need to make a new QTreeWidgetItem and add an
                #an order as a child

                #if there is, we add the order as a child to the existing QTreeWidgetItem

                self.orderList.append(QTreeWidgetItem())
                matrixParents[item['orderID']].addChild(self.orderList[len(self.orderList)-1])
                matrixParents[item['orderID']].setText(0, str(item['customerFirstName']))
                matrixParents[item['orderID']].setFont(0, importantFont)
                matrixParents[item['orderID']].setText(1, str(item['customerLastName']))
                matrixParents[item['orderID']].setFont(1, importantFont)
                matrixParents[item['orderID']].setText(2, self.parsePhoneNumber(str(item['customerPhoneNo'])))
                matrixParents[item['orderID']].setFont(2, importantFont)
                matrixParents[item['orderID']].setText(3, str(item['customerEmail']))
                matrixParents[item['orderID']].setFont(3, importantFont)
                matrixParents[item['orderID']].setFont(4, importantFont)
                matrixParents[item['orderID']].setText(9, str(item['orderID']))
                matrixParents[item['orderID']].setFont(9, importantFont)
                if item['isWorkOrder'] == 1:
                    matrixParents[item['orderID']].setText(13, "Workorder")
                    matrixParents[item['orderID']].setForeground(13,QColor("Blue"))
                    matrixParents[item['orderID']].setFont(13, importantFont)
                else:
                    matrixParents[item['orderID']].setText(13, "Layaway")
                    matrixParents[item['orderID']].setForeground(13,QColor("Green"))
                    matrixParents[item['orderID']].setFont(13, importantFont)

                self.objectIDs[j] = item['objectID']
                #First Name Column
                self.orderList[j].setText(0, str(item['customerFirstName']))
                self.orderList[j].setFont(0, importantFont)
                #Last Name Column
                self.orderList[j].setText(1, str(item['customerLastName']))
                self.orderList[j].setBackground(1,QColor("lightGray"))
                self.orderList[j].setFont(1, importantFont)
                #Phone Column
                self.orderList[j].setText(2, self.parsePhoneNumber(str(item['customerPhoneNo'])))
                self.orderList[j].setFont(2, importantFont)
                #Email Column
                self.orderList[j].setText(3, str(item['customerEmail']))
                self.orderList[j].setBackground(3,QColor("lightGray"))
                self.orderList[j].setFont(3, importantFont)
                #Things
                self.orderList[j].setText(4, str(item['productDesc']))
                self.orderList[j].setFont(4, importantFont)
                #Things
                self.orderList[j].setText(5, str(item['productPartNo']))
                self.orderList[j].setBackground(5,QColor("lightGray"))
                self.orderList[j].setFont(5, importantFont)
                #Things
                self.orderList[j].setText(6, str(item['productSupplier']))
                self.orderList[j].setFont(6, importantFont)
                #Things
                self.orderList[j].setText(7, str(item['dateRequested']))
                self.orderList[j].setBackground(7,QColor("lightGray"))
                self.orderList[j].setFont(7, importantFont)
                #Date Ordered
                if self.orderStatus[item['orderStatus']] == 'Requested':
                    self.orderList[j].setText(8, '')
                elif item['dateOrdered'] == None:
                    self.orderList[j].setText(8, '')
                else:
                    self.orderList[j].setText(8, str(item['dateOrdered']))
                self.orderList[j].setFont(8, importantFont)
                #Things
                self.orderList[j].setText(9, str(item['orderID']))
                self.orderList[j].setBackground(9,QColor("lightGray"))
                self.orderList[j].setFont(9, importantFont)
                #Order Status Column
                self.orderList[j].setText(10, self.orderStatus[item['orderStatus']])
                self.orderList[j].setFont(10, importantFont)
                #Order Status Column
                self.orderList[j].setText(11, str(round(item['price'], 3)))
                self.orderList[j].setBackground(11,QColor("lightGray"))
                self.orderList[j].setFont(11, importantFont)
                #Payment Status Colum
                self.orderList[j].setText(12, self.paymentStatus[item['paymentStatus']])
                self.orderList[j].setFont(12, importantFont)
                #Order Type Column
                if item['isWorkOrder'] == 1:
                    self.orderList[j].setText(13, "Workorder")
                    self.orderList[j].setForeground(13,QColor("Blue"))
                    self.orderList[j].setBackground(13,QColor("lightGray"))
                else:
                    self.orderList[j].setText(13, "Layaway")
                    self.orderList[j].setForeground(13,QColor("Green"))
                    self.orderList[j].setBackground(13,QColor("lightGray"))
                self.orderList[j].setFont(13, importantFont)
                #Things
                self.orderList[j].setText(14, str(item['salesRep']))
                self.orderList[j].setFont(14, importantFont)
                
                self.tableWidgetSO.addTopLevelItem(self.orderList[j])
            
            else:
                self.orderList.append(QTreeWidgetItem())
                self.objectIDs[j] = item['objectID']
                #First Name Column
                self.orderList[j].setText(0, str(item['customerFirstName']))
                self.orderList[j].setFont(0, importantFont)
                #Last Name Column
                self.orderList[j].setText(1, str(item['customerLastName']))
                self.orderList[j].setBackground(1,QColor("lightGray"))
                self.orderList[j].setFont(1, importantFont)
                #Phone Column
                self.orderList[j].setText(2, self.parsePhoneNumber(str(item['customerPhoneNo'])))
                self.orderList[j].setFont(2, importantFont)
                #Email Column
                self.orderList[j].setText(3, str(item['customerEmail']))
                self.orderList[j].setBackground(3,QColor("lightGray"))
                self.orderList[j].setFont(3, importantFont)
                #Things
                self.orderList[j].setText(4, str(item['productDesc']))
                self.orderList[j].setFont(4, importantFont)
                #Things
                self.orderList[j].setText(5, str(item['productPartNo']))
                self.orderList[j].setBackground(5,QColor("lightGray"))
                self.orderList[j].setFont(5, importantFont)
                #Things
                self.orderList[j].setText(6, str(item['productSupplier']))
                self.orderList[j].setFont(6, importantFont)
                #Things
                self.orderList[j].setText(7, str(item['dateRequested']))
                self.orderList[j].setBackground(7,QColor("lightGray"))
                self.orderList[j].setFont(7, importantFont)
                #Date Ordered
                if self.orderStatus[item['orderStatus']] == 'Requested':
                    self.orderList[j].setText(8, '')
                elif item['dateOrdered'] == None:
                    self.orderList[j].setText(8, '')
                else:
                    self.orderList[j].setText(8, str(item['dateOrdered']))
                self.orderList[j].setFont(8, importantFont)
                #Things
                self.orderList[j].setText(9, str(item['orderID']))
                self.orderList[j].setBackground(9,QColor("lightGray"))
                self.orderList[j].setFont(9, importantFont)
                #Order Status Column
                self.orderList[j].setText(10, self.orderStatus[item['orderStatus']])
                self.orderList[j].setFont(10, importantFont)
                #Order Status Column
                self.orderList[j].setText(11, str(round(item['price'], 3)))
                self.orderList[j].setBackground(11,QColor("lightGray"))
                self.orderList[j].setFont(11, importantFont)
                #Payment Status Colum
                self.orderList[j].setText(12, self.paymentStatus[item['paymentStatus']])
                self.orderList[j].setFont(12, importantFont)
                #Order Type Column
                if item['isWorkOrder'] == 1:
                    self.orderList[j].setText(13, "Workorder")
                    self.orderList[j].setForeground(13,QColor("Blue"))
                    self.orderList[j].setBackground(13,QColor("lightGray"))
                else:
                    self.orderList[j].setText(13, "Layaway")
                    self.orderList[j].setForeground(13,QColor("Green"))
                    self.orderList[j].setBackground(13,QColor("lightGray"))
                self.orderList[j].setFont(13, importantFont)
                #Things
                self.orderList[j].setText(14, str(item['salesRep']))
                self.orderList[j].setFont(14, importantFont)
                
                self.tableWidgetSO.addTopLevelItem(self.orderList[j])
            
            j+=1
        #print(self.objectIDs)
        for i in range(len(self.headerListSO)):
                self.tableWidgetSO.resizeColumnToContents(i)

    def getSelectedOrderNumber(self):
        i = 0
        for item in self.orderList:
            if item.isSelected():
                #9 Pulls Order ID Number to pass
                return self.objectIDs[i]
            i+=1

    def delete(self):
        i=0
        for item in self.orderList:
            if item.isSelected():
                answer = QMessageBox.question(self, 'Deletion', 
                "Are you sure you want to delete this special order?")
                if answer == QMessageBox.Yes:
                    print('Deleting Order #' + str(self.objectIDs[i]))
                    deleteOrder(self.objectIDs[i])
                    item.setHidden(True)
            i+=1

    def deleteSilent(self):
        i=0
        for item in self.orderList:
            if item.isSelected():
                print('Deleting Order #' + str(self.objectIDs[i]))
                deleteOrder(self.objectIDs[i])
                item.setHidden(True)
            i+=1

    def closeBasic(self):
        self.w.close()
        self.search.setText('')

    def createSpecialOrder(self):
        self.w = newOrderWindow()
        self.selectedOrderNumber = None
        
        self.custFirstName = QLineEdit()
        self.custLastName = QLineEdit()
        self.custPhoneNumber = QLineEdit()
        self.custEmail = QLineEdit()
        self.prodDesc = QLineEdit()
        self.partNo = QLineEdit()
        self.supplier = QComboBox()
        self.partPrice = QLineEdit()
        self.orderNumber = QLineEdit()
        self.orderStatusChoice = QComboBox()
        self.orderDesc = QTextEdit()
        self.payStatus = QComboBox()
        self.orderType = QCheckBox()
        self.salesRep = QComboBox()
        self.qty = QSpinBox()
        
        self.payStatus.addItems(self.paymentStatus)
        self.salesRep.addItems(staffMembers)
        self.supplier.addItems(suppliers)
        self.qty.setMaximum(999)
        self.qty.setMinimum(1)
        
        #self.sendOrder = QPushButton("Create")
        #self.cancelCreation = QPushButton("Cancel")

        self.wButtons = QHBoxLayout()
        self.buttonBox = QDialogButtonBox()
        self.wLayout = QGridLayout()
        self.wLayoutCust = QFormLayout()
        self.wLayoutPart = QFormLayout()
        self.wLayoutNotes = QFormLayout()

        self.wLayoutCust.addRow("First Name", self.custFirstName)
        self.wLayoutCust.addRow("Last Name", self.custLastName)
        self.wLayoutCust.addRow("Phone Number", self.custPhoneNumber)
        self.wLayoutCust.addRow("E-Mail Address", self.custEmail)
        self.wLayoutCust.addRow("Order Number", self.orderNumber)
        self.wLayoutCust.addRow("Workorder?", self.orderType)
        self.wLayoutCust.addRow("Payment Status", self.payStatus)
        
        self.wLayoutPart.addRow("Product", self.prodDesc)
        self.wLayoutPart.addRow("Part Number", self.partNo)
        self.wLayoutPart.addRow("Supplier", self.supplier)
        self.wLayoutPart.addRow("Price", self.partPrice)
        self.wLayoutPart.addRow("Placed By", self.salesRep)
        self.wLayoutPart.addRow("Quantity:", self.qty)

        self.wLayoutNotes.addRow("Notes:", self.orderDesc)
        self.objectID = 0

        self.cancelCreation = self.buttonBox.addButton(QDialogButtonBox.Cancel)
        self.sendOrder = self.buttonBox.addButton(QDialogButtonBox.Ok)
        self.wButtons.addWidget(self.buttonBox)
        self.dateOrderedVar = None

        self.wLayout.addLayout(self.wLayoutCust,0,0)
        self.wLayout.addLayout(self.wLayoutPart,0,1)
        self.wLayout.addLayout(self.wLayoutNotes,1,0,1,2)
        self.wLayout.addLayout(self.wButtons,2,0,1,2)

        self.sendOrder.clicked.connect(self.commitSpecialOrder)
        self.cancelCreation.clicked.connect(self.closeBasic) 

        self.w.setGeometry(500, 400, 500, 350)
        self.w.setWindowTitle('New Special Order')
        self.w.setLayout(self.wLayout)
        self.w.show()
        self.stickyDate = None
        return

    def createInfoRequest(self):
        self.w = newOrderWindow()
        self.selectedOrderNumber = None
        
        self.custFirstName = QLineEdit()
        self.custLastName = QLineEdit()
        self.custPhoneNumber = QLineEdit()
        self.custEmail = QLineEdit()
        self.prodDesc = QLineEdit()
        self.partNo = QLineEdit()
        self.supplier = QComboBox()
        self.partPrice = QLineEdit()
        self.orderNumber = QLineEdit()
        self.orderStatusChoice = QComboBox()
        self.orderDesc = QTextEdit()
        self.payStatus = QComboBox()
        self.orderType = QCheckBox()
        self.salesRep = QComboBox()
        self.qty = QSpinBox()
        
        self.payStatus.addItems(self.paymentStatus)
        self.salesRep.addItems(staffMembers)
        self.supplier.addItems(suppliers)
        self.qty.setMaximum(999)
        self.qty.setMinimum(1)
        
        #self.sendOrder = QPushButton("Create")
        #self.cancelCreation = QPushButton("Cancel")

        self.wButtons = QHBoxLayout()
        self.buttonBox = QDialogButtonBox()
        self.wLayout = QGridLayout()
        self.wLayoutCust = QFormLayout()
        self.wLayoutPart = QFormLayout()
        self.wLayoutNotes = QFormLayout()

        self.wLayoutCust.addRow("First Name", self.custFirstName)
        self.wLayoutCust.addRow("Last Name", self.custLastName)
        self.wLayoutCust.addRow("Phone Number", self.custPhoneNumber)
        self.wLayoutCust.addRow("E-Mail Address", self.custEmail)
        #self.wLayoutCust.addRow("Order Number", self.orderNumber)
        #self.wLayoutCust.addRow("Workorder?", self.orderType)
        #self.wLayoutCust.addRow("Payment Status", self.payStatus)
        
        self.wLayoutPart.addRow("Product", self.prodDesc)
        #self.wLayoutPart.addRow("Part Number", self.partNo)
        #self.wLayoutPart.addRow("Supplier", self.supplier)
        #self.wLayoutPart.addRow("Price", self.partPrice)
        self.wLayoutPart.addRow("Placed By", self.salesRep)
        self.wLayoutPart.addRow("Quantity:", self.qty)

        self.wLayoutNotes.addRow("Notes:", self.orderDesc)
        self.objectID = 0



        self.cancelCreation = self.buttonBox.addButton(QDialogButtonBox.Cancel)
        self.sendOrder = self.buttonBox.addButton(QDialogButtonBox.Ok)
        self.wButtons.addWidget(self.buttonBox)
        self.dateOrderedVar = None

        self.wLayout.addLayout(self.wLayoutCust,0,0)
        self.wLayout.addLayout(self.wLayoutPart,0,1)
        self.wLayout.addLayout(self.wLayoutNotes,1,0,1,2)
        self.wLayout.addLayout(self.wButtons,2,0,1,2)

        self.sendOrder.clicked.connect(self.commitInfoRequest)
        self.cancelCreation.clicked.connect(self.closeBasic) 

        self.w.setGeometry(500, 400, 500, 350)
        self.w.setWindowTitle('Product Info Request')
        self.w.setLayout(self.wLayout)
        self.w.show()
        self.stickyDate = None
        return

    def createChildOrder(self):
        self.w = newOrderWindow()
        self.selectedOrderNumber = self.getSelectedOrderNumber()
        
        self.custFirstName = QLineEdit()
        self.custLastName = QLineEdit()
        self.custPhoneNumber = QLineEdit()
        self.custEmail = QLineEdit()
        self.prodDesc = QLineEdit()
        self.partNo = QLineEdit()
        self.supplier = QComboBox()
        self.partPrice = QLineEdit()
        self.orderNumber = QLineEdit()
        self.orderStatusChoice = QComboBox()
        self.orderDesc = QTextEdit()
        self.payStatus = QComboBox()
        self.orderType = QCheckBox()
        self.salesRep = QComboBox()
        self.qty = QSpinBox()

        data = fetchOrder(self.selectedOrderNumber)
        self.custFirstName.setDisabled(True)
        self.custLastName.setDisabled(True)
        self.custPhoneNumber.setDisabled(True)
        self.custEmail.setDisabled(True)
        self.orderNumber.setDisabled(True)
        self.orderType.setDisabled(True)
        self.custFirstName.setText(data['customerFirstName'])
        self.custLastName.setText(data['customerLastName'])
        self.custPhoneNumber.setText(str(data['customerPhoneNo']))
        self.custEmail.setText(data['customerEmail'])
        self.orderNumber.setText(str(data['orderID']))
        if data['isWorkOrder'] == 1:
                self.orderType.setChecked(True)
        self.qty.setMaximum(999)
        self.qty.setMinimum(1)
        
        self.payStatus.addItems(self.paymentStatus)
        self.salesRep.addItems(staffMembers)
        self.supplier.addItems(suppliers)

        self.wButtons = QHBoxLayout()
        self.buttonBox = QDialogButtonBox()
        self.wLayout = QGridLayout()
        self.wLayoutCust = QFormLayout()
        self.wLayoutPart = QFormLayout()
        self.wLayoutNotes = QFormLayout()

        self.wLayoutCust.addRow("First Name", self.custFirstName)
        self.wLayoutCust.addRow("Last Name", self.custLastName)
        self.wLayoutCust.addRow("Phone Number", self.custPhoneNumber)
        self.wLayoutCust.addRow("E-Mail Address", self.custEmail)
        self.wLayoutCust.addRow("Order Number", self.orderNumber)
        self.wLayoutCust.addRow("Workorder?", self.orderType)
        self.wLayoutCust.addRow("Payment Status", self.payStatus)
        
        self.wLayoutPart.addRow("Product", self.prodDesc)
        self.wLayoutPart.addRow("Part Number", self.partNo)
        self.wLayoutPart.addRow("Supplier", self.supplier)
        self.wLayoutPart.addRow("Price", self.partPrice)
        self.wLayoutPart.addRow("Placed By", self.salesRep)
        self.wLayoutPart.addRow("Quantity:", self.qty)

        self.wLayoutNotes.addRow("Notes:", self.orderDesc)
        self.objectID = 0

        self.cancelCreation = self.buttonBox.addButton(QDialogButtonBox.Cancel)
        self.sendOrder = self.buttonBox.addButton(QDialogButtonBox.Ok)
        self.wButtons.addWidget(self.buttonBox)
        self.dateOrderedVar = None

        self.wLayout.addLayout(self.wLayoutCust,0,0)
        self.wLayout.addLayout(self.wLayoutPart,0,1)
        self.wLayout.addLayout(self.wLayoutNotes,1,0,1,2)
        self.wLayout.addLayout(self.wButtons,2,0,1,2)

        self.sendOrder.clicked.connect(self.commitSpecialOrder)
        self.cancelCreation.clicked.connect(self.closeBasic) 

        self.w.setGeometry(500, 400, 500, 350)
        self.w.setWindowTitle('Add Item To Order')
        self.w.setLayout(self.wLayout)
        self.w.show()
        self.stickyDate = None
        return

    def editSpecialOrder(self):
        self.selectedOrderNumber = self.getSelectedOrderNumber()
        print('Editing Order #' + str(self.selectedOrderNumber))
        self.w = newOrderWindow()
        
        self.custFirstName = QLineEdit()
        self.custLastName = QLineEdit()
        self.custPhoneNumber = QLineEdit()
        self.custEmail = QLineEdit()
        self.prodDesc = QLineEdit()
        self.partNo = QLineEdit()
        self.supplier = QComboBox()
        self.partPrice = QLineEdit()
        self.orderNumber = QLineEdit()
        self.orderStatusChoice = QComboBox()
        self.orderDesc = QTextEdit()
        self.payStatus = QComboBox()
        self.orderType = QCheckBox()
        self.salesRep = QComboBox()
        self.dateOrdered = QCalendarWidget()
        self.dateRequested = QLabel()
        self.qty = QSpinBox()

        self.qty.setMaximum(999)
        self.qty.setMinimum(1)
        self.payStatus.addItems(self.paymentStatus)
        self.salesRep.addItems(staffMembers)
        self.supplier.addItems(suppliers)
        self.orderStatusChoice.addItems(self.orderStatus)

        self.wButtons = QHBoxLayout()
        self.buttonBox = QDialogButtonBox()
        self.wLayout = QGridLayout()
        self.wLayoutCust = QFormLayout()
        self.wLayoutPart = QFormLayout()
        self.wLayoutNotes = QFormLayout()

        self.wLayoutCust.addRow("First Name", self.custFirstName)
        self.wLayoutCust.addRow("Last Name", self.custLastName)
        self.wLayoutCust.addRow("Phone Number", self.custPhoneNumber)
        self.wLayoutCust.addRow("E-Mail Address", self.custEmail)
        self.wLayoutCust.addRow("Order Number", self.orderNumber)
        self.wLayoutCust.addRow("Workorder?", self.orderType)
        self.wLayoutCust.addRow("Payment Status", self.payStatus)
        
        self.wLayoutPart.addRow("Product", self.prodDesc)
        self.wLayoutPart.addRow("Part Number", self.partNo)
        self.wLayoutPart.addRow("Supplier", self.supplier)
        self.wLayoutPart.addRow("Price", self.partPrice)
        self.wLayoutPart.addRow("Quantity:", self.qty)
        self.wLayoutPart.addRow("Placed By", self.salesRep)
        self.wLayoutPart.addRow("Order Status:", self.orderStatusChoice)
        self.wLayoutPart.addRow("Requested On:", self.dateRequested)

        self.wLayoutNotes.addRow("Date Ordered", self.dateOrdered)
        self.wLayoutNotes.addRow("Notes:", self.orderDesc)

        if self.selectedOrderNumber != None:
            data = fetchOrder(self.selectedOrderNumber)
            self.custFirstName.setText(data['customerFirstName'])
            self.custLastName.setText(data['customerLastName'])
            self.custPhoneNumber.setText(str(data['customerPhoneNo']))
            self.custEmail.setText(data['customerEmail'])
            self.orderNumber.setText(str(data['orderID']))
            if data['isWorkOrder'] == 1:
                self.orderType.setChecked(True)
            self.payStatus.setCurrentIndex(data['paymentStatus'])
            self.orderStatusChoice.setCurrentIndex(data['orderStatus'])
            
            self.prodDesc.setText(data['productDesc'])
            if type(data['dateOrdered']) == type(date.today()):
                self.dateOrdered.setSelectedDate(data['dateOrdered'])
            self.partNo.setText(data['productPartNo'])
            self.supplier.setCurrentText(data['productSupplier'])
            self.partPrice.setText(str(data['price']))
            self.salesRep.setCurrentText(data['salesRep'])
            self.orderDesc.setText(data['orderDesc'])
            self.dateOrdered.setGridVisible(True)
            self.dateRequested.setText(data['dateRequested'].isoformat())
            self.qty.setValue(data['qty'])
            self.stickyDate = data['dateRequested'].isoformat()
            self.objectID = data['objectID']

            self.cancelCreation = self.buttonBox.addButton(QDialogButtonBox.Cancel)
            self.removeOrder = self.buttonBox.addButton(QDialogButtonBox.Cancel)
            self.sendOrder = self.buttonBox.addButton(QDialogButtonBox.Ok)
            self.addToOrder = self.buttonBox.addButton(QDialogButtonBox.Ok)
            if self.payStatus.currentText() == "Pending Payment":
                self.sendRequestButton = self.buttonBox.addButton(QDialogButtonBox.Reset)
                self.sendRequestButton.setText('Send Payment Request')
                self.sendRequestButton.clicked.connect(self.sendRequest)
            self.wButtons.addWidget(self.buttonBox)
            self.removeOrder.setText('Delete')
            self.sendOrder.setText('Update')
            self.addToOrder.setText('Add Item')
            
            self.wLayout.addLayout(self.wLayoutCust,0,0)
            self.wLayout.addLayout(self.wLayoutPart,0,1)
            self.wLayout.addLayout(self.wLayoutNotes,1,0,1,2)
            self.wLayout.addLayout(self.wButtons,2,0,1,2)

            self.sendOrder.clicked.connect(self.cleanupEditied)
            self.removeOrder.clicked.connect(self.delete)
            self.cancelCreation.clicked.connect(self.closeBasic)
            self.addToOrder.clicked.connect(self.createChildOrder)

            self.w.setGeometry(500, 400, 500, 550)
            self.w.setWindowTitle('Edit Special Order')
            self.w.setLayout(self.wLayout)
            self.w.show()
        return

    def cleanupEditied(self):
        self.dateOrderedVar = self.dateOrdered.selectedDate().toPyDate()
        if self.preCommitCheck():
            self.deleteSilent()
        self.commitSpecialOrder()

    def setNotesSection(self):
        thing = self.getSelectedOrderNumber()
        data = fetchOrder(thing)
        if data != None:
            self.notesSectionSO.setText(data['orderDesc'])
        else:
            self.notesSectionSO.setText('')

    def preCommitCheck(self):
        incomplete = False
        mandatoryList = [
            self.custFirstName,
            self.custLastName,
            self.custPhoneNumber,
            self.custEmail,
            self.orderNumber,
            self.prodDesc,
            self.partNo,
            self.partPrice,
            ]

        
        if self.salesRep.currentText() == '--Choose One--':
            incomplete = True
        if self.supplier.currentText() == '--Choose One--':
            incomplete = True

        for item in mandatoryList:
            if item.text() == '':
                item.setStyleSheet("background-color: rgb(255, 193, 193);")
                incomplete = True
            else:
                item.setStyleSheet("background-color: white;")

        if not self.isInt(self.orderNumber.text()):
            self.orderNumber.setStyleSheet("background-color: rgb(255, 193, 193);")
            incomplete = True
        else:
            self.orderNumber.setStyleSheet("background-color: white;")
        
        if not self.isFloat(self.partPrice.text()):
            self.partPrice.setStyleSheet("background-color: rgb(255, 193, 193);")
            incomplete = True
        else:
            self.partPrice.setStyleSheet("background-color: white;")
        if self.intPhoneNumber(self.custPhoneNumber.text()) == None:
            self.custPhoneNumber.setStyleSheet("background-color: rgb(255, 193, 193);")
            incomplete = True
        else:
            self.custPhoneNumber.setStyleSheet("background-color: white;")
        if not incomplete:
            return True
        else:
            return False

    def commitSpecialOrder(self):
        if self.preCommitCheck():
            if self.stickyDate == None:
                theDate = date.today()
            else:
                theDate = self.stickyDate
            
            if self.orderNumber.text() == '0':
                theNumber = self.objectID
            else:
                theNumber = int(self.orderNumber.text())

            data = {
                'customerFirstName':self.custFirstName.text(),
                'customerLastName':self.custLastName.text(),
                'customerPhoneNo':self.intPhoneNumber(self.custPhoneNumber.text()),
                'customerEmail' :self.custEmail.text(),
                'productDesc' :self.prodDesc.text(),
                'productPartNo' :self.partNo.text(),
                'productSupplier' :self.supplier.currentText(),
                'dateRequested' :theDate,
                'dateOrdered' :self.dateOrderedVar,
                'orderID' :theNumber,
                'orderStatus' :self.orderStatusChoice.currentIndex(),
                'orderDesc' :self.orderDesc.toPlainText(),
                'paymentStatus' :self.payStatus.currentIndex(),
                'isWorkOrder' :self.orderType.isChecked(),
                'salesRep':self.salesRep.currentText(),
                'objectID':self.objectID,
                'price':float(self.partPrice.text()), #Type FLOAT
                'weight':35, #Type INT
                'dimLength': 55, #Type INT
                'dimWidth':9, #Type INT
                'dimHeight':33, #Type INT
                'qty':self.qty.value(),
                }
            if data['orderStatus'] == -1:
                data['orderStatus'] = 0
            self.selectedOrderNumber = writeOrder(data)
            print('Creating Order #' + str(self.selectedOrderNumber))
            self.closeRefresh()
            return True
        else:
            self.w.warning()
            return False

    def commitInfoRequest(self):
        if not self.preCommitCheck():
            if self.stickyDate == None:
                theDate = date.today()
            else:
                theDate = self.stickyDate

            data = {
                'customerFirstName':self.custFirstName.text(),
                'customerLastName':self.custLastName.text(),
                'customerPhoneNo':self.intPhoneNumber(self.custPhoneNumber.text()),
                'customerEmail' :self.custEmail.text(),
                'productDesc' :self.prodDesc.text(),
                'productPartNo' :'0',
                'productSupplier' :'Other',
                'dateRequested' :theDate,
                'dateOrdered' :self.dateOrderedVar,
                'orderID' :self.intPhoneNumber(self.custPhoneNumber.text())/3,
                'orderStatus' :5,
                'orderDesc' :self.orderDesc.toPlainText(),
                'paymentStatus' :0,
                'isWorkOrder' :True,
                'salesRep':self.salesRep.currentText(),
                'objectID':0,
                'price':0.0, #Type FLOAT
                'weight':35, #Type INT
                'dimLength': 55, #Type INT
                'dimWidth':9, #Type INT
                'dimHeight':33, #Type INT
                'qty':self.qty.value(),
                }
            if data['orderStatus'] == -1:
                data['orderStatus'] = 0
            self.selectedOrderNumber = writeOrder(data)
            print('Creating Order #' + str(self.selectedOrderNumber))
            self.closeRefresh()
            return True
        else:
            return False

    def searchOrders(self):
        if self.search.text() == '':
            self.tableWidgetSO.clear()
            self.addOrdersLoop()
            return
        self.tableWidgetSO.clear()
        self.searchedOrdersLoop()

    def filterOrders(self):
        self.tableWidgetSO.clear()
        if self.filterOrderStatus.currentText() == '':
            self.addOrdersLoop()
        else:
            self.filteredOrdersLoop()

# Claim Related Functions
    def addClaimsLoop(self):
        self.claimList = []
        self.objectClaimIDs = {}
        self.orderStatus = ['Requested','Order Placed','Order Recieved',
        'Backordered','Not Available', 'Info Requested', 'Insuffecient Information']
        self.paymentStatus = ['Pending Payment','Partially Paid','Fully Paid']

        warrantyClaims = fetchClaims()
        importantFont = QFont()

        j=0
        for item in warrantyClaims:
            if self.orderStatus[item[10]] == 'Requested':
            #if self.orderStatus[item[10]] == 'Requested' and self.paymentStatus[item[12]] == 'Fully Paid':
                importantFont.setBold(True)
            else:
                importantFont.setBold(False)

            self.claimList.append(QTreeWidgetItem())
            self.objectClaimIDs[j] = item[15]
            #First Name Column
            self.claimList[j].setText(0, str(item[0]))
            self.claimList[j].setFont(0, importantFont)
            #Last Name Column
            self.claimList[j].setText(1, str(item[1]))
            self.claimList[j].setBackground(1,QColor("lightGray"))
            self.claimList[j].setFont(1, importantFont)
            #Phone Column
            self.claimList[j].setText(2, self.parsePhoneNumber(str(item[2])))
            self.claimList[j].setFont(2, importantFont)
            #Email Column
            self.claimList[j].setText(3, str(item[3]))
            self.claimList[j].setBackground(3,QColor("lightGray"))
            self.claimList[j].setFont(3, importantFont)
            #Things
            self.claimList[j].setText(4, str(item[4]))
            self.claimList[j].setFont(4, importantFont)
            #Things
            self.claimList[j].setText(5, str(item[5]))
            self.claimList[j].setBackground(5,QColor("lightGray"))
            self.claimList[j].setFont(5, importantFont)
            #Things
            self.claimList[j].setText(6, str(item[6]))
            self.claimList[j].setFont(6, importantFont)
            #Things
            self.claimList[j].setText(7, str(item[7]))
            self.claimList[j].setBackground(7,QColor("lightGray"))
            self.claimList[j].setFont(7, importantFont)
            #Date Ordered
            if self.orderStatus[item[10]] == 'Requested':
                self.claimList[j].setText(8, '')
            elif item[8] == None:
                self.claimList[j].setText(8, '')
            else:
                self.claimList[j].setText(8, str(item[8]))
            self.claimList[j].setFont(8, importantFont)
            #Things
            self.claimList[j].setText(9, str(item[9]))
            self.claimList[j].setBackground(9,QColor("lightGray"))
            self.claimList[j].setFont(9, importantFont)
            #Order Status Column
            self.claimList[j].setText(10, self.orderStatus[item[10]])
            self.claimList[j].setFont(10, importantFont)
            #Order Status Column
            self.claimList[j].setText(11, str(round(item[16], 3)))
            self.claimList[j].setBackground(11,QColor("lightGray"))
            self.claimList[j].setFont(11, importantFont)
            #Payment Status Colum
            self.claimList[j].setText(12, self.paymentStatus[item[12]])
            self.claimList[j].setFont(12, importantFont)
            #Order Type Column
            if item[13] == 1:
                self.claimList[j].setText(13, "Workorder")
                self.claimList[j].setForeground(13,QColor("Blue"))
                self.claimList[j].setBackground(13,QColor("lightGray"))
            else:
                self.claimList[j].setText(13, "Layaway")
                self.claimList[j].setForeground(13,QColor("Green"))
                self.claimList[j].setBackground(13,QColor("lightGray"))
            self.claimList[j].setFont(13, importantFont)
            #Things
            self.claimList[j].setText(14, str(item[14]))
            self.claimList[j].setFont(14, importantFont)


            self.tableWidgetWC.addTopLevelItem(self.claimList[j])
            j+=1

            for i in range(len(self.headerListWC)):
                self.tableWidgetWC.resizeColumnToContents(i)

    def getSelectedClaimNumber(self):
        i = 0
        for item in self.claimList:
            if item.isSelected():
                #9 Pulls Order ID Number to pass
                return self.objectClaimIDs[i]
            i+=1

    def createWarrantyClaim(self):
        self.w = newOrderWindow()
        self.selectedOrderNumber = None
        
        self.custFirstName = QLineEdit()
        self.custLastName = QLineEdit()
        self.custPhoneNumber = QLineEdit()
        self.custEmail = QLineEdit()
        self.prodDesc = QLineEdit()
        self.partNo = QLineEdit()
        self.supplier = QComboBox()
        self.partPrice = QLineEdit()
        self.orderNumber = QLineEdit()
        self.orderStatusChoice = QComboBox()
        self.orderDesc = QTextEdit()
        self.payStatus = QComboBox()
        self.orderType = QCheckBox()
        self.salesRep = QComboBox()
        self.qty = QSpinBox()
        
        self.payStatus.addItems(self.paymentStatus)
        self.salesRep.addItems(staffMembers)
        self.supplier.addItems(suppliers)
        self.qty.setMaximum(999)
        self.qty.setMinimum(1)
        
        #self.sendOrder = QPushButton("Create")
        #self.cancelCreation = QPushButton("Cancel")

        self.wButtons = QHBoxLayout()
        self.buttonBox = QDialogButtonBox()
        self.wLayout = QGridLayout()
        self.wLayoutCust = QFormLayout()
        self.wLayoutPart = QFormLayout()
        self.wLayoutNotes = QFormLayout()

        self.wLayoutCust.addRow("First Name", self.custFirstName)
        self.wLayoutCust.addRow("Last Name", self.custLastName)
        self.wLayoutCust.addRow("Phone Number", self.custPhoneNumber)
        self.wLayoutCust.addRow("E-Mail Address", self.custEmail)
        self.wLayoutCust.addRow("Order Number", self.orderNumber)
        self.wLayoutCust.addRow("Workorder?", self.orderType)
        self.wLayoutCust.addRow("Payment Status", self.payStatus)
        
        self.wLayoutPart.addRow("Product", self.prodDesc)
        self.wLayoutPart.addRow("Part Number", self.partNo)
        self.wLayoutPart.addRow("Supplier", self.supplier)
        self.wLayoutPart.addRow("Price", self.partPrice)
        self.wLayoutPart.addRow("Placed By", self.salesRep)
        self.wLayoutPart.addRow("Quantity:", self.qty)

        self.wLayoutNotes.addRow("Notes:", self.orderDesc)
        self.objectID = 0

        self.cancelCreation = self.buttonBox.addButton(QDialogButtonBox.Cancel)
        self.sendOrder = self.buttonBox.addButton(QDialogButtonBox.Ok)
        self.wButtons.addWidget(self.buttonBox)
        self.dateOrderedVar = None

        self.wLayout.addLayout(self.wLayoutCust,0,0)
        self.wLayout.addLayout(self.wLayoutPart,0,1)
        self.wLayout.addLayout(self.wLayoutNotes,1,0,1,2)
        self.wLayout.addLayout(self.wButtons,2,0,1,2)

        self.sendOrder.clicked.connect(self.commitWarrantyClaim)
        self.cancelCreation.clicked.connect(self.closeBasic) 

        self.w.setGeometry(500, 400, 500, 350)
        self.w.setWindowTitle('New Warranty Claim')
        self.w.setLayout(self.wLayout)
        self.w.show()
        self.stickyDate = None
        return

    def editWarrantyClaim(self):
        self.selectedClaimNumber = self.getSelectedClaimNumber()
        print('Editing Order #' + str(self.selectedClaimNumber))
        self.w = newOrderWindow()
        
        self.custFirstName = QLineEdit()
        self.custLastName = QLineEdit()
        self.custPhoneNumber = QLineEdit()
        self.custEmail = QLineEdit()
        self.prodDesc = QLineEdit()
        self.partNo = QLineEdit()
        self.supplier = QComboBox()
        self.partPrice = QLineEdit()
        self.orderNumber = QLineEdit()
        self.orderStatusChoice = QComboBox()
        self.orderDesc = QTextEdit()
        self.payStatus = QComboBox()
        self.orderType = QCheckBox()
        self.salesRep = QComboBox()
        self.dateOrdered = QCalendarWidget()
        self.dateRequested = QLabel()
        self.qty = QSpinBox()

        self.qty.setMaximum(999)
        self.qty.setMinimum(1)
        self.payStatus.addItems(self.paymentStatus)
        self.salesRep.addItems(staffMembers)
        self.supplier.addItems(suppliers)
        self.orderStatusChoice.addItems(self.orderStatus)

        self.wButtons = QHBoxLayout()
        self.buttonBox = QDialogButtonBox()
        self.wLayout = QGridLayout()
        self.wLayoutCust = QFormLayout()
        self.wLayoutPart = QFormLayout()
        self.wLayoutNotes = QFormLayout()

        self.wLayoutCust.addRow("First Name", self.custFirstName)
        self.wLayoutCust.addRow("Last Name", self.custLastName)
        self.wLayoutCust.addRow("Phone Number", self.custPhoneNumber)
        self.wLayoutCust.addRow("E-Mail Address", self.custEmail)
        self.wLayoutCust.addRow("Order Number", self.orderNumber)
        self.wLayoutCust.addRow("Workorder?", self.orderType)
        self.wLayoutCust.addRow("Payment Status", self.payStatus)
        
        self.wLayoutPart.addRow("Product", self.prodDesc)
        self.wLayoutPart.addRow("Part Number", self.partNo)
        self.wLayoutPart.addRow("Supplier", self.supplier)
        self.wLayoutPart.addRow("Price", self.partPrice)
        self.wLayoutPart.addRow("Quantity:", self.qty)
        self.wLayoutPart.addRow("Placed By", self.salesRep)
        self.wLayoutPart.addRow("Order Status:", self.orderStatusChoice)
        self.wLayoutPart.addRow("Requested On:", self.dateRequested)

        self.wLayoutNotes.addRow("Date Ordered", self.dateOrdered)
        self.wLayoutNotes.addRow("Notes:", self.orderDesc)

        if self.selectedClaimNumber != None:
            data = fetchClaim(self.selectedClaimNumber)
            self.custFirstName.setText(data['customerFirstName'])
            self.custLastName.setText(data['customerLastName'])
            self.custPhoneNumber.setText(str(data['customerPhoneNo']))
            self.custEmail.setText(data['customerEmail'])
            self.orderNumber.setText(str(data['orderID']))
            if data['isWorkOrder'] == 1:
                self.orderType.setChecked(True)
            self.payStatus.setCurrentIndex(data['paymentStatus'])
            self.orderStatusChoice.setCurrentIndex(data['orderStatus'])
            
            self.prodDesc.setText(data['productDesc'])
            if type(data['dateOrdered']) == type(date.today()):
                self.dateOrdered.setSelectedDate(data['dateOrdered'])
            self.partNo.setText(data['productPartNo'])
            self.supplier.setCurrentText(data['productSupplier'])
            self.partPrice.setText(str(data['price']))
            self.salesRep.setCurrentText(data['salesRep'])
            self.orderDesc.setText(data['orderDesc'])
            self.dateOrdered.setGridVisible(True)
            self.dateRequested.setText(data['dateRequested'].isoformat())
            self.stickyDate = data['dateRequested'].isoformat()
            self.objectID = data['objectID']

            self.cancelCreation = self.buttonBox.addButton(QDialogButtonBox.Cancel)
            self.removeOrder = self.buttonBox.addButton(QDialogButtonBox.Cancel)
            self.sendOrder = self.buttonBox.addButton(QDialogButtonBox.Ok)
            self.addToOrder = self.buttonBox.addButton(QDialogButtonBox.Ok)
            if self.payStatus.currentText() == "Pending Payment":
                self.sendRequestButton = self.buttonBox.addButton(QDialogButtonBox.Reset)
                self.sendRequestButton.setText('Send Payment Request')
                self.sendRequestButton.clicked.connect(self.sendRequest)
            self.wButtons.addWidget(self.buttonBox)
            self.removeOrder.setText('Delete')
            self.sendOrder.setText('Update')
            self.addToOrder.setText('Add Item')
            
            self.wLayout.addLayout(self.wLayoutCust,0,0)
            self.wLayout.addLayout(self.wLayoutPart,0,1)
            self.wLayout.addLayout(self.wLayoutNotes,1,0,1,2)
            self.wLayout.addLayout(self.wButtons,2,0,1,2)

            self.sendOrder.clicked.connect(self.cleanupEditiedClaim)
            self.removeOrder.clicked.connect(self.deleteClaimWarning)
            self.cancelCreation.clicked.connect(self.closeBasic)

            self.w.setGeometry(500, 400, 500, 550)
            self.w.setWindowTitle('Edit Special Order')
            self.w.setLayout(self.wLayout)
            self.w.show()
        return

    def commitWarrantyClaim(self):
        if self.preCommitCheck():
            if self.stickyDate == None:
                theDate = date.today()
            else:
                theDate = self.stickyDate
            
            if self.orderNumber.text() == '0':
                theNumber = self.objectID
            else:
                theNumber = int(self.orderNumber.text())

            data = {
                'customerFirstName':self.custFirstName.text(),
                'customerLastName':self.custLastName.text(),
                'customerPhoneNo':self.intPhoneNumber(self.custPhoneNumber.text()),
                'customerEmail' :self.custEmail.text(),
                'productDesc' :self.prodDesc.text(),
                'productPartNo' :self.partNo.text(),
                'productSupplier' :self.supplier.currentText(),
                'dateRequested' :theDate,
                'dateOrdered' :self.dateOrderedVar,
                'orderID' :theNumber,
                'orderStatus' :self.orderStatusChoice.currentIndex(),
                'orderDesc' :self.orderDesc.toPlainText(),
                'paymentStatus' :self.payStatus.currentIndex(),
                'isWorkOrder' :self.orderType.isChecked(),
                'salesRep':self.salesRep.currentText(),
                'objectID':self.objectID,
                'price':float(self.partPrice.text()), #Type FLOAT
                'weight':35, #Type INT
                'dimLength': 55, #Type INT
                'dimWidth':9, #Type INT
                'dimHeight':33, #Type INT
                'qty':self.qty.value(),
                }
            if data['orderStatus'] == -1:
                data['orderStatus'] = 0
            self.selectedClaimNumber = writeClaim(data)
            print('Creating Order #' + str(self.selectedClaimNumber))
            self.closeRefresh()
            return True
        else:
            self.w.warning()
            return False

    def getSelectedClaimNumber(self):
        i = 0
        for item in self.claimList:
            if item.isSelected():
                #9 Pulls Order ID Number to pass
                return self.objectClaimIDs[i]
            i+=1

    def cleanupEditiedClaim(self):
        self.dateOrderedVar = self.dateOrdered.selectedDate().toPyDate()
        if self.preCommitCheck():
            self.deleteClaimSilent()
        self.commitWarrantyClaim()

    def deleteClaimSilent(self):
        i=0
        for item in self.claimList:
            if item.isSelected():
                print('Deleting Order #' + str(self.objectClaimIDs[i]))
                deleteClaim(self.objectClaimIDs[i])
                item.setHidden(True)
            i+=1

    def deleteClaimWarning(self):
        i=0
        for item in self.claimList:
            if item.isSelected():
                answer = QMessageBox.question(self, 'Deletion', 
                "Are you sure you want to delete this Warranty Claim?")
                if answer == QMessageBox.Yes:
                    print('Deleting Order #' + str(self.objectClaimIDs[i]))
                    deleteClaim(self.objectClaimIDs[i])
                    item.setHidden(True)
            i+=1

# Online Realted Functions
    def addOnlineLoop(self):
        '''onlineOrders = self.wooConnect().get('orders/72015').json()
        test = QTreeWidgetItem()
        test2 = QTreeWidgetItem()
        test3 = QTreeWidgetItem()
        self.tableWidgetOO2.addTopLevelItem(test)
        test.addChildren([test2, test3])

        test.setText(0, onlineOrders['shipping']['first_name'])
        test.setText(1, onlineOrders['shipping']['last_name'])
        test.setText(2, onlineOrders['billing']['phone'])
        test.setText(3, onlineOrders['billing']['email'])
        test.setText(4, '------')
        test.setText(5, '------')
        test.setText(6, '$'+onlineOrders['total'])
        test.setText(7, '------')
        for i in range(8):
            test.setBackground(i, QColor("lightGray"))

        test2.setText(0, onlineOrders['shipping']['first_name'])
        test2.setText(1, onlineOrders['shipping']['last_name'])
        test2.setText(2, onlineOrders['billing']['phone'])
        test2.setText(3, onlineOrders['billing']['email'])
        test2.setText(4, onlineOrders['line_items'][0]['name'])
        test2.setText(5, str(onlineOrders['line_items'][0]['quantity']))
        test2.setText(6, '$'+str(onlineOrders['line_items'][0]['subtotal']))
        test2.setText(7, str(onlineOrders['line_items'][0]['sku']))

        test3.setText(0, onlineOrders['shipping']['first_name'])
        test3.setText(1, onlineOrders['shipping']['last_name'])
        test3.setText(2, onlineOrders['billing']['phone'])
        test3.setText(3, onlineOrders['billing']['email'])
        test3.setText(4, onlineOrders['line_items'][1]['name'])
        test3.setText(5, str(onlineOrders['line_items'][1]['quantity']))
        test3.setText(6, '$'+str(onlineOrders['line_items'][1]['subtotal']))
        test3.setText(7, str(onlineOrders['line_items'][1]['sku']))'''

        return

    def createOnlineOrder(self):
        self.w = newOrderWindow()
        
        self.custFirstName = QLineEdit()
        self.custLastName = QLineEdit()
        self.custPhoneNumber = QLineEdit()
        self.custEmail = QLineEdit()
        self.layawayNumber = QLineEdit()
        self.layawaySubtotal = QLineEdit()
        self.productName = QLineEdit()
        self.salesRep = QComboBox()
        self.sendOrder = QPushButton("Send")
        self.cancelCreation = QPushButton("Cancel")

        self.salesRep.addItems(staffMembers)
        self.wButtons = QHBoxLayout()
        self.wProgLayout = QVBoxLayout()
        self.wLayout = QFormLayout()
        self.wLayout.addRow("First Name", self.custFirstName)
        self.wLayout.addRow("Last Name", self.custLastName)
        self.wLayout.addRow("Phone Number", self.custPhoneNumber)
        self.wLayout.addRow("E-Mail Address", self.custEmail)
        self.wLayout.addRow("Product Name", self.productName)
        self.wLayout.addRow("Layaway/Work Order Number", self.layawayNumber)
        self.wLayout.addRow("Layaway Total (Before Tax)", self.layawaySubtotal)
        self.wLayout.addRow("Staff Name", self.salesRep)
        self.wButtons.addWidget(self.sendOrder)
        self.wButtons.addWidget(self.cancelCreation)
        
        self.progress = QProgressBar()
        self.progressLabel = QLabel()
        self.progress.setMinimum(0)
        self.progress.setMaximum(100)
        self.progress.setTextVisible(True)
        self.wProgLayout.addWidget(self.progressLabel)
        self.wProgLayout.addWidget(self.progress)
        
        self.wLayout.addRow(self.wProgLayout)
        self.wLayout.addRow(self.wButtons)


        self.w.setGeometry(500, 400, 400, 300)
        self.w.setWindowTitle('Send Payment Request')
        self.w.setLayout(self.wLayout)

        self.w.show()
        self.sendOrder.clicked.connect(self.sendPaymentRequest)
        self.cancelCreation.clicked.connect(self.w.close)
        return

# Core Functions
    def isFloat(self, i):
        try:
            float(i)
            return True
        except ValueError:
            return False

    def isInt(self, i):
        try:
            int(i)
            return True
        except ValueError:
            return False

    def intPhoneNumber(self, number):
        if len(number) == 0:
            return None
        
        i = 0
        newNumber = ""
        forbiddenChars = ["-"," ","(",")","+","."]
        
        for item in number:
            if item not in forbiddenChars:
                newNumber += item

        if newNumber[0] == "1":
            newNumber = newNumber[1:]
        dashNumber = ""
        for item in newNumber:
            dashNumber += item
            i+=1

        if self.isInt(dashNumber):
            return int(dashNumber)
        else:
            return None

    def parsePhoneNumber(self, number):
        i = 0
        newNumber = ""
        forbiddenChars = ["-"," ","(",")","+","."]
        
        for item in number:
            if item not in forbiddenChars:
                newNumber += item

        if newNumber[0] == "1":
            newNumber = newNumber[1:]
        newNumber = "1 " + newNumber
        dashNumber = ""
        for item in newNumber:
            if i == 5:
                dashNumber += " "
                dashNumber += item
            elif i == 8:
                dashNumber += " "
                dashNumber += item
            else:
                dashNumber += item
            i+=1

        return dashNumber

    def wooConnect(self):
        wcapi = API(
            url = wcAPIConfig['url'],
            consumer_key = wcAPIConfig['consumer_key'],
            consumer_secret = wcAPIConfig['consumer_secret'],
            wp_api = True,
            version = "wc/v3"
        )

        return wcapi

    def createWooProduct(self, first_name, last_name, layaway, total, weight='', length='', width='', height=''):
        #Connecting to the Woo Commerce REST API
        print('Building WooCommerce Product')
        wcapi = API(
            url=wcAPILegacyConfig['url'],
            consumer_key=wcAPILegacyConfig['consumer_key'],
            consumer_secret=wcAPILegacyConfig['consumer_secret'],
            wp_api=wcAPILegacyConfig['wp_api'],
            version=wcAPILegacyConfig['version'],
            verify_ssl=wcAPILegacyConfig['verify_ssl'],
            timeout=wcAPILegacyConfig['timeout'],
        )

        check = wcapi.get('products?sku='+layaway).json()
        self.progress.setValue(66)
        if check == []:
            print('Payment for this order hasn\'t been sent yet. Building new Product')
            data = {
                "name": "Online Payment - "+layaway,
                "catalog_visibility": "visible",
                "type": "simple",
                "price": total,
                "regular_price": total,
                "manage_stock": True,
                "stock_quantity": 1,
                "in_stock": True,
                "sku":layaway,
                "description": "Online Payment for Special Order #"+layaway,
                "weight": weight,
                "dimensions": {
                    "length": length,
                    "width": width,
                    "height": height
                    },
                "purchasable": True,
                "images": [{
                        "src": "https://www.revolutioncycle.com/wp-content/uploads/2015/06/Online-purchase-template1.jpg",
                        "position": 0
                    }]
            }
            return wcapi.post("products", data).json()['permalink']
        else:
            print('Payment for this order has already been sent.')
            return check[0]['permalink']

    def sendRequest(self):
        self.progress = QProgressBar()
        self.progressLabel = QLabel()
        self.progress.setMinimum(0)
        self.progress.setMaximum(100)
        self.progress.setTextVisible(True)
        self.wLayoutNotes.addWidget(self.progressLabel)
        self.wLayoutNotes.addWidget(self.progress)
        self.progress.show()
        self.progressLabel.show()

        self.progressLabel.setText('Building/Re-Sending Online Payment')
        self.progress.setValue(33)
        
        self.data = {
            'firstName':self.custFirstName.text(),
            'lastName':self.custLastName.text(),
            'email':self.custEmail.text(),
            'product':self.prodDesc.text(),
            'link':self.createWooProduct(
                self.custFirstName.text(), 
                self.custLastName.text(),
                self.orderNumber.text(),
                self.partPrice.text()
                ),
            'salesperson':self.salesRep.currentText(),
            'orderNo':int(self.orderNumber.text()),
            'backETA':'idk',
            'shipETA':'idk',
        }
        print(self.data)
        self.progressLabel.setText('Sending Email')
        self.progress.setValue(66)
        if isEmail(self.data['email']):
            sendEmail('request', self.data)
            self.progressLabel.setText('Email Sent!')
            self.progress.setValue(100)
            sleep(1)
            self.w.close()
            return
        else:
            self.progressLabel.setText('Error: Invalid Email Address Entered.')
            self.progress.setValue(0)
            return

    def sendPaymentRequest(self):
        self.progress.show()
        self.progressLabel.show()
        self.progressLabel.setText('Building/Re-Sending Online Payment')
        self.progress.setValue(33)

        self.data = {
            'firstName':self.custFirstName.text(),
            'lastName':self.custLastName.text(),
            'email':self.custEmail.text(),
            'product':self.productName.text(),
            'link':self.createWooProduct(
                self.custFirstName.text(), 
                self.custLastName.text(),
                self.layawayNumber.text(),
                self.layawaySubtotal.text()
                ),
            'salesperson':self.salesRep.currentText(),
            'orderNo':self.layawayNumber.text(),
            'backETA':'idk',
            'shipETA':'idk',
        }
        print(self.data)
        sendEmail('request', self.data)
        self.progress.setValue(100)
        ex = QMessageBox()
        ex.setText("Success: Payment Request has been created on our website and sent to "+self.custFirstName.text())
        ex.setWindowTitle("Payment Request Sent")
        ex.setIcon(QMessageBox().Information)
        ex.exec()
        self.w.close()
        return

    def closeRefresh(self):
        self.w.close()
        self.tableWidgetSO.clear()
        self.tableWidgetWC.clear()
        self.addOrdersLoop()
        self.addClaimsLoop()
        self.search.setText('')

    def createByContext(self):
        if self.tabs.currentIndex()==0:
            self.createSpecialOrder()
        elif self.tabs.currentIndex()==1:
            self.createOnlineOrder()
        elif self.tabs.currentIndex()==2:
            self.createWarrantyClaim()
        return

    def editByContext(self):
        if self.tabs.currentIndex()==0:
            self.editSpecialOrder()
        elif self.tabs.currentIndex()==2:
            self.editWarrantyClaim()
        return

    def deleteByContext(self):
        if self.tabs.currentIndex()==0:
            self.delete()
        elif self.tabs.currentIndex()==2:
            self.deleteClaimWarning()
        return

class newOrderWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.initUI()
    def initUI(self):
        return
    def warning(self):
        about = QMessageBox.about(self, 'Incomplete', "You're missing information! Please check all the feilds in red and make sure you've selected a Supplier and Sales Person")
        return 
