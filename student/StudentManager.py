from academic_calendar.models import Year
from invoice.InvoiceManager import InvoiceManager
from academic_calendar.CalendarManager import CalendarManager

class StudentManager():
    """The student manager is responsible for managing the state of the Student """

    def register_student(self, student):
        # set the current grade
        student.current_grade = student.grade_admitted_to

        # Set year and term
        calendar_manager = CalendarManager()
        student.year_admitted = calendar_manager.get_year(student.date_of_admission)
        student.term_admitted = calendar_manager.get_term(student.date_of_admission)
        student.curent_year = student.year_admitted
        student.current_term = student.term_admitted
        # save the student to the database
        student.save()

        # invoice the student for the current term
        invoice_manager = InvoiceManager()
        invoice_manager.invoice_new_student(student)

        return student

    def inactivate_student(self):
        pass

    def edit_student(self, id):
        pass

    def retrieve_student(self, id):
        pass
