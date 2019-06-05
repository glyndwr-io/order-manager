#-ORDER MANAGER - SQL.py
#
#   This library handles all MariaDB/MySQL Interaction for Order Manager such as read,
#   write, and delete. Functions are named apropriatley.

import mysql.connector
from config import *

#-----General Operation Functions-------------------------------------------------------

def connect():
    cnx = mysql.connector.connect(
    user=sqlConfig['user'], 
    password=sqlConfig['password'], 
    host=sqlConfig['host'], 
    database=sqlConfig['database'])
    return cnx

def generateID():

    cnx = connect()

    query="SELECT MAX(objectID) FROM Orders"
    query2="SELECT MAX(objectID) FROM Claims"
    output =[]

    #Open Cursor for executing the query
    cursor = cnx.cursor()

    #Run the SELECT query
    cursor.execute(query)

    #DEBUG: Print Query output to command line
    for item in cursor:
        output.append(item)

    #Run the SELECT query
    cursor.execute(query2)

    #DEBUG: Print Query output to command line
    for item in cursor:
        output.append(item)

    #Tie up loose ends and return
    cursor.close()
    cnx.close()

    max=0
    for item in output:
        if item[0] != None:
            if item[0] >= max:
                max=item[0]
    if max == 0:
        return 1
    else:
        return max+1

def makeFakeOrders():
    for i in range(20):
        fakeOrder = orderTemplate
        orderTemplate['orderID']+=i
        writeOrder(fakeOrder)

def sanitizeInput(userInput):
    output = ''
    okSpecialChars = [46, 64, 95]
    if type(userInput) != type(''):
        return ''

    for item in userInput:
        if item in userInput:
            if ord(item) in range(48,58) or ord(item) in range(65,91) \
            or ord(item) in range(97,123) or ord(item) in okSpecialChars:
                output+=item
    return output

def performQuery(userInput):
    cnx = connect()
    
    output =[]

    #Open Cursor for executing the query
    cursor = cnx.cursor()

    #Run the user query
    cursor.execute(userInput)

    #DEBUG: Print Query output to command line
    for item in cursor:
        output.append(item)

    #Tie up loose ends and return
    cursor.close()
    cnx.close()
    return output

#-----Functions for Special Order Writing-----------------------------------------------

def writeOrder(dataOrder=orderTemplate):

    cnx = connect()

    if dataOrder['objectID'] == 0:
        dataOrder['objectID']=generateID()

    #Open Cursor for executing the query
    cursor = cnx.cursor()

    #The Query that we will execute
    addOrder = ("INSERT INTO Orders "
        "(customerFirstName, customerLastName, customerPhoneNo, customerEmail,"
        "productDesc, productPartNo, productSupplier, dateRequested, dateOrdered,"
        "orderID,orderStatus,orderDesc,paymentStatus,isWorkOrder,salesRep,"
        "objectID,price,weight,dimLength,dimWidth,dimHeight,qty)"
        " VALUES (%(customerFirstName)s, %(customerLastName)s, %(customerPhoneNo)s,"
        " %(customerEmail)s, %(productDesc)s, %(productPartNo)s, %(productSupplier)s,"
        " %(dateRequested)s, %(dateOrdered)s, %(orderID)s, %(orderStatus)s,"
        " %(orderDesc)s, %(paymentStatus)s, %(isWorkOrder)s, %(salesRep)s,"
        " %(objectID)s, %(price)s, %(weight)s, %(dimLength)s, %(dimWidth)s,"
        " %(dimHeight)s, %(qty)s);")

    #Write and commit changes to database
    cursor.execute(addOrder, dataOrder)
    cnx.commit()

    #Tie up loose ends and return
    cursor.close()
    cnx.close()
    return dataOrder['objectID']

def fetchOrders():

    cnx = connect()
    
    query="SELECT * FROM Orders"
    output =[]

    #Open Cursor for executing the query
    cursor = cnx.cursor()

    #Run the SELECT query
    cursor.execute(query)

    #DEBUG: Print Query output to command line
    for item in cursor:
        output.append(item)

    #Tie up loose ends and return
    cursor.close()
    cnx.close()
    return output

def fetchOrder(orderNo):

    cnx = connect()

    if orderNo == None:
        cnx.close()
        return
    
    query=("SELECT * FROM Orders WHERE objectID = "+str(orderNo))
    output=[]

    #Open Cursor for executing the query
    cursor = cnx.cursor()

    #Run the SELECT query
    cursor.execute(query)

    for item in cursor:
        output.append(item)

    #DEBUG: Print Query output to command line
    data = {
        'customerFirstName':output[0][0], #Type TEXT
        'customerLastName':output[0][1], #Type TEXT
        'customerPhoneNo':output[0][2], #Type BIGINT
        'customerEmail' :output[0][3], #Type TEXT
        'productDesc' :output[0][4], #Type TEXT
        'productPartNo' :output[0][5], #Type TEXT
        'productSupplier' :output[0][6], #Type TEXT
        'dateRequested' :output[0][7], #Type DATE
        'dateOrdered' :output[0][8], #Type DATE
        'orderID' :output[0][9], #Type BIGINT
        'orderStatus' :output[0][10], #Type TINYINT
        'orderDesc' :output[0][11], #Type Text
        'paymentStatus' :output[0][12], #Type TINTINT
        'isWorkOrder' :output[0][13], #Type BOOLEAN
        'salesRep':output[0][14], #Type TEXT
        'objectID':output[0][15], #Type INT
        'price':output[0][16], #Type FLOAT
        'weight':output[0][17], #Type INT
        'dimLength':output[0][18], #Type INT
        'dimWidth':output[0][19], #Type INT
        'dimHeight':output[0][20], #Type INT
        'qty':output[0][21], #Type TINYINT
        }

    #Tie up loose ends and return
    cursor.close()
    cnx.close()
    return data

def findOrder(searchText):

    cnx = connect()

    if searchText == None:
        cnx.close()
        return
    elif type(searchText) != type(''):
        cnx.close()
        return

    searchText=sanitizeInput(searchText)
    
    query=("SELECT * FROM Orders" 
        "   WHERE customerFirstName LIKE \'%"+searchText+"%\' "
        "   OR customerLastName LIKE \'%"+searchText+"%\' "
        "   OR customerPhoneNo LIKE \'%"+searchText+"%\' "
        "   OR customerEmail LIKE \'%"+searchText+"%\' "
        "   OR productDesc LIKE \'%"+searchText+"%\' "
        "   OR productPartNo LIKE \'%"+searchText+"%\' "
        "   OR orderDesc LIKE \'%"+searchText+"%\' "
        "   OR orderID LIKE \'%"+searchText+"%\' "
    )

    output=[]
    results=[]

    #Open Cursor for executing the query
    cursor = cnx.cursor()

    #Run the SELECT query
    cursor.execute(query)

    for item in cursor:
        output.append(item)

    #DEBUG: Print Query output to command line

    for i in range(len(output)):
        results.append({
            'customerFirstName':output[i][0], #Type TEXT
            'customerLastName':output[i][1], #Type TEXT
            'customerPhoneNo':output[i][2], #Type BIGINT
            'customerEmail' :output[i][3], #Type TEXT
            'productDesc' :output[i][4], #Type TEXT
            'productPartNo' :output[i][5], #Type TEXT
            'productSupplier' :output[i][6], #Type TEXT
            'dateRequested' :output[i][7], #Type DATE
            'dateOrdered' :output[i][8], #Type DATE
            'orderID' :output[i][9], #Type BIGINT
            'orderStatus' :output[i][10], #Type TINYINT
            'orderDesc' :output[i][11], #Type Text
            'paymentStatus' :output[i][12], #Type TINTINT
            'isWorkOrder' :output[i][13], #Type BOOLEAN
            'salesRep':output[i][14], #Type TEXT
            'objectID':output[i][15], #Type INT
            'price':output[i][16], #Type FLOAT
            'weight':output[i][17], #Type INT
            'dimLength':output[i][18], #Type INT
            'dimWidth':output[i][19], #Type INT
            'dimHeight':output[i][20], #Type INT
            'qty':output[0][21], #Type TINYINT
            })

    #Tie up loose ends and return
    cursor.close()
    cnx.close()
    return results

def filterOrders(filterName, filterValue):

    cnx = connect()

    if filterValue == None:
        cnx.close()
        return
    elif type(filterValue) != type(''):
        cnx.close()
        return

    filterValue=sanitizeInput(filterValue)
    
    query=("SELECT * FROM Orders" 
        "   WHERE "+filterName+" = "+filterValue
    )

    output=[]
    results=[]

    #Open Cursor for executing the query
    cursor = cnx.cursor()

    #Run the SELECT query
    cursor.execute(query)

    for item in cursor:
        output.append(item)

    #DEBUG: Print Query output to command line

    for i in range(len(output)):
        results.append({
            'customerFirstName':output[i][0], #Type TEXT
            'customerLastName':output[i][1], #Type TEXT
            'customerPhoneNo':output[i][2], #Type BIGINT
            'customerEmail' :output[i][3], #Type TEXT
            'productDesc' :output[i][4], #Type TEXT
            'productPartNo' :output[i][5], #Type TEXT
            'productSupplier' :output[i][6], #Type TEXT
            'dateRequested' :output[i][7], #Type DATE
            'dateOrdered' :output[i][8], #Type DATE
            'orderID' :output[i][9], #Type BIGINT
            'orderStatus' :output[i][10], #Type TINYINT
            'orderDesc' :output[i][11], #Type Text
            'paymentStatus' :output[i][12], #Type TINTINT
            'isWorkOrder' :output[i][13], #Type BOOLEAN
            'salesRep':output[i][14], #Type TEXT
            'objectID':output[i][15], #Type INT
            'price':output[i][16], #Type FLOAT
            'weight':output[i][17], #Type INT
            'dimLength':output[i][18], #Type INT
            'dimWidth':output[i][19], #Type INT
            'dimHeight':output[i][20], #Type INT
            'qty':output[0][21], #Type TINYINT
            })

    #Tie up loose ends and return
    cursor.close()
    cnx.close()
    return results

def deleteOrder(ID):
    cnx = connect()

    if ID == None:
        return

    #If ID is passed into function, then operate
    query = "DELETE FROM Orders WHERE objectID = "+str(ID)
 
    #Open Cursor for executing the query
    cursor = cnx.cursor()

    #Run and commit the DELETE query
    cursor.execute(query)
    cnx.commit()

    #Tie up loose ends and return
    cursor.close()
    cnx.close()
    return

def updateOrders(col1='customerFirstName', col2='customerLastName', 
    data=('Steve', 'Morris')):
    
    cnx = connect()
    
    query = "UPDATE Orders SET "+col1+" = %s WHERE "+col2+" = %s;"

    #Open Cursor for executing the query
    cursor = cnx.cursor()

    #Run and commit the DELETE query
    cursor.execute(query, data)
    cnx.commit()

    #Tie up loose ends and return
    cursor.close()
    cnx.close()
    return

#-----Functions for Warranty Claims----------------------------------------------------

def writeClaim(dataOrder=orderTemplate):

    cnx = connect()

    if dataOrder['objectID'] == 0:
        dataOrder['objectID']=generateID()

    #Open Cursor for executing the query
    cursor = cnx.cursor()

    #The Query that we will execute
    addOrder = ("INSERT INTO Claims "
        "(customerFirstName, customerLastName, customerPhoneNo, customerEmail,"
        "productDesc, productPartNo, productSupplier, dateRequested, dateOrdered,"
        "orderID,orderStatus,orderDesc,paymentStatus,isWorkOrder,salesRep,"
        "objectID,price,weight,dimLength,dimWidth,dimHeight,raNumber,probDesc,dateRecieved)"
        " VALUES (%(customerFirstName)s, %(customerLastName)s, %(customerPhoneNo)s,"
        " %(customerEmail)s, %(productDesc)s, %(productPartNo)s, %(productSupplier)s,"
        " %(dateRequested)s, %(dateOrdered)s, %(orderID)s, %(orderStatus)s,"
        " %(orderDesc)s, %(paymentStatus)s, %(isWorkOrder)s, %(salesRep)s,"
        " %(objectID)s, %(price)s, %(weight)s, %(dimLength)s, %(dimWidth)s,"
        " %(dimHeight)s, %(raNumber)s, %(probDesc)s, %(dateRecieved)s);")

    #Write and commit changes to database
    cursor.execute(addOrder, dataOrder)
    cnx.commit()

    #Tie up loose ends and return
    cursor.close()
    cnx.close()
    return dataOrder['objectID']

def fetchClaims():

    cnx = connect()
    
    query="SELECT * FROM Claims"
    output =[]

    #Open Cursor for executing the query
    cursor = cnx.cursor()

    #Run the SELECT query
    cursor.execute(query)

    #DEBUG: Print Query output to command line
    for item in cursor:
        output.append(item)

    #Tie up loose ends and return
    cursor.close()
    cnx.close()
    return output

def fetchClaim(claimNo):

    cnx = connect()

    if claimNo == None:
        cnx.close()
        return
    
    query=("SELECT * FROM Claims WHERE objectID = "+str(claimNo))
    output=[]

    #Open Cursor for executing the query
    cursor = cnx.cursor()

    #Run the SELECT query
    cursor.execute(query)

    for item in cursor:
        output.append(item)

    #DEBUG: Print Query output to command line
    data = {
        'customerFirstName':output[0][0], #Type TEXT
        'customerLastName':output[0][1], #Type TEXT
        'customerPhoneNo':output[0][2], #Type BIGINT
        'customerEmail' :output[0][3], #Type TEXT
        'productDesc' :output[0][4], #Type TEXT
        'productPartNo' :output[0][5], #Type TEXT
        'productSupplier' :output[0][6], #Type TEXT
        'dateRequested' :output[0][7], #Type DATE
        'dateOrdered' :output[0][8], #Type DATE
        'orderID' :output[0][9], #Type BIGINT
        'orderStatus' :output[0][10], #Type TINYINT
        'orderDesc' :output[0][11], #Type Text
        'paymentStatus' :output[0][12], #Type TINTINT
        'isWorkOrder' :output[0][13], #Type BOOLEAN
        'salesRep':output[0][14], #Type TEXT
        'objectID':output[0][15], #Type INT
        'price':output[0][16], #Type FLOAT
        'weight':output[0][17], #Type INT
        'dimLength':output[0][18], #Type INT
        'dimWidth':output[0][19], #Type INT
        'dimHeight':output[0][20], #Type INT
        'raNumber':output[0][21], #Type TEXT
        'probDesc':output[0][22], #Type TEXT
        'dateRecieved':output[0][23], #Type DATE
        }

    #Tie up loose ends and return
    cursor.close()
    cnx.close()
    return data

def deleteClaim(ID):
    cnx = connect()

    if ID == None:
        return

    #If ID is passed into function, then operate
    query = "DELETE FROM Claims WHERE objectID = "+str(ID)
 
    #Open Cursor for executing the query
    cursor = cnx.cursor()

    #Run and commit the DELETE query
    cursor.execute(query)
    cnx.commit()

    #Tie up loose ends and return
    cursor.close()
    cnx.close()
    return

def updateClaims(col1='customerFirstName', col2='customerLastName', 
    data=('Steve', 'Morris')):
    
    cnx = connect()
    
    query = "UPDATE Claims SET "+col1+" = %s WHERE "+col2+" = %s;"

    #Open Cursor for executing the query
    cursor = cnx.cursor()

    #Run and commit the DELETE query
    cursor.execute(query, data)
    cnx.commit()

    #Tie up loose ends and return
    cursor.close()
    cnx.close()
    return
