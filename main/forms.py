from django import forms
from .models import Document, Value


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('document',)


class ValueForm(forms.ModelForm):
    cutoff_freq = forms.FloatField()
    decay_level = forms.IntegerField()
    delta_F = forms.FloatField()
    Rp = forms.FloatField(required=False)
    Rs = forms.FloatField(required=False)

    class Meta:
        model = Value
        fields = ('cutoff_freq', 'decay_level', 'delta_F', 'Rp', 'Rs')
