from core.celery import app


@app.task
def createBillPayment():
    pass

@app.task
def readBillPayment():
    pass

@app.task
def updateBillPayment():
    pass

@app.task
def deleteBillPayment():
    pass
