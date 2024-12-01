# ravintolat/forms.py
from django import forms
from .models import Arvostelu

class ArvosteluForm(forms.ModelForm):
    class Meta:
        model = Arvostelu
        fields = ['tähdet', 'kommentti']
        labels = {
            'tähdet': 'Tähtien määrä',
            'kommentti': 'Kommentti',
        }
        widgets = {
            'tähdet': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'kommentti': forms.Textarea(attrs={'rows': 4}),
        }
