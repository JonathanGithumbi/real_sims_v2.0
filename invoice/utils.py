from student.utils import generate_admission_number
from .models import Invoice
from fees_structure.models import FeesStructure
from student.models import Student
import datetime 
from datetime import datetime,timedelta

def generate_invoice_number(id):
    """Returns an invoice number in the format 'i+<id>.zfill(4)'"""
    return 'i'+str(id).zfill(4)

class InvoiceGenerationManager():
    """The purpose of this class is to create an ivoice for every student in the system.
        It can create an invoice for a student during registration, and also whenever a new term starts    
    """
    def get_term(date):
        pass

    def get_year(date):
        pass

    def create_invoice(self,student):
        self.student = Student.objects.get(pk=student.id)
        invoice = Invoice.objects.create(
            student = self.student,
            grade = self.student.current_grade,
            term = self.get_term(self.student.date_of_admission),
            year = self.get_year(self.student.date_of_admission),
        )
        invoice.save()
        invoice.invoice_number = generate_invoice_number(invoice.id)
        return invoice

        
    def create_invoice_at_registration(self,student):
        #after student.save() method
        #get the grade, term, year 
        # use grade term year to get the fees_structure
        # create invoice for each item

        


        pass

    def create_invoice_at_new_term(self,student):

        pass


