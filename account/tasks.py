from core.celery import app
"""
These methods will take in variable data and sew them into the qbXML docs
The methods in the tasks files will return qbXML required to record data"""

@app.task
def createAccount():
    pass

@app.task
def editAccount():
    pass

@app.task
def readAccount():
    pass

@app.task
def deleteAccount():
    pass
