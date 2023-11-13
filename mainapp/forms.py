from django import forms

class ScraperForm(forms.Form):
    my_base_url = forms.URLField(label='Base URL')