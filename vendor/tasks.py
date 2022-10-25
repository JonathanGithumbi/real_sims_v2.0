from core.celery import app

@app.task
def createVendor():
    pass

@app.task
def readVendor():
    pass

@app.task
def updateVendor():
    pass

@app.task
def deleteVendor():
    pass

