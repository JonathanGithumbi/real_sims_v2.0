from .models import Grade
from bootstrap_modal_forms.forms import BSModalModelForm


class GradeModelForm(BSModalModelForm):
    class Meta:
        model = Grade
        fields = ['title']
