from celery import shared_task
import xml.etree.ElementTree as ET


@shared_task()
def createCustomer(self):
    tree = ET.parse('qbxml/legacy/CustomerAddRq.xml')
    root = tree.getroot(tree)

    # Modify root attributes with user entered data
    CustomerAddRq = root.find('QBXMLMsgsRq/CustomerAddRq')
    CustomerAddRq_requestID = CustomerAddRq.attrib['requestID']
    name_element = root.find('QBXMLMsgsRq/CustomerAddRq/CustomerAdd/Name')
    phone_element = root.find('QBXMLMsgsRq/CustomerAddRq/CustomerAdd/Phone')
    alt_phone_element = root.find('QBXMLMsgsRq/CustomerAddRq/CustomerAdd/AltPhone')
    CustomerAddRq_requestID.text = 'fefrygy34534v5jhg53'  # random for now
    name_element.text = self.first_name+self.middle_name+self.last_name
    phone_element.text = self.primary_contact_phone_number
    alt_phone_element.self = self.secondary_contact_phone_number

    request_string = ET.tostring(root, encoding='utf8').decode('utf8')

    return request_string


@app.task
def readCustomer():
    pass


@app.task
def updateCustomer():
    pass


@app.task
def deleteCustomer():
    pass
