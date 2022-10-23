#the tasks  will be functions that sendRequestXML() will call to generate requests for quickbooks,
#the task will therefore return the qbXML strings needed for any given operation to be performed in quickbooks,
#e.g if createNewCustomer() task is queued in the views,when sendRequestXML is called, createNewCustomer() task is dequeued and sent to 
#quickbooks

