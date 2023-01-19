
import openpyxl
from grade.models import Grade


def load_data(path):
    """
        Returns a list of all the data contained in  a given .xlsx files
        """

    wb = openpyxl.load_workbook(path)

    sheets = wb.sheetnames

    # create an empty list to store all the rows
    rows_list = []

    for sheet in sheets:
        current_sheet = wb[sheet]

        # iterate over the rows in the sheet
        for row in range(1, current_sheet.max_row + 1):
            # create an empty list to store the contents of the row
            row_list = []

            # iterate over the columns in the sheet
            for col in range(1, current_sheet.max_column + 1):
                # append the value in the cell to the list
                row_list.append(current_sheet.cell(row, col).value)

            # append the row list to the rows list
            rows_list.append(row_list)

    return rows_list


def parse_row(row):
    """Returns a dictionary containing key/value pairs"""

    full_names = row[0]
    balance_brought_forward = row[1]
    grade = row[2]
    active = row[3]

    full_names_list = full_names.split(' ')
    first_name = full_names_list[0]
    last_name = full_names_list[-1]
    balance_brought_forward = int(balance_brought_forward)
    grade = Grade.objects.get(title=grade)
    if active == 'TRUE' or active == 'True':
        status = True
        active = bool(status)
    if active == 'FALSE' or active == 'False':
        status = False
        active = bool(status)

    my_obj = {
        'first_name': first_name,
        'last_name': last_name,
        'balance_brought_forward': balance_brought_forward,
        'grade': grade,
        'active': active
    }
    return my_obj


def register_students(my_obj):
    from student.models import Student
    print("Registering: {}".format(my_obj['first_name']))
    Student.objects.create(
        first_name=my_obj['first_name'],
        last_name=my_obj['last_name'],
        grade_admitted_to=my_obj['grade'],
        active=my_obj['active']
    )
    print("Complete.")
    return True
