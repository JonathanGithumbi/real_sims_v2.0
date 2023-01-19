from django.core.management.base import BaseCommand
from student.models import Student


def Command(BaseCommand):
    help = "Creates student object from a .xlsx file"

    def add_arguments(self, parser):
        parser.add_argument('-f', '--file', type=str,
                            help=" String Path to he xlsx file containing the data")

    def register_student(self, first_name, last_name, status, grade):

        Student.objects.create(
            first_name=first_name,
            last_name=last_name,
            status=status,
            grade_admitted_to=grade
        )

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        from openpyxl import load_workbook
        wb = load_workbook(file_path)

        for row in wb.active.rows:
            data = [cell.value for cell in row]
        i = 0
        for student in data[1:]:
            print("processing {} out of {} records...".format(
                i+1, len(data[1:])))
            full_name = student[0]
            balance_brought_forward = student[1]
            grade = student[2]
            status = student[3]
            full_names_list = full_name.split(' ')
            first_name = full_names_list[0]
            last_name = full_names_list[-1]
