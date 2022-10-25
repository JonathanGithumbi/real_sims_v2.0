from core.celery import app

@app.task
def createBill():
    pass

@app.task
def editBill():
    pass

@app.task
def readBill():
    pass

@app.task
def deleteBill():
    pass

