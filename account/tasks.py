from core.celery import app
import xml.etree.ElementTree as ET
"""
These methods will take in variable data and sew them into the qbXML docs
The methods in the tasks files will return qbXML required to record data"""


@app.task
def createAccount(self):
    tree = ET.parse('qbxml/legacy/AccountAddRq.xml')
    root = tree.getroot(tree)

    # Modify root attributes with user entered data
    AccountAddRq = root.find('QBXMLMsgsRq/AccountAddRq')
    AccountAddRq_requestID = AccountAddRq.attrib['requestID']
    name_element = root.find('QBXMLMsgsRq/AccountAddRq/AccountAdd/Name')

    request_string = ET.tostring(root, encoding='utf8').decode('utf8')

    return request_string


@app.task
def editAccount():
    pass


@app.task
def readAccount():
    pass


@app.task
def deleteAccount():
    pass
