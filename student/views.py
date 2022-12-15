from .models import Student
from django.template.loader import render_to_string
from .forms import StudentModelForm
from django.http import JsonResponse
from bootstrap_modal_forms.generic import (
    BSModalCreateView,
    BSModalUpdateView,
    BSModalReadView,
    BSModalDeleteView
)
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from academic_calendar.CalendarManager import CalendarManager
from invoice.InvoiceManager import InvoiceManager


class StudentListView(generic.ListView):
    model = Student
    template_name = 'student_list.html'
    context_object_name = 'student_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['students_total'] = Student.objects.count()
        return context


class StudentCreateView(BSModalCreateView):
    template_name = 'student/create_student.html'
    form_class = StudentModelForm
    success_message = 'Success: Student was created'
    success_url = reverse_lazy('student_list')


class StudentUpdateView(BSModalUpdateView):
    model = Student
    template_name = 'student/update_student.html'
    form_class = StudentModelForm
    success_message = 'Success: Student was updated'
    success_url = reverse_lazy('student_list')


class StudentReadView(BSModalReadView):
    model = Student
    template_name = 'student/read_student.html'


class StudentDeleteView(BSModalDeleteView):
    model = Student
    template_name = 'student/delete_student.html'
    success_message = 'Success: Student was created'
    success_url = reverse_lazy('student_list')


def students(request):
    data = dict()
    if request.method == 'GET':
        student_list = Student.objects.all()
        data['table'] = render_to_string(
            '_students_table.html',
            {'student_list': student_list},
            request=request
        )
        return JsonResponse(data)


def deactivate_student(request, student):
    student.active = False
    student.save()
    from django.shortcuts import redirect
    return redirect('student_list')
