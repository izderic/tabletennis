from django.forms.models import ModelForm

from .models import League


class LeagueForm(ModelForm):

    class Meta:
        model = League
        fields = ['name', 'num_of_sets', 'points_per_set', 'players']

    def __init__(self, *args, **kwargs):
        super(LeagueForm, self).__init__(*args, **kwargs)
        self.fields['players'].widget.attrs['style'] = 'height: 300px; width: 300px;'
        self.fields['players'].help_text = '<br /><i>Hold the Ctrl key to select multiple players.</i>'

    def save(self, commit=True, players=None):
        instance = super(LeagueForm, self).save(commit=False)
        instance.save(players=players)
        self.save_m2m()
