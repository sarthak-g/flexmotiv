from django import forms

class AccountTypeForm(forms.Form):
    c  = [("1","Main"),("2","BIRAC")]
    choices = forms.ChoiceField(choices=c, label="Choices")

class CSVFileForm(forms.Form):
    file = forms.FileField()
# class FormForUntagged(forms.Form):
