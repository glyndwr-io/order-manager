import email
import smtplib
import os
from config import *

scriptDir = os.path.dirname(__file__)

default = {
    'firstName':'Foo',
    'lastName':'Bar',
    'email':'foo@bar.com',
    'product':'ACME Part',
    'link':'https://morris.glyndwr.io/',
    'salesperson':'John Doe',
    'orderNo':'55634',
    'backETA':'idk',
    'shipETA':'idk',
}

def readTemplate(template):
    if template == 'request':
        relPath = "Email Templates/online_payment_request.html"
    elif template == 'backordered':
        relPath = "Email Templates/special_order_backordered.html"
    elif template == 'notAvailable':
        relPath = "Email Templates/special_order_not_available.html"
    elif template == 'ordered':
        relPath = "Email Templates/special_order_ordered.html"
    elif template == 'received':
        relPath = "Email Templates/special_order_recieved.html"
    else:
        return
    with open(os.path.join(scriptDir, relPath), 'r') as html:
        data = html.read()
    return data

def sendEmail(template, info=default):
    
    msg_header = ('From: [Store Name] [Store Eamil]\n'
             'To: '+info['firstName']+" "+info['lastName']+' <'+info['email']+'>'
             'MIME-Version: 1.0\n'
             'Content-type: text/html\n'
             'Subject: Online Payment Request from [Store Name]\n')
    title = 'Hello '+info['firstName']
    
    msg_content = readTemplate(template)
    if msg_content == None:
        return
    msg_content = msg_content.replace('[CUSTOMER FIRST NAME]', info['firstName'])
    msg_content = msg_content.replace('[PRODUCT NAME HERE]', info['product'])
    msg_content = msg_content.replace('[SALESPERSON]', info['salesperson'])
    msg_content = msg_content.replace('[PRODUCT LINK]', info['link'])
    msg_content = msg_content.replace('[ORDER NUMBER]', info['orderNo'])
   
    msg = (''.join([msg_header, msg_content])).encode()
    
    server = smtplib.SMTP_SSL('mail.hover.com', 465) #
    server.ehlo()
    #server.starttls()
    server.ehlo()
    server.login(emailConfig['username'], emailConfig['password'])
    
    server.sendmail(emailConfig['username'], info['email'], msg)
    
    server.quit()

def isEmail(email):
    try:
        str(email)
        
        atIndex = 0
        dotIndex = 0
        for i in range(len(email)):
            if email[i] == '@':
                atIndex = i
            elif email[i] == '.':
                dotIndex = i
        if dotIndex == 0 or atIndex == 0:
            return False
        elif dotIndex < atIndex:
            return False
        return True
    except:
        return False