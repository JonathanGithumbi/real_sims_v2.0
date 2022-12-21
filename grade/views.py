from .models import Grade
from django.template.loader import render_to_string
from .forms import GradeModelForm

from django.http import JsonResponse
from bootstrap_modal_forms.generic import (
    BSModalCreateView,
    BSModalUpdateView,
    BSModalReadView,
    BSModalDeleteView
)
from django.urls import reverse_lazy
from django.views import generic


class GradeListView(generic.ListView):
    model = Grade
    template_name = 'grade_list.html'
    context_object_name = 'grade_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_no_grades'] = Grade.objects.all().count()
        return context


class GradeCreateView(BSModalCreateView):
    template_name = 'grade/create_grade.html'
    form_class = GradeModelForm
    success_message = 'Success: Grade was created'
    success_url = reverse_lazy('grade_list')


class GradeUpdateView(BSModalUpdateView):
    model = Grade
    template_name = 'grade/update_grade.html'
    form_class = GradeModelForm
    success_message = 'Success: Grade was updated'
    success_url = reverse_lazy('grade_list')


class GradeReadView(BSModalReadView):
    model = Grade
    template_name = 'grade/read_grade.html'


class GradeDeleteView(BSModalDeleteView):
    model = Grade
    template_name = 'grade/delete_grade.html'
    success_message = 'Success: Grade was created'
    success_url = reverse_lazy('grade_list')


def grades(request):
    data = dict()
    if request.method == 'GET':
        grade_list = Grade.objects.all()
        data['table'] = render_to_string(
            '_grades_table.html',
            {'grade_list': grade_list},
            request=request
        )
        return JsonResponse(data)
