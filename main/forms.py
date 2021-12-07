from django import forms
from .models import Document, Value


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('document',)


class ValueForm(forms.ModelForm):
    font_size = forms.IntegerField()
    cutoff_freq = forms.FloatField()
    decay_level = forms.IntegerField()

    class Meta:
        model = Value
        fields = ('font_size', 'cutoff_freq', 'decay_level')
