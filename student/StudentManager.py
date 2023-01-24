from invoice.InvoiceManager import InvoiceManager
from academic_calendar.CalendarManager import CalendarManager
from invoice.models import BalanceTable
from django.shortcuts import get_object_or_404

class StudentManager():
    """The registered_student manager is responsible for managing the state of the Student """

    



    def register_student(self, registration_form):
        """Takes a registration form and gives you a registered_student"""
        # get student object
        registered_student = registration_form.save(commit=False)
        # set the current grade
        registered_student.current_grade = registered_student.grade_admitted_to
        # Set year and term
        calendar_manager = CalendarManager()
        registered_student.year_admitted = calendar_manager.get_year(
            registered_student.date_of_admission)
        print(registered_student.year_admitted)
        registered_student.term_admitted = calendar_manager.get_term(
            registered_student.date_of_admission)
        registered_student.current_year = registered_student.year_admitted
        print(registered_student.year_admitted)
        registered_student.current_term = registered_student.term_admitted
        # save the registered_student to the database
        registered_student.save()

        # invoice the registered_student for the current term
        invoice_manager = InvoiceManager()
        invoice_manager.invoice_new_student(registered_student)

        return registered_student

    def inactivate_student(self, student):
        student.active = False
        student.save(update_fields=['active'])
        return True

    def edit_student(self, form):
        if form.has_changed():
            student_object = form.save()

            invoice_manager = InvoiceManager()

            # Subscribing/unsubscribing a student to lunch/transport
            if 'lunch' in form.changed_data:
                if student_object.lunch == True:
                    invoice_manager.invoice_student_lunch(student_object)
                else:
                    invoice_manager.uninvoice_student_lunch(student_object)

            if 'transport' in form.changed_data:

                if student_object.transport == True:
                    invoice_manager.invoice_student_transport(student_object)
                else:
                    invoice_manager.uninvoice_student_transport(student_object)

            return True
        else:
            return False

    def delete_student(self, student):
        # What happends when you delete a student who has overpaid an invoice
        student.visible = False
        student.active = False
        student.save(update_fields=['visible', 'active'])
        return True

    def retrieve_student(self, id):
        pass

    def get_fees_balance(self, student):
        try:
            bal_rec = BalanceTable.objects.get(student=student)
        except:
            return None
        else:
            return bal_rec.balance
