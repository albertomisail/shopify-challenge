from django import forms

class LoadBalanceForm(forms.Form):
    balance = forms.DecimalField()

class UploadForm(forms.Form):
    title = forms.CharField(max_length=200)
    image = forms.ImageField()
    price = forms.DecimalField()

class SearchForm(forms.Form):
    search = forms.CharField(max_length=200)
