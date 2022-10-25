from core.celery import app

@app.task
def createPayment():
    pass

@app.task
def readPayment():
    pass

@app.task
def updatePayment():
    pass

@app.task
def deletePayment():
    pass

