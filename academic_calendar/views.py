
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
from django.shortcuts import get_object_or_404


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

    template_name = 'term_list.html'
    context_object_name = 'term_list'

    # Add year to thte context data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["year"] = get_object_or_404(
            Year, pk=self.kwargs['year_pk'])
        return context

    def get_queryset(self):
        year_pk = int(self.kwargs['year_pk'])
        year = Year.objects.get(id=year_pk)
        return Term.objects.filter(year=year)


class TermCreateView(BSModalCreateView):
    template_name = 'academic_calendar/create_term.html'
    form_class = TermModelForm
    success_message = 'Success: Term was created'

    def get_form_kwargs(self):
        kwargs = super(TermCreateView, self).get_form_kwargs()
        year = Year.objects.get(pk=self.kwargs['year_pk'])
        kwargs.update({'year': year})
        return kwargs

    def get_success_url(self):
        return reverse_lazy('term_list', kwargs={'year_pk': self.kwargs['year_pk']})


class TermUpdateView(BSModalUpdateView):
    model = Term
    template_name = 'academic_calendar/update_term.html'
    form_class = TermModelForm
    success_message = 'Success: Term was updated'

    def get_form_kwargs(self):
        kwargs = super(TermUpdateView, self).get_form_kwargs()
        year = Year.objects.get(pk=self.kwargs['year_pk'])
        kwargs.update({'year': year})
        return kwargs

    def get_success_url(self):
        return reverse_lazy('term_list', kwargs={'year_pk': self.kwargs['year_pk']})


class TermReadView(BSModalReadView):
    model = Term
    template_name = 'academic_calendar/read_term.html'


class TermDeleteView(BSModalDeleteView):
    model = Term
    template_name = 'academic_calendar/delete_term.html'
    success_message = 'Success: Term was created'

    def get_success_url(self):
        return reverse_lazy('term_list', kwargs={'year_pk': self.kwargs['year_pk']})


def terms(request, year_pk):
    year = Year.objects.get(pk=year_pk)
    data = dict()
    if request.method == 'GET':
        term_list = Term.objects.filter(year=year)
        data['table'] = render_to_string(
            '_terms_table.html',
            {'term_list': term_list, 'year': year},
            request=request
        )
        return JsonResponse(data)


def load_terms(request):
    year_id = request.GET.get('year')
    terms = Term.objects.filter(year_id=year_id).order_by('term')
    from django.shortcuts import render
    return render(request, 'academic_calendar/term_dropdown_list_options.html', {'terms': terms})
