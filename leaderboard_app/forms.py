# forms.py
from django import forms
from .models import Competitor
from django.contrib.auth.models import User

class CompetitorAdminForm(forms.ModelForm):
    class Meta:
        model = Competitor
        fields = '__all__'
        widgets = {
            'laps': forms.TextInput (attrs = {'class': 'form-control form-control-sm'}),
        }

    def clean_laps(self):
        laps_str = self.cleaned_data['laps']
        if laps_str is "":
            try:
                laps = []
                return laps
            except ValueError:
                pass
        
        try:
            laps = [float(laps_str)]
            return laps
        except ValueError:
            pass
        try:
            laps = [float(x) for x in laps_str.split(',')]
            return laps
        except ValueError:
            pass
        try:
            laps = [float(x) for x in laps_str[1:-1].split(',')]
        except ValueError:
            raise forms.ValidationError("Invalid list of floats")
        return laps
    
class AddLapScoreForm(forms.Form):
  user = forms.ModelChoiceField(queryset=User.objects.all(), label="Competitor")
  lap_score = forms.FloatField(label="Lap Score")