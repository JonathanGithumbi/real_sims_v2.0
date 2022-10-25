from core.celery import app

@app.task
def createInvoice():
    pass

@app.task
def readInvoice():
    pass

@app.task
def updateInvoice():
    pass

@app.task
def deleteInvoice():
    pass


@app.task
def invoiceStudents():
    pass

@app.task
def unsubscribeStudents():
    pass

