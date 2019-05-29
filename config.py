from datetime import date

versionNumber = "v0.1.15"

sqlConfig = {
    'user':'', 
    'password':'', 
    'host':'', 
    'database':''
}

wcAPIConfig = {
    'url':"",
    'consumer_key':"",
    'consumer_secret':"",
    'wp_api':False,
    'version':""
}

wcAPILegacyConfig = {
    'url':"",
    'consumer_key':"",
    'consumer_secret':"",
    'wp_api':True,
    'version':"",
    'verify_ssl':True,
    'timeout':30,
}

emailConfig = {
    'username':'',
    'password':'',
}

orderTemplate = {
    'customerFirstName':'Foo', #Type TEXT
    'customerLastName':'Bar', #Type TEXT
    'customerPhoneNo':1234567890, #Type BIGINT
    'customerEmail' :'foo@bar.com', #Type TEXT
    'productDesc' :'Foo Bar', #Type TEXT
    'productPartNo' :'42069-01', #Type TEXT
    'productSupplier' :'ACME', #Type TEXT
    'dateRequested' :date(2018,11,26), #Type DATE
    'dateOrdered' :date(2018,11,26), #Type DATE
    'orderID' :65902, #Type BIGINT
    'orderStatus' :0, #Type TINYINT
    'orderDesc' :'ACME part for Foo Bar', #Type Text
    'paymentStatus' :1, #Type TINTINT
    'isWorkOrder' :False, #Type BOOLEAN
    'salesRep':'John Doe', #Type TEXT
    'objectID':0, #Type INT
    'price':123456.78, #Type FLOAT
    'weight':35, #Type INT
    'dimLength': 55, #Type INT
    'dimWidth':9, #Type INT
    'dimHeight':33, #Type INT
}

staffMembers = [
    '--Choose One--',
    '',
]

suppliers = [
    '--Choose One--',
    '',
]
