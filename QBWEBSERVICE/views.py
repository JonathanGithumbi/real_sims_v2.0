from django.shortcuts import render
from spyne.service import ServiceBase
from spyne.decorator import rpc
# Create your views here.


class QBWEBSERVICE(ServiceBase):

    # user code
    def authenticate(self):
        # return session token(ticket)
        # and "nvu" (invalid user)
        # or "none" (no requests)
        # or company name (QBFS)
        # or empty string(current company)

        # optionally and time to wait before next poll
        #optionally and minimumruneverynseconds
        pass

    def clientVersion(self):
        # return empty string to continue,
        # or return W:<warning sttring>
        # or return E:<error string>
        # or return O:<required QBWC version string>
        pass

    def closeConnection(self):
        pass

    def connectionError(self):
        pass

    def getLastError(self):
        # return "Noop" to pause QBWC for some seconds before retryin
        # return "Interactive mode" to request interactive mode
        # return any other string to display as an error string
        pass

    def receiveResponseXML(self):
        # process data and return a positive integer
        # indicates percentage of work completed, with 100="done"
        # return a negative integer to indicate an error
        pass

    def sendRequestXML(self):
        # authenticate callback
        # return empty string if no requests to send
        # return empty string for interactive mode
        # any other string must be qbXML request
        pass
