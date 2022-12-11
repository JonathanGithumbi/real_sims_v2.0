
from .models import Year, Term
from django.template.loader import render_to_string
from .forms import YearModelForm, TermModelForm
from django.http import JsonResponse
from bootstrap_modal_forms.generic import (
    BSModalCreateView,
    BSModalUpdateView,
    BSModalReadView,
    BSModalDeleteView
)
from django.urls import reverse_lazy
from django.views import generic


class YearListView(generic.ListView):
    model = Year
    template_name = 'year_list.html'
    context_object_name = 'year_list'


class YearCreateView(BSModalCreateView):
    template_name = 'academic_calendar/create_year.html'
    form_class = YearModelForm
    success_message = 'Success: Year was created'
    success_url = reverse_lazy('year_list')


class YearUpdateView(BSModalUpdateView):
    model = Year
    template_name = 'academic_calendar/update_year.html'
    form_class = YearModelForm
    success_message = 'Success: Year was updated'
    success_url = reverse_lazy('year_list')


class YearReadView(BSModalReadView):
    model = Year
    template_name = 'academic_calendar/read_year.html'


class YearDeleteView(BSModalDeleteView):
    model = Year
    template_name = 'academic_calendar/delete_year.html'
    success_message = 'Success: Year was created'
    success_url = reverse_lazy('year_list')


def years(request):
    data = dict()
    if request.method == 'GET':
        year_list = Year.objects.all()
        data['table'] = render_to_string(
            '_years_table.html',
            {'year_list': year_list},
            request=request
        )
        return JsonResponse(data)


class TermListView(generic.ListView):
    model = Term
    template_name = 'term_list.html'
    context_object_name = 'term_list'


class TermCreateView(BSModalCreateView):
    template_name = 'academic_calendar/create_term.html'
    form_class = TermModelForm
    success_message = 'Success: Term was created'
    success_url = reverse_lazy('term_list')


class TermUpdateView(BSModalUpdateView):
    model = Term
    template_name = 'academic_calendar/update_term.html'
    form_class = TermModelForm
    success_message = 'Success: Term was updated'
    success_url = reverse_lazy('term_list')


class TermReadView(BSModalReadView):
    model = Term
    template_name = 'academic_calendar/read_term.html'


class TermDeleteView(BSModalDeleteView):
    model = Term
    template_name = 'academic_calendar/delete_term.html'
    success_message = 'Success: Term was created'
    success_url = reverse_lazy('term_list')


def terms(request):
    data = dict()
    if request.method == 'GET':
        term_list = Term.objects.all()
        data['table'] = render_to_string(
            '_terms_table.html',
            {'term_list': term_list},
            request=request
        )
        return JsonResponse(data)
