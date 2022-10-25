from core.celery import app

@app.task
def createCustomer():
    pass

@app.task
def readCustomer():
    pass

@app.task
def updateCustomer():
    pass

@app.task
def deleteCustomer():
    pass