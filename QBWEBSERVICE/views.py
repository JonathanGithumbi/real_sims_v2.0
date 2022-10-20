from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.views.decorators.csrf import csrf_exempt

from spyne.error import ResourceNotFoundError, ResourceAlreadyExistsError
from spyne.server.django import DjangoApplication
from spyne.model.primitive import Unicode, Integer
from spyne.model.complex import Iterable
from spyne.service import Service
from spyne.protocol.soap import Soap11
from spyne.application import Application
from spyne.decorator import rpc
from spyne.util.django import DjangoComplexModel, DjangoService
from spyne.protocol.http import HttpRpc
#from rpctest.core.models import FieldContainer


class QBWEBSERVICE(Service):

    # @rpc decorator passes a spyne.MethodContext instanc as first argumnt to the usr code
    # the Method Context holds all information about the current state of execution of a remote procedure call
    @rpc(Unicode, Unicode, _returns=Iterable(Unicode))
    def authenticate(ctx, username, password):
        # GOAL:authenticate the specified user,and specify the company to be used in the session
        # return session token(ticket)
        """
        #Log Samples
            string evLogTxt="WebMethod: authenticate() has been called by QBWebconnector" + "
            evLogTxt=evLogTxt+"Parameters received:
            evLogTxt=evLogTxt+"string strUserName = " + strUserName + "
            evLogTxt=evLogTxt+"string strPassword = " + strPassword + "
            evLogTxt=evLogTxt+"

            evLogTxt=evLogTxt+"
            evLogTxt=evLogTxt+"Return values: " + "
            authenticate 65
            (c) 2009 Intuit Inc. All rights reserved.
            evLogTxt=evLogTxt+"string[] authReturn[0] = " + authReturn[0].ToString() + "
            evLogTxt=evLogTxt+"string[] authReturn[1] = " + authReturn[1].ToString();
            logEvent(evLogTxt);
        """
        # and "nvu" (invalid user)
        # or "none" (no requests)
        # or company name (QBFS)
        # or empty string(current company)

        # optionally and time to wait before next poll
        #optionally and minimumruneverynseconds
        pass

    @rpc(Unicode, _returns=Unicode)
    def clientVersion(ctx, version):
        # Goal: evaluate the current web connnector version and reacti to it.
        """
        # Log Samples
        string evLogTxt="WebMethod: clientVersion() has been called " + 
        "by QBWebconnector" + "
        evLogTxt=evLogTxt+"Parameters received:
        evLogTxt=evLogTxt+"string strVersion = " + strVersion + "
        evLogTxt=evLogTxt+
        evLogTxt=evLogTxt+"QBWebConnector version = " + strVersion + "
        evLogTxt=evLogTxt+"Recommended Version = " + recommendedVersion.ToString() + "
        evLogTxt=evLogTxt+"Supported Min Version = " + supportedMinVersion.ToString() + "
        evLogTxt=evLogTxt+"SuppliedVersion = " + suppliedVersion.ToString()+
        evLogTxt=evLogTxt+"
        evLogTxt=evLogTxt+"Return values: " + "
        evLogTxt=evLogTxt+"string retVal = " + retVal;
        logEvent(evLogTxt)
        """
        # return empty string to continue,
        # or return W:<warning sttring>
        # or return E:<error string>
        # or return O:<required QBWC version string>
        pass

    @rpc(Unicode, _returns=Unicode)
    def closeConnection(ctx, ticket):
        """
        Log Samples
        string evLogTxt="WebMethod: closeConnection() has been called by QBWebconnector" + "
        evLogTxt=evLogTxt+"Parameters received:
        evLogTxt=evLogTxt+"string ticket = " + ticket + "
        evLogTxt=evLogTxt+"
        string retVal=null;
        retVal="OK";
        evLogTxt=evLogTxt+"
        evLogTxt=evLogTxt+"Return values: " + "
        evLogTxt=evLogTxt+"string retVal= " + retVal + "
        logEvent(evLogTxt)
        """
        # web service is informed that the web connector is finished with the update session
        # the ticket is the session token your, web service returned to the web connnector's authenticate call,
        # return a string that you want the web connector to display to the user showing the status of the web service action on behalf of your user
        # e.g "Data Synced: 100%"
        pass

    @rpc(Unicode, Unicode, Unicode, _returns=Unicode)
    def connectionError(ctx, ticked, hresult, message):
        # tells web service about an error the web connector encountered in its attempt to connect to quickbbooks
        """
        #log samples
        evLogTxt=evLogTxt+"Parameters received:
        evLogTxt=evLogTxt+"string ticket = " + ticket + "
        evLogTxt=evLogTxt+"string hresult = " + hresult + "
        evLogTxt=evLogTxt+"string message = " + message + "
        evLogTxt=evLogTxt+"
        string retVal=null;
        // 0x80040400 - QuickBooks found an error when parsing the provided XML text stream. 
        const string QB_ERROR_WHEN_PARSING="0x80040400"; 
        // 0x80040401 - Could not access QuickBooks. 
        const string QB_COULDNT_ACCESS_QB="0x80040401";
        // 0x80040402 - Unexpected error. Check the qbsdklog.txt file
        const string QB_UNEXPECTED_ERROR="0x80040402";
        // Add more as you need...
        if(hresult.Trim().Equals(QB_ERROR_WHEN_PARSING)){
        evLogTxt=evLogTxt+ "HRESULT = " + hresult + "
        evLogTxt=evLogTxt+ "Message = " + message + "
        retVal = "DONE";
        }
        else if(hresult.Trim().Equals(QB_COULDNT_ACCESS_QB)){
        evLogTxt=evLogTxt+ "HRESULT = " + hresult + "
        evLogTxt=evLogTxt+ "Message = " + message + "
        retVal = "DONE";
        }
        else if(hresult.Trim().Equals(QB_UNEXPECTED_ERROR)){
        evLogTxt=evLogTxt+ "HRESULT = " + hresult + "
        evLogTxt=evLogTxt+ "Message = " + message + "
        retVal = "DONE";
        }
        else { 
        // Depending on various hresults return different value 
        // Try again with this company file
        evLogTxt=evLogTxt+ "HRESULT = " + hresult + "
        evLogTxt=evLogTxt+ "Message = " + message + "
        retVal = "";
        }
        evLogTxt=evLogTxt+"
        evLogTxt=evLogTxt+"Return values: " + "
        evLogTxt=evLogTxt+"string retVal = " + retVal + "
        logEvent(evLogTxt);
        return retVal
        """
        pass

    @rpc(Unicode, Unicode, _returns=Unicode)
    def getInteractiveURL(ctx, wcTicket, sessionID):
        # Lets your web service tell WBQC where to get the web page to display in the browser at start of interactive mode
        # return a message string containing the URL of the web page you want opened in the browser
        pass

    @rpc(Unicode, _returns=Unicode)
    def getLastError(ctx, ticket):
        """
        #log samples
        string evLogTxt="WebMethod: getLastError() has been called by QBWebconnector" + "
        evLogTxt=evLogTxt+"Parameters received:
        evLogTxt=evLogTxt+"string ticket = " + ticket + "
        evLogTxt=evLogTxt+"
        evLogTxt=evLogTxt+"
        evLogTxt=evLogTxt+"Return values: " + "
        evLogTxt=evLogTxt+"string retVal= " + retVal + "
        logEvent(evLogTxt);
        """
        # allows your web service to return the last web service error,normally for display to the user b4 causing the update action to stop
        # returna message string describing the problem and any other info the user shud see
        # return "Noop" to pause QBWC for some seconds before retryin
        # return "Interactive mode" to request interactive mode
        # return any other string to display as an error string
        # allows your web service to return the last web service error,normally for display to the user before causing the update action to stop
        pass

    @rpc(Unicode, _returns=Unicode)
    def getServerVersion(ctx, ticket):
        # provides a way for web-seervice to notify QBWC of its version.
        # version shows up in the more information pop-up dialog in QBWC
        # return a message string describing the server version
        pass

    @rpc(Unicode, _returns=Unicode)
    def interactiveDone(ctx, wcTicket):
        # allows web service to indicate to QBWC that it is done with interactive mode
        # return a message string with the value "Done" when the interactive session is over
        pass

    @rpc(Unicode, Unicode, _returns=Unicode)
    def interactiveRejected(ctx, wcTicket, reason):
        # allows the web service to take alternative axtion when the interactive session it requested was rejected by the user or by timeout in the absence of the user
        # return a message string to be displayed
        pass

    @rpc(Unicode, Unicode, Unicode, Unicode, _returns=Integer)
    def receiveResponseXML(ctx, ticket, response, hresult, message):
        # returns the data request response from quickbooks
        # response contains the qbXML response from Quickbooks
        # hresult and message could b returned as a result of certain errors that could occur whenQuickbooks sends requests,to the QB request processor,
        # if no error occurs, hresult and message will be empty strings
        # return a +ve integer less that 100 represents a percentage of work completed
        # return a -ve value meaning that an error has occurred and the web conector responds with a getLastError call.
        """
        when the web connector gets a responsse from quickbooks it sends the response to the web service through receiveResponseXML
        the job of this methos is to process the message and return a message
        A positive integer if you want it to serve as the 
        estimated percent complete for the session, a negative integer if you want to indicate to the 
        web connector that an error has occurred.

        log samples
        string evLogTxt="WebMethod: receiveResponseXML() called by QBWebconnector" + "
        evLogTxt=evLogTxt+"Parameters received:
        evLogTxt=evLogTxt+"string ticket = " + ticket + "
        evLogTxt=evLogTxt+"string response = " + response + "
        evLogTxt=evLogTxt+"string hresult = " + hresult + "
        evLogTxt=evLogTxt+"string message = " + message + "
        evLogTxt=evLogTxt+"
        evLogTxt=evLogTxt+"
        evLogTxt=evLogTxt+"Return values: " + "
        receiveResponseXML 79
        (c) 2009 Intuit Inc. All rights reserved.
        evLogTxt=evLogTxt+"int retVal= " + retVal.ToString() + "
        logEvent(evLogTxt);
        """
        # process data and return a positive integer
        # indicates percentage of work completed, with 100="done"
        # return a negative integer to indicate an error
        pass

    @rpc(Unicode, Unicode, Unicode, Integer, Integer, _returns=Unicode)
    def sendRequestXML(ctx, ticket, HCPResponse, CompanyFileName, qbXMLMajorVers, qbXMLMinorVers):
        # this is the web connector's invitation to the web service to send a request
        # this will check if the request queue is populated and start dending them
        """
        log samples
        string evLogTxt="WebMethod: sendRequestXML() has been called by QBWebconnector" + "
        evLogTxt=evLogTxt+"Parameters received:
        evLogTxt=evLogTxt+"string ticket = " + ticket + "
        evLogTxt=evLogTxt+"string strHCPResponse = " + strHCPResponse + "
        evLogTxt=evLogTxt+"string strCompanyFileName = " + strCompanyFileName + "
        evLogTxt=evLogTxt+"string Country = " + Country + "
        evLogTxt=evLogTxt+"int qbXMLMajorVers = " + qbXMLMajorVers.ToString() + "
        evLogTxt=evLogTxt+"int qbXMLMinorVers = " + qbXMLMinorVers.ToString() + "
        evLogTxt=evLogTxt+"
        evLogTxt=evLogTxt+"
        evLogTxt=evLogTxt+"Return values: " + "
        evLogTxt=evLogTxt+"string request = " + request + "
        logEvent(evLogTxt);
        """
        # authenticate callback
        # return empty string if no requests to send
        # return empty string for interactive mode
        # any other string must be qbXML request
        pass


app = Application([QBWEBSERVICE],
                  "http://developer.intuit.com/",
                  in_protocol=Soap11(validator='lxml'),
                  out_protocol=Soap11())

qb_web_service = csrf_exempt(DjangoApplication(app))
