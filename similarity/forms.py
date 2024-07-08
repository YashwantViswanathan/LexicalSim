from django import forms

class SentenceForm(forms.Form):
    sentence1 = forms.CharField(label='First Sentence', max_length=200)
    sentence2 = forms.CharField(label='Second Sentence', max_length=200)

