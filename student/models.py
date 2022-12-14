
from django.db import models

from grade.models import Grade

from academic_calendar.models import Year, Term


class AdmissionNumber(models.Model):
    """Generates the unformatted admission number"""
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id


class Student(models.Model):
    """this model represents a student enrolled in school"""

    class Meta:
        ordering = ['-date_of_admission']
    first_name = models.CharField(max_length=255, blank=True)
    middle_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    grade_admitted_to = models.ForeignKey(
        Grade, on_delete=models.CASCADE, related_name='grade_admitted_to')
    current_grade = models.ForeignKey(
        Grade, on_delete=models.CASCADE, blank=True, null=True)
    date_of_admission = models.DateField(auto_now_add=True, blank=True)
    year_admitted = models.ForeignKey(
        Year, on_delete=models.CASCADE, null=True, blank=True)
    term_admitted = models.ForeignKey(
        Term, on_delete=models.CASCADE, null=True, blank=True)
    current_term = models.ForeignKey(
        Term, on_delete=models.CASCADE, related_name='current_term', null=True, blank=True)
    current_year = models.ForeignKey(
        Year, on_delete=models.CASCADE, related_name='current_year', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    contact1_name = models.CharField(max_length=255, blank=True)
    contact1_number = models.CharField(max_length=255, blank=True)
    contact2_name = models.CharField(max_length=255, blank=True)
    contact2_number = models.CharField(
        max_length=255, blank=True)

    # This active flag defines whether or not the student gets  invoiced
    active = models.BooleanField(null=True, default=True, blank=True)

    # This visible flag will determing whether the student is visible; an alternative to deleting data
    visible = models.BooleanField(null=True, default=True, blank=True)

    # optionals
    lunch = models.BooleanField(default=False, blank=True)
    transport = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}"

    def get_fees_balance(self):
        from student.StudentManager import StudentManager
        man = StudentManager()
        return man.get_fees_balance(self)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("student_profile", kwargs={"student_id": self.id})

    def format_adm_no(self):
        return 's' + str(self.admission_number).zfill(4)

    def get_items(self):
        """These are the compulsory recurring items for continuing students"""
        items = ['Tuition', 'Computer Lessons']

        return items

    def student_is_upper_class(self):
        LOWER_CLASSES = ['Grade 1', 'Grade 2', 'Grade 3',
                         'Pre Primary 1', 'Pre Primary 2', 'Play Group']
        if self.current_grade.title in LOWER_CLASSES:
            return False
        else:
            return True
