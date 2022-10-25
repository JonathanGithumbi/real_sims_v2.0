from core.celery import app

# crud operation tasks on expense object
@app.task
def readExpense():
    pass

@app.task
def createExpense():
    pass

@app.task
def updateExpense():
    pass

@app.task
def deleteExpense():
    pass
