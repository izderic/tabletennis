from django.forms.models import ModelForm

from .models import League


class LeagueForm(ModelForm):

    class Meta:
        model = League
        fields = ['name', 'num_of_sets', 'points_per_set', 'players']

    def __init__(self, *args, **kwargs):
        super(LeagueForm, self).__init__(*args, **kwargs)
        self.fields['players'].widget.attrs['style'] = 'height: 100px;'
        self.fields['players'].help_text = '<br /><i>Hold the Ctrl key to select multiple players.</i>'
